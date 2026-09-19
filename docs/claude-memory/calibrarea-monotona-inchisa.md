---
name: calibrarea-monotona-inchisa
description: "22 aug 2026 - familia monotona generala pana la 455 de candidati nu bate cele 15 trepte; podeaua de zgomot creste cu bazinul si mananca tot; prio_K insusi e doar +0.00148 peste zgomot"
metadata:
  type: project
---

Rulat **22 august 2026**, `analysis_calibrare.py` -> `output/e_calibrare.md`. Zero inferenta.

## Familia, si de ce nu e o spline

Cu cinci atomi, Pearson e invariant la orice transformare afina cu panta pozitiva a vectorului de
valori, fiindca randurile lui P insumeaza 1. Deci vectorul se normalizeaza cu v0 = 0 si v4 = 1 si raman
exact **trei parametri liberi**. O spline monotona cu 3-4 noduri n-are unde sa adauge ceva peste o
grila pe simplexul cresterilor, iar grila are avantajul ca numarul de candidati se declara exact.

## Cifrele, si podeaua e coloana care decide

| familie | candidati | castig pe B | podea de zgomot | exces |
|---|---|---|---|---|
| colaps, 15 trepte | 15 | +0.002044 | +0.000563 | **+0.001480** |
| grila 1/4 | 35 | -0.001979 | +0.001162 | -0.003141 |
| grila 1/8 | 165 | **+0.002309** | +0.001587 | +0.000722 |
| grila 1/12 | 455 | +0.000339 | +0.001568 | -0.001229 |

Podeaua e un bazin ALEATOR de aceeasi marime, care contine si el citirea neutra, trecut prin selectia
LOLO identica, 10 seminte. **Grila de 165 are castigul brut cel mai mare si excesul mai MIC decat cele
15 trepte**, fiindca podeaua creste cu bazinul. Pe fuziune, la dilutia masurata de 0.55-0.82, excesul
maxim ar da +0.0008..+0.0012, deci sub bara de +0.0045. Se inchide.

## Ce trebuie scris in paper, si nu e placut

**Castigul lui `prio_K` insusi, +0.002044 pe B, e doar +0.001480 peste podeaua de zgomot a unui bazin
de 15 candidati.** Peste un sfert din el e noroc de selectie. Vezi
[[prioritizarea-parghiilor-masurata]].

## Cod

`make_fs_runs.py` are `--mod calibrare --pas {4,8,12}`, cu `--pas 0` pentru cele 15 partitii de colaps
scrise ca vectori. `b_of` primeste `vals`. Doua controale trec: octet identic cu
`output/bakeoff_test_Text/` pe calea implicita, si `--pas 0` reproduce `--mod colaps` la 1.9e-09 cu
aceeasi partitie 1|23|45 unanim. `pas` trebuie divizibil cu 4, altfel spatierea egala n-ar fi in grila
si selectia n-ar putea sa nu schimbe nimic.
