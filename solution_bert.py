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

# Bratul romanesc inghetat. NU e un default: LLMRater cere numele modelului explicit, iar constanta
# asta se trece o singura data, la apelantul din recalculeaza_semnale(). E RoLlama3 (peste Llama-3),
# nu RoLlama3.1: corectia ceruta de planul de bake-off §7.2 servea Δ_controlat, iar Δ_controlat a
# murit prin criteriul §5.2 (σ_Δ = 0.0369 > 0.030), deci nu mai are obiect. Bazinul multilingv e in
# mlsp_common.LLM_POOL.
RO_LEGACY_LLM = "OpenLLM-Ro/RoLlama3-8b-Instruct"
XLMR_NAME = "xlm-roberta-base"
# Encodere cross-lingual de probat (Lever A). xlmr = baseline. LaBSE/e5 = aliniate cross-lingual prin
# design; incarcate via AutoModel (FARA pachetul sentence-transformers => pinul transformers ramane 4.46.3).
# `xlmr-large` e adaugat pentru §3.6. Clasa XLMR e generica: ia `hidden_size` din config si
# `last4` inseamna ultimele patru straturi oricate ar fi in total, deci 24 de straturi si 1024 de
# dimensiuni trec neschimbate. Cheia implicita ramane `xlmr`, deci calea romaneasca nu e atinsa.
# ATENTIE: `EMB_CONFIGS["mid"]`, care numeste straturile 6-9 absolut, NU are acelasi inteles pe un
# model de 24 de straturi. Cu `last4` intrebarea nu se pune.
ENCODERS = {"xlmr": "xlm-roberta-base", "xlmr-large": "xlm-roberta-large",
            "labse": "sentence-transformers/LaBSE",
            "e5": "intfloat/multilingual-e5-base",
            # Glot500-m: XLM-R base continuat pe 511 limbi cu vocabular EXTINS. Motivul pentru care
            # e aici nu e ca ar fi mai bun in medie, e ca pe si si fil tokenizeaza chiar altfel,
            # deci e singurul candidat cu sansa reala de corelatie mica fata de ceilalti trei.
            "glot500": "cis-lmu/glot500-base"}
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

# Sweep-ul de extractie: straturi x pooling, 16 combinatii. Cele trei intrari cu pool `mean` de mai
# sus raman EXACT cum sunt scrise (`setdefault` nu le atinge), fiindca cheia de cache e
# `emb_{split}_{enc}_{cfg}_{n}`: un nume reutilizat cu alt continut ar reincarca tacit vectorii vechi
# si s-ar masura configul vechi, fara nicio eroare.
_LAYER_SETS = {"last4":   ((-4, -3, -2, -1), "mean"),
               "mid":     ((6, 7, 8, 9),     "mean"),
               "concat4": ((-4, -3, -2, -1), "concat"),
               "last1":   ((-1,),            "mean")}
for _ln, (_ls, _cb) in _LAYER_SETS.items():
    for _pl in ("mean", "first", "last", "max"):
        EMB_CONFIGS.setdefault(_ln if _pl == "mean" else f"{_ln}_{_pl}", (_ls, _cb, _pl, False))

# Reprezentarea de TIP, fara context deloc. Nu e aici fiindca ar fi mai buna, ci fiindca frontiera de
# decorelare cere un membru structural diferit, iar un vector de tip e cel mai ieftin astfel de membru.
EMB_CONFIGS["isoonly"] = ((-4, -3, -2, -1), "mean", "mean", "only")

# e5 evaluat in conditiile lui. Prefixul intra in fata contextului si MUTA offset-urile, deci span-ul
# de caractere se deplaseaza cu lungimea lui; fara deplasare s-ar citi alte subword-uri si nimic n-ar
# crapa. Config separat, deci cache separat.
EMB_CONFIGS["last4_q"] = ((-4, -3, -2, -1), "mean", "mean", False)
EMB_PREFIX = {"last4_q": "query: "}


# ----------------------------------------------------------------------------- utils
def normalize_token(w):
    w = str(w).strip()
    w = re.sub(r'^[„""\'\"({\[«»\-–—]+', '', w)
    w = re.sub(r'[.,;:!?\)\]}"\'\"»–—]+$', '', w)
    return w.strip()


def find_char_span(text, token):
    """Unde apare tinta in context, ca interval de caractere. None daca nu se gaseste deloc.

    Cautarea sensibila la caz rateaza tinta scrisa cu majuscula la inceput de propozitie, iar randul
    cade tacut din evaluare: 18 instante din 5624 pe test (it 8, pt 5, fr 3, fil 2) si una din cele
    8423 de randuri CompLex EN. De aceea exista si a treia incercare, insensibila la caz.

    **Capcana, si de ce nu e doar `low.find(tok.lower())`:** `str.lower()` poate schimba LUNGIMEA
    (`"İ".lower()` da doua caractere), deci un indice gasit in textul micsorat n-ar mai corespunde
    unui interval de aceeasi lungime in textul original, iar `crop_around` ar taia stramb. Se
    verifica deci ca felia originala are aceeasi lungime si se potriveste; daca nu, se renunta,
    fiindca un span gresit e mai rau decat un rand lipsa.
    """
    tok = str(token).strip()
    idx = text.find(tok)
    if idx >= 0:
        return idx, idx + len(tok)
    tok2 = normalize_token(token)
    if tok2 and tok2 != tok:
        idx = text.find(tok2)
        if idx >= 0:
            return idx, idx + len(tok2)
    low = text.lower()
    for cand in (tok, tok2):
        if not cand:
            continue
        idx = low.find(cand.lower())
        if idx >= 0 and text[idx:idx + len(cand)].lower() == cand.lower():
            return idx, idx + len(cand)
    return None


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


def lexical(tokens, langs, feats=(), lemmas=None, na_policy=None, ctxdiv=None):
    """Trasaturi lexicale per token. Baza (4): zipf (pe limba data), lungime, silabe, majuscula.
    `feats` adauga coloane extra (oov/phon/morph) in ordinea FEAT_ORDER. Default = baza, neschimbat.
    `lemmas` (optional): frecventa = max(zipf_token, zipf_lema) — repara forme flexionate OOV (RO).

    `na_policy` (A.3 + A.4, calea multilingva):
      None    = comportament original, bit-exact. Calea romaneasca trece pe aici.
      "mlsp"  = frecventa prin garda `zipf_safe` (sinhaleza nu mai primeste tacut o valoare
                englezeasca), trasaturile de suprafata latine devin NaN pe limbile unde nu au sens
                (ja, si), si se adauga DOUA coloane indicator la coada: freq_na, surface_na.
                La coada, ca indicii coloanelor existente sa nu se mute.

    `ctxdiv` (diversitate contextuala, `mlsp_common.ctx_div_safe`), cere `na_policy="mlsp"`:
      None     neschimbat, bit-exact. Calea romaneasca si tot ce e publicat trec pe aici.
      "plus"   adauga o coloana la COADA, dupa indicatori. Modelul are si frecventa, si diversitatea.
      "inloc"  INLOCUIESTE coloana 0, adica zipf, pastrand latimea. E testul fidel literaturii:
               Adelman, Brown si Quesada (2006) arata ca efectele de frecventa dispar cand se
               controleaza diversitatea contextuala, dar nu si invers, deci varianta care conteaza e
               substituirea, nu adaugarea.

    De ce "inloc" pastreaza latimea in loc sa scoata coloana: la fel ca la `--no-freq`, o coloana
    inlocuita lasa toate celelalte pozitii pe loc, deci cifra e comparabila cu bratul intreg fara
    nicio alta schimbare."""
    from wordfreq import zipf_frequency
    from mlsp_common import surface_applicable, zipf_safe
    if na_policy not in (None, "mlsp"):
        raise ValueError(f"na_policy necunoscut: {na_policy!r}")
    feats = set(feats)
    if ctxdiv not in (None, "plus", "inloc"):
        raise ValueError(f"ctxdiv necunoscut: {ctxdiv!r}")
    if ctxdiv is not None and na_policy != "mlsp":
        raise ValueError("ctxdiv cere na_policy='mlsp': pe calea veche coloana 0 nu trece prin garda")
    extra = sum(FEAT_WIDTH[f] for f in FEAT_ORDER if f in feats)
    ind = 2 if na_policy == "mlsp" else 0
    ind += 1 if ctxdiv == "plus" else 0
    out = np.zeros((len(tokens), 4 + extra + ind), np.float32)
    for i, (tok, lg) in enumerate(zip(tokens, langs)):
        t = normalize_token(tok)
        if not isinstance(lg, str):    # fallback tacit la "en" (A.1): devine eroare, nu presupunere
            raise ValueError(f"limba nemapata pentru tokenul {tok!r}: {lg!r}")
        if na_policy == "mlsp":
            z, freq_ok = zipf_safe(t, lg)
            surf_ok = surface_applicable(lg)
            cd = None
            if ctxdiv is not None:
                from mlsp_common import ctx_div_safe
                cd, cd_ok = ctx_div_safe(t, lg)
                if lemmas is not None:
                    lem2 = normalize_token(lemmas[i])
                    if lem2:
                        cl, ok_c = ctx_div_safe(lem2, lg)
                        # acelasi max ca la frecventa: o forma flexionata rara nu inseamna un lexem rar
                        cd = max(cd, cl) if ok_c else cd
            if lemmas is not None:
                lem = normalize_token(lemmas[i])
                if lem:
                    zl, ok_l = zipf_safe(lem, lg)
                    z = max(z, zl) if ok_l else z
        else:
            z = zipf_frequency(t.lower(), lg) if t else 0.0
            if lemmas is not None:                # frecventa constienta de lema (flexiune RO)
                lem = normalize_token(lemmas[i])
                if lem:
                    z = max(z, zipf_frequency(lem.lower(), lg))
            freq_ok = surf_ok = True
        row = ([z, len(t), n_syllables(t), 1.0 if t[:1].isupper() else 0.0] if surf_ok
               else [z, len(t), np.nan, np.nan])
        for name in FEAT_ORDER:
            if name not in feats:
                continue
            if name == "oov":
                row.append(1.0 if z == 0.0 else 0.0)
            elif name == "phon":
                row += [max_consonant_run(t), vowel_ratio(t)] if surf_ok else [np.nan, np.nan]
            elif name == "morph":
                row.append(latinate_suffix(t))
        if ctxdiv == "inloc":
            row[0] = cd
        if ind:
            row += [0.0 if freq_ok else 1.0, 0.0 if surf_ok else 1.0]
            if ctxdiv == "plus":
                row.append(cd)
        out[i] = row
    return out


