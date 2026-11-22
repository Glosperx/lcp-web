"""Stage 2: export the paper's signal A models and fusion constants to artifacts/, with a parity gate.

Per encoder (xlmr, labse, e5; setting mlsp+ro), on the data of signal_a.run (embeddings and lemmas
from the release cache, nothing is embedded or lemmatised here):
  p_en         ridge + HGB fitted on CompLex only;
  p_multi_L    one per language: CompLex plus the other ten languages (for en, without CompLex).
The estimators are those of signal_a.blend_ridge_hgb (lcp.fusion.make_estimators); every fit is
checked to give bit for bit the prediction of blend_ridge_hgb on the same data (--no-verify skips
the second fit). Also exported: the centring of every language (mu_L, fert_mu_L, from its test
rows, as signal_a.per_language) and of CompLex.

The exported models' predictions are written as signal_a.csv to a writable folder, next to a copy
of the release's signal_b.csv, and everything downstream is computed there with the functions of
fuse.py: the z-score constants of fuse.load_a and fuse.z_a (per encoder and arm, then the mean of
the encoders, then the mix with w_src), the LOLO parameters (model, T, partition, w_src, w) and the
constants of B. lcp/fusion.py then recomputes A, B and the fusion of every test row from the
artifacts alone.

Parity gate, fixed beforehand:
  - per encoder, exported predictions on the test rows (predicted one language at a time, as the
    site does) against p_en / p_multi of the release's signal_a.csv: max |dp| and r per language;
  - lcp/fusion.py against `fuse.py --with-ro --out` on the release, every row: max |d|;
  - mean r over the 11 languages 0.692521. If not bit-identical: r >= 0.9999 per language and
    encoder and a fused mean within 0.0005 of 0.692521, or the script stops (exit 1).

  docker/run_cuda.sh python scripts/export_model.py
Writes artifacts/ (params.json, centering.npz, signal_a_{enc}.joblib) and
bench/results/export_parity.txt. No dataset text is written or printed.
"""
import argparse
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
import data                                    # noqa: E402  (lcp_model on PYTHONPATH)
import fuse                                    # noqa: E402
import signal_a                                # noqa: E402
import signal_b                                # noqa: E402
from lcp import fusion as F                    # noqa: E402
from lcp.paper import use_release              # noqa: E402

SETTING = "mlsp+ro"
PAPER_MEAN = 0.692521
R_MIN, MEAN_TOL = 0.9999, 0.0005
SCALE_POINTS = 1001
LOG = []


def say(msg=""):
    print(msg, flush=True)
    LOG.append(msg)


def stop(msg):
    say(f"\n[STOP] {msg}")
    raise SystemExit(1)


# ----------------------------------------------------------------------------- data, as signal_a.run
class CachedOnly:
    """Stands in for signal_a.Encoder in embed_cached: the embeddings must come from the cache."""
    def __init__(self, key):
        self.key = key

    def embed(self, *_):
        stop(f"embeddings of {self.key} are not in the cache: the rows are not the expected ones")


def _no_lemmatize(work):
    stop(f"data.lemmas would lemmatise {len(work)} rows: cache/lemmas.csv does not cover the "
         "expected rows")


def prepare():
    data._lemmatize = _no_lemmatize        # guard: lemmas only from the cache, never written
    ev = data.load_eval(True)
    en = data.load_complex_en()
    lem_ev, lem_en = data.lemmas([("test", ev), ("complex_en", en.assign(lang="en"))])
    lex_en = data.lexical(list(en["token"]), ["en"] * len(en), lem_en)
    lex_ev = data.lexical(list(ev["token"]), list(ev["lang"]), lem_ev)
    fert_en = data.fertility(list(en["token"]))
    fert_ev = data.fertility(list(ev["token"]))
    return ev, en, lex_en, lex_ev, fert_en, fert_ev


def fit_pair(X, y):
    models = F.make_estimators()
    for m in models:
        m.fit(X, y)
    return models


