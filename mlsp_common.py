"""Sursa unica pentru calea multilingva MLSP: maparea limbii, incarcarea datelor, garda de frecventa.

Absoarbe functiile deja scrise corect in measure_fertility.py si le pune intr-un singur loc, fiindca
azi patru fisiere fac acelasi lucru in patru feluri divergente (solution_bert.py, recompute_gpu.py,
finetune_xlmr.py, measure_fertility.py).

Ce NU face: nu atinge calea veche, romaneasca. `solution_bert._load_mlsp` si `recompute_gpu._load_mlsp`
raman pe data/mlsp/ cu cele 5 fisiere romanice, ca reproducerea bit-exacta a lui 64.81 sa se pastreze.
Modulul asta serveste doar experimentele multilingve noi.
"""
import glob
import os
import urllib.request

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# Cele 10 limbi MLSP, mapate din coloana `language` a TSV-ului. Eroare la nemapare, nu fallback tacut:
# maparea veche cu 5 intrari producea NaN pentru ja/si/de/en/fil, iar fallback-ul de dupa le trimitea
# tacut pe frecventa engleza.
MLSP_LANGS = {"catalan": "ca", "english": "en", "filipino": "fil", "french": "fr",
              "german": "de", "italian": "it", "japanese": "ja", "portuguese": "pt",
              "sinhala": "si", "spanish": "es"}

# Alias explicit. wordfreq rezolva singur `tl` catre `fil`, dar prin acelasi mecanism de "nearest
# match" care trimite sinhaleza pe engleza. Normalizam noi, ca sa nu depindem de el.
LANG_ALIASES = {"tl": "fil", "tgl": "fil", "fil": "fil"}

# Limbile unde silabele, sirul de consoane, raportul de vocale si majuscula au sens. VOWELS din
# solution_bert.py:55 e un set latin, deci pe kana, kanji si sinhaleza cele patru trasaturi nu masoara
# nimic. Nu devin zero (ar fi o valoare inventata), devin NaN plus coloana indicator.
SURFACE_APPLICABLE = frozenset({"ca", "en", "fil", "fr", "de", "it", "pt", "es"})

COMPLEX_EN_BASE = "https://raw.githubusercontent.com/MMU-TDMLab/CompLex/master"
COMPLEX_EN_FILES = {"train": "train/lcp_single_train.tsv",
                    "trial": "trial/lcp_single_trial.tsv",
                    "test": "test-labels/lcp_single_test.tsv"}

