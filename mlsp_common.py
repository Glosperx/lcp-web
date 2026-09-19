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
# "ro" e inclus: romana e alfabet latin, exact limba pe care tasaturile astea au fost scrise initial.
SURFACE_APPLICABLE = frozenset({"ca", "en", "fil", "fr", "de", "it", "pt", "es", "ro"})

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
    # `model_config` forteaza remaparea, si e opt-in DOAR pentru intrarea asta: aplicata global ar
    # schimba tacut arhitectura si altor modele. D.4 e testul care spune daca modelul asa incarcat
    # produce cifre valide sau doar nu crapa.
    "gemma4-12b-4bit": dict(repo="mlx-community/gemma-4-12B-it-qat-OptiQ-4bit",
                            revision="63912b888c04ba2c555f198685d10b05f54cf564",
                            backend="mlx", rol="robustete, checkpoint QAT",
                            model_config={"model_type": "gemma4"}),
    # Controlul de cuantizare pentru modelul lui B din sistem. ACELASI checkpoint QAT, alta
    # cuantizare, deci diferenta masurata e a cuantizarii si nu a modelului. Are nevoie de ACEEASI
    # remapare ca varianta de 4 biti: si el declara `model_type: gemma4_unified`. Prima versiune a
    # intrarii astea presupunea contrariul, dedus din config-ul altui repo Gemma 4, si incarcarea a
    # picat imediat cu `ValueError: Model type gemma4_unified not supported`. Se noteaza fiindca e
    # exact felul de presupunere care, daca n-ar crapa zgomotos, ar schimba tacit arhitectura.
    "gemma4-12b-8bit": dict(repo="mlx-community/gemma-4-12B-it-qat-8bit",
                            revision="eafed06893a6ee299315ebe0e0feb82f435e92fe",
                            backend="mlx", rol="control de cuantizare pentru semnalul B",
                            model_config={"model_type": "gemma4"}),
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


# Numele englez al limbii, pentru promptul multilingv al semnalului B. Inversul lui MLSP_LANGS, ca
# lista de limbi sa aiba o singura sursa. Toate cele 10 sunt cuvinte simple, deci `capitalize()` da
# forma corecta ("filipino" -> "Filipino", "sinhala" -> "Sinhala").
LANG_NAMES = {code: name.capitalize() for name, code in MLSP_LANGS.items()}
# Romana, adaugata separat de MLSP_LANGS: nu vine dintr-o coloana `language` de TSV MLSP, ci din
# load_rolcp(). Cerut explicit de coordonator (Sergiu) pe 29 aug 2026, ca a 11-a limba din grila
# LOLO, cu acelasi prompt multilingv in engleza ca celelalte 10 (nu prompturile vechi romanesti).
LANG_NAMES["ro"] = "Romanian"


def lang_name(code):
    """Numele englez al limbii, din codul ei. Exceptie la nemapare, ca la lang_code().

    `lang_name("ro")` intoarce acum "Romanian": romana a intrat in grila multilingva ca a 11-a
    limba. Calea veche, `lang=None` in `LLMRater.rate()`, ramane neatinsa si separata — foloseste
    inca prompturile romanesti originale, nu trece niciodata prin functia asta.
    """
    nm = LANG_NAMES.get(LANG_ALIASES.get(str(code), str(code)))
    if nm is None:
        raise ValueError(f"cod de limba fara nume englez: {code!r} (cunoscute: {sorted(LANG_NAMES)})")
    return nm


# ----------------------------------------------------------------------------- datele
ROLCP_TEST = os.path.join(DATA, "test_set.csv")
ROLCP_CSV = os.environ.get("ROLCP_CSV", os.path.join(DATA, "RoLCP.csv"))