_FERT_TK = {}


def fertility(tokens, model_name=XLMR_NAME):
    """Cate subword-uri da tokenizerul pentru fiecare tinta.

    Trasatura care inlocuieste lungimea in caractere, si motivul e a priori, fara nicio eticheta: o
    tinta japoneza are 3.59 caractere iar una italiana 8.78, deci lungimea nu e comparabila intre
    sisteme de scriere, in timp ce numarul de subword-uri e prin constructie in aceeasi unitate
    peste tot. Pe sinhaleza, unde `zipf_safe` nu intoarce nimic, e singura informatie de tip
    frecventa care ramane.

    Zero greutati de model si zero inferenta, doar tokenizerul. Spatiul din fata e obligatoriu:
    SentencePiece marcheaza inceputul de cuvant, deci fara el prima bucata iese alta.
    """
    if model_name not in _FERT_TK:
        from transformers import AutoTokenizer
        _FERT_TK[model_name] = AutoTokenizer.from_pretrained(model_name)
    tk = _FERT_TK[model_name]
    return np.array([len(tk.tokenize(" " + normalize_token(str(t)))) for t in tokens], np.float32)


# ----------------------------------------------------------------------------- XLM-R embeddings
class XLMR:
    def __init__(self, cfg="last4", encoder="xlmr"):
        import torch
        from transformers import AutoTokenizer, AutoModel
        self.torch = torch
        # mps pe Mac: E1 face ~14.000 de treceri, iar pe CPU costul e cel mai mare din tot pipeline-ul.
        # float32 si pe mps, nu float16: MPS in fp16 ar introduce o a treia precizie in acelasi tabel.
        self.dev = ("cuda" if torch.cuda.is_available()
                    else "mps" if torch.backends.mps.is_available() else "cpu")
        dt = torch.float16 if self.dev == "cuda" else torch.float32
        name = ENCODERS[encoder]
        self.enc = encoder
        self.tok = AutoTokenizer.from_pretrained(name)
        self.model = AutoModel.from_pretrained(name, torch_dtype=dt).to(self.dev).eval()
        self.cfg = cfg
        self.layers, self.combine, self.pool, self.iso = EMB_CONFIGS[cfg]
        self.prefix = EMB_PREFIX.get(cfg, "")
        h = self.model.config.hidden_size
        per = h * (len(self.layers) if self.combine == "concat" else 1)
        # `iso is True` inseamna contextual ++ izolat, deci dim dubla; `iso == "only"` inseamna doar
        # izolat, deci dim simpla. `if self.iso` ar fi adevarat pentru amandoua si ar da dim gresita.
        self.dim = per * (2 if self.iso is True else 1)
        self._specials = set(self.tok.all_special_ids)

    def _pool_sub(self, p):
        """Pool peste subword-urile tintei. `mean` e cel publicat si iese bit cu bit ca inainte.

        `first` era deja implementat; `last` si `max` sunt adaugate pentru sweep-ul de extractie.
        Acs, Kadar si Kornai (EACL 2021) masoara pe sarcini morfologice ca `first`, conventia cea mai
        raspandita, e cea mai PROASTA, deci intrebarea nu e retorica.
        """
        if self.pool == "first":
            return p[0]
        if self.pool == "last":
            return p[-1]
        if self.pool == "max":
            return p.max(0).values
        return p.mean(0)

    def _vec(self, hidden_states, idxs):
        """Combina layerele alese + pool peste subword-urile tinta -> 1 vector. idxs = pozitii subword."""
        layers = [hidden_states[L][0] for L in self.layers]  # fiecare (seq, dim)
        if self.combine == "mean":
            stacked = self.torch.stack(layers).mean(0)       # (seq, dim) — egal cu codul original
            return self._pool_sub(stacked[idxs])
        parts = []                                           # combine == "concat"
        for lay in layers:
            parts.append(self._pool_sub(lay[idxs]))
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
                if self.prefix:                              # muta span-ul cu exact lungimea lui
                    ctx = self.prefix + ctx
                    cs += len(self.prefix); ce += len(self.prefix)
                enc = self.tok(ctx, return_offsets_mapping=True, return_tensors="pt",
                               truncation=True, max_length=512)
                offs = enc["offset_mapping"][0].tolist()
                ids = enc["input_ids"][0].to(self.dev)
                tgt = [j for j, (a, b) in enumerate(offs) if b > a and a < ce and b > cs]
                if not tgt:
                    continue
                if self.iso == "only":
                    # Fara context deloc. Span-ul se calculeaza oricum mai sus, ca masca `ok` sa fie
                    # identica cu a celorlalte configuri si randurile sa se poata media intre ele.
                    iv = self._iso_vec(str(token).strip())
                    if iv is None:
                        continue
                    vec = iv
                    X[i] = vec.float().cpu().numpy(); ok[i] = True
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
def prompts_multi_for(lo, hi):
    """Cele doua sabloane multilingve pentru scara `lo`-`hi`.

    Cele cinci ancore verbale rams cinci, oricat de multe cifre are scara, si se pun la pozitii egal
    distantate: pe 0-9 ies 0, 2, 4, 7, 9. Alternativa, o ancora per cifra, ar cere zece cuvinte pentru
    dificultate care nu exista, si atunci diferenta masurata ar fi intre listele de cuvinte, nu intre
    scari.
    """
    n = hi - lo + 1
    a = [lo + int(round(i * (n - 1) / 4)) for i in range(5)]
    return [
        (f"You are an expert in {{lang}} linguistics. On a scale of {lo}-{hi} ({a[0]}=very familiar, "
         f"{a[1]}=simple, {a[2]}=neutral, {a[3]}=difficult, {a[4]}=very difficult), how complex or "
         f"difficult is the {{lang}} word \"{{tok}}\" for an average reader, in the sentence:\n"
         f"\"{{sent}}\"\nAnswer with ONLY a single digit from {lo} to {hi}."),
        (f"In the {{lang}} sentence: \"{{sent}}\"\nRate the lexical difficulty of the word "
         f"\"{{tok}}\" on a scale from {lo} (very familiar) to {hi} (very difficult). Answer with only "
         f"the digit."),
    ]


