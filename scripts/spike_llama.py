"""Spike: signal B through llama.cpp on CPU, against the paper's stored readings.

Gates, fixed before the run; the script stops at the first that fails and prints the number:
  1. vocabulary: for every spike prompt, the GGUF tokeniser turns the rendered chat text into the
     same ids as the Hugging Face tokenizer used in the paper, and every digit id decodes to its
     digit in the GGUF vocabulary;
  2. digit mass: at least 0.5 of the probability on the digits for every reading, no NaN;
  3. agreement: on the first ROWS rows per language (as `signal_b.py --limit`) x 3 prompts, the
     expected rating averaged over the prompts correlates with predictions/signal_b.csv at
     r >= 0.90 in each of the 11 languages and r >= 0.95 over all rows pooled. (The CUDA path of
     the release, bitsandbytes NF4 on a T4, gave 0.97 pooled.)
Not a gate: the same readings again with the KV prefix reused, and the largest change in p.

Per-reading output (no dataset text): bench/results/spike_llama.csv.
  docker/run_cpu.sh python scripts/spike_llama.py --paper-release /paper/release
"""
import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import data                                    # noqa: E402  (lcp_model on PYTHONPATH)
import signal_b                                # noqa: E402
from lcp import rater as R                     # noqa: E402
from lcp.paper import use_release              # noqa: E402

GATE_MASS, GATE_R_LANG, GATE_R_POOLED = 0.5, 0.90, 0.95