def load_rolcp():
    """RoLCP (RALS, Anghel et al. 2025), in aceeasi schema cu `load_mlsp`: lang, sent, token,
    complexity, split, context_id. Cerut de coordonator pe 29 aug 2026, ca a 11-a limba din grila
    LOLO, langa cele 10 MLSP.

    Test-only: RoLCP n-are un split de trial separat. Nu e o gaura, fiindca configuratia adoptata
    (`--fit test --pick-split test` in `fuse_ab.py`) deja potriveste ponderea si alege modelul pe
    randurile de TEST ale celorlalte limbi, niciodata pe trial, deci romana nu are nevoie de unul.

    Join in doi pasi, IDENTIC cu `score_rolcp.py` (care il valideaza separat la 1587/1587): intai
    cheia completa (text_name, token, text), apoi perechea unica (text_name, token), cu media la
    ambiguitate. Etichetele nu se tiparesc niciodata per-item de aici: `data/RoLCP.csv` e protejat
    cu parola tocmai ca sa nu ajunga per-item intr-un context de LLM, si regula se respecta si aici.
    """
    if not os.path.exists(ROLCP_TEST):
        raise FileNotFoundError(f"{ROLCP_TEST} lipseste")
    if not os.path.exists(ROLCP_CSV):
        raise FileNotFoundError(
            f"{ROLCP_CSV} lipseste. Descarca din github.com/senisioi/RALS (data.zip, parola in "
            "README-ul lor) si pune-l la calea de mai sus, sau seteaza ROLCP_CSV.")

    test = pd.read_csv(ROLCP_TEST, dtype=str, keep_default_na=False)
    need = {"datapointID", "text_name", "token", "text"}
    if not need.issubset(test.columns):
        raise ValueError(f"{ROLCP_TEST}: lipsesc coloanele {sorted(need - set(test.columns))}")

    gold = pd.read_csv(ROLCP_CSV, dtype=str, keep_default_na=False)
    gold = gold[gold["complexity"].str.strip() != ""].copy()
    gold["complexity"] = gold["complexity"].astype(float)
    by_full, by_pair = {}, {}
    for r in gold.itertuples():
        by_full[(r.text_name, r.token, r.text)] = r.complexity
        by_pair.setdefault((r.text_name, r.token), []).append(r.complexity)

    rows = []
    for r in test.itertuples():
        v = by_full.get((r.text_name, r.token, r.text))
        if v is None:
            cand = by_pair.get((r.text_name, r.token), [])
            if len(cand) == 1:
                v = cand[0]
            elif len(cand) > 1:
                v = sum(cand) / len(cand)
            else:
                continue
        rows.append((r.text, r.token, v))
    if len(rows) != len(test):
        raise SystemExit(f"load_rolcp: {len(rows)}/{len(test)} randuri gasite in gold, asteptat "
                         f"{len(test)}/{len(test)} ca in score_rolcp.py")

    d = pd.DataFrame(rows, columns=["sent", "token", "complexity"])
    d["lang"] = "ro"
    d["split"] = "test"
    d["context_id"] = "ro|" + d["sent"].astype(str)
    return d[["lang", "sent", "token", "complexity", "split", "context_id"]]


