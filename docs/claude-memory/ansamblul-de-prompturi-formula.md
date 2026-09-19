---
name: ansamblul-de-prompturi-formula
description: "22 aug 2026 - castigul unui al treilea prompt e EXACT formula de reducere a variantei; few-shot e primul pe trial prin ambele protocoale iar marcat e ultimul, deci FS3K e ales pe trial si M3K e selectie pe test"
metadata: 
  node_type: memory
  type: project
  originSessionId: c41c7657-b13d-4c6e-b16c-1f1864b8ecb1
  modified: 2026-08-22T12:52:09.229Z
---

Rulat **22 august 2026**, ca **control de mecanism** pentru [[fewshot-pe-test-masurat]].
Raport: `output/e_al3lea.md`. Trei prompturi alternative pe test, ~38 min fiecare, o singura incarcare.

## Formula, si e exacta

Pentru media a n semnale standardizate, `r_ens = (suma r_i) / sqrt(n + 2*suma_{i<j} rho_ij)`. Prezice
ansamblul observat la **0.0003 pana la 0.0024**:

| al treilea membru | r_3 | rho(3,p1) | rho(3,p2) | r_ens prezis | r_ens observat | eroare |
|---|---|---|---|---|---|---|
| few-shot | +0.630 | 0.884 | 0.860 | +0.663513 | +0.664449 | -0.000936 |
| rubrica | +0.632 | 0.918 | 0.887 | +0.659049 | +0.660059 | -0.001010 |
| marcat | +0.617 | 0.811 | 0.884 | +0.663065 | +0.663347 | -0.000282 |
| learner | +0.617 | 0.926 | 0.827 | +0.657081 | +0.659488 | -0.002407 |

Perechea de acum are r_p1 = +0.623, r_p2 = +0.653, rho = 0.874. **Deci nu exista niciun reziduu care
sa fie „informatie noua adusa de exemplele few-shot".** Aritmetica de ansamblu explica totul.

**Niciun rezumat scalar nu prezice castigul, si de aia intuitia greseste de doua ori.** `rubrica` are
cel mai bun r solo (+0.632) si nu aduce nimic, fiindca e prea corelata (0.918/0.887). `learner` e cel
mai decorelat in medie si nu aduce nimic, fiindca r-ul lui e mic. `marcat` are r mic dar e decorelat de
promptul 1 (0.811), si aduce cel mai mult. Corectie fata de ce scria in [[fewshot-pe-test-masurat]] si
in [[prompt-ansamblu-decorelat]]: nu e „decorelarea", e combinatia completa.

## Fuziunea, cele patru configuratii de control

| config | al treilea | r mediu | fata de 0.683849 | CI 95% pereche | limbi stricate |
|---|---|---|---|---|---|
| `M3K` | marcat | **0.690001** | +0.006153 | [+0.003436, +0.008713] | niciuna |
| `FS3K` | few-shot | 0.688506 | +0.004642 | [+0.002619, +0.006756] | niciuna |
| `R3K` | rubrica | 0.685921 | +0.002030 | [-0.000013, +0.004214] | niciuna |
| `L3K` | learner | 0.683912 | +0.000040 | [-0.001656, +0.001800] | es, it |

`M3K` fata de `FS3K` da +0.001510 [-0.001142, +0.004239], P = 86.6%, deci **NU sunt distinctibile**.
Nici bazina de a declara marcat castigator, nici bazina de a spune ca few-shot e special.
`learner` e controlul negativ si se comporta ca atare: zero, plus doua limbi stricate.

## Consecinta pentru paper, si e negativa

**Revendicarea fata de G-Eval nu se poate scrie.** Motivul pentru care few-shot merita rulat era ca
G-Eval e 3-shot in limba tinta si noi am fi zero-label. Dar `marcat`, care nu foloseste NICIO eticheta
(doar marcheaza tinta inline cu ghilimele unghiulare), da un castig indistinguibil. Deci castigul nu
vine din exemple, si fraza corecta ar fi „trei prompturi bat doua", care nu e o contributie.

## Capcana de metoda, si e cea mai importanta de aici

Formula e exacta INAINTEA splitului, dar **intrarile ei nu transfera**. Ordinea membrilor pe trial:
few-shot +0.7109, rubrica +0.6904, marcat +0.6895, learner +0.6773. Pe test, dupa castigul pe B:
few-shot +0.005247, marcat +0.004146, rubrica +0.000857, learner +0.000286. **Rubrica si marcat isi
schimba locurile**, si erau la 0.001 unul de altul pe trial. E a doua rasturnare trial-test in acelasi
fir, dupa few-shot singur.

