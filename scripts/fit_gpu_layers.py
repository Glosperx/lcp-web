"""How many of Gemma's layers fit on the GPU: n_gpu_layers from the top down.

Each value is tried in a fresh process, so all CUDA memory goes back between tries and a failed
allocation cannot leave a broken context behind. The child loads LlamaRater with that many layers,
warms up on three readings, then reads the three prompts on the first content words of a fixed
sentence (bench/texts/en_1.txt, KV reuse on, as on the site) and reports: whether it loaded, the
buffers llama.cpp allocated (from its log), the VRAM used on the whole GPU (nvidia-smi; under WSL2
there is no per-process figure, so the Windows desktop is included) before loading, after loading
and after the readings, and the seconds per reading.

On Windows the driver can page VRAM out to system memory instead of failing (NVIDIA control
panel, "CUDA - Sysmem Fallback Policy"). A value can then load and just be slow, so the value to
use is the fastest one, not the largest one that loads.

Gemma 4 12B has 48 layers; n_gpu_layers 49 also puts the output layer on the GPU.

  docker/run_cuda.sh python scripts/fit_gpu_layers.py --n-ctx 2048
  docker/run_cuda.sh python scripts/fit_gpu_layers.py --n-ctx 2048 --flash-attn
Writes bench/results/fit_gpu_layers[_fa].csv and prints one line per try.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import signal_b                                # noqa: E402  (lcp_model on PYTHONPATH)
from lcp import segment as S                   # noqa: E402
from bench_cpu import gpu_mem                  # noqa: E402  (scripts/ is sys.path[0])

PROMPTS = list(signal_b.PROMPTS)
TAG = "FIT_RESULT "
BUF = re.compile(r"(\S+) (model|KV|compute) buffer size =\s*([\d.]+) MiB")
OFF = re.compile(r"offloaded (\d+)/(\d+) layers")


def one(a, n):
    """Child: load with n layers on the GPU, time the readings, print one JSON line."""
    from lcp.rater import LlamaRater
    with open(os.path.join(a.texts, "en_1.txt"), encoding="utf-8") as fh:
        sent = S._regex("en", fh.read().strip())[0]
    words = [w.text for w in sent.content_words if len(w.text) >= 4][:a.words]
    out = {"n_gpu_layers": n, "flash_attn": a.flash_attn, "n_ctx": a.n_ctx, "words": len(words)}
    out["vram_before_mib"] = gpu_mem()
    rt = LlamaRater(n_threads=a.threads, n_ctx=a.n_ctx, n_batch=a.n_batch, n_gpu_layers=n,
                    flash_attn=a.flash_attn, verbose=True)
    out["load_s"] = rt.load_seconds
    out["threads"] = rt.llm.n_threads
    out["vram_loaded_mib"] = gpu_mem()
    rt.reuse = False
    t0 = time.perf_counter()
    for pr in PROMPTS:
        rt.read(pr, "en", "The cat sat on the mat.", "cat")
    out["warmup_s"] = time.perf_counter() - t0
    rt.reuse, rt._prev = True, []
    n_eval = n_read = 0
    masses = []
    t0 = time.perf_counter()
    for pr in PROMPTS:
        for w in words:
            p, raw = rt.read(pr, "en", sent.text, w)
            n_eval += rt.last[1]
            n_read += 1
            masses.append(raw)
    dt = time.perf_counter() - t0
    out |= {"readings": n_read, "evaluated_tokens": n_eval, "seconds": dt,
            "s_per_reading": dt / n_read, "tok_s": n_eval / dt, "min_mass": min(masses),
            "vram_after_mib": gpu_mem(), "refused": rt.refused}
    print(TAG + json.dumps(out), flush=True)


def parse_log(log):
    """{device kind: MiB summed} from llama.cpp's buffer lines, and 'k/n' offloaded layers."""
    bufs = {}
    for dev, kind, mib in BUF.findall(log):
        bufs[f"{dev} {kind}"] = round(bufs.get(f"{dev} {kind}", 0.0) + float(mib), 1)
    m = OFF.findall(log)
    return bufs, (f"{m[-1][0]}/{m[-1][1]}" if m else None)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--layers", nargs="+", type=int,
                    default=[49, 48, 46, 44, 42, 40, 38, 36, 32, 24],
                    help="values of n_gpu_layers to try, in this order")
    ap.add_argument("--n-ctx", type=int, default=2048)
    ap.add_argument("--n-batch", type=int, default=512)
    ap.add_argument("--suffix", default="", help="appended to the output file name")
    ap.add_argument("--flash-attn", action="store_true")
    ap.add_argument("--threads", type=int, default=None)
    ap.add_argument("--words", type=int, default=8, help="content words read per prompt")
    ap.add_argument("--texts", default="bench/texts")
    ap.add_argument("--out", default="bench/results")
    ap.add_argument("--timeout", type=int, default=900, help="seconds per try")
    ap.add_argument("--one", type=int, default=None, help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.one is not None:
        return one(a, a.one)

    import pandas as pd
    rows = []
    path = os.path.join(a.out, "fit_gpu_layers" + ("_fa" if a.flash_attn else "") + a.suffix
                        + ".csv")
    for n in a.layers:
        cmd = [sys.executable, os.path.abspath(__file__), "--one", str(n), "--n-ctx", str(a.n_ctx),
               "--n-batch", str(a.n_batch), "--words", str(a.words), "--texts", a.texts]
        cmd += ["--flash-attn"] if a.flash_attn else []
        cmd += ["--threads", str(a.threads)] if a.threads else []
        t0 = time.perf_counter()
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=a.timeout)
            log, code = p.stdout + p.stderr, p.returncode
        except subprocess.TimeoutExpired as e:
            log = (e.stdout or b"").decode(errors="replace") + (e.stderr or b"").decode(errors="replace")
            code = "timeout"
        bufs, offloaded = parse_log(log)
        res = [json.loads(ln[len(TAG):]) for ln in log.splitlines() if ln.startswith(TAG)]
        row = {"n_gpu_layers": n, "flash_attn": a.flash_attn, "n_ctx": a.n_ctx,
               "n_batch": a.n_batch,
               "ok": bool(res), "exit": code, "wall_s": round(time.perf_counter() - t0, 1),
               "offloaded": offloaded}
        if res:
            r = res[0]
            row |= {k: r[k] for k in ("load_s", "warmup_s", "readings", "s_per_reading", "tok_s",
                                      "min_mass", "refused", "threads")}
            for k in ("vram_before_mib", "vram_loaded_mib", "vram_after_mib"):
                row[k] = r[k][0] if r[k] else None
        else:
            err = [ln for ln in log.splitlines()
                   if re.search(r"out of memory|failed|error|Error", ln)]
            row["error"] = (err[-1] if err else log.strip().splitlines()[-1:] or [""])[0][:300]
        row |= {f"buf {k}": v for k, v in bufs.items()}
        rows.append(row)
        pd.DataFrame(rows).to_csv(path, index=False)
        if res:
            print(f"[fit] n_gpu_layers {n:2d} ({offloaded}): load {row['load_s']:.1f}s, "
                  f"{row['s_per_reading']:.3f} s/reading, {row['tok_s']:.0f} tok/s, "
                  f"VRAM {row['vram_before_mib']} -> {row['vram_loaded_mib']} -> "
                  f"{row['vram_after_mib']} MiB, min mass {row['min_mass']:.4f}, buffers {bufs}",
                  flush=True)
        else:
            print(f"[fit] n_gpu_layers {n:2d}: FAILED ({code}) {row['error']}, buffers {bufs}",
                  flush=True)
    ok = [r for r in rows if r["ok"]]
    if ok:
        best = min(ok, key=lambda r: r["s_per_reading"])
        print(f"[fit] fastest: n_gpu_layers {best['n_gpu_layers']}, "
              f"{best['s_per_reading']:.3f} s/reading; largest that loads: "
              f"{max(r['n_gpu_layers'] for r in ok)}")
    print(f"-> {path}")


if __name__ == "__main__":
    main()