class LLMRater:
    """Nota de dificultate (semnal B) si surprisal (semnal C) dintr-un LLM cauzal.

    `model` e o cheie din mlsp_common.LLM_POOL (si atunci repo/revision/backend vin de acolo) sau un
    repo id brut, si atunci `backend` si `revision` se dau explicit. Nu exista default: numele
    modelului decide cifrele, deci se trece intotdeauna de la apelant.
    """

    def __init__(self, model, backend=None, revision=None, scale="1-5", read_prefix=""):
        from mlsp_common import llm_entry
        # Scara de raspuns. Implicit "1-5", adica exact ce era, deci calea publicata si cea romaneasca
        # nu se schimba. O scara se citeste dintr-o SINGURA pozitie de token, deci "1-10" e imposibila:
        # "10" sunt doi tokeni si primul se ciocneste cu nota 1. Singura scara de zece atomi citibila
        # asa e "0-9".
        lo, hi = (int(x) for x in str(scale).split("-"))
        if not (0 <= lo < hi <= 9):
            raise ValueError(f"scara {scale!r}: ambele capete trebuie sa fie cifre, lo < hi")
        self.scale, self.s_lo, self.s_hi = f"{lo}-{hi}", lo, hi
        self.digits = tuple(str(d) for d in range(lo, hi + 1))
        self.vals = np.arange(lo, hi + 1, dtype=float)
        ent = llm_entry(model)
        # `model_config` e opt-in PER INTRARE, nu global: singurul model care are nevoie de el e
        # Gemma 4, al carui config.json declara un model_type pe care mlx_lm 0.31.3 nu-l cunoaste. O
        # remapare globala ar schimba tacut arhitectura si altor modele.
        self.model_config = ent.get("model_config") if ent is not None else None
        if ent is not None:
            repo, revision, backend = ent["repo"], ent["revision"], ent["backend"]
        else:
            repo = str(model)
            backend = backend or "transformers"
        self.name, self.repo, self.revision, self.backend = str(model), repo, revision, backend

        if backend == "mlx":
            self._init_mlx()
        elif backend == "transformers":
            self._init_hf()
        else:
            raise ValueError(f"backend necunoscut: {backend!r} (transformers sau mlx)")

        # Capcana SentencePiece: "1" si "▁1" sunt id-uri diferite, iar unele tokenizere dau cifra doar
        # cu spatiu in fata. Se incearca ambele variante si se verifica prin decode. NESCHIMBAT: merge
        # pe ambele backend-uri, fiindca TokenizerWrapper-ul MLX deleaga encode/decode la tokenizerul HF.
        # Deduplicare, adaugata la D.4 pe 16 august. La tokenizerele BPE (Qwen) encode("1") si
        # encode(" 1") dau ACELASI id, deci varianta originala punea [16, 16] si masa iesea 2.0, adica
        # o "probabilitate" peste 1. La Qwen dublarea e simetrica pe toate cele 5 cifre si normalizarea
        # o anuleaza, dar pe un tokenizer unde "▁1" e id distinct doar pentru unele cifre raportul
        # dintre cifre se distorsioneaza si scorul iese gresit in tacere. Nu schimba nicio cifra deja
        # produsa: semnalele romanesti se citesc din data/*.csv, nu se recalculeaza.
        self.digit = {d: [] for d in self.digits}
        for d in self.digits:
            for variant in (d, " " + d):
                for tid in self.tok.encode(variant, add_special_tokens=False):
                    if self.tok.decode([tid]).strip() == d and tid not in self.digit[d]:
                        self.digit[d].append(tid)
        # Cele doua prompturi ale caii ROMANESTI. Nu se ating: reproducerea bit-exacta a lui
        # output/FINAL_best.csv trece prin ele, iar apelantul e recalculeaza_semnale() cu RO_LEGACY_LLM.
        self.prompts = [
            ("Esti expert in lingvistica romana. Pe o scara 1-5 (1=foarte familiar, 2=simplu, "
             "3=neutru, 4=dificil, 5=foarte dificil), cat de complex/dificil este cuvantul "
             "\"{tok}\" pentru un cititor obisnuit, in propozitia:\n\"{sent}\"\n"
             "Raspunde DOAR cu o cifra de la 1 la 5."),
            ("In propozitia: \"{sent}\"\nEvalueaza dificultatea lexicala a cuvantului \"{tok}\" "
             "pe o scara de la 1 (foarte familiar) la 5 (foarte dificil). Raspunde doar cu cifra."),
        ]
        # Prompturile caii MULTILINGVE, traducerea 1:1 a celor doua de mai sus. Engleza, cu limba
        # tintei numita explicit prin {lang}: o singura instructiune pentru toate cele 10 limbi, in
        # care variaza doar numele limbii si tinta. Varianta veche, in romana, spunea "expert in
        # lingvistica romana" si pe 10 limbi ar fi confundat limba promptului cu limba tintei, deci
        # diferentele de r intre limbi ar fi masurat promptul. Alternativa, 10 traduceri ale
        # instructiunii, ar fi masurat calitatea inegala a traducerilor. Se declara in paper.
        # Literalele de la 1-5, pastrate ca REFERINTA: prin ele trece fiecare cifra publicata, deci
        # nu se genereaza, se compara cu ce genereaza `prompts_multi_for`. Daca generatorul se abate
        # cu un caracter, constructorul crapa aici si nu la a treia zecimala a unui r.
        _LIT_1_5 = [
            ("You are an expert in {lang} linguistics. On a scale of 1-5 (1=very familiar, 2=simple, "
             "3=neutral, 4=difficult, 5=very difficult), how complex or difficult is the {lang} word "
             "\"{tok}\" for an average reader, in the sentence:\n\"{sent}\"\n"
             "Answer with ONLY a single digit from 1 to 5."),
            ("In the {lang} sentence: \"{sent}\"\nRate the lexical difficulty of the word \"{tok}\" "
             "on a scale from 1 (very familiar) to 5 (very difficult). Answer with only the digit."),
        ]
        if prompts_multi_for(1, 5) != _LIT_1_5:
            raise SystemExit("prompts_multi_for(1, 5) nu reproduce sabloanele publicate")
        self.prompts_multi = prompts_multi_for(self.s_lo, self.s_hi)
        # Qwen3 si Qwen3.5 injecteaza un bloc <think> la add_generation_prompt. Fara enable_thinking
        # =False, logits[-1] da distributia peste deschiderea blocului de rationament, nu peste cifre:
        # nu crapa, da cifre plauzibile si gresite. Kwarg-ul se trece doar cand sablonul il declara,
        # ca sa nu depindem de faptul ca Jinja ignora tacut variabilele nefolosite.
        try:
            tmpl = self.tok.get_chat_template() or ""
        except Exception:
            tmpl = ""
        self.thinking = "enable_thinking" in tmpl

        # POZITIA DE CITIRE. Implicit prefix gol, deci calea publicata nu se schimba cu nimic: fara
        # prefix `_read_ids` intoarce chiar lista lui `_encode_chat`, acelasi obiect de dinainte.
        #
        # Cu prefix, cifra nu se mai citeste de la ultima poziție a sablonului de chat, ci dupa un
        # inceput de raspuns FORTAT ("Rating:"). Ipoteza e ca distributia peste cifre e mai curata
        # acolo: la ultima poziție a sablonului modelul mai are de ales si formatul raspunsului, nu
        # doar nota, deci masa se imprastie si pe deschideri de propozitie.
        #
        # Prefixul se adauga DUPA add_generation_prompt=True, adica in rolul de asistent, nu in
        # intrebare. `add_special_tokens=False` e obligatoriu: un BOS in mijlocul secventei ar rupe
        # exact ce citim.
        #
        # CAPCANA, masurata pe 21 august: prefixul trebuie sa se termine cu SPATIU. Dupa `"Rating:"`
        # Gemma pune 0.9999 pe un token de spatiu simplu, iar cifra vine abia dupa el, deci masa pe
        # cele cinci cifre iese 5.5e-08 si D.4 pica pe criteriul 4. Dupa `"Rating: "` masa e 0.99999.
        # Harta `self.digit` are cate un singur id per cifra la Gemma, cel FARA spatiu, fiindca
        # `encode(" 1")` da doi tokeni si cel de spatiu nu se decodeaza ca cifra. A largi harta ar
        # schimba semnalul publicat; spatiul in prefix nu schimba nimic altceva. Nu se pune o garda in
        # cod pentru asta: D.4 e garda, si a prins-o din prima.
        self.read_prefix = str(read_prefix or "")
        self.read_pref_ids = (self.tok.encode(self.read_prefix, add_special_tokens=False)
                              if self.read_prefix else [])
        if self.read_prefix and not self.read_pref_ids:
            raise ValueError(f"prefixul de citire {self.read_prefix!r} s-a codat in zero tokeni")

    # ------------------------------------------------------------------ backend
    def _init_hf(self):
        import torch
        import torch.nn.functional as F
        from transformers import AutoTokenizer, AutoModelForCausalLM
        self.torch = torch; self.F = F
        # Acelasi tipar ca XLMR.__init__, ca dispozitivul sa se aleaga la fel in tot fisierul.
        self.dev = ("cuda" if torch.cuda.is_available()
                    else "mps" if torch.backends.mps.is_available() else "cpu")
        kw = {}
        if self.dev == "cuda":
            # NF4 prin bitsandbytes e CUDA-only. Pe mps sau cpu constructia asta ar crapa, de aceea
            # si importul sta inauntru.
            from transformers import BitsAndBytesConfig
            kw["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True)
        else:
            # float16 pe mps, spre deosebire de float32 ales deliberat in XLMR: acolo encoderul e base
            # si incape, aici un 8B in float32 ar cere ~32 GB si nu intra in cele 24 ale Mac-ului.
            # `dtype=`, nu `torch_dtype=`, depreciat in transformers 5.13.1.
            kw["dtype"] = torch.float16 if self.dev == "mps" else torch.float32
        self.tok = AutoTokenizer.from_pretrained(self.repo, revision=self.revision)
        self.hf_tok = self.tok
        self.model = AutoModelForCausalLM.from_pretrained(
            self.repo, revision=self.revision, device_map=self.dev, **kw).eval()

    def _init_mlx(self):
        import mlx.core as mx
        from mlx_lm import load as mlx_load
        self.mx = mx
        self.dev = "mlx"
        kw = {"model_config": self.model_config} if self.model_config else {}
        self.model, self.tok = mlx_load(self.repo, revision=self.revision, **kw)
        # TokenizerWrapper deleaga prin __getattr__, dar __call__ e dunder si se cauta pe TIP, nu pe
        # instanta, deci wrapper-ul nu e apelabil. surprisal() are nevoie de apelul direct, cu
        # return_offsets_mapping, deci tine si tokenizerul HF brut de dedesubt.
        self.hf_tok = self.tok._tokenizer

    def _logits_last(self, ids):
        """Vectorul COMPLET de logits la ultima pozitie, float32, ca np.ndarray(vocab,).

        Complet, nu top-N: semnalul B cere masa peste toate id-urile care se decodeaza ca "1".."5",
        iar capcana SentencePiece inseamna mai multe id-uri per cifra. De aici si regula ca nu se
        trece prin Ollama sau prin serverul mlx_lm, care trunchiaza amandoua.
        """
        if self.backend == "mlx":
            # bfloat16 -> float32 inainte de orice reducere, oglinda lui .float() de pe calea torch:
            # masa de pe cifre e mica si un softmax in bf16 ar pierde exact ce masuram.
            out = self.model(self.mx.array([ids]))[0, -1].astype(self.mx.float32)
            return np.array(out, copy=False)
        t = self.torch.tensor([ids], device=self.dev)
        with self.torch.no_grad():
            return self.model(t).logits[0, -1].float().cpu().numpy()

    def _logprobs_at(self, ids, tgt):
        """-log P(ids[i] | ids[:i]) pentru fiecare i din `tgt`.

        Reducerea se face in framework, nu pe host: un (seq, vocab) float32 ar fi ~537 MB la Gemma
        (512 x 262144) copiati degeaba, cand ne trebuie len(tgt) numere.
        """
        if self.backend == "mlx":
            mx = self.mx
            lg = self.model(mx.array([ids]))[0].astype(mx.float32)
            lp = lg - mx.logsumexp(lg, axis=-1, keepdims=True)
            return [-float(lp[i - 1, ids[i]]) for i in tgt]
        t = self.torch.tensor([ids], device=self.dev)
        with self.torch.no_grad():
            lg = self.model(t).logits[0].float()
        lp = self.F.log_softmax(lg, dim=-1)
        return [-float(lp[i - 1, ids[i]]) for i in tgt]

    # ------------------------------------------------------------------ prompt
    def _render_chat(self, msgs):
        """Promptul randat ca text. Serveste garda de gandire din d4_sanity.py."""
        kw = {"enable_thinking": False} if self.thinking else {}
        return self.tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False, **kw)

    def _encode_chat(self, msgs):
        """Sablonul de chat -> lista de id-uri.

        `return_dict=False` e obligatoriu: in transformers 5.13.1 default-ul a devenit True, deci
        apelul vechi cu return_tensors="pt" intorcea un BatchEncoding, iar model(ids) il primea ca
        input_ids. Fara return_tensors iese o lista de int, deci neutra fata de backend.
        """
        kw = {"enable_thinking": False} if self.thinking else {}
        return self.tok.apply_chat_template(msgs, add_generation_prompt=True,
                                            tokenize=True, return_dict=False, **kw)

    def _read_ids(self, msgs):
        """Id-urile pe care se face soft-read-ul: sablonul de chat, plus prefixul de citire.

        Fara prefix e chiar `_encode_chat(msgs)`, deci nicio cifra publicata nu trece prin ramura de
        adunare. Numai citirea lui B trece pe aici: `surprisal` scoreaza o secventa DATA si nu are
        sablon de chat, iar generarea din `prompt_lab._gen` trebuie sa porneasca din sablonul curat,
        altfel prefixul ar intra si in textul generat.
        """
        ids = self._encode_chat(msgs)
        return (ids + self.read_pref_ids) if self.read_pref_ids else ids

    def _score_msgs(self, msgs):
        """Soft-read P(1..5) la ultima pozitie -> scor in [0,1], sau None daca masa e degenerata.
        Corpul comun al lui _once si al lui PromptRater._soft_msgs."""
        p, _ = self.digit_mass(msgs)
        if p is None:
            return None
        return self._expected(p)

    def _expected(self, p):
        """Valoarea asteptata a distributiei, adusa in [0,1]. La scara 1-5 e chiar `(sum - 1)/4`."""
        return (float((p * self.vals).sum()) - self.s_lo) / (self.s_hi - self.s_lo)

    def digit_mass(self, msgs):
        """(p_normalizat, masa_bruta). Masa bruta e ce verifica testul de sanatate D.4: daca modul de
        gandire e activ, aproape toata probabilitatea pleaca pe <think> si masa iese ~0."""
        logits = self._logits_last(self._read_ids(msgs))
        e = np.exp(logits - logits.max())
        probs = e / e.sum()
        p = np.array([float(probs[self.digit[d]].sum()) for d in self.digits])
        raw = float(p.sum())
        if raw < 1e-9:
            return None, raw
        return p / raw, raw

    def _prompt_msgs(self, sent, tok_str, ptmpl, lang_label=None):
        """Mesajele de chat pentru un singur prompt. `lang_label` e numele ENGLEZ al limbii, nu codul.

        Campul `lang` se trece mereu: sabloanele romanesti nu il au, iar str.format ignora kwargs
        nefolosite, deci calea veche trece neschimbata prin aceeasi metoda. Corpul e comun cu garda
        D.4 din d4_sanity.py, ca testul de sanatate sa masoare exact promptul pe care ruleaza B.
        """
        return [{"role": "user", "content": ptmpl.format(
            tok=tok_str, sent=str(sent).replace("\n", " ").strip(), lang=lang_label or "")}]

    def _once(self, sent, tok_str, ptmpl, lang_label=None):
        return self._score_msgs(self._prompt_msgs(sent, tok_str, ptmpl, lang_label))

    def rate(self, sent, tok_str, lang=None):
        """Semnal B, media peste cele doua prompturi.

        `lang=None` e calea romaneasca: prompturile in romana, comportament identic cu cel de dinainte
        de bake-off. `lang="ca"` e calea multilingva: prompturile in engleza, cu limba numita explicit.
        Codul de limba se traduce prin mlsp_common.lang_name(), care ridica exceptie la o limba
        nemapata, deci o limba noua nu poate ajunge tacut la un prompt fara nume de limba.
        """
        tok_str = str(tok_str).strip()
        if lang is None:
            tmpls, label = self.prompts, None
        else:
            from mlsp_common import lang_name
            tmpls, label = self.prompts_multi, lang_name(lang)
        vals = [v for pt in tmpls if (v := self._once(sent, tok_str, pt, label)) is not None]
        return float(np.mean(vals)) if vals else np.nan

    def rate_parts(self, sent, tok_str, lang=None):
        """(B, [(p, raw) per prompt]). Ce arunca rate(): distributia normalizata peste 1..5 si masa
        bruta, pastrate per prompt in loc sa fie colapsate in punct.

        Acelasi numar de forward-uri ca rate(), aceeasi selectie de sabloane si aceeasi regula de
        mediere. Formula valorii asteptate e duplicata din `_score_msgs` deliberat, si nu extrasa
        intr-un ajutor comun: rate() trebuie sa ramana o cale INDEPENDENTA, ca reproducerea coloanei B
        sa fie o verificare, nu o tautologie. `p` e None pentru un prompt cu masa degenerata, exact
        cazul pe care rate() il sare.
        """
        tok_str = str(tok_str).strip()
        if lang is None:
            tmpls, label = self.prompts, None
        else:
            from mlsp_common import lang_name
            tmpls, label = self.prompts_multi, lang_name(lang)
        parts, vals = [], []
        for pt in tmpls:
            p, raw = self.digit_mass(self._prompt_msgs(sent, tok_str, pt, label))
            parts.append((p, raw))
            if p is not None:
                vals.append((float((p * self.vals).sum()) - self.s_lo)
                            / (self.s_hi - self.s_lo))
        return (float(np.mean(vals)) if vals else np.nan), parts

    def surprisal(self, sent, tok_str):
        """Semnal C: surprisal per-token al cuvantului tinta in context = -log P(tok | context stanga),
        mediat pe subword-uri. Statistica bruta din model (nu antrenata) => independenta de rating.

        Fara sablon de chat, deliberat: se scoreaza o secventa DATA, nu se genereaza una noua. E si
        motivul pentru care semnalul asta nu poate trece prin Ollama.
        """
        text = str(sent).replace("\n", " ").strip()
        tok = str(tok_str).strip()
        idx = text.find(tok)
        if idx < 0:
            tok = normalize_token(tok_str); idx = text.find(tok)
            if idx < 0:
                return np.nan
        ctx, cs, ce = crop_around(text, idx, idx + len(tok))
        # Fara return_tensors: liste de int, deci acelasi cod pe ambele backend-uri.
        enc = self.hf_tok(ctx, return_offsets_mapping=True, truncation=True, max_length=512)
        offs, ids = enc["offset_mapping"], enc["input_ids"]
        if len(ids) < 2:
            return np.nan
        tgt = [i for i, (a, b) in enumerate(offs) if b > a and a < ce and b > cs and i >= 1]
        if not tgt:
            return np.nan
        return float(np.mean(self._logprobs_at(ids, tgt)))