# ----------------------------------------------------------------------------- bazinul de LLM-uri
# Bazinul de bake-off pentru semnalele B (nota) si C (surprisal). `revision` se trece la FIECARE
# incarcare: un `main` mutat schimba greutatile, deci cifrele, in tacere.
#
# SHA-urile sunt aceleasi cu cele din download_pool.py (POOL + CONTROL_8BIT), reconfirmate pe
# 16 august (planul de bake-off, §12.4). Cele doua liste TREBUIE sa ramana identice; verificarea
# e in d4_sanity.py --check-pool. De unificat cand download_pool.py se mai atinge o data.
#
# Toate sunt MLX: bitsandbytes NF4 e CUDA-only, iar Mac-ul nu are CUDA. Perechile 4bit/8bit ale lui
# Qwen3-8B si Qwen3.5-9B sunt controlul de cuantizare (E.4), de aceea stau in acelasi tabel.
LLM_POOL = {
    "qwen3-8b-4bit": dict(repo="mlx-community/Qwen3-8B-4bit",
                          revision="545dc4251c05440727734bcd94334791f6ab0192",
                          backend="mlx", rol="brat universal principal"),
    "qwen3-8b-8bit": dict(repo="mlx-community/Qwen3-8B-8bit",
                          revision="48a0b75b1ae72503e21e1558d040bc227510ff06",
                          backend="mlx", rol="control de cuantizare"),
    "qwen35-9b-4bit": dict(repo="mlx-community/Qwen3.5-9B-MLX-4bit",
                           revision="938d8919941c6e7efd3c7150eff7fe9d12afa631",
                           backend="mlx", rol="robustete"),
    "qwen35-9b-8bit": dict(repo="mlx-community/Qwen3.5-9B-MLX-8bit",
                           revision="84f7c2deea248d8df56240f88102def51c7ed5d6",
                           backend="mlx", rol="control de cuantizare"),
    # ATENTIE: config.json declara model_type "gemma4_unified", iar mlx_lm 0.31.3 livreaza doar
    # gemma4/gemma4_text si nu are intrare in MODEL_REMAPPING => load() ridica ValueError.
    # Neverificat: ocolirea prin model_config={"model_type": "gemma4"}. Blocheaza Bloc E, nu Bloc D.
    "gemma4-12b-4bit": dict(repo="mlx-community/gemma-4-12B-it-qat-OptiQ-4bit",
                            revision="63912b888c04ba2c555f198685d10b05f54cf564",
                            backend="mlx", rol="robustete, checkpoint QAT"),
    "llama31-8b-4bit": dict(repo="mlx-community/Meta-Llama-3.1-8B-Instruct-4bit",
                            revision="241a666dad6cb93c8ff213d39a7f34a36bf26db4",
                            backend="mlx", rol="referinta"),
    "aya-expanse-8b-4bit": dict(repo="mlx-community/aya-expanse-8b-4bit",
                                revision="3a7cee37dd4ab4ed76642f61f6253da4748e63ba",
                                backend="mlx", rol="brat universal"),
}


def llm_entry(model):
    """Intrarea din LLM_POOL pentru o cheie, sau None daca `model` e un repo id brut."""
    return LLM_POOL.get(str(model))


# ----------------------------------------------------------------------------- maparea limbii
def lang_code(name):
    """Codul de limba din coloana `language`. Ridica exceptie la nemapare, fara fallback."""
    lg = MLSP_LANGS.get(str(name).strip().lower())
    if lg is None:
        raise ValueError(f"limba MLSP nemapata: {name!r}")
    return lg


# ----------------------------------------------------------------------------- datele
def load_mlsp(split="test", drop_multiword=False):
    """Instantele MLSP per limba. Tipar explicit, All/ exclus, split marcat.

    Fara excluderea lui All/ si fara filtrul pe `lcp_labels` fiecare instanta s-ar numara de PATRU ori:
    lcp + combined, per limba si in All/.

    `drop_multiword` e implicit False, spre deosebire de codul vechi. Cele 8 tinte cu spatiu, toate
    italiene, raman in set: `find_char_span` le gaseste, `embed_frame` face pool peste subword-urile
    lor, iar n per limba trebuie sa coincida cu setul oficial (it=570) ca sa fie comparabil cu
    tabelele publicate.

    Coloane intoarse: lang, sent, token, complexity, split, context_id.
    `context_id` e unitatea de reesantionare pentru bootstrap: sapte limbi din zece au in medie 3 tinte
    per context, deci itemii nu sunt independenti.
    """
    pat = os.path.join(DATA, "mlsp_full", "*", f"multils_{split}_*_lcp_labels.tsv")
    rows = []
    for f in sorted(glob.glob(pat)):
        if os.sep + "All" + os.sep in f:
            continue
        x = pd.read_csv(f, sep="\t")
        missing = {"language", "context", "target", "complexity"} - set(x.columns)
        if missing:
            raise ValueError(f"{f}: lipsesc coloanele {sorted(missing)}")
        x["lang"] = [lang_code(v) for v in x["language"]]
        x = x.rename(columns={"context": "sent", "target": "token"})
        x["split"] = split
        rows.append(x[["lang", "sent", "token", "complexity", "split"]])
    if not rows:
        raise FileNotFoundError(f"niciun fisier pentru tiparul {pat}")

    ml = pd.concat(rows, ignore_index=True)
    if drop_multiword:
        ml = ml[~ml["token"].astype(str).str.contains(" ", na=False)]
    ml = ml.dropna(subset=["sent", "token", "complexity"]).reset_index(drop=True)
    ml["context_id"] = ml["lang"].astype(str) + "|" + ml["sent"].astype(str)
    return ml


