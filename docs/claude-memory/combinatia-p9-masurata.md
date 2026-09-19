---
name: combinatia-p9-masurata
description: "ISTORIC, pe n=5606. P9 a aratat ca cele doua parghii NU sunt redundante, ceea ce a dus la adoptie; cifrele curente sunt in p11-adoptia-facuta"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1db2cc03-b25b-478b-93a1-cce9b8a92faf
  modified: 2026-08-18T21:51:50.208Z
---

> **ISTORIC.** Toate cifrele de aici sunt pe **n = 5606**, dinainte de fixul din `find_char_span`.
> Au fost baza deciziei de adoptare, si de asta se pastreaza, dar **nu se citeaza**. Cifrele curente
> sunt in [[p11-adoptia-facuta]].

Rulat **19 august 2026**. `analysis_adoptie.py` -> `output/e_adoptie.md` plus `output/adoptie.csv`.
Zero inferenta LLM, zero descarcari, zece secunde de rulare. Planul: `PROMPT-p9-combinatia-si-dosarul-adoptiei.md`.

## Cele patru configuratii

| configuratie | r mediu | fata de sistem |
|---|---|---|
| sistemul publicat | 0.664555 | referinta |
| media a patru encodere | 0.671952 | +0.007396 |
| selectia lui B pe test, `--pick-split test` | 0.669591 | +0.005036 |
| **combinatia, tag `ens_encmean_picktest`** | **0.676253** | **+0.011698** |

Suma naiva era +0.012432. Masurat s-a recuperat **94%**, deci **se aduna aproape complet**. Poarta 3
(daca iese sub 0.671952 te opresti) a trecut lejer.

## Cele patru comparatii perechi, si care decide

| comparatie | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|
| combinatia vs sistem | +0.011698 | [+0.0078, +0.0155] | 100% |
| **combinatia vs encmean singur** | **+0.004302** | **[+0.0017, +0.0070]** | **100%** |
| combinatia vs picktest singur | +0.006662 | [+0.0037, +0.0095] | 100% |
| encmean vs picktest | +0.002360 | [-0.0017, +0.0064] | 85.6% |

**Comparatia care decide EXCLUDE zero.** Selectia pe test adauga ceva real peste media de encodere,
deci cele doua **nu sunt redundante** si regula de rezerva („daca include zero, adopta doar
`--pick-split test`") nu s-a declansat. Ultima linie arata insa ca cele doua parghii nu se disting
una de alta ca marime.

## Cifrele care incurca, si trebuie tinute minte

- Combinatia are media cea mai mare **dar e cea mai buna doar pe 4 limbi din 10**; media de encodere
  singura e cea mai buna pe 5. Din +0.0117 pe medie, **franceza singura duce +0.0062, adica 53%**,
  dintr-o limba din zece.
- `fil` scade cu -0.0081, interval care exclude zero, si vine din encmean.
- **Suprapunerea temuta pe franceza NU s-a materializat.** Recuperarea acolo e 94%, aceeasi cu media,
  deci suprapunerea e mica si uniforma, nu concentrata pe fr.
- Mecanismul prezis al realocarii lui `w` se vede totusi in ponderi: `w` mediu e 0.390 la sistem,
  urca la 0.445 cand A se face mai bun prin encodere, coboara la 0.370 cand B se face mai bun prin
  selectie, si iese 0.420 la combinatie.

## Recomandarea data, si e argument, nu decizie

1. **`--pick-split test` se adopta**, necondiționat. E reparatie de corectitudine, nu castig de cifra:
   elimina o asimetrie pe care docstringul propriului fisier o condamna. Costa zero la inferenta.
2. **Media de encodere NU se adopta inca.** Nu fiindca cifra ar fi proasta, ci fiindca alegerea binara
   „mediaza in loc sa selectezi" s-a facut dupa ce s-a vazut rezultatul pe test. Intai M3 (40 min,
   poate scoate `xlmr-large`), apoi M1. Vezi [[encoderul-masurat-lolo]].
3. **„Combinatia" nu se adopta ca pachet.** Nu e un al treilea design, sunt doua decizii separate.

**Why:** dosarul exista tocmai ca decizia sa se ia pe cifre puse una langa alta, inclusiv cele care
incurca, nu pe cifra cea mai mare.

**How to apply:** **adoptia S-A FACUT** in aceeasi zi, deci nu mai cita nimic de aici. Cifra e
**0.674946 pe n = 5624**, iar maximul masurat, care nu e acelasi lucru, e 0.675996. Vezi
[[p11-adoptia-facuta]], [[m1-si-m3-au-trecut]], [[selectia-modelului-b-e-pe-splitul-gresit]] si
[[bifurcatii-de-declarat]].
