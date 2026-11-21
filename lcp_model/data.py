"""Data loading and lexical features shared by both signals.

Evaluation rows are identified by (lang, idx), where idx is the position of the row in the frame
returned by `load_eval`. Predictions in `predictions/` use the same key, so they can be joined to
the data without redistributing any of its text.
"""
import functools
import glob
import os
import re
import urllib.request

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
CACHE_DIR = os.path.join(ROOT, "cache")
PRED_DIR = os.path.join(ROOT, "predictions")
SEED = 42

MLSP_LANGS = {"catalan": "ca", "english": "en", "filipino": "fil", "french": "fr",
              "german": "de", "italian": "it", "japanese": "ja", "portuguese": "pt",
              "sinhala": "si", "spanish": "es"}

# Languages written in Latin script, where syllable count and capitalisation are defined.
LATIN_SCRIPT = frozenset({"ca", "en", "fil", "fr", "de", "it", "pt", "es", "ro"})
# Languages with a stanza lemmatiser. Sinhala has no lemma processor and Tagalog has no model.
STANZA_LANGS = ("ca", "de", "en", "es", "fr", "it", "ja", "pt", "ro")

COMPLEX_URL = ("https://raw.githubusercontent.com/MMU-TDMLab/CompLex/"
               "4b31c2bd34da4c1265f9db3d727d95ee23099f14/")
COMPLEX_FILES = ("train/lcp_single_train.tsv", "trial/lcp_single_trial.tsv",
                 "test-labels/lcp_single_test.tsv")
CHAR_WINDOW = 500
VOWELS = set("aeiouyăâîáéíóúàèìòùäëïöü")
# xlm-roberta-base, which also provides the tokeniser behind the fertility feature
XLMR_REVISION = "e73636d4f797dec63c3081bb6ed5c7b0bb3f2089"


# ----------------------------------------------------------------------------- datasets
def mlsp_dir():
    """Local copy of MLSP2024, downloaded from the gated Hugging Face dataset if absent."""
    d = os.environ.get("MLSP_DIR", os.path.join(DATA_DIR, "MLSP2024"))
    if glob.glob(os.path.join(d, "*", "multils_test_*_lcp_labels.tsv")):
        return d
    from huggingface_hub import snapshot_download
    print(f"[data] downloading MLSP2024 to {d} (requires accepting the dataset terms on HF)")
    return snapshot_download("MLSP2024/MLSP2024", repo_type="dataset", local_dir=d,
                             allow_patterns=["*/multils_*_lcp_labels.tsv"])


def load_mlsp(split="test"):
    """MLSP2024 lexical complexity rows: lang, sent, token, complexity."""
    rows = []
    for f in sorted(glob.glob(os.path.join(mlsp_dir(), "*", f"multils_{split}_*_lcp_labels.tsv"))):
        if os.sep + "All" + os.sep in f:
            continue
        x = pd.read_csv(f, sep="\t")
        x["lang"] = [MLSP_LANGS[str(v).strip().lower()] for v in x["language"]]
        rows.append(x.rename(columns={"context": "sent", "target": "token"})
                    [["lang", "sent", "token", "complexity"]])
    if not rows:
        raise FileNotFoundError(f"no MLSP files for split {split!r}")
    return pd.concat(rows, ignore_index=True).dropna().reset_index(drop=True)


def load_rolcp():
    """RoLCP (Romanian), from the RALS repository. Same columns as `load_mlsp`."""
    p = os.environ.get("ROLCP_CSV", os.path.join(DATA_DIR, "RoLCP.csv"))
    if not os.path.exists(p):
        raise FileNotFoundError(f"{p} not found. See README, section Data.")
    d = pd.read_csv(p, dtype=str, keep_default_na=False)
    d = d[d["complexity"].str.strip() != ""]
    return pd.DataFrame({"lang": "ro", "sent": d["text"].values, "token": d["token"].values,
                         "complexity": d["complexity"].astype(float).values})


def load_eval(with_ro=False):
    """The evaluation frame: MLSP2024 test (10 languages), plus RoLCP as an 11th if requested."""
    d = load_mlsp("test")
    if with_ro:
        d = pd.concat([d, load_rolcp()], ignore_index=True)
    d["context_id"] = d["lang"] + "|" + d["sent"].astype(str)
    d["idx"] = np.arange(len(d))
    return d


