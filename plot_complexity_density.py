"""Densitatea scorurilor gold de complexitate lexicala, per limba, pe setul de test MLSP.
Reproduce stilul graficului de referinta (KDE per limba, acelasi x/y).
"""
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np

df = pd.read_csv("output/fusion_preds_lolo_adoptat.csv")

LANG_NAME = {
    "ca": "Catalan", "de": "German", "en": "English", "es": "Spanish",
    "fil": "Filipino", "fr": "French", "it": "Italian", "ja": "Japanese",
    "pt": "Portuguese", "si": "Sinhala",
}
ORDER = ["en", "es", "fil", "si", "ja", "pt", "de", "fr", "it", "ca"]

fig, ax = plt.subplots(figsize=(8, 6))
xs = np.linspace(0, 1, 400)

for lang in ORDER:
    y = df.loc[df["lang"] == lang, "y"].dropna().values
    if len(y) < 2:
        continue
    kde = gaussian_kde(y)
    ax.plot(xs, kde(xs), label=LANG_NAME[lang], linewidth=1.6)

ax.set_xlabel("Lexical Complexity Scores")
ax.set_ylabel("Density")
ax.grid(True, alpha=0.4)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig("output/fig_gold_complexity_density.png", dpi=200)
print("scris output/fig_gold_complexity_density.png")
