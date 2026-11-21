"""SHAP of the adopted signal A with the embedding split by encoder, for the documentation figure.

Same computation as analysis_shap_signal_a.py (same models, same language background, same three
controls), reused from it. The only difference is the grouping: that script sums dimension j of the
three encoders into one embedding row, which cannot be undone from its saved values, so the per-encoder
contributions are recomputed here. The lexical columns are the same for the three encoders and stay
summed. Labels name what each column is (fertility, frequency of form or lemma).

Run (envs/ml_def, about 15 minutes, embeddings are cached):
  python analysis_shap_signal_a_per_encoder.py --blocks DIR
  python analysis_shap_signal_a_per_encoder.py --plot-only
Outputs: output/shap_signal_a_per_encoder_lexical.{pdf,png} (beeswarm, main text),
output/shap_signal_a_per_encoder_all_inputs.{pdf,png} (beeswarm, appendix), output/shap_signal_a_per_encoder_correlations.csv,
output/shap_signal_a_per_encoder_importance.csv,
output/shap_signal_a_per_encoder_raw.npz, plus the copies figures/fig_shap_signal_a.pdf and fig_shap_signal_a_all.pdf.
The outputs of analysis_shap_signal_a.py are not touched.
"""
import argparse
import os
import shutil
import tempfile

import numpy as np
import pandas as pd

import analysis_shap_signal_a as base_script
from analysis_shap_signal_a import D, ENCODERS, FUSION, OUT, FIG, TOL_A, TOL_SUM, encoder_arms, zscore

ENC_NAMES = {"xlmr": "Embedding, XLM-R base", "labse": "Embedding, LaBSE",
             "e5": "Embedding, multilingual E5 base"}
LEX = ["Subword count (fertility)", "Word frequency (max of form and lemma)", "Syllable count",
       "Capitalised first letter", "No frequency list (flag)", "Non-Latin script (flag)"]
assert len(LEX) == len(base_script.LEX)
SHORT = {"Embedding, XLM-R base": "XLM-R embedding", "Embedding, LaBSE": "LaBSE embedding",
         "Embedding, multilingual E5 base": "mE5 embedding", LEX[0]: "Subword count",
         LEX[1]: "Word frequency", LEX[2]: "Syllable count", LEX[3]: "Capitalised"}
RAW = os.path.join(OUT, "shap_signal_a_per_encoder_raw.npz")
STEM = os.path.join(OUT, "shap_signal_a_per_encoder")


