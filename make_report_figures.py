# Genereaza figurile pentru raport (regresie => folosim SHAP, corelatii, confuzie pe split sursa,
# ablatie, curbe sweep). Scrie in output/raport/. Toate pe CPU.
# Rulare: "C:/Users/.../Python311/python.exe" make_report_figures.py
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

from solutie_finala import (HERE, DATA, citeste_semnale_cache, semnal_et,
                            zscore, fill, lexical)
from recompute_gpu import lexical as lexical_en, blend_ridge_hgb, _Xc

OUT = os.path.join(HERE, "output", "raport")
os.makedirs(OUT, exist_ok=True)


# --- Fig 1: ablatie 5 trepte (baseline -> sistem complet cu 4 semnale) ---
def fig_ablation():
    labels = ["constant\n0.27", "surface-only", "ET + surface\n(self-sup)",
              "3 semnale\n(extern+LLM)", "4 semnale\n(+eye-track)"]
    scores = [0.0, 10.27, 41.76, 68.90, 69.74]
    fig, ax = plt.subplots(figsize=(7.5, 4))
    bars = ax.bar(labels, scores, color=["#bbb", "#7aa6c2", "#5b9e6f", "#c2562a", "#9b3d1a"])
    for b, s in zip(bars, scores):
        ax.text(b.get_x() + b.get_width() / 2, s + 1, f"{s:.2f}", ha="center", fontsize=10)
    ax.set_ylabel(r"Public score  $50\,(|r| + \max(0,R^2))$")
    ax.set_title("Ablation: contribution of signal sources")
    ax.set_ylim(0, 80)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_ablation.png"), dpi=150); plt.close(fig)


# --- Fig 2: curbele de sweep ale ponderilor (public) ---
def fig_sweeps():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    # surprisal: puncte publice cunoscute
    ws = [0.0, 0.08, 0.12, 0.20]; ps = [64.52, 64.81, 64.71, 63.84]
    a1.plot(ws, ps, "-o", color="#c2562a")
    a1.axvline(0.08, ls="--", color="gray", lw=1)
    a1.annotate("peak w=0.08", (0.08, 64.81), textcoords="offset points", xytext=(12, -4), fontsize=9)
    a1.set_xlabel("surprisal weight $W_{SURP}$"); a1.set_ylabel("public score")
    a1.set_title("Surprisal weight sweep")
    # eye-tracking: puncte publice cunoscute
    we = [0.0, 0.10, 0.20, 0.30]; pe = [68.90, 69.66, 69.74, 69.00]
    a2.plot(we, pe, "-o", color="#9b3d1a")
    a2.axvline(0.20, ls="--", color="gray", lw=1)
    a2.annotate("peak w=0.20", (0.20, 69.74), textcoords="offset points", xytext=(-60, -4), fontsize=9)
    a2.set_xlabel("eye-tracking weight $W_{ET}$"); a2.set_ylabel("public score")
    a2.set_title("Eye-tracking weight sweep")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_sweeps.png"), dpi=150); plt.close(fig)


# --- Fig 3: matricea de corelatie a celor 4 semnale + frecventa (pe test RO) ---
def fig_corr():
    test = pd.read_csv(os.path.join(DATA, "test_set.csv"))
    A_en, A_mlsp, B, C = citeste_semnale_cache(test)
    et = semnal_et(test, verbose=False)
    A = zscore(0.5 * zscore(fill(A_mlsp)) + 0.5 * zscore(fill(A_en)))
    freq = lexical(list(test["token"]), ["ro"] * len(test), lemmas=test["lemma"].values)[:, 0]
    M = pd.DataFrame({
        "A cross-ling": A, "B LLM": zscore(fill(B)), "C surprisal": zscore(fill(C)),
        "D eye-track": zscore(fill(et)), "frequency": zscore(freq),
    })
    corr = M.corr().values
    names = list(M.columns)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(names))); ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
    for i in range(len(names)):
        for j in range(len(names)):
            ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center",
                    color="white" if abs(corr[i, j]) > 0.5 else "black", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Signal correlation matrix (RO test, z-scored)")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_corr_matrix.png"), dpi=150); plt.close(fig)


# --- Fig 4: matrice de confuzie pe split held-out CompLex EN (etichete reale) + Pearson local ---
def _load_complex_split(k):
    d = pd.read_csv(os.path.join(DATA, "complex_en", f"lcp_single_{k}.tsv"), sep="\t")
    d = d.dropna(subset=["sentence", "token", "complexity"]).reset_index(drop=True)
    E = np.load(os.path.join(DATA, f"xlemb_base_en_{k}.npy"))
    ok = np.load(os.path.join(DATA, f"xlemb_base_en_{k}_ok.npy"))
    assert len(d) == len(E), f"{k}: {len(d)} vs {len(E)}"
    d, E = d[ok].reset_index(drop=True), E[ok]
    lex = lexical_en(list(d["token"]), ["en"] * len(d))
    return E, lex, d["complexity"].values.astype(float)


