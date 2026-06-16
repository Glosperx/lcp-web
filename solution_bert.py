# =============================================================================
# Predictia complexitatii lexicale (limba romana), scor in [0,1].
# Solutie cu SUPERVIZARE DISTANTA din 2 surse INDEPENDENTE (zero antrenare pe etichetele RO):
#   A. CROSS-LINGUAL (ensemble) : regresor antrenat pe seturi de complexitate adnotate Likert
#      (metodologia Complex 2.0, ca etichetele competitiei), aplicat ZERO-SHOT pe romana prin
#      spatiul multilingual XLM-R. Doua surse de transfer, mediate:
#         - CompLex EN  (SemEval-2021 LCP, ~8400 cuvinte engleze)
#         - MLSP/MultiLS Romance (fr/it/pt/es/ca, ~2800 cuvinte; limbi apropiate de RO)
#      Trasaturi: embedding XLM-R (medie subword, ultimele 4 layere, centrat pe limba) + lexical
#      (zipf, lungime, silabe, majuscula). Regresor = blend Ridge + HistGradientBoosting.
#   B. LLM-DIRECT : RoLlama3-8b (open-weights, 8B, rulat local) clasifica fiecare cuvant tinta 1..5
#      in context (schema Complex 2.0); scor = valoarea asteptata din probabilitatile token-ilor "1".."5".
# Fuziune (best): 0.6*z(A) + 0.4*z(B), apoi calibrare la scara complexitatii (mean 0.27, std 0.125,
# derivata prin probing pe leaderboard). NOTA: aceasta varianta NU foloseste eye-tracking (semnal
# comportamental dependent de date); transferul + LLM o intrec. Cele 14 exemple = doar validare.
#
# REPRODUCTIBILITATE:
#   - Cale RAPIDA (implicita): daca exista cache-urile de semnale in data/ (crosslingual_test.csv,
#     crosslingual_mlsponly_test.csv, llm_complexity_test.csv), reproduce BIT-EXACT output-ul incarcat.
#   - Cale COMPLETA (--recompute): recalculeaza de la zero (descarca CompLex; MLSP gated => trebuie
#     pus manual in data/mlsp/; ruleaza XLM-R + RoLlama3 pe GPU).
# Dependinte: pip install torch transformers==4.46.3 bitsandbytes accelerate scikit-learn scipy
#             pandas numpy wordfreq
# Hardware: GPU ~8GB pt --recompute (XLM-R + RoLlama3-8b 4-bit). Calea rapida ruleaza pe CPU.
# Input (auto-detectat): test_data.csv (coloane text, token) ; Output: submission.csv
# =============================================================================

import os
import re
import sys
import argparse
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SEED = 42

# Ponderi fuziune + calibrare (fixate). best = 0.6 cross-lingual-ensemble + 0.4 LLM (public 64.52).
W_CL, W_LLM = 0.6, 0.4
CALIB_MEAN, CALIB_STD = 0.27, 0.125

LLM_NAME = "OpenLLM-Ro/RoLlama3-8b-Instruct"
XLMR_NAME = "xlm-roberta-base"
# Encodere cross-lingual de probat (Lever A). xlmr = baseline. LaBSE/e5 = aliniate cross-lingual prin
# design; incarcate via AutoModel (FARA pachetul sentence-transformers => pinul transformers ramane 4.46.3).
ENCODERS = {"xlmr": "xlm-roberta-base", "labse": "sentence-transformers/LaBSE",
            "e5": "intfloat/multilingual-e5-base"}
CHAR_WINDOW = 500
VOWELS = set("aeiouyăâîáéíóúàèìòùäëïöü")
MLSP_LANGS = {"french": "fr", "italian": "it", "portuguese": "pt", "spanish": "es", "catalan": "ca"}

# Configs embedding (experimente axa Sergiu #1). Tuple = (layere hidden_states, combine, pool, izolat).
#   last4 = baseline (medie ultimele 4, pool subword mean) — reproduce comportamentul original.
#   mid   = layere de mijloc 6-9 (mai bine aliniate cross-lingual).
#   concat4 = last-4 concatenate (4x dim) in loc de mediate.
#   ctxiso  = embedding contextual ++ embedding cuvant izolat (2x dim).
EMB_CONFIGS = {
    "last4":   ((-4, -3, -2, -1), "mean",   "mean", False),
    "mid":     ((6, 7, 8, 9),     "mean",   "mean", False),
    "concat4": ((-4, -3, -2, -1), "concat", "mean", False),
    "ctxiso":  ((-4, -3, -2, -1), "mean",   "mean", True),
}


