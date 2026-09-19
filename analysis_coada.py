"""Coada: ce se poate face pentru sinhaleza si filipineza, unde resursele lexicale lipsesc.

Punctul de plecare, masurat: pe `si` wordfreq nu serveste limba deloc, deci 600 din 600 de tinte n-au
frecventa; pe `fil` limba e servita dar 152 din 570 de tinte sunt OOV, de patru ori mai mult decat
urmatoarea limba. Sunt exact cele doua limbi pe care sistemul merge cel mai prost (A 0.3166 si 0.4159).

Trei intrebari, in ordinea in care se pun:
  1. PLAFONUL: cat valoreaza coloana de frecventa acolo unde EXISTA? Se raspunde cu ablatia
     `--no-freq`, care o anuleaza peste tot. Cat pierd celelalte opt limbi e o estimare directa a
     ce le lipseste lui si si fil.
  2. CASTIGUL: cat aduce tabelul din Wikipedia, pe cele trei trepte de backoff.
  3. CONTROLUL: celelalte opt limbi trebuie sa ramana neatinse.

Rulare, ~15 secunde, citeste de pe disc:
  python analysis_coada.py
"""
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

REF = "output/e1_frozen_preds_lemma_fert_inloc.csv"       # xlmr singur, last4, sistemul de trasaturi
VAR = {"nofreq": "_nofreq", "ft_exact": "_ft-exact", "ft_prefix": "_ft-prefix",
       "ft_subword": "_ft-subword"}
COADA = ["si", "fil"]


def rA(path):
    d = pd.read_csv(path)
    d = d[d["split"] == "test"]
    return {lg: pearsonr(g["p_multi"], g["complexity"])[0] for lg, g in d.groupby("lang")}


def fuz(tag):
    p = os.path.join(OUT, f"fusion_lolo_{tag}.csv")
    if not os.path.exists(p):
        return None
    return pd.read_csv(p)


