"""Tabel de frecventa pentru limbile de coada, unde `wordfreq` nu ajunge.

De ce exista. Pe sinhaleza `wordfreq` nu serveste limba deloc: `zipf_safe` intoarce
`disponibil = False` pentru toate cele 600 de randuri de test, deci una din cele trei trasaturi
lexicale ale semnalului A pur si simplu nu exista acolo. Pe filipineza limba e servita, dar 152 din
570 de tinte (26.7%) au zipf 0, de patru ori mai mult decat urmatoarea limba (catalana, 7.0%).
Sunt exact cele doua limbi pe care sistemul merge cel mai prost.

Sursa: Wikipedia, prin parquet-urile `wikimedia/wikipedia` (dump 20231101), descarcate in
`data/wiki_tail/`. **Asimetria de sursa se declara**: celelalte opt limbi iau frecventa din `wordfreq`,
care agrega subtitrari, web, stiri si Wikipedia, iar si si fil o iau numai din Wikipedia. O comparatie
intre limbi facuta pe cifrele astea e in parte o comparatie intre corpusuri.

Capcana platita, si merita scrisa fiindca nu crapa. Prima versiune folosea
`re.findall(r"[^\\W\\d_]+")`. In Python, `\\w` NU cuprinde semnele vocalice sinhaleze, care sunt in
categoria Unicode Mn, deci fiecare cuvant sinhalez se sparge in consoane separate:
`ලංකාව` devine `ල`, `ක`, `ව`. Tabelul ar fi iesit plin de litere izolate, cu frecvente uriase, si
nimic nu s-ar fi plans. Se foloseste `regex` cu `[\\p{L}\\p{M}]`, care pastreaza si ZWJ-ul din
interiorul conjunctelor sinhaleze.

Scara: aceeasi conventie ca `wordfreq`, adica zipf = log10(aparitii la un miliard de cuvinte),
taiat la 0.

Rulare, ~2 minute:
  python build_freq_tail.py
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
SRC = os.path.join(DATA, "wiki_tail")
DEST = os.path.join(DATA, "freq_tail")

# Litere, semne diacritice combinate, si cei doi separatori de latime zero care apar INTERIOR de
# cuvant in scrierea sinhaleza. Tot restul, inclusiv cifrele, e separator.
TOKEN = regex.compile(r"[\p{L}\p{M}‌‍]+")
LANGS = {"si": "si", "tl": "fil"}       # cheia = fisierul wiki, valoarea = codul de limba MLSP
MIN_PREFIX = 4                           # lungimea minima a unui prefix acceptat la backoff


def numara(path):
    import pyarrow.parquet as pq
    c = Counter()
    f = pq.ParquetFile(path)
    for b in f.iter_batches(batch_size=512, columns=["text"]):
        for t in b.column("text").to_pylist():
            c.update(TOKEN.findall(t.lower()))
    return c


def tabel(c):
    tot = sum(c.values())
    w = pd.DataFrame({"word": list(c.keys()), "count": list(c.values())})
    w["zipf"] = np.maximum(0.0, np.log10(w["count"] / tot * 1e9)).round(2)
    return w.sort_values("count", ascending=False).reset_index(drop=True), tot


def main():
    os.makedirs(DEST, exist_ok=True)
    sys.path.insert(0, HERE)
    from mlsp_common import load_mlsp, zipf_safe
    from solution_bert import normalize_token

    ml = load_mlsp("test")
    L = ["# Frecventa pentru limbile de coada, din Wikipedia", "",
         "Generat de `build_freq_tail.py`. Sursa: `wikimedia/wikipedia`, dump 20231101.", ""]
    rez = {}
    for wiki, lg in LANGS.items():
        p = os.path.join(SRC, f"{wiki}.parquet")
        if not os.path.exists(p):
            sys.exit(f"{p} lipseste")
        print(f"[{wiki}] numar unigrame ...", flush=True)
        c = numara(p)
        t, tot = tabel(c)
        t.to_csv(os.path.join(DEST, f"{wiki}.csv.gz"), index=False, compression="gzip")
        rez[lg] = (t, tot)
        print(f"[{wiki}] {tot:,} tokeni, {len(t):,} tipuri -> {DEST}/{wiki}.csv.gz", flush=True)
        L += [f"## `{lg}` (wiki `{wiki}`)", "",
              f"- {tot:,} tokeni, {len(t):,} tipuri distincte",
              f"- cele mai frecvente 8: " + ", ".join(f"`{w}` ({z})" for w, z in
                                                      zip(t["word"][:8], t["zipf"][:8])), ""]

    # ---------------------------------------------------------------- acoperirea pe tintele MLSP
    L += ["## Acoperirea pe tintele de test, in trepte de backoff", "",
          "Treapta 1 e forma exacta. Treapta 2 e cel mai lung PREFIX de cel putin "
          f"{MIN_PREFIX} caractere care apare in tabel, ca inlocuitor de stem pentru limbile "
          "aglutinante care sufixeaza. Treapta 3 e primul subword al tokenizerului XLM-R, care e o "
          "segmentare invatata si nu cere niciun lematizator.", ""]
    from transformers import AutoTokenizer
    tk = AutoTokenizer.from_pretrained("xlm-roberta-base")
    rows = []
    for lg, (t, tot) in rez.items():
        tab = dict(zip(t["word"], t["zipf"]))
        g = ml[ml["lang"] == lg]
        n = len(g)
        n1 = n2 = n3 = 0
        exemple = []
        for tok in g["token"]:
            w = normalize_token(str(tok)).lower()
            if w in tab:
                n1 += 1
                continue
            pref = None
            for k in range(len(w) - 1, MIN_PREFIX - 1, -1):
                if w[:k] in tab:
                    pref = w[:k]
                    break
            if pref is not None:
                n2 += 1
                if len(exemple) < 4:
                    exemple.append(f"`{w}` -> `{pref}` ({tab[pref]})")
                continue
            sub = tk.tokenize(" " + w)
            s0 = sub[0].replace("▁", "") if sub else ""
            if s0 and s0 in tab:
                n3 += 1
        vechi = np.array([zipf_safe(normalize_token(str(x)), lg)[0] for x in g["token"]], float)
        rows.append(dict(lang=lg, n=n, wordfreq_ok=int((vechi > 0).sum()),
                         exact=n1, plus_prefix=n1 + n2, plus_subword=n1 + n2 + n3,
                         ramase=n - n1 - n2 - n3))
        L += [f"Exemple de backoff pe prefix, `{lg}`: " + "; ".join(exemple) if exemple else "", ""]
    cov = pd.DataFrame(rows).set_index("lang")
    for c in ("exact", "plus_prefix", "plus_subword"):
        cov[f"pct_{c}"] = (100.0 * cov[c] / cov["n"]).round(1)
    L += ["```", cov.to_string(), "```", "",
          "`wordfreq_ok` e cate tinte aveau frecventa NENULA in sistemul de acum. Pe `si` e zero prin "
          "constructie, fiindca limba nu e servita deloc.", ""]

    dest = os.path.join(OUT, "e_freq_tail.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[-14:]))
    print(f"\n-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
