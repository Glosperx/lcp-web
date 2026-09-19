---
name: tabfm-maxfeat256-rezultatul
description: "26 aug 2026 - rularea TabFM la MAXFEAT=256 s-a terminat: A urca +0.0132 dar rho urca si el la 0.887, fuziunea da 0.6806 vs 0.6803 controlul, P(>0)=51.8%. Axa e inchisa cu al treilea punct pe tendinta."
metadata:
  type: project
---

Rezultatul rularii cerute in [[cerere-verificare-parametri-tabfm-256]]. **Raspuns masurat, axa
[[axa-regresorului-inchisa]] ramane inchisa, acum cu masuratoarea directa care lipsea.**

## Rularea

12 cereri x 8 membri pe T4, doua sesiuni Colab gratuite (prima taiata dupa 8.5 cereri, reluata din
checkpointul pe membru fara sa piarda decat 4 membri). 56 min de GPU in a doua sesiune.
`setari.json` confirma ca **`max_num_features` e SINGURA diferenta** fata de rularea de la 160.
Toate 12 chei se potrivesc cu blocurile locale.

## Cifrele

    A singur           tabfm @160  0.5541      tabfm @256  0.5673      +0.0132

    fuziune, --arm lolo --fit test --pick-split test, acelasi B (M3K)
    ctrl    A = ridge+hgb      0.6803
    rt@160  A = ridge+tabfm    0.6798     -0.0005
    rt@256  A = ridge+tabfm    0.6806     +0.0003

    pereche, rt@256 vs ctrl    +0.0003   P(>0) = 51.8%    <- o moneda
    pe limbi                   5 sus / 5 jos; ja +0.0050 (96%) dar fil -0.0059 (0%) si en -0.0023 (3%)
    pereche, rt@256 vs ADOPTAT -0.0094   P(>0) = 15.9%

## De ce nu s-a miscat: A si rho se anuleaza

               rho(tabfm,ridge)  rho(tabfm,hgb)  mediu   prag cerut
    proj-200                                     0.829
    proj-394 @160     0.877           0.851      0.864     0.781
    proj-394 @256     0.900           0.873      0.887     0.813

**Al treilea punct pe aceeasi tendinta, toate trei in directia gresita.** Mai multa capacitate face
TabFM mai bun SI mai asemanator cu ce avem deja. Verdictul scriptului: `CADE`.

Transmisia se verifica singura: A a urcat +0.0037 pe bratul compus, fuziunea +0.0008, factor 0.22,
in intervalul 0.09-0.26 din [[transmisia-a-fuziune-masurata]]. Nimic anormal, doar castig mancat
de corelatie.

## Capcana care conteaza pentru decizie

0.6806 e sub 0.690001 al sistemului cu 0.0094, dar deficitul NU e al lui TabFM: ca sa poti rula
TabFM deloc trebuie sa reduci embeddingul la `proj-394` (nu incape pe 774) si sa renunti la media
celor trei encodere. Deci ca sa incasezi cele +0.0003 platesti -0.0094. **Sistemul ramane 0.690001.**

## Adaos, aceeasi zi: "ar ajuta hiperparametri mai mari" - NU, si acum se stie DE CE

**TabFM nu e boosting.** Se re-formeaza credinta asta periodic, deci: `_batch_forward` trece membrii
INDEPENDENT (`batch_size=1`) si `_combine_predictions` face `np.mean`. Bagging peste invatare in
context, nu boosting. Dovada operationala cea mai buna: checkpointul pe membru functioneaza — la
boosting membrul 5 n-ar putea fi calculat fara 1-4. Si `fit()` nu antreneaza nimic, greutatile vin
inghetate.

**Inlocuitor sau al treilea membru.** `ridge` si `hgb` sunt perechea cea mai decorelata din tabel
(0.815); tabfm e la 0.900 de ridge, deci MAI APROAPE decat e hgb. Valoarea lui hgb in blend nu e ca
e boosting, e distanta fata de ridge. De asta:

    ctrl        ridge+hgb        0.6803
    inlocuire   ridge+tabfm      0.6806   +0.0003   P 51.8%
    adaugare    ridge+hgb+tabfm  0.6810   +0.0007   P 68.3%

**Curba pe n_estimators, din cei 96 de membri de pe disc** (subseturi echilibrate pe familia de
normalizare; m0,m1=none m2,m3=power m4,m5=quantile_rtdl m6,m7=robust, fiindca
`prepare_ensemble_tensors` grupeaza pe norma):

     k     r_A   rho mediu   prag   distanta
     1  0.4755    0.764     0.601    0.163
     2  0.5479    0.868     0.767    0.101
     4  0.5586    0.876     0.792    0.084
    4b  0.5603    0.871     0.796    0.075
     8  0.5673    0.887     0.813    0.074

