---
name: sesiunea-obiectivului-rezultatul
description: "26 aug 2026 - sesiunea de research pe algoritmii lui A: 49 de rulari, 4 axe. Ipoteza despre LOSS e greșita, dar INCADRAREA ordinala e vie: +0.0083 pe A pe 3/3 encodere si pozitiva pe ambele brate. Fuziunea tot nu se mișca, si acum se stie DE CE."
metadata:
  type: project
---

Rezultatul cererii din [[cerere-sesiune-gbdt]]. **Sistemul rămâne 0.690001.** Rapoarte:
`output/e_obiectiv_sinteza.md` (sinteza, regenerabila), `e_regresor_obiectiv.md` (3 encodere),
`e_regresor_obiectiv_xlmr.md` (54 de candidati pe unul), `_predictii_obiectiv.md` (pre-inregistrarea).

49 de rulari, 71 de minute de CPU, 2 caderi reluate cu succes. Cod: [[cod-nou-sesiunea-obiectivului]].

## Premisa cererii era partial FALSA, si asta s-a aflat inainte de a rula orice

Axa loss-ului NU era neatinsa: `huber` si `svr-lin` sunt amandoi pierderi non-patratice in familia
liniara, deci exact experimentul cerut, si erau pe disc. Ce muta rho, masurat pe xlmr:

    penalizare 0.243 (lasso-a3e-2) > familie 0.189 (hgb) > regularizare 0.123 > LOSS 0.020-0.040

**Loss-ul e cea mai SLABA parghie din tabel.** Mecanismul: `r` e invariant la transformari afine, iar
pentru un liniar directia care minimizeaza patratul e chiar cea care maximizeaza corelatia, deci
schimbarea pierderii e aproape un no-op prin construcie. Prezis din asta si CONFIRMAT: la arbori
pierderea e o parghie de 2.5x mai mare, `1-rho(hgb-abs, hgb)` = 0.050 fata de 0.020 la `huber`.

## Raspunsul la intrebarea de research, pe 3 encodere

    clasa           n   slack mediu    cel mai bun delta
    REGULARIZARE   15      +0.0139     +0.0068 (lasso-a3e-3)     <- norul de referinta
    FAMILIE        14      -0.0046     +0.0091 (extratrees)
    LOSS            4      -0.0079     +0.0003 (huber)
    TINTA           7      -0.0205     +0.0008 (tt-logit2-ridge)
    INCADRARE       8      +0.0172     +0.0083 (orde-hgb-k5)
    INFORMATIE      4      -0.0187     -0.0016 (w-ridge-c1)

Agregatul da NU (+0.0026, in banda prezisa de ±0.010), **dar agregatul e statistica greșita**: cele
trei clase de obiectiv se despica pe 0.0377, de 14 ori mai mult. Pierderea si tinta sunt moarte,
incadrarea e singura clasa non-reper cu slack pozitiv.

## Mecanismul, izolat pe aceeasi baza HGB

`hgb-abs` si `orde-hgb-k5` decoreleaza de baza cu aproape acelasi lucru, 0.050 fata de 0.054. Toata
diferenta e ce se intampla cu `r`: pierderea il pierde (-0.0110), incadrarea il urca (+0.0206).
Decorelarea era disponibila pe ambele drumuri, semnalul supravietuieste pe unul.

**Unde:** `hgb` se prabuseste fata de `ridge` pe exact doua limbi (ja -0.1756, si -0.0626), iar
incadrarea ordinala recupereaza exact acele doua (ja +0.1458, si +0.0862), restul fiind neutru. Iar
`hgb-abs` strica exact limba critica (ja -0.0969). Vezi [[sinhaleza-decorelarea-e-capitalul]].

## Rolul in care judeci candidatul muta verdictul cu 0.017

Codul de dinainte compara fiecare candidat numai ca `X + hgb`, adica in locul jumatatii LINIARE. Pe
`extratrees`, media pe 3 encodere: **-0.0079 in locul lui ridge, +0.0086 in locul lui hgb, +0.0080 ca
al treilea.** Un tabel cu un singur rol arata cel mai bun al treilea membru drept cel mai prost
candidat. Cele trei roluri sunt acum in cod.

## Ce e nou si conteaza: patru candidati pozitivi 3/3 pe AMBELE brate

Sesiunea trecuta ([[axa-liniara-inchisa]]) gasise unul singur, `ridge-a1000`. Acum:

    extratrees   p_multi +0.0091   p_en +0.0064      cat-d3       +0.0088   +0.0028
    orde-hgb-k5  p_multi +0.0083   p_en +0.0064      rf-n300      +0.0076   +0.0030

