"""The whole system on raw text: every content word gets the paper's fused score, a 0-1 score and a
level 1-5, sentence by sentence.

Per sentence (lcp.segment: stanza for nine languages, regex for fil and si):
  A   lcp.encoders (one forward pass per crop window, the vectors of signal_a.Encoder.embed), the
      lexical columns of data.lexical (frequency through the stanza lemma) and the fertility of
      data.fertility, then the exported regressors and z-scores (lcp.fusion);
  B   the three prompts through llama.cpp with KV reuse, in the order of the stage 3 reference
      (prompt by prompt, word by word), then lcp.fusion with the llama.cpp constants;
  fusion, 0-1 score and level from artifacts/params.json.

Long sentences: a sentence of more than PIECE_TOKENS Gemma tokens (192, more than ~99% of the test
contexts) or more than PIECE_WORDS content words (40) is split at word boundaries, preferably after
a comma or similar, into pieces within both limits, and each piece is then a sentence of its own
(context of A and B, KV reuse, one streamed event, one turn of the server); its words are flagged
`cropped`. Without this a single long sentence costs
(words x sentence length): the expert and marked prompts put the word before the sentence, so every
reading evaluates the whole sentence again, and nothing is streamed until it is done.
Prompt length: a prompt longer than n_ctx - margin tokens (1008 with the site's n_ctx 1024) does not
fit; the context is then cropped around the word, in steps of fewer characters on each side, until
it fits (a safeguard: after the split above only a very long word can get there), and the word is
flagged `cropped`. A word whose prompt fits no crop gets no B reading; its B is then the language
mean (z = 0), as data.zscore treats a missing value, and it is flagged `no_B`. A word the encoders
cannot locate gets the language mean for A in the same way (`no_A`).

  python -m lcp.pipeline --lang en --file bench/texts/en_1.txt
"""
import argparse
import json
import re
import time

import numpy as np

import data
import signal_b
from lcp import rater as R
from lcp.encoders import Encoders
from lcp.fusion import Fusion, LEVELS
from lcp.segment import LANGS, Segmenter, _has_letter

PROMPTS = list(signal_b.PROMPTS)        # reading order, as scripts/b_reference.py and bench_cpu.py
CROP_STEPS = (data.CHAR_WINDOW, 400, 300, 200, 150, 100, 60, 30)
PIECE_TOKENS = 192
PIECE_WORDS = 40             # content words per piece: one piece is one turn of the server
BREAK_AFTER = set(",;:)]}»”、，；：")
MAX_CHARS = 20000            # hard limit of one text (~10 pages)
PARA_MAX = 4000              # a longer paragraph is cut at a line break (or a space) for stanza
# Above WARN_CHARS the frontend asks for confirmation. Japanese has ~0.31 content words per
# character, the other languages 0.07-0.11, so 700 characters of Japanese cost about what 2000
# cost elsewhere.
WARN_CHARS, WARN_CHARS_LANG = 2000, {"ja": 700}
# Seconds per 1000 characters on the PC's RTX 2070 SUPER (stage 4, 2-paragraph benchmark texts,
# pt 1 paragraph, stanza loaded, one text at a time), for the frontend's estimate.
EST_S_PER_1000 = {"ca": 21.0, "de": 17.4, "en": 17.9, "es": 19.5, "fil": 23.1, "fr": 22.2,
                  "it": 21.0, "ja": 67.1, "pt": 19.5, "ro": 21.9, "si": 33.9}


def warn_chars(lang):
    return WARN_CHARS_LANG.get(lang, WARN_CHARS)


