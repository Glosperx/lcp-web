# E.14. Al treilea prompt, cernut pe trial sub protocolul complet

Generat 2026-08-22 18:41:19 de `analysis_al3lea_trial.py`. 300 instante de trial, 10 limbi. Criteriul de selectie e chiar `make_fs_runs.pick_params`, nerescris.

Intrebarea, si e una de procedura, nu de performanta. Pe test, `M3K` cu `marcat` da 0.690001 si `FS3K`
cu `few-shot` da 0.688506, iar diferenta e +0.001510 [-0.001142, +0.004239], adica nu se distinge.
Atunci singurul lucru care le separa e CUM a fost ales al treilea membru: few-shot era clar primul pe
trial, marcat era al treilea. Deci `FS3K` e „ales pe trial, evaluat o data pe test", iar `M3K` are o
decizie de test in plus.

Dar clasamentul de trial pe care se sprijină afirmatia aia a fost calculat din
`output/promptlab_gemma4-12b-4bit.csv`, care are numai scorul scalar, deci **la T = 1 si fara nicio
selecție**. Pe test, protocolul e altul: distributii, temperatura aleasa LOLO, si opțional partitia de
unire a cifrelor. Comparatia corecta cere acelasi protocol pe trial.

Daca sub protocolul complet marcat iese primul si pe trial, atunci `M3K` devine si el „ales pe trial"
si cele doua configuratii nu mai difera prin nimic care sa se poata apara. Daca few-shot rams primul,
atunci `FS3K` pastreaza avantajul de procedura.

Perechea de acum, sub acelasi protocol: **+0.701251** cu T ales LOLO, **+0.697191** cu T plus partitia.

## Clasamentul, si ce se compara cu ce

`la T=1, fara selecție` e clasamentul vechi, din `output/promptlab_gemma4-12b-4bit.csv`, pe care s-a sprijinit afirmatia `few-shot a fost ales pe trial`. `sub protocol complet` e acelasi lucru masurat cum se masoara pe test. `castig pe B, pe TEST` e coloana cu care se compara ordinea.

| membru | la T=1, fara selecție | solo, protocol complet | in trei, T LOLO | in trei, T + partitie | castig peste pereche | castig pe B, pe TEST |
|---|---|---|---|---|---|---|
| `few-shot` | +0.7109, primul | +0.709243 | +0.716585 | +0.717655 | **+0.015334** | +0.005247 |
| `marcat` | +0.6895, al treilea | +0.638869 | +0.693124 | +0.680766 | **-0.008127** | +0.004146 |
| `rubrica` | +0.6904, al doilea | +0.653407 | +0.698125 | +0.688863 | **-0.003126** | +0.000857 |
| `learner` | +0.6773, sub perechea de doua | +0.668069 | +0.701502 | +0.686048 | **+0.000251** | +0.000286 |

### Comparatii perechi pe trial, fata de perechea de acum

Reesantionare pe contexte, seed fix, deci perechea vede aceeasi reesantionare. Intervalele sunt late fiindca sunt 30 de instante per limba.

| membru | in trei fata de pereche | CI 95% pereche | P(>0) |
|---|---|---|---|
| `few-shot` | **+0.015092** | [+0.004978, +0.024963] | 99.9% |
| `marcat` | **-0.007407** | [-0.023528, +0.010015] | 18.4% |
| `rubrica` | **-0.002917** | [-0.013725, +0.007838] | 29.9% |
| `learner` | **-0.000652** | [-0.010994, +0.010715] | 43.7% |

## Verdict de procedura

Ordinea pe trial, sub protocolul complet: `few-shot` > `learner` > `rubrica` > `marcat`.

Ordinea pe test, dupa castigul pe B: `few-shot` > `marcat` > `rubrica` > `learner`.

Concordanta Kendall intre cele doua ordini, pe cei 4 membri: **+0.000**.

**Primul e acelasi in ambele, `few-shot`.** Deci configuratia cu el e aleasa pe trial si evaluata o data pe test, si nu are nicio decizie de test in alegerea membrului. Celalalt candidat rams cu o decizie de test in plus, si asta e singurul lucru care le separa, fiindca cifrele lor nu se distinge.

