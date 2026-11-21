"""Extra ablations for Table 2 of the documentation, with paired bootstrap intervals.

Runs the fusion of release/fuse.py on the stored predictions (no language model and no encoder is
run) under settings that fuse.py has no flag for: temperature fixed at 1, no grouping of ratings,
a subset of the prompts, one regressor only, and Gemma 4 restricted to the reading stored for the
Qwen models. release/ is imported, never modified; the settings are changed on the module at run
time. The Romanian Qwen rows come from output/doc_qwen_ro_signal_b.csv (run on 10 Oct 2026 in a
copy of release/, see output/doc_ablations_qwen_ro.txt).

Every difference is paired: data.boot_r uses the same seed and the same contexts in every run, so
resample k of a language is the same set of contexts in the full method and in the ablation. The
interval of a difference in the mean over languages is the 2.5th and 97.5th percentile of the
per-resample differences, averaged over languages as in fuse.py.

Also prints, per language, the share of targets with word frequency 0 (not listed by wordfreq).

Usage (envs ml_def):  python analysis_doc_ablations_extra.py > output/doc_ablations_extra.txt
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
REL = os.path.join(ROOT, "release")
QWEN_RO = os.path.join(ROOT, "output", "doc_qwen_ro_signal_b.csv")
sys.path.insert(0, REL)
os.chdir(REL)
import data  # noqa: E402
import fuse  # noqa: E402

GEMMA = "gemma4-12b-4bit"
DEFAULT = dict(T_GRID=fuse.T_GRID, PARTITIONS=fuse.PARTITIONS, NEUTRAL=fuse.NEUTRAL,
               SRC_GRID=fuse.SRC_GRID)
B_ALL = pd.read_csv(os.path.join(data.PRED_DIR, "signal_b.csv"))
B_ALL = pd.concat([B_ALL, pd.read_csv(QWEN_RO)], ignore_index=True)


def run(with_ro, encoders=("xlmr", "labse", "e5"), models=None, prompts=None, **settings):
    """fuse.main without printing: {lang: {"F"|"A"|"B": (r, bootstrap samples)}}."""
    for k, v in {**DEFAULT, **settings}.items():
        setattr(fuse, k, v)
    b = B_ALL if prompts is None else B_ALL[B_ALL["prompt"].isin(prompts)]
    read_csv = pd.read_csv
    pd.read_csv = lambda p, *a, **kw: b.copy() if str(p).endswith("signal_b.csv") else read_csv(p, *a, **kw)
    try:
        ev = data.load_eval(with_ro)
        A = fuse.load_a("mlsp+ro" if with_ro else "mlsp", list(encoders))
        Bs = fuse.load_b(ev, models)
    finally:
        pd.read_csv = read_csv
    y = ev.set_index("idx")["complexity"]
    r_b = {m: {lg: data.pearson(g["B"].values, y.loc[g["idx"]].values)
               for lg, g in f.groupby("lang")} for m, f in Bs.items()}
    out = {}
    for lg, d in fuse.signals(ev, A, Bs, r_b, exclude=()).items():
        fit_langs = {l: f for l, f in fuse.signals(ev, A, Bs, r_b, exclude={lg}).items() if l != lg}
        w_src, w = fuse.fit(fit_langs)
        zA = fuse.z_a(d, w_src)
        P = w * zA + (1 - w) * d["zB"].values
        y_l, g = d["complexity"].values, d["context_id"].values
        out[lg] = {k: data.boot_r(y_l, v, g, 2000) for k, v in
                   (("F", P), ("A", zA), ("B", d["zB"].values))}
    for k, v in DEFAULT.items():
        setattr(fuse, k, v)
    return out


def mean(o, k="F"):
    return float(np.mean([v[k][0] for v in o.values()]))


def paired(o, base, k="F", kb="F"):
    """Difference in the mean over languages, its 95% interval, languages where o is higher."""
    langs = sorted(base)
    m = min(min(len(o[l][k][1]), len(base[l][kb][1])) for l in langs)
    s = np.mean([o[l][k][1][:m] - base[l][kb][1][:m] for l in langs], axis=0)
    lo, hi = np.percentile(s, [2.5, 97.5])
    wins = sum(o[l][k][0] > base[l][kb][0] for l in langs)
    return f"{mean(o, k) - mean(base, kb):+.4f} [{lo:+.4f}, {hi:+.4f}] higher on {wins}/{len(langs)}"


def main():
    pd.set_option("display.width", 200)
    for ro in (True, False):
        n = 11 if ro else 10
        base = run(ro)
        print(f"\n=== {n} languages ({'fuse.py --with-ro' if ro else 'fuse.py'}) ===")
        print(f"full method: fused {mean(base):.6f} | A {mean(base, 'A'):.6f} | B {mean(base, 'B'):.6f}")
        print(f"  signal A only  vs full: {paired(base, base, 'A', 'F')}")
        print(f"  signal B only  vs full: {paired(base, base, 'B', 'F')}")
        rows = [
            ("XLM-R base only", dict(encoders=("xlmr",))),
            ("LaBSE only", dict(encoders=("labse",))),
            ("multilingual E5 base only", dict(encoders=("e5",))),
            ("plus XLM-R large", dict(encoders=("xlmr", "labse", "e5", "xlmr-large"))),
            ("T fixed at 1 (grouping still chosen)", dict(models=[GEMMA], T_GRID=(1.0,))),
            ("no grouping (T still chosen)", dict(models=[GEMMA], PARTITIONS=[DEFAULT["PARTITIONS"][DEFAULT["NEUTRAL"]]], NEUTRAL=0)),
            ("prompt expert only", dict(models=[GEMMA], prompts=["expert"])),
            ("prompt short only", dict(models=[GEMMA], prompts=["short"])),
            ("prompt marked only", dict(models=[GEMMA], prompts=["marked"])),
            ("prompts expert and short", dict(models=[GEMMA], prompts=["expert", "short"])),
            ("English regressor only (w_src = 1)", dict(SRC_GRID=np.array([1.0]))),
            ("multilingual regressor only (w_src = 0)", dict(SRC_GRID=np.array([0.0]))),
            ("Gemma 4 as stored for Qwen (expert+short, T = 1, no grouping)",
             dict(models=[GEMMA], prompts=["expert", "short"], T_GRID=(1.0,),
                  PARTITIONS=[DEFAULT["PARTITIONS"][DEFAULT["NEUTRAL"]]], NEUTRAL=0)),
            ("Qwen3 8B only", dict(models=["qwen3-8b-4bit"])),
            ("Qwen3.5 9B only", dict(models=["qwen35-9b-8bit"])),
        ]
        per_lang = {"full method": base}
        for name, kw in rows:
            o = run(ro, **kw)
            per_lang[name] = o
            print(f"  {name}: fused {mean(o):.6f} | A {mean(o, 'A'):.6f} | B {mean(o, 'B'):.6f}")
            print(f"      fused vs full {paired(o, base)} | B vs full B {paired(o, base, 'B', 'B')}")
        print(f"\nper-language fused r ({n} languages):")
        t = pd.DataFrame({k: {l: v[l]["F"][0] for l in v} for k, v in per_lang.items()}).T
        print(t.to_string(float_format=lambda v: f"{v:.4f}"))

    print("\ngrouping chosen for Gemma 4 when T is fixed at 1 (11 languages):")
    fuse.T_GRID = (1.0,)
    ev = data.load_eval(True)
    B = fuse.load_b(ev, [GEMMA])[GEMMA]
    fuse.T_GRID = DEFAULT["T_GRID"]
    print(" ".join(f"{l} {p}" for l, p in B.groupby("lang")["partition"].first().items()))

    lem_ev, _ = data.lemmas([("test", ev), ("complex_en", data.load_complex_en().assign(lang="en"))])
    lex = data.lexical(list(ev["token"]), list(ev["lang"]), lem_ev)
    share = pd.Series(lex[:, 0] == 0).groupby(ev["lang"].values).mean()
    print("\nshare of targets with word frequency 0 (release/data.py lexical, column 0):")
    print(" ".join(f"{l} {v:.3f}" for l, v in share.items()))


if __name__ == "__main__":
    main()