def paragraphs(text):
    """[(start, end)] of the paragraphs of `text` (separated by blank lines), whitespace stripped;
    a paragraph longer than PARA_MAX is cut at its last line break (else space) before the limit."""
    spans, pos = [], 0
    for m in re.finditer(r"\n[ \t\r]*\n\s*", text):
        spans.append((pos, m.start()))
        pos = m.end()
    spans.append((pos, len(text)))
    out = []
    for a, b in spans:
        while a < b and text[a].isspace():
            a += 1
        while b > a and text[b - 1].isspace():
            b -= 1
        while b - a > PARA_MAX:
            cut = text.rfind("\n", a + PARA_MAX // 2, a + PARA_MAX)
            if cut < 0:
                cut = max(text.rfind(" ", a + PARA_MAX // 2, a + PARA_MAX), a + PARA_MAX)
            e = cut
            while e > a and text[e - 1].isspace():
                e -= 1
            out.append((a, e))
            a = cut
            while a < b and text[a].isspace():
                a += 1
        if a < b:
            out.append((a, b))
    return out


class Unit:
    """A sentence, or a piece of a long one: what A and B see as the context of its words."""
    def __init__(self, text, start, end, words, split=False):
        self.text, self.start, self.end, self.words, self.split = text, start, end, words, split

    @property
    def content_words(self):
        return [w for w in self.words if w.content]


class Cancelled(Exception):
    pass


class Pipeline:
    def __init__(self, artifacts=None, gpu_layers=None, flash_attn=None, n_ctx=None, n_batch=None,
                 threads=None, margin=16, stanza_keep=0, preload_stanza=False, log=print):
        t0 = time.perf_counter()
        self.fz = Fusion(artifacts) if artifacts else Fusion()
        rt_cfg = self.fz.params["b"].get("runtime", {})
        self.config = {"n_gpu_layers": rt_cfg.get("n_gpu_layers", 49) if gpu_layers is None
                       else gpu_layers,
                       "flash_attn": rt_cfg.get("flash_attn", True) if flash_attn is None
                       else flash_attn,
                       "n_ctx": rt_cfg.get("n_ctx", 1024) if n_ctx is None else n_ctx,
                       "n_batch": rt_cfg.get("n_batch", 256) if n_batch is None else n_batch}
        self.limit = self.config["n_ctx"] - margin
        self.langs = [L for L in LANGS if L in self.fz.langs]
        self.load_seconds = {}
        t = time.perf_counter()
        self.enc = Encoders(tuple(self.fz.encoders))
        self.load_seconds["encoders"] = time.perf_counter() - t
        t = time.perf_counter()
        self.rt = R.LlamaRater(n_threads=threads, n_ctx=self.config["n_ctx"],
                               n_batch=self.config["n_batch"],
                               n_gpu_layers=self.config["n_gpu_layers"],
                               flash_attn=self.config["flash_attn"])
        self.rt.reuse = True
        self.load_seconds["gemma"] = time.perf_counter() - t
        from transformers import AutoTokenizer
        self._fert_tok = AutoTokenizer.from_pretrained("xlm-roberta-base",
                                                       revision=data.XLMR_REVISION)
        self.seg = Segmenter()
        self.stanza_keep = stanza_keep
        self._stanza_used = []
        if preload_stanza:          # the first text of a language then waits no 2-3 s for it
            t = time.perf_counter()
            for lg in data.STANZA_LANGS:
                self.seg.pipeline(lg)
                self._stanza_lru(lg)
            self.load_seconds["stanza"] = time.perf_counter() - t
        self.log = log
        # Warm-up: page in the weights, one reading and one encoder pass (not timed).
        t = time.perf_counter()
        self.score_words("en", "The cat sat on the mat.", [(4, 7, "cat", "cat")])
        self.load_seconds["warmup"] = time.perf_counter() - t
        self.load_seconds["total"] = time.perf_counter() - t0

    # ------------------------------------------------------------------ features
    def fertility(self, tokens):
        """data.fertility with the tokenizer kept loaded (same formula, same revision)."""
        tk = self._fert_tok
        return np.array([len(tk.tokenize(" " + data.normalize_token(str(t)))) for t in tokens],
                        np.float32)

    def _prompt(self, pr, lang, sent, w):
        """(prompt text, cropped) for word w = (start, end, text, lemma) of `sent`, or (None, True)
        when no crop fits."""
        content = signal_b.render(pr, lang, sent, w[2])
        if len(self.rt.prompt_ids(content)) <= self.limit:
            return content, False
        for win in CROP_STEPS:
            lo, hi = max(0, w[0] - win), min(len(sent), w[1] + win)
            content = signal_b.render(pr, lang, sent[lo:hi], w[2])
            if len(self.rt.prompt_ids(content)) <= self.limit:
                return content, True
        return None, True

    # ------------------------------------------------------------------ one sentence
    def score_words(self, lang, sent, words, cancel=None):
        """Scores of `words` [(start, end, text, lemma)] in sentence `sent` of language `lang`.

        Returns (list of dicts in the order of `words`, stats). `sent` is the text the encoders and
        prompts see: newlines replaced by spaces, no surrounding whitespace."""
        fz, n = self.fz, len(words)
        st = {"t_A": 0.0, "t_B": 0.0, "t_fusion": 0.0, "readings": 0, "prompt_tokens": 0,
              "evaluated_tokens": 0, "low_mass": 0}
        t = time.perf_counter()
        spans = [(w[0], w[1]) for w in words]
        emb = self.enc.embed(sent, spans)
        texts = [w[2] for w in words]
        lex = data.lexical(texts, [lang] * n, [w[3] for w in words])
        fert = self.fertility(texts)
        arms, a_ok = {}, np.ones(n, bool)
        for e in fz.encoders:
            X, ok = emb[e]
            a_ok &= ok
            pe, pm = np.full(n, np.nan), np.full(n, np.nan)
            if ok.any():
                pe[ok], pm[ok] = fz.arms(e, lang, fz.features(e, lang, X[ok], lex[ok], fert[ok]))
            arms[e] = (pe, pm)
        zA = fz.a_z(lang, arms)
        st["t_A"] = time.perf_counter() - t

        t = time.perf_counter()
        Ps = {pr: np.full((n, 5), np.nan) for pr in PROMPTS}
        cropped, b_ok = np.zeros(n, bool), np.ones(n, bool)
        for pr in PROMPTS:
            for i, w in enumerate(words):
                if cancel is not None and cancel.is_set():
                    raise Cancelled()
                content, crop = self._prompt(pr, lang, sent, w)
                cropped[i] |= crop
                if content is None:
                    b_ok[i] = False
                    continue
                p, raw = self.rt.digit_probs(content)
                if not np.isfinite(p).all():
                    raise RuntimeError("non-finite digit distribution from llama.cpp")
                st["low_mass"] += int(raw < 0.5)
                Ps[pr][i] = p
                st["readings"] += 1
                st["prompt_tokens"] += self.rt.last[0]
                st["evaluated_tokens"] += self.rt.last[1]
        b_raw = fz.b_raw(lang, Ps)
        b_raw[~b_ok] = np.nan                    # data.zscore semantics: the language mean
        zB = fz.b_z(lang, b_raw)
        st["t_B"] = time.perf_counter() - t

        t = time.perf_counter()
        fused = fz.fused(lang, zA, zB)
        score = fz.score01(lang, fused)
        level = fz.level(score)
        z_freq, f_ok = lex[:, 0], lex[:, 3] == 0
        out = []
        for i, w in enumerate(words):
            out.append({"start": int(w[0]), "end": int(w[1]), "text": w[2], "lemma": w[3],
                        "level": int(level[i]), "label": LEVELS[int(level[i])],
                        "score": round(float(score[i]), 4),
                        "zipf": round(float(z_freq[i]), 2) if f_ok[i] else None,
                        "A": round(float(zA[i]), 3), "B": round(float(zB[i]), 3),
                        "fused": round(float(fused[i]), 4),
                        **({"cropped": True} if cropped[i] else {}),
                        **({"no_B": True} if not b_ok[i] else {}),
                        **({"no_A": True} if not a_ok[i] else {})})
        st["t_fusion"] = time.perf_counter() - t
        return out, st

    # ------------------------------------------------------------------ a text
    def _ntok(self, s):
        return len(self.rt.tok.encode(s, add_special_tokens=False))

    def units(self, sent):
        """[Unit]: the sentence itself, or its pieces of at most PIECE_TOKENS tokens and
        PIECE_WORDS content words."""
        n_cw = sum(1 for w in sent.words if w.content)
        if (self._ntok(sent.text) <= PIECE_TOKENS and n_cw <= PIECE_WORDS) or len(sent.words) < 2:
            return [Unit(sent.text, sent.start, sent.end, list(sent.words))]
        out, ws, i = [], sent.words, 0
        cum = [0]
        for w in ws:
            cum.append(cum[-1] + int(w.content))
        while i < len(ws):
            a = ws[i].start
            # the furthest word end that keeps the piece within both limits (binary search)
            lo, hi = i, len(ws) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if (cum[mid + 1] - cum[i] <= PIECE_WORDS
                        and self._ntok(sent.text[a:ws[mid].end]) <= PIECE_TOKENS):
                    lo = mid
                else:
                    hi = mid - 1
            j = lo
            if j < len(ws) - 1:
                # prefer to end after punctuation in the second half of the piece
                for k in range(j, i + (j - i) // 2, -1):
                    nxt = sent.text[ws[k].end:ws[k + 1].start]
                    if any(c in BREAK_AFTER for c in nxt) or (
                            ws[k + 1].text and not ws[k + 1].content
                            and all(c in BREAK_AFTER for c in ws[k + 1].text)):
                        j = k
                        break
            # punctuation tokens right after the piece stay with it
            while j + 1 < len(ws) and ws[j + 1].text and all(c in BREAK_AFTER for c in ws[j + 1].text):
                j += 1
            b = ws[j].end
            piece = [type(w)(w.text, w.start - a, w.end - a, w.lemma, w.upos, w.content)
                     for w in ws[i:j + 1]]
            out.append(Unit(sent.text[a:b], sent.start + a, sent.start + b, piece, split=True))
            i = j + 1
        return out

    def _stanza_lru(self, lang):
        """Keep at most `stanza_keep` stanza pipelines in memory (least recently used dropped)."""
        if lang not in data.STANZA_LANGS:
            return
        if lang in self._stanza_used:
            self._stanza_used.remove(lang)
        self._stanza_used.append(lang)
        while self.stanza_keep and len(self._stanza_used) > self.stanza_keep:
            self.seg._nlp.pop(self._stanza_used.pop(0), None)

    def analyze(self, lang, text, cancel=None):
        """Events for `text`, one step per `next()` (the server interleaves texts step by step):
          {"type": "paragraphs", "paragraphs": [{i, start, end}]}            first, no model work
          {"type": "sentences", "paragraph": p, "sentences": [{i, start, end, content_words}]}
                                                    when paragraph p is segmented (stanza/regex)
          {"type": "sentence", "i", "paragraph", "start", "end", "words": [...]}  per sentence
          {"type": "done", ...}                     counts and timings
        Sentence indices run over the whole text; offsets are in characters of `text`."""
        if lang not in self.langs:
            raise ValueError(f"unsupported language {lang!r}")
        t0 = time.perf_counter()
        self._stanza_lru(lang)
        loaded = lang in self.seg._nlp or lang not in data.STANZA_LANGS
        paras = paragraphs(text)
        yield {"type": "paragraphs", "lang": lang,
               "paragraphs": [{"i": i, "start": a, "end": b} for i, (a, b) in enumerate(paras)]}
        tot = {"t_A": 0.0, "t_B": 0.0, "t_fusion": 0.0, "readings": 0, "prompt_tokens": 0,
               "evaluated_tokens": 0, "low_mass": 0}
        self.rt._prev = []                       # KV reuse starts afresh for every text
        t_seg, t_first, words_all, cropped, n_sent, n_function = 0.0, None, 0, 0, 0, 0
        for pi, (a, b) in enumerate(paras):
            if cancel is not None and cancel.is_set():
                raise Cancelled()
            t = time.perf_counter()
            sents = [u for s in self.seg.segment(lang, text[a:b]) for u in self.units(s)]
            for u in sents:
                u.start += a
                u.end += a
            t_seg += time.perf_counter() - t
            yield {"type": "sentences", "paragraph": pi,
                   "sentences": [{"i": n_sent + k, "start": s.start, "end": s.end,
                                  "content_words": len(s.content_words),
                                  **({"split": True} if s.split else {})}
                                 for k, s in enumerate(sents)]}
            for s in sents:
                if cancel is not None and cancel.is_set():
                    raise Cancelled()
                cw = s.content_words
                res = []
                if cw:
                    res, st = self.score_words(lang, s.text, [(w.start, w.end, w.text, w.lemma)
                                                              for w in cw], cancel)
                    for k in tot:
                        tot[k] += st[k]
                    for r in res:
                        r["start"] += s.start
                        r["end"] += s.start
                        if s.split:
                            r["cropped"] = True
                    words_all += len(res)
                    cropped += sum(1 for r in res if r.get("cropped"))
                # Function words (with a letter, not content) are shown as level 1 without being
                # scored: the system was evaluated on content words (MLSP targets) only.
                fw = [{"start": s.start + w.start, "end": s.start + w.end, "text": w.text,
                       "lemma": w.lemma, "level": 1, "label": LEVELS[1], "function": True}
                      for w in s.words if not w.content and _has_letter(w.text)]
                n_function += len(fw)
                res = sorted(res + fw, key=lambda r: r["start"])
                if t_first is None and cw:
                    t_first = time.perf_counter() - t0
                yield {"type": "sentence", "i": n_sent, "paragraph": pi, "start": s.start,
                       "end": s.end, "words": res}
                n_sent += 1
        total = time.perf_counter() - t0
        yield {"type": "done", "lang": lang, "paragraphs": len(paras), "sentences": n_sent,
               "content_words": words_all, "function_words": n_function,
               "cropped": cropped, "low_mass": tot["low_mass"],
               "timings": {"segment_s": round(t_seg, 3), "stanza_loaded": not loaded,
                           "A_s": round(tot["t_A"], 3), "B_s": round(tot["t_B"], 3),
                           "fusion_s": round(tot["t_fusion"], 4), "total_s": round(total, 3),
                           "first_sentence_s": None if t_first is None else round(t_first, 3),
                           "readings": tot["readings"],
                           "s_per_reading": round(tot["t_B"] / tot["readings"], 4)
                           if tot["readings"] else None,
                           "prompt_tokens": tot["prompt_tokens"],
                           "evaluated_tokens": tot["evaluated_tokens"]}}

    def languages(self):
        p = self.fz.params
        return {"languages": [{"code": L, "name": signal_b.LANG_NAMES[L],
                               "r": round(p["lang"][L]["r"]["fused"], 4),
                               "ci": [round(p["lang"][L]["r"]["lo"], 4),
                                      round(p["lang"][L]["r"]["hi"], 4)],
                               "n_test": p["lang"][L]["n"],
                               "warn_chars": warn_chars(L),
                               "est_s_per_1000_chars": EST_S_PER_1000.get(L)}
                              for L in self.langs],
                "mean_r": round(p["mean_r"]["fused"], 4),
                "mean_ci": [round(v, 4) for v in p["mean_r"]["ci"]],
                "paper_mean_r": round(p.get("paper_stage2", p)["mean_r"]["fused"], 4),
                "levels": {str(k): v for k, v in LEVELS.items()},
                "max_chars": MAX_CHARS}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lang", required=True, choices=LANGS)
    ap.add_argument("--file", required=True)
    a = ap.parse_args()
    with open(a.file, encoding="utf-8") as fh:
        text = fh.read().strip()
    p = Pipeline()
    print(f"[pipeline] loaded in {p.load_seconds['total']:.1f}s {p.load_seconds}", flush=True)
    for ev in p.analyze(a.lang, text):
        if ev["type"] == "sentence":
            lv = [w["level"] for w in ev["words"]]
            print(f"[sentence {ev['i']}] {len(lv)} content words, levels "
                  + "/".join(str(lv.count(k)) for k in range(1, 6)), flush=True)
        elif ev["type"] == "done":
            print(json.dumps(ev), flush=True)


if __name__ == "__main__":
    main()
