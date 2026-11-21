"""Correlation tables for the documentation (Section 4): signal A against signal B per language, the
language models of signal B against each other, the three prompts of Gemma 4 against each other, the
ridge regression against HGB inside signal A per language, and the three encoders against each other.

Everything comes from the stored predictions: output/doc_fuse_ro11.csv (fuse.py --with-ro --out),
release/predictions/signal_b.csv and output/doc_qwen_ro_signal_b.csv (the Qwen rows for Romanian, see
output/doc_ablations_qwen_ro.txt), output/doc_signal_a_models/signal_a_{ridge,hgb}.csv (see
analysis_doc_signal_a_models.py) and release/predictions/signal_a.csv. release/ is imported, never modified. Every correlation is a Pearson
correlation within one language; means are over the 11 languages.

Usage (envs ml_def):  python analysis_doc_correlations.py > output/doc_correlations.txt
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
REL = os.path.join(ROOT, "release")
sys.path.insert(0, REL)
os.chdir(REL)
import data  # noqa: E402
import fuse  # noqa: E402

GEMMA, QWEN3, QWEN35 = "gemma4-12b-4bit", "qwen3-8b-4bit", "qwen35-9b-8bit"
B_ALL = pd.concat([pd.read_csv(os.path.join(data.PRED_DIR, "signal_b.csv")),
                   pd.read_csv(os.path.join(ROOT, "output", "doc_qwen_ro_signal_b.csv"))],
                  ignore_index=True)
DEFAULT = dict(T_GRID=fuse.T_GRID, PARTITIONS=fuse.PARTITIONS, NEUTRAL=fuse.NEUTRAL)


def load_b(ev, model, prompts=None, **settings):
    """fuse.load_b for one model on B_ALL, with optional prompt filter and fuse.py settings."""
    for k, v in {**DEFAULT, **settings}.items():
        setattr(fuse, k, v)
    b = B_ALL if prompts is None else B_ALL[B_ALL["prompt"].isin(prompts)]
    read_csv = pd.read_csv
    pd.read_csv = lambda p, *a, **kw: b.copy() if str(p).endswith("signal_b.csv") else read_csv(p, *a, **kw)
    try:
        out = fuse.load_b(ev, [model])[model].set_index("idx")
    finally:
        pd.read_csv = read_csv
        for k, v in DEFAULT.items():
            setattr(fuse, k, v)
    return out


def corr_table(cols, lang):
    """Mean over languages of the within-language Pearson correlation of every pair of columns."""
    names = list(cols)
    langs = sorted(set(lang))
    C = pd.DataFrame(index=names, columns=names, dtype=float)
    for a in names:
        for b in names:
            C.loc[a, b] = np.mean([np.corrcoef(cols[a][lang == l], cols[b][lang == l])[0, 1]
                                   for l in langs])
    return C


def signal_a_one_setup(ev, encoders):
    """Signal A as it enters the fusion of fuse.py --with-ro --encoders ...: w_src chosen on the other
    languages, exactly as in fuse.main. Returns a Series indexed by idx and the mean r_A."""
    A = fuse.load_a("mlsp+ro", encoders)
    Bs = fuse.load_b(ev, None)
    y = ev.set_index("idx")["complexity"]
    r_b = {m: {lg: data.pearson(g["B"].values, y.loc[g["idx"]].values)
               for lg, g in f.groupby("lang")} for m, f in Bs.items()}
    parts, r_a = [], []
    for lg, d in fuse.signals(ev, A, Bs, r_b, exclude=()).items():
        fit_langs = {l: f for l, f in fuse.signals(ev, A, Bs, r_b, exclude={lg}).items() if l != lg}
        w_src, _ = fuse.fit(fit_langs)
        zA = fuse.z_a(d, w_src)
        parts.append(pd.Series(zA, index=d["idx"].values))
        r_a.append(data.pearson(zA, d["complexity"].values))
    return pd.concat(parts), float(np.mean(r_a))


def main():
    ev = data.load_eval(True)
    d = pd.read_csv(os.path.join(ROOT, "output", "doc_fuse_ro11.csv"))
    print("Correlation tables for the documentation. Written by analysis_doc_correlations.py from "
          "output/doc_fuse_ro11.csv,\nrelease/predictions/signal_b.csv and output/doc_qwen_ro_signal_b.csv. "
          "Pearson within each language.\n")

    print("1. Signal A against signal B, as they enter the fusion (fuse.py --with-ro), with r of each:")
    y = ev.set_index("idx")["complexity"]
    rows = []
    for l, g in d.groupby("lang"):
        yl = y.loc[g["idx"]].values
        rows.append(dict(lang=l, rho_AB=np.corrcoef(g["A"], g["B"])[0, 1], r_A=data.pearson(g["A"], yl),
                         r_B=data.pearson(g["B"], yl), r_fused=data.pearson(g["fused"], yl)))
    t = pd.DataFrame(rows).set_index("lang")
    t.loc["mean"] = t.mean()
    print(t.to_string(float_format=lambda v: f"{v:.4f}"))
    print(f"Spearman, over the 11 languages, of rho(A,B) with r_fused - max(r_A, r_B): "
          f"{t.iloc[:-1]['rho_AB'].corr(t.iloc[:-1]['r_fused'] - t.iloc[:-1][['r_A', 'r_B']].max(axis=1), method='spearman'):.3f}")

    print("\n2. Signal B of the language models (each as the only candidate, as in Table 2 rows):")
    ref = load_b(ev, GEMMA)
    idx = ref.index.values
    lang = ref["lang"].values
    cols = {"Gemma 4": ref["B"].values,
            "Gemma 4, Qwen reading": load_b(ev, GEMMA, prompts=["expert", "short"], T_GRID=(1.0,),
                                            PARTITIONS=[DEFAULT["PARTITIONS"][DEFAULT["NEUTRAL"]]],
                                            NEUTRAL=0).loc[idx, "B"].values,
            "Qwen3 8B": load_b(ev, QWEN3).loc[idx, "B"].values,
            "Qwen3.5 9B": load_b(ev, QWEN35).loc[idx, "B"].values}
    print(corr_table(cols, lang).to_string(float_format=lambda v: f"{v:.3f}"))

    print("\n3. The three prompts of Gemma 4, each read with the temperature and grouping chosen for its "
          "test language in the full method:")
    wide = {p: B_ALL[(B_ALL["model"] == GEMMA) & (B_ALL["prompt"] == p)].set_index("idx")
            for p in ("expert", "short", "marked")}
    pcols = [f"p{k}" for k in "12345"]
    out = {p: np.empty(len(idx)) for p in wide}
    for l in sorted(set(lang)):
        m = lang == l
        T = float(ref.loc[idx[m], "T"].iloc[0])
        part = [[int(c) - 1 for c in blk] for blk in ref.loc[idx[m], "partition"].iloc[0].split("|")]
        for p, w in wide.items():
            out[p][m] = fuse.b_of([w.loc[idx[m], pcols].values.astype(float)], T, part)
    print(corr_table(out, lang).to_string(float_format=lambda v: f"{v:.3f}"))
    yy = y.loc[idx].values
    print("r with ground truth, mean over languages: " + ", ".join(
        f"{p} {np.mean([data.pearson(out[p][lang == l], yy[lang == l]) for l in sorted(set(lang))]):.4f}"
        for p in out))

    print("\n4. Signal A with ridge alone against signal A with HGB alone, each as it enters the fusion "
          "(output/doc_signal_a_models, the rows Ridge and HGB of output/doc_signal_a_models.txt):")
    import analysis_doc_signal_a_models as sam
    ridge, hgb = sam.fuse_with("ridge"), sam.fuse_with("hgb")
    rh = pd.Series({l: np.corrcoef(ridge[l]["zA"], hgb[l]["zA"])[0, 1] for l in sorted(ridge)})
    assert all((ridge[l]["idx"] == hgb[l]["idx"]).all() for l in rh.index)
    rh.loc["mean"] = rh.mean()
    print(rh.to_frame("rho_ridge_hgb").to_string(float_format=lambda v: f"{v:.4f}"))

    print("\n5. Signal A with one encoder only (fuse.py --with-ro --encoders <one>), each as it enters "
          "the fusion:")
    enc = {}
    for e, name in (("xlmr", "XLM-R base"), ("labse", "LaBSE"), ("e5", "Multilingual E5 base")):
        a_e, r_a = signal_a_one_setup(ev, [e])
        enc[name] = a_e.loc[idx].values
        print(f"   {name}: mean r_A {r_a:.6f} (check against output/doc_ablations.txt)")
    print(corr_table(enc, lang).to_string(float_format=lambda v: f"{v:.3f}"))
    print("per language:")
    print(pd.DataFrame({f"{a} - {b}": {l: np.corrcoef(enc[a][lang == l], enc[b][lang == l])[0, 1]
                                       for l in sorted(set(lang))}
                        for i, a in enumerate(enc) for b in list(enc)[i + 1:]})
          .to_string(float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
