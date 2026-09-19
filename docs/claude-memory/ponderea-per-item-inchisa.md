---
name: ponderea-per-item-inchisa
description: "22 aug 2026 - w per item in fuziune: selectia alege a = 0 pe 10/10 limbi si la semnal real si la zgomot; dar grila largita strica prin criteriul imbricat chiar cand parametrul nu se foloseste"
metadata:
  type: project
---

Rulat **22 august 2026**. Zero inferenta. `fuse_ab.py --h {entropie,dezacord,zgomot} --h-src ...`

## Ce s-a incercat

`w_i = clip(w + a*h_i, 0, 1)`, cu `h` standardizat in interiorul limbii si `a` ales LOLO impreuna cu
`w`, pe o grila de 7x21 = 147 de perechi care CONTINE `a = 0`. Doua marimi `h`: entropia distributiei
lui B la T ales LOLO, si dezacordul JS intre cele doua prompturi. Atomii efectivi sunt exclusi
deliberat, fiind `exp(entropie)`, deci o transformare monotona.

## Rezultat

**Selectia alege `a = 0` pe toate zece limbile, si la entropie, si la dezacord, si pe cinci seminte de
zgomot pur.** Nu o cifra mica, zero exact. Podeaua de zgomot a parghiei e chiar 0.000000: procedura
imbricata, cu punctul neutru in grila, nu urmareste zgomotul.

Controlul de reproducere trece: cu grila lui `a` redusa la zero, `p_fuz` iese identic la **0.0** fata
de `output/fusion_preds_lolo_adoptat_temp.csv` si r pana la a zecea zecimala.

## Efectul secundar, si e general, nu despre parghia asta

`dezacord` iese la **-0.000331** desi `a = 0` peste tot. Pierderea vine din nivelul al doilea al
selectiei: acolo argmaxul peste matricea (a, w) al unei limbi de potrivire poate cadea pe `a` nenul,
ceea ce muta `w_src` ales pentru limba tinuta deoparte. Pe sinhaleza `w_src` sare de la 0.750 la 0.250
si limba pierde -0.0031.

**Why:** un grad de libertate in plus poate strica si atunci cand ajunge sa nu fie folosit, prin
criteriul imbricat, nu prin parametrul insusi. E un argument in favoarea grilelor mici peste tot in
`fit_choice`, nu doar aici.

**How to apply:** orice largire de grila in `fuse_ab.fit_choice` se masoara si cu parametrul nou fixat
la neutru, ca sa se separe efectul parghiei de efectul largirii. Vezi [[criteriu-plat-mediaza-nu-alege]].
