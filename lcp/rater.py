"""Signal B through llama.cpp: the digit reading of `signal_b.Rater`, from Google's QAT q4_0 GGUF.

The prompt is built as in the paper: `signal_b.render` for the text, then the Hugging Face tokenizer
of `signal_b.GEMMA4_QAT` through apply_chat_template (its tokenizer.json and chat template are
byte-identical to those of the MLX checkpoint the paper used). llama.cpp receives these token ids,
not text. The probability over "1".."5" is computed by `signal_b.Rater.digit_probs` itself, on the
last-position logits llama.cpp returns; only `logits` is replaced.

With `reuse=True` the KV cache keeps the longest prefix shared with the previous prompt and only the
rest is evaluated: the `short` prompt puts the sentence before the word, so consecutive readings of
words of one sentence share most of their tokens.
"""
import os
import time

import numpy as np

import signal_b

# Google's GGUF of the same QAT weights: (repo, revision, file)
GGUF = ("google/gemma-4-12B-it-qat-q4_0-gguf", "29d097773436b69ff9feafd636ab4cf873786537",
        "gemma-4-12b-it-qat-q4_0.gguf")
KEY = "gemma4-12b-4bit"            # the paper's model key in predictions/signal_b.csv


def gguf_path():
    from huggingface_hub import hf_hub_download
    return hf_hub_download(GGUF[0], GGUF[2], revision=GGUF[1])


def load_tokenizer():
    from transformers import TokenizersBackend
    repo, rev = signal_b.GEMMA4_QAT
    return TokenizersBackend.from_pretrained(repo, revision=rev)


def digit_ids(tok):
    """Every token id that decodes to the digit, with and without a leading space.
    Same loop as signal_b.Rater.__init__."""
    ids = {d: [] for d in signal_b.DIGITS}
    for d in signal_b.DIGITS:
        for variant in (d, " " + d):
            for t in tok.encode(variant, add_special_tokens=False):
                if tok.decode([t]).strip() == d and t not in ids[d]:
                    ids[d].append(t)
    return ids


def chat_kwargs(tok):
    """As signal_b.Rater.__init__: thinking off when the template knows the switch."""
    try:
        tmpl = tok.get_chat_template() or ""
    except Exception:
        tmpl = ""
    return {"enable_thinking": False} if "enable_thinking" in tmpl else {}


class LlamaRater(signal_b.Rater):
    def __init__(self, n_threads=None, n_ctx=4096, n_batch=512, n_gpu_layers=0, path=None):
        # signal_b.Rater.__init__ loads MLX or transformers; only its attributes are rebuilt here.
        import llama_cpp
        self.llama_cpp = llama_cpp
        self.backend = "llama.cpp"
        self.tok = load_tokenizer()
        self.ids = digit_ids(self.tok)
        self.chat_kw = chat_kwargs(self.tok)
        n_threads = n_threads or os.cpu_count()
        t0 = time.perf_counter()
        self.llm = llama_cpp.Llama(model_path=path or gguf_path(), n_ctx=n_ctx, n_batch=n_batch,
                                   n_ubatch=n_batch, n_threads=n_threads,
                                   n_threads_batch=n_threads, n_gpu_layers=n_gpu_layers,
                                   logits_all=False, verbose=False)
        self.load_seconds = time.perf_counter() - t0
        self.n_vocab = self.llm.n_vocab()
        self.reuse = False
        self.refused = 0               # partial KV removals llama.cpp refused (reuse mode)
        self._prev = []
        self.last = (0, 0)             # (prompt tokens, tokens evaluated) of the last reading

    def prompt_ids(self, content):
        return self.tok.apply_chat_template([{"role": "user", "content": content}],
                                            add_generation_prompt=True, tokenize=True,
                                            return_dict=False, **self.chat_kw)

    def logits(self, ids):
        ids = list(ids)
        if len(ids) >= self.llm.n_ctx():
            raise ValueError(f"prompt of {len(ids)} tokens does not fit n_ctx={self.llm.n_ctx()}")
        k = 0
        if self.reuse:
            n = min(len(self._prev), len(ids) - 1)      # at least one token is evaluated
            while k < n and self._prev[k] == ids[k]:
                k += 1
        # Drop every cached position from k on. Llama.eval does this too but ignores the result; a
        # refused partial removal (possible with a sliding-window cache) would leave stale KV, so
        # it is checked here and the prompt is then evaluated from scratch.
        if k and not self.llm._ctx.kv_cache_seq_rm(-1, k, -1):
            self.refused += 1
            k = 0
        if k == 0 and not self.llm._ctx.kv_cache_seq_rm(-1, 0, -1):
            raise RuntimeError("llama.cpp refused to clear the KV cache")
        self.llm.n_tokens = k
        self.llm.eval(ids[k:])
        ptr = self.llama_cpp.llama_get_logits_ith(self.llm.ctx, -1)
        out = np.ctypeslib.as_array(ptr, shape=(self.n_vocab,)).astype(np.float32, copy=True)
        self._prev = ids
        self.last = (len(ids), len(ids) - k)
        return out

    def read(self, prompt, lang, sent, token):
        """(p over 1..5, mass on the digits) for one word, as signal_b.run reads it."""
        return self.digit_probs(signal_b.render(prompt, lang, sent, token))


def score(p):
    """The expected rating rescaled to [0, 1], the `score` column of signal_b.csv."""
    return (float(np.asarray(p) @ np.arange(1.0, 6.0)) - 1.0) / 4.0
