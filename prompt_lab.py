"""E.10: optimizarea promptului pentru semnalul B, pe cele 300 de instante de trial.

Variantele, si ce intreaba fiecare:

  v0_zeroshot  cele doua prompturi din bake-off, mediate. E baseline-ul, r = 0.565 pe qwen3-8b-4bit.
  v1_learner   acelasi prompt, dar rolul e "intermediate learner of {lang}", nu "expert in {lang}
               linguistics". Precedent publicat: ablatia G-Eval da R² 0.498 cu rol si limba fata de
               0.360 fara. Eticheta MLSP masoara dificultatea pentru un cititor obisnuit, deci rolul
               de expert e nealiniat cu constructul masurat.
  v2_rubrica   factorii numiti explicit: frecventa, lungime si silabe, termen tehnic, morfologie.
  v3_fewshot   k exemple ETICHETATE din trial-ul CELORLALTE 9 limbi. Zero-label in limba tinta se
               pastreaza, fiindca L nu apare niciodata printre exemple.
  v4_cot       genereaza o analiza scurta, apoi citeste P(1..5). Wei et al. 2022.
  v5_cot_sc    k rationale esantionate cu temperatura, scorurile mediate. Wang et al. 2022.
  v6_ansamblu  media lui v0, v1, v2. Nu costa niciun forward in plus, se calculeaza la agregare.

**Ce nu poate face few-shot-ul aici, si trebuie stiut inainte de a interpreta rezultatul.** Pearson e
invariant la orice functie liniara cu panta pozitiva, deci calibrarea scalei, care e beneficiul
principal al exemplelor etichetate, e invizibila in metrica noastra. Ablatia publicata o arata direct:
G-Eval fata de G-Scale, adica fara fata de cu cele 30 de etichete tinta, difera cu **+0.012 in
Pearson**, desi in R² diferenta era de la -0.499 la +0.293. Deci de la v3 se asteapta putin, iar daca
iese mult, prima ipoteza e ca exemplele schimba ORDINEA, nu scala.

**Selectia variantei e si ea o forma de tuning**, exact ca alegerea modelului din §5.1. Daca varianta
se alege pe trial-ul tuturor celor 10 limbi, atunci pentru fiecare limba tinuta deoparte i-am folosit
trial-ul ca sa aleg promptul. De aceea agregarea face selectie leave-one-language-out si peste
variante, nu doar peste modele.

Rulare:
  python prompt_lab.py --model qwen3-8b-4bit --variants v0_zeroshot,v1_learner,v2_rubrica,v3_fewshot
  python prompt_lab.py --model qwen3-8b-4bit --variants v4_cot --limit 20
  python prompt_lab.py --aggregate
  python prompt_lab.py --model gemma4-12b-4bit --variants v3_fewshot --split test

**`--split test` si de ce exemplele rams pe trial.** Splitul schimba DOAR instantele de notat.
Exemplele few-shot vin intotdeauna din trial-ul celorlalte limbi, fiindca ele poarta etichete: luate
din test ar pune etichete de test in prompt si ar invalida orice cifra de test. `measure` cheama de
aceea `load_mlsp("trial")` literal pentru `lolo_shots`, si `load_mlsp(split)` pentru instantele notate.
Consecinta buna: cele 6 exemple ale unei limbi sunt ACELEASI pe trial si pe test, deci configuratia e
fixa, nu reesantionata.

Fisierele nu se amesteca: trial scrie pe calea canonica `output/promptlab_<model>.csv`, orice alt split
in `output/promptlab_<split>/<model>.csv`. Vezi `csv_path`.
"""
import argparse
import csv
import glob
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from solution_bert import LLMRater, SEED                     # noqa: E402
from bakeoff_trial import dist_cols                          # noqa: E402

OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e10_prompt.md")
# Cele sase coloane istorice, plus distributiile la coada. `score` singur nu e destul: fara
# distributia peste cifre nu se poate aplica temperatura, iar temperatura valoreaza +0.0089 pe test,
# deci o comparatie intre o varianta de prompt fara temperatura si sistemul CU temperatura ar masura
# temperatura, nu promptul. Numele si idiomul sunt cele din `bakeoff_trial`, ca fisierele sa se poata
# citi cu acelasi cod.
BASE_COLS = ["lang", "token", "complexity", "variant", "score", "sec"]
COLS = BASE_COLS + dist_cols()
K_SHOTS = 6            # exemple few-shot, din celelalte 9 limbi
COT_TOKENS = 70        # buget de generare pentru analiza; peste atat nu e "scurt"
COT_SC_K = 5           # esantioane de self-consistency

# Sabloanele. {lang} e numele englez al limbii tintei, {tok} tinta, {sent} contextul.
P_EXPERT = ("You are an expert in {lang} linguistics. On a scale of 1-5 (1=very familiar, 2=simple, "
            "3=neutral, 4=difficult, 5=very difficult), how complex or difficult is the {lang} word "
            "\"{tok}\" for an average reader, in the sentence:\n\"{sent}\"\n"
            "Answer with ONLY a single digit from 1 to 5.")