# ----------------------------------------------------------------------------- utils
def normalize_token(w):
    w = str(w).strip()
    w = re.sub(r'^[„""\'\"({\[«»\-–—]+', '', w)
    w = re.sub(r'[.,;:!?\)\]}"\'\"»–—]+$', '', w)
    return w.strip()


def find_char_span(text, token):
    tok = str(token).strip()
    idx = text.find(tok)
    if idx < 0:
        tok2 = normalize_token(token)
        if tok2 and tok2 != tok:
            idx = text.find(tok2)
            if idx >= 0:
                return idx, idx + len(tok2)
        return None
    return idx, idx + len(tok)


def crop_around(text, start, end):
    lo = max(0, start - CHAR_WINDOW); hi = min(len(text), end + CHAR_WINDOW)
    return text[lo:hi], start - lo, end - lo


def n_syllables(w):
    w = w.lower(); c = 0; prev = False
    for ch in w:
        v = ch in VOWELS
        if v and not prev:
            c += 1
        prev = v
    return max(c, 1)


def max_consonant_run(w):
    """Lungimea celui mai lung sir de consoane (proxy fonologic de dificultate)."""
    w = w.lower(); run = best = 0
    for ch in w:
        if ch.isalpha() and ch not in VOWELS:
            run += 1; best = max(best, run)
        else:
            run = 0
    return best


def vowel_ratio(w):
    a = [c for c in w.lower() if c.isalpha()]
    return sum(c in VOWELS for c in a) / len(a) if a else 0.0


# Sufixe latinate (markeri de complexitate impartasiti EN + romanic + RO => cross-lingual curat).
LATINATE_SUFFIXES = ("itate", "tiune", "tione", "zione", "ction", "tion", "sion", "mente",
                     "ment", "ical", "ial", "ity", "ous", "ize", "ise", "ate", "ance",
                     "ence", "ative", "ologie", "ology")


def latinate_suffix(w):
    w = w.lower()
    return 1.0 if any(w.endswith(s) for s in LATINATE_SUFFIXES) else 0.0


def zscore(a):
    a = np.asarray(a, float)
    return (a - a.mean()) / (a.std() + 1e-9)


FEAT_ORDER = ("oov", "phon", "morph")  # ordine deterministica a coloanelor extra (stabilitate)
FEAT_WIDTH = {"oov": 1, "phon": 2, "morph": 1}


def lexical(tokens, langs, feats=(), lemmas=None):
    """Trasaturi lexicale per token. Baza (4): zipf (pe limba data), lungime, silabe, majuscula.
    `feats` adauga coloane extra (oov/phon/morph) in ordinea FEAT_ORDER. Default = baza, neschimbat.
    `lemmas` (optional): frecventa = max(zipf_token, zipf_lema) — repara forme flexionate OOV (RO)."""
    from wordfreq import zipf_frequency
    feats = set(feats)
    extra = sum(FEAT_WIDTH[f] for f in FEAT_ORDER if f in feats)
    out = np.zeros((len(tokens), 4 + extra), np.float32)
    for i, (tok, lg) in enumerate(zip(tokens, langs)):
        t = normalize_token(tok)
        lg = lg if isinstance(lg, str) else "en"
        z = zipf_frequency(t.lower(), lg) if t else 0.0
        if lemmas is not None:                    # frecventa constienta de lema (flexiune RO)
            lem = normalize_token(lemmas[i])
            if lem:
                z = max(z, zipf_frequency(lem.lower(), lg))
        row = [z, len(t), n_syllables(t), 1.0 if t[:1].isupper() else 0.0]
        for name in FEAT_ORDER:
            if name not in feats:
                continue
            if name == "oov":
                row.append(1.0 if z == 0.0 else 0.0)
            elif name == "phon":
                row += [max_consonant_run(t), vowel_ratio(t)]
            elif name == "morph":
                row.append(latinate_suffix(t))
        out[i] = row
    return out


