# Sesiunea OBIECTIVULUI pe semnalul A: sinteza si raspunsul la cele doua intrebari

Generat de `make_obi_sinteza.py`. Toate cifrele se recalculeaza din predictiile de pe disc si din rapoartele lui `fuse_ab`; niciuna nu e tastata in text. Tabelele complete sunt in `e_regresor_obiectiv.md` (trei encodere) si `e_regresor_obiectiv_xlmr.md` (un encoder, toti candidatii). Predictiile scrise INAINTE de rulari sunt in `_predictii_obiectiv.md`.

## Ce s-a rulat

```
  rulari                49
  reusite               47
  cazute                2   (lgbm, coliziune libomp; reluate cu n_jobs=1)
  minute de CPU         71.3
  candidati distincti   29
```

## Intrebarea 1: a coborat vreun candidat `rho` fata de `ridge` sub 0.811 pastrand `r_A` peste 0.53?

**DA.** Poarta e trecuta de **7** candidati din 54, mediat pe cele trei encodere. Dar poarta, luata ca atare, nu separa ce trebuie, si asta e prima concluzie a sesiunii: pragul de `r` din cerere, 0.53, e SUB `r` al lui `hgb` insusi (0.5379), deci poarta admite candidati mai SLABI decat chiar membrul pe care ar trebui sa-l inlocuiasca. Iar reperul de rho, 0.811, e `rho(hgb, ridge)` pe xlmr; mediat pe cele trei encodere el e 0.793, deci poarta e usor mai larga decat pare cand se citeste ca o constanta.

```
  candidat           clasa            r_A  rho_ri    d_arb  verdict exact
  rf-n300            FAMILIE       0.5558   0.807  +0.0076          TRECE
  lgbmlin-l8         FAMILIE       0.5523   0.810  +0.0052          TRECE
  hgb-q50            LOSS          0.5363   0.787  -0.0017           CADE
  w-hgb-c1           INFORMATIE    0.5402   0.802  -0.0022           CADE
  tt-rank-hgb        TINTA         0.5349   0.784  -0.0024           CADE
  tt-logit2-hgb      TINTA         0.5328   0.794  -0.0051           CADE
  hgb-adanc          FAMILIE       0.5321   0.800  -0.0064           CADE
```

Criteriul EXACT pentru rolul acesta nu e o pereche de praguri, e identitatea de frontiera: `r(ridge + X) > r(ridge + hgb)`. Dintre cei 7 care trec poarta din cerere, **2** o trec si pe ea. Restul au `rho` mai mic dar `r` prea mic, adica exact tiparul masurat deja de patru ori in proiect: decorelarea care vine din zgomot nu valoreaza nimic.

## Intrebarea 2, cea de research: au candidatii care schimba OBIECTIVUL un `rho` sistematic mai mic la `r` comparabil?

`slack` e cat `rho` i-ar fi fost permis candidatului ca sa lege la egalitate cu controlul, la `r`-ul lui, minus cat `rho` are. Pozitiv inseamna sub curba de compromis. Iese direct din identitatea de frontiera, deci nu are niciun parametru potrivit.

```
  clasa            n  slack mediu  slack median  r_A mediu    cel mai bun delta
  REGULARIZARE    15      +0.0139       +0.0070     0.5500     +0.0068 (lasso-a3e-3)
  FAMILIE         14      -0.0046       -0.0023     0.5247     +0.0091 (extratrees)
  LOSS             4      -0.0079       -0.0091     0.5390     +0.0003 (huber)
  TINTA            7      -0.0205       -0.0137     0.5345     +0.0008 (tt-logit2-ridge)
  INCADRARE        8      +0.0172       +0.0141     0.5455     +0.0083 (orde-hgb-k5)
  INFORMATIE       4      -0.0187       -0.0133     0.5318     -0.0016 (w-ridge-c1)
  CONTROL          2      +0.0000       +0.0000     0.5519     +0.0000 (rs-ridge-f10-n1)
```

**Raspunsul agregat este NU.** Cele trei clase care schimba obiectivul, luate impreuna (n=19), au slack mediu -0.0019, iar `FAMILIE` (n=14) -0.0046. Diferenta e +0.0026.

**Dar agregatul e statistica greșita, si asta e rezultatul sesiunii.** Cele trei clase nu se comporta la fel; se despica pe 0.0377, adica de 14 ori mai mult decat diferenta pe care agregatul o raporteaza:

```
  LOSS         -0.0079   fata de FAMILIE -0.0033
  TINTA        -0.0205   fata de FAMILIE -0.0159
  INCADRARE    +0.0172   fata de FAMILIE +0.0218
```