P_SHORT = ("In the {lang} sentence: \"{sent}\"\nRate the lexical difficulty of the word \"{tok}\" "
           "on a scale from 1 (very familiar) to 5 (very difficult). Answer with only the digit.")
P_LEARNER = ("You are an intermediate learner of {lang}. On a scale of 1-5 (1=very familiar, "
             "2=simple, 3=neutral, 4=difficult, 5=very difficult), how complex or difficult is the "
             "{lang} word \"{tok}\" for you, in the sentence:\n\"{sent}\"\n"
             "Answer with ONLY a single digit from 1 to 5.")
P_RUBRIC = ("Rate how difficult the {lang} word \"{tok}\" is for an average reader, in the sentence:"
            "\n\"{sent}\"\nConsider its frequency of use, its length in syllables, whether it is a "
            "technical or specialized term, and its morphological complexity. On a scale of 1 (very "
            "familiar) to 5 (very difficult), answer with ONLY a single digit.")
COT_ASK = ("In the {lang} sentence: \"{sent}\"\nBriefly analyze what makes the word \"{tok}\" easy or "
           "difficult for an average reader: its frequency of use, its length in syllables, whether "
           "it is a technical or specialized term, and its morphological complexity. At most two "
           "sentences. Do NOT give a score yet.")
COT_SCORE = ("Based on your analysis, on a scale of 1 (very familiar) to 5 (very difficult), answer "
             "with ONLY a single digit.")
FEWSHOT_HEAD = ("Rate the lexical difficulty of a word in context, on a scale of 1 (very familiar) to "
                "5 (very difficult).\nExamples:\n{ex}\n\nNow rate the {lang} word \"{tok}\" in the "
                "sentence:\n\"{sent}\"\nAnswer with ONLY a single digit from 1 to 5.")
# Reformularea ca PROPORTIE, nu ca nota. Cifra cerută e un numar de cititori din cinci, deci o cantitate
# gradata prin natura ei: un model care raspunde despre proportii are motiv intern sa imprastie masa
# peste cifre, iar imprastierea corelata cu dificultatea e exact ce citeste semnalul B. Scala rămâne
# 1..5 fiindca citirea soft e legata de id-urile cifrelor "1".."5".
P_PROPORTIE = ("Out of five average readers of {lang}, how many would find the word \"{tok}\" hard to "
               "understand in this sentence?\n\"{sent}\"\nAnswer with ONLY a single digit from 1 to 5, "
               "where 1 means almost none of them and 5 means all of them.")
# Tinta marcata inline, nu doar citata separat. Pe japoneza si sinhaleza, unde tokenizarea e oricum
# problema, gasirea tintei in context nu e gratuita pentru model.
P_MARCAT = ("In the {lang} sentence below, the target word is marked with «».\n\"{marked}\"\n"
            "On a scale of 1 (very familiar) to 5 (very difficult), how difficult is «{tok}» for an "
            "average reader? Answer with ONLY a single digit from 1 to 5.")

# ----------------------------------------------------------------- prompturi STRUCTURAL decorelate
# Cele patru de mai jos nu sunt reformulari. Motivul e masurat: castigul unui al treilea prompt e
# EXACT formula de reducere a variantei, `r_ens = (suma r_i)/sqrt(n + 2*suma rho_ij)`, verificata pe
# test cu eroare -0.000142 pe ansamblul de patru. In ea, singura parghie care se poate misca mult e
# `rho`, iar prompturile care schimba doar FORMULAREA raman toate la rho ~0.85-0.90 (few-shot 0.867,
# rubrica 0.902, marcat 0.845, learner 0.876, masurate la temperatura aleasa LOLO, nu la T=1).
# Un prompt cu r3 = +0.50, mult mai slab decat oricare de pana acum, bate perechea daca rho3 < 0.62.
# Deci ce trebuie schimbat e CE conditioneaza modelul, nu cat de bine e formulata intrebarea.

# (1) Tinta SINGURA, fara propozitie. Ambele prompturi ale sistemului conditioneaza pe context, deci
# o greseala indusa de context nu poate fi impartasita cu asta. Capcana, masurata inainte de rulare:
# pe test sunt 5135 perechi (limba, tinta) distincte din 5624 randuri, iar sinhaleza are 214 din 600,
# adica 64% legaturi. Fara context randurile cu aceeasi tinta primesc B IDENTIC, iar legaturile
# plafoneaza Pearson. Predictia declarata e ca varianta asta cade pe `si`.
P_FARA_CONTEXT = ("How complex or difficult is the {lang} word \"{tok}\" for an average reader of "
                  "{lang}? On a scale of 1-5 (1=very familiar, 2=simple, 3=neutral, 4=difficult, "
                  "5=very difficult), answer with ONLY a single digit from 1 to 5.")

