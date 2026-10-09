import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
S = "/private/tmp/claude-501/-Users-alexandrucojoaca-Documents-GitHub-ia-sahistii/a4bad522-1669-4ce3-bea7-5798908e1981/scratchpad"
d = np.load(f"{S}/fig/proiectii.npz", allow_pickle=True); lang = d["lang"]
NUME = {"ca": "Catalan", "de": "German", "en": "English", "es": "Spanish", "fil": "Filipino",
        "fr": "French", "it": "Italian", "ja": "Japanese", "pt": "Portuguese", "ro": "Romanian",
        "si": "Sinhala"}
# culorile cele mai distincte merg la limbile care se suprapun (romanice + engleza)
COL = {"pt": "#2a78d6", "es": "#00b3d6", "it": "#008300", "fr": "#e34948", "ca": "#4a3aa7",
       "ro": "#eda100", "en": "#1f1f1f", "ja": "#e87ba4", "si": "#1baf7a", "fil": "#8a5a2b",
       "de": "#7d8a99"}
KNN = {"inainte": 0.64, "dupa": 0.39}
SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "text.color": INK})
rng = np.random.default_rng(0); o = rng.permutation(len(lang))   # ordine aleatoare, nu pe limba
for met, titlu in (("tsne", "t-SNE"), ("umap", "UMAP")):
    fig, axs = plt.subplots(1, 2, figsize=(14, 6.6))
    for ax, (k, et) in zip(axs, (("inainte", "Before per-language centring"),
                                 ("dupa", "After per-language centring"))):
        P = d[f"{met}_{k}"][o]; c = [COL[l] for l in lang[o]]
        ax.scatter(P[:, 0], P[:, 1], s=4, c=c, linewidths=0, alpha=0.8, rasterized=True)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)
        ax.set_title(f"{et}\nsame-language share of 15 nearest neighbours: {KNN[k]:.2f} (chance 0.11)",
                     loc="left", fontsize=10, color=INK)
    h = [Line2D([], [], marker="o", ls="", ms=7, mfc=COL[l], mec=COL[l], label=NUME[l])
         for l in sorted(NUME, key=lambda x: NUME[x])]
    fig.legend(handles=h, loc="lower center", ncol=11, frameon=False, fontsize=9,
               handletextpad=0.2, columnspacing=1.0)
    fig.suptitle(f"{titlu} of XLM-R target-word embeddings, test split, 11 languages (n={len(lang)})",
                 x=0.01, ha="left", fontsize=12)
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(f"{S}/fig/{met}_colorat.png", dpi=170)
print("gata")
