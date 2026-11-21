"""Download, at pinned revisions, the models stage 7 needs on the PC into the Hugging Face cache
(HF_HUB_CACHE, the lcp-hf volume in docker/run_cuda.sh):
  - gguf:      Google's QAT q4_0 GGUF of Gemma 4 12B (lcp.rater.GGUF), sha256 checked; no mmproj;
  - tokenizer: tokenizer.json, tokenizer_config.json, chat_template.jinja and config.json of
               signal_b.GEMMA4_QAT (the prompt is tokenised by it, llama.cpp gets the ids);
  - encoders:  the three encoders of signal A (signal_a.ENCODERS), through signal_a.Encoder
               itself, so exactly the files it loads.
Each part is then loaded back offline as a check. Stanza is separate: python -m lcp.segment --prepare.

  HF_ONLINE=1 docker/run_cuda.sh python scripts/fetch_models.py [--only gguf tokenizer encoders]
"""
import argparse
import hashlib
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import signal_b                                # noqa: E402  (lcp_model on PYTHONPATH)
from lcp import rater                          # noqa: E402

GGUF_SHA256 = "93567e57a8fe10b23569b9d9ec38cd005deedf71e29477c421a4b83f418a538b"
TOKENIZER_FILES = ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja", "config.json")


def sha256(path, chunk=1 << 24):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while b := fh.read(chunk):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="+", choices=["gguf", "tokenizer", "encoders"],
                    default=["tokenizer", "gguf", "encoders"])
    a = ap.parse_args()
    from huggingface_hub import hf_hub_download
    if "tokenizer" in a.only:
        repo, rev = signal_b.GEMMA4_QAT
        for f in TOKENIZER_FILES:
            print(f"[fetch] {repo}@{rev[:8]} {f} -> {hf_hub_download(repo, f, revision=rev)}",
                  flush=True)
        tok = rater.load_tokenizer()
        ids = rater.digit_ids(tok)
        print(f"[fetch] tokenizer loads, digit ids {ids}", flush=True)
    if "gguf" in a.only:
        repo, rev, f = rater.GGUF
        t0 = time.perf_counter()
        path = hf_hub_download(repo, f, revision=rev)
        size = os.path.getsize(path)
        print(f"[fetch] {repo}@{rev[:8]} {f}: {size / 1e9:.2f} GB in "
              f"{time.perf_counter() - t0:.0f}s -> {path}", flush=True)
        t0 = time.perf_counter()
        digest = sha256(path)
        print(f"[fetch] sha256 {digest} ({time.perf_counter() - t0:.0f}s): "
              f"{'OK' if digest == GGUF_SHA256 else 'MISMATCH, expected ' + GGUF_SHA256}",
              flush=True)
        if digest != GGUF_SHA256:
            raise SystemExit(1)
    if "encoders" in a.only:
        from signal_a import ENCODERS, Encoder
        from lcp.encoders import DEFAULT
        for k in DEFAULT:
            t0 = time.perf_counter()
            enc = Encoder(k)
            print(f"[fetch] encoder {k} {ENCODERS[k][0]}@{ENCODERS[k][1][:8]}: dim {enc.dim}, "
                  f"{time.perf_counter() - t0:.0f}s", flush=True)
            del enc


if __name__ == "__main__":
    main()