def fig_confusion():
    Etr1, l1, y1 = _load_complex_split("train")
    Etr2, l2, y2 = _load_complex_split("trial")
    Ete, lte, yte = _load_complex_split("test")
    Etr = np.vstack([Etr1, Etr2]); ltr = np.vstack([l1, l2]); ytr = np.concatenate([y1, y2])
    mu = Etr.mean(0, keepdims=True)
    pred = blend_ridge_hgb(_Xc(Etr, ltr, mu), ytr, _Xc(Ete, lte, mu))
    r = pearsonr(pred, yte)[0]
    print(f"[confusion] held-out CompLex EN test: n={len(yte)}, local Pearson r = {r:.4f}")

    thr = np.quantile(ytr, [1 / 3, 2 / 3])
    band = lambda v: np.digitize(v, thr)
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(band(yte), band(pred))
    cmn = cm / cm.sum(1, keepdims=True)
    labels = ["easy", "medium", "hard"]
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    im = ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(3)); ax.set_xticklabels(labels)
    ax.set_yticks(range(3)); ax.set_yticklabels(labels)
    ax.set_xlabel("predicted band"); ax.set_ylabel("true band")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{cmn[i, j]:.2f}\n({cm[i, j]})", ha="center", va="center",
                    color="white" if cmn[i, j] > 0.5 else "black", fontsize=9)
    ax.set_title(f"Confusion matrix, held-out CompLex EN\n(local Pearson r={r:.3f}, tertile bands)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_confusion.png"), dpi=150); plt.close(fig)
    return r


# --- Fig 5: ET timpuriu vs tarziu (corelatie controlata) + loadings PC1 ---
def fig_et():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    grp = ["early\n(FFD/FPRT)", "late\n(RRT/RPD/reread)"]; val = [0.0103, 0.2430]
    a1.bar(grp, val, color=["#7aa6c2", "#9b3d1a"])
    for i, v in enumerate(val):
        a1.text(i, v + 0.005, f"{v:.4f}", ha="center", fontsize=10)
    a1.set_ylabel("partial corr with prediction (freq/len controlled)")
    a1.set_title("Early vs late eye-tracking")
    a1.set_ylim(0, 0.30)
    load = {"TFT": 0.438, "TFC": 0.426, "FPRT": 0.417, "FPFC": 0.388,
            "RRT": 0.355, "FFD": 0.290, "RPD_inc": 0.276, "TRC_in": 0.127}
    a2.barh(list(load.keys())[::-1], list(load.values())[::-1], color="#5b9e6f")
    a2.set_xlabel("PC1 loading"); a2.set_title("PCA reading_effort loadings (PC1)")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_et_early_late.png"), dpi=150); plt.close(fig)


# --- Fig: PCA of the eye-tracking effort metrics (scree + biplot on PC1-PC2) ---
ET_EFFORT = ["TFT_mean_norm", "FFD_mean_norm", "FPRT_mean_norm", "RRT_mean_norm",
             "TFC_mean_norm", "FPFC_mean_norm", "TRC_in_mean_norm", "RPD_inc_mean_norm"]


def fig_pca():
    x = pd.read_csv(os.path.join(DATA, "X_test.csv"))
    cols = [c for c in ET_EFFORT if c in x.columns]
    short = [c.replace("_mean_norm", "") for c in cols]
    has = (x["has_et_features"] == 1).values if "has_et_features" in x.columns else x[cols[0]].notna().values
    M = x[cols].astype(float)
    Z = ((M - M[has].mean()) / (M[has].std() + 1e-9)).fillna(0.0).values[has]
    Z = Z - Z.mean(0)
    _, S, Vt = np.linalg.svd(Z, full_matrices=False)
    var = S ** 2 / (S ** 2).sum()
    if Vt[0][cols.index("TFT_mean_norm")] < 0:          # fix sign: more TFT = more effort
        Vt[0] = -Vt[0]

    # O singura bara orizontala: loadings PC1 (cat cantareste fiecare metrica pe axa de efort), sortata.
    load = Vt[0]
    order = np.argsort(load)                       # crescator -> cel mai mare sus pe barh
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.barh([short[i] for i in order], load[order], color="#5b9e6f")
    for i, v in zip(range(len(order)), load[order]):
        ax.text(v + 0.006, i, f"{v:.2f}", va="center", fontsize=9)
    ax.set_xlabel("PC1 loading (contribution to the reading-effort axis)")
    ax.set_title(f"Reading effort = PC1 of 8 eye-tracking metrics (explains {var[0]*100:.0f}% of variance)")
    ax.set_xlim(0, max(load) * 1.18)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_pca.png"), dpi=150); plt.close(fig)


# --- Fig 6: SHAP la nivel de semnal, etichete EN (valori din shap_et.py, W_ET=0.20) ---
def fig_shap_signals():
    names = ["A cross-lingual", "B LLM rating", "D eye-tracking", "C surprisal", "frequency (zipf)"]
    vals = [0.0609, 0.0341, 0.0174, 0.0060, 0.0023]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.barh(names[::-1], vals[::-1], color="#1f8fff")
    for i, v in enumerate(vals[::-1]):
        ax.text(v + 0.001, i, f"{v:.4f}", va="center", fontsize=9)
    ax.set_xlabel("mean(|SHAP value|) — impact on final prediction")
    ax.set_title("SHAP signal importance in the final fusion (W_ET=0.20)")
    ax.set_xlim(0, 0.072)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_shap_signals.png"), dpi=150); plt.close(fig)


if __name__ == "__main__":
    # Figurile folosite in raport: corelatie, confuzie (split sursa), PCA (scree+biplot).
    # ablation/sweeps/et/shap_signals raman definite mai sus dar nu se mai apeleaza (taiate din raport).
    fig_corr()
    fig_confusion()
    fig_pca()
    print("Figuri scrise in", OUT)
    print(sorted(os.listdir(OUT)))
