"""Parity gate for llama.cpp on another machine (stage 7, GPU on the PC) against the Mac's CPU run.

Same prompts as bench_cpu.py on the Mac: the texts of bench/texts are segmented the same way and,
on the first --sents sentences of each 1-paragraph text, every content word is read with the three
prompts in the bench's order (sentence, prompt, word), with KV reuse. Each reading is matched to
bench/results/cpu_docker_mac_readings.csv on (lang, size, sent, word, prompt), mode reuse, run 0;
the prompt length in tokens must match too (same segmentation, same prompt), otherwise it stops.

Gate, fixed beforehand: Pearson r >= 0.99 between the two scores (expected rating rescaled to
0-1, lcp.rater.score) over all readings, and mass on the digits >= 0.5 without NaN. Also reported:
r per language and per prompt, max |dp| over the five probabilities, max |d score|.

  docker/run_cuda.sh python scripts/parity_mac.py --gpu-layers 40 --n-ctx 2048
Writes bench/results/{prefix}.csv (one row per reading, indices only, no text) and {prefix}.txt.
"""
import argparse
import gc
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import signal_b                                # noqa: E402  (lcp_model on PYTHONPATH)
from lcp import segment as S                   # noqa: E402
from lcp.rater import LlamaRater, score       # noqa: E402

PROMPTS = list(signal_b.PROMPTS)
P = [f"p{d}" for d in signal_b.DIGITS]
KEY = ["lang", "size", "sent", "word", "prompt"]
R_MIN, MASS_MIN = 0.99, 0.5


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ref", default="bench/results/cpu_docker_mac_readings.csv")
    ap.add_argument("--texts", default="bench/texts")
    ap.add_argument("--out", default="bench/results")
    ap.add_argument("--prefix", default="parity_gpu_pc")
    ap.add_argument("--langs", nargs="+", default=list(S.LANGS))
    ap.add_argument("--size", type=int, default=1)
    ap.add_argument("--sents", type=int, default=2, help="first sentences of each text")
    ap.add_argument("--gpu-layers", type=int, default=0)
    ap.add_argument("--flash-attn", action="store_true")
    ap.add_argument("--n-ctx", type=int, default=4096)
    ap.add_argument("--n-batch", type=int, default=512)
    ap.add_argument("--threads", type=int, default=None)
    a = ap.parse_args()

    ref = pd.read_csv(a.ref)
    ref = ref[(ref["mode"] == "reuse") & (ref["run"] == 0) & (ref["size"] == a.size)]
    ref = ref.set_index(KEY)
    rt = LlamaRater(n_threads=a.threads, n_ctx=a.n_ctx, n_batch=a.n_batch,
                    n_gpu_layers=a.gpu_layers, flash_attn=a.flash_attn)
    rt.reuse = True
    seg = S.Segmenter()
    rows = []
    for lg in a.langs:
        with open(os.path.join(a.texts, f"{lg}_{a.size}.txt"), encoding="utf-8") as fh:
            sents = seg.segment(lg, fh.read().strip())
        rt._prev = []
        for si, s in enumerate(sents[:a.sents]):
            for pr in PROMPTS:
                for wi, w in enumerate(s.content_words):
                    p, raw = rt.read(pr, lg, s.text, w.text)
                    k = (lg, a.size, si, wi, pr)
                    if k not in ref.index:
                        raise SystemExit(f"no Mac reading for {k}: segmentation differs")
                    m = ref.loc[k]
                    if int(m["n_tokens"]) != rt.last[0]:
                        raise SystemExit(f"{k}: {rt.last[0]} prompt tokens here, "
                                         f"{int(m['n_tokens'])} on the Mac")
                    pm = m[P].to_numpy(float)
                    rows.append(dict(zip(KEY, k), raw=raw, raw_mac=float(m["raw"]),
                                     score=score(p), score_mac=score(pm),
                                     max_dp=float(np.abs(np.asarray(p) - pm).max()),
                                     n_tokens=rt.last[0],
                                     **{c: float(x) for c, x in zip(P, p)}))
        print(f"[parity] {lg}: {sum(r['lang'] == lg for r in rows)} readings", flush=True)
        if seg._nlp.pop(lg, None) is not None:
            gc.collect()

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(a.out, a.prefix + ".csv"), index=False)
    r_all = float(np.corrcoef(df["score"], df["score_mac"])[0, 1])
    nan = int(df[P + ["raw"]].isna().any(axis=1).sum())
    ok = r_all >= R_MIN and df["raw"].min() >= MASS_MIN and nan == 0
    L = [f"Poarta de paritate: llama.cpp aici (gpu layers {a.gpu_layers}, flash attn "
         f"{a.flash_attn}, n_ctx {a.n_ctx}, n_batch {a.n_batch}) fata de CPU in Docker pe Mac",
         f"subset: primele {a.sents} propozitii din fiecare text de {a.size} paragraf, "
         f"{len(df)} citiri, {df['lang'].nunique()} limbi; cheie {', '.join(KEY)}, "
         f"mod reuse, run 0; tokenii de prompt identici pe toate citirile",
         f"r scor (toate citirile): {r_all:.5f} (prag {R_MIN})",
         f"masa pe cifre: minim {df['raw'].min():.5f} aici, {df['raw_mac'].min():.5f} pe Mac "
         f"(prag {MASS_MIN}); NaN: {nan}",
         f"max |dp| pe cele 5 probabilitati: {df['max_dp'].max():.4g} (median "
         f"{df['max_dp'].median():.3g}); max |d scor|: "
         f"{(df['score'] - df['score_mac']).abs().max():.4g}",
         "r pe limba: " + ", ".join(
             f"{lg} {np.corrcoef(g['score'], g['score_mac'])[0, 1]:.4f}"
             for lg, g in df.groupby("lang")),
         "r pe prompt: " + ", ".join(
             f"{pr} {np.corrcoef(g['score'], g['score_mac'])[0, 1]:.4f}"
             for pr, g in df.groupby("prompt")),
         f"POARTA {'TRECE' if ok else 'PICA'}"]
    with open(os.path.join(a.out, a.prefix + ".txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
