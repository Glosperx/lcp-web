"""Signal A with other regression models, for the documentation (Section 4, signal A tables).

Step 3 of signal A (release/signal_a.py) averages a ridge regression and gradient-boosted trees. Here the
same step is run with one model at a time instead: ridge alone, HGB alone, ExtraTrees, RandomForest,
LightGBM, CatBoost, XGBoost, an MLP and kNN, with the hyperparameters of the development runs
(solution_bert.py, August 2026). Everything else is the release pipeline: the same features (cached
embeddings of the three encoders, centred per language, plus subword count and the lexical columns),
the same two regressors per encoder (English and multilingual, LOLO over 11 languages), then the
fusion of release/fuse.py with signal B unchanged and w_src, w chosen on the other languages.

release/ is imported, never modified. No encoder and no language model is run: the embeddings come
from release/cache. The model "blend" is the release regressor and must reproduce
release/predictions/signal_a.csv (setting mlsp+ro); the script stops if it does not.

Usage (envs ml_def; XGBoost is not in ml_def, pass a directory that has it with --pylib):
  python analysis_doc_signal_a_models.py features            # once, writes the feature blocks
  python analysis_doc_signal_a_models.py fit --model catboost  # one model, writes its predictions
  python analysis_doc_signal_a_models.py report > output/doc_signal_a_models.txt
"""
import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
REL = os.path.join(ROOT, "release")
WORK = os.path.join(ROOT, "output", "doc_signal_a_models")
sys.path.insert(0, REL)
os.chdir(REL)
import data  # noqa: E402
import signal_a  # noqa: E402

ENCODERS = ("xlmr", "labse", "e5")
SEED = data.SEED
MODELS = ("blend", "ridge", "hgb", "extratrees", "randomforest", "lightgbm", "catboost", "xgboost",
          "mlp", "knn")
NAMES = {"blend": "Ridge + HGB (ours)", "ridge": "Ridge", "hgb": "HGB", "extratrees": "ExtraTrees",
         "randomforest": "RandomForest", "lightgbm": "LightGBM", "catboost": "CatBoost",
         "xgboost": "XGBoost", "mlp": "MLP", "knn": "kNN"}


# ----------------------------------------------------------------------------- models
def _pipe(Xtr, ytr, Xpred, est):
    """Median imputer + scaler + estimator, as the ridge half of release/signal_a.py:91-101."""
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    m = Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                  ("s", StandardScaler()), ("e", est)])
    return np.asarray(m.fit(Xtr, ytr).predict(Xpred), float).ravel()


def predict(model, Xtr, ytr, Xpred):
    if model == "blend":                       # the release regressor, unchanged
        return signal_a.blend_ridge_hgb(Xtr, ytr, Xpred)
    if model == "ridge":
        from sklearn.linear_model import Ridge
        return _pipe(Xtr, ytr, Xpred, Ridge(alpha=300, random_state=SEED))
    if model == "hgb":                         # the HGB half of the blend, native NaN handling
        from sklearn.ensemble import HistGradientBoostingRegressor
        return HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                             l2_regularization=1.0, random_state=SEED
                                             ).fit(Xtr, ytr).predict(Xpred)
    if model == "extratrees":                  # solution_bert.py _mk_et
        from sklearn.ensemble import ExtraTreesRegressor
        return _pipe(Xtr, ytr, Xpred, ExtraTreesRegressor(n_estimators=500, max_features=0.3,
                                                          n_jobs=-1, random_state=SEED))
    if model == "randomforest":                # solution_bert.py _mk_rf(300)
        from sklearn.ensemble import RandomForestRegressor
        return _pipe(Xtr, ytr, Xpred, RandomForestRegressor(n_estimators=300, max_features=0.3,
                                                            n_jobs=-1, random_state=SEED))
    if model == "lightgbm":                    # solution_bert.py _lgbm_pred, lgbm-l8; n_jobs=1 (libomp)
        from lightgbm import LGBMRegressor
        return np.asarray(LGBMRegressor(num_leaves=8, max_depth=3, learning_rate=0.05,
                                        n_estimators=400, reg_lambda=1.0, n_jobs=1,
                                        random_state=SEED, verbose=-1
                                        ).fit(Xtr, ytr).predict(Xpred), float)
    if model == "catboost":                    # solution_bert.py _cat_pred, cat-d3
        from catboost import CatBoostRegressor
        return np.asarray(CatBoostRegressor(depth=3, learning_rate=0.05, iterations=400,
                                            l2_leaf_reg=1.0, random_seed=SEED, verbose=False,
                                            allow_writing_files=False, thread_count=-1
                                            ).fit(Xtr, ytr).predict(Xpred), float)
    if model == "xgboost":                     # new: same capacity as HGB (depth 3, 400 trees)
        from xgboost import XGBRegressor
        return np.asarray(XGBRegressor(max_depth=3, learning_rate=0.05, n_estimators=400,
                                       reg_lambda=1.0, tree_method="hist", n_jobs=-1,
                                       random_state=SEED).fit(Xtr, ytr).predict(Xpred), float)
    if model == "mlp":                         # solution_bert.py _mk_mlp(128)
        from sklearn.neural_network import MLPRegressor
        return _pipe(Xtr, ytr, Xpred, MLPRegressor(hidden_layer_sizes=(128,), alpha=1e-3,
                                                   early_stopping=True, n_iter_no_change=10,
                                                   max_iter=300, random_state=SEED))
    if model == "knn":                         # solution_bert.py _mk_knn(50)
        from sklearn.neighbors import KNeighborsRegressor
        return _pipe(Xtr, ytr, Xpred, KNeighborsRegressor(n_neighbors=50, n_jobs=-1))
    raise ValueError(model)


