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

The paper's repository is the branch `lcp_model` (its own history, never merged into `main`),
checked out as a worktree next to this repo; `docker/run_cuda.sh` mounts its `release/` read-only at
`/paper/release`. Git for Windows writes the symlinks of `release/` as text files, so they are
replaced by copies and hidden from `git status`:

```bash
git config extensions.worktreeConfig true
git -c core.autocrlf=false worktree add --track -b lcp_model ../lcp-paper origin/lcp_model
cd ../lcp-paper && git config --worktree core.autocrlf false
L=$(git ls-tree -r HEAD release/ | awk '$1=="120000"{print $4}')
for f in $L; do t="$(dirname "$f")/$(cat "$f")"
  if [ -d "$t" ]; then rm "$f" && cp -r "$t" "$f"; else cp "$t" "$f.tmp" && mv "$f.tmp" "$f"; fi; done
git update-index --skip-worktree $L
```

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
2-3 times slower. n_ctx 1024 / n_batch 256 keeps it at ~7.4 GB. The Windows desktop must leave room
for it: with two screens at a high refresh rate it held ~850 MiB and Gemma spilled (check that
`nvidia-smi` shows under ~700 MiB in use before a GPU run).

### Stages 2 and 3 on the PC: exported model and the site's own signal B

Results and conclusion: `bench/results/concluzie_etapa2_3.txt`.

```
lcp/fusion.py            A (z), B (z), fused score, 0-1 score and level 1-5 from artifacts/
scripts/export_model.py  stage 2: signal A models (ridge + HGB per encoder: p_en, 11 x p_multi_L),
                         centring, z-score constants, LOLO parameters; parity gate against the paper
scripts/b_reference.py   stage 3: prompt length gate, B on the whole test set through llama.cpp in
                         the site's configuration, gates, LOLO fusion with that B, final params.json
artifacts/               params.json, centering.npz, signal_a_{xlmr,labse,e5}.joblib (numbers only)
reference/               signal_b_llamacpp.csv (format of signal_b.csv, model gemma4-12b-qat-gguf,
                         no text), per-reading timings, log
```

```bash
GPU=0 docker/run_cuda.sh python scripts/export_model.py                # ~7 min, CPU
GPU=0 docker/run_cuda.sh python scripts/b_reference.py --steps lengths
docker/run_cuda.sh python scripts/b_reference.py --steps run           # ~32 min on the GPU, resumable
GPU=0 docker/run_cuda.sh python scripts/b_reference.py --steps gates artifacts \
    --signal-a reference/_work/export/signal_a.csv --work reference/_work/fuse_llamacpp_exportA
```

`artifacts` reruns the LOLO fusion (`fuse.py --with-ro --out`) on the exported signal A and the
llama.cpp signal B and writes the final `params.json`; `reference/_work/` (gitignored) holds the
copies and outputs it needs.

### Stage 4: pipeline and API

Results and conclusion: `bench/results/concluzie_etapa4.txt`.

```
lcp/pipeline.py          raw text -> per content word: level 1-5, score 0-1, lemma, Zipf, A, B
server.py                FastAPI: POST /api/analyze (NDJSON stream), GET /api/languages, /api/health
scripts/pipeline_check.py  gate: the site's code path on test rows against the stage 3 reference
scripts/api_check.py     the running API on the benchmark texts, limits, long sentences, queue, cancel
docker/requirements.server.txt  fastapi, starlette, uvicorn (last layer of Dockerfile.cuda)
```

```bash
docker/run_cuda.sh python scripts/pipeline_check.py
PORT=8000 docker/run_cuda.sh uvicorn server:app --host 0.0.0.0 --port 8000
python scripts/api_check.py --url http://localhost:8000      # host, standard library only
curl -N -X POST localhost:8000/api/analyze -H 'Content-Type: application/json' \
    -d '{"lang": "en", "text": "The committee postponed the ratification of the treaty."}'
```

`POST /api/analyze` answers with one JSON object per line: `queued` (only when 6 texts are already
running), `paragraphs` (paragraph spans), per paragraph `sentences` (its sentence spans), one
`sentence` per finished sentence (its content words: `start`, `end`, `text`, `lemma`, `level`,
`label`, `score`, `zipf`, `A`, `B`, `fused`, and the flags `cropped`, `no_A`, `no_B`), then `done`
with the timings. A text may have up to 20000 characters (`max_chars`); above `warn_chars` (2000,
700 for Japanese, which has about three times more content words per character) the frontend asks
for confirmation, with the estimate `est_s_per_1000_chars` of `/api/languages`. One worker thread
owns the models; up to 6 texts run at once and take turns sentence by sentence, so a short text is
not held up by a long one. Sentences of more than 192 tokens or 40 content words are split into
pieces. A client that disconnects cancels its text. Texts are never logged. The models take ~40 s
to load; `/api/health` answers 503 until then. All nine stanza pipelines stay loaded
(`LCP_STANZA_KEEP=0`, ~7.2 GB for the container).