Deci: schimbarea PIERDERII nu ajuta, schimbarea FUNCTIONALULUI TINTEI nu ajuta, dar schimbarea INCADRARII e singura clasa non-reper cu slack pozitiv. Ipoteza din cerere e corecta pentru o treime din ea si greșita pentru doua treimi, iar treimea corecta nu e cea pe care punea accentul (loss-ul), e a treia axa.

## Mecanismul: de ce incadrarea merge si pierderea nu

Comparatia care izoleaza. Aceeasi baza HGB, aceiasi hiperparametri, acelasi X, acelasi protocol; se schimba numai ce anume i se cere modelului sa prezica. Encoder xlmr.

```
  variantă         clasa             r  dr vs hgb  1-rho(X,hgb)
  hgb-abs          LOSS         0.5363    -0.0110         0.050
  hgb-q50          LOSS         0.5363    -0.0110         0.050
  orde-hgb-k5      INCADRARE    0.5678    +0.0206         0.054
  ord-hgb-k5       INCADRARE    0.5598    +0.0126         0.055
  clf-hgb-k5       INCADRARE    0.5562    +0.0090         0.070
  tt-rank-hgb      TINTA        0.5349    -0.0123         0.037
  tt-logit2-hgb    TINTA        0.5328    -0.0144         0.033
  w-hgb-c1         INFORMATIE   0.5402    -0.0070         0.029
  rs-hgb-f3-n10    INFORMATIE   0.5277    -0.0195         0.147
```

Cifra care explica totul: `hgb-abs` (pierdere L1) si `orde-hgb-k5` (incadrare ordinala) decoreleaza de baza cu aproape exact aceeasi cantitate, 0.050 fata de 0.054. Diferenta nu e cat de mult decoreleaza, e ce se intampla cu `r`: pierderea il pierde (-0.0110), incadrarea il urca (+0.0206). Decorelarea era disponibila pe ambele drumuri; numai pe unul supravietuieste semnalul.

Si reperul care raspunde la predictia pre-inregistrata: la LINIARI, aceeasi schimbare de pierdere decoreleaza doar 0.020 (`huber`) si 0.040 (`svr-lin`). Deci pierderea e o parghie de 2.5 ori mai puternica la arbori decat la liniari, exact cum prezice invarianta la transformari afine: pentru un liniar, directia care minimizeaza patratul e chiar directia care maximizeaza corelatia, deci schimbarea pierderii e aproape un no-op prin construcie.

Unde e concentrat, pe limba. `hgb` se prabuseste fata de `ridge` pe exact doua limbi, si incadrarea ordinala recupereaza exact acele doua:

```
  colapsul lui hgb fata de ridge   ja -0.1756  si -0.0626  ca -0.0070
  ce recupereaza orde-hgb-k5       ja +0.1458  si +0.0862  fr +0.0171
  pe restul limbilor               intre -0.0161 si +0.0066
```

Deci incadrarea ordinala nu face HGB mai bun in general. Ii repara colapsul pe japoneza si sinhaleza, adica exact sarcina pentru care jumatatea liniara era acolo. Iar `hgb-abs` strica exact limba critica (-0.0969 pe ja), si de asta axa pierderii e moarta chiar avand decorelarea de partea ei.

## Fuziunea reala, pe drumul care conteaza pentru sistem

`--arm lolo --fit test --pick-split test --ens`, acelasi B (M3K), media a trei encodere. Numai A variaza. Diferenta e PEREACHE.

```
  configuratie                                control      nou     delta   P(>0)
  encmean(ridge + hgb + orde-hgb-k5) + ens     0.6900   0.6902   +0.0002   58.1%
  encmean(ridge + hgb + cat-d3) + ens          0.6900   0.6901   +0.0001   52.8%
  encmean(ridge + orde-hgb-k5) + ens           0.6900   0.6895   -0.0005   42.0%
  encmean(ridge + cat-d3) + ens                0.6900   0.6896   -0.0004   36.1%
  encmean(ridge + hgb + rf-n300) + ens         0.6900   0.6895   -0.0005   40.0%
  encmean(ridge + hgb + extratrees) + ens      0.6900   0.6893   -0.0007   42.2%
  encmean(ridge + extratrees) + ens            0.6900   0.6881   -0.0019   30.2%
```

Bara e +0.0045. **Niciuna nu o trece.** Cea mai buna e +0.0002 (`encmean(ridge + hgb + orde-hgb-k5) + ens`) la P(>0) 58.1%, adica o moneda. Sistemul rămâne 0.6900.