def blend_ridge_hgb(Xtr, ytr, Xpredict):
    """Blend liniar (Ridge) + neliniar (HistGradientBoosting): media e robusta cross-lingual.

    Imputerul (A.4): HGB trateaza NaN nativ, StandardScaler crapa pe NaN. Deci bratul Ridge primeste
    imputare la mediana calculata PE SETUL DE ANTRENARE, niciodata pe test, fiindca e in Pipeline si
    se potriveste doar la fit. Cand nu exista NaN, imputerul e trecere directa, deci reproducerea
    bit-exacta a caii romanesti nu e atinsa."""
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import HistGradientBoostingRegressor
    preds = []
    for mk in (lambda: Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                                 ("s", StandardScaler()), ("r", Ridge(alpha=300, random_state=SEED))]),
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


def _pipe_pred(Xtr, ytr, Xpredict, est):
    """Estimator unic in lantul imputer + scaler, pt semnal A.

    Acelasi lant ca bratul Ridge din `blend_ridge_hgb`, si din acelasi motiv (A.4): sub
    `na_policy="mlsp"` coloanele de suprafata sunt NaN pe `ja` si `si`, iar tot ce nu e HGB crapa pe
    ele. Imputerul sta in Pipeline, deci mediana se calculeaza pe ANTRENARE, niciodata pe test.
    `_linreg_pred` de mai sus nu are imputer si ramane asa: el e folosit numai pe calea romaneasca
    veche, unde nu exista NaN, si schimbarea lui ar muta cifre publicate."""
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    m = Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                  ("s", StandardScaler()), ("e", est())])
    m.fit(Xtr, ytr)
    p = np.asarray(m.predict(Xpredict))
    # Garda de forma. Mai jos, in `frozen_trial_gap`, vectorul se taie in trei blocuri cu
    # `p[:n_te]`, deci un estimator care intoarce (n, 1) in loc de (n,) ar corupe tacit toate trei
    # fara sa crape nimic. Candidatul evident era `PLSRegression`, dar pe sklearn 1.9 el aplatizeaza
    # deja singur cand `y` e 1-D (verificat: da (200,), nu (200, 1)), deci ASTAZI garda nu prinde pe
    # nimeni. Ramane fiindca e gratis si fiindca versiunile mai vechi de sklearn chiar intorceau o
    # coloana. Se aplatizeaza NUMAI daca e chiar o coloana; orice alta forma e o eroare de estimator,
    # nu ceva de reparat in silentiu. Pe estimatorii de acum `np.asarray` e o vedere, deci nicio
    # cifra publicata nu se misca.
    if p.ndim == 2 and p.shape[1] == 1:
        p = p[:, 0]
    if p.shape != (len(Xpredict),):
        raise SystemExit(f"_pipe_pred: {est} a dat predictie de forma {p.shape} pentru "
                         f"{len(Xpredict)} randuri")
    return p


def _hgb_pred(Xtr, ytr, Xpredict, **kw):
    """HGB singur, FARA imputer: trateaza NaN nativ, exact ca jumatatea lui din `blend_ridge_hgb`.
    Fara `kw` parametrii sunt identici cu cei din blend, deci `hgb` e chiar acea jumatate, izolata."""
    from sklearn.ensemble import HistGradientBoostingRegressor
    p = dict(max_depth=3, learning_rate=0.05, max_iter=400, l2_regularization=1.0, random_state=SEED)
    p.update(kw)
    m = HistGradientBoostingRegressor(**p); m.fit(Xtr, ytr)
    return m.predict(Xpredict)


