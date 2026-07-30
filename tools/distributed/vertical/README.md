# AutoDiCE — AlexNet Vertical Partition Example

This example demonstrates vertical (layer-wise) partitioning of AlexNet across two CPU nodes using AutoDiCE, ncnn, and MPI.

## Overview

The model ([BVLC AlexNet ONNX](https://github.com/onnx/models/tree/main/validated/vision/classification/alexnet), `bvlcalexnet-9.onnx`) is split at the `fc6` layer boundary into two sub-models:

| Rank | Node key | Layers |
|------|----------|--------|
| 0 | `lenovo_cpu0` | `conv1` → `fc6_2` (conv, norm, pool, first FC) |
| 1 | `lenovo_cpu1` | `fc6_3` → `prob_1` (remaining FC + softmax) |

The intermediate tensor `fc6_2` is sent from rank 0 to rank 1 via MPI.

```
Input image
    │
    ▼
[lenovo_cpu0]  conv1 → pool → conv2 → pool → conv3-5 → pool → fc6 (partial)
    │  fc6_2 (MPI_Isend)
    ▼
[lenovo_cpu1]  fc6 (rest) → fc7 → fc8 → softmax → Top-3 prediction
```

## Prerequisites

- Docker

No other local dependencies are required — the image bundles everything (CMake, OpenMPI, OpenCV, ncnn, Python + onnx/numpy/psutil).

**Models are not part of the image.** `.dockerignore` excludes `models/` and `out/`, so
the image ships no weights and one image serves any model. Mount `models/` on every run —
without it the pipeline stops immediately with `No model found`.

**Inputs and outputs are separate directories:**

| Directory | Direction | Contents |
|-----------|-----------|----------|
| `models/` | read only | The ONNX networks you want to split. Never written to — mount it `:ro`. |
| `out/` | written | Everything generated: sub-models, ncnn weights, `rankfile`, `multinode.cpp`, the binary. |

Because nothing generated is ever written into `models/`, model selection stays
unambiguous no matter how many times you run or what you rename.

## Quick Start

Two shorthands used below — paste them into your shell, or write the paths out in full:

```bash
L=$(pwd)/tools/distributed/vertical            # on your machine
V=/autodice/tools/distributed/vertical         # inside the container
```

### 1. Fetch the model

The ONNX weights are not in this repository — download them into `models/` (≈233 MB):

```bash
mkdir -p $L/models
curl -L -o $L/models/bvlcalexnet-9.onnx \
  https://github.com/onnx/models/raw/main/validated/vision/classification/alexnet/model/bvlcalexnet-9.onnx
```

### 2. Build the Docker image

From the repository root:

```bash
docker build -t autodice .
```

### 3. Run the splitting

```bash
docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out \
  autodice python3 interface.py
```

This produces the following files inside `out/`:

| File | Description |
|------|-------------|
| `lenovo_cpu0.onnx` | Sub-model for rank 0 |
| `lenovo_cpu1.onnx` | Sub-model for rank 1 |
| `lenovo_cpu0.{param,bin}` | ncnn weights for rank 0 |
| `lenovo_cpu1.{param,bin}` | ncnn weights for rank 1 |
| `receiver.json` | Which rank receives which tensor and from whom |
| `sender.json` | Which rank sends which tensor and to whom |
| `rankfile` | MPI rank-to-slot mapping |
| `hostfile` | MPI hostfile |
| `multinode.cpp` | Auto-generated C++ inference engine |
| `format_*.onnx` | Normalised copy of the input model |

### 4. Run the full pipeline (split + compile + infer)

The default Docker `CMD` runs `run.sh`, which performs all steps end-to-end:

```bash
docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out autodice
```

The `out` mount is optional — leave it off and the results are discarded with the
container.

`run.sh` does the following:
1. Runs `interface.py` — splits the ONNX model and generates `multinode.cpp`
2. Converts sub-models to ncnn format via `onnx2ncnn`
3. Recompiles the project to build the `multinode` binary
4. Launches `mpirun` with one rank per line of the generated `rankfile`

Expected output (top-3 ImageNet classes for the bundled dog photo):

```
215 = 0.589278
207 = 0.127041
213 = 0.103414
 Brittany spaniel
 golden retriever
 Irish setter, red setter
```

To poke at the pipeline by hand instead, start an interactive shell:

```bash
docker run --rm -it -v $L/models:$V/models:ro -v $L/out:$V/out autodice bash
```

Then inside the container:

```bash
cd /autodice/tools/distributed/vertical/out
mpirun --allow-run-as-root --oversubscribe -np 2 -rf rankfile ./multinode dog.jpg
```

`--allow-run-as-root` is needed because the container runs as root; OpenMPI otherwise
refuses to launch. Expect a `failed to bind memory` warning — containers cannot bind
memory to a NUMA node. It is harmless and CPU pinning still applies; the only way to
silence it is `--bind-to none`, which discards the pinning.

## Cleaning Up Between Runs

Nothing to do. `--rm` removes the container when `run.sh` finishes, and the mount is a
bind mount of a host directory, not a named volume — there is no `docker volume` to
remove.

Nothing accumulates in `models/`, because nothing is written there. Everything in `out/`
is regenerated and overwritten on each run, including when you rename node keys in
`mapping.json` or switch to a different network. If you want a guaranteed-fresh result
anyway, delete the output directory — it is recreated automatically:

```bash
rm -rf tools/distributed/vertical/out
```

Sub-models from a previous mapping stay in `out/` under their old names until you do
that. They are never loaded — only the names currently in `mapping.json` are read — so
they waste disk and nothing else.

## Environment Variables

Every knob in one place. All are optional; the defaults are what the quick start uses.

| Variable | Default | Purpose |
|----------|---------|---------|
| `AUTODICE_MODEL` | auto-detect | Which network in `models/` to split. Only needed when more than one is present. |
| `AUTODICE_IN` | `./models` | Input directory, inside the container. |
| `AUTODICE_OUT` | `./out` | Output directory, inside the container. |
| `AUTODICE_HOST` | local hostname | Single MPI host for every rank. |
| `AUTODICE_HOSTS` | — | Per-device MPI hosts, e.g. `lenovo=node-a,jetson=node-b`. |

## Host Configuration

The device part of a mapping key (`lenovo` in `lenovo_cpu0`) is a **logical** name — it
picks the sub-model filenames. MPI, on the other hand, needs a host it can actually
resolve. The two are decoupled by two environment variables read by `interface.py`:

| Variable | Meaning |
|----------|---------|
| `AUTODICE_HOST` | Single host for every rank. Defaults to the machine's own hostname. |
| `AUTODICE_HOSTS` | Per-device mapping, e.g. `lenovo=node-a,jetson=node-b`. Devices not listed fall back to `AUTODICE_HOST`. |

So the default case needs no configuration at all — a container with a random hostname
writes a `rankfile` pointing at itself and runs both ranks locally:

```bash
docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out autodice
```

To spread the same partition over two real machines:

```bash
docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out \
  -e AUTODICE_HOSTS="lenovo=node-a" autodice python3 interface.py
```

which yields `rank 0=node-a slots=0` / `rank 1=node-a slots=1` and a matching `hostfile`.
Point the two device keys at different hosts to get one rank per machine. Note that
multi-machine MPI additionally needs passwordless SSH between the hosts and the `out/`
directory (sub-models, weights, binary) present on each — the image does not ship an SSH
daemon.

The generated `multinode.cpp` itself contains **no** hostnames: it dispatches on the MPI
rank index (`if (irank == 0)`) and sends to rank numbers, so only `rankfile`/`hostfile`
are host-dependent.

## Partition Configuration

The layer-to-node assignment is defined in `mapping.json`:

```json
{
  "lenovo_cpu0": [
    "conv1_1", "conv1_2", "norm1_1", "pool1_1",
    "conv2_1", "conv2_2", "norm2_1", "pool2_1",
    "conv3_1", "conv3_2", "conv4_1", "conv4_2",
    "conv5_1", "conv5_2", "pool5_1",
    "OC2_DUMMY_0", "fc6_1", "fc6_2"
  ],
  "lenovo_cpu1": [
    "fc6_3", "fc7_1", "fc7_2", "fc7_3", "fc8_1", "prob_1"
  ]
}
```

Node key format: `<device>_<resource>` where `<resource>` is one of:
- `cpu<core-ids>` — e.g. `cpu01` means cores 0 and 1
- `arm<core-ids>` — same, for ARM targets
- `gpu<id>` — GPU device

To change the split point, edit `mapping.json` and re-run `interface.py`.

## Using Your Own Model

1. Place your ONNX model in `models/`.
2. Edit `mapping.json` to assign your model's layer names to nodes.
3. Run the splitting step as shown above.

No code change is needed to select the model. If `models/` holds exactly one network, it
is used automatically. With more than one network present the run stops and lists them;
name the one you want with `AUTODICE_MODEL`:

```bash
docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out \
  -e AUTODICE_MODEL=models/vgg16-7.onnx \
  autodice
```

**The layer names are rewritten before splitting.** `format_onnx()` renames every node to
its first output tensor, with `/` replaced by `_`, so the names in `mapping.json` will not
match what you see in Netron. Always dump them from the *formatted* model:

```bash
docker run --rm -v $L/models:$V/models:ro autodice python3 -c "
from onnx_split import format_onnx
import onnx
m = onnx.load(format_onnx('models/YOURMODEL.onnx'))
print([n.name for n in m.graph.node])
"
```

## File Structure

```
tools/distributed/vertical/
├── interface.py          # Main entry point: splits model, generates C++ engine
├── onnx_split.py         # onnx_extract() and onnx_split() utilities
├── code_generator.py     # Low-level C++ file writer
├── cpp_generator.py      # Higher-level C++ code patterns
├── data_json.py          # JSON helpers
├── mapping.json          # Layer-to-node assignment (edit this to change partition)
├── run.sh                # End-to-end pipeline script
├── generate_docker_guide.py   # Builds AutoDiCE_Docker_Guide.pdf, the command guide
├── AutoDiCE_Docker_Guide.pdf  # Illustrated command guide for this example
├── dog.jpg               # Sample input image
├── synset_words.txt      # ImageNet class labels
├── models/               # INPUT: your ONNX networks. Mount read-only. Never written to.
└── out/                  # OUTPUT: everything generated by a run.
                          # Both excluded from the image via .dockerignore.
```
