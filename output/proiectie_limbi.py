"""t-SNE si UMAP pe embeddingurile xlmr de test (11 limbi), inainte si dupa centrarea pe media limbii.

Pe langa grafice, doua masuri in spatiul ORIGINAL de 768 de dimensiuni, fiindca proiectia 2D poate
insela: (1) cat din cei 15 vecini ai unui punct sunt din aceeasi limba, fata de sansa; (2) acuratetea
unui clasificator liniar de limba, validat incrucisat. Daca (2) ramane mare dupa centrare, limbile
sunt inca separabile, doar nu prin medie.
"""
import sys, time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = "/Users/alexandrucojoaca/Documents/GitHub/ia-sahistii"
OUT = sys.argv[1]
sys.path.insert(0, REPO)
from mlsp_common import load_mlsp

ml = load_mlsp("test", include_ro=True)
E = np.load(f"{REPO}/data/emb_mlsp10_xlmr_last4_7211.npy")
ok = np.load(f"{REPO}/data/emb_mlsp10_xlmr_last4_7211_ok.npy")
assert len(ml) == len(E) == 7211, (len(ml), len(E))
lang = np.asarray(ml["lang"].astype(str).to_numpy())[ok]
y = ml["complexity"].to_numpy(dtype=float)[ok]
X = E[ok].astype(np.float64)
print("randuri valide", ok.sum(), dict(pd.Series(lang).value_counts()))

Xc = X.copy()
for L in np.unique(lang):
    m = lang == L
    Xc[m] -= X[m].mean(0, keepdims=True)

# ---------------------------------------------------------------- masuri in 768 de dimensiuni
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

p = pd.Series(lang).value_counts(normalize=True)
sansa_knn = float((p ** 2).sum())
sansa_clf = float(p.max())


def knn_same(Z, k=15):
    nn = NearestNeighbors(n_neighbors=k + 1, metric="cosine").fit(Z)
    idx = nn.kneighbors(Z, return_distance=False)[:, 1:]
    return float((lang[idx] == lang[:, None]).mean())


def probe(Z):
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=0.1))
    cv = StratifiedKFold(5, shuffle=True, random_state=0)
    return float(cross_val_score(clf, Z, lang, cv=cv).mean())


rez = {}
for nume, Z in (("inainte", X), ("dupa", Xc)):
    rez[nume] = (knn_same(Z), float("nan"))
    print(f"{nume:8s} vecini aceeasi limba {rez[nume][0]:.3f} (sansa {sansa_knn:.3f}) | "
          f"clasificator liniar {rez[nume][1]:.3f} (sansa {sansa_clf:.3f})", flush=True)

# ---------------------------------------------------------------- proiectii
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

proj = {}
for nume, Z in (("inainte", X), ("dupa", Xc)):
    Zp = PCA(50, random_state=0).fit_transform(Z)
    t0 = time.time()
    proj[("tsne", nume)] = TSNE(2, perplexity=30, init="pca", random_state=0).fit_transform(Zp)
    proj[("umap", nume)] = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine",
                                     random_state=0).fit_transform(Zp)
    print(nume, f"proiectii gata in {time.time()-t0:.0f}s", flush=True)

np.savez(f"{OUT}/proiectii.npz", lang=lang, y=y,
         **{f"{a}_{b}": v for (a, b), v in proj.items()})

# ---------------------------------------------------------------- grafice
NUME = {"ca": "Catalan", "de": "German", "en": "English", "es": "Spanish", "fil": "Filipino",
        "fr": "French", "it": "Italian", "ja": "Japanese", "pt": "Portuguese", "ro": "Romanian",
        "si": "Sinhala"}
LANGS = sorted(NUME, key=lambda c: NUME[c])
SURF, INK, INK2, GRAY, BLUE = "#fcfcfb", "#0b0b0b", "#52514e", "#d9d8d3", "#2a78d6"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": INK,
                     "figure.facecolor": SURF, "axes.facecolor": SURF})

for met, titlu in (("tsne", "t-SNE"), ("umap", "UMAP")):
    fig, axs = plt.subplots(4, 6, figsize=(15, 10.2))
    for r0, nume, eticheta in ((0, "inainte", "Before per-language centring"),
                               (2, "dupa", "After per-language centring")):
        P = proj[(met, nume)]
        k, c = rez[nume]
        for i in range(12):
            ax = axs[r0 + i // 6, i % 6]
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_visible(False)
            if i == 11:
                ax.text(0.02, 0.5, f"{eticheta}\n\nsame-language share of\n15 nearest neighbours: "
                        f"{k:.2f}\n(chance {sansa_knn:.2f})", va="center", ha="left",
                        color=INK2, fontsize=9, transform=ax.transAxes)
                continue
            L = LANGS[i]
            m = lang == L
            ax.scatter(P[~m, 0], P[~m, 1], s=2, c=GRAY, linewidths=0, rasterized=True)
            ax.scatter(P[m, 0], P[m, 1], s=3, c=BLUE, linewidths=0, rasterized=True)
            ax.set_title(NUME[L], fontsize=9, color=INK, loc="left")
        axs[r0, 0].set_ylabel(eticheta, color=INK2, fontsize=10)
    fig.suptitle(f"{titlu} of XLM-R target-word embeddings, test split, 11 languages "
                 f"(n={len(lang)}); highlighted language in blue, all others in grey",
                 x=0.01, ha="left", fontsize=11, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(f"{OUT}/{met}_limbi.png", dpi=160)
    plt.close(fig)

# complexitatea, dupa centrare: gradient vizibil sau nu
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("seq", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab",
                                                 "#0d366b"])
fig, axs = plt.subplots(1, 2, figsize=(12, 5.6))
for ax, (met, titlu) in zip(axs, (("tsne", "t-SNE"), ("umap", "UMAP"))):
    P = proj[(met, "dupa")]
    o = np.argsort(y)
    sc = ax.scatter(P[o, 0], P[o, 1], s=3, c=y[o], cmap=cmap, vmin=0, vmax=0.8, linewidths=0,
                    rasterized=True)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(titlu, loc="left", fontsize=10)
cb = fig.colorbar(sc, ax=axs, shrink=0.7, pad=0.02)
cb.set_label("gold complexity", color=INK2)
fig.suptitle("After per-language centring, coloured by gold complexity (all 11 languages)",
             x=0.01, ha="left", fontsize=11)
fig.savefig(f"{OUT}/complexitate_dupa.png", dpi=160, bbox_inches="tight")
print("gata")
