---
name: distributia-b-temperatura
description: ADOPTAT 20 aug 2026 - sistemul e 0.683849 cu temperatura aleasa LOLO; 0.674946 devine ablatia fara temperatura. Se revendica un platou de T, nu o valoare.
metadata:
  type: project
---

**Cifra de citat e 0.683849**, pe n=5624, din `output/e_fusion_lolo_adoptat_temp.md`, interval
[0.6694, 0.6980]. Inlocuieste 0.674946 din [[p11-adoptia-facuta]], care ramane valid ca **ablatia
cu T=1**, nu ca cifra moarta. Diferenta +0.0089, interval pereche [+0.0056, +0.0124].

**Ce se revendica e un platou, nu o valoare a lui T.** Castigul fata de T=1 are interval care exclude
zero pe 19 din 21 de valori intre 1.25 si 64, iar intre T=4 si T=24 r variaza cu 0.0028. Daca vine
intrebarea „de ce T=12", raspunsul e tabelul (e) din `output/e_dist.md`, nu o justificare a valorii.

**Temperatura e parghia lui Nohejl**, aia care duce G-Eval 0.657 la G-Scale 0.669. Intra la
rezultate, NU la contributii. Ce e al nostru e ca T se alege fara nicio eticheta din limba evaluata,
pe cand el il alege pe trial-ul tuturor celor zece. Vezi [[noutate-si-precedente-lcp-multilingv]].

**Doua variante respinse deliberat**, ca sa nu fie reluate: 0.682977 e cu grila din briefing, care se
termina la T=4 exact unde cade argmaxul la toate zece limbile, deci argmax pe margine; 0.685763 e cu
cate o temperatura per prompt, mai mare dar aleasa dintre 256 de perechi cu marginea 0.001 pe un
criteriu lat de 0.085, si strica spaniola cu interval care exclude zero.

**Entropia si masa pe capete au murit la controlul corect.** Par sa aiba validitate incrementala
peste B liniar, dar dispar complet la control flexibil (B, B^2, B^3): erau curbura lui B, adica exact
ce repara temperatura, citita a doua oara. Supravietuieste numai dezacordul INTRE cele doua
prompturi, la jumatate din marime. Regula generala: cand semnalul nou e o functie de aceeasi
distributie ca semnalul vechi, controlul liniar pe cel vechi nu decide nimic. Vezi
[[criteriu-plat-mediaza-nu-alege]].

**Cum se scrie in paper:** temperatura se citeaza la Nohejl CHIAR acolo unde apare cifra, nu doar in related work. Un reviewer care stie G-Scale altfel vede +0.0089 aparut din senin. Formularea care ne avantajeaza: noi alegem T fara nicio eticheta din limba evaluata, el il alege pe trial-ul tuturor celor zece. Vezi si [[parametri-llm-de-explorat]].

**Ramas de facut, 20 aug:** `output/update_paper_draft.txt` si paperul inca spun 0.674946. Nu le-am
atins, din cauza regulii din [[update-paper-draft-linia-de-taiere]].

## CE FACE de fapt temperatura, masurat 21 august

Nu muta greutatea de la capul distributiei la coada. **Capul si coada sunt doua citiri aproape la fel
de bune si parțial independente ale aceleiasi distributii, iar T gaseste proportia intre ele**, si
amestecul bate ambele capete:

| ce se citeste | pe trial | pe test |
|---|---|---|
| cifra generata, adica argmaxul | +0.6777 | +0.6274 |
| capul: citire moale la T=1 | +0.6860 | +0.6420 |
| coada: citire moale la T -> infinit | +0.6852 | +0.6550 |
| amestecul: la T ales LOLO | **+0.7067** (T=8) | **+0.6592** |

Coada e `analysis_dist.s_limit`, `suma_i (i-3) log p_i`, forma inchisa a limitei. E gratis de calculat
si e diagnosticul care spune daca T mai are de unde sa scoata: cand coada se strica, T* cade si
castigul dispare, chiar daca masa pe argmax si entropia rams identice. Asa s-a inchis prefixul de
citire, vezi [[pozitia-de-citire-masurata]].

Pentru ce inseamna asta la „de ce citirea moale bate cifra generata": cifra generata da 87 de valori
distincte pe 5624 de randuri, citirea moale da 5624, deci discretizarea plafoneaza Pearson.

## Doi candidati peste ea, din 21 august

`prio_K`, unirea cifrelor vecine, da **0.685530**, +0.00168, CI pereche [+0.00072, +0.00269], zero
limbi stricate. Vezi [[prioritizarea-parghiilor-masurata]].

`FS3K`, ansamblul de trei prompturi plus unirea cifrelor, da **0.688506**, +0.004642, CI pereche
[+0.002619, +0.006756], zero limbi stricate, si e ADITIV cu `prio_K`. Vezi
[[fewshot-pe-test-masurat]].

**Niciunul nu e adoptat, si pana la o decizie cifra de citat ramane 0.683849.** Doua intrebari deschise
lasate lui Alexandru pe 21 august seara: (1) se adopta `FS3K`, care insa CONTINE `prio_K` refuzat
dimineata si trece conditia „nicio limba stricata" pe muchie prin germana la -0.0055 [-0.0122,
+0.0014]; sau `FS3` singur, care strica germana cu -0.0110; sau nimic, si cifra intra in Limitations.
(2) se ruleaza cate un T per prompt in ansamblul de trei, care acum imparte un singur T=6 desi
few-shot singur vrea T=4 si perechea zero-shot vrea T=12. A doua e gratis, `make_bt_runs.pick_temps`
are deja grila `per-prompt`.
