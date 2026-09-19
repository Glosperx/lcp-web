---
name: prompturi-decorelate-cernute
description: "22 aug 2026 - cinci prompturi structural decorelate cernute pe trial cu frontiera calibrata; frecventa trece portile cu rho3 0.770, cel mai mic obtinut, si CADE pe test cu -0.0024; a patra rasturnare"
metadata:
  type: project
---

Rulat **22 august 2026**. Rapoarte: `output/e_frontiera.md` (cernerea) si `output/e_research.md`
(sinteza). Cod nou: sabloane in `prompt_lab.py`, `analysis_frontiera.py`. **Nimic nu s-a adoptat.**

## Cei cinci candidati, si ce schimba fiecare

Toti pe scara 1-5 cu un singur soft-read, deci zero infrastructura noua. Cifre de TRIAL, la T ales LOLO:

| candidat | ce schimba | r3 | rho3 | ansamblu | fata de pereche | porti |
|---|---|---|---|---|---|---|
| `frecventa` | cat de comun, nu cat de dificil | +0.641 | **0.770** | +0.713418 | **+0.012996** | trece |
| `fara context` | tinta singura, fara propozitie | +0.643 | 0.825 | +0.701538 | -0.001037 | cade |
| `lema` | lema, nu forma flexionata | +0.663 | 0.869 | +0.700942 | -0.000377 | cade |
| `binar x3` | citire binara la trei praguri | +0.521 | 0.722 | +0.667746 | -0.030719 | cade |
| `proportie` | cati cititori din cinci | +0.520 | 0.733 | +0.681556 | -0.019157 | cade |

Perechea sub acelasi protocol: +0.701251. Trei candidati au coborat `rho3` sub 0.845, cel mai mic de
pana atunci, **deci parghia decorelarii structurale EXISTA**. Dar numai unul a facut-o pastrand r3.

## Poarta a fost calibrata, nu aleasa

Aceleasi doua porti aplicate celor patru membri cu rezultat cunoscut pe test: trece `few-shot`
(+0.005247), cad `marcat` (+0.004146), `rubrica` (+0.000857), `learner` (+0.000286). Recall mic, dar
separa. **Fara blocul asta pragul ar fi fost arbitrar si n-ar fi decis nimic.**

## Rezultatul pe test: cade

| configuratie | limbi stricate | r mediu | fata de 0.683849 | CI 95% pereche |
|---|---|---|---|---|
| `FR3` | fil, pt, si | 0.681462 | **-0.002422** | [-0.004829, -0.000051] |
| `FR3K` | fil, pt | 0.680073 | **-0.003798** | [-0.006548, -0.001112] |

A patra rasturnare trial-test din acelasi fir, si cea mai informativa: **portile au tinut pe medie**
si tot a cazut. Cauza in [[transferul-se-masoara-pe-limba]].

## Doua lucruri de retinut dincolo de verdict

1. **Un castig pe B nu inseamna un castig pe fuziune.** `FR3` urca B cu +0.001217 si coboara fuziunea
   cu -0.002386, adica dilutie **-1.96**. Cele trei configuratii masurate inainte aveau dilutia intre
   +0.55 si +0.82, si de acolo venea obiceiul de a extrapola. Obiceiul e gresit.
2. **Trei predictii declarate inainte s-au adeverit.** `lema` e cel mai putin decorelat, exact fiindca
   `fil` si `si` n-au lema. `fara context` cade pe sinhaleza, dar prin alt mecanism decat cel prezis:
   pe trial, unde nu exista nicio legatura, r3 solo pe `si` e +0.050, deci intrebarea nu merge acolo
   fara context; cele 64% legaturi de pe test ar fi venit peste. `frecventa` era cel mai promitator, si
   a fost, dar numai pe trial.

`binar x3` cade cu o explicatie mecanica curata: rho3 fata de pereche 0.722, cel mai mic, dar corelatia
INTRE cele trei praguri 0.883, deci trei copii aproape identice care costa trei inferente si aduc cat
una. Vezi [[frontiera-e-identitate-nu-aproximare]] si [[ansamblul-de-prompturi-formula]].
