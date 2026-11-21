"""Signal A's encoders on raw text: one forward pass per sentence, pooled on each word's span.

The forward pass gets the input `signal_a.Encoder.embed` builds for a target (the context cropped to
data.CHAR_WINDOW characters on each side of the target, at most 512 subwords) and the pooling is
the same (mean of the last four layers, averaged over the subwords that overlap the target's
characters). Words whose crop windows coincide, which is every word of a sentence shorter than the
window, share one forward pass, and each gets the vector `Encoder.embed` gives for it.

One difference by construction: `Encoder.embed` locates a target with `data.find_char_span`, i.e.
its first occurrence in the context; here the span of the word itself is used, so a word that
occurs twice in a sentence gets the vector of its own occurrence.

Parity check against `Encoder.embed` on MLSP rows (needs the paper's data):
  python -m lcp.encoders --check --paper-release /paper/release
"""
import argparse
import time

import numpy as np

import data
from signal_a import Encoder

DEFAULT = ("xlmr", "labse", "e5")        # the three encoders the system averages


def embed_spans(enc, sent, spans):
    """(vectors (n, dim) float32, ok (n,) bool) for the character spans of `sent`.

    `sent` must be the text `Encoder.embed` would see (newlines replaced, no surrounding space).
    """
    torch = enc.torch
    text = str(sent).replace("\n", " ")
    if text != text.strip():
        raise ValueError("sentence text must not start or end with whitespace")
    X = np.zeros((len(spans), enc.dim), np.float32)
    ok = np.zeros(len(spans), bool)
    windows = {}
    for i, (s, e) in enumerate(spans):
        lo, hi = max(0, s - data.CHAR_WINDOW), min(len(text), e + data.CHAR_WINDOW)
        windows.setdefault((lo, hi), []).append(i)
    with torch.no_grad():
        for (lo, hi), members in windows.items():
            t = enc.tok(text[lo:hi], return_offsets_mapping=True, return_tensors="pt",
                        truncation=True, max_length=512)
            ids = t["input_ids"][0].to(enc.dev)
            hs = enc.model(ids.unsqueeze(0), output_hidden_states=True).hidden_states
            H = torch.stack([hs[k][0] for k in (-4, -3, -2, -1)]).mean(0)
            offs = t["offset_mapping"][0].tolist()
            for i in members:
                cs, ce = spans[i][0] - lo, spans[i][1] - lo
                tgt = [j for j, (a, b) in enumerate(offs) if b > a and a < ce and b > cs]
                if tgt:
                    X[i] = H[tgt].mean(0).float().cpu().numpy()
                    ok[i] = True
    return X, ok


class Encoders:
    def __init__(self, keys=DEFAULT):
        self.load_seconds = {}
        self.models = {}
        for k in keys:
            t0 = time.perf_counter()
            self.models[k] = Encoder(k)
            self.load_seconds[k] = time.perf_counter() - t0

    def embed(self, sent, spans):
        """{encoder: (vectors, ok)} for the words at `spans` of `sent`."""
        return {k: embed_spans(e, sent, spans) for k, e in self.models.items()}


# ----------------------------------------------------------------------------- parity check
def check(release, per_lang):
    """Vectors of `embed_spans` against `Encoder.embed` on the first contexts of each language.

    All targets of a context go through one `embed_spans` call (the shared forward pass), and each
    is compared with its own `Encoder.embed` call. Prints the largest absolute difference."""
    from lcp.paper import use_release
    use_release(release)
    ev = data.load_eval(with_ro=True)
    worst = 0.0
    for key in DEFAULT:
        enc = Encoder(key)
        n_ctx = n_tgt = 0
        for lg, g in ev.groupby("lang"):
            for ctx, gc in list(g.groupby("context_id", sort=False))[:per_lang]:
                text = str(gc["sent"].iloc[0]).replace("\n", " ").strip()
                spans = [data.find_char_span(text, str(t)) for t in gc["token"]]
                keep = [i for i, s in enumerate(spans) if s is not None]
                X, ok = embed_spans(enc, text, [spans[i] for i in keep])
                R, okr = enc.embed(list(gc["sent"].iloc[keep]), list(gc["token"].iloc[keep]))
                if not np.array_equal(ok, okr):
                    raise SystemExit(f"{key} {lg}: located targets differ")
                d = float(np.abs(X[ok] - R[ok]).max()) if ok.any() else 0.0
                worst = max(worst, d)
                n_ctx += 1
                n_tgt += int(ok.sum())
        print(f"[check] {key}: {n_tgt} targets in {n_ctx} contexts, max |diff| so far {worst:.3g}",
              flush=True)
    print(f"[check] max |embed_spans - Encoder.embed| = {worst:.3g}")
    return worst


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--paper-release", default="/paper/release")
    ap.add_argument("--contexts", type=int, default=5, help="contexts per language for --check")
    a = ap.parse_args()
    if a.check:
        check(a.paper_release, a.contexts)
