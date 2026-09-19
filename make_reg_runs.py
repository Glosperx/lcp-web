"""Ruleaza matricea encoder x regresor pentru semnalul A, o rulare per casuta, si o cronometreaza.

De ce un driver si nu o bucla in shell. Trei lucruri se vor uitate altfel, si toate trei au costat
timp in proiect:

  1. **Calea de iesire se calculeaza aici cu aceeasi regula ca `_p()` din `finetune_xlmr.py`**, deci
     saritul peste ce exista deja e sigur. Fara el, o reluare dupa o sesiune intrerupta ar re-rula
     o ora de CPU degeaba, sau mai rau, ar re-rula NUMAI o parte si ar lasa doua configuratii
     amestecate intr-un tabel.
  2. **Jurnalul**. `analysis_regresor.py` citeste CSV-urile de pe disc si nu poate sti daca unul
     lipseste fiindca a picat rularea sau fiindca n-a fost cerut. Jurnalul spune care.
  3. **Serial, nu paralel.** `krr-rbf` are un varf de ~4.5 GB (kernel exact 13.5k x 13.5k), iar
     `extratrees` ia deja toate nucleele prin `n_jobs=-1`. Paralelizarea ar da swap, nu viteza.

Nu atinge nimic din ce e publicat: fiecare rulare scrie la calea ei, cu sufixul `_reg-<nume>`, iar
`blend` (sufix gol, adica fisierul adoptat) NU e in lista si nu se poate cere din greseala.

Rulare:
    python make_reg_runs.py                      # tot ce lipseste
    python make_reg_runs.py --encodere xlmr      # numai un encoder
    python make_reg_runs.py --doar krr-rbf ard   # numai niste regresori
    python make_reg_runs.py --uscat              # spune ce ar rula, fara sa ruleze
"""
import argparse
import os
import subprocess
import sys
import time

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
PY = sys.executable
JURNAL = os.path.join(OUT, "_reg_runs_log.csv")

# Sufixul de encoder din `_p()`: gol la xlmr, ca fisierul publicat.
ENC_SUF = {"xlmr": "", "e5": "_e5", "labse": "_labse"}

# Jumatatea LINIARA, axa neatinsa pana acum. Grila de alpha e aici ca sa fie CERNUTA LOLO mai tarziu,
# nu ca sa se aleaga cel mai bun pe test.
LINIARI = ["lasso", "elasticnet",
           "ridge-a30", "ridge-a100", "ridge-a1000", "ridge-a3000", "ridge-a10000", "ridge-a30000",
           "lasso-a1e-4", "lasso-a3e-4", "lasso-a1e-3", "lasso-a3e-3", "lasso-a3e-2",
           "pls-k4", "pls-k8", "pls-k16", "pls-k32", "pls-k64",
           "huber", "bayesridge", "ard", "krr-rbf", "svr-lin"]
# Partenerii, plus `ridge` care e punctul alpha=300 al grilei. Pe xlmr exista deja toti trei.
PARTENERI = ["ridge", "hgb", "extratrees"]

# ---------------------------------------------------------------------------------------------
# Sesiunea OBIECTIVULUI (26 aug). Listele stau AICI, pe clase de mecanism, si nu in istoricul de
# shell, din doua motive. Unul: sesiunea trebuie sa fie reluabila fara sa-si aminteasca nimeni ce
# s-a dat lui `--doar`. Doi, si conteaza mai mult: clasa de mecanism e ceea ce se compara la final,
# iar daca apartenenta la clasa s-ar scrie dupa ce se vad reziduurile, comparatia n-ar insemna nimic.
# Aceleasi clase sunt scrise si in `output/_predictii_obiectiv.md`, inainte de orice rulare.

# Alta FORMA de functie, acelasi loss, aceeasi tinta. Capacitatea e egalata cu incumbentul (8 foi =
# adancime 3), nu lasata pe implicitul bibliotecii, ca diferenta sa se poata atribui.
ARBORI = ["lgbm-l8", "lgbmlin-l8", "cat-d3", "rf-n300", "mlp-h128", "knn-k50"]
# Acelasi model, aceeasi tinta, ALTA pierdere. Singura comparatie in care nimic altceva nu se schimba.
LOSS = ["hgb-abs", "hgb-q50"]
# Se prezice alt FUNCTIONAL al aceleiasi etichete.
TINTA = ["tt-rank-ridge", "tt-rank-hgb", "ttz-rank-ridge", "ttz-rank-hgb",
         "tt-logit2-ridge", "tt-logit2-hgb", "tt-logit005-ridge"]
# Problema nu mai e regresie: clase plus valoare asteptata.
INCADRARE = ["ord-lin-k5", "ord-hgb-k5", "ord-lin-k10", "ord-hgb-k10",
             "orde-lin-k5", "orde-hgb-k5", "clf-lin-k5", "clf-hgb-k5"]