# (2) ALT CONSTRUCT: cat de comun e cuvantul, nu cat de dificil. Frecventa e cel mai bun corelat
# cunoscut al complexitatii lexicale, dar e o alta intrebare, deci modelul o poate greasi altfel.
# ATENTIE LA SEMN: scara e scrisa ca 5 = foarte rar, tocmai ca r(B, y) sa ramana POZITIV. Un membru
# cu semn inversat nu doar ca n-ar ajuta, ar distruge ansamblul, iar formula frontierei presupune r
# pozitiv. Verificarea de semn pe trial se face inainte de orice agregare.
P_FRECVENTA = ("How common is the {lang} word \"{tok}\" in everyday written {lang}, as used in the "
               "sentence:\n\"{sent}\"\nOn a scale of 1-5 (1=among the most common words, 2=common, "
               "3=neither common nor rare, 4=rare, 5=very rare), answer with ONLY a single digit "
               "from 1 to 5.")

# (3) CITIRE BINARA la trei praguri. Se cere cifra 5 pentru da si 1 pentru nu, deci `digit_mass`,
# harta `self.digit` si D.4 raman NEATINSE: nu se umbla la `scale=`, iar fisierul iese cu aceleasi
# cinci coloane `p1_*`. Masa se aduna pe cifrele 1 si 5, restul raman aproape goale, si `_expected`
# da o valoare in [0,1] ca oricare alta. Cele trei praguri intra ca TREI surse in `make_fs_runs`, cu
# T comun; media lor e o citire de tip legatura cumulativa a scarii ordinale, adica alta FORMA de
# citire, nu alta formulare a aceleiasi citiri.
P_BIN_NECUNOSCUT = ("In the {lang} sentence: \"{sent}\"\nWould an average reader of {lang} be "
                    "UNFAMILIAR with the word \"{tok}\"?\nAnswer with ONLY the digit 5 if yes, or "
                    "the digit 1 if no.")
P_BIN_DIFICIL = ("In the {lang} sentence: \"{sent}\"\nWould an average reader of {lang} find the "
                 "word \"{tok}\" DIFFICULT to understand?\nAnswer with ONLY the digit 5 if yes, or "
                 "the digit 1 if no.")
P_BIN_DICTIONAR = ("In the {lang} sentence: \"{sent}\"\nWould an average reader of {lang} need a "
                   "DICTIONARY to understand the word \"{tok}\"?\nAnswer with ONLY the digit 5 if "
                   "yes, or the digit 1 if no.")

# (4) LEMA in loc de forma flexionata. Predictie declarata INAINTE de rulare: e cel mai putin
# decorelat dintre cei patru. `output/e_lemma_coverage.md` spune de ce: `fil` si `si` n-au lema
# deloc, deci pe doua limbi din zece intrebarea e literal despre acelasi sir, iar pe restul lema
# difera de forma pe 37-67% din randuri. Pe trial germana are 2 randuri din 30 cu lema diferita,
# deci cernerea de trial e ea insasi slaba pentru varianta asta anume.
# Cand lema lipseste sau coincide cu forma, `{lemma}` primeste chiar forma: UN singur sablon, nu
# doua, ca sa nu se compare doua intrebari diferite intre limbi.
P_LEMA = ("In the {lang} sentence: \"{sent}\"\nThe word \"{tok}\" is a form of the {lang} lemma "
          "\"{lemma}\". Rate the lexical difficulty of the LEMMA \"{lemma}\" on a scale from 1 "
          "(very familiar) to 5 (very difficult). Answer with only the digit.")


def c2s(c):
    """complexitate [0,1] -> intreg 1-5, pentru exemplele few-shot. Acelasi ca llm_prompt.c2s:33."""
    return int(np.clip(round(1 + 4 * float(c)), 1, 5))


