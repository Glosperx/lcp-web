"""Fuse signals A and B leave-one-language-out and report Pearson r per language.

Every parameter applied to a held-out language L is chosen on the other languages:

  1. Signal A is the average of the encoders' predictions, each standardised within the language.
     Its two arms are mixed as z(w_src * z(p_en) + (1 - w_src) * z(p_multi)).
  2. Signal B is the mean over prompts of the expected rating under the digit distribution raised
     to 1/T and renormalised, with the five digits optionally merged into contiguous blocks. T is
     chosen first, then the partition, each by mean r over the other languages.
  3. The language model is the one with the highest mean r of B over the other languages.
  4. The fused prediction is w * z(A) + (1 - w) * z(B). The pair (w_src, w) is chosen by a nested
     criterion: a candidate w_src is scored by its mean r over the fitting languages, where the w
     used for each fitting language L' is itself fitted without L and L'.
The signals of the fitting languages are their own leave-one-out predictions, so L's labels reach
them at second order (as training data for A, and through T and the partition of B). Excluding L
from the choice of T and partition as well changes the mean r by less than 0.0002.

Usage:
  python fuse.py                       # 10 MLSP languages, the configuration in the paper
  python fuse.py --with-ro             # plus RoLCP as an 11th language
  python fuse.py --encoders xlmr       # a single encoder
  python fuse.py --models qwen3-8b-4bit
"""
import argparse
import itertools

import numpy as np
import pandas as pd

import data

T_GRID = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0, 24.0, 32.0, 64.0)
# Every partition of the five ratings into contiguous blocks; a block is valued at its mean rating.
PARTITIONS = [[list(range(a, b)) for a, b in zip((0,) + c, c + (5,))]
              for k in (2, 3, 4, 5) for c in itertools.combinations(range(1, 5), k - 1)]
NEUTRAL = PARTITIONS.index([[0], [1], [2], [3], [4]])
W_GRID = np.round(np.arange(0.0, 1.0001, 0.05), 2)
SRC_GRID = np.round(np.arange(0.0, 1.0001, 0.125), 3)


# ----------------------------------------------------------------------------- signal A
def load_a(setting, encoders):
    """{idx: (lang, p_en, p_multi)} as a frame; several encoders are averaged on z-scores."""
    d = pd.read_csv(f"{data.PRED_DIR}/signal_a.csv")
    d = d[d["setting"] == setting]
    frames = []
    for e in encoders:
        f = d[d["encoder"] == e].sort_values(["lang", "idx"]).reset_index(drop=True)
        if f.empty:
            raise SystemExit(f"no signal A for encoder {e!r} in setting {setting!r}. "
                             f"Run: python signal_a.py --encoder {e}"
                             + (" --with-ro" if setting == "mlsp+ro" else ""))
        if frames and not f["idx"].equals(frames[0]["idx"]):
            raise SystemExit(f"encoder {e!r} does not cover the same rows as {encoders[0]!r}")
        frames.append(f)
    out = frames[0][["lang", "idx"]].copy()
    for c in ("p_en", "p_multi"):
        if len(frames) == 1:
            out[c] = frames[0][c].values
            continue
        acc = np.zeros(len(out))
        for f in frames:
            z = np.zeros(len(f))
            for _, g in f.groupby("lang", sort=False):
                z[g.index.values] = data.zscore(g[c].values)
            acc += z
        out[c] = acc / len(frames)
    return out


def z_a(d, w_src):
    pm = d["p_multi"].values
    if w_src == 0.0:
        return data.zscore(pm)
    return data.zscore(w_src * data.zscore(d["p_en"].values) + (1 - w_src) * data.zscore(pm))


# ----------------------------------------------------------------------------- signal B
def temper(P, T):
    if T == 1.0:
        return P
    Q = np.power(P, 1.0 / T)
    return Q / Q.sum(axis=1, keepdims=True)


def b_of(Ps, T, part):
    v = np.array([np.mean([i + 1 for i in b]) for b in part], float)
    E = [np.column_stack([temper(P, T)[:, b].sum(axis=1) for b in part]) @ v for P in Ps]
    return (np.mean(E, axis=0) - 1.0) / 4.0


