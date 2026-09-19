"""Diversitate contextuala: in cate DOCUMENTE distincte apare cuvantul, nu de cate ori.

De ce, si e singurul candidat lexical din literatura cu dovada ca subsumeaza frecventa. Adelman,
Brown si Quesada (Psychological Science 2006, 17:814-823) masoara pe trei seturi de citire cu voce
tare si trei de decizie lexicala: **efectele de frecventa dispar cand se controleaza diversitatea
contextuala, dar nu si invers**. Efectul se extinde la duratele de fixatie in citirea de propozitii.

De ce ACUM, si nu dimineata. Sesiunea din 23 august a aratat ca sistemul se sprijina puternic pe
`zipf` (importanta 0.29-0.75 in surogatul lexical, dupa masura) si ca acea coloana e stricata in trei
limbi din zece, din trei motive distincte: **absenta** (si, `wordfreq` nu serveste limba),
**gauri** (fil, 152 din 570 de tinte cu zipf 0) si **nesiguranta de segmentare** (ja, `wordfreq` cere
MeCab, care lipseste). Dropout-ul pe coloana a confirmat mecanismul, urcand pe bratul A exact acele
trei limbi si numai ele, dar n-a trecut in fuziune fiindca lucreaza IN JURUL defectului. Diversitatea
contextuala il repara LA SURSA: se calculeaza din corpus, pentru toate cele zece limbi, cu acelasi
tokenizer, deci nu are nici gauri de acoperire, nici dependenta de MeCab.

Sursa si asimetria ei, declarate. `wikimedia/wikipedia`, dump 20231101, **un singur shard per limba**
pentru cele opt limbi mari, adica 140.000-185.000 de articole fiecare, si dump-ul intreg pentru si
(~17k articole) si tl (~45k). Un shard e o felie arbitrara a dump-ului, deci un esantion, nu tot
corpusul. Cifra scrisa nu e numarul brut de documente ci **rata**, normalizata ca la `wordfreq`:

    cd = max(0, log10(documente_cu_cuvantul / documente_totale * 1e9))

Aceeasi conventie ca `zipf` din `build_freq_tail.py`, deci cele doua coloane sunt pe scari comparabile
si diferenta dintre ele e chiar ce vrem sa masuram, nu un artefact de unitate.

Capcana mostenita, si nu se re-plateste: tokenizarea foloseste `regex` cu `[\\p{L}\\p{M}]` plus cei doi
separatori de latime zero. In Python `\\w` NU cuprinde semnele vocalice sinhaleze (categoria Unicode
Mn), deci `re.findall(r"[^\\W\\d_]+")` sparge fiecare cuvant sinhalez in consoane separate, si nimic nu
se plange.

Diferenta de cod fata de `build_freq_tail.numara` e **un `set()`**: se numara documentele in care
apare cuvantul, nu aparitiile lui.

Rulare:
  python build_ctx_div.py
"""
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd
import regex

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output")
SRC = os.path.join(DATA, "wiki_ctx")
DEST = os.path.join(DATA, "ctx_div")

TOKEN = regex.compile(r"[\p{L}\p{M}‌‍]+")
# cheia = fisierul wiki, valoarea = codul de limba MLSP
LANGS = {"ca": "ca", "de": "de", "en": "en", "es": "es", "fr": "fr",
         "it": "it", "ja": "ja", "pt": "pt", "si": "si", "tl": "fil"}
MIN_DOCS = 2        # sub doua documente cuvantul nu are "diversitate", are o aparitie


def numara(path):
    """(Counter de DOCUMENTE per cuvant, numar total de documente).

    `set()` e toata diferenta fata de numararea de frecventa: un cuvant care apare de 300 de ori
    intr-un singur articol contribuie cu 1, nu cu 300. Exact distinctia pe care o masoara Adelman si
    colegii.
    """
    import pyarrow.parquet as pq
    c, n = Counter(), 0
    f = pq.ParquetFile(path)
    for b in f.iter_batches(batch_size=256, columns=["text"]):
        for t in b.column("text").to_pylist():
            c.update(set(TOKEN.findall(t.lower())))
            n += 1
    return c, n


def tabel(c, n_doc):
    w = pd.DataFrame({"word": list(c.keys()), "docs": list(c.values())})
    w = w[w["docs"] >= MIN_DOCS]
    w["cd"] = np.maximum(0.0, np.log10(w["docs"] / n_doc * 1e9)).round(2)
    return w.sort_values("docs", ascending=False).reset_index(drop=True)


def main():
    os.makedirs(DEST, exist_ok=True)
    sys.path.insert(0, HERE)
    from mlsp_common import load_mlsp
    from solution_bert import normalize_token

    ml = load_mlsp("test")
    L = ["# Diversitate contextuala, din Wikipedia", "",
         "Generat de `build_ctx_div.py`. In cate DOCUMENTE distincte apare cuvantul, normalizat ca "
         "rata, pe aceeasi scara ca `zipf`. Sursa: `wikimedia/wikipedia`, dump 20231101, un shard "
         "per limba pentru cele opt mari si dump-ul intreg pentru `si` si `fil`.", ""]
    rows = []
    for wiki, lg in LANGS.items():
        p = os.path.join(SRC, f"{wiki}.parquet")
        if not os.path.exists(p):
            print(f"[{wiki}] {p} lipseste, se sare", flush=True)
            continue
        print(f"[{wiki}] numar documente ...", flush=True)
        c, n_doc = numara(p)
        t = tabel(c, n_doc)
        t.to_csv(os.path.join(DEST, f"{wiki}.csv.gz"), index=False, compression="gzip")
        # acoperirea pe tintele de test ale limbii
        tab = set(t["word"])
        g = ml[ml["lang"] == lg]
        hit = sum(1 for tok in g["token"] if normalize_token(str(tok)).lower() in tab)
        rows.append(dict(lang=lg, wiki=wiki, documente=n_doc, tipuri=len(t),
                         tinte=len(g), acoperite=hit, acoperire=round(100 * hit / max(1, len(g)), 1)))
        print(f"[{wiki}] {n_doc:,} documente, {len(t):,} tipuri, acoperire "
              f"{100 * hit / max(1, len(g)):.1f}%", flush=True)

    t = pd.DataFrame(rows).set_index("lang")
    L += ["```", t.to_string(), "```", "",
          "`acoperire` e procentul tintelor de test gasite ca forma EXACTA in tabel. Fara backoff: "
          "diversitatea contextuala a unui prefix nu e diversitatea cuvantului, iar `build_freq_tail` "
          "a masurat deja ca backoff-ul pe prefix pierde pe filipineza (-0.0097), care foloseste "
          "infixe si reduplicare.", ""]
    dest = os.path.join(OUT, "e_ctx_div.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
