# =============================================================================
# Recalcularea semnalelor A, B si C de la zero, pe GPU (companion pentru solutie_finala).
#
# Acest fisier NU este necesar pentru a rula solutia: solutie_finala citeste in mod normal semnalele
# deja calculate din data/*.csv si ruleaza pe CPU. Codul de aici exista pentru reproductibilitate
# (regenerarea cache-ului din modelele brute) si pentru cazul in care setul de test se schimba.
#
# Se foloseste prin: python solutie_finala.py --recompute
# (acela importa de aici functia recalculeaza_semnale).
#
# Semnalul A (transfer cross-lingual): embedding XLM-RoBERTa + regresor Ridge/HistGradientBoosting,
#   antrenat pe CompLex (engleza) si MLSP (limbi romanice), aplicat pe romana.
# Semnalele B (nota) si C (surprisal): modelul RoLlama3-8B.
#
# Dependinte suplimentare fata de calea CPU: torch, transformers==4.46.3, bitsandbytes, scikit-learn.
# Hardware: GPU de aproximativ 8 GB.
# =============================================================================
import os
import glob
import urllib.request
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SEED = 15129

XLMR_NAME = "xlm-roberta-base"
LLM_NAME = "OpenLLM-Ro/RoLlama3-8b-Instruct"
VOWELS = set("aeiouyăâîáéíóúàèìòùäëïöü")
MLSP_LANGS = {"french": "fr", "italian": "it", "portuguese": "pt", "spanish": "es", "catalan": "ca"}
CHAR_WINDOW = 500

import re


# --- trasaturi lexicale (duplicat minimal din solutie_finala, ca fisierul sa fie de sine statator) ---
def normalize_token(w):
    """Elimina punctuatia din jurul cuvantului."""
    w = str(w).strip()
    w = re.sub(r'^[„""\'\"({\[«»\-–—]+', '', w)
    w = re.sub(r'[.,;:!?\)\]}"\'\"»–—]+$', '', w)
    return w.strip()


def n_syllables(w):
    """Numarul de silabe, aproximat prin grupurile de vocale."""
    w = w.lower(); c = 0; prev_vowel = False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            c += 1
        prev_vowel = is_vowel
    return max(c, 1)


def lexical(tokens, langs, lemmas=None):
    """Matricea (n, 4): [frecventa zipf, lungime, silabe, majuscula], cu corectia de lema pentru romana."""
    from wordfreq import zipf_frequency
    out = np.zeros((len(tokens), 4), np.float32)
    for i, (tok, lg) in enumerate(zip(tokens, langs)):
        t = normalize_token(tok)
        if not isinstance(lg, str):    # fallback tacit la "en" (A.1): devine eroare, nu presupunere
            raise ValueError(f"limba nemapata pentru tokenul {tok!r}: {lg!r}")
        z = zipf_frequency(t.lower(), lg) if t else 0.0
        if lemmas is not None:
            lem = normalize_token(lemmas[i])
            if lem:
                z = max(z, zipf_frequency(lem.lower(), lg))
        out[i] = [z, len(t), n_syllables(t), 1.0 if t[:1].isupper() else 0.0]
    return out


def find_char_span(text, token):
    """Pozitia (inceput, sfarsit) a cuvantului in propozitie, sau None."""
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
    """Fereastra de context in jurul cuvantului."""
    lo = max(0, start - CHAR_WINDOW); hi = min(len(text), end + CHAR_WINDOW)
    return text[lo:hi], start - lo, end - lo


# --- embedding XLM-RoBERTa ---
class XLMR:
    """Embedding contextual XLM-RoBERTa: media ultimelor patru straturi, apoi medie pe subcuvinte (768)."""

    def __init__(self):
        import torch
        from transformers import AutoTokenizer, AutoModel
        self.torch = torch
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"
        dt = torch.float16 if self.dev == "cuda" else torch.float32
        self.tok = AutoTokenizer.from_pretrained(XLMR_NAME)
        self.model = AutoModel.from_pretrained(XLMR_NAME, torch_dtype=dt).to(self.dev).eval()
        self.dim = self.model.config.hidden_size

    def _vec(self, hidden_states, idxs):
        stacked = self.torch.stack([hidden_states[L][0] for L in (-4, -3, -2, -1)]).mean(0)
        return stacked[idxs].mean(0)

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
                X[i] = self._vec(out.hidden_states, tgt).float().cpu().numpy(); ok[i] = True
        return X, ok


# --- regresor + asamblare trasaturi ---
def blend_ridge_hgb(Xtr, ytr, Xpredict):
    """Media (Ridge + HistGradientBoosting). Regularizare puternica fiindca transferul intre limbi e fragil."""
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import HistGradientBoostingRegressor
    preds = []
    for make in (
        lambda: Pipeline([("s", StandardScaler()), ("r", Ridge(alpha=300, random_state=SEED))]),
        lambda: HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                              l2_regularization=1.0, random_state=SEED),
    ):
        m = make(); m.fit(Xtr, ytr); preds.append(m.predict(Xpredict))
    return np.mean(preds, axis=0)


