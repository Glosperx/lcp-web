"""Pe fiecare encoder: UMAP inainte/dupa centrarea pe limba, cat de izolata ramane fiecare limba
(vecini din aceeasi limba, fara vecinii din aceeasi propozitie, raportat la ponderea limbii), si
legatura cu r al semnalului A pe acea limba."""
import sys, numpy as np, pandas as pd
REPO = "/Users/alexandrucojoaca/Documents/GitHub/ia-sahistii"; sys.path.insert(0, REPO)
from mlsp_common import load_mlsp
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import umap
OUT = sys.argv[1]
ml = load_mlsp("test", include_ro=True)
lang_all = np.asarray(ml["lang"].astype(str).to_numpy())
ctx_all = np.asarray((ml["lang"].astype(str) + "|" + ml["context_id"].astype(str)).to_numpy())
PRED = {"xlmr": "", "labse": "labse_", "e5": "e5_"}
rows, proj = [], {}
for enc in ("xlmr", "labse", "e5"):
    E = np.load(f"{REPO}/data/emb_mlsp10_{enc}_last4_7211.npy"); ok = np.load(f"{REPO}/data/emb_mlsp10_{enc}_last4_7211_ok.npy")
    lang, ctx, X = lang_all[ok], ctx_all[ok], E[ok].astype(np.float64)
    Xc = X.copy()
    for L in np.unique(lang):
        m = lang == L; Xc[m] -= X[m].mean(0, keepdims=True)
    pL = pd.Series(lang).value_counts(normalize=True)
    pr = pd.read_csv(f"{REPO}/output/e1_frozen_preds_{PRED[enc]}lemma_fert_inloc_ro11.csv")
    pr = pr[pr["split"] == "test"]
    rA = pr.groupby("lang").apply(lambda g: np.corrcoef(g["p_multi"], g["complexity"])[0, 1])
    for k, Z in (("inainte", X), ("dupa", Xc)):
        idx = NearestNeighbors(n_neighbors=80, metric="cosine").fit(Z).kneighbors(Z, return_distance=False)
        share = np.array([np.mean(lang[[j for j in idx[i] if j != i and ctx[j] != ctx[i]][:15]] == lang[i])
                          for i in range(len(Z))])
        for L in np.unique(lang):
            s = share[lang == L].mean()
            rows.append(dict(enc=enc, stare=k, lang=L, share=s, pL=pL[L], lift=s / pL[L], rA=rA[L]))
        proj[(enc, k)] = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=0
                                   ).fit_transform(PCA(50, random_state=0).fit_transform(Z))
        print(enc, k, "share total", round(share.mean(), 3), flush=True)
    np.save(f"{OUT}/lang_{enc}.npy", lang)
df = pd.DataFrame(rows); df.to_csv(f"{OUT}/izolare_limbi.csv", index=False)
np.savez(f"{OUT}/umap3.npz", **{f"{a}_{b}": v for (a, b), v in proj.items()})
from scipy.stats import pearsonr, spearmanr
for enc in ("xlmr", "labse", "e5"):
    for k in ("inainte", "dupa"):
        d = df[(df.enc == enc) & (df.stare == k)]
        print(f"{enc:6s} {k:8s} corr(izolare, r_A) pearson {pearsonr(d.lift, d.rA)[0]:+.2f} "
              f"spearman {spearmanr(d.lift, d.rA)[0]:+.2f}")
print(df[df.stare == "dupa"].pivot(index="lang", columns="enc", values="lift").round(2))
print(df[df.stare == "dupa"].pivot(index="lang", columns="enc", values="rA").round(3))