def build_b(per_lang):
    """{lang: (B, T, partition)}. `per_lang` maps a language to (list of prompt matrices, y)."""
    langs = sorted(per_lang)
    R = {lg: np.array([[data.pearson(b_of(Ps, T, p), y) for p in PARTITIONS] for T in T_GRID])
         for lg, (Ps, y) in per_lang.items()}

    def pick_t(exclude):
        crit = np.mean([R[l][:, NEUTRAL] for l in langs if l not in exclude], axis=0)
        return int(np.argmax(crit))

    out = {}
    for lg in langs:
        keep = [l for l in langs if l != lg]
        crit = np.zeros(len(PARTITIONS))
        for l in keep:
            crit += R[l][pick_t((lg, l)), :]
        T, part = T_GRID[pick_t((lg,))], PARTITIONS[int(np.argmax(crit / len(keep)))]
        out[lg] = (b_of(per_lang[lg][0], T, part), T, part)
    return out


def load_b(ev, models):
    """{model: frame with lang, idx, B, T, partition}."""
    d = pd.read_csv(f"{data.PRED_DIR}/signal_b.csv")
    d = d[d["idx"].isin(ev["idx"])]
    y = ev.set_index("idx")["complexity"]
    out = {}
    for m in models or sorted(d["model"].unique()):
        dm = d[d["model"] == m]
        if dm.empty:
            raise SystemExit(f"no signal B for model {m!r}. Run: python signal_b.py --model {m}")
        prompts = list(dict.fromkeys(dm["prompt"]))
        wide = {p: dm[dm["prompt"] == p].set_index("idx") for p in prompts}
        idx = sorted(set.intersection(*(set(w.index) for w in wide.values())))
        pcols = [f"p{k}" for k in "12345"]
        dist = all(np.isfinite(w.loc[idx, pcols].values).all() for w in wide.values())
        frame = pd.DataFrame({"idx": idx, "lang": wide[prompts[0]].loc[idx, "lang"].values})
        n = frame["lang"].value_counts()
        short = sorted(lg for lg, k in n.items() if k < (ev["lang"] == lg).sum())
        if short:
            raise SystemExit(f"model {m!r} covers only part of {short}. "
                             f"Run: python signal_b.py --model {m}, without --limit or --langs")
        if dist:
            per_lang = {lg: ([wide[p].loc[g["idx"], pcols].values.astype(float) for p in prompts],
                             y.loc[g["idx"]].values) for lg, g in frame.groupby("lang")}
            for lg, (B, T, part) in build_b(per_lang).items():
                m_lg = frame["lang"] == lg
                frame.loc[m_lg, "B"] = B
                frame.loc[m_lg, "T"] = T
                frame.loc[m_lg, "partition"] = "|".join("".join(str(i + 1) for i in b) for b in part)
        else:
            # Only the averaged reading at T = 1 was stored for this model.
            frame["B"] = np.mean([wide[p].loc[idx, "score"].values for p in prompts], axis=0)
            frame["T"], frame["partition"] = 1.0, "1|2|3|4|5"
        out[m] = frame
    return out


# ----------------------------------------------------------------------------- fusion
def moments(a, b, y):
    """The six moments from which r(w*a + (1-w)*b, y) follows in closed form for any w."""
    a, b, y = a - a.mean(), b - b.mean(), y - y.mean()
    k = 1.0 / len(y)
    return (float(a @ y) * k, float(b @ y) * k, float(a @ a) * k, float(b @ b) * k,
            float(a @ b) * k, float(np.sqrt(float(y @ y) * k)))


def r_mom(M, w):
    cay, cby, va, vb, cab, sy = M
    den = w * w * va + (1 - w) * (1 - w) * vb + 2 * w * (1 - w) * cab
    return (w * cay + (1 - w) * cby) / (np.sqrt(den) * sy) if den > 0 and sy > 0 else np.nan


def pick_model(r_b, exclude, pool):
    best, best_m = None, -np.inf
    for m, per in r_b.items():
        vals = [r for l, r in per.items() if l not in exclude and np.isfinite(r)]
        if m in pool and vals and np.mean(vals) > best_m:
            best, best_m = m, float(np.mean(vals))
    return best


def signals(ev, A, Bs, r_b, exclude):
    """{lang: frame with y, ctx, p_en, p_multi, zB, model}; the model for each language is chosen
    without that language and without those in `exclude`."""
    out = {}
    for lg, ga in A.groupby("lang", sort=True):
        pool = {m for m, f in Bs.items() if (f["lang"] == lg).any()}
        m = pick_model(r_b, set(exclude) | {lg}, pool)
        if m is None:
            continue
        d = ga.merge(Bs[m][["idx", "B"]], on="idx", how="inner").merge(
            ev[["idx", "complexity", "context_id"]], on="idx")
        d["zB"] = data.zscore(d["B"].values)
        d["model"] = m
        out[lg] = d
    return out


