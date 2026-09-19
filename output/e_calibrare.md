# E.15. Calibrare monotona a lui B, cu podeaua de zgomot

Generat 2026-08-22 19:30:35 de `analysis_calibrare.py`. 5624 randuri de test, 10 limbi, media pe limbi. Zero inferenta: aceleasi distributii de pe disc, alta citire a lor.

Intrebarea. `B` e UN anume functional liniar al distributiei, cel cu notele 1..5 EGAL spatiate.
Doua alternative au fost deja masurate si stau la capete opuse:

  - unirea cifrelor vecine (`prio_K`), adica 15 citiri monotone in trepte, aleasa LOLO: B urca de la
    +0.659202 la +0.661254, si fuziunea cu +0.001682;
  - citirea liniara NECONSTRANSA a celor cinci probabilitati, cu 5 coeficienti alesi LOLO: B COBOARA
    la +0.6407, desi plafonul ei in-sample e +0.6760 (`output/e_prioritate.md` §3b).

Deci scorul LOLO are un maxim undeva sub 15 candidati si se prabuseste pana la 5 parametri liberi.
Intre cele doua nu s-a masurat nimic, iar acolo se afla intrebarea: exista o regularizare intermediara
care sa scoata mai mult decat treptele?

Ce e familia, si de ce nu e o spline. Pearson e invariant la orice transformare afina cu panta
pozitiva a vectorului de valori `v`, fiindca randurile lui P insumeaza 1. Deci `v` se normalizeaza cu
v0 = 0 si v4 = 1, si raman exact TREI parametri liberi, cu constrangerea de monotonie. Cu cinci atomi,
o spline monotona cu 3-4 noduri nu are unde sa adauge ceva peste o grila pe simplexul cresterilor, iar
grila are avantajul ca numarul de candidati se declara exact. Familia de colaps e o submultime a
aceleiasi familii monotone, dar NU cade pe grila discreta (mediile de bloc dau numere ca 3/7), deci
cele doua se raporteaza separat.

Podeaua de zgomot e chiar punctul experimentului, nu un accesoriu. Un bazin de 455 de candidati
castiga ceva si daca toti candidatii sunt zgomot pur. Pentru fiecare marime de familie se construieste
un bazin ALEATOR de aceeasi marime, care contine si el citirea neutra, se trece prin selectia LOLO
IDENTICA, cu mai multe seminte, si se raporteaza cat da norocul singur. Un castig sub podea nu e
castig.

Asteptare declarata INAINTE de rulare, si e negativa. Dilutia masurata de la B la fuziune e intre
0.55 si 0.82, deci ca sa treaca bara de +0.0045 pe fuziune familia ar trebui sa dea +0.0055..+0.0082
pe B, adica de trei ori cat da colapsul si peste tot ce s-a masurat pe axa asta.

Controlul care valideaza codul, si a trecut inainte de a se scrie orice cifra: `--mod calibrare
--pas 0`, adica cele 15 partitii de colaps scrise ca vectori, reproduce `--mod colaps` pe toate zece
limbile la 1.9e-09, si alege aceeasi partitie 1|23|45 unanim.

## 0. Linia de baza se reproduce

Citirea neutra, cu T ales LOLO prin aceeasi conducta: **0.659202**. Semnalul B al sistemului, citit din `output/fusion_lolo_adoptat_temp.csv`: **0.659202**. Abatere: **2.72e-10**.

## 1. Familiile reale

`margine` e criteriul castigatorului minus criteriul citirii neutre, mediat pe limbi; `latime` e cat separa criteriul cel mai bun candidat de cel mai slab. O margine mica pe un criteriu lat e tiparul pe care l-a avut `distTpp`, adica alegere pe zgomot.

