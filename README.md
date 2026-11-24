# lcp-web

A web interface for multilingual lexical complexity prediction. Given a text in one of eleven
languages, the system assigns every content word a complexity level from 1 to 5 and highlights it
accordingly. Selecting a word shows its part of speech, level, score and lemma.

Supported languages: Catalan, English, Filipino, French, German, Italian, Japanese, Portuguese,
Romanian, Sinhala and Spanish.

## Method

The site runs the system described in the accompanying paper. Each content word receives two
predictions. Signal A comes from ridge and gradient-boosting regressors trained on contextual
embeddings from three multilingual encoders (XLM-RoBERTa, LaBSE and multilingual E5). Signal B is a
rating produced by Gemma 4 12B, prompted with the word in its sentence and run through llama.cpp
with Google's quantisation-aware q4_0 weights. Both signals are standardised within each language
and then combined.

The setup is cross-lingual throughout. The signal A models applied to a language are trained
without any data from that language, and the fusion parameters are selected leave-one-language-out.

Only content words are scored, in line with the targets of the MLSP datasets. Function words are
given level 1 without consulting the models, and proper nouns, numerals and foreign words are left
unmarked.

## Reliability

Scores are relative to the language in which they are computed and should not be compared across
languages. Prediction quality also differs between languages. Pearson correlations of the fused
score on each language's test set are given below.

| Language   | r     | Language   | r     |
|------------|-------|------------|-------|
| English    | 0.870 | Italian    | 0.682 |
| Portuguese | 0.844 | French     | 0.653 |
| Japanese   | 0.781 | Catalan    | 0.563 |
| German     | 0.771 | Filipino   | 0.498 |
| Spanish    | 0.770 | Sinhala    | 0.426 |
| Romanian   | 0.746 |            |       |

The mean over the eleven languages is 0.691 (95% CI 0.677 to 0.704). These figures are for the
deployed configuration, where signal B comes from llama.cpp. They are therefore slightly different
from those in the paper, which reports a mean of 0.693.

## Repository structure

```
lcp/            segmentation, encoders, llama.cpp rater, fusion and the full pipeline
lcp_model/      model code from the paper's release, unchanged
artifacts/      exported signal A models and fusion parameters
server.py       FastAPI backend
static/         front end (plain HTML, CSS and JavaScript, no build step)
docker/         CUDA image, and a CPU image used for benchmarking
scripts/        model download, export, verification, benchmarks, site start and stop
bench/          benchmark texts and results
reference/      signal B for the test set computed with llama.cpp (no text)
```

The repository contains no text from the evaluation datasets. The benchmark texts are taken from
Wikipedia and are distributed under CC BY-SA 4.0 (see `bench/texts/README.md`).

## Running locally

Running the system requires an NVIDIA GPU with at least 8 GB of memory and Docker with GPU support.
The commands below assume a bash shell (Git Bash on Windows).

```bash
docker build -f docker/Dockerfile.cuda -t lcp-web:cuda .
HF_ONLINE=1 docker/run_cuda.sh python scripts/fetch_models.py    # Gemma GGUF (7 GB), tokenizer, encoders
HF_ONLINE=1 docker/run_cuda.sh python -m lcp.segment --prepare   # stanza models
cp .env.example .env
docker compose up -d
```

The interface is then served at http://localhost:8000. Loading the models takes about a minute,
during which `/api/health` returns 503.

The model occupies about 7.4 GB of GPU memory. On Windows, if other applications leave too little
free memory, the driver moves part of the model into system memory and analysis becomes two to
three times slower. This shows up in `/api/health` as a low `tok_s` value; around 1000 is normal on
an RTX 2070 SUPER.

## API

| Endpoint              | Description                                                       |
|-----------------------|-------------------------------------------------------------------|
| `GET /api/languages`  | Supported languages and text length limits                        |
| `POST /api/analyze`   | Takes `{"lang": "en", "text": "..."}` and streams results as NDJSON, one line per completed sentence |
| `GET /api/health`     | Returns 503 while the models load, then reports GPU throughput    |
| `POST /api/auth`      | Verifies the access code, when one is configured in `.env`        |

Texts may be up to 20,000 characters long. Up to six texts are processed concurrently, and they
are interleaved sentence by sentence so that a short text is not held back by a long one.
Submitted texts are not logged.

## Deployment

The front end is a static site hosted on Vercel from `static/`. The API runs on a single
workstation GPU and is exposed through Tailscale Funnel. `scripts/site_start.cmd` and
`scripts/site_stop.cmd` start and stop the service on that machine.
