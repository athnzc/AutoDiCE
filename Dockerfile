FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        cmake \
        libomp-dev \
        libprotobuf-dev \
        protobuf-compiler \
        openmpi-bin \
        libopenmpi-dev \
        libopencv-dev \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ───────────────────────────────────────────────────────
RUN pip3 install --no-cache-dir numpy psutil onnx reportlab

# ── Copy source ───────────────────────────────────────────────────────────────
WORKDIR /autodice
COPY . /autodice

# ── Build AutoDiCE (ncnn + MPI + OpenMP, CPU-only) ───────────────────────────
RUN mkdir -p /autodice/build && cd /autodice/build && \
    cmake \
        -DNCNN_VULKAN=OFF \
        -DNCNN_CUDA=OFF \
        -DNCNN_MPI=ON \
        -DNCNN_OPENMP=ON \
        -DNCNN_BUILD_TESTS=OFF \
        -DNCNN_BUILD_EXAMPLES=ON \
        -DNCNN_BUILD_BENCHMARK=OFF \
        .. && \
    make -j"$(nproc)"

# ── Working directory for run.sh ──────────────────────────────────────────────
WORKDIR /autodice/tools/distributed/vertical

CMD ["bash", "run.sh"]
