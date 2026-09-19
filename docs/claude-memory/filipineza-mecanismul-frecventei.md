---
name: filipineza-mecanismul-frecventei
description: "23 aug 2026 - INCHIS: 26.7% din tintele filipineze au zipf exact 0, iar pe ele fuziunea da 0.2320 fata de 0.4642 pe restul; de asta scoaterea coloanei ajuta si de asta indicatorul de OOV nu repara"
metadata: 
  node_type: memory
  type: project
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-23T15:59:39.660Z
---

Intrebarea era deschisa din sesiunea din 23 august dimineata, formulata acolo ca **"nu stim
mecanismul"**: scoaterea coloanei de frecventa urca fuziunea pe filipineza cu +0.0225, CI exclude zero,
dar `feats=("oov",)`, un indicator per token pentru `zipf == 0`, nu repara nimic.

Raspunsul, din doua masuratori independente, `output/e_shap_multi.md` si
`output/e_al3lea_semnal.md` sectiunea 5.

## Cifrele

Un surogat lexical care prezice `p_fuz` doar din trasaturi numite reconstruieste filipineza la
r = **0.867**, iar importanta lui `zipf` acolo e **0.8608** prin permutare, printre cele mai mari din
tabel. Deci sistemul se sprijina puternic pe frecventa pe limba aia.

Si:

    limba   tinte cu zipf = 0   r al fuziunii pe ELE   r pe restul
    fil     152 din 570 (26.7%)  +0.2320                +0.4642

Nicio alta limba cu frecventa disponibila nu trece de **3.6%** tinte cu zipf 0 (ca 3.6, de 3.3, en 1.1,
it 1.6, es 0.3, fr 0.5, pt 0.5, ja 0.0). Sinhaleza e la 100%, dar acolo coloana e goala prin
constructie, nu amestecata.

Rata de esec comun al celor doua semnale, adica itemii unde si A si B sunt deplasate in acelasi sens cu
peste o deviatie standard: **25.7% pe itemii cu zipf = 0** fata de **15.6% pe restul** aceleiasi limbi.

## Mecanismul

**Sistemul se sprijina cel mai tare pe frecventa exact pe limba unde frecventa lipseste pentru un
sfert din tinte.** Scoaterea coloanei ajuta fiindca il forteaza sa nu mai depinda de o trasatura pe
care 26.7% din itemi n-o pot furniza.

**Si de asta indicatorul de OOV n-a reparat:** un indicator spune "aici valoarea lipseste", dar nu pune
nimic in locul ei. Marcarea unei gauri nu e umplerea ei.

Se leaga direct de observatia deja masurata pe sinhaleza, unde scoaterea frecventei din CELELALTE noua
limbi urca bratul A cu +0.0243. **Aceeasi propozitie, doua limbi: un model antrenat pe limbi care AU
frecventa invata sa depinda de ea, iar limbile care n-o au platesc.** Asta e forma publicabila a
observatiei despre coada, si acum are mecanismul, nu doar efectul.

**Ce ramane de incercat, si e cel mai direct test al mecanismului:** imputarea celor 152 de tinte cu
frecventa de coada din Wikipedia tagalog, care exista deja in `data/freq_tail/`. Varianta masurata pe
23 august a schimbat coloana peste tot si a pierdut pe medie (-0.0009), dar pe filipineza a castigat
(+0.003). Varianta care ar trebui incercata umple **numai zerourile**, nu inlocuieste coloana.

Vezi [[coada-frecventa-masurata]] si [[prioritate-contributie-si-drumul-la-07]].
