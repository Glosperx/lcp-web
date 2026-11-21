"""Signal B: a complexity rating read from the next-token probabilities of an open-weight LLM.

For each prompt we take the probability the model assigns to the tokens "1".."5" at the first
answer position, renormalised over the five digits. Nothing is generated. The distributions are
stored per prompt together with their expected value rescaled to [0, 1] (`score`); `fuse.py` turns
them into the signal, choosing temperature and scale partition leave-one-language-out.

The paper's numbers come from the MLX checkpoints below, run on Apple silicon. On CUDA the same
models are loaded from the original Hugging Face weights with bitsandbytes quantisation. That path
was not used for the paper; its quantisation, and so its ratings, differ from MLX (see README).

Usage:
  python signal_b.py --model gemma4-12b-4bit                 # 10 MLSP languages, three prompts
  python signal_b.py --model gemma4-12b-4bit --with-ro       # plus RoLCP
  python signal_b.py --model qwen3-8b-4bit --limit 20        # quick check
Readings are cached in cache/, so an interrupted run resumes where it stopped. Runs restricted with
--limit or --langs stay in cache/; only a complete run updates predictions/signal_b.csv.
"""
import argparse
import csv
import os
import platform
import time

import numpy as np
import pandas as pd

import data

# Original Hugging Face weights for the CUDA path. The Gemma 4 MLX checkpoints are quantised from
# Google's quantisation-aware-trained (QAT) release, so the CUDA path loads that one too.
GEMMA4_QAT = ("google/gemma-4-12B-it-qat-q4_0-unquantized",
              "b6ed86275a6a5735884e208bfed95b445a684ca2")
QWEN3 = ("Qwen/Qwen3-8B", "b968826d9c46dd6066d109eabc6255188de91218")
QWEN35 = ("Qwen/Qwen3.5-9B", "c202236235762e1c871ad0ccb60c8ee5ba337b9a")
# key: (MLX repo, MLX revision, (HF repo, HF revision), HF quantisation bits)
MODELS = {
    "gemma4-12b-4bit": ("mlx-community/gemma-4-12B-it-qat-OptiQ-4bit",
                        "63912b888c04ba2c555f198685d10b05f54cf564", GEMMA4_QAT, 4),
    "gemma4-12b-8bit": ("mlx-community/gemma-4-12B-it-qat-8bit",
                        "eafed06893a6ee299315ebe0e0feb82f435e92fe", GEMMA4_QAT, 8),
    "qwen3-8b-4bit": ("mlx-community/Qwen3-8B-4bit",
                      "545dc4251c05440727734bcd94334791f6ab0192", QWEN3, 4),
    "qwen3-8b-8bit": ("mlx-community/Qwen3-8B-8bit",
                      "48a0b75b1ae72503e21e1558d040bc227510ff06", QWEN3, 8),
    "qwen35-9b-4bit": ("mlx-community/Qwen3.5-9B-MLX-4bit",
                       "938d8919941c6e7efd3c7150eff7fe9d12afa631", QWEN35, 4),
    "qwen35-9b-8bit": ("mlx-community/Qwen3.5-9B-MLX-8bit",
                       "84f7c2deea248d8df56240f88102def51c7ed5d6", QWEN35, 8),
    "llama31-8b-4bit": ("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit",
                        "241a666dad6cb93c8ff213d39a7f34a36bf26db4",
                        ("meta-llama/Llama-3.1-8B-Instruct",
                         "0e9e39f249a16976918f6564b8830bc894c89659"), 4),
    "aya-expanse-8b-4bit": ("mlx-community/aya-expanse-8b-4bit",
                            "3a7cee37dd4ab4ed76642f61f6253da4748e63ba",
                            ("CohereLabs/aya-expanse-8b",
                             "5062468bf9bc0c6035fd64e06274333ec127d980"), 4),
}

