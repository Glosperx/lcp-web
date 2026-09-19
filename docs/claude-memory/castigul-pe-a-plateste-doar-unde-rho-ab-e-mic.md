---
name: castigul-pe-a-plateste-doar-unde-rho-ab-e-mic
description: "Regula transversala masurata 26 aug 2026: pe cele 10 limbi, corelatia intre CAT CREŞTE r_A si CAT CREŞTE rho(A,B) e +0.917. Deci un castig pe A plateste in fuziune numai unde rho(A,B) e deja mic, adica practic numai pe sinhaleza."
metadata:
  type: feedback
---

Explica de ce **sase sesiuni la rand** au gasit castiguri reale pe semnalul A care nu au ajuns
niciodata in fuziune. Nu e ghinion, e aritmetica, si acum are o cifra.

Frontiera spune ca `r_fuz` creste cu `r_A` si SCADE cu `rho(A,B)`. Identitatea e verificata pe fiecare
limba la 2.22e-16, deci nu e o aproximare.

**Masurat pe `ridge + orde-hgb-k5` fata de sistemul adoptat, pe cele zece limbi:**

    corelatia intre d(r_A) si d(rho(A,B))              +0.917

Aproape o identitate empirica: fiecare limba pe care A se imbunatateste e o limba pe care A devine mai
asemanator cu B, si al doilea efect mananca primul.

**Excepția, si e singura, spune unde s-ar putea plati:**

    limba   rho(A,B) de pornire   d r_A     d rho(A,B)   d r_fuz
    si            0.387          +0.0286     +0.0511     +0.0048   <- singurul castig real
    ja            0.597          +0.0166     +0.0226     -0.0028
    ca            0.534          -0.0177     -0.0098     -0.0054

Pe sinhaleza `rho(A,B)` de pornire e cel mai mic din set, deci exista loc: rho urca mult si fuziunea
tot creste. Pe japoneza, unde B e deja puternic (0.7795), acelasi tip de castig pe A da fuziune
negativa.

Acelasi lacat se vede si peste MODELE, nu doar peste limbi. Pe cele 231 de perechi de regresori
masurate pe 26 august, corelatia intre `r_A` si `rho(A,B)` e **+0.915**. Deci nu e o proprietate a
limbilor, e o proprietate a spatiului: orice pereche mai buna pe A e mai asemanatoare cu B.

**Why:** un A mai bun obtinut pe limbile unde B e deja bun e redundant cu B prin construcie. Fuziunea
plateste pentru informatie NOUA, nu pentru acuratete.

**How to apply:** orice propunere pe semnalul A trebuie sa vina cu `rho(A,B)` PE LIMBA inainte de a fi
crezuta, nu doar cu `r_A`. O sesiune pe A care nu se uita la asta e o sesiune care va gasi un castig si
il va pierde in fuziune. Concret, urmatoarea sesiune pe A ar trebui sa fie despre **sinhaleza si
filipineza** (unde `rho(A,B)` e mic si lipsesc `wordfreq` si lematizatorul), nu despre algoritmi.

Vezi [[transmisia-a-fuziune-masurata]], [[frontiera-e-identitate-nu-aproximare]],
[[sinhaleza-decorelarea-e-capitalul]], [[filipineza-mecanismul-frecventei]],
[[sesiunea-obiectivului-rezultatul]].
