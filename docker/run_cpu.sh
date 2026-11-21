#!/usr/bin/env bash
# Runs a command in the stage 1 CPU image (lcp-web:cpu), for example:
#   docker/run_cpu.sh python scripts/spike_llama.py --paper-release /paper/release
#
# Mounts: this repo at /app; the Mac's Hugging Face cache read-only at /hf/hub; the named volume
# lcp-stanza at /stanza; the paper's release/ read-only at /paper/release, plus the two data paths
# its data/ symlinks point to (../../data/mlsp_full, ../../data/RoLCP.csv), also read-only. No
# dataset file is copied into this repo.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PAPER="${PAPER:-$HOME/Documents/GitHub/ia-sahistii}"
HF_CACHE="${HF_CACHE:-$HOME/.cache/huggingface/hub}"
TTY=""
[ -t 0 ] && [ -t 1 ] && TTY="-it"
exec docker run --rm $TTY \
  -v "$REPO":/app \
  -v "$HF_CACHE":/hf/hub:ro \
  -v lcp-stanza:/stanza \
  -v "$PAPER/release":/paper/release:ro \
  -v "$PAPER/data/mlsp_full":/paper/data/mlsp_full:ro \
  -v "$PAPER/data/RoLCP.csv":/paper/data/RoLCP.csv:ro \
  "${LCP_IMAGE:-lcp-web:cpu}" "$@"
