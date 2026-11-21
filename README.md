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
