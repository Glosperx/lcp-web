---
name: optimismul-de-selectie-masurat
description: "22 aug 2026 - cat costa alegerea configuratiei pe scorul de test, masurat: optimismul maximului peste 23 de configuratii e +0.001937; selectia LOLO a configuratiei da +0.004520 dar strica portugheza"
metadata:
  type: project
---

Rulat **22 august 2026**, ca raspuns la o obiectie corecta a lui Alexandru: „nu conteaza de fapt scorul
pe test, nu pe trial?". Da, conteaza, si argumentul cu trial-ul nu era decisiv. Calculul care il
inlocuieste, pe cele 23 de configuratii de semnal B masurate pe aceleasi 5624 de randuri.

## Optimismul maximului, masurat de doua ori

**Selecția configuratiei facuta LOLO**, adica exact ca T, `w`, `w_src`, setul lui A si partitia de
colaps: pentru limba L se alege configuratia pe celelalte NOUA limbi si se evalueaza pe L.

- castig mediu sub selecție LOLO: **+0.004535**
- maximul pe toate zece: +0.006472
- **optimismul maximului: +0.001937**

Selecția LOLO alege doar DOUA configuratii distincte peste cele zece harti: `FM4K` pe 8 limbi si `M3K`
pe 2. Niciodata `FS3K`. Deci alegerea e stabila si nu e la mila zgomotului.

A doua masuratoare, prin 252 de impartiri 5/5 pe limbi, cu selecție pe o jumatate si evaluare pe
cealalta: castigul procedurii **+0.003631**, oracolul pe jumatatea de evaluare +0.007514, optimism
+0.003883. Mai mare decat la LOLO, si trebuie sa fie: cu 5 limbi de selecție alegerea e mai zgomotoasa
decat cu 9. Procedura iese negativa pe **9%** din impartiri.

Stabilitatea alegerii pe cele 252 de impartiri: `M3K` 43%, `FM4K` 28%, `FS3K` 13%, `FS3P` 12%, restul
sub 2%. Deci `FS3K` NU e ce alege o procedura onesta; e a treia.

## Sistemul cu configuratia aleasa LOLO, construit si evaluat

`output/fusion_preds_lolo_cfglolo.csv`. r = **0.688383**, +0.004520 fata de 0.683849, CI pereche
[+0.001711, +0.007231], P(>0) = 99.9%. Urca germana si franceza cu interval care exclude zero.

**Dar STRICA portugheza: -0.0049 [-0.0096, -0.0003].** Fiindca pentru pt configuratia aleasa pe
celelalte noua e chiar `FM4K`, adica exact cea care coboara pt. Asta e modul in care selecția LOLO
poate sa cada: nu protejeaza o limba de o configuratie buna in alta parte si proasta acolo.

Deci **si varianta cu procedura curata cade pe conditia a doua**, aceeasi care a respins `distTpp`,
`prio_KW`, `FM4`, `FM4K`. Singurele doua care trec ambele conditii rams `M3K` (0.690001) si `FS3K`
(0.688506), si ele nu se distinge intre ele.

## Ce se citeste de aici, si e cifra de folosit

Castigul onest de asteptat pe o limba noua din toata linia asta de lucru e **~+0.0045**, nu +0.0065.
Numarul de test al unei configuratii e nedeplasat PENTRU acea configuratie, dar motivul pentru care te
uiti la ea e ca a castigat, deci cifra raportata poarta acelasi optimism de +0.0019.

Pentru scara: intervalul propriu al lui r pe sistem e [0.6694, 0.6980], adica ±0.015. Toata discutia
dintre 0.6885 si 0.6903 e despre o marime de cinci ori mai mica decat incertitudinea cifrei insesi.

Vezi [[ansamblul-de-prompturi-formula]] pentru configuratii, [[bifurcatii-de-declarat]] pentru ce se
declara.
