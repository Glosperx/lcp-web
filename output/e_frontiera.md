# E.16. Prompturi structural decorelate, cernute pe trial cu frontiera

Generat 2026-08-22 19:52:17 de `analysis_frontiera.py`. 300 instante de trial, 10 limbi. Criteriul de selectie e chiar `make_fs_runs.pick_params`, nerescris.

De ce directia asta si nu alta. Castigul unui al treilea prompt e EXACT formula de reducere a
variantei, `r_ens = (suma r_i)/sqrt(n + 2*suma_{i<j} rho_ij)`, verificata pe test cu eroare -0.000142
pe un ansamblu de patru prezis inainte de a fi construit. In formula, singura parghie care se poate
misca mult e `rho`: cele patru prompturi incercate pana acum stau toate intre 0.845 si 0.903, iar un
prompt cu r3 = +0.50, mult mai slab decat oricare dintre ele, bate perechea daca rho3 < 0.62. Deci
ce trebuie schimbat e CE conditioneaza modelul, nu cat de bine e formulata intrebarea.

**Capcana de masurare, si a fost verificata inainte de a scrie codul asta.** `analysis_al3lea.corel`
calculeaza rho la T = 1, unde cei patru membri cunoscuti dau 0.805 / 0.845 / 0.806 / 0.734. Frontiera
insa lucreaza pe semnalul TEMPERAT la T-ul ales LOLO, unde aceiasi patru dau 0.867 / 0.902 / 0.845 /
0.876. La few-shot diferenta e 0.062, adica destul cat sa rastoarne verdictul. Aici rho se masoara
mereu pe semnalul temperat, prin acelasi `make_fs_runs.pick_params` care alege T si pe test.

**Frontiera e o identitate in interiorul splitului, nu un predictor peste split.** Ordinea data de ea
pe trial, fata de castigul real pe B pe test, are Kendall +0.333 pe cei patru membri cunoscuti, deci
pe n = 4 nu inseamna nimic. Ce transfera, masurat, e `rho3`, cu corelatie trial-test +0.997; `r3`
transfera prost, +0.726, si se deplaseaza in JOS cu 0.025..0.097. De aceea cernerea NU e "duc pe test
ce prezice frontiera mai sus", ci doua porti scrise inainte de a vedea vreo cifra:

  1. `r3` pe trial cel putin +0.55, ca sa ramana peste +0.50 pe test dupa deplasare;
  2. dupa ce se aplica deplasarile in sensul cel mai NEFAVORABIL, `r3` minus 0.097 si `rho3` plus
     0.036, frontiera sa prezica in continuare castig peste perechea de acum.

Perechea de acum, sub acelasi protocol: **+0.701251**, cu r1 = +0.688, r2 = +0.669, rho12 = 0.827.

## 0. Verificarea de semn

Un membru cu r NEGATIV n-ar doar sa nu ajute, ar distruge ansamblul, iar formula frontierei presupune r pozitiv. `v11_frecventa` e singurul candidat la care semnul nu e garantat de constructie, fiindca intreaba despre frecventa, nu despre dificultate; scara lui e scrisa cu 5 = foarte rar tocmai ca semnul sa iasa pozitiv. Se verifica pe toate zece limbile, inainte de orice agregare.

| candidat | r pe limba, min | max | limbi cu semn negativ |
|---|---|---|---|
| `fara context` | +0.0337 | +0.8200 | **niciuna** |
| `frecventa` | +0.4556 | +0.7361 | **niciuna** |
| `binar x3` | -0.0265 | +0.8287 | fil, si |
| `lema` | +0.1452 | +0.8380 | **niciuna** |
| `proportie` | +0.1324 | +0.7707 | **niciuna** |

## 1. Calibrarea portii, pe membrii cu rezultat cunoscut pe test

Un prag ales de mine n-ar decide nimic. Cei patru membri de mai jos au fost dusi pana la capat pe test, deci se stie care a functionat: `few-shot` +0.005247 si `marcat` +0.004146 pe semnalul B, fata de `rubrica` +0.000857 si `learner` +0.000286. Aceleasi doua porti se aplica pe distributiile lor de TRIAL. Daca poarta ii respinge pe toti patru, e stricata si nu are voie sa decida nimic despre candidatii noi; daca ii separa, pragul e calibrat.

Referinta portii 2 e perechea trecuta prin aceeasi deplasare: **+0.608101**, fata de +0.701251 nedeplasata.

| membru | castig REAL pe B pe test | r3 | rho3 | frontiera dep. | poarta 1 | poarta 2 |
|---|---|---|---|---|---|---|
| `few-shot` | +0.005247, a functionat | +0.702 | 0.858 | **+0.617331** | DA | DA |
| `marcat` | +0.004146, a functionat | +0.631 | 0.842 | **+0.594183** | DA | nu |
| `rubrica` | +0.000857, nu a functionat | +0.654 | 0.889 | **+0.596261** | DA | nu |
| `learner` | +0.000286, nu a functionat | +0.661 | 0.850 | **+0.601022** | DA | nu |

**Poarta separa partial.** Trec `few-shot`, fata de cei care au functionat pe test, `few-shot`, `marcat`.

## 2. Cernerea, cu cele doua porti

`r3` si `rho3` sunt masurate pe semnalul TEMPERAT la T-ul ales LOLO. `r3 dupa dep.` e `r3 -0.097`, `rho3 dupa dep.` e `rho3 +0.036`, adica deplasarile trial-test masurate, aplicate in sensul nefavorabil. `frontiera dep.` e formula recalculata cu ele, si ea decide poarta 2, fata de perechea deplasata la fel, +0.608101.

