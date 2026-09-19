---
name: pooling-first-inverseaza-literatura
description: "23 aug 2026 - poolingul `first` peste subword-urile tintei bate `last` cu +0.0253 pe 10/10 limbi, INVERS fata de Acs et al. EACL 2021; ansamblul cu `first` da 0.686010 dar strica filipineza"
metadata:
  type: project
---

Masurat **23 august 2026**, sweep de 16 configuratii (straturi x pooling) pe xlmr.
`analysis_extractie.py` -> `output/e_extractie.md`. `--emb-cfg` a fost expus in `finetune_xlmr.py`;
`frozen_trial_gap` accepta parametrul de cand exista dar `main()` nu-l pasa niciodata.

## Rezultatul

`first` bate `last` cu **+0.0253** pe bratul A, cu acelasi semn pe **10 limbi din 10** si pe toate
cele 4 familii de straturi. Acs, Kadar si Kornai (EACL 2021, "Subword Pooling Makes a Difference")
masoara exact invers pe probing morfologic: `first` e cea mai proasta strategie, pana la 45 de puncte
sub `last` pe finlandeza.

**Explicatia, si e o delimitare de domeniu, nu o contrazicere.** Ei probeaza morfologie (caz, gen,
forma verbala), care traieste in SUFIX. Noi prezicem o proprietate lexicala, care tine de identitatea
cuvantului. Ultimele bucati sunt fragmente scurte impartite de mii de cuvinte (`ts`, `es`, `a`), deci
nu identifica lexemul; prima bucata poarta materialul initial. Verificat in trei feluri: efectul
creste cu fertilitatea (r = +0.726, p = 0.017), e mai mare pe tintele multi-subword (+0.0299 fata de
+0.0253), si e maxim pe sinhaleza (+0.097).

Nuanta: segmentarea XLM-R nu e morfologica (`controvertits` -> `contro`+`verti`+`ts`), deci
formularea corecta e "ultima bucata e un fragment impartit, prima nu", nu "prima bucata e lema".

## Straturile NU conteaza, si de ce e usor de gresit

Latimea PE LIMBA e aproape identica pe cele doua axe (0.0296 pooling, 0.0287 straturi), deci dupa ea
ar parea la fel de importante. Dupa mediere se despart: 0.0253 fata de 0.0087. Ce le separa e
**constanta semnului**: pooling 10/10, straturi 7/10. Selectia LOLO peste toata grila de 16 valoreaza
+0.00016 peste podeaua de zgomot, adica nimic.

## Cifra, si de ce NU se adopta

Ansamblul de trei encodere cu `first` da **0.686010**, cea mai mare cifra a sesiunii, **+0.0022 fata
de sistem**, CI al mediei [+0.0004, +0.0039], P = 99.0%, in urcare pe 8 limbi din 10. Sinhaleza urca
cu **+0.0154** (0.4251 -> 0.4406).

**Dar filipineza e stricata cu CI care exclude zero**, -0.0028 [-0.0052, -0.0003]. Protocolul cere ca
aceasta conditie sa se citeasca INAINTEA mediei, deci nu se califica. Si +0.0022 e oricum sub bara de
+0.0045. Coerent cu mecanismul: `fil` are 11.9% tinte de un singur subword, deci e printre limbile
unde `first` aduce cel mai putin.

Vezi [[transmisia-a-fuziune-masurata]] si [[criteriu-plat-mediaza-nu-alege]].
