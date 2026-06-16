# =============================================================================
# Importanta trasaturilor pt semnalul cross-lingual (regresor pe embedding XLM-R + lexical).
# Raspunde: ce conteaza mai mult — embedding-ul (768 dim) sau frecventa/lungime/silabe/majuscula?
# (cerut de reguli pt raport). CPU: foloseste embeddingurile cache (.npy), NU blocheaza GPU.
#   - Permutare pe GRUPURI (embedding ca un grup) -> caderea corelatiei pe test = importanta robusta.
#   - SHAP (mean|shap|) agregat embedding vs lexical, ca verificare.
# Output: output/shap/feature_importance.csv + .txt
# =============================================================================
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output", "shap")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)
from solution_bert import lexical
from finetune_xlmr import load_complex_en

LEX_NAMES = ["zipf", "length", "syllables", "capital"]


def main():
    E = np.load(os.path.join(DATA, "emb_en_xlmr_last4_8423.npy"))
    ok = np.load(os.path.join(DATA, "emb_en_xlmr_last4_8423_ok.npy"))
    en = load_complex_en()
    assert len(en) == len(E), f"nepotrivire {len(en)} vs {len(E)}"
    lex = lexical(list(en["token"]), ["en"] * len(en))            # [zipf, length, syllables, capital]
    y = en["complexity"].values.astype(float)
    E, lex, y = E[ok], lex[ok], y[ok]
    Ec = E - E.mean(0, keepdims=True)                              # centrat pe limba (ca productia)
    X = np.hstack([Ec, lex]).astype(np.float32)
    D = E.shape[1]
    groups = {"embedding(768)": list(range(D))}
    for j, nm in enumerate(LEX_NAMES):
        groups[nm] = [D + j]

    from sklearn.ensemble import HistGradientBoostingRegressor
    rng = np.random.RandomState(42)
    idx = rng.permutation(len(X)); cut = int(0.8 * len(X))
    tr, te = idx[:cut], idx[cut:]
    m = HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                      l2_regularization=1.0, random_state=42).fit(X[tr], y[tr])
    base = pearsonr(m.predict(X[te]), y[te])[0]
    print(f"Pearson test (toate features) = {base:.4f}")

    # --- importanta prin permutare pe grupuri (cadere corelatie, mediat pe 5 repetari) ---
    rows = []
    for name, cols in groups.items():
        drops = []
        for s in range(5):
            Xp = X[te].copy()
            perm = np.random.RandomState(s).permutation(len(Xp))
            Xp[:, cols] = Xp[perm][:, cols]
            drops.append(base - pearsonr(m.predict(Xp), y[te])[0])
        rows.append({"feature": name, "perm_importance": round(float(np.mean(drops)), 4),
                     "std": round(float(np.std(drops)), 4)})
    imp = pd.DataFrame(rows).sort_values("perm_importance", ascending=False)

    # --- SHAP agregat (verificare) ---
    shap_agg = {}
    try:
        import shap
        expl = shap.TreeExplainer(m)
        sv = expl.shap_values(X[te][:600])
        a = np.abs(sv).mean(0)
        shap_agg["embedding(768)"] = float(a[:D].sum())
        for j, nm in enumerate(LEX_NAMES):
            shap_agg[nm] = float(a[D + j])
        imp["shap_mean_abs"] = imp["feature"].map(lambda f: round(shap_agg.get(f, np.nan), 5))
    except Exception as ex:
        print(f"(SHAP a esuat: {ex}; raportez doar permutarea)")

    imp.to_csv(os.path.join(OUT, "feature_importance.csv"), index=False)
    with open(os.path.join(OUT, "feature_importance.txt"), "w", encoding="utf-8") as f:
        f.write(f"Pearson test (toate) = {base:.4f}\n\n")
        f.write(imp.to_string(index=False) + "\n")
    print("\n--- Importanta features (semnal cross-lingual, sursa EN) ---")
    print(imp.to_string(index=False))

    # --- grafic ---
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        d = imp.sort_values("perm_importance")
        has_shap = "shap_mean_abs" in d.columns and d["shap_mean_abs"].notna().any()
        fig, axes = plt.subplots(1, 2 if has_shap else 1, figsize=(11 if has_shap else 6, 4.5))
        axes = np.atleast_1d(axes)
        axes[0].barh(d["feature"], d["perm_importance"], xerr=d["std"], color="#3b7dd8")
        axes[0].set_title(f"Permutare (cadere Pearson)\nsemnal cross-lingual EN, base r={base:.3f}")
        axes[0].set_xlabel("importanta")
        if has_shap:
            axes[1].barh(d["feature"], d["shap_mean_abs"], color="#d8843b")
            axes[1].set_title("SHAP (mean |valoare|)")
            axes[1].set_xlabel("importanta")
        fig.tight_layout()
        png = os.path.join(OUT, "feature_importance.png")
        fig.savefig(png, dpi=140)
        print(f"-> grafic: {png}")
    except Exception as ex:
        print(f"(plot esuat: {ex})")
    print("-> output/shap/feature_importance.csv")


if __name__ == "__main__":
    main()