def _Xc(E, lex, mu):
    """[embedding centrat pe limba] + [coloana rezervata] + [trasaturi lexicale]."""
    return np.hstack([E - mu, np.zeros((len(E), 1), np.float32), lex])


def _embed_cached(xr, sents, tokens, split):
    """Embedding cu cache pe disc (.npy)."""
    tag = f"emb_{split}_xlmr_last4_{len(sents)}"
    ep = os.path.join(DATA, tag + ".npy"); op = os.path.join(DATA, tag + "_ok.npy")
    if os.path.exists(ep) and os.path.exists(op):
        E = np.load(ep)
        if E.shape[1] == xr.dim:
            return E, np.load(op)
    E, ok = xr.embed_frame(sents, tokens)
    os.makedirs(DATA, exist_ok=True)
    np.save(ep, E); np.save(op, ok)
    return E, ok


def _load_complex_en(xr):
    """CompLex (engleza, SemEval-2021), descarcat daca lipseste."""
    en_dir = os.path.join(DATA, "complex_en"); os.makedirs(en_dir, exist_ok=True)
    base = "https://raw.githubusercontent.com/MMU-TDMLab/CompLex/master"
    files = {"train": "train/lcp_single_train.tsv", "trial": "trial/lcp_single_trial.tsv",
             "test": "test-labels/lcp_single_test.tsv"}
    parts = []
    for k, rel in files.items():
        p = os.path.join(en_dir, f"lcp_single_{k}.tsv")
        if not os.path.exists(p):
            urllib.request.urlretrieve(f"{base}/{rel}", p)
        parts.append(pd.read_csv(p, sep="\t").dropna(subset=["sentence", "token", "complexity"]))
    en = pd.concat(parts, ignore_index=True)
    E, ok = _embed_cached(xr, list(en["sentence"]), list(en["token"]), "en")
    lex = lexical(list(en["token"]), ["en"] * len(en))
    return E, lex, en["complexity"].values.astype(float), ok


def _load_mlsp(xr):
    """MLSP (limbi romanice), pus manual in data/mlsp/. None daca lipseste."""
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
    lex = lexical(list(ml["token"]), list(ml["lg"]))
    return E, lex, ml["complexity"].values.astype(float), ok


# --- model de limbaj: nota (B) + surprisal (C) ---
class LLMRater:
    """RoLlama3-8B (4 biti) pentru nota de dificultate (B) si surprisal (C)."""

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


def recalculeaza_semnale(test):
    """Recalculeaza semnalele A (cele doua parti), B si C de la zero pe GPU si rescrie cache-ul.
    B si C se reutilizeaza din cache daca exista (sunt native pentru romana). Returneaza
    (A_en, A_mlsp, B_llm, C_surp)."""
    os.makedirs(DATA, exist_ok=True)
    xr = XLMR()
    ro_tokens = list(test["token"])
    Ete, okte = _embed_cached(xr, list(test["text"]), ro_tokens, "ro")
    lex_ro = lexical(ro_tokens, ["ro"] * len(test), lemmas=test["lemma"].values)
    mean_ro = Ete.mean(0, keepdims=True)

    def predict_from(source_loader, out_name):
        src = source_loader(xr)
        if src is None:
            return None
        E, lex, y, ok = src
        pred = blend_ridge_hgb(_Xc(E[ok], lex[ok], E[ok].mean(0, keepdims=True)),
                               y[ok], _Xc(Ete, lex_ro, mean_ro))
        if (~okte).any():
            pred[~okte] = np.median(pred[okte])
        pd.DataFrame({"datapointID": test["datapointID"], "xl_complexity": pred}).to_csv(
            os.path.join(DATA, out_name), index=False)
        return pred

    A_en = predict_from(_load_complex_en, "crosslingual_test_xlmr_last4_base_lemma.csv")
    A_mlsp = predict_from(_load_mlsp, "crosslingual_mlsponly_test_xlmr_last4_base_lemma.csv")

    llm_path = os.path.join(DATA, "llm_complexity_test.csv")
    surp_path = os.path.join(DATA, "surprisal_test.csv")
    B_llm = (test.merge(pd.read_csv(llm_path), on="datapointID", how="left")["llm_cx"].values
             if os.path.exists(llm_path) else None)
    C_surp = (test.merge(pd.read_csv(surp_path), on="datapointID", how="left")["surp"].values
              if os.path.exists(surp_path) else None)
    if B_llm is None or C_surp is None:
        rater = LLMRater()
        if B_llm is None:
            B_llm = np.array([rater.rate(r.text, r.token) for r in test.itertuples()])
            pd.DataFrame({"datapointID": test["datapointID"], "llm_cx": B_llm}).to_csv(llm_path, index=False)
        if C_surp is None:
            C_surp = np.array([rater.surprisal(r.text, r.token) for r in test.itertuples()])
            pd.DataFrame({"datapointID": test["datapointID"], "surp": C_surp}).to_csv(surp_path, index=False)
    return A_en, A_mlsp, B_llm, C_surp