def export_encoder(e, ev, en, lex_en, lex_ev, fert_en, fert_ev, verify):
    """Fitted models, centring and the exported predictions of one encoder."""
    t0 = time.time()
    Een, oken = signal_a.embed_cached(CachedOnly(e), en, "complex_en")
    Eev, okev = signal_a.embed_cached(CachedOnly(e), ev, "eval_ro")
    yen = en["complexity"].values.astype(float)[oken]
    mu_c = Een[oken].mean(0, keepdims=True)
    fmu_c = fert_en[oken].mean()
    Xen = signal_a.features(Een[oken], lex_en[oken], fert_en[oken], mu_c, fmu_c)
    y = ev["complexity"].values.astype(float)[okev]
    lang = ev["lang"].values[okev]
    idx = ev["idx"].values[okev]
    E, lex, fert = Eev[okev], lex_ev[okev], fert_ev[okev]
    X = signal_a.per_language(E, lex, fert, lang)
    langs = sorted(pd.unique(lang))

    mu, fmu = {"complex": mu_c[0]}, {"complex": float(fmu_c)}
    for L in langs:
        m = lang == L
        mu[L] = E[m].mean(0, keepdims=True)[0]
        fmu[L] = float(fert[m].mean())
        Xs = signal_a.features(E[m], lex[m], fert[m], mu[L][None, :], fmu[L])
        if not np.array_equal(Xs, X[m], equal_nan=True):     # NaN: non-Latin lexical columns
            stop(f"{e} {L}: features from the stored centring differ from per_language")

    models = {"p_en": fit_pair(Xen, yen), "p_multi": {}}
    if verify and not np.array_equal(F.blend_predict(models["p_en"], X),
                                     signal_a.blend_ridge_hgb(Xen, yen, X)):
        stop(f"{e} p_en: the exported estimators do not reproduce blend_ridge_hgb bit for bit")
    p_en, p_multi = np.empty(len(X)), np.empty(len(X))
    for L in langs:
        te, tr = lang == L, lang != L
        if L == "en":
            Xtr, ytr = X[tr], y[tr]
        else:
            Xtr, ytr = np.vstack([Xen, X[tr]]), np.concatenate([yen, y[tr]])
        models["p_multi"][L] = fit_pair(Xtr, ytr)
        if verify and not np.array_equal(F.blend_predict(models["p_multi"][L], X[te]),
                                         signal_a.blend_ridge_hgb(Xtr, ytr, X[te])):
            stop(f"{e} p_multi_{L}: the exported estimators do not reproduce blend_ridge_hgb")
        # predicted one language at a time from the stored centring, as on the site
        Xs = signal_a.features(E[te], lex[te], fert[te], mu[L][None, :], fmu[L])
        p_multi[te] = F.blend_predict(models["p_multi"][L], Xs)
        p_en[te] = p_multi[te] if L == "en" else F.blend_predict(models["p_en"], Xs)
    say(f"[A] {e}: CompLex {oken.sum()}/{len(en)}, test {okev.sum()}/{len(ev)}, "
        f"{1 + len(langs)} model pairs in {time.time() - t0:.0f}s"
        + (" (each checked against blend_ridge_hgb: identical)" if verify else ""))
    frame = pd.DataFrame({"setting": SETTING, "encoder": e, "lang": lang, "idx": idx,
                          "p_en": p_en, "p_multi": p_multi})
    feats = {L: (E[lang == L], lex[lang == L], fert[lang == L], idx[lang == L]) for L in langs}
    return models, mu, fmu, frame, feats


# ----------------------------------------------------------------------------- LOLO, as fuse.main
def test_features(ev, lex_ev, fert_ev):
    """{enc: {lang: (E, lex, fert, idx)}} of the test rows each encoder covers (no fitting)."""
    out = {}
    for e in F.ENCODERS:
        Eev, okev = signal_a.embed_cached(CachedOnly(e), ev, "eval_ro")
        lang, idx = ev["lang"].values[okev], ev["idx"].values[okev]
        E, lex, fert = Eev[okev], lex_ev[okev], fert_ev[okev]
        out[e] = {L: (E[lang == L], lex[lang == L], fert[lang == L], idx[lang == L])
                  for L in sorted(pd.unique(lang))}
    return out


