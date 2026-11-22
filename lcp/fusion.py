"""The paper's fusion for given rows, from the exported artifacts (scripts/export_model.py).

For a word of language L, with its three encoder embeddings, lexical columns and fertility, and
its three digit distributions from signal B:

  A   each encoder: features centred on L's stored means (signal_a.features), then p_en (the
      CompLex-only model; for en the multi model, as in signal_a.run) and p_multi_L (the model fitted
      without L). Each arm is z-scored with the constants of fuse.load_a, the encoders are averaged,
      and the two arms are mixed with w_src_L and z-scored again, as in fuse.z_a.
  B   fuse.b_of with L's temperature and partition, z-scored with L's constants.
  fused = w_L * zA + (1 - w_L) * zB, as in fuse.main.
  score 0-1: the percentile of `fused` in L's stored distribution of fused values (test rows),
      mapped through the quantiles of the labels of all eleven languages pooled; monotone, so the
      ranking is exactly the system's. level: the rating 1..5 nearest to 1 + 4 * score.

Every constant is a plain number in artifacts/params.json (the embedding means are in
artifacts/centering.npz); `data.zscore` is reproduced with stored means and deviations, so on the
test rows the result is that of fuse.py to the last bit.
"""
import json
import os

import numpy as np

import fuse                                    # lcp_model on PYTHONPATH
import signal_a

ART = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "artifacts")
ENCODERS = ("xlmr", "labse", "e5")
LEVELS = {1: "very easy", 2: "easy", 3: "neutral", 4: "difficult", 5: "very difficult"}


# ----------------------------------------------------------------------------- signal A models
def make_estimators():
    """The two unfitted estimators of signal_a.blend_ridge_hgb, with its hyperparameters."""
    import data
    from sklearn.ensemble import HistGradientBoostingRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    ridge = Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                      ("s", StandardScaler()), ("r", Ridge(alpha=300, random_state=data.SEED))])
    hgb = HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                        l2_regularization=1.0, random_state=data.SEED)
    return ridge, hgb


def blend_predict(models, X):
    """The prediction of blend_ridge_hgb from the two fitted estimators: the same mean."""
    return np.mean([m.predict(X) for m in models], axis=0)


def zs(v, mean_std):
    """data.zscore with stored constants: (v - mean) / std, non-finite values become 0."""
    mean, std = mean_std
    v = np.asarray(v, float)
    m = np.isfinite(v)
    z = np.zeros(len(v))
    z[m] = (v[m] - mean) / std
    return z


def partition_of(s):
    """'1|23|45' -> [[0], [1, 2], [3, 4]], the form of fuse.PARTITIONS."""
    return [[int(c) - 1 for c in b] for b in s.split("|")]


# ----------------------------------------------------------------------------- the system
class Fusion:
    def __init__(self, art=ART, load_models=True):
        with open(os.path.join(art, "params.json"), encoding="utf-8") as fh:
            self.params = json.load(fh)
        self.langs = list(self.params["languages"])
        self.encoders = list(self.params["encoders"])
        c = np.load(os.path.join(art, "centering.npz"))
        self.mu = {k: c[k] for k in c.files}
        self.models = {}
        if load_models:
            import joblib
            for e in self.encoders:
                self.models[e] = joblib.load(os.path.join(art, f"signal_a_{e}.joblib"))
        sc = self.params.get("scale")
        if sc:
            self.grid = np.linspace(0.0, 1.0, int(sc["points"]))
            self.label_q = np.asarray(sc["label_quantiles"], float)
            self.fused_q = {L: np.asarray(v, float) for L, v in sc["fused_quantiles"].items()}

    def lang(self, L):
        if L not in self.params["lang"]:
            raise ValueError(f"unknown language {L!r}")
        return self.params["lang"][L]

    # ------------------------------------------------------------------ A
    def features(self, enc, L, E, lex, fert):
        """signal_a.features with L's stored centring (mu_L, fert_mu_L)."""
        return signal_a.features(np.asarray(E, np.float32), np.asarray(lex, np.float32),
                                 np.asarray(fert, np.float32), self.mu[f"{enc}_{L}"],
                                 self.params["signal_a"]["fert_mu"][enc][L])

    def arms(self, enc, L, X):
        """(p_en, p_multi) of one encoder for feature rows X of language L."""
        m = self.models[enc]
        p_multi = blend_predict(m["p_multi"][L], X)
        p_en = p_multi if L == "en" else blend_predict(m["p_en"], X)
        return p_en, p_multi

    def a_z(self, L, arms):
        """z(A) of language L. `arms` maps each encoder to its (p_en, p_multi)."""
        za = self.params["signal_a"]["z"]
        avg = {}
        for k, c in enumerate(("p_en", "p_multi")):
            if len(self.encoders) == 1:
                avg[c] = np.asarray(arms[self.encoders[0]][k], float)
                continue
            acc = np.zeros(len(arms[self.encoders[0]][k]))
            for e in self.encoders:                   # the order of fuse.load_a
                acc += zs(arms[e][k], za[e][L][c])
            avg[c] = acc / len(self.encoders)
        p = self.lang(L)
        mix, w_src = p["a_mix"], p["w_src"]
        if w_src == 0.0:
            return zs(avg["p_multi"], mix["p_multi"])
        return zs(w_src * zs(avg["p_en"], mix["p_en"])
                  + (1 - w_src) * zs(avg["p_multi"], mix["p_multi"]), mix["mix"])

    # ------------------------------------------------------------------ B
    def b_raw(self, L, Ps):
        """fuse.b_of for language L. `Ps` maps each prompt to its (n, 5) digit distributions."""
        p = self.lang(L)["b"]
        order = self.params["b"]["prompts"]          # the order of fuse.load_b
        return fuse.b_of([np.asarray(Ps[k], float) for k in order], float(p["T"]),
                         partition_of(p["partition"]))

    def b_z(self, L, B):
        p = self.lang(L)["b"]
        return zs(B, (p["mean"], p["std"]))

    # ------------------------------------------------------------------ fusion and display
    def fused(self, L, zA, zB):
        w = self.lang(L)["w"]
        return w * np.asarray(zA, float) + (1 - w) * np.asarray(zB, float)

    def score01(self, L, fused):
        """Percentile in L's fused distribution, mapped through the pooled label quantiles."""
        pct = np.interp(np.asarray(fused, float), self.fused_q[L], self.grid)
        return np.interp(pct, self.grid, self.label_q)

    @staticmethod
    def level(score):
        """The rating 1..5 nearest to 1 + 4 * score (halves round up)."""
        return np.clip(np.floor(1.0 + 4.0 * np.asarray(score, float) + 0.5), 1, 5).astype(int)