PROMPTS = {
    "expert": ("You are an expert in {lang} linguistics. On a scale of 1-5 (1=very familiar, "
               "2=simple, 3=neutral, 4=difficult, 5=very difficult), how complex or difficult is the "
               "{lang} word \"{tok}\" for an average reader, in the sentence:\n\"{sent}\"\n"
               "Answer with ONLY a single digit from 1 to 5."),
    "short": ("In the {lang} sentence: \"{sent}\"\nRate the lexical difficulty of the word \"{tok}\" "
              "on a scale from 1 (very familiar) to 5 (very difficult). Answer with only the digit."),
    "marked": ("In the {lang} sentence below, the target word is marked with «».\n\"{sent}\"\n"
               "On a scale of 1 (very familiar) to 5 (very difficult), how difficult is «{tok}» for "
               "an average reader? Answer with ONLY a single digit from 1 to 5."),
}
LANG_NAMES = {code: name.capitalize() for name, code in data.MLSP_LANGS.items()} | {"ro": "Romanian"}
DIGITS = "12345"
OUT = os.path.join(data.PRED_DIR, "signal_b.csv")
COLS = ["model", "prompt", "lang", "idx"] + [f"p{d}" for d in DIGITS] + ["score"]


class Rater:
    def __init__(self, key, backend):
        mlx_repo, rev, (hf_repo, hf_rev), bits = MODELS[key]
        self.backend = backend
        if backend == "mlx":
            import mlx.core as mx
            from mlx_lm import load
            self.mx = mx
            # Gemma 4 declares model_type "gemma4_unified", which mlx-lm 0.31 does not map.
            kw = {"model_config": {"model_type": "gemma4"}} if key.startswith("gemma4") else {}
            self.model, self.tok = load(mlx_repo, revision=rev, **kw)
        else:
            import torch
            from transformers import AutoModelForCausalLM, BitsAndBytesConfig, TokenizersBackend
            if not torch.cuda.is_available():
                raise SystemExit("--backend hf needs a CUDA GPU; on Apple silicon use --backend mlx")
            self.torch = torch
            q = (BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                    bnb_4bit_compute_dtype=torch.bfloat16,
                                    bnb_4bit_use_double_quant=True) if bits == 4
                 else BitsAndBytesConfig(load_in_8bit=True))
            # tokenizer.json as published. AutoTokenizer maps Qwen3.5 to Qwen2Tokenizer, whose
            # pre-tokeniser splits on combining marks and so tokenises Sinhala differently.
            self.tok = TokenizersBackend.from_pretrained(hf_repo, revision=hf_rev)
            self.model = AutoModelForCausalLM.from_pretrained(
                hf_repo, revision=hf_rev, quantization_config=q, device_map="cuda").eval()
        # Every token id that decodes to the digit, with and without a leading space.
        self.ids = {d: [] for d in DIGITS}
        for d in DIGITS:
            for variant in (d, " " + d):
                for t in self.tok.encode(variant, add_special_tokens=False):
                    if self.tok.decode([t]).strip() == d and t not in self.ids[d]:
                        self.ids[d].append(t)
        # Qwen3 opens a <think> block unless told not to; the digits would then be read from it.
        try:
            tmpl = self.tok.get_chat_template() or ""
        except Exception:
            tmpl = ""
        self.chat_kw = {"enable_thinking": False} if "enable_thinking" in tmpl else {}

    def logits(self, ids):
        if self.backend == "mlx":
            out = self.model(self.mx.array([ids]))[0, -1].astype(self.mx.float32)
            return np.array(out, copy=False)
        with self.torch.no_grad():
            t = self.torch.tensor([ids], device="cuda")
            return self.model(t).logits[0, -1].float().cpu().numpy()

    def digit_probs(self, content):
        """(p over 1..5 renormalised, raw probability mass on the digits)."""
        ids = self.tok.apply_chat_template([{"role": "user", "content": content}],
                                           add_generation_prompt=True, tokenize=True,
                                           return_dict=False, **self.chat_kw)
        lg = self.logits(ids)
        e = np.exp(lg - lg.max())
        probs = e / e.sum()
        p = np.array([float(probs[self.ids[d]].sum()) for d in DIGITS])
        raw = float(p.sum())
        return p / raw, raw