Deci al treilea prompt **nu se poate alege pe trial** cu incredere, iar orice alegere facuta pe test e
selectie pe setul de test. Singura formulare onesta care supravietuieste: selectia pe trial alege
few-shot (era clar primul, +0.7109 fata de +0.6904), si atunci `FS3K` = 0.688506 e o cifra selectata pe
trial si evaluata o data pe test. Celelalte sase sunt controale, nu candidati.

**Am scris in docstring-ul lui `analysis_al3lea.py`, INAINTE de a vedea cifrele, ca un membru
alternativ mai bun e dovada CONTRA povestii few-shot si nu un candidat nou.** `M3K` nu se propune
pentru adoptare, si angajamentul ala se tine.

## T per prompt: inchis in aceeasi zi

`FS3P` = 0.687241 (+0.003396, strica pt), `FS3KP` = 0.687604 (+0.003728, strica pt). Amandoua SUB
`FS3K` si amandoua strica portugheza, exact ca `distTpp` care strica spaniola. **T per prompt strica
sistematic o limba romanica.**

Temperaturile se separa foarte clar, deci semnal exista: few-shot vrea T=4-6, promptul expert T=16-32,
promptul scurt T=3-4. Si totusi e mai rau. Alegerea nu e pe criteriu plat: `crit_lat` 0.03-0.036 cu
marginea +0.0017..+0.0051, adica 5-17% din latime, fata de 1.2% la `distTpp`, si nicio limba la
marginea grilei.

**Nu s-a folosit grila plina.** `analysis_dist.step_f_pick` face argmax pe 16x16 pentru doua prompturi
si exact asa a fost respins `distTpp`; pentru trei ar fi 4096 de candidati. `make_fs_runs --per-prompt`
face o rafinare INDEPENDENTA pe cate un prompt in jurul lui T comun: 16 + 15 + 48 = 79 de candidati,
fara ordine intre prompturi, deci fara gradul ala de libertate.

## Formula prezice, si a fost verificata cu o predictie declarata inainte

Ansamblul de PATRU (few-shot, marcat, expert, scurt) a fost prezis cu formula **inainte** de a fi
construit: **+0.665642**. Observat: **+0.665784**. Eroare **-0.000142**. Deci formula nu e doar un
rezumat post-hoc, e un predictor folosibil in interiorul splitului.

| config | ce e | r mediu | fata de 0.683849 | CI 95% pereche | limbi stricate |
|---|---|---|---|---|---|
| `FM4K` | patru prompturi + colaps | **0.690320** | +0.006467 | [+0.003698, +0.009237] | **pt** |
| `M3K` | marcat + colaps | 0.690001 | +0.006153 | [+0.003436, +0.008713] | niciuna |
| `FM4` | patru prompturi | 0.689146 | +0.005310 | [+0.002624, +0.007898] | **pt** |
| `FS3K` | few-shot + colaps | 0.688506 | +0.004642 | [+0.002619, +0.006756] | niciuna |

**Cifra cea mai mare, `FM4K` = 0.690320, e RESPINSA pe portugheza.** Al treilea caz in care conditia
„nicio limba stricata" respinge maximul, dupa `distTpp` si `prio_KW`.

## De ce nu se alege pur si simplu cifra cea mai mare, cu cifre

Niciuna dintre cele trei de sus nu se distinge de celelalte:

- `M3K` fata de `FS3K`: +0.001510 [-0.001142, +0.004239], P = 86.6%
- `FM4K` fata de `FS3K`: +0.001825 [-0.000185, +0.003769], P = 96.3%
- `FM4K` fata de `M3K`: +0.000315 [-0.001041, +0.001601], P = 67.3%

Deci 0.690 si 0.688 **nu sunt doua cifre diferite**. A alege intre ele pe zecimala a treia e a alege pe
zgomot. Singura asimetrie reala intre `M3K` si `FS3K`: al treilea membru al lui `FS3K` a fost ales pe
TRIAL, unde few-shot era clar primul (+0.7109 fata de +0.6904); al lui `M3K` a ieșit primul abia
uitandu-ne la test, fiindca pe trial marcat era al treilea. `FS3K` are deci o decizie de test mai
puțin.

