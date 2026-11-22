"""Stage 4 parity gate: the site's code path (lcp/pipeline.py) on MLSP/RoLCP test rows, against the
stage 3 reference built from the stored signals.

For the first --contexts contexts of every language, each context goes through
Pipeline.score_words as a sentence of the site would (one forward pass per crop window through
lcp.encoders, data.lexical with the paper's cached lemma, the pipeline's fertility, the exported
regressors; then the three prompts with KV reuse, prompt by prompt, word by word). The reference for
the same rows: A from the release's cached embeddings with data.lexical and data.fertility through
lcp/fusion.py, B from reference/signal_b_llamacpp.csv through lcp/fusion.py.

Gates, fixed beforehand (exit 1 on the first failure):
  - fertility: Pipeline.fertility == data.fertility on every row;
  - A: r(zA site, zA reference) >= 0.9999 in every language;
  - B: r(zB) >= 0.99 in every language and >= 0.995 pooled (re-reading on the GPU with KV reuse is
    not bit-identical: r 0.9991 between modes in stage 7);
  - fused: pooled r >= 0.998, and the same level for at least 95% of the words.

  docker/run_cuda.sh python scripts/pipeline_check.py
Writes bench/results/pipeline_check.txt (numbers only, no text).
"""
import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import data                                    # noqa: E402  (lcp_model on PYTHONPATH)
import signal_a                                # noqa: E402
import export_model as X                       # noqa: E402
from lcp.fusion import Fusion                  # noqa: E402
from lcp.paper import use_release              # noqa: E402

LOG = []


def say(msg=""):
    print(msg, flush=True)
    LOG.append(msg)


