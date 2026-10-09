import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import pearsonr, spearmanr
F = "/private/tmp/claude-501/-Users-alexandrucojoaca-Documents-GitHub-ia-sahistii/a4bad522-1669-4ce3-bea7-5798908e1981/scratchpad/fig"
d = np.load(f"{F}/umap3.npz"); df = pd.read_csv(f"{F}/izolare_limbi.csv")
NUME = {"ca": "Catalan", "de": "German", "en": "English", "es": "Spanish", "fil": "Filipino",
        "fr": "French", "it": "Italian", "ja": "Japanese", "pt": "Portuguese", "ro": "Romanian",
        "si": "Sinhala"}
COL = {"pt": "#2a78d6", "es": "#00b3d6", "it": "#008300", "fr": "#e34948", "ca": "#4a3aa7",
       "ro": "#eda100", "en": "#1f1f1f", "ja": "#e87ba4", "si": "#1baf7a", "fil": "#8a5a2b",
       "de": "#7d8a99"}
ENC = {"xlmr": "XLM-R base", "labse": "LaBSE", "e5": "multilingual-E5 base"}
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "text.color": INK})
tot = df.assign(s=df.share * 1).groupby(["enc", "stare"]).apply(
    lambda g: np.average(g.share, weights=g.pL)).to_dict()

fig, axs = plt.subplots(2, 3, figsize=(16, 10.4))
for j, enc in enumerate(ENC):
    lang = np.load(f"{F}/lang_{enc}.npy", allow_pickle=True)
    o = np.random.default_rng(0).permutation(len(lang)); c = [COL[l] for l in lang[o]]
    for i, (k, et) in enumerate((("inainte", "before centring"), ("dupa", "after centring"))):
        ax = axs[i, j]; P = d[f"{enc}_{k}"][o]
        ax.scatter(P[:, 0], P[:, 1], s=3, c=c, linewidths=0, alpha=0.8, rasterized=True)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)
        ax.set_title(f"{ENC[enc]}, {et}\nsame-language neighbours: {tot[(enc, k)]:.2f} (chance 0.11)",
                     loc="left", fontsize=10)
h = [Line2D([], [], marker="o", ls="", ms=7, mfc=COL[l], mec=COL[l], label=NUME[l])
     for l in sorted(NUME, key=lambda x: NUME[x])]
fig.legend(handles=h, loc="lower center", ncol=11, frameon=False, fontsize=9, handletextpad=0.2,
           columnspacing=1.0)
fig.suptitle("UMAP of target-word embeddings per encoder, test split, 11 languages (n=7211)",
             x=0.01, ha="left", fontsize=12)
fig.tight_layout(rect=(0, 0.04, 1, 0.96)); fig.savefig(f"{F}/umap_3encodere.png", dpi=160); plt.close(fig)

# izolare dupa centrare vs r_A, medie pe cele 3 encodere
m = df[df.stare == "dupa"].groupby("lang")[["lift", "rA"]].mean()
r, rs = pearsonr(m.lift, m.rA)[0], spearmanr(m.lift, m.rA)[0]
fig, ax = plt.subplots(figsize=(8, 5.6))
ax.scatter(m.lift, m.rA, s=60, c="#2a78d6", edgecolors=SURF, linewidths=2, zorder=3)
for L, row in m.iterrows():
    ax.annotate(NUME[L], (row.lift, row.rA), xytext=(7, 4) if L == "ro" else (7, -3), textcoords="offset points",
                fontsize=9, color=INK2)
ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(GRID)
ax.tick_params(colors=INK2)
ax.set_xlabel("isolation after centring: same-language neighbour share / language share", color=INK2)
ax.set_ylabel("Pearson r of transfer signal A", color=INK2)
ax.set_title(f"Isolation after centring and the transfer signal, per language\n"
             f"mean over 3 encoders; Pearson {r:+.2f}, Spearman {rs:+.2f}, 11 languages",
             loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(f"{F}/izolare_vs_rA.png", dpi=170)
print(round(r, 3), round(rs, 3)); print(m.round(3))