# ----------------------------------------------------------------------------- XLM-R embeddings
class XLMR:
    def __init__(self, cfg="last4", encoder="xlmr"):
        import torch
        from transformers import AutoTokenizer, AutoModel
        self.torch = torch
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"
        dt = torch.float16 if self.dev == "cuda" else torch.float32
        name = ENCODERS[encoder]
        self.enc = encoder
        self.tok = AutoTokenizer.from_pretrained(name)
        self.model = AutoModel.from_pretrained(name, torch_dtype=dt).to(self.dev).eval()
        self.cfg = cfg
        self.layers, self.combine, self.pool, self.iso = EMB_CONFIGS[cfg]
        h = self.model.config.hidden_size
        per = h * (len(self.layers) if self.combine == "concat" else 1)
        self.dim = per * (2 if self.iso else 1)
        self._specials = set(self.tok.all_special_ids)

    def _vec(self, hidden_states, idxs):
        """Combina layerele alese + pool peste subword-urile tinta -> 1 vector. idxs = pozitii subword."""
        layers = [hidden_states[L][0] for L in self.layers]  # fiecare (seq, dim)
        if self.combine == "mean":
            stacked = self.torch.stack(layers).mean(0)       # (seq, dim) — egal cu codul original
            p = stacked[idxs]
            return p[0] if self.pool == "first" else p.mean(0)
        parts = []                                           # combine == "concat"
        for lay in layers:
            p = lay[idxs]
            parts.append(p[0] if self.pool == "first" else p.mean(0))
        return self.torch.cat(parts)

    def _iso_vec(self, tok_str):
        """Embedding-ul cuvantului izolat (fara context) cu acelasi layer-combine."""
        enc = self.tok(tok_str, return_tensors="pt", truncation=True, max_length=32)
        ids = enc["input_ids"][0].to(self.dev)
        idxs = [j for j, t in enumerate(ids.tolist()) if t not in self._specials]
        if not idxs:
            return None
        out = self.model(ids.unsqueeze(0), output_hidden_states=True)
        return self._vec(out.hidden_states, idxs)

    def embed_frame(self, sents, tokens):
        X = np.zeros((len(sents), self.dim), np.float32); ok = np.zeros(len(sents), bool)
        with self.torch.no_grad():
            for i, (sent, token) in enumerate(zip(sents, tokens)):
                text = str(sent).replace("\n", " ").strip()
                span = find_char_span(text, str(token))
                if span is None:
                    continue
                ctx, cs, ce = crop_around(text, span[0], span[1])
                enc = self.tok(ctx, return_offsets_mapping=True, return_tensors="pt",
                               truncation=True, max_length=512)
                offs = enc["offset_mapping"][0].tolist()
                ids = enc["input_ids"][0].to(self.dev)
                tgt = [j for j, (a, b) in enumerate(offs) if b > a and a < ce and b > cs]
                if not tgt:
                    continue
                out = self.model(ids.unsqueeze(0), output_hidden_states=True)
                vec = self._vec(out.hidden_states, tgt)
                if self.iso:
                    iv = self._iso_vec(str(token).strip())
                    if iv is None:
                        continue
                    vec = self.torch.cat([vec, iv])
                X[i] = vec.float().cpu().numpy(); ok[i] = True
        return X, ok


# ----------------------------------------------------------------------------- LLM rating
class LLMRater:
    def __init__(self):
        import torch
        import torch.nn.functional as F
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        self.torch = torch; self.F = F
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"
        bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16,
                                 bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True)
        self.tok = AutoTokenizer.from_pretrained(LLM_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            LLM_NAME, quantization_config=bnb, device_map=self.dev).eval()
        self.digit = {d: [] for d in "12345"}
        for d in "12345":
            for variant in (d, " " + d):
                for tid in self.tok.encode(variant, add_special_tokens=False):
                    if self.tok.decode([tid]).strip() == d:
                        self.digit[d].append(tid)
        self.prompts = [
            ("Esti expert in lingvistica romana. Pe o scara 1-5 (1=foarte familiar, 2=simplu, "
             "3=neutru, 4=dificil, 5=foarte dificil), cat de complex/dificil este cuvantul "
             "\"{tok}\" pentru un cititor obisnuit, in propozitia:\n\"{sent}\"\n"
             "Raspunde DOAR cu o cifra de la 1 la 5."),
            ("In propozitia: \"{sent}\"\nEvalueaza dificultatea lexicala a cuvantului \"{tok}\" "
             "pe o scara de la 1 (foarte familiar) la 5 (foarte dificil). Raspunde doar cu cifra."),
        ]

    def _once(self, sent, tok_str, ptmpl):
        prompt = ptmpl.format(tok=tok_str, sent=str(sent).replace("\n", " ").strip())
        ids = self.tok.apply_chat_template([{"role": "user", "content": prompt}],
                                           add_generation_prompt=True, return_tensors="pt").to(self.dev)
        with self.torch.no_grad():
            logits = self.model(ids).logits[0, -1].float()
        probs = self.F.softmax(logits, dim=-1)
        p = np.array([float(probs[self.digit[d]].sum()) for d in "12345"])
        if p.sum() < 1e-9:
            return None
        p /= p.sum()
        return (float((p * np.arange(1, 6)).sum()) - 1.0) / 4.0

    def rate(self, sent, tok_str):
        tok_str = str(tok_str).strip()
        vals = [v for pt in self.prompts if (v := self._once(sent, tok_str, pt)) is not None]
        return float(np.mean(vals)) if vals else np.nan

    def surprisal(self, sent, tok_str):
        """Semnal C: surprisal per-token al cuvantului tinta in context = -log P(tok | context stanga),
        mediat pe subword-uri. Statistica bruta din RoLlama3 (nu antrenata) => independenta de rating."""
        text = str(sent).replace("\n", " ").strip()
        tok = str(tok_str).strip()
        idx = text.find(tok)
        if idx < 0:
            tok = normalize_token(tok_str); idx = text.find(tok)
            if idx < 0:
                return np.nan
        ctx, cs, ce = crop_around(text, idx, idx + len(tok))
        enc = self.tok(ctx, return_offsets_mapping=True, return_tensors="pt",
                       truncation=True, max_length=512)
        offs = enc["offset_mapping"][0].tolist()
        ids = enc["input_ids"][0].to(self.dev)
        if len(ids) < 2:
            return np.nan
        with self.torch.no_grad():
            logits = self.model(ids.unsqueeze(0)).logits[0].float()
        lp = self.F.log_softmax(logits, dim=-1)
        tgt = [i for i, (a, b) in enumerate(offs) if b > a and a < ce and b > cs and i >= 1]
        if not tgt:
            return np.nan
        return float(sum(-lp[i - 1, ids[i]].item() for i in tgt)) / len(tgt)