| familie | candidati | r mediu pe B | fata de neutru | CI 95% pereche | P(>0) | limbi cu citire neutra | margine medie | latime medie |
|---|---|---|---|---|---|---|---|---|
| colaps, 15 trepte | 15 | **0.661253** | +0.002044 | [+0.000793, +0.003317] | 99.9% | 0/10 | +0.00208 | 0.39081 |
| grila 1/4 | 35 | **0.657216** | -0.001979 | [-0.003599, -0.000371] | 0.7% | 3/10 | +0.00033 | 0.38906 |
| grila 1/8 | 165 | **0.661520** | +0.002309 | [+0.000978, +0.003729] | 99.9% | 0/10 | +0.00258 | 0.39131 |
| grila 1/12 | 455 | **0.659526** | +0.000339 | [-0.001122, +0.001862] | 68.7% | 0/10 | +0.00237 | 0.39110 |

### Ce citire s-a ales, per limba

| familie | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| colaps, 15 trepte | .00/.43/.43/1/1 | .00/.43/.43/1/1 | .00/.43/.43/1/1 | .00/.43/.43/1/1 | .00/.43/.43/1/1 | .00/.43/.43/1/1 | .00/.43/.43/1/1 | .00/.43/.43/1/1 | .00/.43/.43/1/1 | .00/.43/.43/1/1 |
| grila 1/4 | .00/.25/.50/1/1 | .00/.25/.50/1/1 | .00/.25/.50/1/1 | neutru | neutru | .00/.25/.25/1/1 | .00/.25/.50/1/1 | neutru | .00/.25/.50/1/1 | .00/.25/.50/1/1 |
| grila 1/8 | .00/.38/.38/1/1 | .00/.38/.38/1/1 | .00/.38/.38/1/1 | .00/.38/.38/.88/1 | .00/.38/.38/1/1 | .00/.38/.38/1/1 | .00/.38/.38/1/1 | .00/.38/.38/1/1 | .00/.38/.38/1/1 | .00/.38/.38/1/1 |
| grila 1/12 | .00/.42/.42/1/1 | .00/.42/.42/1/1 | .00/.42/.42/1/1 | .00/.42/.42/.92/1 | .00/.33/.33/1/1 | .00/.33/.33/1/1 | .00/.42/.42/1/1 | .00/.33/.33/.92/1 | .00/.33/.33/1/1 | .00/.33/.33/.92/1 |

## 2. Podeaua de zgomot

Pentru fiecare marime de familie, 10 bazine ALEATOARE de aceeasi marime, fiecare continand si citirea neutra, trecute prin selectia LOLO identica. `podea` e castigul mediu peste cele 10 de seminte, adica **cat da norocul singur** la marimea aia de bazin. `exces` e castigul real minus podeaua, si e singura coloana care spune ceva.

| familie | candidati | castig real | podea de zgomot | interval al podelei | exces |
|---|---|---|---|---|---|
| colaps, 15 trepte | 15 | +0.002044 | **+0.000563** | [-0.001132, +0.002025] | **+0.001480** |
| grila 1/4 | 35 | -0.001979 | **+0.001162** | [-0.000610, +0.002025] | **-0.003141** |
| grila 1/8 | 165 | +0.002309 | **+0.001587** | [+0.000763, +0.002488] | **+0.000722** |
| grila 1/12 | 455 | +0.000339 | **+0.001568** | [-0.000232, +0.002473] | **-0.001229** |

## Verdict

Cel mai mare exces peste podea il da **colaps, 15 trepte**, cu 15 candidati: castig real +0.002044 pe B, podea +0.000563, exces **+0.001480**.

Dilutia de la B la fuziune, masurata pe cele trei configuratii deja rulate cap la cap (`prio_K` 0.82, `FS3` 0.55, `FS3K` 0.64), e intre 0.55 si 0.82. Deci excesul de mai sus s-ar traduce in **+0.000813 .. +0.001214** pe fuziune.

**NU bate bara de +0.0045**, nici la capatul favorabil al dilutiei (+0.001214). Asteptarea declarata inainte de rulare era chiar asta, si se confirma. Parghia se inchide ca sursa de castig, dar cifra ramane utila ca argument: familia monotona generala, cu de pana la 455 de candidati, nu scoate mai mult decat cele 15 trepte, deci spatierea nu mai are ce da.