def fail(msg):
    print(f"\n[GATE FAILED] {msg}", flush=True)
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--paper-release", default="/paper/release")
    ap.add_argument("--rows", type=int, default=10, help="rows per language")
    ap.add_argument("--threads", type=int, default=None)
    ap.add_argument("--out", default="bench/results/spike_llama.csv")
    a = ap.parse_args()
    use_release(a.paper_release)

    ev = data.load_eval(with_ro=True).groupby("lang").head(a.rows)
    prompts = list(signal_b.PROMPTS)
    todo = [(p, r) for p in prompts for r in ev.itertuples()]     # the order of signal_b.run
    print(f"[spike] {len(ev)} rows ({a.rows} per language, {ev['lang'].nunique()} languages) "
          f"x {len(prompts)} prompts = {len(todo)} readings", flush=True)

    # ------------------------------------------------------------ gate 1: vocabulary
    import llama_cpp
    tok = R.load_tokenizer()
    ids = R.digit_ids(tok)
    kw = R.chat_kwargs(tok)
    voc = llama_cpp.Llama(model_path=R.gguf_path(), vocab_only=True, verbose=False)
    print(f"[gate 1] HF vocab {len(tok)}, GGUF vocab {voc.n_vocab()}, digit ids {ids}, "
          f"chat kwargs {kw}", flush=True)
    bad_digits = [(d, t, voc.detokenize([t]).decode("utf-8", "replace"))
                  for d, ts in ids.items() for t in ts
                  if voc.detokenize([t]).decode("utf-8", "replace").strip() != d]
    if bad_digits or not all(ids.values()):
        fail(f"digit ids do not decode to their digit in the GGUF vocabulary: {bad_digits or ids}")
    mism = 0
    for pr, r in todo:
        msgs = [{"role": "user", "content": signal_b.render(pr, r.lang, r.sent, r.token)}]
        hf = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True,
                                     return_dict=False, **kw)
        txt = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False, **kw)
        gg = voc.tokenize(txt.encode("utf-8"), add_bos=False, special=True)
        if list(hf) != list(gg):
            if mism == 0:
                k = next((i for i, (x, y) in enumerate(zip(hf, gg)) if x != y), min(len(hf), len(gg)))
                print(f"[gate 1] first mismatch: {pr} {r.lang} idx {r.idx}, position {k}, "
                      f"HF {list(hf[k:k + 5])} vs GGUF {list(gg[k:k + 5])}", flush=True)
            mism += 1
    if mism:
        fail(f"vocabulary: {mism}/{len(todo)} prompts tokenised differently by the GGUF vocabulary")
    print(f"[gate 1] PASS: {len(todo)}/{len(todo)} prompts give identical ids; "
          f"all {sum(map(len, ids.values()))} digit ids decode to their digit", flush=True)
    del voc

    # ------------------------------------------------------------ gate 2: readings
    rt = R.LlamaRater(n_threads=a.threads)
    print(f"[spike] GGUF loaded in {rt.load_seconds:.1f}s, threads {rt.llm.n_threads}", flush=True)
    rows = []
    t_all = time.perf_counter()
    for reuse in (False, True):
        rt.reuse = reuse
        rt._prev = []
        for i, (pr, r) in enumerate(todo, 1):
            t0 = time.perf_counter()
            p, raw = rt.read(pr, r.lang, r.sent, r.token)
            dt = time.perf_counter() - t0
            n_tok, n_eval = rt.last
            rows.append(dict(reuse=reuse, prompt=pr, lang=r.lang, idx=r.idx,
                             **{f"p{d}": float(x) for d, x in zip(signal_b.DIGITS, p)},
                             raw=raw, score=R.score(p), n_tokens=n_tok, n_evaluated=n_eval,
                             seconds=dt))
            if not reuse and not (raw >= GATE_MASS and np.isfinite(p).all()):
                fail(f"digit mass: {pr} {r.lang} idx {r.idx}: {raw!r} on the digits, p={p}")
            if i % 50 == 0 or i == len(todo):
                done = [x for x in rows if x["reuse"] == reuse]
                print(f"[B reuse={reuse}] {i}/{len(todo)}  "
                      f"{np.mean([x['seconds'] for x in done]):.2f}s per reading", flush=True)
        if not reuse:
            d0 = pd.DataFrame(rows)
            print(f"[gate 2] PASS: min mass on digits {d0['raw'].min():.4f}, no NaN", flush=True)

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    d = pd.DataFrame(rows)
    d.to_csv(a.out, index=False)
    print(f"-> {a.out} ({time.perf_counter() - t_all:.0f}s of readings)", flush=True)

    # ------------------------------------------------------------ gate 3: agreement
    st = pd.read_csv(os.path.join(data.PRED_DIR, "signal_b.csv"), float_precision="round_trip")
    st = st[(st["model"] == R.KEY) & st["prompt"].isin(prompts) & st["idx"].isin(ev["idx"])]
    new = d[~d["reuse"]]
    mean_new = new.groupby("idx")["score"].mean()
    mean_old = st.groupby("idx")["score"].mean()
    j = pd.DataFrame({"new": mean_new, "old": mean_old}).dropna()
    j["lang"] = ev.set_index("idx").loc[j.index, "lang"]
    if len(j) != len(ev):
        fail(f"agreement: stored readings found for {len(j)}/{len(ev)} rows")
    per = {lg: data.pearson(g["new"], g["old"]) for lg, g in j.groupby("lang")}
    pooled = data.pearson(j["new"], j["old"])
    per_prompt = {}
    for pr in prompts:
        a_ = new[new["prompt"] == pr].set_index("idx")["score"]
        b_ = st[st["prompt"] == pr].set_index("idx")["score"]
        per_prompt[pr] = data.pearson(a_, b_.loc[a_.index])
    print("[gate 3] r(mean of 3 prompts, stored) per language: "
          + "  ".join(f"{lg} {v:.4f}" for lg, v in per.items()))
    print(f"[gate 3] pooled r {pooled:.4f} | per prompt, pooled: "
          + "  ".join(f"{k} {v:.4f}" for k, v in per_prompt.items())
          + f" | mean |score diff| {np.abs(j['new'] - j['old']).mean():.4f}", flush=True)

    # ------------------------------------------------------------ KV reuse (not a gate)
    k = ["prompt", "idx"]
    m = new.merge(d[d["reuse"]], on=k, suffixes=("", "_r"))
    dp = np.abs(m[[f"p{x}" for x in signal_b.DIGITS]].values
                - m[[f"p{x}_r" for x in signal_b.DIGITS]].values).max()
    print(f"[kv reuse] {m['n_evaluated_r'].sum()}/{m['n_tokens'].sum()} tokens evaluated with reuse,"
          f" {m['seconds'].mean():.2f}s vs {m['seconds_r'].mean():.2f}s per reading,"
          f" max |dp| {dp:.3g}, partial KV removals refused {rt.refused}", flush=True)

    bad = {lg: v for lg, v in per.items() if not v >= GATE_R_LANG}
    if bad:
        fail("agreement: r below %.2f in %s" % (GATE_R_LANG,
                                               ", ".join(f"{lg} {v:.4f}" for lg, v in bad.items())))
    if not pooled >= GATE_R_POOLED:
        fail(f"agreement: pooled r {pooled:.4f} below {GATE_R_POOLED}")
    print("[gate 3] PASS")
    tps = new["n_evaluated"].sum() / new["seconds"].sum()
    print(f"[spike] all gates pass. CPU: {new['seconds'].mean():.2f}s per reading, "
          f"{new['n_tokens'].mean():.0f} prompt tokens, prefill {tps:.1f} tokens/s")


if __name__ == "__main__":
    main()
