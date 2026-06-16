# =============================================================================
# SHAP la nivel de SEMNAL — cat conduce fiecare din cele 4 semnale predictia finala (cu ET).
# Surogat: HGB pe [A cross-lingual, B nota LLM, C surprisal, D eye-tracking, frecventa] -> prezice
# raspunsul final cu 4 semnale (W_ET ales). SHAP => importanta (mean|SHAP|) + directie.
#
# ATENTIE (onest): asta e DESCRIPTIV. Tinteste propria predictie => importanta lui D depinde de W_ET
# pe care l-ai pus (circular pt ALES ponderea). Importanta REALA a ET = lift-ul pe leaderboard
# (68.90 -> 69.66 la w0.10 -> 69.74 la w0.20). SHAP nu inlocuieste asta.
#
# Output: output/shap/semnale_bar.png + output/shap/semnale_beeswarm.png
# Rulare: python shap_et.py            (sau:  python shap_et.py 0.20  pt alt W_ET)
# =============================================================================
import os
import sys
import numpy as np
import pandas as pd

from solutie_finala import (HERE, DATA, citeste_semnale_cache, semnal_et,
                            combina_semnale, lexical, zscore, fill)

OUT = os.path.join(HERE, "output", "shap")
os.makedirs(OUT, exist_ok=True)


def main():
    w_et = float(sys.argv[1]) if len(sys.argv) > 1 else 0.20    # implicit varful public curent

    test = pd.read_csv(os.path.join(DATA, "test_set.csv"))
    A_en, A_mlsp, B, C = citeste_semnale_cache(test)
    et = semnal_et(test, verbose=False)

    # Tinta = raspunsul final cu 4 semnale la W_ET ales.
    y = combina_semnale(A_en, A_mlsp, B, C, et=et, w_et=w_et)

    # Cele 4 semnale (+ frecventa) ca trasaturi numite pentru surogat.
    A = zscore(0.5 * zscore(fill(A_mlsp)) + 0.5 * zscore(fill(A_en)))
    freq = lexical(list(test["token"]), ["ro"] * len(test), lemmas=test["lemma"].values)[:, 0]
    feats = {
        "A cross-lingual": A,
        "B nota LLM": zscore(fill(B)),
        "C surprisal": zscore(fill(C)),
        "D eye-tracking (PCA)": zscore(fill(et)),
        "frecventa (zipf)": zscore(freq),
    }
    names = list(feats)
    Xf = np.column_stack([feats[n] for n in names])

    from sklearn.ensemble import HistGradientBoostingRegressor
    from scipy.stats import pearsonr
    m = HistGradientBoostingRegressor(max_depth=4, learning_rate=0.05, max_iter=500,
                                      random_state=42).fit(Xf, y)
    print(f"Surogat HGB pe 5 trasaturi -> raspuns final (W_ET={w_et}), r={pearsonr(m.predict(Xf), y)[0]:.3f}")

    import shap
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sv = shap.TreeExplainer(m).shap_values(Xf)

    imp = np.abs(sv).mean(0)
    print("\nImportanta SHAP (mean|SHAP|) pe semnal:")
    for n, v in sorted(zip(names, imp), key=lambda t: -t[1]):
        print(f"  {n:24s} {v:.4f}")

    # 1. bar (importanta medie)
    shap.summary_plot(sv, Xf, feature_names=names, plot_type="bar", show=False)
    plt.title(f"SHAP — importanta semnalelor in predictia finala (W_ET={w_et})")
    plt.tight_layout(); p1 = os.path.join(OUT, "semnale_bar.png")
    plt.savefig(p1, dpi=140, bbox_inches="tight"); plt.close()
    print(f"-> {p1}")

    # 2. beeswarm (importanta + directie: rosu=valoare mare a semnalului)
    shap.summary_plot(sv, Xf, feature_names=names, show=False)
    plt.title(f"SHAP — semnale (rosu=valoare mare) in predictia finala (W_ET={w_et})")
    plt.tight_layout(); p2 = os.path.join(OUT, "semnale_beeswarm.png")
    plt.savefig(p2, dpi=140, bbox_inches="tight"); plt.close()
    print(f"-> {p2}")


if __name__ == "__main__":
    main()