def lolo(ev, models=None, boot=2000):
    """fuse.main with data.PRED_DIR as set: per language the frame d, model, T, partition, w_src,
    w, zA, fused, r and the bootstrap samples; plus the CI of the mean."""
    A = fuse.load_a(SETTING, list(F.ENCODERS))
    Bs = fuse.load_b(ev, models)
    y = ev.set_index("idx")["complexity"]
    r_b = {m: {lg: data.pearson(g["B"].values, y.loc[g["idx"]].values)
               for lg, g in f.groupby("lang")} for m, f in Bs.items()}
    test = fuse.signals(ev, A, Bs, r_b, exclude=())
    out, boots = {}, []
    for lg, d in test.items():
        fit_langs = {l: f for l, f in fuse.signals(ev, A, Bs, r_b, exclude={lg}).items() if l != lg}
        w_src, w = fuse.fit(fit_langs)
        zA = fuse.z_a(d, w_src)
        P = w * zA + (1 - w) * d["zB"].values
        y_l = d["complexity"].values
        r_f, s = data.boot_r(y_l, P, d["context_id"].values, boot)
        boots.append(s)
        lo, hi = np.percentile(s, [2.5, 97.5])
        b = Bs[d["model"].iloc[0]]
        b = b[b["lang"] == lg].iloc[0]
        out[lg] = dict(d=d, model=d["model"].iloc[0], T=float(b["T"]), partition=b["partition"],
                       w_src=w_src, w=w, zA=zA, fused=P, r_A=data.pearson(zA, y_l),
                       r_B=data.pearson(d["zB"].values, y_l), r_fused=r_f, lo=lo, hi=hi)
    m = min(len(s) for s in boots)
    lo, hi = np.percentile(np.vstack([s[:m] for s in boots]).mean(axis=0), [2.5, 97.5])
    return out, (float(lo), float(hi))


def mean_std(v):
    """The mean and deviation data.zscore would use on v."""
    v = np.asarray(v, float)
    m = np.isfinite(v)
    if m.sum() < 2 or not np.std(v[m]) > 0:
        stop("a z-score has fewer than two finite values or no spread")
    return [float(v[m].mean()), float(v[m].std())]


def a_constants():
    """{enc: {lang: {arm: [mean, std]}}} of the per-encoder z-scores in fuse.load_a."""
    d = pd.read_csv(f"{data.PRED_DIR}/signal_a.csv")
    d = d[d["setting"] == SETTING]
    out = {}
    for e in F.ENCODERS:
        f = d[d["encoder"] == e].sort_values(["lang", "idx"]).reset_index(drop=True)
        out[e] = {lg: {c: mean_std(g[c].values) for c in ("p_en", "p_multi")}
                  for lg, g in f.groupby("lang", sort=False)}
    return out


def lang_params(res):
    """params["lang"] and the per-row checks of the stored constants against fuse.py."""
    out = {}
    for lg, r in res.items():
        d = r["d"]
        pe, pm = d["p_en"].values, d["p_multi"].values
        mix = {"p_multi": mean_std(pm)}
        if r["w_src"] != 0.0:
            mix["p_en"] = mean_std(pe)
            mix["mix"] = mean_std(r["w_src"] * F.zs(pe, mix["p_en"])
                                  + (1 - r["w_src"]) * F.zs(pm, mix["p_multi"]))
        out[lg] = {"n": int(len(d)), "model": r["model"], "w_src": r["w_src"], "w": r["w"],
                   "a_mix": mix,
                   "b": {"T": r["T"], "partition": r["partition"], **dict(zip(
                       ("mean", "std"), mean_std(d["B"].values)))},
                   "r": {"A": r["r_A"], "B": r["r_B"], "fused": r["r_fused"], "lo": float(r["lo"]),
                         "hi": float(r["hi"])}}
    return out


def scale(res):
    """The display scale: fused quantiles per language, label quantiles of all languages pooled."""
    grid = np.linspace(0.0, 1.0, SCALE_POINTS)
    labels = np.concatenate([r["d"]["complexity"].values.astype(float) for r in res.values()])
    return {"points": SCALE_POINTS,
            "label_quantiles": [float(v) for v in np.quantile(labels, grid)],
            "fused_quantiles": {lg: [float(v) for v in np.quantile(r["fused"], grid)]
                                for lg, r in res.items()}}