| candidat | membri | r3 | rho3 | sd noi / sd sistem | ansamblu, media bruta | identitatea, media standardizata | brut - standardizat | r3 dupa dep. | rho3 dupa dep. | frontiera dep. | poarta 1 | poarta 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `fara context` | 1 | +0.643 | 0.825 | 0.94 | **+0.701538** | +0.704205 | -0.002667 | +0.546 | 0.861 | **+0.600478** | DA | nu |
| `frecventa` | 1 | +0.641 | 0.770 | 0.80 | **+0.713418** | +0.717155 | -0.003737 | +0.544 | 0.806 | **+0.609899** | DA | DA |
| `binar x3` | 3 | +0.521 | 0.722 | 0.57 | **+0.667746** | +0.642394 | +0.025352 | +0.424 | 0.758 | **+0.532273** | nu | nu |
| `lema` | 1 | +0.663 | 0.869 | 1.05 | **+0.700942** | +0.705036 | -0.004094 | +0.566 | 0.905 | **+0.601055** | DA | nu |
| `proportie` | 1 | +0.520 | 0.733 | 0.86 | **+0.681556** | +0.679259 | +0.002298 | +0.423 | 0.769 | **+0.571205** | nu | nu |

### Fata de perechea de acum, pe trial

Reesantionare pe contexte, seed fix, deci perechea vede aceeasi reesantionare. Intervalele sunt late si trebuie sa fie: 30 de instante per limba. Ce se citeste de aici e ORDINEA, nu cifrele.

| candidat | in ansamblu fata de pereche | CI 95% pereche | P(>0) |
|---|---|---|---|
| `fara context` | **-0.001037** | [-0.016894, +0.015744] | 46.1% |
| `frecventa` | **+0.012996** | [-0.006718, +0.032683] | 90.7% |
| `binar x3` | **-0.030719** | [-0.052521, -0.007963] | 0.7% |
| `lema` | **-0.000377** | [-0.012149, +0.011920] | 47.9% |
| `proportie` | **-0.019157** | [-0.036382, -0.003186] | 0.6% |

### Ce e de fapt frontiera, si corectia unei formulari vechi

`r_ens = (suma r_i)/sqrt(n + 2*suma rho_ij)` **nu e o aproximare, e o identitate algebrica**, si e identitatea mediei STANDARDIZATE a membrilor. Verificat pe toti candidatii si toate limbile de aici: abatere maxima **3.3e-16**, adica precizia masinii.

Ce se abate deci nu e formula, ci `make_fs_runs.b_of`, care mediaza valorile asteptate BRUTE, nu standardizate. Cand membrii au deviatii standard apropiate, cele doua marimi coincid pana la a treia zecimala, si de acolo vin `erorile` de 0.0003..0.0024 raportate pana acum in `output/e_al3lea.md`. Cand nu coincid, se despart mult: `binar x3` are membrii la 0.57 din deviatia standard a perechii, fiindca masa lui sta pe doua cifre din cinci, si atunci media bruta si cea standardizata difera cu 0.025.

Consecinta practica, si e in favoarea codului de acum: media BRUTA a lui `b_of` e mai buna decat cea standardizata la exact acest candidat, +0.667746 fata de +0.642394, fiindca coboara singura greutatea unui membru slab. Deci `binar x3` nu cade dintr-un artefact de mediere; ar cadea si mai rau daca s-ar standardiza.

## 3. Control: frontiera reproduce cifrele cunoscute de pe test

Pe date de test DEJA masurate, deci fara nicio configuratie noua pe test. Daca unealta de aici ar fi alta decat cea care a dat eroarea -0.000142 pe ansamblul de patru, cernerea de mai sus n-ar insemna nimic.

| membru | r3 | rho3 | identitatea, media standardizata | observat, media bruta | brut - standardizat |
|---|---|---|---|---|---|
| `few-shot` | +0.630 | 0.872 | +0.663513 | +0.664449 | +0.000936 |
| `rubrica` | +0.632 | 0.903 | +0.659049 | +0.660059 | +0.001010 |
| `marcat` | +0.617 | 0.847 | +0.663065 | +0.663347 | +0.000282 |
| `learner` | +0.617 | 0.876 | +0.657081 | +0.659488 | +0.002407 |

## Verdict

Trec amandoua portile, deci merg pe test: `frecventa` (r3 +0.641, rho3 0.770, frontiera deplasata +0.609899 fata de +0.608101).

- `lema` (lema in loc de forma flexionata): rho3 = 0.869. Cade: frontiera deplasata +0.601055, sub perechea deplasata +0.608101.
- `fara context` (tinta singura, fara propozitie): rho3 = 0.825. Cade: frontiera deplasata +0.600478, sub perechea deplasata +0.608101.
- `frecventa` (alt construct: cat de comun, nu cat de dificil): rho3 = 0.770. **Trece.**
- `proportie` (cati cititori din cinci, nu ce nota): rho3 = 0.733. Cade: r3 = +0.520, sub pragul de +0.55; frontiera deplasata +0.571205, sub perechea deplasata +0.608101.
- `binar x3` (citire binara la trei praguri, agregata): rho3 = 0.722, rho intre membri 0.883. Cade: r3 = +0.521, sub pragul de +0.55; frontiera deplasata +0.532273, sub perechea deplasata +0.608101.

Cel mai mic `rho3` obtinut e **0.722**, la `binar x3`, fata de 0.845 al celui mai decorelat prompt de pana acum. Pragul de care ar fi nevoie ca un membru slab sa bata perechea e `rho3` sub 0.62.