class PromptLab(LLMRater):
    """LLMRater plus modurile de prompt. MLX, fiindca tot bazinul multilingv e MLX.

    Generarea trece prin `mlx_lm.generate`, adica API-ul de biblioteca. Serverul `mlx_lm` si Ollama
    raman excluse din alt motiv: ele trunchiaza logits-urile, deci ar rupe citirea P(1..5) de la final,
    nu generarea.
    """

    def _gen(self, msgs, max_tokens=COT_TOKENS, temp=0.0, top_p=0.0, seed=None):
        if self.backend != "mlx":
            raise RuntimeError(f"prompt_lab e scris pentru MLX, nu {self.backend!r}")
        from mlx_lm import generate
        from mlx_lm.sample_utils import make_sampler
        if seed is not None:
            self.mx.random.seed(int(seed))
        return generate(self.model, self.tok, prompt=self._encode_chat(msgs), max_tokens=max_tokens,
                        sampler=make_sampler(temp=temp, top_p=top_p), verbose=False).strip()

    def _soft(self, msgs):
        """(scor, (p, masa_bruta)) pentru UN soft-read.

        `digit_mass` plus `_expected`, adica exact corpul lui `LLMRater._score_msgs`, dar fara sa
        arunce distributia. Scorul iese bit-identic cu cel de dinainte: aceeasi functie pe acelasi
        vector. `p` e None cand masa e degenerata, si atunci scorul e NaN, ca si pana acum.
        """
        p, raw = self.digit_mass(msgs)
        return (np.nan if p is None else self._expected(p)), (p, raw)

    def _score(self, tmpl, sent, tok, lang_label):
        return self._soft(self._prompt_msgs(sent, tok, tmpl, lang_label))

    def v_single(self, tmpl, sent, tok, lang_label):
        v, part = self._score(tmpl, sent, tok, lang_label)
        return v, [part]

    def v_zeroshot(self, sent, tok, lang_label):
        """Baseline-ul din bake-off: media celor doua prompturi. Identic cu LLMRater.rate()."""
        out = [self._score(t, sent, tok, lang_label) for t in (P_EXPERT, P_SHORT)]
        vals = [v for v, _ in out if np.isfinite(v)]
        return (float(np.mean(vals)) if vals else np.nan), [pt for _, pt in out]

    def v_marcat(self, sent, tok, lang_label):
        """Tinta marcata inline cu «». Daca nu se gaseste ca subsir, propozitia rămâne nemarcata si
        intrebarea o numeste oricum, ca sa nu pierdem itemul: aceeasi politica de negasire ca la
        surprisal(), unde 18 tinte din 5624 nu se gasesc."""
        from solution_bert import normalize_token
        text = str(sent).replace("\n", " ").strip()
        i = text.find(tok)
        if i < 0:
            t2 = normalize_token(tok)
            i = text.find(t2)
            if i >= 0:
                tok = t2
        marked = text if i < 0 else text[:i] + "«" + tok + "»" + text[i + len(tok):]
        v, part = self._soft([{"role": "user", "content": P_MARCAT.format(
            lang=lang_label, tok=tok, marked=marked)}])
        return v, [part]

    def v_lema(self, sent, tok, lang_label, lemma):
        """Intrebarea despre LEMA, cu propozitia pastrata ca context.

        `lemma` vine din `output/lemmas_mlsp.csv`, unde e deja calculata de `lemmatize_mlsp.py`. Cand
        lipseste, apelantul trece chiar forma: politica de negasire e aceeasi cu a lui `v_marcat` si
        a lui `surprisal()`, adica itemul nu se pierde, dar se numara.
        """
        v, part = self._soft([{"role": "user", "content": P_LEMA.format(
            lang=lang_label, tok=tok, lemma=lemma,
            sent=str(sent).replace("\n", " ").strip())}])
        return v, [part]

    def v_fewshot(self, sent, tok, lang_label, shots):
        ex = "\n".join(f'- "{w}" in "{s}" -> {sc}' for (s, w, sc) in shots)
        content = FEWSHOT_HEAD.format(ex=ex, lang=lang_label, tok=tok,
                                      sent=str(sent).replace("\n", " ").strip())
        v, part = self._soft([{"role": "user", "content": content}])
        return v, [part]

    def _cot_msgs(self, sent, tok, lang_label):
        return [{"role": "user", "content": COT_ASK.format(
            lang=lang_label, tok=tok, sent=str(sent).replace("\n", " ").strip())}]

    def v_cot(self, sent, tok, lang_label):
        ask = self._cot_msgs(sent, tok, lang_label)
        rationale = self._gen(ask)
        v, part = self._soft(ask + [{"role": "assistant", "content": rationale},
                                    {"role": "user", "content": COT_SCORE}])
        return v, [part]

    def v_cot_sc(self, sent, tok, lang_label, k=COT_SC_K):
        ask = self._cot_msgs(sent, tok, lang_label)
        out = []
        for i in range(k):
            rationale = self._gen(ask, temp=0.7, top_p=0.9, seed=SEED + i)
            out.append(self._soft(ask + [{"role": "assistant", "content": rationale},
                                         {"role": "user", "content": COT_SCORE}]))
        vals = [v for v, _ in out if np.isfinite(v)]
        return (float(np.mean(vals)) if vals else np.nan), [pt for _, pt in out]


# v0a si v0b sunt cele DOUA prompturi din care v0_zeroshot face media. Fara ele, comparatia v0 fata de
# v1 sau v2 confunda doua lucruri: contintutul promptului si faptul ca v0 mediaza doua prompturi, deci
# are varianta mai mica prin construcție. Adaugate pe 17 august, dupa ce v0 a castigat pe toate limbile.
VARIANTS = ["v0_zeroshot", "v0a_expert", "v0b_short", "v1_learner", "v2_rubrica", "v3_fewshot",
            "v4_cot", "v5_cot_sc", "v7_proportie", "v8_marcat",
            # structural decorelate, adaugate 22 august: schimba CE conditioneaza modelul
            "v9_fara_context", "v10_lema", "v11_frecventa",
            "v12_bin_necunoscut", "v12_bin_dificil", "v12_bin_dictionar"]
