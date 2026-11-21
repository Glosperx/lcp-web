"""Stage 1 benchmark: how long the expensive part of the system takes on raw text, CPU only.

Per text: stanza (or regex) segmentation, the three encoders of signal A (one forward pass per
sentence) and signal B (3 Gemma readings per content word). The regressors and the fusion take
milliseconds and come in stage 2. Sentences are processed in order, as the site will stream them:
segmentation of the whole text, then for each sentence A and its B readings (prompt by prompt, so
consecutive readings of one sentence can share their KV prefix when --modes includes reuse).

Measured once: loading stanza (per language), the encoders and Gemma, and the peak memory.
Measured per language x size, after --warmup runs, --reps runs of segmentation and A alone (mode
"A-only"); then per B mode, after --b-warmup runs, --b-reps full runs: words, content words,
sentences, B readings, prompt tokens, evaluated tokens, segmentation / A / B / total seconds,
seconds per reading, prefill tokens per second, and the time until the first sentence is done.
By default --b-warmup and --b-reps equal --warmup and --reps. Before the first language, a few
readings and one encoder pass warm the models up (not recorded).

Outputs, in bench/results/:
  cpu_docker_mac.csv           one row per run (warm-up runs flagged)
  cpu_docker_mac_readings.csv  one row per B reading (indices only, no text)
  cpu_docker_mac_load.json     load times, memory peaks, threads, versions
  cpu_docker_mac_summary.txt   median over the timed runs, per language and size

  docker/run_cpu.sh python scripts/bench_cpu.py

On the PC (stage 7): --gpu-layers, --flash-attn, --n-ctx and --no-mmap go to llama.cpp, --skip-a
drops the encoders (x86 CPU reference for B), and the load JSON also records the VRAM used.
  docker/run_cuda.sh python scripts/bench_cpu.py --gpu-layers 40 --n-ctx 2048 --prefix gpu_docker_pc
"""
import argparse
import gc
import json
import os
import platform
import resource
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import signal_b                                # noqa: E402  (lcp_model on PYTHONPATH)
from lcp import segment as S                   # noqa: E402

PROMPTS = list(signal_b.PROMPTS)
SIZES = (1, 2)


def mem_detail():
    """{rss, anon, file, swap, hwm} of this process in GB, from /proc/self/status. `file` is
    memory-mapped file pages (GGUF, safetensors), which the kernel can drop and reread."""
    out = {}
    keys = {"VmRSS": "rss", "RssAnon": "anon", "RssFile": "file", "VmSwap": "swap", "VmHWM": "hwm"}
    try:
        for ln in open("/proc/self/status"):
            k = ln.split(":")[0]
            if k in keys:
                out[keys[k]] = round(int(ln.split()[1]) / 1e6, 3)
    except OSError:
        pass
    return out


def mem():
    """(peak RSS of this process in GB, cgroup peak in GB or None, cgroup current in GB or None).
    The cgroup figures include the page cache, hence the memory-mapped GGUF."""
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6      # kB on Linux
    out = [rss]
    for f in ("/sys/fs/cgroup/memory.peak", "/sys/fs/cgroup/memory.current"):
        try:
            out.append(int(open(f).read().strip()) / 1e9)
        except (OSError, ValueError):
            out.append(None)
    return tuple(out)


def gpu_mem():
    """(used MiB, total MiB) of the whole GPU from nvidia-smi, or None without a GPU. Under WSL2
    there is no per-process figure, so this includes the Windows desktop."""
    import subprocess
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                              "--format=csv,noheader,nounits"], capture_output=True, text=True,
                             timeout=20)
        used, total = (int(x) for x in out.stdout.strip().splitlines()[0].split(","))
        return used, total
    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
        return None


def analyze(seg, enc, rt, lang, text, reuse, log_readings, run_key):
    """One pass over `text`. reuse=None skips B (segmentation and A only); enc=None skips A."""
    rt.reuse = bool(reuse)
    rt._prev = []
    t0 = time.perf_counter()
    sents = seg.segment(lang, text)
    t_seg = time.perf_counter() - t0
    t_a = t_b = 0.0
    n_read = n_tok = n_eval = 0
    t_first = None
    for si, s in enumerate(sents):
        cw = s.content_words
        if cw:
            if enc is not None:
                ta = time.perf_counter()
                enc.embed(s.text, [(w.start, w.end) for w in cw])
                t_a += time.perf_counter() - ta
            for pr in (PROMPTS if reuse is not None else ()):
                for wi, w in enumerate(cw):
                    tb = time.perf_counter()
                    p, raw = rt.read(pr, lang, s.text, w.text)
                    dt = time.perf_counter() - tb
                    t_b += dt
                    n_read += 1
                    n_tok += rt.last[0]
                    n_eval += rt.last[1]
                    log_readings.append(dict(run_key, sent=si, word=wi, prompt=pr,
                                             **{f"p{d}": float(x) for d, x in
                                                zip(signal_b.DIGITS, p)},
                                             raw=raw, n_tokens=rt.last[0],
                                             n_evaluated=rt.last[1], seconds=dt))
        if t_first is None and cw:
            t_first = time.perf_counter() - t0
    total = time.perf_counter() - t0
    words = sum(1 for s in sents for w in s.words if S._has_letter(w.text))
    content = sum(len(s.content_words) for s in sents)
    return dict(sentences=len(sents), words=words, content_words=content, readings=n_read,
                prompt_tokens=n_tok, evaluated_tokens=n_eval, t_segment=t_seg, t_A=t_a, t_B=t_b,
                total=total, s_per_reading=t_b / n_read if n_read else np.nan,
                prefill_tok_s=n_eval / t_b if t_b else np.nan, t_first_sentence=t_first)


