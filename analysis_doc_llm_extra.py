"""Llama 3.1 8B and Aya Expanse 8B as signal B on the test data, for Table 3 of the documentation.

The two models were tried only on the trial split (output/e_bakeoff.md). Their ratings on the 7,211
test instances (10 MLSP languages + RoLCP, three prompts) were run with release/signal_b.py in a copy
of release/ outside the repo (~/lcp-llm-extra/release, MLX, pinned revisions) and the rows of the two
models were copied into output/doc_llm_extra_signal_b.csv, in the format of predictions/signal_b.csv.
This script reads them from there; no language model is run here. release/ is imported, never modified.

For each new model, with the model as the only candidate for signal B:
  - Table 3 reading, the same as for Qwen: prompts expert and short, T = 1, no grouping (the five
    ratings kept apart). Per-language r of B, the fusion with signal A (w_src and w chosen on the
    other languages, as in fuse.py), and the paired interval against the full method (0.692521) and
    against Gemma 4 read the same way.
  - full reading: three prompts, T and the grouping chosen on the other languages, as for Gemma 4
    (the same as `fuse.py --with-ro --models <key>` in the copy).
Also: the correlation of B between models (Table 3 reading), a check that the probability mass is not
degenerate, and the control that with all five models in the pool the full method does not move.

Usage (envs ml_def):  python analysis_doc_llm_extra.py > output/doc_llm_extra.txt
"""
import argparse
import contextlib
import os
import re
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import analysis_doc_ablations_extra as aex  # noqa: E402  (chdir to release/, imports data and fuse)
import analysis_doc_correlations as adc  # noqa: E402

data, fuse = aex.data, aex.fuse
GEMMA, QWEN3, QWEN35 = "gemma4-12b-4bit", "qwen3-8b-4bit", "qwen35-9b-8bit"
NAMES = {"llama31-8b-4bit": "Llama 3.1 8B", "aya-expanse-8b-4bit": "Aya Expanse 8B",
         GEMMA: "Gemma 4 12B", QWEN3: "Qwen3 8B", QWEN35: "Qwen3.5 9B"}
NEUTRAL_PART = [aex.DEFAULT["PARTITIONS"][aex.DEFAULT["NEUTRAL"]]]
# Table 3 reading: prompts expert and short, T = 1, no grouping
READ = dict(prompts=["expert", "short"], T_GRID=(1.0,), PARTITIONS=NEUTRAL_PART, NEUTRAL=0)
LOGS = {"llama31-8b-4bit": "llama.log", "aya-expanse-8b-4bit": "aya.log"}
PROMPTS = ("expert", "short", "marked")
PCOLS = [f"p{k}" for k in "12345"]


@contextlib.contextmanager
def stored_b(b):
    read_csv = pd.read_csv
    pd.read_csv = lambda p, *a, **kw: b.copy() if str(p).endswith("signal_b.csv") else read_csv(p, *a, **kw)
    try:
        yield
    finally:
        pd.read_csv = read_csv


def check_rows(extra, ev, models):
    """Every model must have every row of every prompt, finite and normalised; a partial CSV would turn
    NaN into zero after standardisation and give plausible numbers."""
    n_lang = ev["lang"].value_counts()
    for m in models:
        d = extra[extra["model"] == m]
        assert set(d["prompt"]) == set(PROMPTS), f"{m}: prompts {sorted(set(d['prompt']))}"
        for p in PROMPTS:
            g = d[d["prompt"] == p]
            assert g["idx"].is_unique and len(g) == len(ev), f"{m}/{p}: {len(g)} rows, expected {len(ev)}"
            assert set(g["idx"]) == set(ev["idx"]), f"{m}/{p}: idx differ from the evaluation frame"
            assert np.isfinite(g[PCOLS + ["score"]].values).all(), f"{m}/{p}: non-finite values"
            assert np.allclose(g[PCOLS].sum(axis=1), 1.0, atol=1e-9), f"{m}/{p}: p does not sum to 1"
            assert (g["lang"].value_counts().sort_index() == n_lang.sort_index()).all(), f"{m}/{p}: short language"
        print(f"  {NAMES[m]}: {len(d)} rows, {len(PROMPTS)} prompts x {len(ev)} instances, all finite, p sums to 1")