**MECANISMUL, masurat.** Un SINGUR membru are rho **0.764**, sub pragul de watch de 0.78-0.80 — cel
mai decorelat lucru de pe axa asta. Dar r e 0.4755. De la 1 la 2 membri rho sare la 0.868. Deci
**partea din TabFM care e decorelata de ridge e ZGOMOTUL lui, nu semnalul**; medierea sterge exact
acel zgomot. Nu e un efect secundar al lui `n_estimators`, e ce FACE `n_estimators`.

**Extrapolarea, pe metrica directa (deficitul de calitate, nu distanta in rho).** La rho-ul pe care
il are, ce r3 i-ar fi trebuit? k=1: 0.5467 cerut, 0.4755 are, deficit 0.0712. k=8: 0.5984 cerut,
0.5673 are, deficit 0.0311. Si r3 si rho converg ca 1/k, deci `deficit(k) = 0.04696/k + 0.02260`
(reziduu 0.0035 pe 4 puncte). La k=inf deficitul e **+0.0226, tot pozitiv**. 8 -> infinit cumpara
0.008 dintr-un deficit de 0.031. Nu e limita de tuning, e limita a ce poate medierea.

**Randul cu k=1 spune toata povestea axei.** E cel mai decorelat lucru masurat vreodata aici (0.764,
sub pragul de watch), si totusi adaugat in blend face A **mai prost cu 0.0083** (0.5666 fata de
0.5749). Decorelarea nu valoreaza nimic daca vine din zgomot. Iar la k=8, ca sa treaca bara, TabFM ar
trebui r=0.5984: mai bun decat ridge (0.5627), decat hgb (0.5326) si decat blend-ul intreg (0.5749).
Un al treilea membru ar trebui sa bata ansamblul de doi in care intra.

**Media pe encodere cu ridge+tabfm: aritmetica o inchide.** TabFM nu incape pe 774 de coloane pe T4
(~18-23 GiB fata de 14.6), deci fiecare brat trebuie mutat pe `proj-394`. Cat costa mutarea, masurat
pe acelasi B si acelasi protocol:

    A = blend pe xlmr PLIN (774)  fuziune 0.6828
    A = blend pe xlmr proj-394    fuziune 0.6803      proiectia costa -0.0025

Deci -0.0025 platit sigur pe fiecare encoder ca sa vanezi +0.0007 nedovedit. Raport 3.5:1 impotriva,
inainte de ~14 ore de GPU pe patru encodere. Ruta care ar evita handicapul e TabFM pe embeddingul
plin, adica o placa de 40 GB.

## Plafonul intregii axe, ca sa nu se redeschida a patra oara

TabFM nu se poate ANTRENA pe Colab: greutatile sunt inghetate, iar potrivirea ar cere ~24.6 GiB doar
greutati+gradienti+Adam in fp32, pe o placa de 14.6. Nici LoRA (backprop prin 24 de blocuri ICL la
T=14107). Deci doar configuratia la inferenta. Din cele sase configuratii masurate:

    scenariu                          r_A tabfm    rho   r_A(3)  vs blend  fuziune
    masurat azi   MAXFEAT 256, k=8      0.5673   0.887   0.5814  +0.0065   +0.0017
    PLAFON        MAXFEAT 400, k=inf    0.5927   0.925   0.5849  +0.0101   +0.0026

Bara e +0.0045, deci **plafonul nu o trece nici optimist**. Calibrare: identitatea prezicea +0.0017
iar `fuse_ab` a masurat +0.0007 (factor 0.41), deci castigul realist la plafon e **+0.0011**.

Cifra care inchide: plafonul optimist pe proj-394 e **0.6829**, iar `blend` pe xlmr PLIN fara TabFM
deloc si zero ore de GPU da **0.6828**. Tot calculul ar cumpara inapoi ce s-a pierdut ca sa poata
rula TabFM. Costul plafonului: ~79 ore de GPU pe A100 (la 420 de coloane reale varful e ~15.3 GiB,
peste T4), pentru +0.0011..+0.0026.

## Ce ramane refolosibil

`data/preds_proj394_maxfeat256/` cu cei 96 de membri separat in `_ckpt/`: ablatia pe
`n_estimators` (media primilor k) se calculeaza fara nicio rulare noua. `make_a_blend.py` e
constructia validata pentru orice A compus din CSV-uri (control pe `p_en` si `p_multi` la 1.11e-16).

Rapoarte: `output/e_tabfm_mf256.md` (sinteza), `e_fusion_lolo_rt_mf256*.md`,
`e_regresor_a_proj-394_mf{160,256}.md`. Cod: [[cod-nou-checkpoint-membru-tabfm]].
