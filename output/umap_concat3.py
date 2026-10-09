"""Cele trei encodere ale semnalului A lipite (xlmr ++ labse ++ e5), fiecare bloc scalat la aceeasi
varianta totala. Nu e media embeddingurilor: spatiile nu sunt aliniate, deci media coordonatelor n-ar
insemna nimic. Sistemul mediaza PREDICTIILE; lipirea e cea mai apropiata imagine a ce vad impreuna."""
import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
REPO = "/Users/alexandrucojoaca/Documents/GitHub/ia-sahistii"; sys.path.insert(0, REPO)
from mlsp_common import load_mlsp
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import umap
OUT = sys.argv[1]
ml = load_mlsp("test", include_ro=True)
lang_all = np.asarray(ml["lang"].astype(str).to_numpy())
ctx_all = np.asarray((ml["lang"].astype(str) + "|" + ml["context_id"].astype(str)).to_numpy())
E, OK = {}, None
for enc in ("xlmr", "labse", "e5"):
    E[enc] = np.load(f"{REPO}/data/emb_mlsp10_{enc}_last4_7211.npy").astype(np.float64)
    ok = np.load(f"{REPO}/data/emb_mlsp10_{enc}_last4_7211_ok.npy"); OK = ok if OK is None else OK & ok
lang, ctx = lang_all[OK], ctx_all[OK]

def bloc(X, centrat):
    X = X[OK].copy()
    if centrat:
        for L in np.unique(lang):
            m = lang == L; X[m] -= X[m].mean(0, keepdims=True)
    Xg = X - X.mean(0, keepdims=True)
    return X / np.sqrt((Xg ** 2).sum(1).mean())        # aceeasi varianta totala pe fiecare bloc

res = {}
for k, c in (("inainte", False), ("dupa", True)):
    Z = np.hstack([bloc(E[e], c) for e in E])
    idx = NearestNeighbors(n_neighbors=80, metric="cosine").fit(Z).kneighbors(Z, return_distance=False)
    share = np.mean([np.mean(lang[[j for j in idx[i] if j != i and ctx[j] != ctx[i]][:15]] == lang[i])
                     for i in range(len(Z))])
    P = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=0).fit_transform(
        PCA(50, random_state=0).fit_transform(Z))
    res[k] = (P, share); print(k, Z.shape, round(share, 3), flush=True)

NUME = {"ca": "Catalan", "de": "German", "en": "English", "es": "Spanish", "fil": "Filipino",
        "fr": "French", "it": "Italian", "ja": "Japanese", "pt": "Portuguese", "ro": "Romanian",
        "si": "Sinhala"}
COL = {"pt": "#2a78d6", "es": "#00b3d6", "it": "#008300", "fr": "#e34948", "ca": "#4a3aa7",
       "ro": "#eda100", "en": "#1f1f1f", "ja": "#e87ba4", "si": "#1baf7a", "fil": "#8a5a2b",
       "de": "#7d8a99"}
SURF, INK = "#fcfcfb", "#0b0b0b"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "text.color": INK})
o = np.random.default_rng(0).permutation(len(lang)); col = [COL[l] for l in lang[o]]
fig, axs = plt.subplots(1, 2, figsize=(14, 6.8))
for ax, (k, et) in zip(axs, (("inainte", "Before per-language centring"),
                             ("dupa", "After per-language centring"))):
    P, sh = res[k]; P = P[o]
    ax.scatter(P[:, 0], P[:, 1], s=4, c=col, linewidths=0, alpha=0.8, rasterized=True)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title(f"{et}\nsame-language share of 15 nearest neighbours: {sh:.2f} (chance 0.11)",
                 loc="left", fontsize=10)
h = [Line2D([], [], marker="o", ls="", ms=7, mfc=COL[l], mec=COL[l], label=NUME[l])
     for l in sorted(NUME, key=lambda x: NUME[x])]
fig.legend(handles=h, loc="lower center", ncol=11, frameon=False, fontsize=9, handletextpad=0.2,
           columnspacing=1.0)
fig.suptitle(f"UMAP of target-word embeddings, XLM-R base + LaBSE + multilingual-E5 base concatenated, "
             f"test split, 11 languages (n={len(lang)})", x=0.01, ha="left", fontsize=12)
fig.tight_layout(rect=(0, 0.06, 1, 0.95))
fig.savefig(f"{OUT}/umap_3encodere_concat.png", dpi=170)