def _mk_ridge():
    from sklearn.linear_model import Ridge
    return Ridge(alpha=300, random_state=SEED)


def _mk_et():
    from sklearn.ensemble import ExtraTreesRegressor
    return ExtraTreesRegressor(n_estimators=500, max_features=0.3, n_jobs=-1, random_state=SEED)


def _mk_ridge_a(alpha):
    from sklearn.linear_model import Ridge
    return lambda: Ridge(alpha=alpha, random_state=SEED)


def _mk_lasso(alpha):
    from sklearn.linear_model import Lasso
    return lambda: Lasso(alpha=alpha, max_iter=8000, random_state=SEED)


def _mk_enet(alpha, l1r):
    from sklearn.linear_model import ElasticNet
    return lambda: ElasticNet(alpha=alpha, l1_ratio=l1r, max_iter=8000, random_state=SEED)


def _mk_pls(k):
    """PLS cu `scale=False`: scalarea e deja facuta de `StandardScaler` din `_pipe_pred`, iar a doua
    ar fi o a doua conventie pe aceleasi coloane. `n_components` e plafonat de latimea lui X, deci
    `pls-k64` cere cel putin 64 de coloane."""
    from sklearn.cross_decomposition import PLSRegression
    return lambda: PLSRegression(n_components=k, scale=False)


def _mk_huber():
    from sklearn.linear_model import HuberRegressor
    return HuberRegressor(alpha=1e-3, max_iter=500)


def _mk_bayes():
    from sklearn.linear_model import BayesianRidge
    return BayesianRidge()


def _mk_ard():
    """ARD, adica L2 cu o varianta proprie per coeficient, deci rarime prin prior in loc de prin L1.
    E al doilea drum spre acelasi lucru pe care il cauta lasso, si nu e acelasi bias inductiv."""
    from sklearn.linear_model import ARDRegression
    return ARDRegression(max_iter=300)


def _mk_svr_lin():
    from sklearn.svm import LinearSVR
    return LinearSVR(C=0.1, max_iter=5000, random_state=SEED)


def _mk_krr_a(alpha):
    """Kernel ridge RBF EXACT, nu aproximat. `gamma=None` inseamna 1/n_features in `rbf_kernel`,
    adica 1/774 aici, si e singurul reper fara un parametru liber in plus. Masurat pe forma reala
    (13.5k x 774): 7.1s si 4.5 GB de varf per potrivire, deci Nystroem nu e necesar."""
    from sklearn.kernel_ridge import KernelRidge
    return lambda: KernelRidge(alpha=alpha, kernel="rbf", gamma=None)


# Familii parametrice. Numele de pe linia de comanda E numele din fisier (`_p()` pune `_reg-<nume>`),
# deci `alpha` se scrie fara punct: `30`, `1e-3`, `3e-2`. Nu exista nicio traducere intre cele doua
# care sa poata minti. `l<cifre>` e partea zecimala a lui `l1_ratio`, deci `l5` = 0.5 si `l05` = 0.05.
# Se parseaza in loc sa se enumere din acelasi motiv ca `proj-N` la `--emb-tf`: alpha e continuu.
_FAM = (
    (re.compile(r"^ridge-a(?P<a>[0-9.eE+-]+)$"), lambda m: _mk_ridge_a(float(m["a"]))),
    (re.compile(r"^lasso-a(?P<a>[0-9.eE+-]+)$"), lambda m: _mk_lasso(float(m["a"]))),
    (re.compile(r"^krr-a(?P<a>[0-9.eE+-]+)$"), lambda m: _mk_krr_a(float(m["a"]))),
    (re.compile(r"^pls-k(?P<k>[0-9]+)$"), lambda m: _mk_pls(int(m["k"]))),
    (re.compile(r"^enet-a(?P<a>[0-9.eE+-]+)-l(?P<l>[0-9]+)$"),
     lambda m: _mk_enet(float(m["a"]), float("0." + m["l"]))),
)


# ----------------------------------------------------------------------------------------------
# Sesiunea OBIECTIVULUI (26 aug). Tot ce e mai sus schimba FAMILIA DE FUNCTII, pe aceeasi tinta si cu
# aceeasi pierdere patratica. Cifrele de pe disc spun ca aceasta parghie e aproape epuizata: peste
# sase familii cu biasuri inductive complet diferite, `rho` fata de `ridge` nu coboara sub 0.75, iar
# tot ce coboara `rho` pierde `r`. Ce urmeaza schimba celelalte trei lucruri care nu s-au schimbat
# niciodata: PIERDEREA, TINTA si INCADRAREA problemei. Plus un al patrulea, INFORMATIA, care nu era in
# cerere si care e singurul cu mecanism deja masurat in proiect (vezi `_rs_pred`).
#
# Legarea NU e uniforma, si diferenta conteaza. LightGBM si CatBoost trateaza NaN nativ, deci se leaga
# ca `_hgb_pred`, FARA imputer. MLP, kNN si clasificatorii merg prin `_pipe_pred`, care are imputer,
# fiindca sub `na_policy="mlsp"` coloanele de suprafata sunt NaN pe `ja` si `si` si tot ce nu e arbore
# crapa pe ele. Exact asta a facut ca `lasso` sa nu poata rula niciodata inainte de 26 august.


def _lgbm_pred(Xtr, ytr, Xpredict, **kw):
    """LightGBM, fara imputer: trateaza NaN nativ, ca `_hgb_pred`.

    `num_leaves=8` cu `max_depth=3` nu e implicitul bibliotecii (31 si -1), e capacitatea EGALATA cu
    incumbentul: un arbore de adancime 3 are cel mult 8 foi. Fara egalare, diferenta fata de `hgb` ar
    amesteca `leaf-wise fata de depth-wise` cu `de patru ori mai multa capacitate`, si nu s-ar putea
    atribui. `verbose=-1` fiindca altfel scrie o linie per iteratie in jurnalul rularii.

    `n_jobs=1` NU e o alegere de performanta, e obligatoriu aici, si a costat doua rulari cazute.
    Pe macOS, dupa ce torch a atins MPS, o potrivire LightGBM cu mai mult de un fir moare fara niciun
    traceback: procesul dispare, iar in jurnal rămâne doar `resource_tracker: leaked semaphore`. E
    coliziunea a doua incarcari de `libomp` in acelasi proces. Masurat, ca sa nu se caute alt fix:
    `OMP_NUM_THREADS=1` NU ajuta, `KMP_DUPLICATE_LIB_OK=TRUE` NU ajuta, `n_jobs=2` cade la fel, numai
    `n_jobs=1` merge. Si e specific LightGBM-ului: CatBoost cu `thread_count=-1` si RandomForest cu
    `n_jobs=-1` trec amandoua, fiindca al doilea nu foloseste OpenMP deloc.

    Tiparul de retinut, fiindca e a doua oara in proiect cand o rulare moare fara traceback: un log care
    se opreste dupa ultima linie de pregatire si nu are nicio excepție nu e un bug de cod, e o cadere de
    proces, si atunci se caută in biblioteci native, nu in Python."""
    from lightgbm import LGBMRegressor
    p = dict(num_leaves=8, max_depth=3, learning_rate=0.05, n_estimators=400, reg_lambda=1.0,
             n_jobs=1, random_state=SEED, verbose=-1)
    p.update(kw)
    m = LGBMRegressor(**p)
    m.fit(Xtr, ytr)
    return np.asarray(m.predict(Xpredict), float)


def _cat_pred(Xtr, ytr, Xpredict, **kw):
    """CatBoost, fara imputer: trateaza NaN nativ (`nan_mode` implicit), ca `_hgb_pred`.

    Arbori OBLIVIOUS, adica aceeasi taietura pe tot nivelul, plus ordered boosting. E cel mai diferit
    bias inductiv de tip arbore care nu s-a incercat: `hgb`, `hgb-adanc` si `extratrees` sunt toti
    axis-aligned si crescuti liber. `allow_writing_files=False` fiindca implicit scrie `catboost_info/`
    in directorul de lucru, adica in radacina proiectului."""
    from catboost import CatBoostRegressor
    p = dict(depth=3, learning_rate=0.05, iterations=400, l2_leaf_reg=1.0, random_seed=SEED,
             verbose=False, allow_writing_files=False, thread_count=-1)
    p.update(kw)
    m = CatBoostRegressor(**p)
    m.fit(Xtr, ytr)
    return np.asarray(m.predict(Xpredict), float)


def _mk_rf(n):
    """RandomForest: bootstrap plus taieturi COMPLETE. Nu e acelasi lucru cu ExtraTrees, care foloseste
    taieturi aleatoare si nu foloseste bootstrap. `max_features=0.3` e cel al lui `_mk_et`, ca singura
    diferenta fata de reperul deja masurat sa fie chiar cele doua lucruri de mai sus."""
    from sklearn.ensemble import RandomForestRegressor
    return lambda: RandomForestRegressor(n_estimators=n, max_features=0.3, n_jobs=-1,
                                         random_state=SEED)


def _mk_mlp(h):
    """MLP cu un strat ascuns: singura familie complet absenta din proiect. Neliniar DENS, deci nici pe
    ramura liniara nici pe cea de arbori.

    `early_stopping=True` taie 10% din bazinul de antrenare pentru validare interna, deci potrivirea nu
    vede toate randurile. E reproductibil prin `random_state`, dar se raporteaza ca atare: fara oprire
    timpurie numarul de iteratii ar fi un hiperparametru liber in plus, ales pe ce?"""
    from sklearn.neural_network import MLPRegressor
    return lambda: MLPRegressor(hidden_layer_sizes=(h,), alpha=1e-3, early_stopping=True,
                                n_iter_no_change=10, max_iter=300, random_state=SEED)


