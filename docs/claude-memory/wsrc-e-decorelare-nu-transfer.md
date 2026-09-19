---
name: wsrc-e-decorelare-nu-transfer
description: "23 aug 2026 - w_src=0.738 NU inseamna ca transferul din engleza e mai bun; p_en e mai SLAB (0.5945 vs 0.5980) dar mai decorelat de B pe 9/10 limbi, iar toata parghia valoreaza 0.0027"
metadata:
  type: project
---

Masurat **23 august 2026**, `analysis_wsrc.py` -> `output/e_wsrc.md`. Zero inferenta.

## Premisa intrebarii era falsa

`p_en`, antrenat numai pe CompLex EN, da **0.5945** pe zece limbi. `p_multi`, care vede in plus
randurile de test ale celorlalte noua, da **0.5980**. Deci bratul englez **nu e mai bun**, e cu
0.0035 mai slab, si castiga pe doar 6 din 10 limbi cu marje mici. Fisa veche care spunea "bratul
EN-only e in medie mai bun, 0.5687 fata de 0.5630" e dinainte de ansamblul de encodere; s-a inversat.

## Criteriul e plat, si argmaxul e zgomot

Curba adevarata a lui `w_src` pe test are latimea medie **0.0067**; curba de criteriu, adica exact ce
vede `fit_choice`, are **0.0033**. Argmaxul criteriului nimereste argmaxul adevarat pe **1 din 10
limbi**. Costul selectiei fata de oracol e doar -0.0027, tocmai fiindca e plata.

Fuziunea cu `w_src` FIXAT, media pe zece limbi: 0.682053 la `w_src=0`, monoton pana la 0.684764 la
`w_src=1`. Selectia LOLO da **0.683849**. **Toata parghia valoreaza 0.0027 cap la cap**, adica sub
bara de +0.0045.

## Mecanismul, masurat direct

Corelatia cu semnalul B: `p_multi` **0.7084**, `p_en` **0.6813**. `p_en` e mai decorelat pe **9 din
10 limbi**, diferenta medie +0.0270, iar pe `si` +0.1521. Frontiera A+B la 50/50 prezice +0.0025 in
favoarea lui `p_en`, iar diferenta masurata cap la cap e +0.0027. Se inchide exact.

**Deci:** bratul englez cantareste mai mult fiindca, nevazand niciun rand de MLSP, face ALTE greseli
decat un LLM care vede propozitia. Fuziunea plateste pentru greseli diferite, nu pentru greseli mai
putine. Acelasi mecanism ca [[frontiera-e-identitate-nu-aproximare]], la alt nivel.

**How to apply:** in paper, `w_src` nu se prezinta ca rezultat despre transfer cross-lingual. Se
prezinta ca reducere de varianta intre doua surse de antrenare, si se declara ca parghia e de 0.0027.
Vezi [[criteriu-plat-mediaza-nu-alege]].