def degenerate(extra, models):
    """Share of the probability mass and the spread of B by language: a tokenizer that fails on a script
    would show as a constant rating."""
    for m in models:
        d = extra[extra["model"] == m]
        print(f"\n  {NAMES[m]}: per language, mean over the three prompts of: mean p(1..5), share of readings "
              "with max p > 0.99, and the standard deviation of the expected rating B (0 to 1 scale)")
        rows = {}
        for lg, g in d.groupby("lang"):
            P = g[PCOLS].values
            rows[lg] = dict(**{f"mean_p{k + 1}": P[:, k].mean() for k in range(5)},
                            onehot=float((P.max(axis=1) > 0.99).mean()),
                            std_B=float(g["score"].std()), n_prompt_rows=len(g))
        t = pd.DataFrame(rows).T
        t["n_prompt_rows"] = t["n_prompt_rows"].astype(int)
        print(t.to_string(float_format=lambda v: f"{v:.3f}"))


def per_lang_table(o, ref, lab, lab_ref):
    t = pd.DataFrame({f"B {lab}": {l: v["B"][0] for l, v in o.items()},
                      f"B {lab_ref}": {l: ref[l]["B"][0] for l in o},
                      f"fused {lab}": {l: v["F"][0] for l, v in o.items()},
                      f"fused {lab_ref}": {l: ref[l]["F"][0] for l in o}})
    t.loc["mean"] = t.mean()
    print(t.to_string(float_format=lambda v: f"{v:.4f}"))
    langs = [l for l in o]
    for k, name in (("B", "B"), ("F", "fused")):
        win = [l for l in langs if o[l][k][0] > ref[l][k][0] + 1e-9]
        print(f"  {lab} higher than {lab_ref} in {name} on {len(win)}/{len(langs)} languages: {' '.join(win) or 'none'}")


def chosen_and_rb(ev, extra_pool):
    """The language model chosen for every test language with the whole pool, and for every fitting
    language, plus r of B per model and language (fuse.load_b, T and grouping chosen)."""
    with stored_b(extra_pool):
        A = fuse.load_a("mlsp+ro", ["xlmr", "labse", "e5"])
        Bs = fuse.load_b(ev, None)
    y = ev.set_index("idx")["complexity"]
    r_b = {m: {lg: data.pearson(g["B"].values, y.loc[g["idx"]].values) for lg, g in f.groupby("lang")}
           for m, f in Bs.items()}
    test = fuse.signals(ev, A, Bs, r_b, exclude=())
    chosen = {lg: d["model"].iloc[0] for lg, d in test.items()}
    fit_choice = {}
    for lg in test:
        for l2, d in fuse.signals(ev, A, Bs, r_b, exclude={lg}).items():
            fit_choice[(lg, l2)] = d["model"].iloc[0]
    return chosen, fit_choice, r_b