## De ce nu se mișca: `r_A` si `rho(A,B)` sunt legate, si acum se stie cu cat

Frontiera spune ca `r_fuz` creste cu `r_A` si SCADE cu `rho(A,B)`. Identitatea e verificata pe fiecare limba la ordinul 1e-16 in codul care produce tabelul. Deci un A mai bun care e si mai asemanator cu B poate cobori fuziunea, si asta e ce se intampla.

`ridge + orde-hgb-k5` fata de controlul adoptat, pe limba:

```
  lg       r_B  r_A ctrl    d r_A  rho(A,B) ctrl  d rho(A,B)   d r_fuz
  si    0.3979    0.3166  +0.0286          0.387     +0.0511   +0.0048
  ja    0.7795    0.6031  +0.0166          0.597     +0.0226   -0.0028
  es    0.7553    0.7014  +0.0035          0.827     -0.0028   +0.0018
  fil   0.5000    0.4174  +0.0031          0.697     +0.0117   -0.0004
  pt    0.8243    0.7856  +0.0021          0.843     +0.0018   +0.0004
  fr    0.6752    0.5460  +0.0016          0.757     +0.0020   +0.0003
  de    0.7108    0.6784  -0.0015          0.610     +0.0093   -0.0026
  en    0.8471    0.8287  -0.0021          0.843     -0.0031   -0.0001
  it    0.6406    0.6489  -0.0034          0.773     -0.0013   -0.0010
  ca    0.5187    0.4668  -0.0177          0.534     -0.0098   -0.0054
```

Cifra care inchide axa: peste cele zece limbi, corelatia intre CAT CREŞTE `r_A` si CAT CREŞTE `rho(A,B)` este **+0.917**. Nu e o tendinta, e aproape o identitate empirica: fiecare limba pe care A se imbunatateste e o limba pe care A devine mai asemanator cu B.

Excepția, si e singura, spune unde s-ar putea plati. Pe sinhaleza `rho(A,B)` de pornire e 0.387, cea mai mica din set, deci exista loc: `r_A` urca +0.0286, `rho` urca +0.0511 si fuziunea tot CREŞTE cu +0.0048, cel mai mult din tabel. Pe japoneza, unde `rho` de pornire e 0.597 si B e deja puternic (0.7795), acelasi tip de castig pe A (+0.0166) da fuziune -0.0028.

**Regula care rezulta, si e transferabila la orice sesiune viitoare pe A:** un castig pe A plateste in fuziune numai pe limbile unde `rho(A,B)` e deja mic. Pe restul, imbunatatirea lui A e redundanta cu B prin construcie. Asta explica de ce sase sesiuni la rand au gasit castiguri reale pe A care nu au ajuns niciodata in fuziune, si nu prin ghinion.

## Predictie fata de masuratoare, pe candidat

Intervalele vin din `_predictii_obiectiv.md`, scrise inainte de instalare si inainte de orice rulare. Cifrele masurate sunt pe xlmr, encoderul pe care s-a facut cernerea si pe care au fost scrise predictiile. `r` cu referinta inseamna ca predictia era o DIFERENTA fata de baza invelisului, nu o valoare absoluta.