Propozitia "si aici nu tine niciunul" din `analysis_regresor_multi.py` a devenit FALSA fara sa crape
nimic; e acum calculata. Al treilea caz de [[constante-hardcodate-mint-dupa-renumerotare]].

## Fuziunea: nimic nu trece, dar cifra care conteaza e alta

3 encodere, `--ens`, acelasi B (M3K), fata de 0.6900: cel mai bun e `ridge+hgb+orde-hgb-k5` la
**+0.0002, P 58.1%**. Pe xlmr singur cel mai bun e +0.0020 (dar acela e ales pe test). Bara e +0.0045.

Maximul peste 6017 submultimi e 0.5885 pe A, umflat cu **+0.0081**; selectia onesta LOLO da 0.5804,
adica SUB `ridge+hgb+extratrees` (0.5818) care era deja cunoscut. Optimismul de selectie e acum
masurat si tiparit de `analysis_regresor.py`.

## De ce nu se mișca: vezi [[castigul-pe-a-plateste-doar-unde-rho-ab-e-mic]]

Acolo e cifra care inchide toata axa A, nu doar sesiunea asta.

## Cernerea COMPLETA a perechilor, facuta la cererea lui Alexandru dupa sesiune

Intrebarea a fost: dintre perechile care bat `ridge+hgb` pe `r_A`, exista una cu `rho(A,B)` mai MIC?
Masurat pe toate cele **231 de perechi** din 22 de membri prezenti pe 3 encodere (B nu depinde de A,
deci coloana B din rularea adoptata e B-ul corect pentru orice pereche):

    reper ridge+hgb:  r_A 0.5980   rho(A,B) 0.7021
    perechi cu r_A mai MARE si rho(A,B) mai MIC:  14 din 231     <- DA, exista

Duse in `fuse_ab` real, toate cad: intre -0.0014 si +0.0000, `P(>0)` intre 33% si 46%.

    cat-d3+orde-lin-k5   r_A 0.6027   fuziune 0.6894  -0.0006
    cat-d3+pls-k16       r_A 0.6036   fuziune 0.6898  -0.0002
    cat-d3+lasso-a3e-4   r_A 0.6028   fuziune 0.6900  +0.0000
    cat-d3+krr-rbf       r_A 0.6061   fuziune 0.6886  -0.0014   <- cel mai bun r_A masurat VREODATA

**`cat-d3+krr-rbf` are cel mai bun `r_A` din tot proiectul (+0.0068 peste sistem), trece si poarta de
rho, si da cea mai proasta fuziune din tabel.** Corelatia `r_A` cu fuziunea reala peste cele 13
configuratii duse pana la capat: **+0.393**.

Unde sta `ridge+hgb`: locul **51/231 pe r_A**, **161/231 pe rho(A,B)**, si nebatuta in fuziune. E
mediocra pe fiecare axa separat. Motivul: corelatia `r_A` cu `rho(A,B)` peste cele 231 de perechi e
**+0.915**, acelasi lacat ca cel de +0.917 pe limbi.

**Capcana de metoda, platita:** un screening analitic pe `p_multi` a prezis +0.0013..+0.0022 pentru
toate cele sapte perechi de sus, iar realitatea a dat -0.0014..+0.0000. Bias sistematic **-0.0020**,
corelatie cu realitatea doar +0.575. Cauza: la nivel `p_multi` rho(A,B) al sistemului e 0.7021, dar la
nivelul lui A real, cu ambele brate, e 0.6870 - deci bratul `p_en` face el o parte din decorelare, iar
orice candidat care imbunatateste `p_multi` mananca din ea. **Nu se cerne pe `p_multi` si nu se citeaza
o cifra analitica de fuziune fara `fuse_ab`.**

Un pozitiv: **`cat-d3` apare in 9 din primele 10 perechi ale cernerii.** CatBoost e cel mai bun membru
nou gasit; daca vreodata `rho(A,B)` scade din alt motiv, el e primul de reincercat.

## Ce s-a inchis

Familia de functii (al doilea punct pe tendinta, acum cu lgbm, catboost, randomforest, foi liniare,
MLP, kNN), pierderea, functionalul tintei, informatia prin subspatii fixe si prin ponderare pe coada.
Rămâne VIE numai incadrarea ordinala, si numai ca mecanism, nu ca adoptare.