Ce are `M3K` de partea lui, si trebuie spus: e mai IEFTIN, 0.40 s per item fata de 1.03 la few-shot;
nu foloseste nicio eticheta; si urca 8 limbi din 10, in timp ce `FS3K` isi ia castigul aproape numai
din franceza (+0.0208) si japoneza (+0.0166). `M3K` ia +0.0244 pe germana, adica exact limba pe care
`FS3K` o coboara. Cele doua nu sunt aceeasi soluție, doar au aceeasi medie.

`v8_marcat` are o singura slabiciune de implementare, si e mica: tinta nu se gaseste ca subsir pe
**18 din 5624** de randuri de test, 0.32%, si atunci propozitia rams nemarcata.

## CERNEREA PE TRIAL SUB PROTOCOLUL COMPLET, si inchide intrebarea M3K contra FS3K

Rulat **22 august**, `analysis_al3lea_trial.py` -> `output/e_al3lea_trial.md`. 4 variante x 300
instante, 10 minute. Criteriul NU e rescris: se cheama chiar `make_fs_runs.pick_params`, deci T si
partitia se aleg pe trial in exact aceeasi forma ca pe test.

Perechea de acum, pe trial sub acelasi protocol: **+0.701251** cu T LOLO, +0.697191 cu T plus partitia.

| membru | solo | in trei, T LOLO | in trei, T+partitie | castig peste pereche | CI 95% pereche | castig pe B pe TEST |
|---|---|---|---|---|---|---|
| few-shot | +0.709243 | **+0.716585** | +0.717655 | **+0.015334** | [+0.004978, +0.024963] | +0.005247 |
| learner | +0.668069 | +0.701502 | +0.686048 | +0.000251 | [-0.010994, +0.010715] | +0.000286 |
| rubrica | +0.653407 | +0.698125 | +0.688863 | -0.003126 | [-0.013725, +0.007838] | +0.000857 |
| marcat | +0.638869 | +0.693124 | +0.680766 | **-0.008127** | [-0.023528, +0.010015] | +0.004146 |

**Trei fapte, si primul inchide intrebarea.**

1. **few-shot e primul si sub protocolul complet**, si e SINGURUL cu interval care exclude zero pe
   trial, +0.015092 [+0.004978, +0.024963], P = 99.9%. Deci `FS3K` e ales pe trial si evaluat o data
   pe test, prin ambele protocoale de cernere, cel grosier la T=1 si cel complet.
2. **marcat e ULTIMUL pe trial si coboara sub pereche**, -0.008127. Deci `M3K` nu putea fi ales pe
   trial prin nicio procedura: alegerea lui e in intregime o selecție pe setul de test. E cazul cel mai
   rau posibil pentru argumentul „si marcat ar fi fost ales oricum".
3. **Dincolo de primul loc nu transfera nimic:** Kendall intre ordinea de trial si cea de test e
   **+0.000**. marcat trece de la ultimul pe trial la al doilea pe test, learner invers.

Deci intrebarea „de ce nu M3K, are 0.690" are un raspuns care nu depinde de zecimale: cifrele nu se
distinge (+0.001510 [-0.001142, +0.004239]), iar la performanta egala `FS3K` are o decizie de test mai
puțin. Daca se ia `M3K`, se ia pentru cost (0.40 s per item fata de 1.03) si pentru acoperirea pe limbi
(8 din 10 in sus, plus +0.0244 pe germana), NU pentru scor, si cu selecția pe test declarata.

**Detaliu de reținut despre partitia de colaps:** pe trial ea ajuta NUMAI la few-shot (+0.717655 fata
de +0.716585) si strica la ceilalti trei, pana la -0.0124 la marcat. Confirma ce se vedea si la `FS`:
unirea cifrelor cere o forma anume de distributie, nu merge pe orice B.

## FRONTIERA, si e unealta pentru sesiunea urmatoare

Perechea de acum, in termenii formulei: r1 = +0.623, r2 = +0.653, rho12 = 0.874, deci r_ens = 0.659099.
Ce trebuie sa aiba un al TREILEA prompt ca sa o bata, cu `rho3` = media corelatiilor lui cu cele doua:

