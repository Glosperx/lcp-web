"""Stage 3: signal B of the whole test set (RoLCP included) through llama.cpp, in the site's mode.

Steps (--steps, in this order; each stops with exit 1 on a failed gate):
  lengths    all 21,633 prompts (7,211 rows x 3 prompts: signal_b.render, then apply_chat_template
             as lcp/rater.py) tokenised without the model; max and p99 per language. Gate: every
             prompt has at most n_ctx - --margin tokens.
  run        the readings, with the site's configuration (--gpu-layers 49 --flash-attn --n-ctx 1024
             --n-batch 256) and KV reuse, in the order of bench_cpu.analyze: the test rows grouped
             by context (contexts and their rows in idx order), then for each context prompt by
             prompt, word by word. The KV prefix is kept across contexts, as across the sentences
             of one text; it starts empty at the first reading and after a resume. Resumes from
             reference/signal_b_llamacpp.part.csv (complete contexts are kept, a partial one is
             read again). Output reference/signal_b_llamacpp.csv in the format of signal_b.csv
             (model gemma4-12b-qat-gguf, no text) and reference/b_reference_readings.csv (tokens,
             seconds and digit mass per reading).
  gates      digit mass >= 0.5 and no NaN on every reading; r between the mean of the 3 prompts
             (score, T = 1) and the stored MLX readings (gemma4-12b-4bit) >= 0.90 in every language
             and >= 0.95 pooled; per prompt figures reported.
  fuse       a writable folder with the release's signal_a.csv and a signal_b.csv holding only
             gemma4-12b-qat-gguf; `fuse.py --with-ro --out` there (T, partition, w_src and w chosen
             again, LOLO). r per language, mean and CI next to 0.692521, parameters next to the
             paper's. Gate: mean >= 0.6825 (paper - 0.01) before any artifact is written.
  artifacts  artifacts/params.json updated from that run: LOLO parameters, B's mean, deviation, T
             and partition per language, the display scale, r per language. Check: lcp/fusion.py
             on the test rows, from the artifacts, reproduces the fusion of `fuse`.

  docker/run_cuda.sh python scripts/b_reference.py --steps lengths
  docker/run_cuda.sh python scripts/b_reference.py --steps run gates fuse artifacts
No dataset text is written or printed.
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import data                                    # noqa: E402  (lcp_model on PYTHONPATH)
import signal_b                                # noqa: E402
import export_model as X                       # noqa: E402
from lcp import fusion as F                    # noqa: E402
from lcp import rater as R                     # noqa: E402
from lcp.paper import use_release              # noqa: E402

KEY = "gemma4-12b-qat-gguf"
PROMPTS = list(signal_b.PROMPTS)               # the order of bench_cpu.analyze
EXTRA = ["raw", "n_tokens", "n_evaluated", "seconds", "ctx"]
GATE_MASS, GATE_R_LANG, GATE_R_POOLED = 0.5, 0.90, 0.95
MEAN_MIN = round(X.PAPER_MEAN - 0.01, 4)        # 0.6825
LOG = []


def say(msg=""):
    print(msg, flush=True)
    LOG.append(msg)


def stop(msg):
    say(f"\n[STOP] {msg}")
    flush_log()
    raise SystemExit(1)


def flush_log():
    if A.log:
        with open(A.log, "a", encoding="utf-8") as fh:
            fh.write("\n".join(LOG) + "\n")
        LOG.clear()


def gpu_mem():
    """(used MiB, total MiB) of the whole GPU (WSL2 has no per-process figure), or None."""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                              "--format=csv,noheader,nounits"], capture_output=True, text=True,
                             timeout=20)
        return tuple(int(x) for x in out.stdout.strip().splitlines()[0].split(","))
    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
        return None


def plan(ev):
    """Contexts in order of their first idx, each with its rows in idx order."""
    ev = ev.sort_values("idx")
    order = list(dict.fromkeys(ev["context_id"]))
    groups = {c: g for c, g in ev.groupby("context_id", sort=False)}
    return [(k, groups[c]) for k, c in enumerate(order)]


# ----------------------------------------------------------------------------- steps
def step_lengths(ev):
    tok = R.load_tokenizer()
    kw = R.chat_kwargs(tok)
    n = []
    t0 = time.time()
    for r in ev.itertuples():
        for pr in PROMPTS:
            ids = tok.apply_chat_template(
                [{"role": "user", "content": signal_b.render(pr, r.lang, r.sent, r.token)}],
                add_generation_prompt=True, tokenize=True, return_dict=False, **kw)
            n.append((r.lang, pr, len(ids)))
    d = pd.DataFrame(n, columns=["lang", "prompt", "tokens"])
    limit = A.n_ctx - A.margin
    say(f"[lengths] {len(d)} prompts tokenised in {time.time() - t0:.0f}s; limit n_ctx {A.n_ctx} "
        f"- margin {A.margin} = {limit} tokens")
    for lg, g in d.groupby("lang"):
        say(f"  {lg:4s} n {len(g):5d}  median {g['tokens'].median():5.0f}  "
            f"p99 {np.percentile(g['tokens'], 99):6.1f}  max {g['tokens'].max():5d}  "
            f"(max per prompt: " + ", ".join(f"{p} {g[g['prompt'] == p]['tokens'].max()}"
                                            for p in PROMPTS) + ")")
    say(f"  all  n {len(d):5d}  median {d['tokens'].median():5.0f}  "
        f"p99 {np.percentile(d['tokens'], 99):6.1f}  max {d['tokens'].max():5d}")
    over = d[d["tokens"] > limit]
    if len(over):
        stop(f"{len(over)} prompts exceed {limit} tokens: "
             + ", ".join(f"{lg} {k}" for lg, k in over["lang"].value_counts().items()))
    say(f"[lengths] PASS: longest prompt {d['tokens'].max()} tokens <= {limit}")


def step_run(ev):
    part = A.out.replace(".csv", ".part.csv")
    cols = signal_b.COLS + EXTRA
    contexts = plan(ev)
    need = {k: 3 * len(g) for k, g in contexts}
    done_ctx = set()
    if os.path.exists(part):
        d = pd.read_csv(part, float_precision="round_trip")
        cnt = d.groupby("ctx").size()
        done_ctx = {int(k) for k, v in cnt.items() if v == need[int(k)]}
        keep = d[d["ctx"].isin(done_ctx)]
        if len(keep) != len(d):
            say(f"[run] dropping {len(d) - len(keep)} readings of an incomplete context")
        keep.to_csv(part, index=False)       # every float written by repr, so this round-trips
    todo = [(k, g) for k, g in contexts if k not in done_ctx]
    n_todo = sum(need[k] for k, _ in todo)
    n_all = sum(need.values())
    say(f"[run] {len(contexts)} contexts, {n_all} readings; done {n_all - n_todo}, to do {n_todo}")
    if not todo:
        return
    vram0 = gpu_mem()
    rt = R.LlamaRater(n_threads=A.threads, n_ctx=A.n_ctx, n_batch=A.n_batch,
                      n_gpu_layers=A.gpu_layers, flash_attn=A.flash_attn)
    rt.reuse = True
    rt._prev = []
    vram1 = gpu_mem()
    say(f"[run] Gemma GGUF loaded in {rt.load_seconds:.1f}s, gpu layers {A.gpu_layers}, flash attn "
        f"{A.flash_attn}, n_ctx {A.n_ctx}, n_batch {A.n_batch}, threads {rt.llm.n_threads}; "
        f"VRAM (whole GPU) {vram0} -> {vram1} MiB")
    flush_log()
    header = not os.path.exists(part)
    t0 = time.time()
    i = 0
    win = []                      # (seconds, evaluated tokens) of the last readings
    tot_s = tot_ev = tot_tok = 0.0
    vram_max = vram1[0] if vram1 else None
    with open(part, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if header:
            w.writerow(cols)
        for k, g in todo:
            for pr in PROMPTS:
                for r in g.itertuples():
                    tb = time.perf_counter()
                    p, raw = rt.read(pr, r.lang, r.sent, r.token)
                    dt = time.perf_counter() - tb
                    n_tok, n_ev = rt.last
                    if not (raw >= GATE_MASS and np.isfinite(p).all()):
                        stop(f"digit mass: {pr} {r.lang} idx {r.idx}: {raw!r} on the digits")
                    w.writerow([KEY, pr, r.lang, r.idx] + [repr(float(x)) for x in p]
                               + [repr(R.score(p)), repr(float(raw)), n_tok, n_ev, repr(dt), k])
                    i += 1
                    tot_s += dt
                    tot_ev += n_ev
                    tot_tok += n_tok
                    win.append((dt, n_ev))
                    if i % A.status == 0 or i == n_todo:
                        fh.flush()
                        vr = gpu_mem()
                        if vr and vram_max is not None:
                            vram_max = max(vram_max, vr[0])
                        ws = sum(x for x, _ in win)
                        el = time.time() - t0
                        say(f"[run] {i}/{n_todo} ({100 * i / n_todo:.1f}%) {r.lang}  last "
                            f"{len(win)}: {ws / len(win):.3f}s/reading, "
                            f"{sum(e for _, e in win) / ws:.0f} tok/s | all: "
                            f"{tot_s / i:.3f}s/reading | elapsed {el / 60:.1f} min, ETA "
                            f"{el / i * (n_todo - i) / 60:.1f} min | VRAM {vr} MiB")
                        flush_log()
                        win = []
            fh.flush()
    say(f"[run] done: {i} readings in {(time.time() - t0) / 60:.1f} min, "
        f"{tot_s / i:.4f}s per reading, {tot_tok / i:.0f} prompt tokens and {tot_ev / i:.0f} "
        f"evaluated per reading, {tot_ev / tot_s:.0f} tok/s; partial KV removals refused "
        f"{rt.refused}; VRAM max (whole GPU) {vram_max} MiB")
    finish(part)


def finish(part):
    d = pd.read_csv(part, float_precision="round_trip")
    if d.duplicated(["prompt", "idx"]).any():
        stop("duplicate readings in the .part file")
    d.sort_values(["model", "prompt", "idx"], kind="stable")[signal_b.COLS].to_csv(
        A.out, index=False, float_format=None)
    d[["prompt", "lang", "idx"] + EXTRA].to_csv(A.readings, index=False)
    say(f"-> {A.out} ({len(d)} readings), {A.readings}")


def step_gates(ev):
    if not os.path.exists(A.out):
        part = A.out.replace(".csv", ".part.csv")
        if os.path.exists(part):
            finish(part)
        else:
            stop(f"{A.out} not found: run the readings first")
    new = pd.read_csv(A.out, float_precision="round_trip")
    rd = pd.read_csv(A.readings)
    if len(new) != 3 * len(ev) or set(new["idx"]) != set(ev["idx"]):
        stop(f"{len(new)} readings, expected {3 * len(ev)}")
    p = new[[f"p{k}" for k in signal_b.DIGITS]].values
    if not (np.isfinite(p).all() and np.isfinite(new["score"]).all()):
        stop("NaN in the readings")
    if not (rd["raw"] >= GATE_MASS).all():
        stop(f"digit mass below {GATE_MASS}: {(rd['raw'] < GATE_MASS).sum()} readings")
    say(f"[gates] digit mass: min {rd['raw'].min():.4f}, median {rd['raw'].median():.4f}, no NaN")
    say(f"[gates] time: {rd['seconds'].mean():.4f}s per reading (median {rd['seconds'].median():.4f},"
        f" p95 {rd['seconds'].quantile(0.95):.4f}), {rd['n_tokens'].mean():.0f} prompt tokens, "
        f"{rd['n_evaluated'].mean():.0f} evaluated ({100 * rd['n_evaluated'].sum() / rd['n_tokens'].sum():.0f}%), "
        f"{rd['n_evaluated'].sum() / rd['seconds'].sum():.0f} tok/s, {rd['seconds'].sum() / 60:.1f} "
        "min of readings")
    for lg, g in rd.groupby("lang"):
        say(f"  {lg:4s} {g['seconds'].mean():.4f}s/reading, {g['n_tokens'].mean():.0f} tokens, "
            f"{g['n_evaluated'].mean():.0f} evaluated")
    st = pd.read_csv(os.path.join(A.paper_release, "predictions", "signal_b.csv"),
                     float_precision="round_trip")
    st = st[(st["model"] == R.KEY) & st["prompt"].isin(PROMPTS)]
    lang = ev.set_index("idx")["lang"]
    m_new = new.groupby("idx")["score"].mean()
    m_old = st.groupby("idx")["score"].mean()
    j = pd.DataFrame({"new": m_new, "old": m_old}).dropna()
    j["lang"] = lang.loc[j.index].values
    if len(j) != len(ev):
        stop(f"stored MLX readings found for {len(j)}/{len(ev)} rows")
    per = {lg: data.pearson(g["new"], g["old"]) for lg, g in j.groupby("lang")}
    pooled = data.pearson(j["new"], j["old"])
    say("[gates] r(mean of 3 prompts, stored MLX) per language: "
        + "  ".join(f"{lg} {v:.4f}" for lg, v in per.items()))
    say(f"[gates] pooled r {pooled:.4f}, mean |score diff| {np.abs(j['new'] - j['old']).mean():.4f}")
    for pr in PROMPTS:
        a_ = new[new["prompt"] == pr].set_index("idx")["score"]
        b_ = st[st["prompt"] == pr].set_index("idx")["score"].loc[a_.index]
        pl = {lg: data.pearson(a_[lang.loc[a_.index].values == lg],
                               b_[lang.loc[a_.index].values == lg]) for lg in sorted(per)}
        say(f"[gates] prompt {pr:6s}: pooled r {data.pearson(a_, b_):.4f}; per language "
            + "  ".join(f"{lg} {v:.3f}" for lg, v in pl.items()))
    bad = {lg: v for lg, v in per.items() if not v >= GATE_R_LANG}
    if bad:
        stop(f"r below {GATE_R_LANG} in " + ", ".join(f"{lg} {v:.4f}" for lg, v in bad.items()))
    if not pooled >= GATE_R_POOLED:
        stop(f"pooled r {pooled:.4f} below {GATE_R_POOLED}")
    say("[gates] PASS")


def work_dir():
    d = os.path.abspath(A.work)
    os.makedirs(d, exist_ok=True)
    shutil.copyfile(A.signal_a, os.path.join(d, "signal_a.csv"))
    b = pd.read_csv(A.out, float_precision="round_trip")
    if set(b["model"]) != {KEY}:
        stop(f"{A.out} holds models {set(b['model'])}")
    shutil.copyfile(A.out, os.path.join(d, "signal_b.csv"))
    return d


def step_fuse(ev):
    d = work_dir()
    out_csv = os.path.join(d, "fused_llamacpp.csv")
    txt = X.run_fuse(d, out_csv, A.paper_release)
    say("`fuse.py --with-ro --out` with B from llama.cpp (only gemma4-12b-qat-gguf):")
    say(txt.rstrip().split("\n-> ")[0])
    data.PRED_DIR = d
    res, ci = X.lolo(ev, None, A.boot)
    mean = float(np.mean([r["r_fused"] for r in res.values()]))
    with open(os.path.join(A.artifacts, "params.json"), encoding="utf-8") as fh:
        old = json.load(fh)
    old = old.get("paper_stage2", old)          # the paper's parameters (stage 2)
    say(f"\n[fuse] mean over {len(res)} languages {mean:.6f}, 95% CI [{ci[0]:.4f}, {ci[1]:.4f}];"
        f" paper {X.PAPER_MEAN} (CI [0.6789, 0.7057]); difference {mean - X.PAPER_MEAN:+.6f}")
    for lg, r in res.items():
        o = old["lang"][lg]
        say(f"  {lg:4s} r {r['r_fused']:.4f} (paper {o['r']['fused']:.4f}, {r['r_fused'] - o['r']['fused']:+.4f})"
            f"  r_B {r['r_B']:.4f} (paper {o['r']['B']:.4f})  T {r['T']:g} (paper {o['b']['T']:g})"
            f"  {r['partition']} (paper {o['b']['partition']})  w_src {r['w_src']:g} "
            f"(paper {o['w_src']:g})  w {r['w']:g} (paper {o['w']:g})")
    if not mean >= MEAN_MIN:
        stop(f"mean fused r {mean:.6f} below {MEAN_MIN}: discuss before writing the artifacts")
    say(f"[fuse] PASS: mean {mean:.6f} >= {MEAN_MIN}")
    return res, ci


def step_artifacts(ev, res, ci):
    d = os.path.abspath(A.work)
    data.PRED_DIR = d
    path = os.path.join(A.artifacts, "params.json")
    with open(path, encoding="utf-8") as fh:
        params = json.load(fh)
    za = X.a_constants()
    if za != params["signal_a"]["z"]:
        stop("the z-score constants of A from the copied signal_a.csv differ from the exported ones")
    order, bmat = X.b_matrices(KEY)
    if "paper_stage2" not in params:          # kept from the first run of this step
        params["paper_stage2"] = {"b": params["b"], "mean_r": params["mean_r"],
                                  "lang": {lg: {k: p[k] for k in ("w_src", "w", "b", "r")}
                                           for lg, p in params["lang"].items()}}
    params["created"] = time.strftime("%Y-%m-%d %H:%M:%S")
    params["description"] = ("lcp-web stages 2-3: signal A models, centring, z-score constants, "
                             "LOLO fusion parameters with B from llama.cpp, display scale. "
                             "Numbers only, no dataset text.")
    params["b"] = {"source": "llama.cpp GPU, site configuration, KV reuse "
                             "(reference/signal_b_llamacpp.csv)",
                   "model": KEY, "prompts": order,
                   "runtime": {"gguf": list(R.GGUF), "n_gpu_layers": A.gpu_layers,
                               "flash_attn": A.flash_attn, "n_ctx": A.n_ctx, "n_batch": A.n_batch,
                               "kv_reuse": True}}
    params["lang"] = X.lang_params(res)
    params["mean_r"] = {"A": float(np.mean([r["r_A"] for r in res.values()])),
                        "B": float(np.mean([r["r_B"] for r in res.values()])),
                        "fused": float(np.mean([r["r_fused"] for r in res.values()])),
                        "ci": list(ci)}
    params["scale"] = X.scale(res)
    params["data_sha256"]["reference/signal_b_llamacpp.csv"] = X.sha256(A.out)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(params, fh, indent=1)
    say(f"-> {path}")

    # check: lcp/fusion.py from the artifacts alone reproduces the fusion of step fuse
    _, _, _, lex_ev, _, fert_ev = X.prepare()
    feats = X.test_features(ev, lex_ev, fert_ev)
    fz = F.Fusion(A.artifacts)
    got = X.fusion_rows(fz, res, feats, bmat)
    ref = pd.read_csv(os.path.join(d, "fused_llamacpp.csv"), float_precision="round_trip")
    m = got.merge(ref, on=["lang", "idx"], suffixes=("", "_ref"), how="outer", indicator=True)
    if not (m["_merge"] == "both").all():
        stop("rows of lcp/fusion.py and of fuse.py --out differ")
    dd = {c: float(np.abs(m[c] - m[c + "_ref"]).max()) for c in ("A", "B", "fused")}
    y = ev.set_index("idx")["complexity"]
    r_lang = {lg: data.pearson(g["fused"].values, y.loc[g["idx"]].values)
              for lg, g in got.groupby("lang")}
    say(f"[artifacts] lcp/fusion.py vs fuse.py --out, {len(m)} rows: max |d| "
        + ", ".join(f"{c} {v:.3g}" for c, v in dd.items())
        + f"; mean r {np.mean(list(r_lang.values())):.6f}")
    lv = []
    for lg, g in got.groupby("lang"):
        s = fz.score01(lg, g["fused"].values)
        lvl = fz.level(s)
        lv.append(f"{lg} " + "/".join(str(int((lvl == k).sum())) for k in range(1, 6)))
        if not np.all(np.diff(s[np.argsort(g["fused"].values)]) >= 0):
            stop(f"{lg}: the 0-1 score is not monotone in the fused value")
    say("[artifacts] test rows per level 1/2/3/4/5: " + "  ".join(lv))
    if max(dd.values()) > 1e-9:
        stop("lcp/fusion.py does not reproduce the fusion of fuse.py")
    say("[artifacts] PASS")


def main():
    global A
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--steps", nargs="+", default=["lengths", "run", "gates", "fuse", "artifacts"],
                    choices=["lengths", "run", "gates", "fuse", "artifacts"])
    ap.add_argument("--paper-release", default="/paper/release")
    ap.add_argument("--out", default="reference/signal_b_llamacpp.csv")
    ap.add_argument("--readings", default="reference/b_reference_readings.csv")
    ap.add_argument("--log", default="reference/b_reference.log")
    ap.add_argument("--artifacts", default="artifacts")
    ap.add_argument("--work", default="reference/_work/fuse_llamacpp")
    ap.add_argument("--signal-a", default=None,
                    help="signal_a.csv for the fusion (default: the release's)")
    ap.add_argument("--gpu-layers", type=int, default=49)
    ap.add_argument("--flash-attn", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--n-ctx", type=int, default=1024)
    ap.add_argument("--n-batch", type=int, default=256)
    ap.add_argument("--threads", type=int, default=None)
    ap.add_argument("--margin", type=int, default=16, help="tokens kept free below n_ctx")
    ap.add_argument("--status", type=int, default=250, help="readings between status lines")
    ap.add_argument("--boot", type=int, default=2000)
    A = ap.parse_args()
    A.paper_release = use_release(A.paper_release)
    A.signal_a = A.signal_a or os.path.join(A.paper_release, "predictions", "signal_a.csv")
    os.makedirs(os.path.dirname(A.out) or ".", exist_ok=True)
    say(f"=== b_reference {' '.join(A.steps)} | {time.strftime('%Y-%m-%d %H:%M:%S')}")
    ev = data.load_eval(True)
    res = ci = None
    for s in A.steps:
        if s == "lengths":
            step_lengths(ev)
        elif s == "run":
            step_run(ev)
        elif s == "gates":
            step_gates(ev)
        elif s == "fuse":
            res, ci = step_fuse(ev)
        elif s == "artifacts":
            if res is None:
                res, ci = step_fuse(ev)
            step_artifacts(ev, res, ci)
        flush_log()


A = None

if __name__ == "__main__":
    main()