def fit(fit_langs):
    """(w_src, w) for a held-out language, from the signals of its fitting languages."""
    best, crit_best = None, -np.inf
    for s in SRC_GRID:
        M = {l: moments(z_a(d, s), d["zB"].values, d["complexity"].values)
             for l, d in fit_langs.items()}
        vals = []
        for l2 in M:
            inner = [np.mean([r_mom(M[l3], w) for l3 in M if l3 != l2]) for w in W_GRID]
            vals.append(r_mom(M[l2], float(W_GRID[int(np.argmax(inner))])))
        if np.mean(vals) > crit_best:
            best, crit_best = (float(s), M), float(np.mean(vals))
    s, M = best
    curve = [np.mean([r_mom(M[l], w) for l in M]) for w in W_GRID]
    return s, float(W_GRID[int(np.argmax(curve))])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--with-ro", action="store_true", help="add RoLCP as an 11th language")
    ap.add_argument("--encoders", nargs="+", default=["xlmr", "labse", "e5"])
    ap.add_argument("--models", nargs="+", default=None,
                    help="candidate language models (default: every model in signal_b.csv)")
    ap.add_argument("--boot", type=int, default=2000, help="bootstrap resamples of contexts")
    ap.add_argument("--out", default=None, help="optional CSV for the per-item predictions")
    a = ap.parse_args()
    if a.boot < 1:
        ap.error("--boot must be at least 1")

    ev = data.load_eval(a.with_ro)
    A = load_a("mlsp+ro" if a.with_ro else "mlsp", a.encoders)
    Bs = load_b(ev, a.models)
    y = ev.set_index("idx")["complexity"]
    r_b = {m: {lg: data.pearson(g["B"].values, y.loc[g["idx"]].values)
               for lg, g in f.groupby("lang")} for m, f in Bs.items()}
    test = signals(ev, A, Bs, r_b, exclude=())
    skipped = sorted(set(A["lang"]) - set(test))
    if skipped:
        print(f"no language model covers {skipped}; these languages are left out")

    rows, preds, boots = [], [], []
    for lg, d in test.items():
        fit_langs = {l: f for l, f in signals(ev, A, Bs, r_b, exclude={lg}).items() if l != lg}
        if len(fit_langs) < 2:
            raise SystemExit(f"{lg}: the fusion weights need signal B for at least two other "
                             "languages")
        w_src, w = fit(fit_langs)
        zA = z_a(d, w_src)
        P = w * zA + (1 - w) * d["zB"].values
        y_l = d["complexity"].values
        r_f, s = data.boot_r(y_l, P, d["context_id"].values, a.boot)
        boots.append(s)
        lo, hi = np.percentile(s, [2.5, 97.5])
        b = Bs[d["model"].iloc[0]]
        b = b[b["lang"] == lg].iloc[0]
        rows.append(dict(lang=lg, n=len(d), model=d["model"].iloc[0], T=b["T"],
                         partition=b["partition"], w_src=w_src, w=w, r_A=data.pearson(zA, y_l),
                         r_B=data.pearson(d["zB"].values, y_l), r_fused=r_f, lo=lo, hi=hi))
        preds.append(pd.DataFrame({"lang": lg, "idx": d["idx"], "A": zA, "B": d["zB"],
                                   "fused": P}))

    t = pd.DataFrame(rows)
    # Resample k of every language is averaged, which gives the interval of the mean over languages.
    m = min(len(s) for s in boots)
    mean_boot = np.vstack([s[:m] for s in boots]).mean(axis=0)
    lo, hi = np.percentile(mean_boot, [2.5, 97.5])
    pd.set_option("display.width", 200)
    print(t.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\nmean over {len(t)} languages: A {t['r_A'].mean():.6f} | B {t['r_B'].mean():.6f} | "
          f"fused {t['r_fused'].mean():.6f}  95% CI [{lo:.4f}, {hi:.4f}]")
    if a.out:
        pd.concat(preds, ignore_index=True).to_csv(a.out, index=False)
        print(f"-> {a.out}")


if __name__ == "__main__":
    main()