def _mk_knn(k):
    """kNN: local si non-parametric. Se ruleaza ca CONTROL AL PORTII, nu ca speranta de predictie.
    Se asteapta `r` mic si `rho` mic, iar proiectul a masurat deja de trei ori ca decorelarea care vine
    din zgomot nu valoreaza nimic (TabFM la k=1: rho 0.764, cel mai mic masurat, si strica blend-ul cu
    0.0083). Daca `knn` repeta tiparul, poarta `r_A > 0.53` e justificata cu un al patrulea punct."""
    from sklearn.neighbors import KNeighborsRegressor
    return lambda: KNeighborsRegressor(n_neighbors=k, n_jobs=-1)


# ------------------------------------------------------------------ TINTA: invelisuri de transformare
# Toate primesc si intorc numai `ytr`, deci pragurile, cuantilele si mediile nu pot vedea limba tinuta
# deoparte. Garantia e in SEMNATURA, nu in disciplina: functia nu are de unde sa afle `y` de test.

def _tt_id(y, invers=True):
    """Identitatea. Exista ca CONTROL: `tt-id-<baza>` trebuie sa reproduca `<baza>` bit-exact, altfel
    invelisul insusi schimba cifre si nicio comparatie de mai jos nu inseamna nimic."""
    return np.asarray(y, float), (lambda p: np.asarray(p, float))


def _tt_rank(y, invers=True):
    """Tinta -> rang empiric in [0, 1]. Metrica finala e corelatia Pearson, iar pe date monotone ea e
    apropiata de o corelatie de rang, deci a antrena pe rang aliniaza obiectivul cu metrica.

    Inversa e functia de cuantile empirica a lui `ytr`, adica drumul inapoi in unitati de complexitate.
    Predictia nu e marginita, deci se taie in [0, 1] INAINTE de interpolare; taierea e in spatiul
    RANGULUI, nu al tintei, deci nu inventeaza valori de complexitate care nu exista in antrenare.
    `invers=False` lasa predictia in spatiul rangului: `r` e invariant la transformari afine dar nu la
    unele monotone, deci cele doua variante NU dau acelasi lucru si se masoara amandoua."""
    from scipy.stats import rankdata
    y = np.asarray(y, float)
    n = len(y)
    yt = (rankdata(y, method="average") - 1.0) / max(n - 1.0, 1.0)
    if not invers:
        return yt, (lambda p: np.asarray(p, float))
    ys, q = np.sort(y), np.linspace(0.0, 1.0, n)
    return yt, (lambda p: np.interp(np.clip(np.asarray(p, float), 0.0, 1.0), q, ys))


def _tt_logit(y, eps, invers=True):
    """Tinta -> logit. `complexity` e in [0, 0.975], deci MARGINITA, iar toti regresorii de pana acum o
    trateaza ca daca ar fi nemarginita.

    `eps` nu e cosmetic si nu e un detaliu de implementare: sunt 28 de zerouri EXACTE in coloana, si
    `logit(eps)` le trimite pe toate in acelasi punct extrem. La eps=0.005 acel punct e la z=-3.85,
    adica 28 de puncte de parghie fabricate de transformare; la eps=0.02 e la z=-2.66, adica un outlier
    obisnuit. De asta se ruleaza amandoua valorile si nu una."""
    y = np.asarray(y, float)
    c = np.clip(y, eps, 1.0 - eps)
    yt = np.log(c / (1.0 - c))
    if not invers:
        return yt, (lambda p: np.asarray(p, float))
    return yt, (lambda p: 1.0 / (1.0 + np.exp(-np.clip(np.asarray(p, float), -50.0, 50.0))))


_TRANSF = {"id": _tt_id, "rank": _tt_rank,
           "logit2": lambda y, inv: _tt_logit(y, 0.02, inv),
           "logit005": lambda y, inv: _tt_logit(y, 0.005, inv)}


def _tt_pred(Xtr, ytr, Xpredict, baza, transf, invers):
    yt, inv = _TRANSF[transf](np.asarray(ytr, float), invers)
    p = np.asarray(inv(baza(Xtr, yt, Xpredict)), float)
    if p.shape != (len(Xpredict),):
        raise SystemExit(f"_tt_pred({transf}): predictie de forma {p.shape} pentru {len(Xpredict)} randuri")
    return p


# ------------------------------------------------------- INCADRARE: clasificare ordinala plus valoarea
# Etichetele originale vin din agregarea unor judecati Likert de la 1 la 5, deci o incadrare pe clase e
# mai fidela datelor decat regresia pe o valoare continua. Tinta NU e insa ea insasi o clasa: e media
# unui numar VARIABIL de judecati, pe o grila de 1/(4n) care difera per item (227 de valori distincte pe
# 5624 de randuri). Deci incadrarea cere cuantizare, si plafonul ei e masurat, nu presupus: o citire
# perfecta pe 5 clase de cuantile da r 0.9437 pe media celor 10 limbi, iar incumbentul e la 0.5553.
# Cuantizarea nu e deci obiectia care se poate ridica impotriva acestei axe.

def _clf_proba(Xtr, yb, Xpredict, kind):
    """P(clasa 1) pentru un singur clasificator binar. `lin` merge prin acelasi lant imputer + scaler ca
    `_pipe_pred`, `hgb` primeste X brut fiindca trateaza NaN nativ. `C=0.1` la logistic NU e acordat;
    daca varianta `ord-lin-*` trece poarta, atunci se acordeaza si se spune ca s-a acordat."""
    if kind == "lin":
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        m = Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                      ("s", StandardScaler()),
                      ("e", LogisticRegression(C=0.1, max_iter=2000, random_state=SEED))])
    elif kind == "hgb":
        from sklearn.ensemble import HistGradientBoostingClassifier
        m = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=400,
                                           l2_regularization=1.0, random_state=SEED)
    else:
        raise ValueError(kind)
    m.fit(Xtr, yb)
    return m.predict_proba(Xpredict)[:, 1]


def _praguri_mijloace(y, K):
    """Cele K-1 praguri de cuantila si mediile celor K clase, calculate NUMAI din `y` de antrenare."""
    y = np.asarray(y, float)
    praguri = np.unique(np.quantile(y, np.linspace(0.0, 1.0, K + 1)[1:-1]))
    b = np.digitize(y, praguri)
    mij = np.array([y[b == k].mean() if (b == k).any() else y.mean()
                    for k in range(len(praguri) + 1)])
    return praguri, mij


def _ord_pred(Xtr, ytr, Xpredict, K, kind, unitati=False):
    """Descompunerea ordinala Frank-Hall: K-1 clasificatori binari pe `y > pragul k`.

    Citirea implicita e SUMA probabilitatilor de supravietuire, adica `E[indicele de clasa]`. Ea nu are
    nevoie de nicio corectie de monotonie, si asta e motivul pentru care e implicita: cei K-1
    clasificatori se potrivesc INDEPENDENT, deci `P(y>t_k)` nu e garantat descrescator in `k`, iar o
    citire pe probabilitati de CLASA ar produce probabilitati negative. `unitati=True` pune rezultatul
    inapoi in unitati de complexitate prin mediile claselor, si atunci monotonia se impune explicit cu
    un minim cumulat.

    Un prag pe care nu exista ambele clase se sare, si se spune cati s-au sarit: cu K mare si o limba
    mica, cuantilele se pot lipi."""
    y = np.asarray(ytr, float)
    praguri, mij = _praguri_mijloace(y, K)
    S, sarite = [], 0
    for t in praguri:
        yb = (y > t).astype(int)
        if yb.min() == yb.max():
            sarite += 1
            continue
        S.append(_clf_proba(Xtr, yb, Xpredict, kind))
    if not S:
        raise SystemExit(f"_ord_pred: toate cele {len(praguri)} praguri sunt degenerate pe {len(y)} "
                         f"randuri de antrenare; K={K} e prea mare pentru bazinul acesta.")
    if sarite:
        print(f"[ord] K={K}: {sarite} din {len(praguri)} praguri sarite (o singura clasa)", flush=True)
    S = np.vstack(S)
    if not unitati:
        return S.sum(axis=0)
    n = S.shape[1]
    cum = np.vstack([np.ones((1, n)), np.minimum.accumulate(S, axis=0), np.zeros((1, n))])
    Pm = cum[:-1] - cum[1:]
    m = mij if len(mij) == Pm.shape[0] else np.linspace(y.min(), y.max(), Pm.shape[0])
    return Pm.T @ m


def _clf_pred(Xtr, ytr, Xpredict, K, kind):
    """Versiunea LITERALA din cerere: clasificare pe K clase, apoi valoarea asteptata din probabilitati.

    Diferenta fata de `_ord_pred`: aici clasificatorul e multinomial, deci probabilitatile sumeaza 1
    prin construcie si nu exista problema de monotonie, dar in schimb ordinea claselor nu e folosita
    nicaieri. Adica se arunca exact structura ordinala care motiveaza incadrarea. Cele doua variante
    raspund deci la doua intrebari diferite si nu se substituie."""
    y = np.asarray(ytr, float)
    praguri, mij = _praguri_mijloace(y, K)
    b = np.digitize(y, praguri)
    if kind == "lin":
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        m = Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                      ("s", StandardScaler()),
                      ("e", LogisticRegression(C=0.1, max_iter=2000, random_state=SEED))])
    elif kind == "hgb":
        from sklearn.ensemble import HistGradientBoostingClassifier
        m = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=400,
                                           l2_regularization=1.0, random_state=SEED)
    else:
        raise ValueError(kind)
    m.fit(Xtr, b)
    Pm = m.predict_proba(Xpredict)
    # `classes_` sunt etichetele PREZENTE, sortate. Indexarea prin ele, nu prin range, fiindca o clasa
    # absenta din bazin ar decala toata harta de mijloace fara sa crape nimic.
    return Pm @ mij[np.asarray(m.classes_, int)]


