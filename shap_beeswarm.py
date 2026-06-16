# =============================================================================
# SHAP beeswarm (ca exemplul Boston housing) pe trasaturi cu NUME, interpretabile.
# Model surogat: HGB pe features lexicale numite -> prezice OUTPUT-ul modelului final (68.90),
# apoi SHAP arata ce trasaturi numite conduc predictia + directia (rosu=valoare mare).
# Output: output/shap/beeswarm.png
# =============================================================================
import os
import sys
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output", "shap")
os.makedirs(OUT, exist_ok=True)

# feature -> readable label (EN). Includes the 2 LLM signals (rating + surprisal) as features.
LABELS = {
    "llm_cx": "LLM rating", "surp": "surprisal",
    "zipf_best": "frequency (max token/lemma)", "zipf_token": "token frequency",
    "zipf_lemma": "lemma frequency", "word_length": "length", "num_syllables": "syllables",
    "vowel_ratio": "vowel ratio", "num_consonants": "consonants", "has_diacritice": "diacritics",
    "has_hyphen": "hyphen", "is_capitalized": "capitalized", "inflection_diff": "inflection gap",
    "is_oov": "OOV (unknown)", "ends_with_vowel": "ends with vowel",
}


def main():
    X = pd.read_csv(os.path.join(DATA, "X_test.csv"))
    pred = pd.read_csv(os.path.join(HERE, "output", "exp_lemmafreq.csv"))[["datapointID", "answer"]]
    llm = pd.read_csv(os.path.join(DATA, "llm_complexity_test.csv"))      # semnal B (nota)
    surp = pd.read_csv(os.path.join(DATA, "surprisal_test.csv"))          # semnal C (surprisal)
    df = X.merge(pred, on="datapointID").merge(llm, on="datapointID").merge(surp, on="datapointID")
    feats = [c for c in LABELS if c in df.columns]
    Xf = df[feats].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    y = df["answer"].values.astype(float)
    names = [LABELS[c] for c in feats]

    from sklearn.ensemble import HistGradientBoostingRegressor
    m = HistGradientBoostingRegressor(max_depth=4, learning_rate=0.05, max_iter=500,
                                      random_state=42).fit(Xf.values, y)
    from scipy.stats import pearsonr
    print(f"Surogat HGB pe {len(feats)} trasaturi numite: fit pe output final, r={pearsonr(m.predict(Xf.values), y)[0]:.3f}")

    import shap
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    try:
        expl = shap.TreeExplainer(m)
        sv = expl.shap_values(Xf.values)
    except Exception as ex:
        print(f"(TreeExplainer a esuat: {ex}; folosesc Explainer general pe esantion)")
        bg = shap.sample(Xf.values, 100, random_state=42)
        sv = shap.Explainer(m.predict, bg)(Xf.values[:600]).values
        Xf = Xf.iloc[:600]

    shap.summary_plot(sv, Xf.values, feature_names=names, show=False, max_display=8)
    plt.title("SHAP: which features drive the predicted complexity (red = high value)")
    plt.tight_layout()
    png = os.path.join(OUT, "beeswarm.png")
    plt.savefig(png, dpi=140, bbox_inches="tight")
    print(f"-> {png}")


if __name__ == "__main__":
    main()