# ----------------------------------------------------------------------------- features
def features():
    """The feature blocks of release/signal_a.py:run for the 11-language setting, per encoder."""
    ev = data.load_eval(True)
    en = data.load_complex_en()
    lem_ev, lem_en = data.lemmas([("test", ev), ("complex_en", en.assign(lang="en"))])
    lex_en = data.lexical(list(en["token"]), ["en"] * len(en), lem_en)
    lex_ev = data.lexical(list(ev["token"]), list(ev["lang"]), lem_ev)
    fert_en = data.fertility(list(en["token"]))
    fert_ev = data.fertility(list(ev["token"]))
    os.makedirs(WORK, exist_ok=True)
    for enc in ENCODERS:
        load = lambda part, n: (np.load(os.path.join(data.CACHE_DIR, f"emb_{enc}_{part}_{n}.npy")),
                                np.load(os.path.join(data.CACHE_DIR, f"emb_{enc}_{part}_{n}_ok.npy")))
        Een, oken = load("complex_en", len(en))
        Eev, okev = load("eval_ro", len(ev))
        Xen = signal_a.features(Een[oken], lex_en[oken], fert_en[oken],
                                Een[oken].mean(0, keepdims=True), fert_en[oken].mean())
        X = signal_a.per_language(Eev[okev], lex_ev[okev], fert_ev[okev], ev["lang"].values[okev])
        np.savez(os.path.join(WORK, f"features_{enc}.npz"), Xen=Xen,
                 yen=en["complexity"].values.astype(float)[oken], X=X,
                 y=ev["complexity"].values.astype(float)[okev],
                 lang=np.asarray(ev["lang"].values[okev], dtype="U8"), idx=ev["idx"].values[okev])
        print(f"features {enc}: CompLex {Xen.shape}, eval {X.shape}", flush=True)


# ----------------------------------------------------------------------------- fit
def fit(model):
    """p_en and p_multi for every encoder, exactly as release/signal_a.py:run, with `model`."""
    rows = []
    for enc in ENCODERS:
        z = np.load(os.path.join(WORK, f"features_{enc}.npz"))
        Xen, yen, X, y, lang, idx = z["Xen"], z["yen"], z["X"], z["y"], z["lang"], z["idx"]
        t0 = time.time()
        p_en_all = predict(model, Xen, yen, X)
        p_en, p_multi = np.empty(len(X)), np.empty(len(X))
        for L in sorted(pd.unique(lang)):
            te, tr = lang == L, lang != L
            if L == "en":
                Xtr, ytr = X[tr], y[tr]
            else:
                Xtr, ytr = np.vstack([Xen, X[tr]]), np.concatenate([yen, y[tr]])
            p_multi[te] = predict(model, Xtr, ytr, X[te])
            p_en[te] = p_multi[te] if L == "en" else p_en_all[te]
        print(f"{model} {enc}: {time.time() - t0:.0f}s", flush=True)
        rows.append(pd.DataFrame({"setting": "mlsp+ro", "encoder": enc, "lang": lang, "idx": idx,
                                  "p_en": p_en, "p_multi": p_multi}))
    out = pd.concat(rows, ignore_index=True)
    if model == "blend":                       # control: the release predictions
        ref = pd.read_csv(os.path.join(data.PRED_DIR, "signal_a.csv"), float_precision="round_trip")
        ref = ref[(ref["setting"] == "mlsp+ro") & ref["encoder"].isin(ENCODERS)]
        m = out.merge(ref, on=["encoder", "lang", "idx"], suffixes=("", "_ref"))
        err = max(np.abs(m["p_en"] - m["p_en_ref"]).max(), np.abs(m["p_multi"] - m["p_multi_ref"]).max())
        print(f"control: {len(m)}/{len(out)} rows matched, max |diff| vs release = {err:.2e}", flush=True)
        if len(m) != len(out) or err > 1e-9:
            raise SystemExit("blend does not reproduce release/predictions/signal_a.csv")
    out.to_csv(os.path.join(WORK, f"signal_a_{model}.csv"), index=False)


