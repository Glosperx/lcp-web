# Multilingual lexical complexity prediction without target-language labels

Code and predictions for the anonymous submission. The system predicts the complexity of a target
word in context for ten MLSP 2024 languages (and, optionally, Romanian), using no labels in the
language being predicted. It fuses two signals, both evaluated leave-one-language-out (LOLO):

- **Signal A** (`signal_a.py`): a ridge + gradient-boosting regressor over a frozen multilingual
  encoder, with frequency resolved through the lemma and subword fertility in place of character
  length. Fitted on CompLex English plus the other evaluation languages.
- **Signal B** (`signal_b.py`): a 1-5 rating read from an LLM's next-token probabilities over the
  digits, under three prompts.
- **Fusion** (`fuse.py`): averages the encoders, chooses the temperature and rating scale of B, the
  language model, and the fusion weights, each on the other languages only.

```
data.py        data loading, target spans, lemmas, lexical features, evaluation helpers
signal_a.py    signal A for one encoder
signal_b.py    signal B for one language model
fuse.py        LOLO fusion and evaluation (CPU, a few seconds)
predictions/   signal_a.csv and signal_b.csv, the per-item outputs used in the paper
```

## Setup

Python 3.11 (3.13 also works), in a fresh virtual environment:

```bash
pip install -r requirements.txt
```

A `torchvision` left in an existing environment and built for another PyTorch version breaks
`import transformers` ("operator torchvision::nms does not exist"); nothing here uses it, so
uninstall it in that case.

## Data

No dataset text is redistributed here. Predictions are keyed by `(lang, idx)`, the row position in
the frame built by `data.load_eval`.

- **MLSP 2024** (Shardlow et al., 2024) is gated on Hugging Face as `MLSP2024/MLSP2024`. Accept its
  terms and log in (`hf auth login`); it is downloaded to `data/MLSP2024/` on first use.
  A local copy can be used instead with `MLSP_DIR=/path/to/MLSP2024`.
- **CompLex 2.0** (Shardlow et al., 2021) is downloaded automatically from its GitHub repository.
- **RoLCP** (Romanian, optional) comes from the RALS repository, distributed as a password-protected
  archive; the password is in that repository's README. Place `RoLCP.csv` at `data/RoLCP.csv`, or
  set `ROLCP_CSV`. It is needed only for `--with-ro`.

## Reproducing the results

From the stored predictions (CPU, seconds):

```bash
python fuse.py              # ten MLSP languages
python fuse.py --with-ro    # eleven languages, Romanian included
```

Expected output for the ten languages:

```
lang   n           model      T partition  w_src      w    r_A    r_B  r_fused     lo     hi
  ca 445 gemma4-12b-4bit 6.0000   1|23|45 0.7500 0.3500 0.4602 0.5187   0.5625 0.5000 0.6178
  de 570 gemma4-12b-4bit 6.0000   1|23|45 0.6250 0.3500 0.6781 0.7108   0.7710 0.7375 0.8018
  en 570 gemma4-12b-4bit 6.0000   1|23|45 0.7500 0.3500 0.7896 0.8471   0.8692 0.8424 0.8926
  es 593 gemma4-12b-4bit 6.0000   1|23|45 0.7500 0.3500 0.7017 0.7553   0.7666 0.7294 0.7996
 fil 570 gemma4-12b-4bit 6.0000   1|23|45 1.0000 0.3500 0.4184 0.5000   0.5078 0.4404 0.5667
  fr 569 gemma4-12b-4bit 6.0000   1|23|45 1.0000 0.3500 0.5426 0.6752   0.6670 0.6141 0.7141
  it 570 gemma4-12b-4bit 6.0000   1|23|45 0.7500 0.3500 0.6486 0.6406   0.6798 0.6355 0.7231
  ja 570 gemma4-12b-4bit 6.0000   1|23|45 0.8750 0.3500 0.6148 0.7795   0.7954 0.7542 0.8300
  pt 567 gemma4-12b-4bit 6.0000   1|23|45 0.7500 0.3500 0.7858 0.8243   0.8412 0.8112 0.8680
  si 600 gemma4-12b-4bit 6.0000   1|23|45 0.7500 0.3500 0.3205 0.3979   0.4370 0.3782 0.4935

mean over 10 languages: A 0.596033 | B 0.664934 | fused 0.689745  95% CI [0.6751, 0.7035]
```

