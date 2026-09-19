"""Doi candidati aproape gratis pentru al treilea semnal, adusi in acelasi format ca C.

Amandoi scriu `output/c_<nume>.csv` cu coloanele `lang, idx, C`, deci intra in
`analysis_c_frontiera.py` si `analysis_c_fuse.py --c-csv` fara nicio linie noua acolo.

## `incertitudine`: imprastierea ansamblului de prompturi, ca semnal ADITIV

`fuse_ab.h_from_dist` calculeaza deja doua marimi din distributiile salvate in
`output/dist/gemma4-12b-4bit_test.csv`, la temperatura aleasa LOLO, adica exact cea prin care trece
semnalul B adoptat: entropia medie a celor doua distributii temperate, si divergenta Jensen-Shannon
intre prompturi.

**Amandoua au fost deja testate, si au murit, dar ca PONDERE per item**: `w_i = clip(w + a*h_i, 0, 1)`
alege `a = 0` pe 10 limbi din 10, si la semnal real, si pe cinci seminte de zgomot. Ca al treilea
TERMEN aditiv sunt alt obiect: o pondere modifica amestecul existent, un termen aditiv adauga o
directie noua. Nu e o reluare, si nu se raporteaza ca si cum ar fi.

## `vecinatate`: densitatea vecinatatii semantice, din cache

Media similaritatii cosinus la cei mai apropiati `k` vecini din ACEEASI limba, exclusiv el insusi, pe
embeddingurile deja pe disc (`data/emb_mlsp10_xlmr_last4_5624.npy`). Zero inferenta.

Vecinii se cauta in interiorul limbii, nu peste tot: intre limbi similaritatea cosinus e dominata de
componenta de limba a spatiului, deci un vecin "apropiat" ar fi doar un alt cuvant din aceeasi limba,
si marimea ar masura tot limba.

Predictia scrisa inainte, si e pesimista: marimea e derivata din CHIAR embeddingul pe care e antrenat
semnalul A, deci `rho` cu A ar trebui sa fie mare, si frontiera spune ca atunci nu are cum sa treaca.
Se masoara fiindca costa un minut, nu fiindca ar fi promitatoare.

Rulare:
  python analysis_alti_candidati.py
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

DIST = os.path.join(OUT, "dist", "gemma4-12b-4bit_test.csv")
EMB = os.path.join(HERE, "data", "emb_mlsp10_xlmr_last4_5624.npy")
FUZ = os.path.join(OUT, "fusion_preds_lolo_adoptat_temp.csv")
K = 10


def scrie(nume, lang, idx, val):
    p = os.path.join(OUT, f"c_{nume}.csv")
    pd.DataFrame({"lang": lang, "idx": idx, "C": val}).to_csv(p, index=False)
    print(f"-> {p}  ({len(idx)} randuri, {int((~np.isfinite(val)).sum())} nefinite)")
    return p


def main():
    fz = pd.read_csv(FUZ)
    lang, idx = fz["lang"].values, fz["idx"].values

    # --- incertitudinea lui B, prin chiar functia care o calculeaza pentru varianta-pondere
    import fuse_ab
    for kind in ("entropie", "dezacord"):
        H, nume = fuse_ab.h_from_dist(kind, DIST, 0)
        v = np.array([H.get(int(i), np.nan) for i in idx], float)
        print(f"[{kind}] {nume}")
        scrie(kind, lang, idx, v)

    # --- densitatea vecinatatii semantice, in interiorul limbii
    E = np.load(EMB).astype(np.float32)
    ok = np.load(EMB.replace(".npy", "_ok.npy"))
    if not ok.all():
        print(f"[vecinatate] {int((~ok).sum())} randuri fara embedding, ies NaN")
    En = E / np.clip(np.linalg.norm(E, axis=1, keepdims=True), 1e-9, None)
    v = np.full(len(idx), np.nan)
    for lg in sorted(set(lang)):
        m = np.flatnonzero((lang == lg))
        rows = idx[m]
        good = ok[rows]
        X = En[rows[good]]
        S = X @ X.T
        np.fill_diagonal(S, -np.inf)                 # exclude itemul insusi
        k = min(K, S.shape[0] - 1)
        # media celor mai apropiati k: mare = vecinatate DENSA, adica multe cuvinte similare
        v[m[good]] = np.sort(S, axis=1)[:, -k:].mean(1)
    scrie("vecinatate", lang, idx, v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
