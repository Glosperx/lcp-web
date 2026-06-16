# =============================================================================
# Sugestia lui Sergiu: "incercati metode de regresie si regularizare (Ridge, Lasso)".
# Compara regresoare pe feature-space-ul REAL al solutiei (768 embedding XLM-R + lexical),
# prin free-gate-ul cross-lingual (train EN<->test MLSP) + CV 5-fold in-sursa.
# Reutilizeaza loaderele testate din solution_bert (embed din cache .npy => aliniere garantata;
# modelul se incarca o data dar nu re-embed-eaza). Raspunde: bate Lasso/ElasticNet Ridge-ul (alpha=300)?
# NU atinge solutia. CPU.
# =============================================================================
import os
import sys
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from scipy.stats import pearsonr
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold

from solution_bert import XLMR, _load_complex_en, _load_mlsp, _Xc, blend_ridge_hgb, SEED


def pipe_pred(make_est):
    def f(Xtr, ytr, Xp):
        m = Pipeline([("s", StandardScaler()), ("e", make_est())])
        m.fit(Xtr, ytr)
        return m.predict(Xp)
    return f


def cv_r(pred_fn, X, y, k=5):
    pred = np.zeros(len(y))
    for tr, te in KFold(n_splits=k, shuffle=True, random_state=SEED).split(X):
        pred[te] = pred_fn(X[tr], y[tr], X[te])
    return pearsonr(pred, y)[0]


REGRESSORS = {
    "Ridge(a=300) [solutie-liniar]": pipe_pred(lambda: Ridge(alpha=300, random_state=SEED)),
    "Ridge(a=1)":                    pipe_pred(lambda: Ridge(alpha=1, random_state=SEED)),
    "Lasso(a=0.01)":                 pipe_pred(lambda: Lasso(alpha=0.01, max_iter=8000, random_state=SEED)),
    "Lasso(a=0.001)":                pipe_pred(lambda: Lasso(alpha=0.001, max_iter=8000, random_state=SEED)),
    "ElasticNet(a=0.01,l1=.5)":      pipe_pred(lambda: ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=8000, random_state=SEED)),
    "LinearRegression(OLS)":         pipe_pred(lambda: LinearRegression()),
    "blend Ridge300+HGB [SOLUTIE]":  blend_ridge_hgb,
}


def main():
    print("[incarc] XLM-R (embed din cache) + CompLex EN + MLSP Romanic ...")
    xr = XLMR("last4", "xlmr")
    Een, lex_en, yen, oken = _load_complex_en(xr, ())
    src = _load_mlsp(xr, ())
    if src is None:
        sys.exit("nevoie de data/mlsp/")
    Em, lex_ml, yml, okm = src
    Xen = _Xc(Een[oken], lex_en[oken], Een.mean(0, keepdims=True)); yen = yen[oken]
    Xml = _Xc(Em[okm], lex_ml[okm], Em[okm].mean(0, keepdims=True)); yml = yml[okm]
    print(f"[date] EN {Xen.shape} | MLSP {Xml.shape} | dim={Xen.shape[1]}")

    print(f"\n{'regresor':32s} {'EN->ML':>8s} {'ML->EN':>8s} {'transf_avg':>11s} {'cvEN':>7s} {'cvML':>7s}")
    print("-" * 80)
    for name, fn in REGRESSORS.items():
        r_en2ml = pearsonr(fn(Xen, yen, Xml), yml)[0]
        r_ml2en = pearsonr(fn(Xml, yml, Xen), yen)[0]
        cve, cvm = cv_r(fn, Xen, yen), cv_r(fn, Xml, yml)
        print(f"{name:32s} {r_en2ml:8.4f} {r_ml2en:8.4f} {0.5*(r_en2ml+r_ml2en):11.4f} {cve:7.4f} {cvm:7.4f}")


if __name__ == "__main__":
    main()
