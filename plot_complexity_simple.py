"""Grafic simplu: media scorului de complexitate per limba, cu bare de eroare (deviatie standard).
Mai usor de citit decat densitatile suprapuse: o bara = o limba, mai inalta = cuvinte mai complexe in medie.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("output/fusion_preds_lolo_adoptat.csv")

LANG_NAME = {
    "ca": "Catalan", "de": "German", "en": "English", "es": "Spanish",
    "fil": "Filipino", "fr": "French", "it": "Italian", "ja": "Japanese",
    "pt": "Portuguese", "si": "Sinhala",
}

stats = (df.groupby("lang")["y"].agg(["mean", "std", "count"])
           .rename(index=LANG_NAME)
           .sort_values("mean"))

fig, ax = plt.subplots(figsize=(7, 6))
y_pos = np.arange(len(stats))
ax.barh(y_pos, stats["mean"], xerr=stats["std"], color="#4C72B0",
        edgecolor="black", linewidth=0.5, capsize=3)
ax.set_yticks(y_pos)
ax.set_yticklabels(stats.index)
ax.set_xlabel("Scor mediu de complexitate (0 = simplu, 1 = complex)")
ax.set_xlim(0, 1)
ax.grid(True, axis="x", alpha=0.4)
ax.set_title("Cat de complexe sunt cuvintele-tinta, in medie, per limba")
fig.tight_layout()
fig.savefig("output/fig_gold_complexity_bar.png", dpi=200)
print("scris output/fig_gold_complexity_bar.png")
print(stats)