def ensure_complex_en():
    """CompLex EN (SemEval-2021), descarcat daca lipseste. -> DataFrame [sent, token, complexity].

    Descarcarea exista deja in baseline_surface.py:71 si recompute_gpu.py:168, dar NU in
    finetune_xlmr.py:46, care doar citeste. De aceea --frozenmulti crapa cu FileNotFoundError inainte
    de orice altceva pe o masina fara data/complex_en/.
    """
    d = os.path.join(DATA, "complex_en")
    os.makedirs(d, exist_ok=True)
    parts = []
    for k, rel in COMPLEX_EN_FILES.items():
        p = os.path.join(d, f"lcp_single_{k}.tsv")
        if not os.path.exists(p):
            urllib.request.urlretrieve(f"{COMPLEX_EN_BASE}/{rel}", p)
        parts.append(pd.read_csv(p, sep="\t").dropna(subset=["sentence", "token", "complexity"]))
    en = pd.concat(parts, ignore_index=True)
    return en.rename(columns={"sentence": "sent"})[["sent", "token", "complexity"]]


# ----------------------------------------------------------------------------- garda de frecventa
_PROBED = {}


def freq_available(lg):
    """Serveste wordfreq REAL limba asta? Masurat, nu declarat. Memoizat per limba.

    Doua motive pentru care nu e destul `available_languages()` singur:
      1. `si` nu e in lista, iar wordfreq nu ridica eroare, ci face substitutie tacuta catre `en`
         ("Using the nearest match"). Pe cele 600 de tinte sinhaleze rezultatul e zero doar fiindca
         niciun cuvant sinhalez nu apare in lista engleza; un imprumut latin ar primi o frecventa
         englezeasca reala, adica activ gresita.
      2. `ja` E in lista, dar apelul crapa cu ModuleNotFoundError daca lipseste MeCab. Lista nu stie
         de tokenizatoarele externe.
    De aceea limba e si probata cu un apel real, prins in try/except. Proba e lenesa, per limba, ca sa
    nu incarce zeci de liste de frecvente la import.
    """
    lg = LANG_ALIASES.get(str(lg), str(lg))
    if lg in _PROBED:
        return _PROBED[lg]
    from wordfreq import available_languages, zipf_frequency
    ok = lg in set(available_languages())
    if ok:
        try:
            zipf_frequency("a", lg)
        except Exception:
            ok = False
    _PROBED[lg] = ok
    return ok


def freq_langs(langs=None):
    """Submultimea acoperita real, pentru raportare. Implicit cele 10 limbi MLSP plus romana."""
    langs = langs or (set(MLSP_LANGS.values()) | {"ro"})
    return frozenset(lg for lg in langs if freq_available(lg))


def zipf_safe(tok, lg):
    """-> (zipf, disponibil). `disponibil` e o proprietate a LIMBII, nu a tokenului.

    O garda scrisa ca "zipf == 0 deci indisponibil" ar fi gresita: ar marca si cuvintele rare real
    acoperite din celelalte 9 limbi. Un cuvant negasit intr-o limba acoperita are frecventa 0 si
    disponibil=True, ceea ce e informatie adevarata.
    """
    lg = LANG_ALIASES.get(str(lg), str(lg))
    if not freq_available(lg):
        return 0.0, False
    from wordfreq import zipf_frequency
    t = str(tok).strip().lower()
    return (zipf_frequency(t, lg) if t else 0.0), True


def surface_applicable(lg):
    """True daca trasaturile de suprafata latine au sens pe limba data."""
    return LANG_ALIASES.get(str(lg), str(lg)) in SURFACE_APPLICABLE