# ----------------------------------------------------------------------------- report
def fuse_with(model):
    """fuse.py --with-ro with this model's signal A: {lang: dict(F, A, B: (r, boot), zA, zB, y)}."""
    import fuse
    a = pd.read_csv(os.path.join(WORK, f"signal_a_{model}.csv"))
    read_csv = pd.read_csv
    pd.read_csv = lambda p, *x, **kw: a.copy() if str(p).endswith("signal_a.csv") else read_csv(p, *x, **kw)
    try:
        ev = data.load_eval(True)
        A = fuse.load_a("mlsp+ro", list(ENCODERS))
        Bs = fuse.load_b(ev, None)
    finally:
        pd.read_csv = read_csv
    y = ev.set_index("idx")["complexity"]
    r_b = {m: {lg: data.pearson(g["B"].values, y.loc[g["idx"]].values)
               for lg, g in f.groupby("lang")} for m, f in Bs.items()}
    out = {}
    for lg, d in fuse.signals(ev, A, Bs, r_b, exclude=()).items():
        fit_langs = {l: f for l, f in fuse.signals(ev, A, Bs, r_b, exclude={lg}).items() if l != lg}
        w_src, w = fuse.fit(fit_langs)
        zA = fuse.z_a(d, w_src)
        P = w * zA + (1 - w) * d["zB"].values
        y_l, g = d["complexity"].values, d["context_id"].values
        out[lg] = {k: data.boot_r(y_l, v, g, 2000) for k, v in (("F", P), ("A", zA))}
        out[lg].update(zA=zA, zB=d["zB"].values, idx=d["idx"].values, w_src=w_src, w=w)
    return out


def report():
    res = {m: fuse_with(m) for m in MODELS if os.path.exists(os.path.join(WORK, f"signal_a_{m}.csv"))}
    base = res["blend"]
    langs = sorted(base)
    for o in res.values():
        for l in langs:
            assert len(o[l]["F"][1]) == len(base[l]["F"][1]) == 2000, "degenerate bootstrap resample"
            assert (o[l]["idx"] == base[l]["idx"]).all()
    mean = lambda o, k: float(np.mean([o[l][k][0] for l in langs]))
    print("Signal A with other regression models, 11 languages (fuse.py --with-ro logic, signal B "
          "unchanged).\nWritten by analysis_doc_signal_a_models.py. Intervals: paired bootstrap, 2000 "
          "resamples of contexts (data.boot_r seed), difference from Ridge + HGB.\n")
    print(f"{'model':22s} {'r_A':>8s} {'fused':>9s}  {'fused vs ours':>34s}  {'rho(A,B)':>8s}")
    for m, o in res.items():
        s = np.mean([o[l]["F"][1] - base[l]["F"][1] for l in langs], axis=0)
        lo, hi = np.percentile(s, [2.5, 97.5])
        rab = np.mean([np.corrcoef(o[l]["zA"], o[l]["zB"])[0, 1] for l in langs])
        print(f"{NAMES[m]:22s} {mean(o, 'A'):.6f} {mean(o, 'F'):.6f}  "
              f"{mean(o, 'F') - mean(base, 'F'):+.4f} [{lo:+.4f}, {hi:+.4f}]  {rab:8.3f}")
    print("\nper-language r_A:")
    print(pd.DataFrame({NAMES[m]: {l: o[l]["A"][0] for l in langs} for m, o in res.items()}).T
          .to_string(float_format=lambda v: f"{v:.4f}"))
    print("\nper-language fused r:")
    print(pd.DataFrame({NAMES[m]: {l: o[l]["F"][0] for l in langs} for m, o in res.items()}).T
          .to_string(float_format=lambda v: f"{v:.4f}"))
    print("\ncorrelation between the signal A of two models (Pearson within each language, mean over "
          "the 11 languages):")
    ms = list(res)
    C = pd.DataFrame([[np.mean([np.corrcoef(res[a][l]["zA"], res[b][l]["zA"])[0, 1] for l in langs])
                       for b in ms] for a in ms], index=[NAMES[m] for m in ms],
                     columns=[NAMES[m] for m in ms])
    print(C.to_string(float_format=lambda v: f"{v:.3f}"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("step", choices=("features", "fit", "report"))
    ap.add_argument("--model", choices=MODELS)
    ap.add_argument("--pylib", default=None, help="extra directory for imports (XGBoost)")
    a = ap.parse_args()
    if a.pylib:
        sys.path.insert(0, a.pylib)
    if a.step == "features":
        features()
    elif a.step == "fit":
        if not a.model:
            ap.error("fit needs --model")
        fit(a.model)
    else:
        report()


if __name__ == "__main__":
    main()
