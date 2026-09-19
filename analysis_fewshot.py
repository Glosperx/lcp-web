"""E.12. Few-shot din CELELALTE limbi, pe test: aduna cele patru configuratii intr-un singur tabel.

`fuse_ab.py` scrie cate un raport per configuratie, si in fiecare raport apar DOUA statistici `P(>0)`
diferite: media pe limbi a lui P(>0) in tabelul per limba, si P(>0) al MEDIEI in secțiunea
"Intervalele mediei". A doua e cea care se citeaza. Aici se recalculeaza a doua, o singura data,
pentru toate configuratiile, din predictiile per instanta, ca sa nu se poata citi din greseala
cealalta.

Ordinea coloanelor e ordinea in care se citesc: **`limbi stricate` INAINTE de `medie`**. Asa a fost
respins `distTpp` la 0.685763 si `prio_KW` la 0.685727, desi amandoua aveau media mai mare decat
sistemul.

Configuratiile, si care e prespecificata:

  `FS`    few-shot singur, temperatura aleasa LOLO pe grila extinsa. CERUTA, e configuratia din brief.
  `FSK`   few-shot singur, plus partitia de unire a cifrelor aleasa LOLO. CERUTA.
  `FS3`   media celor TREI prompturi: few-shot plus cele doua ale sistemului, care sunt deja pe disc.
          NU e cerută in brief. Motivul pentru care intra, si el e verificabil ca a fost formulat
          INAINTE de orice cifra de test: pe trial, din fisierul deja existent
          `output/promptlab_gemma4-12b-4bit.csv`, media celor trei da +0.7109 fata de +0.6970 al
          few-shot-ului singur si +0.6860 al celor doua de acum. Costa zero inferenta in plus.
  `FS3K`  ansamblul de trei, plus partitia. Aceeasi motivatie.

Cele patru sunt o MULTIPLICITATE de patru si se declara ca atare: patru intervale la 95% pe aceleasi
randuri de test nu sunt patru teste independente, iar alegerea intre ele, daca s-ar face pe cifra de
test, e chiar bifurcatia din `output/e_prioritate.md`. Aici nu se alege nimic, se raporteaza.

Rulare:
  python analysis_fewshot.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_fewshot.md")
REF = os.path.join(OUT, "fusion_preds_lolo_adoptat_temp.csv")
REF_TAB = os.path.join(OUT, "fusion_lolo_adoptat_temp.csv")
# Cifra de referinta NU e o constanta in fisierul asta: se citeste din REF_TAB la fiecare rulare.
# `SIS = 0.664555` hardcodat a facut deja un raport sa se contrazica singur, fara nicio eroare.

CFG = [("FS", "few-shot singur, temperatura LOLO", "ceruta in brief"),
       ("FSK", "few-shot singur, plus unirea cifrelor", "ceruta in brief"),
       ("FS3", "media celor trei prompturi, temperatura LOLO", "cernuta pe trial inainte de test"),
       ("FS3K", "media celor trei, plus unirea cifrelor", "cernuta pe trial inainte de test"),
       ("FS3P", "cele trei, cate un T per prompt", "cerută de Alexandru, 22 aug"),
       ("FS3KP", "cele trei, T per prompt, plus unirea cifrelor", "cerută de Alexandru, 22 aug")]

_DOC = []


def emit(*lines):
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def boots_of(path, langs):
    """[esantioane bootstrap ale lui r, per limba] pentru un fisier de predictii.

    `boot_r_ci` are seed fix si primeste acelasi vector de contexte in toate configuratiile, deci
    reesantionarea k e aceeasi peste tot si diferentele ies PERECHE.
    """
    import analysis_dist as ad
    d = pd.read_csv(path)
    out, r = [], []
    for lg in langs:
        g = d[d["lang"] == lg]
        b = ad.boot_one(g["y"].values.astype(float), g["p_fuz"].values.astype(float),
                        g["ctx"].values)
        out.append(b["boot"])
        r.append(b["r"])
    return out, np.array(r, float)


def main():
    import analysis_dist as ad
    if not os.path.exists(REF):
        raise SystemExit(f"{REF} lipseste")
    ref_tab = pd.read_csv(REF_TAB)
    sis = float(ref_tab["r_fuz_raw"].mean())
    langs = sorted(pd.read_csv(REF)["lang"].unique())
    have = [(k, doc, why) for k, doc, why in CFG
            if os.path.exists(os.path.join(OUT, f"fusion_preds_lolo_fewshot_test_{k}.csv"))]
    if not have:
        raise SystemExit("nicio configuratie rulata: lipsesc output/fusion_preds_lolo_fewshot_test_*.csv")

    Bref, rref = boots_of(REF, langs)
    emit("# E.12. Few-shot din celelalte limbi, pe test\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_fewshot.py`. Referinta e "
         f"sistemul adoptat, **r = {sis:.6f}**, din `output/fusion_lolo_adoptat_temp.csv`. "
         f"Toate cifrele pe cele {len(langs)} limbi de test, agregate ca MEDIE pe limbi, nu pooled.\n",
         __doc__.split("Configuratiile")[0].split("\n", 2)[2].strip() + "\n")

    # --- ce s-a masurat de fapt: semnalul B singur, inainte de fuziune
    emit("## 1. Semnalul B singur, inainte de fuziune\n",
         "Fuziunea amesteca B cu A si cu ponderea, deci un castig pe B se poate dilua sau se poate "
         "amplifica. Coloana asta spune cat a mutat promptul in chiar marimea pe care o schimba.\n",
         "| configuratie | ce e | B mediu | fata de B-ul de acum |", "|---|---|---|---|")
    b_sis = float(ref_tab["r_B_raw"].mean())
    emit(f"| sistemul de acum | doua prompturi zero-shot, temperatura LOLO | {b_sis:+.6f} | - |")
    for k, doc, _ in have:
        t = pd.read_csv(os.path.join(OUT, f"fusion_lolo_fewshot_test_{k}.csv"))
        bk = float(t["r_B_raw"].mean())
        emit(f"| `{k}` | {doc} | {bk:+.6f} | {bk - b_sis:+.6f} |")
    emit("")

    # --- tabelul principal
    emit("## 2. Fuziunea, cu intervalul PERECHE al mediei\n",
         "`limbi stricate` e coloana care se citeste PRIMA: o limba stricata cu interval pereche care "
         "exclude zero respinge configuratia oricare ar fi media. `P(>0)` de aici e al MEDIEI, nu media "
         "pe limbi a lui P(>0) din tabelele lui `fuse_ab`.\n",
         "| configuratie | de ce e in tabel | limbi stricate | limbi urcate | r mediu | fata de "
         f"{sis:.6f} | CI 95% pereche | P(>0) |",
         "|---|---|---|---|---|---|---|---|")
    det = {}
    for k, doc, why in have:
        Bk, rk = boots_of(os.path.join(OUT, f"fusion_preds_lolo_fewshot_test_{k}.csv"), langs)
        dm, lo, hi, pp = ad.mean_diff_ci(Bk, Bref)
        rows, dn, up = [], [], []
        for i, lg in enumerate(langs):
            m = min(len(Bk[i]), len(Bref[i]))
            dv = Bk[i][:m] - Bref[i][:m]
            l2, h2 = float(np.percentile(dv, 2.5)), float(np.percentile(dv, 97.5))
            rows.append((lg, float(np.mean(dv)), l2, h2))
            (dn if h2 < 0 else up if l2 > 0 else []).append(lg)
        det[k] = dict(rows=rows, dm=dm, lo=lo, hi=hi, pp=pp, r=float(rk.mean()), dn=dn, up=up)
        emit(f"| `{k}` | {why} | {', '.join(dn) if dn else '**niciuna**'} | "
             f"{', '.join(up) if up else 'niciuna'} | **{float(rk.mean()):.6f}** | {dm:+.6f} | "
             f"[{lo:+.6f}, {hi:+.6f}] | {pp:.1%} |")
        print(f"    {k:5s} r {float(rk.mean()):.6f}  d {dm:+.6f} [{lo:+.6f},{hi:+.6f}] "
              f"P={pp:.1%}  stricate={dn or '-'}", flush=True)
    emit("")

    emit("### Per limba, fata de sistemul de acum\n",
         "| configuratie | " + " | ".join(langs) + " |", "|---" * (len(langs) + 1) + "|")
    for k in det:
        emit(f"| `{k}` | " + " | ".join(f"{d:+.4f}" for _, d, _, _ in det[k]["rows"]) + " |")
    emit("", "Aceleasi diferente, cu intervalul lor, numai unde intervalul exclude zero:\n",
         "| configuratie | limba | diferenta | CI 95% pereche |", "|---|---|---|---|")
    for k in det:
        for lg, dd, lo, hi in det[k]["rows"]:
            if lo > 0 or hi < 0:
                emit(f"| `{k}` | {lg} | {dd:+.4f} | [{lo:+.4f}, {hi:+.4f}] |")
    emit("")

    # --- verdict, fara nicio cifra scrisa de mana
    best = max(det, key=lambda k: det[k]["dm"])
    D = det[best]
    trece = [k for k in det if det[k]["lo"] > 0 and not det[k]["dn"]]
    emit("## Verdict\n",
         f"Cel mai mare castig pe medie il da `{best}`: r = {D['r']:.6f}, adica {D['dm']:+.6f} fata de "
         f"{sis:.6f}, interval pereche [{D['lo']:+.6f}, {D['hi']:+.6f}], deci "
         f"{ad.zero_out(D['lo'], D['hi'])}, P(>0) = {D['pp']:.1%}. Limbi stricate cu interval care "
         f"exclude zero: {', '.join(D['dn']) if D['dn'] else 'niciuna'}.\n",
         ("Configuratii care trec AMBELE conditii, adica interval pereche care exclude zero in sus si "
          f"nicio limba stricata: {', '.join('`' + k + '`' for k in trece)}."
          if trece else
          "**Nicio configuratie nu trece ambele conditii**: interval pereche care exclude zero in sus "
          "si nicio limba stricata cu interval care exclude zero.") + "\n",
         "Nu se adopta nimic aici. Cele patru configuratii sunt patru intervale pe aceleasi randuri de "
         "test, iar alegerea intre ele pe cifra de test e chiar bifurcatia declarata in "
         "`output/e_prioritate.md`.\n")
    print(f"[E12] -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
