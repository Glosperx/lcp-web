"""E.13. Controlul de al TREILEA prompt: castigul lui FS3K e specific few-shot-ului sau nu?

Intrebarea, si e de identificare a mecanismului, nu de gasire a unei configuratii mai bune.
`FS3K` urca fuziunea cu +0.004642, dar few-shot-ul SINGUR pierde pe test, -0.0246 pe B. Deci castigul
nu vine din faptul ca promptul few-shot ar fi bun, si prima explicație plauzibila e reducerea de
varianta de la doi la trei membri. Daca asa e, atunci **orice** al treilea prompt de calitate
comparabila da acelasi castig, si nimic din rezultat nu e despre few-shot cross-lingual.

Asta conteaza pentru ce se poate SCRIE, nu doar pentru ce se adopta. Motivul pentru care few-shot
merita rulat, din rândul 10 al lui `output/e_prioritate.md`, era revendicarea fata de G-Eval, care e
3-shot in limba tinta. Revendicarea cere ca exemplele sa ajute. Daca rubrica da acelasi castig fara
nicio eticheta, revendicarea nu exista si fraza corecta in paper e „trei prompturi bat doua".

Trei membri alternativi, alesi pe trial INAINTE de rularea pe test, din
`output/promptlab_gemma4-12b-4bit.csv`, care avea toate variantele masurate:

  `rubrica`  al doilea cel mai bun al treilea membru pe trial, +0.6904 fata de +0.7109 al few-shot-ului
  `marcat`   practic egal cu rubrica pe trial, +0.6895, deci un al doilea punct la aceeasi calitate
  `learner`  SUB perechea de doua prompturi pe trial, +0.6773 fata de +0.6860: control negativ

**Ce NU e acest raport.** Nu e o cautare de configuratie. Daca un membru alternativ iese peste
few-shot, aia e dovada CONTRA povestii few-shot, nu un candidat nou de adoptat: ar fi al saptelea
argmax pe aceleasi randuri de test. O adoptare pe baza lui ar cere o prespecificare proprie.

Rulare:
  python make_fs_dist.py --variant v2_rubrica --tag rubrica
  python make_fs_runs.py --dir bakeoff_test_R3 --src output/dist/rubrica_..._test.csv --src <sistem>
  python analysis_al3lea.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_al3lea.md")
REF = os.path.join(OUT, "fusion_preds_lolo_adoptat_temp.csv")
REF_TAB = os.path.join(OUT, "fusion_lolo_adoptat_temp.csv")
SYS_DIST = os.path.join(OUT, "dist", "gemma4-12b-4bit_test.csv")

# (eticheta, tag-ul fisierului de distributii, prefixul directoarelor, ce era pe trial)
MEMBRI = [("few-shot", "fewshot", "FS3", "+0.7109 ca al treilea pe trial, cel mai bun"),
          ("rubrica", "rubrica", "R3", "+0.6904 pe trial, al doilea"),
          ("marcat", "marcat", "M3", "+0.6895 pe trial, egal cu rubrica"),
          ("learner", "learner", "L3", "+0.6773 pe trial, SUB perechea de doua: control negativ")]

_DOC = []


def emit(*lines):
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def dist_path(tag):
    return os.path.join(OUT, "dist", f"{tag}_gemma4-12b-4bit_test.csv")


def solo_r(tag):
    """r mediu al lui B construit din SINGURUL prompt al fisierului, cu T ales LOLO.

    Trece prin `make_fs_runs`, deci prin exact aceeasi selectie ca a configuratiilor de trei: altfel
    comparatia „solo fata de in ansamblu" ar avea doua diferente, nu una.
    """
    import analysis_dist as ad
    from make_fs_runs import load_srcs, pick_params, b_of
    PL, names = load_srcs([dist_path(tag)])
    if len(names) != 1:
        raise SystemExit(f"{tag}: {len(names)} prompturi, se aștepta 1")
    params, _ = pick_params(PL, "temperatura", ad.T_GRID_EXT)
    return float(np.mean([ad.r_of(b_of(PL[lg]["Ps"], params[lg][0], None), PL[lg]["y"])
                          for lg in sorted(PL)]))


def corel(tag):
    """(r cu promptul expert, r cu promptul scurt), la T=1. Cat de decorelat e membrul nou."""
    import analysis_dist as ad
    from bakeoff_trial import with_context
    a = with_context(pd.read_csv(dist_path(tag)), "test")
    b = with_context(pd.read_csv(SYS_DIST), "test")
    o1, o2 = [], []
    for lg in sorted(a["lang"].unique()):
        ga, gb = a[a["lang"] == lg], b[b["lang"] == lg]
        x = ad.expected(ga[[f"p1_{k}" for k in "12345"]].values.astype(float))
        for col, out in (("p1", o1), ("p2", o2)):
            out.append(ad.r_of(x, ad.expected(gb[[f"{col}_{k}" for k in "12345"]]
                                              .values.astype(float))))
    return float(np.mean(o1)), float(np.mean(o2))


def main():
    import analysis_dist as ad
    from analysis_fewshot import boots_of
    ref_tab = pd.read_csv(REF_TAB)
    sis = float(ref_tab["r_fuz_raw"].mean())
    b_sis = float(ref_tab["r_B_raw"].mean())
    langs = sorted(pd.read_csv(REF)["lang"].unique())
    have = [m for m in MEMBRI if os.path.exists(dist_path(m[1]))
            and os.path.exists(os.path.join(OUT, f"fusion_preds_lolo_fewshot_test_{m[2]}K.csv"))]
    if not have:
        raise SystemExit("niciun membru rulat cap la cap")
    Bref, _ = boots_of(REF, langs)

    emit("# E.13. Controlul de al treilea prompt\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_al3lea.py`. Referinta e sistemul "
         f"adoptat, **r = {sis:.6f}**, cu B = {b_sis:.6f} din doua prompturi.\n",
         __doc__.split("Trei membri")[0].split("\n", 2)[2].strip() + "\n")
    if len(have) < len(MEMBRI):
        emit(f"**Membri nerulati**, deci absenti din tabele: "
             f"{[m[0] for m in MEMBRI if m not in have]}.\n")

    emit("## 1. Semnalul B: promptul singur, si acelasi prompt ca al treilea membru\n",
         "`B solo` e promptul singur, cu T ales LOLO prin exact aceeasi conducta. `B in trei` e "
         "perechea de acum plus el. `castig` e cat aduce ca al treilea membru. Coloanele de corelatie "
         "spun daca membrul e decorelat de cele doua de acum, adica daca aduce informatie sau doar "
         "mediere.\n",
         "| membru | ce era pe trial | B solo | B in trei | B in trei + colaps | castig pe B | "
         "r cu expert | r cu scurt |",
         "|---|---|---|---|---|---|---|---|")
    S = {}
    for nm, tag, pre, doc in have:
        t3 = float(pd.read_csv(os.path.join(OUT, f"fusion_lolo_fewshot_test_{pre}.csv"))
                   ["r_B_raw"].mean())
        t3k = float(pd.read_csv(os.path.join(OUT, f"fusion_lolo_fewshot_test_{pre}K.csv"))
                    ["r_B_raw"].mean())
        so = solo_r(tag)
        c1, c2 = corel(tag)
        S[nm] = dict(solo=so, t3=t3, t3k=t3k, pre=pre)
        emit(f"| `{nm}` | {doc} | {so:+.6f} | {t3:+.6f} | {t3k:+.6f} | **{t3 - b_sis:+.6f}** | "
             f"{c1:.3f} | {c2:.3f} |")
        print(f"    {nm:9s} solo {so:+.4f}  in trei {t3:+.4f}  +colaps {t3k:+.4f}  "
              f"castig {t3 - b_sis:+.6f}  corel {c1:.3f}/{c2:.3f}", flush=True)
    emit("")

    emit("## 2. Fuziunea, interval PERECHE al mediei fata de sistemul de acum\n",
         "`limbi stricate` se citeste PRIMA, ca in `output/e_fewshot.md`.\n",
         "| configuratie | membru al treilea | colaps | limbi stricate | r mediu | diferenta | "
         "CI 95% pereche | P(>0) |",
         "|---|---|---|---|---|---|---|---|")
    det = {}
    for nm, tag, pre, doc in have:
        for suf, k_doc in (("", "nu"), ("K", "da")):
            f = os.path.join(OUT, f"fusion_preds_lolo_fewshot_test_{pre}{suf}.csv")
            if not os.path.exists(f):
                continue
            Bk, rk = boots_of(f, langs)
            dm, lo, hi, pp = ad.mean_diff_ci(Bk, Bref)
            dn = []
            for i, lg in enumerate(langs):
                m = min(len(Bk[i]), len(Bref[i]))
                dv = Bk[i][:m] - Bref[i][:m]
                if float(np.percentile(dv, 97.5)) < 0:
                    dn.append(lg)
            det[pre + suf] = dict(nm=nm, k=k_doc, dm=dm, lo=lo, hi=hi, pp=pp,
                                  r=float(rk.mean()), dn=dn)
            emit(f"| `{pre}{suf}` | {nm} | {k_doc} | {', '.join(dn) if dn else '**niciuna**'} | "
                 f"**{float(rk.mean()):.6f}** | {dm:+.6f} | [{lo:+.6f}, {hi:+.6f}] | {pp:.1%} |")
            print(f"    {pre+suf:5s} r {float(rk.mean()):.6f}  d {dm:+.6f} "
                  f"[{lo:+.6f},{hi:+.6f}]  stricate={dn or '-'}", flush=True)
    emit("")

    # --- verdictul mecanismului, fara nicio cifra scrisa de mana
    fs = S.get("few-shot")
    alt = {k: v for k, v in S.items() if k != "few-shot"}
    emit("## Verdict: e specific few-shot-ului?\n")
    if fs and alt:
        best_alt = max(alt, key=lambda k: alt[k]["t3"])
        d_fs = fs["t3"] - b_sis
        d_alt = alt[best_alt]["t3"] - b_sis
        emit(f"Pe semnalul B, few-shot ca al treilea membru aduce **{d_fs:+.6f}**. Cel mai bun membru "
             f"alternativ, `{best_alt}`, aduce **{d_alt:+.6f}**, adica {d_alt - d_fs:+.6f} fata de el. "
             f"Ordinea membrilor pe test, dupa castigul pe B: "
             + ", ".join(f"`{k}` {S[k]['t3'] - b_sis:+.6f}"
                         for k in sorted(S, key=lambda k: -S[k]["t3"])) + ".\n",
             "Corelatia dintre castigul ca al treilea membru si calitatea membrului luat SINGUR, peste "
             f"cei {len(S)} membri: "
             f"r = {np.corrcoef([S[k]['solo'] for k in S], [S[k]['t3'] for k in S])[0, 1]:+.3f}. "
             "Daca e mare, ce conteaza e calitatea promptului, nu ce fel de prompt e.\n",
             ("**Castigul NU e specific few-shot-ului**: cel putin un membru fara nicio eticheta "
              "ajunge la cel puțin 80% din el, deci fraza corecta in paper e `trei prompturi bat "
              "doua`, si revendicarea fata de G-Eval nu se poate scrie."
              if d_alt >= 0.8 * d_fs else
              "**Castigul e specific few-shot-ului**: cel mai bun membru alternativ rams sub 80% din "
              "el, desi pe trial era la 97%. Deci exemplele etichetate din celelalte limbi aduc ceva "
              "ce un prompt oarecare nu aduce, si revendicarea fata de G-Eval se poate scrie chiar "
              "daca promptul singur pierde.") + "\n")
    else:
        emit("Nu se poate decide: lipsesc membri.\n")
    print(f"[E13] -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