def stop(msg, out):
    say(f"\n[GATE FAILED] {msg}")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(LOG) + "\n")
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--paper-release", default="/paper/release")
    ap.add_argument("--contexts", type=int, default=6, help="first contexts per language")
    ap.add_argument("--reference", default="reference/signal_b_llamacpp.csv")
    ap.add_argument("--out", default="bench/results/pipeline_check.txt")
    a = ap.parse_args()
    use_release(a.paper_release)
    data._lemmatize = X._no_lemmatize
    ev = data.load_eval(True)
    (lem,) = data.lemmas([("test", ev)])
    ev["lemma"] = lem

    # rows: first contexts of each language, in idx order
    rows = []
    for lg, g in ev.groupby("lang"):
        keep = list(dict.fromkeys(g.sort_values("idx")["context_id"]))[:a.contexts]
        rows.append(g[g["context_id"].isin(keep)].sort_values("idx"))
    ev_s = pd.concat(rows)
    say(f"[check] {len(ev_s)} rows in {ev_s['context_id'].nunique()} contexts "
        f"({a.contexts} per language)")

    # ------------------------------------------------------------ reference
    fz = Fusion()
    ref = {}
    fert_ref = data.fertility(list(ev_s["token"]))
    lex_ref = data.lexical(list(ev_s["token"]), list(ev_s["lang"]), list(ev_s["lemma"]))
    pos = {ix: k for k, ix in enumerate(ev_s["idx"])}
    arms = {e: (np.full(len(ev_s), np.nan), np.full(len(ev_s), np.nan)) for e in fz.encoders}
    for e in fz.encoders:
        Eev, okev = signal_a.embed_cached(X.CachedOnly(e), ev, "eval_ro")
        sel = ev_s["idx"].values
        for lg in ev_s["lang"].unique():
            m = (ev_s["lang"] == lg).values
            ix = sel[m]
            Fx = fz.features(e, lg, Eev[ix], lex_ref[m], fert_ref[m])
            pe, pm = fz.arms(e, lg, Fx)
            arms[e][0][m], arms[e][1][m] = pe, pm
    zA_ref = np.zeros(len(ev_s))
    for lg in ev_s["lang"].unique():
        m = (ev_s["lang"] == lg).values
        zA_ref[m] = fz.a_z(lg, {e: (arms[e][0][m], arms[e][1][m]) for e in fz.encoders})
    st = pd.read_csv(a.reference, float_precision="round_trip").set_index(["prompt", "idx"])
    pc = [f"p{k}" for k in "12345"]
    zB_ref = np.zeros(len(ev_s))
    for lg in ev_s["lang"].unique():
        m = (ev_s["lang"] == lg).values
        ix = ev_s["idx"].values[m]
        Ps = {p: st.loc[[(p, i) for i in ix], pc].values.astype(float) for p in fz.params["b"]["prompts"]}
        zB_ref[m] = fz.b_z(lg, fz.b_raw(lg, Ps))
    fused_ref = np.zeros(len(ev_s))
    for lg in ev_s["lang"].unique():
        m = (ev_s["lang"] == lg).values
        fused_ref[m] = fz.fused(lg, zA_ref[m], zB_ref[m])

    # ------------------------------------------------------------ the site's path
    from lcp.pipeline import Pipeline
    t0 = time.perf_counter()
    P = Pipeline()
    say(f"[check] pipeline loaded in {time.perf_counter() - t0:.1f}s, config {P.config}, "
        f"prompt limit {P.limit} tokens")
    fert_site = P.fertility(list(ev_s["token"]))
    if not np.array_equal(fert_site, fert_ref):
        stop(f"fertility differs on {(fert_site != fert_ref).sum()} rows", a.out)
    say(f"[gate] fertility: identical to data.fertility on {len(ev_s)} rows")

    out = {}
    n_read = 0
    t_b = 0.0
    P.rt._prev = []
    for ctx, g in ev_s.groupby("context_id", sort=False):
        text = str(g["sent"].iloc[0]).replace("\n", " ").strip()
        words, ids = [], []
        for r in g.itertuples():
            sp = data.find_char_span(text, str(r.token))
            if sp is None:
                stop(f"target not found in its context (idx {r.idx})", a.out)
            words.append((sp[0], sp[1], str(r.token).strip(), r.lemma))
            ids.append(r.idx)
        res, s = P.score_words(g["lang"].iloc[0], text, words)
        n_read += s["readings"]
        t_b += s["t_B"]
        for ix, w in zip(ids, res):
            out[ix] = w
    zA = np.array([out[i]["A"] for i in ev_s["idx"]])
    zB = np.array([out[i]["B"] for i in ev_s["idx"]])
    fused = np.array([out[i]["fused"] for i in ev_s["idx"]])
    lv = np.array([out[i]["level"] for i in ev_s["idx"]])
    lv_ref = fz.level(np.concatenate([fz.score01(lg, fused_ref[(ev_s["lang"] == lg).values])
                                      for lg in ev_s["lang"].unique()]))
    cropped = sum(1 for w in out.values() if w.get("cropped"))
    say(f"[check] {n_read} readings, {t_b / max(n_read, 1):.3f}s per reading; cropped {cropped}")

    # outputs are rounded (A, B to 3 decimals, fused to 4), so |d| below ~5e-4 is rounding
    langs = list(ev_s["lang"].unique())
    rA, rB = {}, {}
    for lg in langs:
        m = (ev_s["lang"] == lg).values
        rA[lg] = data.pearson(zA[m], zA_ref[m])
        rB[lg] = data.pearson(zB[m], zB_ref[m])
    say("[gate] A: r per language " + "  ".join(f"{lg} {v:.5f}" for lg, v in rA.items())
        + f" | max |dA| {np.abs(zA - zA_ref).max():.4f} (outputs rounded to 1e-3)")
    say("[gate] B: r per language " + "  ".join(f"{lg} {v:.4f}" for lg, v in rB.items())
        + f" | pooled {data.pearson(zB, zB_ref):.4f}, max |dB| {np.abs(zB - zB_ref).max():.3f}, "
        f"median {np.median(np.abs(zB - zB_ref)):.4f}")
    rF = data.pearson(fused, fused_ref)
    same = float((lv == lv_ref).mean())
    say(f"[gate] fused: pooled r {rF:.5f}, max |d| {np.abs(fused - fused_ref).max():.4f}; "
        f"same level {100 * same:.1f}% ({(lv == lv_ref).sum()}/{len(lv)}), "
        f"off by more than one level {(np.abs(lv - lv_ref) > 1).sum()}")
    bad = {lg: v for lg, v in rA.items() if not v >= 0.9999}
    if bad:
        stop(f"A: r below 0.9999 in {bad}", a.out)
    bad = {lg: v for lg, v in rB.items() if not v >= 0.99}
    if bad or not data.pearson(zB, zB_ref) >= 0.995:
        stop(f"B: r below the gate ({bad}, pooled {data.pearson(zB, zB_ref):.4f})", a.out)
    if not (rF >= 0.998 and same >= 0.95):
        stop(f"fused: r {rF:.5f} or same level {same:.3f} below the gate", a.out)
    say("[gate] PASS")
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(LOG) + "\n")
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