def summary(df, load, path, title):
    t = df[~df["warmup"]].groupby(["lang", "size", "mode"]).median(numeric_only=True)
    lines = [f"{title}: median over the timed runs",
             f"threads: llama.cpp {load['threads_llama']}, torch {load['threads_torch']}; "
             f"peak RSS {load['peak_rss_gb']:.2f} GB, cgroup peak {load['cgroup_peak_gb']} GB",
             "",
             "lang size mode     sent words content reads  prompt_tok  seg_s    A_s      B_s"
             "    total_s  s/read  tok/s  first_s"]
    for (lg, sz, md), r in t.iterrows():
        lines.append(f"{lg:4s} {sz:4d} {md:8s} {r.sentences:4.0f} {r.words:5.0f} "
                     f"{r.content_words:7.0f} {r.readings:5.0f} {r.prompt_tokens:11.0f} "
                     f"{r.t_segment:6.2f} {r.t_A:7.2f} {r.t_B:8.1f} {r.total:9.1f} "
                     f"{r.s_per_reading:7.3f} {r.prefill_tok_s:6.1f} {r.t_first_sentence:7.1f}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--texts", default="bench/texts")
    ap.add_argument("--out", default="bench/results")
    ap.add_argument("--prefix", default="cpu_docker_mac")
    ap.add_argument("--langs", nargs="+", default=list(S.LANGS))
    ap.add_argument("--sizes", nargs="+", type=int, default=list(SIZES))
    ap.add_argument("--modes", nargs="+", choices=["noreuse", "reuse"], default=["noreuse", "reuse"],
                    help="B without / with the KV prefix kept between readings")
    ap.add_argument("--warmup", type=int, default=1)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--noreuse-sizes", nargs="+", type=int, default=None,
                    help="sizes on which the noreuse mode runs (default: all --sizes)")
    ap.add_argument("--b-warmup", type=int, default=None, help="default: --warmup")
    ap.add_argument("--b-reps", type=int, default=None, help="default: --reps")
    ap.add_argument("--threads", type=int, default=None)
    ap.add_argument("--gpu-layers", type=int, default=0,
                    help="Gemma layers offloaded to the GPU (0 = none; 49 = all + output)")
    ap.add_argument("--flash-attn", action="store_true", help="flash attention in llama.cpp")
    ap.add_argument("--n-ctx", type=int, default=4096,
                    help="llama.cpp context (longest prompt in the spike: 675 tokens)")
    ap.add_argument("--n-batch", type=int, default=512,
                    help="llama.cpp n_batch = n_ubatch (the compute buffer grows with it)")
    ap.add_argument("--no-mmap", action="store_true",
                    help="read the GGUF into memory instead of mapping it")
    ap.add_argument("--skip-a", action="store_true",
                    help="no encoders: segmentation and B only (no A-only runs)")
    ap.add_argument("--title", default="Stage 1, CPU in Docker on the Mac",
                    help="first line of the summary")
    a = ap.parse_args()
    a.b_warmup = a.warmup if a.b_warmup is None else a.b_warmup
    a.b_reps = a.reps if a.b_reps is None else a.b_reps
    os.makedirs(a.out, exist_ok=True)
    stem = os.path.join(a.out, a.prefix)

    import torch
    from lcp.encoders import Encoders
    from lcp.rater import LlamaRater
    if a.threads:
        torch.set_num_threads(a.threads)
    load = {"platform": platform.platform(), "machine": platform.machine(),
            "cpus": os.cpu_count(), "python": platform.python_version(),
            "torch": torch.__version__}
    import llama_cpp
    load["llama_cpp_python"] = llama_cpp.__version__
    si = llama_cpp.llama_print_system_info()
    load["system_info"] = si.decode(errors="replace") if isinstance(si, bytes) else str(si)
    load["vram_start_mib"] = gpu_mem()
    m0 = mem()
    enc = None
    if not a.skip_a:
        t0 = time.perf_counter()
        enc = Encoders()
        load["load_encoders_s"] = time.perf_counter() - t0
        load["load_encoders_each_s"] = enc.load_seconds
        load["mem_after_encoders_gb"] = mem_detail()
    rt = LlamaRater(n_threads=a.threads, n_ctx=a.n_ctx, n_batch=a.n_batch,
                    n_gpu_layers=a.gpu_layers, flash_attn=a.flash_attn, use_mmap=not a.no_mmap)
    load["load_gemma_s"] = rt.load_seconds
    load["mem_after_gemma_gb"] = mem_detail()
    load["vram_after_gemma_mib"] = gpu_mem()
    load["threads_llama"] = rt.llm.n_threads
    load["threads_torch"] = torch.get_num_threads()
    load["mem_start_gb"] = m0
    load["mem_stanza_gb"] = {}
    seg = S.Segmenter()
    print(f"[bench] encoders {load.get('load_encoders_s', float('nan')):.1f}s, "
          f"Gemma {rt.load_seconds:.1f}s, gpu layers {a.gpu_layers}, "
          f"threads llama {rt.llm.n_threads} torch {torch.get_num_threads()}, mem {mem_detail()}, "
          f"vram {load['vram_start_mib']} -> {load['vram_after_gemma_mib']} MiB", flush=True)

    # Warm-up, not recorded: page in the GGUF and run each encoder once.
    t0 = time.perf_counter()
    rt.reuse = False
    for pr in PROMPTS:
        rt.read(pr, "en", "The cat sat on the mat.", "cat")
    if enc is not None:
        enc.embed("The cat sat on the mat.", [(4, 7)])
    load["warmup_s"] = time.perf_counter() - t0
    load["vram_after_warmup_mib"] = gpu_mem()
    load["args"] = vars(a)

    rows, readings = [], []
    for lg in a.langs:
        if lg in S.data.STANZA_LANGS:
            seg.pipeline(lg)
            load["mem_stanza_gb"][lg] = mem_detail()
            print(f"[bench] stanza {lg} loaded in {seg.load_seconds[lg]:.1f}s, "
                  f"mem {load['mem_stanza_gb'][lg]}", flush=True)
        for sz in a.sizes:
            with open(os.path.join(a.texts, f"{lg}_{sz}.txt"), encoding="utf-8") as fh:
                text = fh.read().strip()
            plan = ([] if a.skip_a else [("A-only", a.warmup, a.reps)]) + [
                (md, a.b_warmup, a.b_reps) for md in a.modes
                if not (md == "noreuse" and a.noreuse_sizes and sz not in a.noreuse_sizes)]
            for md, n_warm, n_reps in plan:
                for run in range(n_warm + n_reps):
                    key = dict(lang=lg, size=sz, mode=md, run=run, warmup=run < n_warm)
                    reuse = None if md == "A-only" else md == "reuse"
                    r = analyze(seg, enc, rt, lg, text, reuse, readings, key)
                    rows.append(key | r)
                    print(f"[bench] {lg} size {sz} {md} run {run}{' (warm-up)' if run < n_warm else ''}:"
                          f" {r['content_words']}/{r['words']} content words, {r['readings']} readings,"
                          f" seg {r['t_segment']:.2f}s A {r['t_A']:.2f}s B {r['t_B']:.1f}s"
                          f" total {r['total']:.1f}s, {r['s_per_reading']:.3f}s/reading,"
                          f" {r['prefill_tok_s']:.1f} tok/s, first sentence {r['t_first_sentence']:.1f}s",
                          flush=True)
                    pd.DataFrame(rows).to_csv(stem + ".csv", index=False)
                    pd.DataFrame(readings).to_csv(stem + "_readings.csv", index=False)
        # One stanza pipeline at a time: keeping all nine would push Gemma into swap on a 16 GB VM
        # and distort the B timings. The memory each one adds is in mem_stanza_gb.
        if seg._nlp.pop(lg, None) is not None:
            gc.collect()
        load.setdefault("mem_end_of_lang_gb", {})[lg] = mem_detail()
        load.setdefault("vram_end_of_lang_mib", {})[lg] = gpu_mem()

    rss, peak, cur = mem()
    load |= {"peak_rss_gb": rss, "cgroup_peak_gb": peak, "cgroup_current_gb": cur,
             "mem_end_gb": mem_detail(), "vram_end_mib": gpu_mem(),
             "load_stanza_s": seg.load_seconds}
    with open(stem + "_load.json", "w") as fh:
        json.dump(load, fh, indent=1, default=str)
    summary(pd.DataFrame(rows), load, stem + "_summary.txt", a.title)
    print(f"-> {stem}.csv, {stem}_readings.csv, {stem}_load.json, {stem}_summary.txt")


if __name__ == "__main__":
    main()