```
  candidat                 r prezis   r real      rho prezis  rho real   
  lgbm-l8               0.545-0.555  +0.5527 OK    0.80-0.83     0.821 OK
  cat-d3                0.545-0.560  +0.5610 !!    0.83-0.87     0.820 !!
  rf-n300               0.560-0.570  +0.5658 OK    0.86-0.89     0.827 !!
  lgbmlin-l8            0.565-0.580  +0.5579 !!    0.90-0.94     0.824 !!
  mlp-h128              0.535-0.565  +0.4694 !!    0.88-0.94     0.791 !!
  knn-k50               0.400-0.480  +0.3166 !!    0.60-0.75     0.518 !!
  hgb-abs               0.530-0.550  +0.5363 OK    0.93-0.97     0.950 OK
  hgb-q50               0.530-0.550  +0.5363 OK    0.93-0.97     0.950 OK
  tt-rank-ridge      -0.005..+0.005  -0.0480 !!    0.95-0.99     0.921 !! (fata de ridge)
  ttz-rank-ridge     -0.005..+0.005  -0.0058 !!    0.95-0.99     0.984 OK (fata de ridge)
  tt-rank-hgb        -0.005..+0.005  -0.0123 !!    0.93-0.98     0.963 OK (fata de hgb)
  ttz-rank-hgb       -0.005..+0.005  -0.0192 !!    0.93-0.98     0.960 OK (fata de hgb)
  tt-logit2-ridge    -0.005..+0.005  -0.0045 OK    0.94-0.98     0.986 !! (fata de ridge)
  tt-logit2-hgb      -0.005..+0.005  -0.0144 !!    0.92-0.97     0.967 OK (fata de hgb)
  tt-logit005-ridge  -0.020..-0.005  -0.0066 OK    0.94-0.98     0.984 !! (fata de ridge)
  ord-lin-k5            0.520-0.550  +0.5364 OK    0.93-0.97     0.929 !!
  ord-hgb-k5            0.530-0.560  +0.5598 OK    0.92-0.96     0.945 OK
  clf-hgb-k5            0.510-0.550  +0.5562 !!    0.90-0.95     0.930 OK
  rs-ridge-f3-n10    -0.005..+0.005  -0.0387 !!    0.90-0.96     0.866 !! (fata de ridge)
  rs-hgb-f3-n10      -0.005..+0.005  -0.0195 !!    0.90-0.96     0.853 !! (fata de hgb)
  w-ridge-c1         -0.010..+0.000  -0.0058 OK    0.92-0.97     0.992 !! (fata de ridge)
  w-hgb-c1           -0.010..+0.000  -0.0070 OK    0.92-0.97     0.971 !! (fata de hgb)
```

Bilantul: din 22 candidati cu predictie, `r` a cazut in intervalul prezis la **10** si in afara la **12**; `rho` la **9** si in afara la **13**.

### Unde am greșit, si ce spune fiecare greseala

1. **`mlp-h128` si `knn-k50`, amandoi mult sub intervalul de `r`** (0.4694 fata de 0.535-0.565, si 0.3166 fata de 0.400-0.480). Am subestimat cat de rau e spatiul de 774 de dimensiuni dense pentru un model care nu selecteaza coloane: MLP-ul cu un strat si oprire timpurie nu ajunge nici la nivelul lui `ridge`, iar distanta euclidiana pe 774 de dimensiuni e aproape neinformativa. Corolarul util e ca `rho` mic al lui `knn` (0.518, cel mai mic masurat vreodata pe axa) confirma a patra oara ca decorelarea din zgomot nu valoreaza nimic.

2. **`rs-ridge-f3-n10` si `rs-hgb-f3-n10`, prezisi neutri pe `r`, ies la -0.0387 si -0.0195.** Asta era pariul meu numarul UNU al sesiunii, argumentat pe faptul ca `extratrees` isi ia valoarea din `max_features=0.3`. Greseala de raționament: la ExtraTrees subesantionarea de coloane se face LA FIECARE TAIETURA, deci fiecare arbore vede in cele din urma toate coloanele; la un subspatiu fix per membru, membrul nu mai vede niciodata coloanele lipsa. Nu e acelasi mecanism, desi are acelasi nume.

3. **`tt-rank-ridge` prezis neutru, iese la -0.0480, in timp ce `ttz-rank-ridge` (fara inversa) iese la -0.0058.** Deci nu transformarea tintei strica, ci INVERSA: maparea inapoi prin functia de cuantile empirica. Nu prevazusem ca cele doua variante ale aceluiasi invelis vor diferi cu 0.0422.

4. **`rf-n300` si `lgbmlin-l8` au `rho` fata de `ridge` mult sub ce prezisesem** (0.827 fata de 0.86-0.89, si 0.824 fata de 0.90-0.94). Pe `lgbmlin-l8` argumentul meu era ca un hibrid liniar-arbore sta INTRE cei doi membri si deci se coreleaza cu amandoi; masurat, el are 1-rho(X,hgb) = 0.124, adica e cel mai decorelat de HGB dintre toti arborii. Foile liniare nu il apropie de `ridge`, il indepartează de `hgb`.

5. **Cei trei pe care i-am numit cei mai promitatori au ieșit 1 din 3.** `rs-hgb-f3-n10` (locul 1) a picat cel mai rau din sesiune, `ord-lin-k5` (locul 2) a ieșit exact zero, `rf-n300` (locul 3) a ieșit al patrulea din tabel la +0.0076. **Iar castigatorul, `orde-hgb-k5`, nu era in tabelul meu de predictii.** Exista in lista de nume implementate, ca varianta a lui `ord-*` citita in unitati de complexitate, dar nu i-am scris nicio predictie, deci nu-mi pot revendica nimic pentru el. Diferenta dintre cele doua citiri, +0.0081 pe `r`, e ea insasi un lucru pe care nu il anticipasem: spatierea neliniara a mediilor de clasa conteaza.