def b_matrices(model):
    """(prompt order of fuse.load_b, {prompt: frame of p1..p5 by idx}) of signal_b.csv in
    data.PRED_DIR for one model, parsed as fuse.load_b parses it."""
    d = pd.read_csv(f"{data.PRED_DIR}/signal_b.csv")
    d = d[d["model"] == model]
    order = list(dict.fromkeys(d["prompt"]))
    pcols = [f"p{k}" for k in "12345"]
    return order, {p: d[d["prompt"] == p].set_index("idx")[pcols] for p in order}


# ----------------------------------------------------------------------------- checks
def fusion_rows(fz, res, feats_by_enc, bmat):
    """A, B and fused of every test row recomputed by lcp/fusion.py from the artifacts."""
    out = []
    for lg, r in res.items():
        idx = r["d"]["idx"].values
        arms = {}
        for e in fz.encoders:
            E, lex, fert, ix = feats_by_enc[e][lg]
            if not np.array_equal(ix, idx):
                stop(f"{e} {lg}: test rows of A and of the fusion differ")
            arms[e] = fz.arms(e, lg, fz.features(e, lg, E, lex, fert))
        zA = fz.a_z(lg, arms)
        Ps = {p: bmat[p].loc[idx].values.astype(float) for p in bmat}
        zB = fz.b_z(lg, fz.b_raw(lg, Ps))
        out.append(pd.DataFrame({"lang": lg, "idx": idx, "A": zA, "B": zB,
                                 "fused": fz.fused(lg, zA, zB)}))
    return pd.concat(out, ignore_index=True)


def run_fuse(pred_dir, out_csv, release):
    """`fuse.py --with-ro --out` in a subprocess, with data.PRED_DIR = pred_dir."""
    code = ("import sys, data; from lcp.paper import use_release; use_release(sys.argv[1]); "
            "data.PRED_DIR = sys.argv[2]; import fuse; "
            "sys.argv = ['fuse.py', '--with-ro', '--out', sys.argv[3]]; fuse.main()")
    p = subprocess.run([sys.executable, "-c", code, release, pred_dir, out_csv],
                       capture_output=True, text=True, cwd=ROOT)
    if p.returncode:
        stop(f"fuse.py failed: {p.stderr[-2000:]}")
    return p.stdout


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def data_hashes(release, extra=()):
    rel = os.path.realpath(release)
    files = sorted(glob.glob(os.path.join(data.mlsp_dir(), "*", "multils_test_*_lcp_labels.tsv")))
    files = [f for f in files if os.sep + "All" + os.sep not in f]
    files += [os.environ["ROLCP_CSV"]]
    files += [os.path.join(data.CACHE_DIR, os.path.basename(f)) for f in data.COMPLEX_FILES]
    files += [os.path.join(data.CACHE_DIR, "lemmas.csv")]
    for e in F.ENCODERS:
        for part in ("complex_en_8423", "eval_ro_7211"):
            files += [os.path.join(data.CACHE_DIR, f"emb_{e}_{part}{s}.npy") for s in ("", "_ok")]
    files += [os.path.join(rel, "predictions", "signal_a.csv"),
              os.path.join(rel, "predictions", "signal_b.csv")] + list(extra)
    return {os.path.relpath(os.path.realpath(f), rel).replace(os.sep, "/"): sha256(f)
            for f in files}


def revisions():
    import joblib
    import scipy
    import sklearn
    from lcp import rater
    return {"encoders": {e: list(signal_a.ENCODERS[e]) for e in F.ENCODERS},
            "fertility_tokenizer": ["xlm-roberta-base", data.XLMR_REVISION],
            "gemma_tokenizer": list(signal_b.GEMMA4_QAT), "gguf": list(rater.GGUF),
            "scikit-learn": sklearn.__version__, "numpy": np.__version__,
            "scipy": scipy.__version__, "pandas": pd.__version__, "joblib": joblib.__version__}


