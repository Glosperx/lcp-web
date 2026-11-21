"""Claude baselines for Table 3 of the documentation, recomputed on the release predictions.

The Claude ratings (output/doc_claude/{opus,sonnet}_preds_11lang.csv, copied on 11 Oct 2026 from the
separate Claude session) give each test item a 1-5 and a 0-100 score. The Claude rating is the mean
of the two, each standardised within the language, as in that session.

Three predictors per Claude model, with the fusion of release/fuse.py:
  - Claude alone;
  - signal A + Claude: the Claude rating replaces signal B, and (w_src, w) are chosen leave-one-
    language-out with fuse.fit, exactly as for the full method;
  - full method + Claude: w * z(Claude) + (1 - w) * z(full method), the full method read from
    output/doc_fuse_{ro11,mlsp10}.csv and w chosen on the other languages (mean r, fuse.W_GRID).
Also the correlations between the Claude rating and signal A, signal B and the full method, per
language. Every interval resamples contexts with data.boot_r (same seed, same row order in every
run), so differences are paired, as in analysis_doc_ablations_extra.py.

release/ is imported, never modified.

Usage (envs ml_def):  python analysis_doc_claude.py > output/doc_claude.txt
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
CLAUDE_DIR = os.path.join(ROOT, "output", "doc_claude")
sys.path.insert(0, ROOT)
import analysis_doc_ablations_extra as abl  # noqa: E402  (chdir to release/, imports data and fuse)

data, fuse = abl.data, abl.fuse
CLAUDE = {"sonnet": "sonnet_preds_11lang.csv", "opus": "opus_preds_11lang.csv"}
FUSED = {True: "doc_fuse_ro11.csv", False: "doc_fuse_mlsp10.csv"}


def load_claude(ev, name):
    """Frame idx, lang, B (the Claude rating), aligned to ev by language and row order."""
    c = pd.read_csv(os.path.join(CLAUDE_DIR, CLAUDE[name]), keep_default_na=False)
    out = []
    for lg, g in ev.groupby("lang", sort=True):
        cg = c[c["lang"] == lg].reset_index(drop=True)
        if len(cg) != len(g):
            raise SystemExit(f"{name} {lg}: {len(cg)} ratings for {len(g)} items")
        bad = int((cg["token"].astype(str).values != g["token"].astype(str).values).sum())
        if bad:
            raise SystemExit(f"{name} {lg}: {bad} targets differ from the evaluation frame")
        z = data.zscore(cg["score5"].astype(float)) + data.zscore(cg["score100"].astype(float))
        out.append(pd.DataFrame({"idx": g["idx"].values, "lang": lg, "B": z / 2}))
    return pd.concat(out, ignore_index=True).sort_values("idx").reset_index(drop=True)


def boot(d, p):
    return data.boot_r(d["complexity"].values, p, d["context_id"].values, 2000)


def run(with_ro):
    ev = data.load_eval(with_ro)
    A = fuse.load_a("mlsp+ro" if with_ro else "mlsp", ["xlmr", "labse", "e5"])
    y = ev.set_index("idx")["complexity"]
    F = pd.read_csv(os.path.join(ROOT, "output", FUSED[with_ro])).set_index("idx")
    res = {"method": abl.run(with_ro)}  # {lang: {"F"|"A"|"B": (r, samples)}}, the full method
    corr, weights = {}, {}
    for name in CLAUDE:
        Bs = {name: load_claude(ev, name)}
        r_b = {name: {lg: data.pearson(g["B"].values, y.loc[g["idx"]].values)
                      for lg, g in Bs[name].groupby("lang")}}
        test = fuse.signals(ev, A, Bs, r_b, exclude=())
        zc = {lg: d["zB"].values for lg, d in test.items()}
        zf = {lg: data.zscore(F.loc[d["idx"], "fused"].values) for lg, d in test.items()}
        M = {lg: fuse.moments(zc[lg], zf[lg], d["complexity"].values) for lg, d in test.items()}
        alone, with_a, with_m = {}, {}, {}
        for lg, d in test.items():
            fit_langs = {l: f for l, f in fuse.signals(ev, A, Bs, r_b, exclude={lg}).items() if l != lg}
            w_src, w = fuse.fit(fit_langs)
            zA = fuse.z_a(d, w_src)
            curve = [np.mean([fuse.r_mom(M[l], v) for l in M if l != lg]) for v in fuse.W_GRID]
            wc = float(fuse.W_GRID[int(np.argmax(curve))])
            alone[lg] = {"F": boot(d, zc[lg])}
            with_a[lg] = {"F": boot(d, w * zA + (1 - w) * zc[lg])}
            with_m[lg] = {"F": boot(d, wc * zc[lg] + (1 - wc) * zf[lg])}
            weights[(name, lg)] = (w_src, 1 - w, wc)
            A_m = F.loc[d["idx"], "A"].values
            B_m = F.loc[d["idx"], "B"].values
            corr[(name, lg)] = (data.pearson(zc[lg], A_m), data.pearson(zc[lg], B_m),
                                data.pearson(zc[lg], F.loc[d["idx"], "fused"].values))
        res[name] = alone
        res[f"A + {name}"] = with_a
        res[f"method + {name}"] = with_m
    return res, corr, weights


def ci(o, k="F"):
    m = min(len(v[k][1]) for v in o.values())
    s = np.mean([v[k][1][:m] for v in o.values()], axis=0)
    lo, hi = np.percentile(s, [2.5, 97.5])
    return f"{abl.mean(o, k):.6f} [{lo:.4f}, {hi:.4f}]"


def main():
    pd.set_option("display.width", 200)
    for ro in (True, False):
        n = 11 if ro else 10
        res, corr, weights = run(ro)
        base = res["method"]
        langs = sorted(base)
        print(f"\n=== {n} languages ===")
        print(f"  {'signal A':22s} {ci(base, 'A')}")
        print(f"  {'signal B':22s} {ci(base, 'B')}")
        print(f"  {'full method':22s} {ci(base)}")
        for k in ("sonnet", "opus", "A + sonnet", "A + opus", "method + sonnet", "method + opus"):
            print(f"  {k:22s} {ci(res[k])}")
        print("\npaired differences (mean over languages, 95% interval, languages where the first is higher):")
        pairs = [("sonnet", "method", "F", "F"), ("opus", "method", "F", "F"),
                 ("opus", "sonnet", "F", "F"), ("sonnet", "method", "F", "B"),
                 ("A + sonnet", "method", "F", "F"), ("A + opus", "method", "F", "F"),
                 ("A + sonnet", "sonnet", "F", "F"), ("A + opus", "opus", "F", "F"),
                 ("method + sonnet", "method", "F", "F"), ("method + opus", "method", "F", "F"),
                 ("method + sonnet", "sonnet", "F", "F"), ("method + opus", "opus", "F", "F"),
                 ("method + opus", "A + opus", "F", "F"), ("method + sonnet", "A + sonnet", "F", "F")]
        for a, b, ka, kb in pairs:
            lb = "signal B" if kb == "B" else b
            print(f"  {a:16s} - {lb:12s} {abl.paired(res[a], res[b], ka, kb)}")

        print(f"\nper-language r ({n} languages):")
        t = pd.DataFrame({"A": {l: base[l]["A"][0] for l in langs},
                          "B": {l: base[l]["B"][0] for l in langs},
                          "method": {l: base[l]["F"][0] for l in langs}})
        for k in ("sonnet", "opus", "A + sonnet", "A + opus", "method + sonnet", "method + opus"):
            t[k] = {l: res[k][l]["F"][0] for l in langs}
        print(t.to_string(float_format=lambda v: f"{v:.4f}"))
        print(t.mean().to_frame("mean").T.to_string(float_format=lambda v: f"{v:.6f}"))

        print(f"\nweights chosen leave-one-language-out ({n} languages): w_src and the Claude weight in"
              " A + Claude; the Claude weight in method + Claude")
        w = pd.DataFrame({f"{m} {c}": {l: weights[(m, l)][i] for l in langs}
                          for m in CLAUDE for i, c in enumerate(("w_src", "w_claude(A+)", "w_claude(m+)"))})
        print(w.to_string(float_format=lambda v: f"{v:.3f}"))

        print(f"\nPearson correlation of the Claude rating with signal A, signal B (Gemma 4) and the full"
              f" method, per language ({n} languages; A, B and method as in output/{FUSED[ro]}):")
        c = pd.DataFrame({f"{m} {s}": {l: corr[(m, l)][i] for l in langs}
                          for m in CLAUDE for i, s in enumerate(("~A", "~B", "~method"))})
        print(c.to_string(float_format=lambda v: f"{v:.4f}"))
        print(c.mean().to_frame("mean").T.to_string(float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