`r_A`, `r_B` and `r_fused` are Pearson correlations on the test split; `lo` and `hi` bound a 95%
interval from 2000 bootstrap resamples of contexts, since several targets share a sentence.
With `--with-ro` the mean over eleven languages is 0.692521.

Ablations use the same script:

```bash
python fuse.py --encoders xlmr                          # a single encoder
python fuse.py --encoders xlmr labse e5 xlmr-large      # all four encoders
python fuse.py --models qwen3-8b-4bit                   # one language model, no selection
python fuse.py --out fused.csv                          # also write per-item predictions
```

## Recomputing the signals

Each run rewrites its own rows in `predictions/`, after which `fuse.py` uses them.

**Signal A**, one encoder at a time (`xlmr`, `xlmr-large`, `labse`, `e5`):

```bash
python signal_a.py --encoder xlmr
python signal_a.py --encoder xlmr --with-ro
```

On an Apple M5 the first run takes about 7 minutes, most of it spent downloading the stanza models
(about 8 GB, for nine languages) and lemmatising about 9,500 sentences once. Embedding the 15,634 targets then takes about 2 minutes
for each base encoder and 6 for XLM-R large, and the regressor about 30 seconds. Embeddings and
lemmas are cached in `cache/`. When English is the held-out language, CompLex is removed from
training as well, so English is predicted without any English labels.

**Signal B**, one language model at a time:

```bash
python signal_b.py --model gemma4-12b-4bit
python signal_b.py --model gemma4-12b-4bit --with-ro
python signal_b.py --model qwen3-8b-4bit --limit 20    # quick check, 20 rows per language
```

Three prompts are read per item (`expert`, `short`, `marked`; select with `--prompts`). The paper
used the MLX checkpoints listed in `signal_b.py`, pinned to a revision, on Apple silicon (about
0.36 s per reading for Gemma 4 12B on an M5, so about 2 hours 10 minutes for the 21,633 readings of
`--with-ro`). On a CUDA machine (`--backend hf`) the original Hugging Face weights, also pinned,
are loaded with bitsandbytes quantisation instead; for Gemma 4 these are Google's
quantisation-aware-trained weights, from which the MLX checkpoints were made. That path was not used
for the paper. Checked on a Colab T4 with five rows per language, its readings are well formed (all
probability mass on the digits, no NaN) but follow a different quantisation, so the ratings differ:
the mean of the three Gemma 4 prompts correlates at 0.97 with the stored ratings, a single Qwen3 8B
prompt at about 0.7. A T4 takes about 2 s per Gemma 4 reading. The reported numbers need the MLX
path. Interrupted runs resume from `cache/`.
Runs restricted with `--limit` or `--langs` stay in `cache/`; only a complete run updates
`predictions/`.

## Models

| Signal | Model | In `predictions/` |
|---|---|---|
| A | XLM-R base, LaBSE, multilingual E5 base | 10 and 11 languages (the system averages these three) |
| A | XLM-R large | 10 and 11 languages |
| B | Gemma 4 12B, 4-bit QAT (MLX) | three prompts, 11 languages |
| B | Qwen3 8B 4-bit, Qwen3.5 9B 8-bit (MLX) | 10 languages |

For the two Qwen models only the averaged reading of the `expert` and `short` prompts at
temperature 1 was stored (`prompt = expert+short`), so `fuse.py` uses it as is; rerunning
`signal_b.py` for them replaces it with full distributions. Gemma 4 is selected for every language.
Five more models from the development pool (Qwen3 8B 8-bit, Qwen3.5 9B 4-bit, Gemma 4 12B 8-bit,
Llama 3.1 8B, Aya Expanse 8B) can be run with the same script.

## Determinism

With the pinned versions on Apple silicon, rerunning `signal_a.py` from an empty cache reproduces
the stored predictions bit for bit (lemmas and embeddings included, checked for all four encoders),
and `fuse.py` reproduces the reported correlations. Rerunning `signal_b.py` reproduces the stored
Gemma 4 digit distributions to within 1.2e-16, three quarters of the readings bit for bit, which
leaves every number printed by `fuse.py` unchanged; the stored Qwen3 8B averages come out within
5e-9 (checked on 20 rows per language).

Other hardware changes the embeddings by about 1e-6 in relative terms, which is enough to move some
splits of the gradient-boosted trees. With signal A for XLM-R base recomputed on a Colab T4 (CUDA),
its predictions correlate at 0.9996 with the stored ones and the mean fused r moves from 0.689745
to 0.689708. Signal B on CUDA differs more, through its quantisation (see above).
