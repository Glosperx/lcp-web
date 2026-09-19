"""Lemele pentru fixul de frecventa, pe limbile MLSP plus CompLex EN.

De ce exista. Semnalul A citeste frecventa formei de suprafata. Pe limbile flexionate multe forme
lipsesc din lista `wordfreq` si par FALS rare, deci primesc un zipf mic si arata artificial dificile.
Fixul, masurat pe romana ca cel mai mare castig unic al lucrarii (+4.09), e `max(zipf_forma, zipf_lema)`.
`lexical()` il stie deja, prin argumentul `lemmas=`; ce lipsea erau lemele pentru celelalte limbi.
Romana primise initial leme GOLD de la shared task, dar de la 29 aug 2026, cu romana intrata ca a
11-a limba in grila LOLO, e relematizata cu stanza ca toate celelalte, ca leme gold pe o singura
limba sa nu confunde teza "fixul de lema scaleaza cu bogatia morfologica" cu un artefact de calitate.
Lema gold ramane doar ca ablatie separata, plafon.

Fisierul asta NU atinge niciun semnal. Produce doar lemele si le pune pe disc.

Cine ramane pe dinafara, si de ce se raporteaza in loc sa se ascunda:

  si   `freq_available("si")` e False, deci `zipf_safe` intoarce indisponibil si `lexical()` nu aplica
       lema oricum. In plus stanza nu are procesor de lema pentru sinhaleza. No-op de doua ori.
  fil  stanza nu are deloc tagalog. Ramane pe forma de suprafata.

Deci masuratoarea are 9 limbi din 11 (10 MLSP + romana), nu toate 11. Cele doua absente sunt ele
insele rezultat: palierul 3 al tabelului de resurse nu are lematizator, exact cum prezicea planul.

Lematizarea se face IN CONTEXT, nu pe tinta izolata. Forma ambigua se dezambiguizeaza doar asa, iar
fixul isi pierde jumatate din valoare fara. Alinierea tinta -> cuvant trece prin `find_char_span`,
aceeasi functie folosita de calea de embedding, deci ambele semnale vad aceeasi definitie a tintei.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python lemmatize_mlsp.py
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python lemmatize_mlsp.py --langs de,en
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python lemmatize_mlsp.py --report
"""
import argparse
import os
import sys
import time

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
LEM_MLSP = os.path.join(OUT, "lemmas_mlsp.csv")
LEM_EN = os.path.join(OUT, "lemmas_complex_en.csv")
MSP_PAIRS = os.path.join(OUT, "msp_pairs.csv")
REPORT = os.path.join(OUT, "e_lemma_coverage.md")
COLS = ["split", "lang", "sent", "token", "lemma", "sursa"]

# Cele 9 limbi cu lematizator, verificat pe `resources.json` al lui stanza 1.14.0 inainte de orice
# descarcare. `si` are intrare de limba dar `lemma` gol; `fil` nu are intrare deloc (codul stanza ar fi
# `tl`). Lista e explicita, nu dedusa la rulare: daca stanza adauga tagalog maine, vrem sa fie o
# decizie, nu o schimbare tacuta de acoperire intre doua rulari.
#
# "ro" adaugata pe 29 aug 2026: romana avea deja leme GOLD, primite de la shared task-ul romanesc,
# nu produse de un lematizator. Folosirea lor direct in tabelul cu 11 limbi ar fi un confound in
# directia gresita pentru teza "fixul de lema scaleaza cu bogatia morfologica" - romana ar arata
# artificial cel mai mare castig, exact ce prezice si teza, fara sa distinga intre ele. Lema PREZISA
# aici e pentru tabelul principal; lema gold din data/test_set.csv ramane doar ca ablatie separata,
# plafon.
STANZA_LANGS = ["ca", "de", "en", "es", "fr", "it", "ja", "pt", "ro"]
NO_LEMMATIZER = {"fil": "stanza nu are tagalog", "si": "stanza nu are procesor de lema"}


def _pipeline(lg):
    """Pipeline stanza pentru limba, cu POS. `lemma` cere doar `tokenize`, dar modelul de lema e
    antrenat cu UPOS ca intrare, deci fara tagger calitatea scade exact pe limbile flexionate care
    conteaza pentru teza. Alexandru a ales varianta completa pe 18 august."""
    import stanza
    from stanza.resources.common import load_resources_json
    # Procesoarele se deduc din `default_processors` al limbii, nu se presupun: `mwt` exista doar unde
    # limba are contractii, iar japoneza n-are, deci o lista fixa ar crapa cu UnsupportedProcessorError
    # dupa ce sase limbi au trecut deja.
    have = load_resources_json()[lg]["default_processors"]
    procs = ",".join(x for x in ("tokenize", "mwt", "pos", "lemma") if x in have)
    return stanza.Pipeline(lg, processors=procs, verbose=False,
                           tokenize_no_ssplit=False, download_method=None)