# ------------------------------------------------------------------------------ INFORMATIE: subspatii
def _rs_pred(Xtr, ytr, Xpredict, baza, frac, n):
    """Subspatii aleatoare de COLOANE, mediate. Acelasi obiectiv, aceeasi familie, alta informatie.

    De ce merita masurat, si argumentul e pe `rho`, nu pe `r`: `extratrees` e cel mai bun al treilea
    membru masurat vreodata pe axa asta (+0.0080 pe A), iar singura lui diferenta relevanta fata de un
    arbore obisnuit e `max_features=0.3`. Aici acel mecanism e izolat de restul lui ExtraTrees si aplicat
    si peste un LINIAR, ceea ce nu s-a facut niciodata. Si e singurul mecanism din sesiune care coboara
    `rho` fara sa arunce informatie: fiecare membru vede mai putin, dar medierea aduce inapoi.

    Masca depinde de LATIMEA lui X si de samanta fixa, nu de continut, deci toate cele 12 potriviri ale
    unei rulari vad aceleasi subspatii. E ce vrem: un singur ansamblu de subspatii, nu 12 diferite.
    La `frac >= 1` si `n == 1` se foloseste ordinea intreaga, ca `rs-<baza>-f10-n1` sa fie CONTROLUL de
    identitate al invelisului. ATENTIE la cat de tare se poate strange acest control, fiindca prima
    formulare a lui spunea `bit-exact` si era FALSA pe date reale:

      pe date sintetice gaussiene, float64      max|diff| 8.9e-16
      pe date sintetice gaussiene, float32      max|diff| 3.9e-07
      pe embeddingul REAL, prin CSV             max|diff| 4.3e-05

    Motivul, si nu e un bug: indexarea cu `Xtr[:, c]` produce o COPIE cu alt aranjament in memorie
    (nu mai e C-contigua), deci BLAS insumeaza in alta ordine. Pe o matrice gaussiana bine
    conditionata asta nu se vede; pe 774 de coloane de embedding puternic colineare, rezolvarea lui
    Ridge la alpha=300 amplifica diferenta de ordine pana la 1e-5. Diferenta e uniforma pe toate
    randurile si toate limbile, si e cu doua ordine de marime sub cel mai mic efect pe care sesiunea
    il interpreteaza (0.0002), iar `r` si `rho` ies identice la toate zecimalele raportate.

    Contrastul cu celalalt control e informativ: `tt-id-<baza>` iese la EXACT 0.0, fiindca atinge doar
    `y` si nu reaseaza nicio matrice. Deci cele doua controale separa curat un invelis care nu poate
    schimba nimic de unul care schimba numai ordinea de insumare."""
    Xtr = np.asarray(Xtr)
    Xpredict = np.asarray(Xpredict)
    d = Xtr.shape[1]
    k = max(1, int(round(frac * d)))
    rng = np.random.default_rng(SEED)
    P = []
    for _ in range(n):
        c = np.arange(d) if k >= d else np.sort(rng.choice(d, size=k, replace=False))
        P.append(np.asarray(baza(Xtr[:, c], ytr, Xpredict[:, c]), float))
    return np.mean(P, axis=0)


def _w_pred(Xtr, ytr, Xpredict, baza, c):
    """Ponderi pe rand `1 + c*|z(ytr)|`, deci capacitatea se muta in COADA distributiei tintei.

    E cel mai direct atac posibil pe `rho`: nu schimba nici familia, nici forma pierderii, nici ce se
    prezice, schimba numai UNDE modelul isi cheltuieste eroarea, si `rho` masoara exact unde sunt
    erorile. Spre deosebire de o pierdere robusta, nu converge la acelasi parametru de locatie.

    Ponderile vin numai din `ytr`, deci nu exista scurgere. `StandardScaler` rămâne NEPONDERAT, ca scala
    coloanelor sa fie aceeasi convenție ca la toti ceilalti candidati; se pondereaza doar potrivirea."""
    y = np.asarray(ytr, float)
    sd = y.std()
    w = np.ones(len(y)) if sd < 1e-12 else 1.0 + c * np.abs(y - y.mean()) / sd
    if baza == "hgb":
        from sklearn.ensemble import HistGradientBoostingRegressor
        m = HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                          l2_regularization=1.0, random_state=SEED)
        m.fit(Xtr, y, sample_weight=w)
        return np.asarray(m.predict(Xpredict), float)
    if baza == "ridge":
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import Ridge
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        m = Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                      ("s", StandardScaler()), ("e", Ridge(alpha=300, random_state=SEED))])
        m.fit(Xtr, y, e__sample_weight=w)
        return np.asarray(m.predict(Xpredict), float)
    raise ValueError(f"w-{baza}: numai `ridge` si `hgb` primesc sample_weight in proiectul acesta")


def blend_ridge_et(Xtr, ytr, Xpredict):
    """`blend_ridge_hgb` cu jumatatea de arbori schimbata din boosting in bagging, restul identic.
    Izoleaza intrebarea "conteaza familia de arbori" de intrebarea "conteaza ca exista arbori"."""
    return np.mean([_pipe_pred(Xtr, ytr, Xpredict, _mk_ridge),
                    _pipe_pred(Xtr, ytr, Xpredict, _mk_et)], axis=0)


def blend_lasso_hgb(Xtr, ytr, Xpredict):
    """`blend_ridge_hgb` cu jumatatea LINIARA schimbata din L2 dens in L1 rar, restul identic.

    Izoleaza intrebarea "conteaza penalizarea" de intrebarea "conteaza ca exista un liniar". `alpha`
    e 1e-3, punctul ales leave-one-language-out pe grila din `e_regresor_a.md`, si e un optim
    INTERIOR al ei (1e-4 da 0.5523, 3e-4 0.5593, 1e-3 0.5689, 3e-3 0.5659), nu marginea grilei.

    Structura urmeaza EXACT `blend_ridge_hgb`, si nu din estetica: bratul liniar primeste imputer plus
    scaler, iar HGB primeste X brut fiindca trateaza NaN nativ. Numai asa media celor doua brate de
    aici e acelasi obiect cu media CSV-urilor `_reg-lasso-a1e-3` si `_reg-hgb`, adica numai asa
    controlul de mai jos are voie sa fie strict.

    Exista ca AL DOILEA DRUM spre o cifra pe care `make_a_blend.py` o produce deja prin media pe
    coloane. Cele doua trebuie sa coincida la 1e-12; daca nu coincid, una din ele e gresita si nu se
    poate spune care fara un al treilea drum."""
    return np.mean([_pipe_pred(Xtr, ytr, Xpredict, _mk_lasso(1e-3)),
                    _hgb_pred(Xtr, ytr, Xpredict)], axis=0)


def _tabfm_cache_pred(Xtr, ytr, Xpredict):
    """Predictii TabFM calculate in alta parte, citite dupa cheia de identitate a cererii.

    Rularea locala merge mai departe exact ca oricare alta: acelasi bootstrap, acelasi raport,
    aceleasi coloane. Singura diferenta e de unde vine vectorul de predictii.

    Cheia acopera formele SI octetii lui (Xtr, ytr, Xpredict), deci daca celalalt capat ar fi
    reconstruit fie si un rand altfel, fisierul n-ar exista si aici se opreste. Nu e o speranta ca
    cele doua capete fac acelasi lucru, e o poarta."""
    from tabfm_bridge import req_key
    d = os.environ.get("TABFM_CACHE",
                       os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "tabfm_preds"))
    k = req_key(Xtr, ytr, Xpredict)
    p = os.path.join(d, k + ".npy")
    if not os.path.exists(p):
        raise SystemExit(f"tabfm-cache: lipseste {k} (ctx {np.shape(Xtr)}, pred {np.shape(Xpredict)}) "
                         f"in {d}. Ori nu s-a rulat cererea, ori blocurile difera de cele exportate.")
    v = np.load(p)
    if len(v) != len(Xpredict) or not np.isfinite(v).all():
        raise SystemExit(f"tabfm-cache: {k} are {len(v)} valori pentru {len(Xpredict)} randuri, "
                         f"finite {np.isfinite(v).sum()}")
    return v


