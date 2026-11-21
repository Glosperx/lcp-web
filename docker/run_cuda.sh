#!/usr/bin/env bash
# Runs a command in the stage 7 CUDA image (lcp-web:cuda) on the PC, for example:
#   docker/run_cuda.sh python scripts/fit_gpu_layers.py
#   GPU=0 docker/run_cuda.sh python scripts/bench_cpu.py --skip-a ...     # x86 CPU only
#   HF_ONLINE=1 docker/run_cuda.sh hf download ...                       # downloads
#
# Mounts: this repo at /app; the named volume lcp-hf at /hf/hub (the Hugging Face cache, on the
# Docker VM's own disk rather than /mnt/c, so the 7 GB GGUF reads fast), read-only unless
# HF_ONLINE=1, which also lifts HF_HUB_OFFLINE; the named volume lcp-stanza at /stanza. The paper's
# data is not mounted (not needed on the PC).
# GPU=0 runs without --gpus: the container sees no GPU at all, so llama.cpp cannot move work to it
# even with n_gpu_layers=0; the CUDA driver stub stands in for libcuda.so.1 (see Dockerfile.cuda).
set -euo pipefail
export MSYS_NO_PATHCONV=1          # Git Bash on Windows: leave /app, /hf/hub as they are
REPO="$(cd "$(dirname "$0")/.." && (pwd -W 2>/dev/null || pwd))"
TTY="-i"
[ -t 0 ] && [ -t 1 ] && TTY="-it"
ARGS=()
HF_MODE=ro
if [ "${HF_ONLINE:-0}" = 1 ]; then
  HF_MODE=rw
  ARGS+=(-e HF_HUB_OFFLINE=0)
fi
if [ "${GPU:-1}" = 1 ]; then
  ARGS+=(--gpus all)
else
  ARGS+=(-e LD_LIBRARY_PATH=/opt/cuda-stub)
fi
exec docker run --rm $TTY "${ARGS[@]}" \
  -v "$REPO":/app \
  -v lcp-hf:/hf/hub:$HF_MODE \
  -v lcp-stanza:/stanza \
  "${LCP_IMAGE:-lcp-web:cuda}" "$@"