def main():
    ref = rA(REF)
    langs = sorted(ref)
    L = ["# Coada: frecventa pentru sinhaleza si filipineza", "",
         "Generat de `analysis_coada.py`. Referinta e xlmr SINGUR la `last4`, adica "
         "`e1_frozen_preds_lemma_fert_inloc.csv`, ca diferenta sa fie curat efectul frecventei.", ""]

    tab = {"referinta": ref}
    for k, suf in VAR.items():
        p = os.path.join(OUT, f"e1_frozen_preds{suf}_lemma_fert_inloc.csv")
        if os.path.exists(p):
            tab[k] = rA(p)
    A = pd.DataFrame(tab).loc[langs]

    # --- 1. plafonul
    if "nofreq" in A:
        A["plafon_freq"] = A["referinta"] - A["nofreq"]
        alt = [l for l in langs if l not in COADA]
        L += ["## 1. Plafonul: cat valoreaza coloana de frecventa acolo unde exista", "",
              "`plafon_freq` e cat pierde bratul A cand coloana de frecventa se anuleaza. Pe `si` "
              "cifra e aproape zero PRIN CONSTRUCTIE, fiindca acolo coloana era deja goala; tocmai "
              "asta o face masura a ceea ce lipseste.", "",
              "```", A[["referinta", "nofreq", "plafon_freq"]].round(4).to_string(), "```", "",
              f"Pe cele opt limbi cu frecventa reala, pierderea medie e "
              f"**{A.loc[alt, 'plafon_freq'].mean():+.4f}**; pe `si` "
              f"**{A.loc['si', 'plafon_freq']:+.4f}** si pe `fil` "
              f"**{A.loc['fil', 'plafon_freq']:+.4f}**.", ""]

    # --- 2. castigul
    got = [k for k in VAR if k.startswith("ft_") and k in A]
    if got:
        L += ["## 2. Castigul, pe cele trei trepte de backoff", "",
              "Brat A (`p_multi`) per limba:", "",
              "```", A[["referinta"] + got].round(4).to_string(), "```", "",
              "Diferenta fata de referinta:", "", "```",
              (A[got].sub(A["referinta"], axis=0)).round(4).to_string(), "```", ""]
        for k in got:
            d = A[k] - A["referinta"]
            alt = [l for l in langs if l not in COADA]
            L += [f"- `{k}`: si **{d['si']:+.4f}**, fil **{d['fil']:+.4f}**, "
                  f"celelalte opt (efect indirect, prin datele de antrenare) "
                  f"**{d[alt].mean():+.4f}**, media pe zece **{d.mean():+.4f}**"]
        L += ["", "Pe celelalte opt limbi diferenta NU e zero si nici nu trebuie sa fie: sub LOLO "
              "modelul care prezice limba L se antreneaza pe celelalte noua, ale caror trasaturi "
              "s-au schimbat. E efect indirect prin datele de antrenare, curat de orice efect "
              "direct, exact ca la fixul de lema.", ""]

    # --- fuziunea
    rows = []
    base = fuz("enc_xlmr_now")
    for k in ["referinta"] + list(VAR):
        tag = "enc_xlmr_now" if k == "referinta" else f"cfg_{VAR[k].lstrip('_')}"
        f = fuz(tag)
        if f is None:
            continue
        r = dict(varianta=k, r_fuz=f["r_fuz_raw"].mean())
        for lg in COADA:
            g = f[f["lang"] == lg]
            if len(g):
                r[f"fuz_{lg}"] = float(g["r_fuz_raw"].iloc[0])
        if k != "referinta" and "d_azi" in f:
            r["d_fuz"] = f["d_azi"].mean()
            r["limbi_stricate"] = int((f["d_azi_hi"] < 0).sum())
        rows.append(r)
    if rows:
        Fz = pd.DataFrame(rows).set_index("varianta")
        L += ["## Fuziunea, adica cifra care conteaza", "", "```", Fz.round(6).to_string(), "```", "",
              "`d_fuz` e diferenta PERECHE fata de xlmr singur. `limbi_stricate` numara limbile al "
              "caror interval pereche exclude zero in jos.", ""]

    # --- 3. controlul
    L += ["## 3. Controlul: celelalte opt limbi", "",
          "Verificat separat, cu comparatie constienta de NaN (coloanele de suprafata sunt NaN pe "
          "`ja` si `si`, iar `!=` le-ar raporta ca schimbate la fiecare rulare): **0 randuri "
          "schimbate din 14082** in celelalte opt limbi, pe toate cele trei trepte. Se schimba numai "
          "`si` (600 din 600 pe test, fiindca se muta si indicatorul `freq_na`) si `fil` "
          "(105 la `exact`, 145 la `prefix`, 152 la `subword`).", "",
          "## Limita de resursa, si se declara", "",
          "Corpusul sinhalez are 8.03 milioane de tokeni, deci un cuvant care apare O SINGURA data "
          "primeste zipf 2.10. Aia e o PODEA: sub ea nu se poate distinge nimic, in timp ce celelalte "
          "opt limbi, servite de `wordfreq`, coboara pana la 0. Distributia lui `si` e prin urmare "
          "comprimata (sd 0.80, cea mai mica din set, fata de 0.86-1.14 la celelalte). Nu e un defect "
          "de metoda, e marimea corpusului disponibil, si e chiar observatia care merita scrisa: pe "
          "limba pe care mergem cel mai prost, rezolutia frecventei e limitata de cat text exista.", ""]

    # --- encoderele monolingve: de ce nu intra in protocol
    L += ["## Encoderele monolingve nu sunt compatibile cu protocolul, si de ce", "",
          "Planul prevedea SinBERT si RoBERTa-Tagalog ca membri suplimentari acolo unde exista. "
          "Ideea cade pe un motiv STRUCTURAL, nu pe un scor prost, si merita scris fiindca e o "
          "limitare a protocolului nostru, nu a modelelor lor.", "",
          "Sub LOLO, regresorul care prezice limba L se antreneaza pe CompLex EN plus celelalte noua "
          "limbi, embedate cu ACELASI encoder. Un encoder monolingv sinhalez nu are cum sa reprezinte "
          "franceza sau japoneza, deci antrenarea s-ar face pe reprezentari fara continut. Iar "
          "varianta cealalta, sa antrenam pe etichete sinhaleze, rupe proprietatea zero-label, care e "
          "jumatate din contributia lucrarii.", "",
          "Cat de rau, masurat, ca sa nu ramana un argument teoretic. Fertilitate, adica subword-uri "
          "per tinta:", "", "```",
          "limba   xlmr   sinbert   roberta-tagalog",
          "si      3.32   5.19      21.24",
          "fil     2.37   8.61      1.66",
          "fr      2.02   9.76      3.33",
          "ja      3.37   5.08      9.77",
          "en      1.88   8.93      2.22",
          "```", "",
          "SinBERT sparge celelalte noua limbi in 4.15 ori mai multe bucati decat XLM-R (mediana), "
          "iar RoBERTa-Tagalog in 1.65 ori, si pe sinhaleza cade in fallback pe octeti, 21.24 bucati "
          "per tinta. **Cifra care surprinde:** SinBERT fragmenteaza sinhaleza mai rau decat XLM-R "
          "(5.19 fata de 3.32), desi e monolingv, fiindca are un vocabular de 52.000 fata de 250.000. "
          "Deci nici macar avantajul de tokenizare pe limba proprie nu e garantat.", "",
          "Ce ramane utilizabil dintr-un model monolingv, fara sa strice protocolul: un scalar per "
          "item care nu cere regresor cross-lingual, de exemplu surprisal-ul din capul de MLM. Nu s-a "
          "rulat in sesiunea asta si ramane declarat ca directie.", "",
          "Contrastul cu Glot500 e exact aici: Glot500 e UN singur model aplicat la toate cele zece "
          "limbi, deci intra in protocol fara nicio regula per limba, si tokenizeaza si si fil la "
          "nivel de cuvant intreg.", ""]

    dest = os.path.join(OUT, "e_coada.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
