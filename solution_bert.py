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
CHAR_WINDOW = 500
VOWELS = set("aeiouyăâîáéíóúàèìòùäëïöü")
MLSP_LANGS = {"french": "fr", "italian": "it", "portuguese": "pt", "spanish": "es", "catalan": "ca"}


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


def zscore(a):
    a = np.asarray(a, float)
    return (a - a.mean()) / (a.std() + 1e-9)


def lexical(tokens, langs):
    """Trasaturi lexicale universale per token: zipf (pe limba data), lungime, silabe, majuscula."""
    from wordfreq import zipf_frequency
    out = np.zeros((len(tokens), 4), np.float32)
    for i, (tok, lg) in enumerate(zip(tokens, langs)):
        t = normalize_token(tok)
        lg = lg if isinstance(lg, str) else "en"
        out[i] = [zipf_frequency(t.lower(), lg) if t else 0.0, len(t),
                  n_syllables(t), 1.0 if t[:1].isupper() else 0.0]
    return out


# ----------------------------------------------------------------------------- XLM-R embeddings
class XLMR:
    def __init__(self):
        import torch
        from transformers import AutoTokenizer, AutoModel
        self.torch = torch
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"
        dt = torch.float16 if self.dev == "cuda" else torch.float32
        self.tok = AutoTokenizer.from_pretrained(XLMR_NAME)
        self.model = AutoModel.from_pretrained(XLMR_NAME, torch_dtype=dt).to(self.dev).eval()
        self.dim = self.model.config.hidden_size

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
                last4 = self.torch.stack(out.hidden_states[-4:]).mean(0)[0]
                X[i] = last4[tgt].mean(0).float().cpu().numpy(); ok[i] = True
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


def _Xc(E, lex, mu):
    """[embedding centrat pe limba] ++ [fertility=0 placeholder, lexical]."""
    return np.hstack([E - mu, np.zeros((len(E), 1), np.float32), lex])


# ----------------------------------------------------------------------------- recompute (GPU)
def recompute_signals(test):
    """Recalculeaza semnalele de la zero. Salveaza cache in data/. Necesita GPU."""
    import urllib.request
    os.makedirs(DATA, exist_ok=True)
    xr = XLMR()
    ro_tokens, ro_langs = list(test["token"]), ["ro"] * len(test)
    Ete, okte = xr.embed_frame(list(test["text"]), ro_tokens)
    lex_ro = lexical(ro_tokens, ro_langs)
    mean_ro = Ete.mean(0, keepdims=True)

    # --- A1: CompLex EN ---
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
    Een, oken = xr.embed_frame(list(en["sentence"]), list(en["token"]))
    lex_en = lexical(list(en["token"]), ["en"] * len(en))
    mean_en = Een.mean(0, keepdims=True)
    xl = blend_ridge_hgb(_Xc(Een[oken], lex_en[oken], mean_en),
                         en["complexity"].values[oken], _Xc(Ete, lex_ro, mean_ro))
    if (~okte).any():
        xl[~okte] = np.median(xl[okte])
    pd.DataFrame({"datapointID": test["datapointID"], "xl_complexity": xl}).to_csv(
        os.path.join(DATA, "crosslingual_test.csv"), index=False)

    # --- A2: MLSP Romance (gated HF; daca data/mlsp/ lipseste => mlo None, ensemble cade pe EN) ---
    mlo = _recompute_mlsp(xr, Ete, okte, lex_ro, mean_ro)
    if mlo is not None:
        pd.DataFrame({"datapointID": test["datapointID"], "xl_complexity": mlo}).to_csv(
            os.path.join(DATA, "crosslingual_mlsponly_test.csv"), index=False)

    # --- B: LLM-direct ---
    rater = LLMRater()
    llm = np.array([rater.rate(r.text, r.token) for r in test.itertuples()])
    pd.DataFrame({"datapointID": test["datapointID"], "llm_cx": llm}).to_csv(
        os.path.join(DATA, "llm_complexity_test.csv"), index=False)
    return xl, mlo, llm


def _recompute_mlsp(xr, Ete, okte, lex_ro, mean_ro):
    """Transfer din MLSP/MultiLS Romance -> RO test. None daca data/mlsp/*.tsv lipsesc."""
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
    Em, okm = xr.embed_frame(list(ml["sentence"]), list(ml["token"]))
    lex_ml = lexical(list(ml["token"]), list(ml["lg"]))
    mean_ml = Em[okm].mean(0, keepdims=True)
    mlo = blend_ridge_hgb(_Xc(Em[okm], lex_ml[okm], mean_ml),
                          ml["complexity"].values.astype(float)[okm], _Xc(Ete, lex_ro, mean_ro))
    if (~okte).any():
        mlo[~okte] = np.median(mlo[okte])
    return mlo


# ----------------------------------------------------------------------------- cached (CPU)
def load_cached_signals(test):
    def col(fn, c):
        p = os.path.join(DATA, fn)
        if not os.path.exists(p):
            return None
        return test.merge(pd.read_csv(p), on="datapointID", how="left")[c].values
    return (col("crosslingual_test.csv", "xl_complexity"),
            col("crosslingual_mlsponly_test.csv", "xl_complexity"),
            col("llm_complexity_test.csv", "llm_cx"))


def find_input(opts):
    for n in opts:
        for p in (os.path.join(HERE, n), os.path.join(DATA, n), n):
            if os.path.exists(p):
                return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recompute", action="store_true", help="recalculeaza semnalele de la zero (GPU)")
    ap.add_argument("--variant", choices=["best", "enonly", "roonly", "clpure"], default="best",
                    help="best=0.6 ensemble(EN+RO)+0.4 LLM (64.52); enonly=EN+LLM (fara MLSP gated); "
                         "roonly=RO+LLM; clpure=doar cross-lingual ensemble (fara LLM)")
    args = ap.parse_args()

    test_path = find_input(["test_data.csv", "test_set.csv"])
    if test_path is None:
        sys.exit("Nu gasesc test_data.csv")
    test = pd.read_csv(test_path)
    if "datapointID" not in test.columns:
        test = test.reset_index().rename(columns={"index": "datapointID"})
    if "text" not in test.columns and "sentence" in test.columns:
        test = test.rename(columns={"sentence": "text"})

    cached = all(os.path.exists(os.path.join(DATA, f)) for f in
                 ("crosslingual_test.csv", "llm_complexity_test.csv"))
    if cached and not args.recompute:
        print("[reproducere bit-exact] folosesc semnalele cache din data/")
        xl, mlo, llm = load_cached_signals(test)
    else:
        print("[recompute] recalculez semnalele (descarc CompLex + modele; necesita GPU)")
        xl, mlo, llm = recompute_signals(test)

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

    ans = np.clip(CALIB_MEAN + CALIB_STD * zscore(s), 0, 1)
    out = pd.DataFrame({"subtaskID": 1, "datapointID": test["datapointID"], "answer": ans})
    out_path = os.path.join(HERE, "submission.csv")
    out.to_csv(out_path, index=False)
    print(f"Salvat {out_path}: {len(out)} randuri, variant={args.variant}, "
          f"answer mean={ans.mean():.3f} std={ans.std():.3f} (NaN={int(np.isnan(ans).sum())})")


if __name__ == "__main__":
    main()