def render(prompt, lang, sent, token):
    sent = str(sent).replace("\n", " ").strip()
    tok = str(token).strip()
    if prompt == "marked":
        i = sent.find(tok)
        if i < 0 and (t2 := data.normalize_token(tok)) and sent.find(t2) >= 0:
            tok, i = t2, sent.find(t2)
        if i >= 0:
            sent = sent[:i] + "«" + tok + "»" + sent[i + len(tok):]
    return PROMPTS[prompt].format(lang=LANG_NAMES[lang], tok=tok, sent=sent)


def run(key, prompts, with_ro, backend, langs=None, limit=None):
    ev = data.load_eval(with_ro)
    if langs:
        ev = ev[ev["lang"].isin(langs)]
    if limit:
        ev = ev.groupby("lang").head(limit)
    part = os.path.join(data.CACHE_DIR, f"signal_b_{key}_{backend}.part.csv")
    done = set()
    if os.path.exists(part):
        d = pd.read_csv(part)
        done = set(zip(d["prompt"], d["idx"]))
    todo = [(p, r) for p in prompts for r in ev.itertuples() if (p, r.idx) not in done]
    print(f"[B] {key}: {len(todo)} readings to do ({len(done)} cached), backend {backend}", flush=True)
    if todo:
        r = Rater(key, backend)
        os.makedirs(data.CACHE_DIR, exist_ok=True)
        header = not os.path.exists(part)
        t0 = time.time()
        with open(part, "a", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            if header:
                w.writerow(COLS)
            for i, (pr, row) in enumerate(todo, 1):
                p, raw = r.digit_probs(render(pr, row.lang, row.sent, row.token))
                # Written so that NaN fails too. A low mass on the first reading means the chat
                # template does not end at an answer position.
                if not (raw >= 0.5 if i == 1 else raw > 1e-9):
                    raise SystemExit(f"{pr}, idx {row.idx}: only {raw:.3g} of the probability "
                                     "mass is on the digits")
                # score: the expected rating rescaled to [0, 1], i.e. the signal at temperature 1
                w.writerow([key, pr, row.lang, row.idx] + [repr(float(x)) for x in p]
                           + [repr((float(p @ np.arange(1.0, 6.0)) - 1.0) / 4.0)])
                fh.flush()
                if i % 100 == 0 or i == len(todo):
                    el = time.time() - t0
                    print(f"[B] {i}/{len(todo)}  {el/i:.2f}s per reading", flush=True)

    if langs or limit:
        print(f"[B] partial run, kept in {part}; predictions/ is updated only by a complete run")
        return
    # round_trip: the default parser can move the last bit of the rows that are kept
    new = pd.read_csv(part, float_precision="round_trip")
    new = new[new["prompt"].isin(prompts) & new["idx"].isin(ev["idx"])]
    old = (pd.read_csv(OUT, dtype={"idx": int}, float_precision="round_trip") if os.path.exists(OUT)
           else new.iloc[:0])
    # Replace the rows read now, and any older reading of this model under another prompt name
    # (the stored `expert+short` averages), so that fuse.py never mixes the two.
    keys = set(zip(new["model"], new["prompt"], new["idx"]))
    old = old[[k not in keys and not (k[0] == key and k[1] not in PROMPTS)
               for k in zip(old["model"], old["prompt"], old["idx"])]]
    out = pd.concat([old, new], ignore_index=True).sort_values(["model", "prompt", "idx"],
                                                               kind="stable")
    out.to_csv(OUT, index=False)
    print(f"-> {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", choices=list(MODELS), required=True)
    ap.add_argument("--prompts", nargs="+", choices=list(PROMPTS), default=list(PROMPTS))
    ap.add_argument("--with-ro", action="store_true", help="add RoLCP as an 11th language")
    ap.add_argument("--backend", choices=["mlx", "hf"], default=None,
                    help="default: mlx on Apple silicon, hf (CUDA) elsewhere")
    ap.add_argument("--langs", nargs="+", default=None)
    ap.add_argument("--limit", type=int, default=None, help="rows per language, for a quick check")
    a = ap.parse_args()
    be = a.backend or ("mlx" if platform.system() == "Darwin" and platform.machine() == "arm64"
                       else "hf")
    run(a.model, a.prompts, a.with_ro, be, a.langs, a.limit)
