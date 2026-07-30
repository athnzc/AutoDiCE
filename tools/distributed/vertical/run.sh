#!/bin/sh
set -e

# Input networks are read from $IN (mountable read-only); everything this script and
# interface.py generate goes to $OUT. Keeping them apart means no generated file can
# be mistaken for a model to split, whatever you rename.
IN=${AUTODICE_IN:-./models}
OUT=${AUTODICE_OUT:-./out}
export AUTODICE_IN="$IN"
export AUTODICE_OUT="$OUT"

# Generate Sub-models
echo "Generated Sub-models"
python3 interface.py
cp "$OUT"/multinode.cpp ../../../examples/

cp ../../../build/tools/onnx/onnx2ncnn .
cp synset_words.txt "$OUT"/
cp dog.jpg "$OUT"/
# Compile
echo "compile cpp file into executable binary (./multinode)"
cd ../../../build/ && make -j6
cd ../tools/distributed/vertical/
cp ../../../build/examples/multinode "$OUT"/

#python3 onnx_ncnn.py $1 $2 $3
# Convert the generated sub-models, one per key in mapping.json.
for name in `python3 -c "import json;print(' '.join(json.load(open('mapping.json'))))"`; do
    ./onnx2ncnn "$OUT"/$name.onnx
done

# Distributed inference: one MPI rank per line of the generated rankfile.
# --allow-run-as-root: the container runs as root, which OpenMPI refuses by default.
# Expect a "failed to bind memory" warning: containers cannot bind memory to a NUMA
# node. It is harmless, CPU pinning still applies, and the only way to silence it is
# --bind-to none, which throws away the pinning the rankfile exists to provide.
echo "run distributed inference"
cd "$OUT"
NP=`grep -c '^rank ' rankfile`
MPIRUN="mpirun --allow-run-as-root --oversubscribe -np $NP"
if grep -q "=`hostname`[[:space:]]" rankfile; then
    $MPIRUN -rf rankfile ./multinode dog.jpg
else
    # The rankfile targets other hosts (see AUTODICE_HOSTS in the README), so this
    # machine can only run the ranks locally, without core pinning.
    echo "note: `hostname` is not in rankfile, running without core pinning"
    $MPIRUN ./multinode dog.jpg
fi