# Acelasi obiectiv si aceeasi familie, dar modelul e potrivit pe ALTCEVA. Nu era in cerere; e singura
# clasa cu mecanism deja masurat in proiect (`extratrees` prin `max_features=0.3`).
INFORMATIE = ["rs-ridge-f3-n10", "rs-hgb-f3-n10", "w-ridge-c1", "w-hgb-c1"]
# Controale de identitate ale invelisurilor. Trebuie sa reproduca baza bit-exact; daca nu, invelisul
# insusi muta cifre si nicio comparatie de mai sus nu inseamna nimic.
CONTROALE = ["tt-id-ridge", "rs-ridge-f10-n1"]

OBIECTIV = ARBORI + LOSS + TINTA + INCADRARE + INFORMATIE + CONTROALE
CLASA = {}
for _n, _c in ((ARBORI, "FAMILIE"), (LOSS, "LOSS"), (TINTA, "TINTA"),
               (INCADRARE, "INCADRARE"), (INFORMATIE, "INFORMATIE"), (CONTROALE, "CONTROL")):
    CLASA.update({x: _c for x in _n})


def cale(enc, reg):
    """Aceeasi regula ca `_p()` din `finetune_xlmr.py`, pentru `--lemma-freq --afeat fert_inloc`."""
    return os.path.join(OUT, f"e1_frozen_preds{ENC_SUF[enc]}_reg-{reg}_lemma_fert_inloc.csv")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--encodere", nargs="+", default=list(ENC_SUF), choices=list(ENC_SUF))
    ap.add_argument("--doar", nargs="+", default=None, help="numai regresorii dati")
    ap.add_argument("--uscat", action="store_true", help="listeaza, nu ruleaza")
    ap.add_argument("--force", action="store_true", help="re-ruleaza si ce exista deja")
    ap.add_argument("--grup", nargs="+", default=None,
                    choices=["liniari", "parteneri", "arbori", "loss", "tinta", "incadrare",
                             "informatie", "controale", "obiectiv"],
                    help="ruleaza o clasa intreaga de mecanism, in loc sa se enumere numele")
    a = ap.parse_args(argv)

    GRUPURI = {"liniari": LINIARI, "parteneri": PARTENERI, "arbori": ARBORI, "loss": LOSS,
               "tinta": TINTA, "incadrare": INCADRARE, "informatie": INFORMATIE,
               "controale": CONTROALE, "obiectiv": OBIECTIV}
    if a.grup:
        regs = [r for g in a.grup for r in GRUPURI[g]]
    elif a.doar:
        regs = a.doar
    else:
        regs = LINIARI + PARTENERI
    plan = [(e, r) for e in a.encodere for r in regs]
    lipsa = [(e, r) for e, r in plan if a.force or not os.path.exists(cale(e, r))]
    gata = len(plan) - len(lipsa)
    print(f"[reg] {len(plan)} casute cerute, {gata} deja pe disc, {len(lipsa)} de rulat", flush=True)
    if a.uscat:
        for e, r in lipsa:
            print(f"       {e:6s} {r:14s} -> {os.path.relpath(cale(e, r), HERE)}")
        return 0

    rand = []
    t00 = time.time()
    for i, (e, r) in enumerate(lipsa, 1):
        log = os.path.join(OUT, f"_reg_log_{e}_{r}.txt")
        cmd = [PY, os.path.join(HERE, "finetune_xlmr.py"), "--frozentrial", "--lemma-freq",
               "--afeat", "fert_inloc", "--encoder", e, "--regressor", r]
        t0 = time.time()
        with open(log, "w", encoding="utf-8") as f:
            cod = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=HERE)
        dt = time.time() - t0
        ok = cod == 0 and os.path.exists(cale(e, r))
        print(f"[{i:3d}/{len(lipsa)}] {e:6s} {r:14s} {dt:6.1f}s  "
              f"{'OK' if ok else f'CADE (cod {cod}, vezi {os.path.basename(log)})'}"
              f"   [{(time.time()-t00)/60:.0f} min de la start]", flush=True)
        rand.append({"encoder": e, "regresor": r, "clasa": CLASA.get(r, ""),
                     "secunde": round(dt, 1), "cod": cod, "ok": ok,
                     "csv": os.path.relpath(cale(e, r), HERE) if ok else ""})
        if ok:
            os.remove(log)

    d = pd.DataFrame(rand)
    if os.path.exists(JURNAL):
        d = pd.concat([pd.read_csv(JURNAL), d], ignore_index=True)
    d.to_csv(JURNAL, index=False)
    rele = [x for x in rand if not x["ok"]]
    print(f"\n[reg] gata in {(time.time()-t00)/60:.1f} min, {len(rand)-len(rele)} OK, "
          f"{len(rele)} cazute -> {os.path.relpath(JURNAL, HERE)}")
    for x in rele:
        print(f"       CAZUT {x['encoder']} {x['regresor']}")
    return 1 if rele else 0


if __name__ == "__main__":
    sys.exit(main())