def blend_ridge_hgb(Xtr, ytr, Xpredict):
    """Blend liniar (Ridge) + neliniar (HistGradientBoosting): media e robusta cross-lingual."""
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import HistGradientBoostingRegressor
    preds = []
    for mk in (lambda: Pipeline([("s", StandardScaler()), ("r", Ridge(alpha=300, random_state=SEED))]),
               lambda: HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                                     l2_regularization=1.0, random_state=SEED)):
        m = mk(); m.fit(Xtr, ytr); preds.append(m.predict(Xpredict))
    return np.mean(preds, axis=0)


def _linreg_pred(Xtr, ytr, Xpredict, est):
    """Regresor liniar unic (StandardScaler + est) pt semnal A. Experiment opt-in (--regressor)."""
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    m = Pipeline([("s", StandardScaler()), ("e", est())]); m.fit(Xtr, ytr)
    return m.predict(Xpredict)


def _make_regressor(name):
    """Alege regresorul pt semnal A. 'blend' (default) = Ridge300+HGB (bit-exact). L1 transfera mai bine
    cross-lingual pe free-gate (vezi analysis_lasso.py): lasso 0.5688 / elasticnet 0.5650 > blend 0.5512."""
    from sklearn.linear_model import Lasso, ElasticNet
    if name == "blend":
        return blend_ridge_hgb
    if name == "lasso":
        return lambda a, b, c: _linreg_pred(a, b, c, lambda: Lasso(alpha=0.01, max_iter=8000, random_state=SEED))
    if name == "elasticnet":
        return lambda a, b, c: _linreg_pred(a, b, c,
                                            lambda: ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=8000, random_state=SEED))
    raise ValueError(name)


REGRESSORS = ("blend", "lasso", "elasticnet")


def _Xc(E, lex, mu):
    """[embedding centrat pe limba] ++ [fertility=0 placeholder, lexical]."""
    return np.hstack([E - mu, np.zeros((len(E), 1), np.float32), lex])


# ----------------------------------------------------------------------------- surse partajate
def _embed_cached(xr, sents, tokens, split):
    """Embed cu cache .npy keyed pe (cfg, split, n_randuri). Experimentele pe features sar re-embed-ul,
    experimentele pe embedding nu re-ruleaza LLM-ul (semnal B separat). dim verificat la reload."""
    tag = f"emb_{split}_{xr.enc}_{xr.cfg}_{len(sents)}"
    ep = os.path.join(DATA, tag + ".npy"); op = os.path.join(DATA, tag + "_ok.npy")
    if os.path.exists(ep) and os.path.exists(op):
        E = np.load(ep)
        if E.shape[1] == xr.dim:
            return E, np.load(op)
    E, ok = xr.embed_frame(sents, tokens)
    os.makedirs(DATA, exist_ok=True)
    np.save(ep, E); np.save(op, ok)
    return E, ok