### Ce am prezis corect, si merita spus fiindca a fost prezis din mecanism

1. **Pierderea e mai puternica la arbori decat la liniari.** Prezis `1 - rho(hgb-abs, hgb) > 0.020`; masurat 0.050, deci de 2.5 ori.

2. **`cat-d3` are `rho` fata de `ridge` PESTE reperul de 0.811**, 0.820, adica arborii oblivious de adancime mica se apropie de un model aditiv neted si deci de `ridge`. Scrisesem explicit ca o valoare SUB 0.811 m-ar contrazice; nu s-a intamplat.

3. **`hgb-q50` e un duplicat al lui `hgb-abs`.** Prezisesem `la 0.01`; masurat, sunt identice bit cu bit (max|diff| exact 0 pe date sintetice si aceleasi cifre pe date reale). Motivul: valorile din foi se calculeaza prin mediana ponderata la ambele pierderi, iar factorul 2 din gradient nu schimba argmaxul castigului de taietura.

4. **Niciun candidat nu trece bara.** Prezisesem ca cel mai bun `delta` ca al treilea membru va fi intre +0.004 si +0.009; masurat pe cele trei encodere, cel mai bun e +0.0080.

5. **Raspunsul agregat la intrebarea de research e NU**, cu diferenta obiectiv minus familie +0.0026, in banda de ±0.010 pe care o scrisesem. Dar am avut dreptate pe statistica pe care am numit-o si greșit pe fond: nu prevazusem ca cele trei clase se despica atat de tare intre ele.

## Ce se inchide, ce rămâne deschis

```
  INCHIS  familia de functii: al doilea punct pe aceeasi tendinta, acum cu lgbm, catboost,
          randomforest, foi liniare, MLP si kNN masurate. Nimic nu trece bara.
  INCHIS  pierderea: slack sub FAMILIE pe trei encodere, si strica exact limba critica.
  INCHIS  functionalul tintei: rang si logit, cu si fara inversa, toate negative.
  INCHIS  informatia prin subspatii fixe si prin ponderare pe coada.
  VIU     incadrarea ordinala: singura clasa cu slack pozitiv, +0.0083 pe A pe 3/3
          encodere si pozitiva 3/3 pe AMBELE brate, dar +0.0002 in fuziune.
```

Recomandarea, si iese din cifra de +0.917: nu mai are sens o sesiune care urca `r_A` fara sa se uite la `rho(A,B)` pe limba. Singurul loc unde un castig pe A a plătit efectiv in fuziune in toata sesiunea e sinhaleza, unde `rho(A,B)` e 0.387. Deci o sesiune viitoare pe A ar trebui sa fie o sesiune despre SINHALEZA si FILIPINEZA, nu despre algoritmi: acolo `rho(A,B)` e mic, acolo lipsesc `wordfreq` si lematizatorul, si acolo aritmetica permite ca un castig sa ajunga in fuziune.

## Controale

```
  md5 pe cele 4 fisiere adoptate     identice cu output/_rezerva_reg/MD5.txt
  --regressor blend                  70c74c22218b7525d8e1d3d11b663f67
  make_a_blend --control             1.11e-16 pe p_en si p_multi
  identitatea de frontiera pe limba  2.22e-16
  tt-id-ridge                        0.00e+00
  rs-ridge-f10-n1                    4.27e-05
```

Cele doua controale de invelis nu spun acelasi lucru, si diferenta dintre ele e utila. `tt-id-ridge` iese la EXACT zero: un invelis care atinge numai `y` nu poate schimba nimic. `rs-ridge-f10-n1` iese la 4.3e-05, NU bit-exact, si cauza e masurata: selectia de coloane cu `X[:, c]` produce o copie cu alt aranjament in memorie, deci BLAS insumeaza in alta ordine. Pe date sintetice gaussiene aceeasi operatie da 8.9e-16 in float64 si 3.9e-07 in float32; pe 774 de coloane de embedding puternic colineare, cu Ridge la alpha=300, iese 1e-5. Diferenta e uniforma pe toate randurile si toate limbile, e cu doua ordine de marime sub cel mai mic efect interpretat in sesiune (0.0002), si `r` cu `rho` ies identice la toate zecimalele raportate. Prima formulare a controlului spunea `bit-exact` si era falsa; docstringul din `solution_bert.py` a fost corectat cu cele trei cifre de mai sus.