def compose_per_encoder(arms, fus):
    """As analysis_shap_signal_a.compose, but keeps the contribution of each encoder apart."""
    idx, lang = arms[0]["idx"], arms[0]["lang"]
    n, w = arms[0]["X"].shape
    k = len(arms)
    A, base = np.empty(n), np.empty(n)
    phi = [np.empty((n, w)) for _ in arms]
    for L in sorted(pd.unique(lang)):
        m = lang == L
        w_src = fus.loc[idx[m], "w_src"].unique()
        assert len(w_src) == 1, (L, w_src)
        w_src = float(w_src[0])
        pe = sum(zscore(a["p_en"][m]) for a in arms) / k
        pm = sum(zscore(a["p_mu"][m]) for a in arms) / k
        mix = w_src * zscore(pe) + (1 - w_src) * zscore(pm)
        A[m] = zscore(mix)
        s_pe, s_pm, s_mix = pe.std(), pm.std(), mix.std()
        lin, b = 0.0, 0.0
        for i, a in enumerate(arms):
            c_en = w_src / (k * a["p_en"][m].std() * s_pe * s_mix)
            c_mu = (1 - w_src) / (k * a["p_mu"][m].std() * s_pm * s_mix)
            lin = lin + c_en * a["p_en"][m] + c_mu * a["p_mu"][m]
            phi[i][m] = c_en * a["f_en"][m] + c_mu * a["f_mu"][m]
            b = b + c_en * a["b_en"][m] + c_mu * a["b_mu"][m]
        const = A[m] - lin
        assert np.ptp(const) < 1e-9, (L, np.ptp(const))
        base[m] = b + const.mean()
        assert np.abs(base[m]).max() < TOL_SUM, (L, np.abs(base[m]).max())
    return A, phi, base


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--blocks", default=os.path.join(tempfile.gettempdir(), "shap_signal_a_blocks"))
    ap.add_argument("--plot-only", action="store_true")
    a = ap.parse_args()
    if a.plot_only:
        return plot(RAW)
    os.makedirs(a.blocks, exist_ok=True)

    arms = [encoder_arms(e, a.blocks) for e in ENCODERS]
    for x in arms[1:]:
        assert np.array_equal(x["idx"], arms[0]["idx"])
        assert np.allclose(x["X"][:, D:], arms[0]["X"][:, D:], equal_nan=True, rtol=0, atol=1e-6)

    fus = pd.read_csv(FUSION).set_index("idx")
    A, phi, base = compose_per_encoder(arms, fus)
    total = sum(phi)
    err_a = np.abs(A - fus.loc[arms[0]["idx"], "A"].values).max()
    err_s = np.abs(total.sum(1) + base - A).max()
    print(f"control 2: max |A - A fusion| = {err_a:.2e}\ncontrol 3: max |SHAP + base - A| = {err_s:.2e}")
    if err_a > TOL_A or err_s > TOL_SUM:
        raise SystemExit("controls 2/3 failed, no figure")

    # One embedding row per encoder, then the lexical columns summed over the encoders.
    X, lang = arms[0]["X"], arms[0]["lang"]
    G = np.column_stack([p[:, :D].sum(1) for p in phi] + [total[:, D:]])
    names = [ENC_NAMES[e] for e in ENCODERS] + LEX
    vals = X[:, D:].astype(float).copy()
    vals[vals[:, 4] == 1, 1] = np.nan          # zipf 0 where no frequency list exists: grey, not "rare"
    data = np.column_stack([np.full((len(X), len(ENCODERS)), np.nan), vals])

    emb_all = G[:, :len(ENCODERS)].sum(1)
    imp = pd.DataFrame({"feature": names + ["Embedding, three encoders together"],
                        "all": list(np.abs(G).mean(0)) + [np.abs(emb_all).mean()]})
    for L in sorted(pd.unique(lang)):
        m = lang == L
        imp[L] = list(np.abs(G[m]).mean(0)) + [np.abs(emb_all[m]).mean()]
    imp = imp.sort_values("all", ascending=False)
    imp.to_csv(STEM + "_importance.csv", index=False)
    np.savez(RAW, shap=G, base=base, data=data, names=np.asarray(names),
             lang=np.asarray(lang, dtype="U8"), idx=arms[0]["idx"], A=A)
    print(imp.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    plot(RAW)


def plot(raw):
    """Two native shap beeswarms and the correlation table, all from the saved values.

    The two indicator columns are constant within a language, so with the language as background they
    get exactly 0 (checked here) and are left out. An embedding has no single value to colour a
    beeswarm with, so the main-text beeswarm shows the four lexical features, and the appendix
    beeswarm shows all seven inputs, with the three embeddings in grey. Labels are the short names of
    the table in the text."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import shap
    z = np.load(raw)
    G, data, names = z["shap"], z["data"], [str(v) for v in z["names"]]
    flags = [j for j, nm in enumerate(names) if nm.endswith("(flag)")]
    assert np.abs(G[:, flags]).max() == 0, "an indicator has non-zero SHAP, it cannot be left out"
    keep = [j for j in range(len(names)) if j not in flags]
    lex = [j for j in keep if not names[j].startswith("Embedding")]
    os.makedirs(FIG, exist_ok=True)

    def figure(cols, size, stem, fig_name):
        expl = shap.Explanation(values=G[:, cols], base_values=z["base"], data=data[:, cols],
                                feature_names=[SHORT[names[j]] for j in cols])
        fig, ax = plt.subplots(figsize=size)
        shap.plots.beeswarm(expl, max_display=len(cols), ax=ax, show=False, plot_size=None)
        # No title: the caption in the paper says what the figure shows and gives the unit.
        ax.set_xlabel("SHAP value for Signal A (impact on model output)", fontsize=11)
        fig.savefig(stem + ".pdf", bbox_inches="tight")
        fig.savefig(stem + ".png", dpi=200, bbox_inches="tight")
        shutil.copyfile(stem + ".pdf", os.path.join(FIG, fig_name))
        print(f"-> {stem}.pdf, {stem}.png, {os.path.join(FIG, fig_name)}")

    figure(lex, (6.4, 3.4),
           STEM + "_lexical", "fig_shap_signal_a.pdf")
    figure(keep, (4.6, 4.4),                                          # one column wide
           STEM + "_all_inputs", "fig_shap_signal_a_all.pdf")

    correlations(z, names, keep)


def correlations(z, names, keep):
    """Spearman correlation with gold complexity, within each language, averaged over languages.

    For every input: its SHAP contribution to signal A. For the lexical features also the raw value.
    A language is skipped where the column is constant or missing (frequency in Sinhala, syllables and
    capitalisation outside Latin script), and the number of languages used is reported."""
    from scipy.stats import spearmanr
    G, data, lang = z["shap"], z["data"], z["lang"].astype(str)
    y = pd.read_csv(FUSION).set_index("idx").loc[z["idx"], "y"].values

    def mean_rho(x):
        rs = []
        for L in sorted(set(lang)):
            m = (lang == L) & np.isfinite(x)
            if m.sum() >= 3 and np.ptp(x[m]) > 0:
                rs.append(spearmanr(x[m], y[m])[0])
        return (float(np.mean(rs)) if rs else np.nan), len(rs)

    rows = []
    for j in keep:
        rc, nc = mean_rho(G[:, j])
        rv, nv = (np.nan, 0) if names[j].startswith("Embedding") else mean_rho(data[:, j])
        rows.append(dict(input=names[j], mean_abs_shap=np.abs(G[:, j]).mean(),
                         rho_contribution=rc, langs_contribution=nc, rho_value=rv, langs_value=nv))
    t = pd.DataFrame(rows).sort_values("mean_abs_shap", ascending=False)
    t.to_csv(STEM + "_correlations.csv", index=False)
    print(t.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"-> {STEM}_correlations.csv")


if __name__ == "__main__":
    main()
