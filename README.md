# lcp-web

Web application for the multilingual lexical complexity system of the paper (signals A and B fused
leave-one-language-out, 11 languages). Every content word of a text is coloured by its predicted
complexity.

The model code in `lcp_model/` (`data.py`, `signal_a.py`, `signal_b.py`, `fuse.py`) is copied
unchanged from the paper's release; it is imported with `PYTHONPATH=lcp_model`. No dataset text is
stored here: scripts that need MLSP or RoLCP read them read-only from the paper's release folder
(`--paper-release`).

## Status: stage 1, inference time without a GPU

```
lcp/segment.py     stanza (9 languages) or regex (fil, si) segmentation, content words
lcp/encoders.py    the three encoders of signal A, one forward pass per sentence
lcp/rater.py       signal B through llama.cpp, from Google's QAT q4_0 GGUF of Gemma 4 12B
lcp/paper.py       points lcp_model/data.py at the paper's release folder
scripts/spike_llama.py   gates for the llama.cpp rater against predictions/signal_b.csv
scripts/fetch_texts.py   benchmark texts from Wikipedia (CC BY-SA 4.0, see bench/texts/README.md)
scripts/bench_cpu.py     timing per language and text size
scripts/bench_report.py  plain-text summary of a benchmark run
docker/Dockerfile.cpu    linux/arm64 CPU image; docker/run_cpu.sh runs a command in it
bench/results/           spike, encoder check, benchmark CSVs and summaries
```

### Running it (Docker Desktop, 16 GB and 10 CPUs for the VM)

```bash
docker build -f docker/Dockerfile.cpu -t lcp-web:cpu .
# Gemma GGUF into the host's Hugging Face cache (6.98 GB, pinned revision, see lcp/rater.py)
hf download google/gemma-4-12B-it-qat-q4_0-gguf gemma-4-12b-it-qat-q4_0.gguf \
    --revision 29d097773436b69ff9feafd636ab4cf873786537
docker/run_cpu.sh python -m lcp.segment --prepare          # unpack stanza into volume lcp-stanza
docker/run_cpu.sh python scripts/spike_llama.py             # gates
docker/run_cpu.sh python -m lcp.encoders --check            # A: same vectors as Encoder.embed
python3 scripts/fetch_texts.py --pick Q525                  # texts (host, standard library)
docker/run_cpu.sh python scripts/bench_cpu.py --modes reuse noreuse --noreuse-sizes 1 \
    --warmup 1 --reps 3 --b-warmup 0 --b-reps 1
python scripts/bench_report.py --prefix cpu_docker_mac
```

`docker/run_cpu.sh` mounts the repo at `/app`, the host's Hugging Face cache read-only, the stanza
volume, and the paper's `release/` (with the two data paths its symlinks point to) read-only. The
paper repository is expected at `~/Documents/GitHub/ia-sahistii` (override with `PAPER=`).

### Stage 7 on the PC (CUDA, RTX 2070 SUPER 8 GB, Docker Desktop with WSL2)

Results and conclusion: `bench/results/concluzie_etapa7_pc.txt`. Run from Git Bash; the Hugging
Face cache lives in the Docker volume `lcp-hf` (not on `/mnt/c`), the VM has 12 GB (`.wslconfig`).

```bash
docker build -f docker/Dockerfile.cuda -t lcp-web:cuda .
HF_ONLINE=1 docker/run_cuda.sh python scripts/fetch_models.py      # GGUF (sha256), tokenizer, encoders
HF_ONLINE=1 docker/run_cuda.sh python -m lcp.segment --prepare     # stanza into volume lcp-stanza
docker/run_cuda.sh python scripts/fit_gpu_layers.py --n-ctx 1024 --n-batch 256 --flash-attn
docker/run_cuda.sh python scripts/parity_mac.py --gpu-layers 49 --flash-attn --n-ctx 1024 --n-batch 256
docker/run_cuda.sh python scripts/bench_cpu.py --modes reuse noreuse --noreuse-sizes 1 \
    --warmup 1 --reps 3 --b-warmup 1 --b-reps 3 --gpu-layers 49 --flash-attn --n-ctx 1024 \
    --n-batch 256 --prefix gpu_docker_pc
# x86 CPU reference: no --gpus at all (GPU=0), B only
GPU=0 docker/run_cuda.sh python scripts/bench_cpu.py --skip-a --modes reuse --langs en ro si \
    --sizes 1 --warmup 0 --reps 1 --b-warmup 0 --b-reps 1 --prefix cpu_docker_pc
```

With n_ctx 2048 and n_batch 512 the process needs ~8.1 GB on the card; on Windows the driver then
pages part of it into system memory ("shared GPU memory") instead of failing, and readings get
2-3 times slower. n_ctx 1024 / n_batch 256 keeps it at ~7.4 GB.