def timing(path):
    if not os.path.exists(path):
        return "log not found"
    hits = re.findall(r"\[B\] (\d+)/(\d+)\s+([\d.]+)s per reading", open(path, errors="ignore").read())
    if not hits:
        return "no timing line in the log"
    i, n, s = hits[-1]
    return f"{s} s per reading over the last run ({i} of {n} readings of that run)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extra", default=os.path.join(ROOT, "output", "doc_llm_extra_signal_b.csv"))
    ap.add_argument("--models", nargs="+", default=["llama31-8b-4bit", "aya-expanse-8b-4bit"])
    ap.add_argument("--log-dir", default=os.path.expanduser("~/lcp-llm-extra"))
    a = ap.parse_args()
    new = a.models
    ev = data.load_eval(True)
    extra = pd.read_csv(a.extra, float_precision="round_trip")
    extra = extra[extra["model"].isin(new)]
    print("Llama 3.1 8B and Aya Expanse 8B as signal B on the test data (11 languages, 7,211 instances).")
    print("Written by analysis_doc_llm_extra.py. Ratings: output/doc_llm_extra_signal_b.csv, rows of "
          "release/predictions/signal_b.csv\nfrom the copy ~/lcp-llm-extra/release, produced with "
          "`python signal_b.py --model <key> --with-ro` (MLX, pinned revisions).\nStored rows of the other "
          "models: release/predictions/signal_b.csv and output/doc_qwen_ro_signal_b.csv.\n")

    print("0. Coverage of the new rows (source: output/doc_llm_extra_signal_b.csv):")
    check_rows(extra, ev, new)
    degenerate(extra, new)
    print("\n  time per reading (source: the run logs of signal_b.py in " + a.log_dir + "):")
    for m in new:
        print(f"  {NAMES[m]}: {timing(os.path.join(a.log_dir, LOGS[m]))}")

    base = aex.run(True)  # the full method on the stored rows, before the new models are added
    print(f"\nfull method, stored rows only (source: aex.run(True), as fuse.py --with-ro): fused "
          f"{aex.mean(base):.6f} | A {aex.mean(base, 'A'):.6f} | B {aex.mean(base, 'B'):.6f}")
    aex.B_ALL = pd.concat([aex.B_ALL, extra], ignore_index=True)
    adc.B_ALL = pd.concat([adc.B_ALL, extra], ignore_index=True)

    print("\n1. Table 3 reading (prompts expert and short, T = 1, no grouping), each model as the only "
          "candidate for signal B.\n   Source: aex.run(True, models=[<key>], prompts=[expert, short], "
          "T_GRID=(1.0,), no grouping), the way the Qwen rows of doc_ablations_extra.txt are made.")
    ref = {GEMMA: aex.run(True, models=[GEMMA], **READ)}
    for m in (QWEN3, QWEN35):
        ref[m] = aex.run(True, models=[m], prompts=None, T_GRID=(1.0,), PARTITIONS=NEUTRAL_PART, NEUTRAL=0)
    print("   Reference rows (must equal Table 3 of the documentation; B / fused):")
    for m, o in ref.items():
        print(f"   {NAMES[m]}: B {aex.mean(o, 'B'):.6f} | fused {aex.mean(o):.6f}   (n = {len(o)} languages)")
    reading = {}
    for m in new:
        o = aex.run(True, models=[m], **READ)
        reading[m] = o
        print(f"\n   {NAMES[m]}: B {aex.mean(o, 'B'):.6f} | A {aex.mean(o, 'A'):.6f} | fused {aex.mean(o):.6f}")
        print(f"     fused vs full method (0.692521): {aex.paired(o, base)}")
        print(f"     fused vs Gemma 4, same reading:  {aex.paired(o, ref[GEMMA])}")
        print(f"     B vs Gemma 4, same reading:      {aex.paired(o, ref[GEMMA], 'B', 'B')}")
        per_lang_table(o, ref[GEMMA], NAMES[m], "Gemma 4")

    print("\n2. Full reading (three prompts, T and the grouping chosen on the other languages), each model as "
          "the only candidate.\n   Source: aex.run(True, models=[<key>]); same as `fuse.py --with-ro --models "
          "<key>` in the copy (output/doc_llm_extra_fuse_<key>.txt).")
    full = {}
    for m in new:
        o = aex.run(True, models=[m])
        full[m] = o
        print(f"\n   {NAMES[m]}: B {aex.mean(o, 'B'):.6f} | A {aex.mean(o, 'A'):.6f} | fused {aex.mean(o):.6f}")
        print(f"     fused vs full method (Gemma 4, 0.692521): {aex.paired(o, base)}")
        print(f"     B vs Gemma 4 full reading:                {aex.paired(o, base, 'B', 'B')}")
        per_lang_table(o, base, NAMES[m], "Gemma 4")
        with stored_b(aex.B_ALL):
            Bm = fuse.load_b(ev, [m])[m]
        g = Bm.groupby("lang")[["T", "partition"]].first()
        print("     T and grouping chosen: " + " ".join(f"{l} {r['T']:g} {r['partition']}" for l, r in g.iterrows()))

    print("\n3. Correlation of signal B between models, Table 3 reading, Pearson within each language, "
          "mean over the 11 languages.\n   Source: adc.load_b and adc.corr_table, as part 2 of "
          "output/doc_correlations.txt.")
    ev_idx = adc.load_b(ev, GEMMA, **READ)
    idx, lang = ev_idx.index.values, ev_idx["lang"].values
    cols = {"Gemma 4 (Qwen reading)": ev_idx["B"].values,
            "Qwen3.5 9B": adc.load_b(ev, QWEN35).loc[idx, "B"].values,
            "Qwen3 8B": adc.load_b(ev, QWEN3).loc[idx, "B"].values}
    for m in new:
        cols[NAMES[m]] = adc.load_b(ev, m, **READ).loc[idx, "B"].values
    print(adc.corr_table(cols, lang).to_string(float_format=lambda v: f"{v:.3f}"))
    for m in new:
        print(f"\n   {NAMES[m]}, per language:")
        print(pd.DataFrame({f"with {k}": {l: np.corrcoef(cols[NAMES[m]][lang == l], cols[k][lang == l])[0, 1]
                                          for l in sorted(set(lang))}
                            for k in ("Gemma 4 (Qwen reading)", "Qwen3.5 9B")})
              .to_string(float_format=lambda v: f"{v:.4f}"))

    print("\n4. Control: all five models in the pool (Gemma 4 and the three prompts of the new models in full "
          "reading, Qwen as stored).\n   The full method must not move: Gemma 4 chosen for every test "
          "language and every fitting language, mean 0.692521.\n   Source: fuse.signals / fuse.pick_model on "
          "the five-model pool; aex.run(True) on the same pool.")
    chosen, fit_choice, r_b = chosen_and_rb(ev, aex.B_ALL)
    print("   model chosen per test language: " + " ".join(f"{l} {NAMES[m]}" for l, m in sorted(chosen.items())))
    other = sorted({m for m in fit_choice.values() if m != GEMMA})
    print(f"   fitting languages where a model other than Gemma 4 is chosen: "
          f"{sum(m != GEMMA for m in fit_choice.values())} of {len(fit_choice)}"
          + (f" ({', '.join(NAMES[m] for m in other)})" if other else ""))
    o = aex.run(True)
    print(f"   mean fused with the five-model pool: {aex.mean(o):.6f} (stored rows only: {aex.mean(base):.6f}); "
          f"largest per-language |difference| {max(abs(o[l]['F'][0] - base[l]['F'][0]) for l in o):.2e}")
    print("   mean r of B per model, the criterion of pick_model (source: fuse.load_b, full reading for "
          "three-prompt models, stored reading for Qwen):")
    mlsp = [l for l in sorted(next(iter(r_b.values()))) if l != "ro"]
    for m, per in r_b.items():
        print(f"   {NAMES[m]}: mean r_B over the 10 MLSP languages {np.mean([per[l] for l in mlsp if l in per]):.4f}"
              f", over {len(per)} languages {np.mean(list(per.values())):.4f}")
    ok = (set(chosen.values()) == {GEMMA} and not other
          and abs(aex.mean(o) - aex.mean(base)) < 1e-9)
    print(f"   CONTROL {'PASSED' if ok else 'FAILED'}")
    if not ok:
        raise SystemExit("the system moved with the five models in the pool")


if __name__ == "__main__":
    main()