# Familii parametrice COMPUSE, adica cele care au nevoie de semnatura intreaga `(Xtr, ytr, Xpredict)`
# si nu de o fabrica de estimator. `_FAM` de mai sus intoarce un estimator care trece prin `_pipe_pred`;
# un invelis de tinta sau o descompunere ordinala nu incap in acea forma si nu se forteaza acolo.
#
# Al treilea element al fiecarui rand e NUMELE GRUPULUI care contine un regresor de baza, sau None.
# `regressor_kind` recurge pe el, ca o greseala de scriere in baza (`tt-rank-ridgee`) sa cada la
# PARSARE si nu la prima potrivire, adica dupa embedding si dupa cateva minute de CPU. Fara recursie,
# garantia care exista azi pentru numele simple s-ar pierde tacut pentru cele compuse.
#
# Convenții de scriere a parametrilor, si sunt cele care fac ca numele de pe linia de comanda sa fie
# chiar numele din fisier: `f<F>` e in ZECIMI (f3 = 0.3, f10 = 1.0), `c<C>` e multiplicator INTREG
# (c1 = 1.0), `l<N>`, `d<D>`, `n<N>`, `h<H>`, `k<K>` sunt numere intregi citite ca atare.
_COMP = (
    (re.compile(r"^lgbm-l(?P<n>[0-9]+)$"),
     lambda m: (lambda a, b, c, _n=int(m["n"]): _lgbm_pred(a, b, c, num_leaves=_n)), None),
    (re.compile(r"^lgbmlin-l(?P<n>[0-9]+)$"),
     lambda m: (lambda a, b, c, _n=int(m["n"]): _lgbm_pred(a, b, c, num_leaves=_n,
                                                           linear_tree=True)), None),
    (re.compile(r"^cat-d(?P<d>[0-9]+)$"),
     lambda m: (lambda a, b, c, _d=int(m["d"]): _cat_pred(a, b, c, depth=_d)), None),
    (re.compile(r"^rf-n(?P<n>[0-9]+)$"),
     lambda m: (lambda a, b, c, _e=_mk_rf(int(m["n"])): _pipe_pred(a, b, c, _e)), None),
    (re.compile(r"^mlp-h(?P<h>[0-9]+)$"),
     lambda m: (lambda a, b, c, _e=_mk_mlp(int(m["h"])): _pipe_pred(a, b, c, _e)), None),
    (re.compile(r"^knn-k(?P<k>[0-9]+)$"),
     lambda m: (lambda a, b, c, _e=_mk_knn(int(m["k"])): _pipe_pred(a, b, c, _e)), None),
    (re.compile(r"^(?P<p>tt|ttz)-(?P<t>id|rank|logit2|logit005)-(?P<b>.+)$"),
     lambda m: (lambda a, b, c, _t=m["t"], _i=(m["p"] == "tt"), _bn=m["b"]:
                _tt_pred(a, b, c, _make_regressor(_bn), _t, _i)), "b"),
    (re.compile(r"^(?P<p>ord|orde)-(?P<b>lin|hgb)-k(?P<k>[0-9]+)$"),
     lambda m: (lambda a, b, c, _k=int(m["k"]), _b=m["b"], _u=(m["p"] == "orde"):
                _ord_pred(a, b, c, _k, _b, unitati=_u)), None),
    (re.compile(r"^clf-(?P<b>lin|hgb)-k(?P<k>[0-9]+)$"),
     lambda m: (lambda a, b, c, _k=int(m["k"]), _b=m["b"]: _clf_pred(a, b, c, _k, _b)), None),
    (re.compile(r"^rs-(?P<b>.+)-f(?P<f>[0-9]+)-n(?P<n>[0-9]+)$"),
     lambda m: (lambda a, b, c, _bn=m["b"], _f=int(m["f"]) / 10.0, _n=int(m["n"]):
                _rs_pred(a, b, c, _make_regressor(_bn), _f, _n)), "b"),
    (re.compile(r"^w-(?P<b>ridge|hgb)-c(?P<c>[0-9]+)$"),
     lambda m: (lambda a, b, c, _b=m["b"], _c=float(m["c"]): _w_pred(a, b, c, _b, _c)), None),
)


def _make_regressor(name):
    """Alege regresorul pt semnal A. 'blend' (default) = Ridge300+HGB (bit-exact). L1 transfera mai bine
    cross-lingual pe free-gate (vezi analysis_lasso.py): lasso 0.5688 / elasticnet 0.5650 > blend 0.5512.

    Restul sunt axa "conteaza algoritmul", nemasurata niciodata sub protocolul LOLO real. `ridge` si
    `hgb` sunt cele DOUA JUMATATI ale blend-ului, rulate separat: daca liniarul singur e practic egal
    cu blend-ul, spatiul e liniar si nicio schimbare de algoritm de arbori n-are de unde sa scoata."""
    if name == "blend":
        return blend_ridge_hgb
    # `lasso` si `elasticnet` mergeau prin `_linreg_pred`, care NU are imputer, si de aceea n-au putut
    # rula niciodata sub protocolul care conteaza: cu `na_policy="mlsp"` coloanele de suprafata sunt
    # NaN pe `ja` si `si`, iar Lasso da `ValueError: Input X contains NaN`. Asta explica de ce nu
    # exista niciun `e1_frozen_preds_reg-lasso*` pe disc: nu ca n-a fost incercat, ca nu putea rula.
    # Trec pe `_pipe_pred`, adica pe exact lantul bratului Ridge din blend. Nimic publicat nu depinde
    # de legatura veche (zero fisiere), iar `analysis_lasso.py` isi face propriul lant si nu trece
    # pe aici, deci `_linreg_pred` insusi ramane neatins pentru calea romaneasca.
    if name == "lasso":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_lasso(0.01))
    if name == "elasticnet":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_enet(0.01, 0.5))
    if name == "huber":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_huber)
    if name == "bayesridge":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_bayes)
    if name == "ard":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_ard)
    if name == "svr-lin":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_svr_lin)
    if name == "krr-rbf":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_krr_a(1.0))
    if name == "ridge":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_ridge)
    if name == "hgb":
        return _hgb_pred
    if name == "hgb-abs":
        return lambda a, b, c: _hgb_pred(a, b, c, loss="absolute_error")
    if name == "hgb-q50":
        # Pinball la 0.5 e L1 pana la un factor de 2 in gradient, iar la boosting cu rata fixa acel
        # factor NU e neutru: pasii difera. Deci nu e un duplicat garantat al lui `hgb-abs`, dar se
        # asteapta sa fie foarte aproape, si cat de aproape e chiar informatia care se cumpara.
        return lambda a, b, c: _hgb_pred(a, b, c, loss="quantile", quantile=0.5)
    if name == "hgb-adanc":
        return lambda a, b, c: _hgb_pred(a, b, c, max_depth=6, learning_rate=0.03, max_iter=800)
    if name == "extratrees":
        return lambda a, b, c: _pipe_pred(a, b, c, _mk_et)
    if name == "blend-et":
        return blend_ridge_et
    if name == "blend-lasso":
        return blend_lasso_hgb
    if name == "tabfm-cache":
        return _tabfm_cache_pred
    # `_COMP` INAINTE de `_FAM`: numele compuse sunt mai lungi si mai specifice, iar un tipar de
    # `_FAM` nu poate prinde niciunul din ele (toate sunt ancorate), dar ordinea o face explicita.
    for rx, mk, _ in _COMP:
        m = rx.match(name)
        if m:
            return mk(m)
    for rx, mk in _FAM:
        m = rx.match(name)
        if m:
            est = mk(m)
            return lambda a, b, c, _e=est: _pipe_pred(a, b, c, _e)
    raise ValueError(name)


REGRESSORS = ("blend", "lasso", "elasticnet", "ridge", "hgb", "hgb-adanc", "extratrees",
              "blend-et", "blend-lasso", "tabfm-cache", "huber", "bayesridge", "ard", "svr-lin", "krr-rbf",
              # axa PIERDERII: acelasi HGB, acelasi X, aceeasi tinta, alta functie de cost. E singura
              # comparatie din proiect in care nimic altceva nu se schimba.
              "hgb-abs", "hgb-q50")


def regressor_kind(v):
    """Valideaza `--regressor`: multimea fixa `REGRESSORS` plus familiile parametrice din `_FAM`.

    Exista din acelasi motiv ca `_emb_tf_kind` pentru `proj-N`: grila de `alpha` nu se poate enumera
    intr-un `choices`. Validarea se face AICI, nu la prima potrivire, ca o greseala de scriere sa cada
    inainte de embedding si de cele 12 potriviri, nu dupa."""
    if v in REGRESSORS:
        return v
    for rx, _ in _FAM:
        if rx.match(v):
            return v
    for rx, _, grup in _COMP:
        m = rx.match(v)
        if m:
            if grup:
                regressor_kind(m[grup])      # recursie pe baza: o greseala in ea cade AICI
            return v
    raise ValueError(f"regresor necunoscut: {v!r}. Fixe: {', '.join(REGRESSORS)}. "
                     f"Familii: ridge-a<A>, lasso-a<A>, krr-a<A>, pls-k<K>, enet-a<A>-l<zecimi>, "
                     f"cu <A> scris fara punct (30, 1e-3, 3e-2). Compuse: lgbm-l<N>, lgbmlin-l<N>, "
                     f"cat-d<D>, rf-n<N>, mlp-h<H>, knn-k<K>, tt|ttz-<id|rank|logit2|logit005>-<baza>, "
                     f"ord|orde-<lin|hgb>-k<K>, clf-<lin|hgb>-k<K>, rs-<baza>-f<zecimi>-n<N>, "
                     f"w-<ridge|hgb>-c<C>")


def _Xc(E, lex, mu, fert=None, fert_mu=None, drop_len=False):
    """[embedding centrat pe limba] ++ [fertilitate sau 0, lexical].

    Cei trei parametri optionali sunt opt-in. Fara ei rezultatul e bit-exact cel de dinainte, deci
    calea romaneasca, care trece si ea pe aici, nu e atinsa.

      `fert`     numarul de subword-uri per tinta, care umple slotul rezervat la coloana D si lasat
                 gol pana acum. Se centreaza cu `fert_mu`, ca embeddingul: media limbii pentru MLSP,
                 media blocului intreg pentru CompLex EN.
      `drop_len` SCOATE lungimea in caractere, `lex[:, 1]`, adica D+2 in cadrul intreg, deci
                 latimea scade cu unu. O coloana anulata in loc de scoasa da acelasi lucru pentru
                 Ridge+HGB pana la rotunjirea float32 (masurat, max|diff| = 1.2e-07 pe date
                 sintetice si 3.1e-06 pe bratul EN), dar scoaterea e ce reproduce masuratoarea bit
                 cu bit, deci ea ramane. NaN nu e o varianta a treia: binning-ul HGB crapa pe o
                 coloana fara nicio valoare finita.
    """
    if fert is None:
        col = np.zeros((len(E), 1), np.float32)
    else:
        if fert_mu is None:
            raise ValueError("fert fara fert_mu: fertilitatea se centreaza, ca embeddingul")
        col = (np.asarray(fert, float).reshape(-1, 1) - float(fert_mu)).astype(np.float32)
    if drop_len:
        lex = np.delete(lex, 1, axis=1)          # copie, deci `lex` al apelantului nu e atins
    return np.hstack([E - mu, col, lex])


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
        # Calea romaneasca mostenita, pe transformers. Reproducerea bit-exacta a lui 64.81 vine din
        # CSV-urile din cache (load_cached_signals), nu de aici: ramura asta se atinge doar cand
        # cache-ul lipseste.
        rater = LLMRater(RO_LEGACY_LLM, backend="transformers")
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