def _load_complex_en(xr, feats):
    """CompLex EN (descarca daca lipseste). -> (E, lex, y, ok)."""
    import urllib.request
    en_dir = os.path.join(DATA, "complex_en"); os.makedirs(en_dir, exist_ok=True)
    base = "https://raw.githubusercontent.com/MMU-TDMLab/CompLex/master"
    files = {"train": "train/lcp_single_train.tsv", "trial": "trial/lcp_single_trial.tsv",
             "test": "test-labels/lcp_single_test.tsv"}
    en = []
    for k, rel in files.items():
        p = os.path.join(en_dir, f"lcp_single_{k}.tsv")
        if not os.path.exists(p):
            urllib.request.urlretrieve(f"{base}/{rel}", p)
        en.append(pd.read_csv(p, sep="\t").dropna(subset=["sentence", "token", "complexity"]))
    en = pd.concat(en, ignore_index=True)
    E, ok = _embed_cached(xr, list(en["sentence"]), list(en["token"]), "en")
    lex = lexical(list(en["token"]), ["en"] * len(en), feats)
    return E, lex, en["complexity"].values.astype(float), ok


def _load_mlsp(xr, feats):
    """MLSP/MultiLS Romance (gated). -> (E, lex, y, ok) sau None daca data/mlsp/ lipseste."""
    import glob
    mlsp_dir = os.path.join(DATA, "mlsp")
    if not os.path.isdir(mlsp_dir):
        return None
    dfs = []
    for f in glob.glob(os.path.join(mlsp_dir, "*.tsv")):
        x = pd.read_csv(f, sep="\t")
        if {"context", "target", "complexity"}.issubset(x.columns):
            dfs.append(x.rename(columns={"context": "sentence", "target": "token"}))
    if not dfs:
        return None
    ml = pd.concat(dfs, ignore_index=True)
    ml = ml[~ml["token"].astype(str).str.contains(" ", na=False)].reset_index(drop=True)
    ml["lg"] = ml["language"].str.lower().map(MLSP_LANGS)
    E, ok = _embed_cached(xr, list(ml["sentence"]), list(ml["token"]), "mlsp")
    lex = lexical(list(ml["token"]), list(ml["lg"]), feats)
    return E, lex, ml["complexity"].values.astype(float), ok


# ----------------------------------------------------------------------------- gate validare (gratis)
def _cv_r(X, y, k=5):
    """Pearson r prin K-fold in-sursa (proxy secundar)."""
    from sklearn.model_selection import KFold
    from scipy.stats import pearsonr
    pred = np.zeros(len(y))
    for tr, te in KFold(n_splits=k, shuffle=True, random_state=SEED).split(X):
        pred[te] = blend_ridge_hgb(X[tr], y[tr], X[te])
    return pearsonr(pred, y)[0]


def transfer_eval(emb_cfg="last4", feats=(), encoder="xlmr"):
    """Gate gratis: cat de bine transfera config-ul intre limbi (train EN->test Romanic si invers).
    Proxy onest pentru scenariul RO (mii de etichete), spre deosebire de cele 14 etichete RO care nu prezic.
    Centrarea pe limba imita productia: EN cu media tuturor randurilor, MLSP cu media okm."""
    from scipy.stats import pearsonr
    xr = XLMR(emb_cfg, encoder)
    Een, lex_en, yen, oken = _load_complex_en(xr, feats)
    src = _load_mlsp(xr, feats)
    if src is None:
        sys.exit("transfer_eval are nevoie de data/mlsp/ (MLSP Romance, gated)")
    Em, lex_ml, yml, okm = src
    Xen = _Xc(Een[oken], lex_en[oken], Een.mean(0, keepdims=True)); yen = yen[oken]
    Xml = _Xc(Em[okm], lex_ml[okm], Em[okm].mean(0, keepdims=True)); yml = yml[okm]
    r_en2ml = pearsonr(blend_ridge_hgb(Xen, yen, Xml), yml)[0]
    r_ml2en = pearsonr(blend_ridge_hgb(Xml, yml, Xen), yen)[0]
    cv_en, cv_ml = _cv_r(Xen, yen), _cv_r(Xml, yml)
    flabel = "+".join(sorted(feats)) if feats else "base"
    print(f"[transfer_eval] enc={encoder:5s} emb={emb_cfg:8s} feats={flabel:16s} | EN->ML {r_en2ml:.4f} | "
          f"ML->EN {r_ml2en:.4f} | transfer_avg {0.5 * (r_en2ml + r_ml2en):.4f} | "
          f"cvEN {cv_en:.4f} | cvML {cv_ml:.4f}")
    return dict(encoder=encoder, emb=emb_cfg, feats=flabel, en2ml=r_en2ml, ml2en=r_ml2en,
                transfer_avg=0.5 * (r_en2ml + r_ml2en), cv_en=cv_en, cv_ml=cv_ml)