def compare_a(new, release):
    """Max |dp| and r per encoder, arm and language, exported against the release."""
    old = pd.read_csv(os.path.join(release, "predictions", "signal_a.csv"),
                      float_precision="round_trip")
    old = old[(old["setting"] == SETTING) & old["encoder"].isin(F.ENCODERS)]
    k = ["encoder", "lang", "idx"]
    m = new.merge(old, on=k, suffixes=("", "_old"), how="outer", indicator=True)
    if not (m["_merge"] == "both").all():
        stop(f"exported and stored signal A cover different rows: {m['_merge'].value_counts()}")
    worst_r, identical = 1.0, True
    for e in F.ENCODERS:
        for c in ("p_en", "p_multi"):
            parts = []
            for lg, g in m[m["encoder"] == e].groupby("lang"):
                dp = np.abs(g[c].values - g[c + "_old"].values).max()
                r = data.pearson(g[c].values, g[c + "_old"].values)
                identical &= bool(dp == 0)
                worst_r = min(worst_r, r)
                parts.append(f"{lg} {dp:.2g}/{r:.6f}")
            say(f"  {e:5s} {c:7s} max|dp|/r: " + "  ".join(parts))
    return identical, worst_r


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--paper-release", default="/paper/release")
    ap.add_argument("--artifacts", default="artifacts")
    ap.add_argument("--work", default="reference/_work/export",
                    help="writable folder for the exported signal_a.csv and fuse.py outputs")
    ap.add_argument("--report", default="bench/results/export_parity.txt")
    ap.add_argument("--no-verify", action="store_true",
                    help="skip the second fit of every model through blend_ridge_hgb")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    release = use_release(a.paper_release)
    os.makedirs(a.artifacts, exist_ok=True)
    os.makedirs(a.work, exist_ok=True)
    t_all = time.time()

    ev, en, lex_en, lex_ev, fert_en, fert_ev = prepare()
    say(f"[data] test {len(ev)} rows ({ev['lang'].nunique()} languages), CompLex {len(en)}")
    import joblib
    frames, mus, fmus, feats_by_enc = [], {}, {}, {}
    for e in F.ENCODERS:
        models, mu, fmu, frame, feats = export_encoder(e, ev, en, lex_en, lex_ev, fert_en,
                                                       fert_ev, not a.no_verify)
        path = os.path.join(a.artifacts, f"signal_a_{e}.joblib")
        joblib.dump(models, path, compress=3)
        back = joblib.load(path)
        for L, (E, lex, fert, _) in feats.items():
            Xs = signal_a.features(E, lex, fert, mu[L][None, :], fmu[L])
            if not (np.array_equal(F.blend_predict(back["p_multi"][L], Xs),
                                   F.blend_predict(models["p_multi"][L], Xs))
                    and np.array_equal(F.blend_predict(back["p_en"], Xs),
                                       F.blend_predict(models["p_en"], Xs))):
                stop(f"{e} {L}: the models reloaded from {path} predict differently")
        frames.append(frame)
        mus[e], fmus[e], feats_by_enc[e] = mu, fmu, feats
    np.savez(os.path.join(a.artifacts, "centering.npz"),
             **{f"{e}_{L}": v.astype(np.float32) for e in F.ENCODERS for L, v in mus[e].items()})

    new = pd.concat(frames, ignore_index=True).sort_values(["setting", "encoder", "idx"],
                                                           kind="stable")
    new.to_csv(os.path.join(a.work, "signal_a.csv"), index=False)
    shutil.copyfile(os.path.join(release, "predictions", "signal_b.csv"),
                    os.path.join(a.work, "signal_b.csv"))
    say("\n[gate A] exported predictions (per language, from the stored centring) vs the "
        "release's signal_a.csv")
    a_identical, a_worst_r = compare_a(new, release)
    say(f"[gate A] bit-identical: {a_identical}; lowest r {a_worst_r:.6f}")

    # LOLO and constants from the exported A, with the paper's B
    data.PRED_DIR = os.path.abspath(a.work)
    res, ci = lolo(ev, None, a.boot)
    za = a_constants()
    lp = lang_params(res)
    order, bmat = b_matrices(next(iter(res.values()))["model"])
    models_used = {r["model"] for r in res.values()}
    if len(models_used) != 1:
        stop(f"more than one language model selected: {models_used}")
    params = {
        "description": "lcp-web stage 2: signal A models, centring, z-score constants, LOLO "
                       "fusion parameters and display scale. Numbers only, no dataset text.",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "languages": sorted(res), "encoders": list(F.ENCODERS), "setting": SETTING,
        "revisions": revisions(),
        "data_sha256": data_hashes(release),
        "signal_a": {"fert_mu": fmus, "z": za},
        "b": {"source": "paper, MLX (predictions/signal_b.csv)", "model": next(iter(models_used)),
              "prompts": order},
        "lang": lp,
        "mean_r": {"A": float(np.mean([r["r_A"] for r in res.values()])),
                   "B": float(np.mean([r["r_B"] for r in res.values()])),
                   "fused": float(np.mean([r["r_fused"] for r in res.values()])),
                   "ci": list(ci)},
        "scale": scale(res),
    }
    with open(os.path.join(a.artifacts, "params.json"), "w", encoding="utf-8") as fh:
        json.dump(params, fh, indent=1)

    # ------------------------------------------------------------ gate: fusion
    fz = F.Fusion(a.artifacts)
    got = fusion_rows(fz, res, feats_by_enc, bmat)
    ref_lolo = pd.concat([pd.DataFrame({"lang": lg, "idx": r["d"]["idx"].values, "A": r["zA"],
                                        "B": r["d"]["zB"].values, "fused": r["fused"]})
                          for lg, r in res.items()], ignore_index=True)
    d_self = {c: float(np.abs(got[c].values - ref_lolo[c].values).max()) for c in ("A", "B", "fused")}
    say("\n[gate fusion] lcp/fusion.py from the artifacts vs fuse.py functions on the same "
        "(exported) A: max |d| " + ", ".join(f"{k} {v:.3g}" for k, v in d_self.items()))
    out_paper = os.path.join(a.work, "fused_paper.csv")
    out_export = os.path.join(a.work, "fused_export.csv")
    txt_paper = run_fuse(os.path.join(release, "predictions"), out_paper, release)
    txt_export = run_fuse(os.path.abspath(a.work), out_export, release)
    say("\n`fuse.py --with-ro` on the release (paper):")
    say(txt_paper.rstrip().split("\n-> ")[0])
    say("\n`fuse.py --with-ro` on the exported A:")
    say(txt_export.rstrip().split("\n-> ")[0])
    k = ["lang", "idx"]
    for name, path in (("release (paper)", out_paper), ("exported A", out_export)):
        ref = pd.read_csv(path, float_precision="round_trip")
        m = got.merge(ref, on=k, suffixes=("", "_ref"), how="outer", indicator=True)
        if not (m["_merge"] == "both").all():
            stop(f"fusion rows differ from fuse.py --out on the {name}")
        dd = {c: float(np.abs(m[c] - m[c + "_ref"]).max()) for c in ("A", "B", "fused")}
        say(f"[gate fusion] lcp/fusion.py vs fuse.py --out on the {name}, {len(m)} rows: max |d| "
            + ", ".join(f"{c} {v:.3g}" for c, v in dd.items()))
    y = ev.set_index("idx")["complexity"]
    r_lang = {lg: data.pearson(g["fused"].values, y.loc[g["idx"]].values)
              for lg, g in got.groupby("lang")}
    mean_r = float(np.mean(list(r_lang.values())))
    say("[gate fusion] r per language (lcp/fusion.py): "
        + "  ".join(f"{lg} {v:.4f}" for lg, v in r_lang.items()))
    say(f"[gate fusion] mean over {len(r_lang)} languages {mean_r:.6f} (paper {PAPER_MEAN}), "
        f"95% CI [{ci[0]:.4f}, {ci[1]:.4f}]")
    say("[params] per language: " + "  ".join(
        f"{lg} T{p['b']['T']:g} {p['b']['partition']} w_src {p['w_src']:g} w {p['w']:g}"
        for lg, p in lp.items()))

    exact = a_identical and f"{mean_r:.6f}" == f"{PAPER_MEAN:.6f}"
    ok = exact or (a_worst_r >= R_MIN and abs(mean_r - PAPER_MEAN) <= MEAN_TOL)
    say(f"\n[gate] {'PASS' if ok else 'FAIL'}: "
        + ("bit-identical signal A, mean " if exact else
           f"lowest r of A {a_worst_r:.6f} (>= {R_MIN}), mean ") + f"{mean_r:.6f}"
        + f"; {time.time() - t_all:.0f}s in all")
    os.makedirs(os.path.dirname(a.report) or ".", exist_ok=True)
    with open(a.report, "w", encoding="utf-8") as fh:
        fh.write("\n".join(LOG) + "\n")
    print(f"-> {a.artifacts}/, {a.report}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