def load_mlsp(split="test", drop_multiword=False, include_ro=False):
    """Instantele MLSP per limba. Tipar explicit, All/ exclus, split marcat.

    Fara excluderea lui All/ si fara filtrul pe `lcp_labels` fiecare instanta s-ar numara de PATRU ori:
    lcp + combined, per limba si in All/.

    `drop_multiword` e implicit False, spre deosebire de codul vechi. Cele 8 tinte cu spatiu, toate
    italiene, raman in set: `find_char_span` le gaseste, `embed_frame` face pool peste subword-urile
    lor, iar n per limba trebuie sa coincida cu setul oficial (it=570) ca sa fie comparabil cu
    tabelele publicate.

    `include_ro`, implicit False: adauga RoLCP (`load_rolcp()`) ca a 11-a limba, numai pe splitul de
    test (RoLCP n-are trial). Implicit False peste tot, ca niciun apel existent sa nu se schimbe fara
    sa ceara explicit — cifrele publicate pe cele 10 limbi raman reproductibile bit cu bit.

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
    if include_ro and split == "test":
        ml = pd.concat([ml, load_rolcp()], ignore_index=True)
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


# A DOUA sursa de frecventa, pentru limbile de coada pe care `wordfreq` nu le acopera. Registrul e
# GOL implicit, deci `zipf_safe` se comporta bit cu bit ca inainte pana cand cineva cheama
# `load_tail_freq()` explicit. Tabelele se construiesc cu `build_freq_tail.py`.
TAIL_FREQ = {}
_TAIL_TK = {}
MIN_PREFIX = 4

# Diversitatea contextuala, din `build_ctx_div.py`. Gol implicit, deci nicio cifra publicata nu trece
# prin ramura asta pana cand cineva cheama `load_ctx_div()`.
CTX_DIV = {}


def load_ctx_div(langs=None):
    """Inregistreaza tabelele din `data/ctx_div/` ca sursa pentru `ctx_div_safe`. -> {limba: n tipuri}

    Spre deosebire de `TAIL_FREQ`, care umple GAURILE lasate de `wordfreq`, tabelul asta e o sursa
    de sine statatoare pentru TOATE cele zece limbi: se calculeaza din corpus, cu acelasi tokenizer
    peste tot, deci nu mosteneste nici gaurile lui `wordfreq`, nici dependenta lui de MeCab pentru
    japoneza.
    """
    import glob
    import os as _os
    import pandas as _pd
    fis = {"ca": "ca", "de": "de", "en": "en", "es": "es", "fr": "fr",
           "it": "it", "ja": "ja", "pt": "pt", "si": "si", "fil": "tl"}
    for lg in (langs or list(fis)):
        p = _os.path.join(DATA, "ctx_div", f"{fis[lg]}.csv.gz")
        if not _os.path.exists(p):
            raise SystemExit(f"{p} lipseste. Ruleaza intai build_ctx_div.py")
        d = _pd.read_csv(p)
        CTX_DIV[lg] = dict(zip(d["word"].astype(str), d["cd"].astype(float)))
    return {k: len(v) for k, v in CTX_DIV.items()}


def ctx_div_safe(tok, lg):
    """-> (cd, disponibil). Aceeasi forma ca `zipf_safe`, ca sa fie interschimbabile in `lexical`.

    Un cuvant negasit primeste 0 cu `disponibil = True`, exact conventia lui `zipf_safe` pentru o
    limba servita: 0 inseamna "nu apare in corpus", care e informatie adevarata, nu lipsa de sursa.
    `disponibil = False` numai cand limba n-are deloc tabel.
    """
    lg = LANG_ALIASES.get(str(lg), str(lg))
    if lg not in CTX_DIV:
        return 0.0, False
    return float(CTX_DIV[lg].get(str(tok).strip().lower(), 0.0)), True


def load_tail_freq(mode="exact", langs=("si", "fil")):
    """Inregistreaza tabelele din `data/freq_tail/` ca sursa suplimentara pentru `zipf_safe`.

    `mode` spune cat de departe merge cautarea cand forma exacta lipseste:
      exact    numai forma exacta;
      prefix   plus cel mai lung PREFIX de cel putin MIN_PREFIX caractere care e cuvant in tabel.
               Motivat tipologic pentru sinhaleza, care e aglutinanta si sufixeaza; pentru tagalog,
               care foloseste infixe si reduplicare, motivatia e mai slaba si se declara ca atare;
      subword  plus primul subword al tokenizerului XLM-R, adica o segmentare invatata, uniforma
               peste limbi si fara nicio presupunere tipologica.

    Sursa NU inlocuieste `wordfreq` acolo unde el raspunde: se consulta doar cand el da 0, deci e
    umplere de goluri, nu schimbare de scara pe valorile existente.
    """
    import glob
    import os as _os
    import pandas as _pd
    fis = {"si": "si", "fil": "tl"}
    for lg in langs:
        p = _os.path.join(DATA, "freq_tail", f"{fis[lg]}.csv.gz")
        if not _os.path.exists(p):
            raise SystemExit(f"{p} lipseste. Ruleaza intai build_freq_tail.py")
        d = _pd.read_csv(p)
        TAIL_FREQ[lg] = {"tab": dict(zip(d["word"].astype(str), d["zipf"].astype(float))),
                         "mode": mode}
    return {k: len(v["tab"]) for k, v in TAIL_FREQ.items()}


def _tail_lookup(ent, t):
    """-> zipf sau None. Trepte, in ordine, oprindu-se la prima care raspunde."""
    tab, mode = ent["tab"], ent["mode"]
    if t in tab:
        return tab[t]
    if mode in ("prefix", "subword"):
        for k in range(len(t) - 1, MIN_PREFIX - 1, -1):
            if t[:k] in tab:
                return tab[t[:k]]
    if mode == "subword":
        if "xlmr" not in _TAIL_TK:
            from transformers import AutoTokenizer
            _TAIL_TK["xlmr"] = AutoTokenizer.from_pretrained("xlm-roberta-base")
        sub = _TAIL_TK["xlmr"].tokenize(" " + t)
        s0 = sub[0].replace("\u2581", "") if sub else ""
        if s0 and s0 in tab:
            return tab[s0]
    return None


def zipf_safe(tok, lg):
    """-> (zipf, disponibil). `disponibil` e o proprietate a LIMBII, nu a tokenului.

    O garda scrisa ca "zipf == 0 deci indisponibil" ar fi gresita: ar marca si cuvintele rare real
    acoperite din celelalte 9 limbi. Un cuvant negasit intr-o limba acoperita are frecventa 0 si
    disponibil=True, ceea ce e informatie adevarata.

    Cand limba are un tabel in `TAIL_FREQ`, el se consulta NUMAI acolo unde `wordfreq` da 0, si
    atunci `disponibil` devine True: limba are acum o sursa proprie, deci un 0 inseamna "rar real",
    exact ca la celelalte noua. Cu registrul gol, functia e bit cu bit cea de dinainte.
    """
    lg = LANG_ALIASES.get(str(lg), str(lg))
    t = str(tok).strip().lower()
    base_ok = freq_available(lg)
    z = 0.0
    if base_ok:
        from wordfreq import zipf_frequency
        z = zipf_frequency(t, lg) if t else 0.0
    if z == 0.0 and lg in TAIL_FREQ:
        zt = _tail_lookup(TAIL_FREQ[lg], t)
        if zt is not None:
            return zt, True
    if base_ok:
        return z, True
    return (0.0, True) if lg in TAIL_FREQ else (0.0, False)


def surface_applicable(lg):
    """True daca trasaturile de suprafata latine au sens pe limba data."""
    return LANG_ALIASES.get(str(lg), str(lg)) in SURFACE_APPLICABLE


# ----------------------------------------------------------------------------- intervale pentru r
def boot_r_ci(y, p, groups, n_boot=2000, seed=42, alpha=0.05):
    """Interval pentru un r singur, prin reesantionarea CONTEXTELOR, nu a itemilor (§10.3).

    Sapte limbi din zece au in medie 3 tinte per context, deci itemii nu sunt independenti: un
    bootstrap pe itemi ar da intervale prea inguste exact acolo. `groups` sunt `context_id`-urile.

    Acelasi mecanism ca `finetune_xlmr._boot_delta`, dar pentru un r, nu pentru un Δ. Inlocuieste
    pragul Fisher la etapa 2; pe trial, la n = 30 si cu 20-30 de contexte, Fisher ramane singurul
    lucru rezonabil.

    -> dict(r, lo, hi, se, n, n_ctx, n_boot_ok). `boot` intoarce si esantioanele, ca sa se poata
    construi diferente PERECHE fara a mai reesantiona o data.
    """
    import numpy as np
    from scipy.stats import pearsonr
    y = np.asarray(y, float); p = np.asarray(p, float)
    m = np.isfinite(y) & np.isfinite(p)
    y, p, g = y[m], p[m], np.asarray(groups)[m]
    codes = pd.factorize(g)[0]
    idx_by_g = [np.flatnonzero(codes == k) for k in range(codes.max() + 1)] if len(codes) else []
    G = len(idx_by_g)
    if G < 3 or len(y) < 5 or np.std(y) == 0 or np.std(p) == 0:
        return dict(r=float("nan"), lo=float("nan"), hi=float("nan"), se=float("nan"),
                    n=int(len(y)), n_ctx=G, n_boot_ok=0, boot=np.array([]))
    rng = np.random.default_rng(seed)
    rs = []
    for _ in range(n_boot):
        sel = np.concatenate([idx_by_g[k] for k in rng.integers(0, G, G)])
        if np.unique(y[sel]).size < 2 or np.unique(p[sel]).size < 2:
            continue
        rs.append(float(pearsonr(p[sel], y[sel])[0]))
    rs = np.asarray(rs, float)
    return dict(r=float(pearsonr(p, y)[0]), lo=float(np.percentile(rs, 100 * alpha / 2)),
                hi=float(np.percentile(rs, 100 * (1 - alpha / 2))), se=float(rs.std(ddof=1)),
                n=int(len(y)), n_ctx=G, n_boot_ok=int(len(rs)), boot=rs)
