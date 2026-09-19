---
name: cerere-sesiune-gbdt
description: "INCHISA - sesiunea s-a facut, rezultatul e in sesiunea-obiectivului-rezultatul. Ipoteza despre LOSS a ieșit greșita (si axa nu era neatinsa), dar INCADRAREA ordinala e vie."
metadata:
  type: project
---

**INCHISA 26 august. Rezultatul, cu toate cifrele, e in [[sesiunea-obiectivului-rezultatul]]; regula
transversala care a ieșit din ea e in [[castigul-pe-a-plateste-doar-unde-rho-ab-e-mic]].** Ce urmeaza e
cererea originala, pastrata pentru context.

Cerut imediat dupa ce [[axa-liniara-inchisa]] s-a incheiat fara nicio adoptare. Prima formulare a fost
"as vrea sa incerci si un lightgbm sau poate un catboost ceva, dar asta in alta sesiune de claude", apoi
a largit-o explicit: **"vreau sa avem research sa vedem ce algoritmi sa mai testam, nu doar lightgbm si
catboost"**. Deci sesiunea incepe cu cernere si argumentare, nu cu rulare. Explicit intr-o SESIUNE NOUA.

Promptul, scris in proza completa fiindca il citeste alt agent: `PROMPT_sesiune_gbdt.md` in radacina.
A cerut explicit sa NU fie scris in stil caveman.

## Reformularea care da valoare sesiunii, si e contributia mea la cerere

Poarta e `rho`, nu `r`, iar pe 26 august s-a masurat un compromis STRICT intre ele peste 21 de
candidati x 3 encodere: tot ce coboara rho sub 0.811 pierde r_A (`lasso-a3e-2` rho 0.739 dar r 0.4746;
`krr-rbf` rho 0.726 dar r 0.5322), si tot ce urca r urca si rho (`lasso-a1e-3` r 0.5689, cel mai bun
de pe axa, dar rho 0.858).

**Ipoteza: motivul e ca toti candidatii de pana acum minimizeaza EROAREA PATRATICA pe ACEEASI tinta.**
Familia de functii s-a schimbat enorm (liniar dens, liniar rar, kernel, bagging, boosting, ICL), dar
obiectivul niciodata. Iar `rho` nu masoara cat de mari sunt erorile, ci UNDE sunt. Deci parghia care
lipseste nu e a saptea familie de arbori, e alt loss sau alta tinta.

**Nemasurata, scrisa din raționament.** Sesiunea trebuie sa o verifice, nu sa o creada. Contra-exemplu
posibil: `krr-rbf` are cel mai mic rho de pe axa (0.726) si e tot eroare patratica.

## Ce am verificat ca e GENUIN neatins in cod (26 aug)

`TransformedTargetRegressor`, `MLPRegressor`, `KNeighborsRegressor`, `RandomForest`,
`loss="absolute_error"`, `loss="quantile"`, `linear_tree`, transformarea pe rang: **niciunul nu apare
nicaieri**. Tinta `complexity` e in [0, 0.975] cu **28 de zerouri exacte** si zero unu, deci un logit
cere epsilon de strangere.

Cele trei axe propuse in prompt: (1) familia de functii, aproape epuizata, mai lipsesc lgbm, catboost,
randomforest, lgbm cu `linear_tree`, MLP, kNN; (2) LOSS-ul, complet neatinsa; (3) incadrarea ca
**clasificare ordinala pe 5 clase plus valoare asteptata**, adica exact ce face semnalul B dar pe
embedding, si e candidatul cu cea mai mare sansa de rho mic fiindca schimba complet structura erorii.

## Criteriul de cernere, ca sa nu se cheltuie 3 encodere degeaba

Trece la 3 encodere numai ce are `rho(X, ridge) < 0.811` **SI** `r_A > 0.53`. Fiecare conditie luata
separat nu spune nimic despre blend. Orice candidat propus in plus se judeca la fel, si se argumenteaza
de ce ar cobori rho, nu de ce ar urca r.

## Priorul, ca sa nu se citeasca un +0.001 drept succes

Familia de arbori a fost deja variata si nu conteaza in blend (`extratrees` bate `hgb` cu +0.022 singur
dar `blend-et` e la +0.0004 de `blend`); capacitatea mai mare strica (`hgb-adanc` -0.046); si transmisia
A -> fuziune iese ~ZERO pe axa regresorului (A a urcat +0.0030 pe 3/3 encodere, fuziunea nu s-a miscat).
Bara e +0.0045.

## Unelte gata, si capcana de legare

`_FAM` plus `regressor_kind`, `make_reg_runs.py`, `analysis_regresor.py`, `analysis_regresor_multi.py`,
`make_a_blend.py`, `make_enc_mean.py --cai`. Vezi [[cod-nou-axa-liniara]].

`lightgbm`, `catboost`, `xgboost` NU sunt instalate in `envs/ml_def`. LightGBM si CatBoost trateaza NaN
nativ, deci se leaga ca `_hgb_pred`, **fara imputer**; `MLPRegressor` si `KNeighbors` NU, deci ele merg
prin `_pipe_pred`. Conteaza: `ja` si `si` au coloane de suprafata NaN, si exact asta a facut `lasso` sa
nu poata rula niciodata.