def _spans(doc):
    """-> [(start_char, end_char, lema)] pentru fiecare cuvant din document.

    La limbile cu MWT un token se sparge in mai multe cuvinte (fr `des` -> `de le`), iar cuvintele
    mostenesc spanul tokenului parinte, fiindca ele singure n-au offseturi in textul original.
    """
    out = []
    for s in doc.sentences:
        for t in s.tokens:
            a, b = t.start_char, t.end_char
            if a is None or b is None:
                continue
            for w in t.words:
                out.append((a, b, w.lemma or ""))
    return out


def _lemma_for(spans, start, end):
    """Lemele cuvintelor care se suprapun cu [start, end), inlantuite.

    Tinta multi-cuvant (cele 8 italiene) iese ca lema1 + spatiu + lema2. `zipf_safe` va da 0 pe sirul
    ala, deci `max(z, zl)` lasa frecventa pe loc: degradare catre no-op, nu catre valoare gresita.
    """
    hit = [lem for a, b, lem in spans if a < end and b > start and lem]
    return " ".join(hit)


def lemma_array(sents, tokens, split, langs):
    """Vectorul de leme aliniat rand cu rand, pentru `lexical(..., lemmas=...)`.

    Cautarea e pe cheia (split, limba, propozitie, tinta), NU pe pozitie. Pozitional ar parea mai
    ieftin, dar `lemmatize_mlsp` concateneaza splituri si limbi in ordinea lui, iar `finetune_xlmr`
    parcurge cadrele in ordinea lor: o singura schimbare de ordine intr-unul din cele doua ar corela
    tacut leme cu tinte straine, si nimic n-ar crapa. Cheia face desincronizarea imposibila.

    Limbile fara lematizator (`fil`, `si`) au lema goala in CSV, iar `lexical()` sare peste sirul gol,
    deci nu e nevoie de nicio ramura speciala aici.
    """
    if isinstance(langs, str):
        langs = [langs] * len(tokens)
    tab = pd.concat([pd.read_csv(p, keep_default_na=False) for p in (LEM_MLSP, LEM_EN)
                     if os.path.exists(p)], ignore_index=True)
    if tab.empty:
        raise SystemExit(f"{LEM_MLSP} lipseste. Ruleaza intai lemmatize_mlsp.py")
    key = dict(zip(zip(tab["split"], tab["lang"], tab["sent"].astype(str),
                       tab["token"].astype(str)), tab["lemma"].astype(str)))
    out = [key.get((split, lg, str(s), str(t)), "") for s, t, lg in zip(sents, tokens, langs)]
    miss = sum(1 for x in out if not x)
    print(f"[lem] {split}: {len(out)-miss}/{len(out)} leme gasite", flush=True)
    return out


