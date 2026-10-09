import sys, numpy as np, pandas as pd
REPO="/Users/alexandrucojoaca/Documents/GitHub/ia-sahistii"; sys.path.insert(0, REPO)
from mlsp_common import load_mlsp
from sklearn.neighbors import NearestNeighbors
ml = load_mlsp("test", include_ro=True)
E = np.load(f"{REPO}/data/emb_mlsp10_xlmr_last4_7211.npy"); ok = np.load(f"{REPO}/data/emb_mlsp10_xlmr_last4_7211_ok.npy")
lang = np.asarray(ml["lang"].astype(str).to_numpy())[ok]
ctx = np.asarray((ml["lang"].astype(str) + "|" + ml["context_id"].astype(str)).to_numpy())[ok]
X = E[ok].astype(np.float64); Xc = X.copy()
for L in np.unique(lang):
    m = lang == L; Xc[m] -= X[m].mean(0, keepdims=True)
p = pd.Series(lang).value_counts(normalize=True); print("sansa", round(float((p**2).sum()), 3))
def knn(Z, k=15, K=80):
    idx = NearestNeighbors(n_neighbors=K, metric="cosine").fit(Z).kneighbors(Z, return_distance=False)
    tot, per = [], {}
    for i in range(len(Z)):
        nb = [j for j in idx[i] if j != i and ctx[j] != ctx[i]][:k]
        s = float(np.mean(lang[nb] == lang[i])); tot.append(s); per.setdefault(lang[i], []).append(s)
    return np.mean(tot), {L: round(np.mean(v), 2) for L, v in sorted(per.items())}
for n, Z in (("inainte", X), ("dupa", Xc)):
    t, per = knn(Z); print(n, round(t, 3), per)