# Ansambluri cu ponderi EGALE peste prompturile individuale, calculate la agregare din scorurile deja
# masurate, deci zero forward-uri in plus. Ordinea e prespecificata, "adauga urmatoarea varianta", nu
# aleasa dupa ce s-au vazut cifrele: altfel ar fi pescuit printre 63 de submultimi.
#
# ATENTIE la ponderi: prima versiune media v0_zeroshot cu v1 si v2, iar v0 e el insusi o medie, deci
# prompturile din el primeau 1/6 fiecare si rubrica 1/3. Ansamblul iesea mai slab decat v0 dintr-un
# defect de ponderare, nu fiindca "mai multe prompturi strica".
_S = ["v0a_expert", "v0b_short", "v1_learner", "v2_rubrica"]
DERIVED = {"e2_ansamblu": _S[:2],       # baseline-ul din bake-off, recalculat din componente
           "e3_ansamblu": _S[:3],
           "e4_ansamblu": _S,
           "e5_ansamblu": _S + ["v3_fewshot"],
           "e6_ansamblu": _S + ["v3_fewshot", "v4_cot"],
           "e7_ansamblu": _S + ["v3_fewshot", "v4_cot", "v7_proportie"],
           "e8_ansamblu": _S + ["v3_fewshot", "v4_cot", "v7_proportie", "v8_marcat"]}


def lolo_shots(ml, lang, k=K_SHOTS):
    """k exemple etichetate din trial-ul CELORLALTE limbi, niciodata din `lang`.

    Asta e ce pastreaza revendicarea zero-label pentru limba tinta: exemplele vin din limbile pe care
    protocolul le permite oricum la potrivirea ponderilor de fuziune. Esantion fix pe SEED, deci
    aceleasi exemple la fiecare rulare.
    """
    other = ml[ml["lang"] != lang]
    s = other.sample(min(k, len(other)), random_state=SEED)
    return [(str(r.sent).replace("\n", " ").strip(), str(r.token).strip(), c2s(r.complexity))
            for r in s.itertuples()]


LEMMAS = os.path.join(OUT, "lemmas_mlsp.csv")


def lem_key(lang, token, sent):
    """Cheia de join catre `output/lemmas_mlsp.csv`.

    Fisierul NU e in ordinea lui `load_mlsp`: alinierea pozitionala pe (limba, tinta) nimereste doar
    120 din 300 pe trial si 447 din 5624 pe test, deci un join pozitional ar lipi tacit lema altui
    rand. Cheia (limba, tinta, propozitie) e insa UNICA si completa pe amandoua spliturile, 300/300
    si 5624/5624, verificat inainte de a scrie codul asta.
    """
    return (str(lang).strip(), str(token).strip(),
            str(sent).replace("\n", " ").strip())


def lemma_map(split):
    """{cheie: lema} pentru un split, cu forma de suprafata acolo unde lema lipseste.

    `fil` si `si` n-au lematizator in stanza, deci lema lor e goala pe TOATE randurile. Politica e
    aceeasi cu a lui `v_marcat`: itemul nu se pierde, primeste chiar forma, si numarul de cazuri se
    tipareste, ca sa nu se citeasca un rezultat crezand ca s-a intrebat despre leme peste tot.
    """
    if not os.path.exists(LEMMAS):
        raise SystemExit(f"{LEMMAS} lipseste. Ruleaza intai lemmatize_mlsp.py")
    d = pd.read_csv(LEMMAS)
    d = d[d["split"] == split]
    if d.empty:
        raise SystemExit(f"{LEMMAS} n-are randuri de {split}")
    out = {}
    for r in d.itertuples():
        lm = str(r.lemma).strip()
        out[lem_key(r.lang, r.token, r.sent)] = lm if lm and lm.lower() != "nan" else None
    return out


def csv_path(model_key, split="trial"):
    """Trial rams pe calea canonica; orice alt split scrie intr-un SUBDIRECTOR.

    Subdirector si nu un sufix in nume: `aggregate()` face glob pe `output/promptlab_*.csv`, deci un
    `promptlab_<model>_test.csv` ar intra tacut in raportul E.10 ca al unsprezecelea "model", cu
    randuri de test intr-un raport care spune despre sine "niciodata pe test". Aceeasi conventie cu
    `bakeoff_trial.SPLITS[...]["dirname"]`.
    """
    return (os.path.join(OUT, f"promptlab_{model_key}.csv") if split == "trial"
            else os.path.join(OUT, f"promptlab_{split}", f"{model_key}.csv"))