def lemmatize(langs=None, limit=None):
    from mlsp_common import load_mlsp, ensure_complex_en
    from solution_bert import find_char_span
    import stanza

    langs = [lg for lg in (langs or STANZA_LANGS) if lg in STANZA_LANGS]
    os.makedirs(OUT, exist_ok=True)

    # Un singur cadru cu tot ce trebuie lematizat. CompLex EN e marcat `complex_en`, nu `test`, ca sa
    # se poata scrie separat fara sa se amestece cu MLSP la citire. RoLCP se incarca doar daca "ro"
    # chiar s-a cerut: altfel o rulare `--langs de,en` ar cere pe degeaba `data/RoLCP.csv`, fisierul
    # protejat cu parola care nu e mereu prezent local. Pe "trial" e oricum no-op, RoLCP n-are trial.
    frames = []
    for split in ("test", "trial"):
        d = load_mlsp(split, include_ro=("ro" in langs))[["lang", "sent", "token"]].copy()
        d["split"] = split
        frames.append(d)
    en = ensure_complex_en()[["sent", "token"]].copy()
    en["lang"], en["split"] = "en", "complex_en"
    frames.append(en)
    work = pd.concat(frames, ignore_index=True)
    if limit:
        work = work.groupby(["split", "lang"], group_keys=False).head(limit)

    rows, pairs = [], []
    for lg in langs:
        sub = work[work["lang"] == lg]
        if sub.empty:
            continue
        t0 = time.time()
        nlp = _pipeline(lg)
        # Propozitiile unice, o singura data prin stanza. Sapte limbi din zece au in medie 3 tinte per
        # context, iar CompLex EN repeta si el propozitii, deci fara deduplicare am plati de trei ori.
        sents = list(dict.fromkeys(sub["sent"].astype(str)))
        docs = nlp([stanza.Document([], text=s) for s in sents])
        spans = {s: _spans(d) for s, d in zip(sents, docs)}
        # Inventarul de tipuri pentru MSP, peste TOATE cuvintele, nu doar tintele. Tintele sunt alese
        # de shared task ca fiind interesante, deci un MSP calculat pe ele ar masura selectia lor, nu
        # limba. CompLex EN se exclude: ar da englezei un corpus de 25 de ori mai mare.
        mlsp_sents = set(sub[sub["split"] != "complex_en"]["sent"].astype(str))
        for st, doc in zip(sents, docs):
            if st not in mlsp_sents:
                continue
            for sn in doc.sentences:
                for w in sn.words:
                    if w.text and w.lemma and w.upos not in ("PUNCT", "NUM", "SYM", "X"):
                        pairs.append((lg, w.text.lower(), w.lemma.lower()))
        print(f"[lem] {lg}: {len(sents)} propozitii unice in {time.time()-t0:.0f}s", flush=True)

        for split, sent, tok in zip(sub["split"], sub["sent"].astype(str), sub["token"]):
            sp = find_char_span(sent, tok)
            lem, sursa = "", "gol"
            if sp is not None:
                lem = _lemma_for(spans[sent], *sp)
                sursa = "context" if lem else "gol"
            if not lem:
                # Tinta negasita ca subsir (18 in tot MLSP) sau fara cuvant suprapus. Ultima incercare,
                # pe tinta singura. E mai slaba fiindca n-are context de dezambiguizat, deci se
                # marcheaza ca atare si se numara separat in raport.
                d1 = nlp(str(tok))
                lem = " ".join(w.lemma or "" for s in d1.sentences for w in s.words).strip()
                sursa = "izolat" if lem else "gol"
            rows.append((split, lg, sent, tok, lem, sursa))

    for lg, motiv in NO_LEMMATIZER.items():
        sub = work[work["lang"] == lg]
        for split, sent, tok in zip(sub["split"], sub["sent"].astype(str), sub["token"]):
            rows.append((split, lg, sent, tok, "", "fara_lematizator"))

    pd.DataFrame(pairs, columns=["lang", "form", "lemma"]).to_csv(MSP_PAIRS, index=False)
    d = pd.DataFrame(rows, columns=COLS)
    d[d["split"] != "complex_en"].to_csv(LEM_MLSP, index=False)
    d[d["split"] == "complex_en"].to_csv(LEM_EN, index=False)
    print(f"[lem] scris {LEM_MLSP}, {LEM_EN} si {MSP_PAIRS} ({len(pairs)} perechi)", flush=True)
    return d


def report(d=None):
    from mlsp_common import freq_available
    if d is None:
        d = pd.concat([pd.read_csv(p, keep_default_na=False) for p in (LEM_MLSP, LEM_EN)
                       if os.path.exists(p)], ignore_index=True)
    if d.empty:
        raise SystemExit("nimic de raportat, ruleaza intai fara --report")

    L = ["# Acoperirea lemelor, pe limbile MLSP plus CompLex EN\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `lemmatize_mlsp.py`. Date brute: "
         f"`output/lemmas_mlsp.csv` si `output/lemmas_complex_en.csv`.\n\n",
         "Coloana care conteaza e **lema difera de forma**. Daca lema egaleaza forma, fixul nu are ce "
         "repara: `max(zipf_forma, zipf_lema)` intoarce aceeasi valoare. Ea e predictia directa a "
         "tezei morfologice, inainte de a masura vreun r.\n\n",
         "`frecventa` spune daca `wordfreq` serveste real limba. Unde e nu, fixul e no-op indiferent "
         "de lema, fiindca `zipf_safe` intoarce indisponibil si `lexical()` nu aplica inlocuirea.\n\n",
         "| split | limba | n | context | izolat | gol | lema difera de forma | frecventa |\n",
         "|---|---|---|---|---|---|---|---|\n"]
    for (split, lg), g in d.groupby(["split", "lang"], sort=True):
        n = len(g)
        c = int((g["sursa"] == "context").sum())
        i = int((g["sursa"] == "izolat").sum())
        z = int((g["sursa"].isin(("gol", "fara_lematizator"))).sum())
        dif = int((g["lemma"].astype(str).str.lower().str.strip()
                   != g["token"].astype(str).str.lower().str.strip()).sum() - z)
        fq = "da" if freq_available(lg) else "**nu**"
        L.append(f"| {split} | `{lg}` | {n} | {c} | {i} | {z} | **{dif}** ({100*dif/max(n,1):.1f}%) "
                 f"| {fq} |\n")
    with open(REPORT, "w", encoding="utf-8") as f:
        f.writelines(L)
    print(f"[lem] raport -> {REPORT}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--langs", type=str, default=None, help="lista separata prin virgula")
    ap.add_argument("--limit", type=int, default=None, help="primele N instante per split si limba")
    ap.add_argument("--report", action="store_true", help="doar raportul, din CSV-urile de pe disc")
    a = ap.parse_args()
    if a.report:
        report()
    else:
        report(lemmatize(a.langs.split(",") if a.langs else None, a.limit))
