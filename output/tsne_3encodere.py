"""t-SNE pe aceleasi date ca figurile UMAP: fiecare encoder, si cele trei lipite, inainte/dupa
centrarea pe limba. Cifrele de vecini sunt calculate in spatiul original (izolare_enc3.py si
umap_concat3.py) si nu depind de proiectie."""
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
REPO = "/Users/alexandrucojoaca/Documents/GitHub/ia-sahistii"; sys.path.insert(0, REPO)
from mlsp_common import load_mlsp
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
OUT = sys.argv[1]
ml = load_mlsp("test", include_ro=True)
lang_all = np.asarray(ml["lang"].astype(str).to_numpy())
ENC = {"xlmr": "XLM-R base", "labse": "LaBSE", "e5": "multilingual-E5 base"}
KNN = {("xlmr", 0): 0.64, ("xlmr", 1): 0.39, ("labse", 0): 0.38, ("labse", 1): 0.27,
       ("e5", 0): 0.51, ("e5", 1): 0.30, ("concat", 0): 0.57, ("concat", 1): 0.33}
E, OKS = {}, {}
for e in ENC:
    E[e] = np.load(f"{REPO}/data/emb_mlsp10_{e}_last4_7211.npy").astype(np.float64)
    OKS[e] = np.load(f"{REPO}/data/emb_mlsp10_{e}_last4_7211_ok.npy")

def centreaza(X, lang):
    X = X.copy()
    for L in np.unique(lang):
        m = lang == L; X[m] -= X[m].mean(0, keepdims=True)
    return X

def tsne(Z):
    return TSNE(2, perplexity=30, init="pca", random_state=0).fit_transform(
        PCA(50, random_state=0).fit_transform(Z))

proj = {}
for e in ENC:
    lang = lang_all[OKS[e]]; X = E[e][OKS[e]]
    proj[(e, 0)] = (tsne(X), lang); proj[(e, 1)] = (tsne(centreaza(X, lang)), lang)
    print(e, flush=True)
OK = OKS["xlmr"] & OKS["labse"] & OKS["e5"]; lang = lang_all[OK]
def bloc(X, c):
    X = X[OK]; X = centreaza(X, lang) if c else X.copy()
    Xg = X - X.mean(0, keepdims=True); return X / np.sqrt((Xg ** 2).sum(1).mean())
for c in (0, 1):
    proj[("concat", c)] = (tsne(np.hstack([bloc(E[e], c) for e in ENC])), lang)
print("concat", flush=True)

NUME = {"ca": "Catalan", "de": "German", "en": "English", "es": "Spanish", "fil": "Filipino",
        "fr": "French", "it": "Italian", "ja": "Japanese", "pt": "Portuguese", "ro": "Romanian",
        "si": "Sinhala"}
COL = {"pt": "#2a78d6", "es": "#00b3d6", "it": "#008300", "fr": "#e34948", "ca": "#4a3aa7",
       "ro": "#eda100", "en": "#1f1f1f", "ja": "#e87ba4", "si": "#1baf7a", "fil": "#8a5a2b",
       "de": "#7d8a99"}
SURF, INK = "#fcfcfb", "#0b0b0b"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "text.color": INK})
STARE = {0: "before centring", 1: "after centring"}
def panou(ax, key, titlu):
    P, lg = proj[key]; o = np.random.default_rng(0).permutation(len(lg))
    ax.scatter(P[o, 0], P[o, 1], s=3, c=[COL[l] for l in lg[o]], linewidths=0, alpha=0.8,
               rasterized=True)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title(f"{titlu}\nsame-language share of 15 nearest neighbours: {KNN[key]:.2f} (chance 0.11)",
                 loc="left", fontsize=10)
def legenda(fig):
    h = [Line2D([], [], marker="o", ls="", ms=7, mfc=COL[l], mec=COL[l], label=NUME[l])
         for l in sorted(NUME, key=lambda x: NUME[x])]
    fig.legend(handles=h, loc="lower center", ncol=11, frameon=False, fontsize=9,
               handletextpad=0.2, columnspacing=1.0)

fig, axs = plt.subplots(2, 3, figsize=(16, 10.4))
for j, e in enumerate(ENC):
    for i in (0, 1):
        panou(axs[i, j], (e, i), f"{ENC[e]}, {STARE[i]}")
legenda(fig)
fig.suptitle("t-SNE of target-word embeddings per encoder, test split, 11 languages (n=7211)",
             x=0.01, ha="left", fontsize=12)
fig.tight_layout(rect=(0, 0.04, 1, 0.96)); fig.savefig(f"{OUT}/tsne_3encodere.png", dpi=160)

fig, axs = plt.subplots(1, 2, figsize=(14, 6.8))
for i in (0, 1):
    panou(axs[i], ("concat", i), ["Before per-language centring", "After per-language centring"][i])
legenda(fig)
fig.suptitle("t-SNE of target-word embeddings, XLM-R base + LaBSE + multilingual-E5 base concatenated, "
             f"test split, 11 languages (n={len(lang)})", x=0.01, ha="left", fontsize=12)
fig.tight_layout(rect=(0, 0.06, 1, 0.95)); fig.savefig(f"{OUT}/tsne_3encodere_concat.png", dpi=170)
print("gata")