def dist_cells_pad(parts, k=5, slots=2):
    """Celulele distributiei pentru un rand, in cele `slots` sloturi ale lui `dist_cols`.

    Acelasi idiom ca `bakeoff_trial.dist_cells`: `repr(float(x))`, adica reprezentarea scurta care
    face roundtrip EXACT, deci un B recalculat din coloanele astea iese acelasi float, nu unul
    apropiat, si verificarea nu are toleranta de ales.

    Diferenta fata de `dist_cells` e ca aici numarul de soft-read-uri NU e mereu doi: `v3_fewshot`
    are unul, `v0_zeroshot` are doi, `v5_cot_sc` are cinci. Sloturile lipsa rams complet goale, iar
    din cele in plus se scriu primele doua; `score` ramane media peste TOATE, deci coloana nu se
    schimba. Un slot gol e informatie, nu o lipsa: spune ca varianta a citit o singura distributie.
    """
    out = []
    for j in range(slots):
        p, raw = parts[j] if j < len(parts) else (None, None)
        out += ["" if p is None else repr(float(p[i])) for i in range(k)]
        out.append("" if raw is None else repr(float(raw)))
    return out


def measure(model_key, variants, limit=None, split="trial", out=None):
    from mlsp_common import LLM_POOL, load_mlsp, lang_name
    import d4_sanity

    ent = LLM_POOL.get(model_key)
    if ent is None:
        raise SystemExit(f"model necunoscut: {model_key!r}. Chei: {sorted(LLM_POOL)}")
    bad = [v for v in variants if v not in VARIANTS]
    if bad:
        raise SystemExit(f"variante necunoscute: {bad}. Cunoscute: {VARIANTS}")
    # Verificat INAINTE de a coborî greutatile: `aggregate()` face glob pe `output/promptlab_*.csv`,
    # deci un `--out` care nimereste tiparul ala ar intra tacut in raportul E.10 ca pe un model in
    # plus. Se refuza, nu se avertizeaza, si se refuza inainte de model ca sa nu se piarda o incarcare.
    if out and glob.fnmatch.fnmatch(os.path.basename(out), "promptlab_*.csv") \
            and os.path.dirname(os.path.abspath(out)) == os.path.abspath(OUT):
        raise SystemExit(f"--out {out}: numele nimereste tiparul pe care il citeste --aggregate, deci "
                         "fisierul ar intra in raportul E.10 ca al unsprezecelea model. Alege alt nume "
                         "sau alt director.")

    ml = load_mlsp(split)
    if limit:
        ml = ml.groupby("lang", sort=True).head(max(1, int(limit) // ml["lang"].nunique()))
    # `load_mlsp("trial")` e LITERAL, nu `load_mlsp(split)`: exemplele few-shot poarta etichete, iar
    # exemple din test ar pune etichete de test in prompt si ar invalida orice cifra de test. Efectul
    # secundar e cel dorit: cele 6 exemple ale unei limbi sunt aceleasi pe trial si pe test, deci
    # configuratia e fixa. NU se schimba niciodata in `split`.
    shots = {lg: lolo_shots(load_mlsp("trial"), lg) for lg in sorted(ml["lang"].unique())}

    # Harta de leme se construieste INAINTE de a coborî greutatile, si se cere sa acopere fiecare
    # rand: o cheie lipsa ar da KeyError abia dupa incarcarea modelului si dupa D.4, adica dupa
    # minute pierdute. Acoperirea inseamna „cheia exista", nu „lema e nevida"; a doua se numara.
    leme = {}
    if "v10_lema" in variants:
        lm = lemma_map(split)
        miss = [lem_key(x.lang, str(x.token).strip(), x.sent) for x in ml.itertuples()]
        absente = [k for k in miss if k not in lm]
        if absente:
            raise SystemExit(f"{len(absente)} randuri fara cheie in {LEMMAS}, primul {absente[0]!r}")
        leme = {k: (lm[k] or k[1]) for k in miss}
        gol = sum(1 for k in miss if lm[k] is None)
        dif = sum(1 for k in miss if lm[k] and lm[k] != k[1])
        print(f"[E10] leme: {len(miss)} randuri, {gol} fara lema (primesc forma), "
              f"{dif} cu lema diferita de forma", flush=True)

    t0 = time.time()
    r = PromptLab(model_key)
    t_load = time.time() - t0
    print(f"[E10] {model_key} incarcat in {t_load:.1f}s, {len(ml)} instante de {split}, "
          f"variante {variants}", flush=True)

    first = ml.iloc[0]
    ok, fails = d4_sanity.run_sanity(r, model_key, ent, str(first["lang"]), str(first["sent"]),
                                     str(first["token"]), prompt_set="multi", t_load=t_load)
    if not ok:
        raise SystemExit(f"[E10] D.4 a picat pe {model_key}: {fails}")

    # `--out` scrie in alt fisier decat cel canonic al perechii (model, split). Necesar fiindca
    # fisierele de trial de dinainte de coloanele de distributie au SASE coloane, deci garda de antet
    # de mai jos blocheaza corect un append, si o rulare noua nu are voie sa cada peste una veche.
    path = csv_path(model_key, split) if not out else (
        out if os.path.isabs(out) else os.path.join(HERE, out))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Append, nu overwrite: variantele se ruleaza in loturi separate, fiindca v4 si v5 costa de zeci de
    # ori mai mult decat restul si nu au voie sa blocheze scrierea celorlalte.
    new = not os.path.exists(path)
    if not new:
        # Garda de antet. Fisierele scrise inainte de coloanele de distributie au SASE coloane, si un
        # append de randuri late sub un antet ingust ar da un CSV pe care pandas il citeste cu coloane
        # deplasate, fara nicio eroare. Cine vrea coloanele noi porneste un fisier nou.
        with open(path, newline="", encoding="utf-8") as fh0:
            head = next(csv.reader(fh0))
        if head != COLS:
            raise SystemExit(f"{path} are antetul {head}, iar acum s-ar scrie {COLS}. Un append de "
                             "randuri late sub antetul ingust ar deplasa tacut coloanele. Muta "
                             "fisierul vechi si porneste unul nou.")
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(COLS)
        for vi, var in enumerate(variants, 1):
            t1, nan_v = time.time(), 0
            for i, row in enumerate(ml.itertuples(), 1):
                lab = lang_name(row.lang)
                tok = str(row.token).strip()
                ti = time.time()
                if var == "v0_zeroshot":
                    s, parts = r.v_zeroshot(row.sent, tok, lab)
                elif var == "v0a_expert":
                    s, parts = r.v_single(P_EXPERT, row.sent, tok, lab)
                elif var == "v0b_short":
                    s, parts = r.v_single(P_SHORT, row.sent, tok, lab)
                elif var == "v1_learner":
                    s, parts = r.v_single(P_LEARNER, row.sent, tok, lab)
                elif var == "v2_rubrica":
                    s, parts = r.v_single(P_RUBRIC, row.sent, tok, lab)
                elif var == "v7_proportie":
                    s, parts = r.v_single(P_PROPORTIE, row.sent, tok, lab)
                elif var == "v8_marcat":
                    s, parts = r.v_marcat(row.sent, tok, lab)
                elif var == "v9_fara_context":
                    s, parts = r.v_single(P_FARA_CONTEXT, row.sent, tok, lab)
                elif var == "v11_frecventa":
                    s, parts = r.v_single(P_FRECVENTA, row.sent, tok, lab)
                elif var == "v12_bin_necunoscut":
                    s, parts = r.v_single(P_BIN_NECUNOSCUT, row.sent, tok, lab)
                elif var == "v12_bin_dificil":
                    s, parts = r.v_single(P_BIN_DIFICIL, row.sent, tok, lab)
                elif var == "v12_bin_dictionar":
                    s, parts = r.v_single(P_BIN_DICTIONAR, row.sent, tok, lab)
                elif var == "v10_lema":
                    s, parts = r.v_lema(row.sent, tok, lab,
                                        leme[lem_key(row.lang, tok, row.sent)])
                elif var == "v3_fewshot":
                    s, parts = r.v_fewshot(row.sent, tok, lab, shots[row.lang])
                elif var == "v4_cot":
                    s, parts = r.v_cot(row.sent, tok, lab)
                else:
                    s, parts = r.v_cot_sc(row.sent, tok, lab)
                sec = time.time() - ti
                nan_v += int(not np.isfinite(s))
                w.writerow([row.lang, row.token, f"{float(row.complexity):.6f}", var,
                            "" if not np.isfinite(s) else f"{s:.8f}", f"{sec:.4f}"]
                           + dist_cells_pad(parts, len(r.digits)))
                fh.flush()
                if i % 50 == 0 or i == len(ml):
                    el = time.time() - t1
                    print(f"[E10] {var} ({vi}/{len(variants)})  {i}/{len(ml)}  {el:.0f}s  "
                          f"{el/i:.2f}s per item  NaN={nan_v}", flush=True)
            print(f"[E10] {var}: {len(ml)} in {time.time()-t1:.0f}s, NaN={nan_v}", flush=True)
    print(f"[E10] -> {path}")
    return 0


def aggregate():
    from bakeoff_trial import pearson, fisher_ci, lolo_select, md_matrix
    rows = {}
    for p in sorted(glob.glob(os.path.join(OUT, "promptlab_*.csv"))):
        key = os.path.basename(p)[len("promptlab_"):-len(".csv")]
        rows[key] = pd.read_csv(p)
    if not rows:
        raise SystemExit(f"niciun output/promptlab_*.csv in {OUT}")

    L = ["# E.10. Optimizarea promptului pentru semnalul B\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `prompt_lab.py --aggregate`. "
         "Pe cele 300 de instante de trial, niciodata pe test. Datele brute: "
         "`output/promptlab_<model>.csv`.\n\n",
         "Selectia variantei e tratata ca selectia modelului din §5.1: leave-one-language-out. "
         "Altfel, alegerea promptului pe trial-ul tuturor celor 10 limbi ar fi tuning pe limba "
         "tinuta deoparte.\n"]

    for key, df in rows.items():
        # Ansamblul se calculeaza aici, din scorurile deja masurate. Zero forward-uri in plus.
        wide = df.pivot_table(index=["lang", "token", "complexity"], columns="variant",
                              values="score", aggfunc="first").reset_index()
        for name, parts in DERIVED.items():
            have = [c for c in parts if c in wide.columns]
            if len(have) == len(parts):
                wide[name] = wide[have].mean(axis=1)
        vars_present = [c for c in list(VARIANTS) + list(DERIVED) if c in wide.columns]
        langs = sorted(wide["lang"].unique())

        tab = {v: {lg: pearson(g[v].values, g["complexity"].values)
                   for lg, g in wide.groupby("lang", sort=True)} for v in vars_present}
        L += [f"\n## `{key}`\n"]
        L += md_matrix(tab, langs, "r per limba, per varianta de prompt")

        sec = df.groupby("variant")["sec"].agg(["mean", "sum", "count"])
        L += ["\n### Cost\n\n| varianta | s per item | total | n |\n|---|---|---|---|\n"]
        for v in df["variant"].unique():
            s = sec.loc[v]
            L.append(f"| `{v}` | {s['mean']:.2f} s | {s['sum']/60:.1f} min | {int(s['count'])} |\n")

        sel = lolo_select(tab, langs)
        L += ["\n### Selectia LOLO peste variante\n\n",
              "| limba | varianta aleasa pe celelalte 9 | media pe 9 | r pe L |\n|---|---|---|---|\n"]
        for lg, v, m9, rl in sel:
            L.append(f"| {lg} | `{v}` | {m9:+.4f} | {rl:+.4f} |\n")
        rs = [rl for _, _, _, rl in sel if np.isfinite(rl)]
        base = [tab["v0_zeroshot"][lg][0] for lg in langs
                if "v0_zeroshot" in tab and np.isfinite(tab["v0_zeroshot"][lg][0])]
        L.append(f"\n**r mediu sub selectie LOLO peste variante: {np.mean(rs):+.4f}**"
                 + (f", fata de {np.mean(base):+.4f} al baseline-ului `v0_zeroshot`. "
                    f"Castig: {np.mean(rs) - np.mean(base):+.4f}.\n" if base else ".\n"))
        # Comparatia pereche, limba cu limba, intre varianta aleasa LOLO si baseline. Media singura nu
        # spune daca un castig vine de peste tot sau dintr-o limba.
        if base:
            pairs = [(lg, tab[v][lg][0] - tab["v0_zeroshot"][lg][0])
                     for lg, v, _, _ in sel if np.isfinite(tab[v][lg][0])]
            dd = np.array([d for _, d in pairs], float)
            up = int((dd > 0).sum())
            se = float(dd.std(ddof=1) / np.sqrt(len(dd))) if len(dd) > 1 else float("nan")
            L.append(f"\nComparatie pereche fata de baseline, limba cu limba: **{up} din {len(dd)} "
                     f"limbi se imbunatatesc**, medie {dd.mean():+.4f}, sd {dd.std(ddof=1):.4f}, "
                     f"deci {abs(dd.mean()/se):.1f} erori standard. "
                     + ("Sugestiv, nu stabilit: la 9 grade de libertate asta nu trece pragul obisnuit."
                        if abs(dd.mean() / se) < 2.26 else "Peste pragul de 2.26 la 9 grade de libertate.")
                     + " Per limba: "
                     + ", ".join(f"{lg} {d:+.3f}" for lg, d in pairs) + ".\n")
        lo, hi = fisher_ci(0.60, 30)
        L.append(f"\nPrag de zgomot: la n = 30, intervalul de 95% pentru r = 0.60 e [{lo:.2f}, "
                 f"{hi:.2f}]. O varianta care castiga mai putin decat atat pe o limba nu a castigat "
                 "nimic masurabil acolo; media pe 10 limbi e mai stabila.\n")

    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("".join(L))
    print(f"[E10] {len(rows)} modele -> {REPORT}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None, help="cheie din mlsp_common.LLM_POOL")
    ap.add_argument("--variants", default=",".join(VARIANTS), help=f"din {VARIANTS}")
    ap.add_argument("--limit", type=int, default=None, help="cate instante, impartite pe limbi")
    ap.add_argument("--split", default="trial", choices=("trial", "test"),
                    help="ce instante se noteaza. Exemplele few-shot rams din trial oricum, vezi "
                         "docstring-ul. Trial scrie pe calea canonica, test in output/promptlab_test/")
    ap.add_argument("--out", default=None,
                    help="calea CSV-ului de scris. Implicit cea canonica a perechii (model, split). "
                         "Nu are voie sa nimereasca output/promptlab_*.csv, pe care il citeste "
                         "--aggregate.")
    ap.add_argument("--aggregate", action="store_true")
    a = ap.parse_args()
    if a.aggregate:
        return aggregate()
    if not a.model:
        ap.error("--model <cheie> sau --aggregate")
    return measure(a.model, [v.strip() for v in a.variants.split(",")], a.limit, a.split, a.out)


if __name__ == "__main__":
    sys.exit(main())