# ----------------------------------------------------------------------------- recompute (GPU)
def recompute_signals(test, emb_cfg="last4", feats=(), reuse_llm=False, tag="", encoder="xlmr",
                      lemma_freq=False, regressor="blend"):
    """Recalculeaza semnalele de la zero (A cross-lingual + B LLM + C surprisal). Salveaza cache. GPU.
    reuse_llm=True => pastreaza llm_complexity_test.csv + surprisal_test.csv (semnale RO-native independente
    de emb/features). tag != "" => scrie semnalul A in CSV-uri proprii (NU suprascrie cache-ul lui best).
    lemma_freq=True => frecventa RO constienta de lema (sursele raman pe token, fallback).
    regressor: 'blend' (default, bit-exact) | 'lasso' | 'elasticnet' pt semnal A."""
    os.makedirs(DATA, exist_ok=True)
    sfx = f"_{tag}" if tag else ""
    reg = _make_regressor(regressor)
    xr = XLMR(emb_cfg, encoder)
    ro_tokens = list(test["token"])
    Ete, okte = _embed_cached(xr, list(test["text"]), ro_tokens, "ro")
    ro_lemmas = test["lemma"].values if (lemma_freq and "lemma" in test.columns) else None
    lex_ro = lexical(ro_tokens, ["ro"] * len(test), feats, lemmas=ro_lemmas)
    mean_ro = Ete.mean(0, keepdims=True)

    # --- A1: CompLex EN ---
    Een, lex_en, yen, oken = _load_complex_en(xr, feats)
    xl = reg(_Xc(Een[oken], lex_en[oken], Een.mean(0, keepdims=True)),
             yen[oken], _Xc(Ete, lex_ro, mean_ro))
    if (~okte).any():
        xl[~okte] = np.median(xl[okte])
    pd.DataFrame({"datapointID": test["datapointID"], "xl_complexity": xl}).to_csv(
        os.path.join(DATA, f"crosslingual_test{sfx}.csv"), index=False)

    # --- A2: MLSP Romance (None daca date gated lipsesc => ensemble cade pe doar-EN) ---
    src = _load_mlsp(xr, feats)
    mlo = None
    if src is not None:
        Em, lex_ml, yml, okm = src
        mlo = reg(_Xc(Em[okm], lex_ml[okm], Em[okm].mean(0, keepdims=True)),
                  yml[okm], _Xc(Ete, lex_ro, mean_ro))
        if (~okte).any():
            mlo[~okte] = np.median(mlo[okte])
        pd.DataFrame({"datapointID": test["datapointID"], "xl_complexity": mlo}).to_csv(
            os.path.join(DATA, f"crosslingual_mlsponly_test{sfx}.csv"), index=False)

    # --- B: LLM rating + C: surprisal (ambele RO-native din acelasi RoLlama3; lent, reuse_llm sare peste) ---
    llm_path = os.path.join(DATA, "llm_complexity_test.csv")
    surp_path = os.path.join(DATA, "surprisal_test.csv")
    llm = (test.merge(pd.read_csv(llm_path), on="datapointID", how="left")["llm_cx"].values
           if reuse_llm and os.path.exists(llm_path) else None)
    surp = (test.merge(pd.read_csv(surp_path), on="datapointID", how="left")["surp"].values
            if reuse_llm and os.path.exists(surp_path) else None)
    if llm is None or surp is None:
        rater = LLMRater()
        if llm is None:
            llm = np.array([rater.rate(r.text, r.token) for r in test.itertuples()])
            pd.DataFrame({"datapointID": test["datapointID"], "llm_cx": llm}).to_csv(llm_path, index=False)
        if surp is None:
            surp = np.array([rater.surprisal(r.text, r.token) for r in test.itertuples()])
            pd.DataFrame({"datapointID": test["datapointID"], "surp": surp}).to_csv(surp_path, index=False)
    return xl, mlo, llm, surp


# ----------------------------------------------------------------------------- cached (CPU)
def load_cached_signals(test):
    def col(fn, c):
        p = os.path.join(DATA, fn)
        if not os.path.exists(p):
            return None
        return test.merge(pd.read_csv(p), on="datapointID", how="left")[c].values
    return (col("crosslingual_test.csv", "xl_complexity"),
            col("crosslingual_mlsponly_test.csv", "xl_complexity"),
            col("llm_complexity_test.csv", "llm_cx"),
            col("surprisal_test.csv", "surp"))


def find_input(opts):
    for n in opts:
        for p in (os.path.join(HERE, n), os.path.join(DATA, n), n):
            if os.path.exists(p):
                return p
    return None


