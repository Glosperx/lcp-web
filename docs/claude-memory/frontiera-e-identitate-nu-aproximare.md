---
name: frontiera-e-identitate-nu-aproximare
description: "22 aug 2026 - formula de reducere a variantei reproduce media STANDARDIZATA la 3.3e-16, deci e identitate; ce s-a numit eroarea ei e distanta pana la media BRUTA a lui b_of, si creste cu diferenta de varianta intre membri"
metadata:
  type: project
---

Verificat **22 august 2026**, in `analysis_frontiera.py`, sectiunea "Ce e de fapt frontiera".
Raport: `output/e_frontiera.md`.

## Ce s-a masurat

`r_ens = (suma r_i)/sqrt(n + 2*suma_{i<j} rho_ij)` reproduce corelatia mediei **STANDARDIZATE** a
membrilor la **3.3e-16**, peste toti candidatii si toate cele zece limbi. Nu e o aproximare buna, e o
identitate algebrica: daca fiecare `s_i` are medie 0 si abatere 1, atunci `var(suma s_i)` e chiar
`n + 2*suma rho_ij` si `cov(suma s_i, y)` e `suma r_i * sd(y)`.

## Ce era deci "eroarea"

`make_fs_runs.b_of` mediaza valorile asteptate **BRUTE**, nu standardizate. Cifrele de 0.0003..0.0024
din `output/e_al3lea.md` si -0.000142 pe ansamblul de patru sunt distanta dintre media standardizata
si cea bruta, nu eroarea formulei. Ea creste cu cat deviatiile standard ale membrilor difera:

| candidat | sd membri noi / sd pereche | brut minus standardizat |
|---|---|---|
| lema | 1.05 | +0.0041 |
| fara context | 0.94 | +0.0027 |
| frecventa | 0.80 | +0.0037 |
| proportie | 0.86 | -0.0023 |
| binar x3 | **0.57** | **+0.0253** |

`binar x3` are varianta mica fiindca masa lui sta pe doua cifre din cinci. Si media bruta e acolo mai
BUNA decat cea standardizata, +0.667746 fata de +0.642394: `b_of` coboara singur greutatea unui membru
slab. Deci codul de acum nu are un defect de reparat.

**Why:** propozitia "formula prezice ansamblul cu eroare sub 0.001" invita intrebarea de unde vine
eroarea, si raspunsul nu e despre prompturi. Propozitia corecta e "agregarea e reducere de varianta si
nimic altceva, iar aritmetica ei e exacta", care e si mai tare, si adevarata.

**How to apply:** cand se scrie despre agregare in paper, se scrie identitate, nu predictie. Si `rho`
din formula se masoara pe semnalul TEMPERAT la T-ul ales LOLO, nu la T=1: `analysis_al3lea.corel` il
calculeaza la T=1, unde cei patru membri cunoscuti dau 0.805/0.845/0.806/0.734 in loc de
0.867/0.902/0.845/0.876. Vezi [[ansamblul-de-prompturi-formula]] si [[prompturi-decorelate-cernute]].