def load_complex_en():
    """CompLex 2.0 single-word English data (train, trial and test), downloaded on first use."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    parts = []
    for rel in COMPLEX_FILES:
        p = os.path.join(CACHE_DIR, os.path.basename(rel))
        if not os.path.exists(p):
            urllib.request.urlretrieve(COMPLEX_URL + rel, p + ".tmp")
            os.replace(p + ".tmp", p)          # an interrupted download leaves no partial file
        parts.append(pd.read_csv(p, sep="\t").dropna(subset=["sentence", "token", "complexity"]))
    en = pd.concat(parts, ignore_index=True).rename(columns={"sentence": "sent"})
    return en[["sent", "token", "complexity"]]


# ----------------------------------------------------------------------------- target span
def normalize_token(w):
    w = str(w).strip()
    w = re.sub(r'^[„""\'\"({\[«»\-–—]+', '', w)
    w = re.sub(r'[.,;:!?\)\]}"\'\"»–—]+$', '', w)
    return w.strip()


def find_char_span(text, token):
    """Character span of the target in its context: exact, then normalised, then case-insensitive."""
    tok = str(token).strip()
    i = text.find(tok)
    if i >= 0:
        return i, i + len(tok)
    tok2 = normalize_token(token)
    if tok2 and tok2 != tok:
        i = text.find(tok2)
        if i >= 0:
            return i, i + len(tok2)
    low = text.lower()
    for cand in (tok, tok2):
        if cand:
            i = low.find(cand.lower())
            # lower() can change string length, so the span is only kept if it still matches.
            if i >= 0 and text[i:i + len(cand)].lower() == cand.lower():
                return i, i + len(cand)
    return None


def crop_around(text, start, end):
    lo, hi = max(0, start - CHAR_WINDOW), min(len(text), end + CHAR_WINDOW)
    return text[lo:hi], start - lo, end - lo


# ----------------------------------------------------------------------------- lemmas
def lemmas(frames):
    """Lemma of each target, from stanza run on the full sentence. Cached in cache/lemmas.csv.

    `frames` is a list of (part, DataFrame with lang, sent, token). Returns one list per frame.
    """
    path = os.path.join(CACHE_DIR, "lemmas.csv")
    work = pd.concat([f[["lang", "sent", "token"]].assign(part=p) for p, f in frames],
                     ignore_index=True)
    work["sent"] = work["sent"].astype(str)
    work["token"] = work["token"].astype(str)
    key = ["part", "lang", "sent", "token"]
    tab = (pd.read_csv(path, keep_default_na=False, dtype=str) if os.path.exists(path)
           else pd.DataFrame(columns=key + ["lemma"]))
    have = set(map(tuple, tab[key].values))
    todo = work[[tuple(r) not in have for r in work[key].values]].drop_duplicates(key)
    if len(todo):
        new = _lemmatize(todo)
        tab = pd.concat([tab, new], ignore_index=True)
        os.makedirs(CACHE_DIR, exist_ok=True)
        tab.to_csv(path, index=False)
    look = dict(zip(map(tuple, tab[key].values), tab["lemma"]))
    out = []
    for p, f in frames:
        out.append([look.get((p, lg, str(s), str(t)), "")
                    for lg, s, t in zip(f["lang"], f["sent"], f["token"])])
    return out


def _lemmatize(work):
    import stanza
    from stanza.resources.common import load_resources_json
    rows = []
    for lg in sorted(work["lang"].unique()):
        sub = work[work["lang"] == lg]
        if lg not in STANZA_LANGS:
            rows += [(p, lg, s, t, "") for p, s, t in zip(sub["part"], sub["sent"], sub["token"])]
            continue
        stanza.download(lg, verbose=False)
        have = load_resources_json()[lg]["default_processors"]
        procs = ",".join(x for x in ("tokenize", "mwt", "pos", "lemma") if x in have)
        nlp = stanza.Pipeline(lg, processors=procs, verbose=False, download_method=None)
        sents = list(dict.fromkeys(sub["sent"]))
        print(f"[data] lemmatising {len(sents)} {lg} sentences", flush=True)
        docs = nlp([stanza.Document([], text=s) for s in sents])
        spans = {}
        for s, doc in zip(sents, docs):
            spans[s] = [(t.start_char, t.end_char, w.lemma or "")
                        for sn in doc.sentences for t in sn.tokens
                        if t.start_char is not None and t.end_char is not None for w in t.words]
        for p, s, t in zip(sub["part"], sub["sent"], sub["token"]):
            sp = find_char_span(s, t)
            lem = "" if sp is None else " ".join(
                x for a, b, x in spans[s] if a < sp[1] and b > sp[0] and x)
            if not lem:      # target not found in context: lemmatise it on its own
                d1 = nlp(t)
                lem = " ".join(w.lemma or "" for sn in d1.sentences for w in sn.words).strip()
            rows.append((p, lg, s, t, lem))
    return pd.DataFrame(rows, columns=["part", "lang", "sent", "token", "lemma"])


# ----------------------------------------------------------------------------- lexical features
@functools.cache
def freq_available(lg):
    """True if wordfreq really serves this language. Sinhala is silently mapped to English by
    wordfreq and Japanese needs MeCab, so the language is probed instead of trusted."""
    from wordfreq import available_languages, zipf_frequency
    if lg not in available_languages():
        return False
    try:
        zipf_frequency("a", lg)
        return True
    except Exception:
        return False


def zipf(tok, lg):
    """(Zipf frequency, available). A word missing from a covered language has frequency 0."""
    if not freq_available(lg):
        return 0.0, False
    from wordfreq import zipf_frequency
    t = str(tok).strip().lower()
    return (zipf_frequency(t, lg) if t else 0.0), True


def n_syllables(w):
    c, prev = 0, False
    for ch in w.lower():
        v = ch in VOWELS
        c += v and not prev
        prev = v
    return max(c, 1)


def lexical(tokens, langs, lemmas=None):
    """Per-target columns: frequency, syllables, capitalisation, and two availability flags.

    Frequency is max(zipf(form), zipf(lemma)). Syllables and capitalisation are NaN outside Latin
    script, and the flags record when frequency or the Latin-script features are undefined, so a
    missing value is never read as a small one.
    """
    out = np.zeros((len(tokens), 5), np.float32)
    for i, (tok, lg) in enumerate(zip(tokens, langs)):
        t = normalize_token(tok)
        z, f_ok = zipf(t, lg)
        if lemmas is not None and (lem := normalize_token(lemmas[i])):
            zl, ok = zipf(lem, lg)
            z = max(z, zl) if ok else z
        latin = lg in LATIN_SCRIPT
        out[i] = [z,
                  n_syllables(t) if latin else np.nan,
                  (1.0 if t[:1].isupper() else 0.0) if latin else np.nan,
                  0.0 if f_ok else 1.0,
                  0.0 if latin else 1.0]
    return out


def fertility(tokens, model="xlm-roberta-base", revision=XLMR_REVISION):
    """Number of subword units the tokeniser produces for each target, a script-independent length."""
    from transformers import AutoTokenizer
    tk = AutoTokenizer.from_pretrained(model, revision=revision)
    return np.array([len(tk.tokenize(" " + normalize_token(str(t)))) for t in tokens], np.float32)


# ----------------------------------------------------------------------------- evaluation
def pearson(a, b):
    from scipy.stats import pearsonr
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(pearsonr(a[m], b[m])[0])


def zscore(v):
    """Standardise within a language. Non-finite values become 0, the mean."""
    v = np.asarray(v, float)
    m = np.isfinite(v)
    z = np.zeros(len(v))
    if m.sum() >= 2 and np.std(v[m]) > 0:
        z[m] = (v[m] - v[m].mean()) / v[m].std()
    return z


def boot_r(y, p, groups, n_boot=2000, seed=SEED):
    """Pearson r with a bootstrap over contexts (several targets share a sentence).
    Returns (r, bootstrap samples)."""
    from scipy.stats import pearsonr
    y, p = np.asarray(y, float), np.asarray(p, float)
    codes = pd.factorize(np.asarray(groups))[0]
    by_g = [np.flatnonzero(codes == k) for k in range(codes.max() + 1)]
    rng = np.random.default_rng(seed)
    rs = []
    for _ in range(n_boot):
        sel = np.concatenate([by_g[k] for k in rng.integers(0, len(by_g), len(by_g))])
        if np.unique(y[sel]).size > 1 and np.unique(p[sel]).size > 1:
            rs.append(float(pearsonr(p[sel], y[sel])[0]))
    return float(pearsonr(p, y)[0]), np.asarray(rs)