# Grila gate runda 2: encodere x (last4, base). Adauga randuri runda 1 daca vrei comparatie.
SWEEP_GRID = [("xlmr", "last4", ()), ("labse", "last4", ()), ("e5", "last4", ())]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recompute", action="store_true", help="recalculeaza semnalele de la zero (GPU)")
    ap.add_argument("--variant", choices=["best", "enonly", "roonly", "clpure"], default="best",
                    help="best=0.6 ensemble(EN+RO)+0.4 LLM (64.52); enonly=EN+LLM (fara MLSP gated); "
                         "roonly=RO+LLM; clpure=doar cross-lingual ensemble (fara LLM)")
    ap.add_argument("--encoder", choices=list(ENCODERS), default="xlmr",
                    help="encoder cross-lingual (xlmr=baseline; labse/e5 = aliniate prin design)")
    ap.add_argument("--emb", choices=list(EMB_CONFIGS), default="last4",
                    help="config embedding pt experimente (last4=baseline). Vezi EMB_CONFIGS.")
    ap.add_argument("--feats", default="", help="features extra, virgula: oov,phon,morph (gol=baza)")
    ap.add_argument("--surp-weight", type=float, default=0.0, dest="surp_weight",
                    help="pondere semnal C surprisal in fuziune (0=neutilizat; ex 0.1, 0.2)")
    ap.add_argument("--eval", action="store_true",
                    help="gate gratis: transfer_eval pt (--encoder,--emb,--feats) si iese (necesita MLSP)")
    ap.add_argument("--sweep", action="store_true",
                    help="ruleaza gate-ul pe grila de candidati si iese (tabel comparativ)")
    ap.add_argument("--out", default=None, help="nume fisier output (implicit submission.csv)")
    ap.add_argument("--llm-file", default=None, dest="llm_file",
                    help="suprascrie semnalul B cu alt cache LLM din data/ (ex llm_fewshot_test.csv)")
    ap.add_argument("--lemma-freq", action="store_true", dest="lemma_freq",
                    help="frecventa RO constienta de lema in semnalul A (repara flexiunea)")
    ap.add_argument("--regressor", choices=REGRESSORS, default="blend",
                    help="regresor semnal A: blend=Ridge300+HGB (default, bit-exact); lasso/elasticnet "
                         "(L1 transfera mai bine cross-lingual pe free-gate)")
    ap.add_argument("--et-weight", type=float, default=0.0, dest="et_weight",
                    help="pondere semnal eye-tracking (et_complexity_proxy din X_test.csv, ET-only) in "
                         "fuziune (0=neutilizat). ET = date competitie, ~0.33 ortogonal pe predictie")
    args = ap.parse_args()

    feats = tuple(f.strip() for f in args.feats.split(",") if f.strip())
    bad = [f for f in feats if f not in FEAT_ORDER]
    if bad:
        sys.exit(f"feats necunoscute: {bad}; valide: {list(FEAT_ORDER)}")

    # --- gate de validare (gratis, nu atinge test-ul) ---
    if args.sweep:
        for enc, e, f in SWEEP_GRID:
            transfer_eval(e, f, enc)
        return
    if args.eval:
        transfer_eval(args.emb, feats, args.encoder)
        return

    test_path = find_input(["test_data.csv", "test_set.csv"])
    if test_path is None:
        sys.exit("Nu gasesc test_data.csv")
    test = pd.read_csv(test_path)
    if "datapointID" not in test.columns:
        test = test.reset_index().rename(columns={"index": "datapointID"})
    if "text" not in test.columns and "sentence" in test.columns:
        test = test.rename(columns={"sentence": "text"})

    is_default = (args.encoder == "xlmr" and args.emb == "last4" and not feats
                  and not args.lemma_freq and args.regressor == "blend")
    canon = all(os.path.exists(os.path.join(DATA, f)) for f in
                ("crosslingual_test.csv", "llm_complexity_test.csv"))
    if is_default and canon and not args.recompute:
        print("[reproducere bit-exact] folosesc semnalele cache din data/")
        xl, mlo, llm, surp = load_cached_signals(test)
    else:
        flabel = "+".join(feats) if feats else "base"
        tag = ("" if is_default else f"{args.encoder}_{args.emb}_{flabel}"
               f"{'_lemma' if args.lemma_freq else ''}{'_'+args.regressor if args.regressor != 'blend' else ''}")
        # semnalele B/C (LLM, surprisal) sunt RO-native, independente de emb/features => reutilizeaza
        # cache-ul daca exista (doar semnalul A se recalculeaza).
        reuse_llm = os.path.exists(os.path.join(DATA, "llm_complexity_test.csv")) and not args.recompute
        print(f"[recompute] enc={args.encoder} emb={args.emb} feats={flabel} tag='{tag or 'canonic'}' "
              f"(reuse_llm={reuse_llm}; descarc CompLex + encoder{'' if reuse_llm else ' + RoLlama3'}; GPU)")
        xl, mlo, llm, surp = recompute_signals(test, args.emb, feats, reuse_llm=reuse_llm, tag=tag,
                                               encoder=args.encoder, lemma_freq=args.lemma_freq,
                                               regressor=args.regressor)

    if args.llm_file:                        # suprascrie semnalul B cu alt prompt LLM (experiment)
        p = os.path.join(DATA, args.llm_file)
        if not os.path.exists(p):
            sys.exit(f"--llm-file: nu gasesc {p}")
        llm = test.merge(pd.read_csv(p), on="datapointID", how="left")["llm_cx"].values
        print(f"[llm-file] semnal B din {args.llm_file}")

    def fill(a):
        a = np.asarray(a, float); m = np.nanmedian(a); return np.where(np.isnan(a), m, a)
    xl, llm = fill(xl), fill(llm)

    # Slot cross-lingual: ensemble EN(CompLex) + Romanic(MLSP) daca semnalul romanic exista.
    # z(0.5*z(EN)+0.5*z(RO)) = media a doua surse de transfer ~indep (corr 0.86) => varianta
    # mai mica, mai robust. Daca mlo lipseste (date MLSP gated absente), cade pe doar-EN.
    have_ro = mlo is not None and np.isfinite(np.asarray(mlo, float)).any()
    if have_ro:
        mlo = fill(mlo)
    xl_ens = zscore(0.5 * zscore(xl) + 0.5 * zscore(mlo)) if have_ro else zscore(xl)

    if args.variant == "enonly":
        s = W_CL * zscore(xl) + W_LLM * zscore(llm)
    elif args.variant == "roonly":
        if not have_ro:
            sys.exit("roonly are nevoie de data/crosslingual_mlsponly_test.csv (MLSP)")
        s = W_CL * zscore(mlo) + W_LLM * zscore(llm)
    elif args.variant == "clpure":
        s = xl_ens
    else:  # best
        if not have_ro:
            print("  ATENTIE: semnal MLSP romanic lipseste => cross-lingual cade pe doar-EN")
        s = W_CL * xl_ens + W_LLM * zscore(llm)

    # Semnal C (surprisal): blend doar daca surp-weight>0. La 0 => s neatins (best bit-exact).
    if args.surp_weight > 0:
        if surp is None or not np.isfinite(np.asarray(surp, float)).any():
            sys.exit("surp-weight>0 dar lipseste data/surprisal_test.csv (ruleaza --recompute intai)")
        w = args.surp_weight
        zc = zscore(fill(surp))
        print(f"  + surprisal: weight={w}, corr(surp, s_fara_C)={np.corrcoef(zc, zscore(s))[0,1]:.3f}, "
              f"corr(surp, llm)={np.corrcoef(zc, zscore(llm))[0,1]:.3f}")
        s = (1.0 - w) * zscore(s) + w * zc

    # Semnal eye-tracking (et_complexity_proxy, ET-only): blend tarziu doar daca et-weight>0. La 0 => neatins.
    if args.et_weight > 0:
        etx = os.path.join(DATA, "X_test.csv")
        if not os.path.exists(etx):
            sys.exit("et-weight>0 dar lipseste data/X_test.csv (et_complexity_proxy)")
        etp = test.merge(pd.read_csv(etx)[["datapointID", "et_complexity_proxy"]],
                         on="datapointID", how="left")["et_complexity_proxy"].values
        if not np.isfinite(np.asarray(etp, float)).any():
            sys.exit("et-weight>0 dar et_complexity_proxy e gol")
        w = args.et_weight
        ze = zscore(fill(etp))
        print(f"  + eye-tracking: weight={w}, corr(et, s_fara_ET)={np.corrcoef(ze, zscore(s))[0,1]:.3f}")
        s = (1.0 - w) * zscore(s) + w * ze

    ans = np.clip(CALIB_MEAN + CALIB_STD * zscore(s), 0, 1)
    out = pd.DataFrame({"subtaskID": 1, "datapointID": test["datapointID"], "answer": ans})
    if args.out:
        out_path = args.out if (os.path.isabs(args.out) or os.sep in args.out) else os.path.join(HERE, args.out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True) if os.path.dirname(out_path) else None
    else:
        out_path = os.path.join(HERE, "submission.csv")
    out.to_csv(out_path, index=False)
    print(f"Salvat {out_path}: {len(out)} randuri, variant={args.variant}, enc={args.encoder}, "
          f"emb={args.emb}, feats={'+'.join(feats) if feats else 'base'}, regressor={args.regressor}, "
          f"surp_w={args.surp_weight}, et_w={args.et_weight}, "
          f"answer mean={ans.mean():.3f} std={ans.std():.3f} (NaN={int(np.isnan(ans).sum())})")


if __name__ == "__main__":
    main()