| rho3 | r3 minim ca sa bata perechea | r3 pentru +0.005 | r3 pentru +0.010 |
|---|---|---|---|
| 0.95 | +0.651 | +0.666 | +0.680 |
| 0.874 | +0.616 | +0.631 | +0.645 |
| 0.80 | +0.582 | +0.596 | +0.610 |
| 0.70 | +0.535 | +0.549 | +0.562 |
| 0.60 | +0.486 | +0.500 | +0.513 |
| 0.50 | +0.436 | +0.449 | +0.462 |
| 0.40 | +0.385 | +0.397 | +0.410 |

Cele patru incercate stau toate la `rho3` intre 0.848 si 0.903, deci in zona in care ai nevoie de r3
peste 0.61 doar ca sa nu pierzi. **Un prompt cu r3 = +0.50, adica mult mai slab, bate perechea daca
rho3 < 0.62.** Parghia e DECORELAREA STRUCTURALA, nu calitatea promptului. Prompturi care schimba doar
formularea rams la rho ~0.87; ar trebui unele care schimba CE conditioneaza modelul.

## Ce se poate cerne pe trial si ce nu, masurat

| marime | corelatie trial-test peste cei 4 membri | deplasare sistematica |
|---|---|---|
| `rho3`, decorelarea | **+0.997** | +0.017..+0.036 in SUS |
| `r3`, calitatea | +0.726 | -0.025..-0.097 in JOS |

**Decorelarea se cerne pe trial si transfera aproape perfect. Calitatea nu.** Deplasarea in jos a lui
r3 e mai mare la prompturile „inteligente" (few-shot -0.083, learner -0.097) decat la cele simple
(marcat -0.025, rubrica -0.028). Deci strategia de cernere: cauta `rho3` mic pe trial, care e fiabil,
intre prompturi cu r3 de cel puțin ~0.55 pe trial ca sa mai rams peste 0.50 pe test.

## Semnalul C e mort, cu cifra

`r(C, y)` pe test = **-0.0649**, semn greasit, si nu intra deloc in `fuse_ab`. Ca al treilea membru cu
pondere egala ar duce ansamblul de la 0.659 la 0.577. Nu se mai reia.

## Starea multiplicitatii, de declarat

Pe aceleasi 5624 de randuri de test s-au masurat acum **saisprezece** configuratii: FS, FSK, FS3,
FS3K, FS3P, FS3KP, R3, R3K, M3, M3K, L3, L3K, FM4, FM4K, plus `prio_*` de pe 21 august. `FS3K` si `M3K` rezista amandoua la
Bonferroni pe opt, CI 99.375% [+0.001817, +0.007461] si [+0.002531, +0.009606]. Dar maximul a
paisprezece nu e un rezultat, si asta trebuie sa intre in [[bifurcatii-de-declarat]].

## CORECTIE, 22 august seara: formula nu are eroare, si rho de aici e la T gresit

Doua lucruri din fisa asta se citesc gresit si s-au verificat pe date, vezi
[[frontiera-e-identitate-nu-aproximare]].

1. **Formula e o IDENTITATE, nu un predictor cu eroare.** Reproduce media STANDARDIZATA a membrilor la
   3.3e-16. Cifrele de -0.000936 / -0.001010 / -0.000282 / -0.002407 de mai sus, si -0.000142 pe
   ansamblul de patru, sunt distanta dintre media standardizata si media BRUTA calculata de
   `make_fs_runs.b_of`, si ea creste cu diferenta de varianta intre membri. Nu e eroarea aritmeticii.

2. **Tabelul frontierei foloseste rho la temperatura aleasa LOLO, nu la T = 1.** Cei patru membri au
   acolo 0.867 / 0.902 / 0.845 / 0.876, iar `analysis_al3lea.corel`, care e in cod, calculeaza rho la
   T = 1 si da 0.805 / 0.845 / 0.806 / 0.734. Diferenta la few-shot e 0.062, destul cat sa mute
   verdictul unui candidat nou. Orice script care refoloseste `corel` pentru frontiera va gresi.

**Si verdictul din `output/e_al3lea.md` nu se citeaza asa cum e.** El spune "castigul e specific
few-shot-ului", pe un prag de 80% aplicat castigului pe B, iar `marcat` cade la 79.0% (0.004146 /
0.005247), adica sub prag cu un punct. La nivelul fuziunii `marcat` chiar CASTIGA, 0.690001 fata de
0.688506. Deci proza raportului contrazice tabelul lui. Formularea care supravietuieste amandurora e
cea de mai sus in fisa: nu se disting, si revendicarea fata de G-Eval nu se poate scrie.
