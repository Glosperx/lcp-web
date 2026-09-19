# Axa LINIARA a semnalului A, pe toate encoderele

Generat de `analysis_regresor_multi.py`. Coloana `p_multi`, splitul test, configuratia `--lemma-freq --afeat fert_inloc`. Bratul B nu intra nicaieri.

Jumatatea liniara a blend-ului a fost `Ridge(alpha=300)` in absolut toate variantele masurate vreodata pe axa regresorului; tot ce s-a schimbat pana acum a fost jumatatea de arbori. Aici se schimba liniarul, cu ACELASI partener `hgb` si pe ACELASI encoder.

Controlul, per encoder, e `ridge+hgb` ca medie standardizata:

```
  xlmr   0.575296   (10 limbi)
  e5     0.571931   (10 limbi)
  labse  0.574504   (10 limbi)
```

Bara pe fuziune e +0.0045 si factorul de transmisie A -> fuziune e 0.259 mediu, deci un candidat trebuie sa urce A cu +0.0174 ca sa fie chiar si optimist adoptabil.

## delta pe A fata de `ridge+hgb`, per encoder

`sus` e pe cate encodere din `n` diferenta e pozitiva. Trei din trei la +0.002 e un efect; unu din trei la +0.006 e o loterie cu trei bilete.

`delta` e cel mai bun dintre CELE TREI ROLURI in care poate intra candidatul: in locul jumatatii liniare, in locul jumatatii de arbori, sau ca al treilea membru. Rolul ales e in coloana `rol` (`lin`, `arb`, `tri`), si e majoritar peste encodere. Un arbore judecat numai in rol de liniar iese cel mai prost din tabel chiar cand e cel mai bun al treilea membru; pe `extratrees` diferenta intre roluri e 0.017.

```
  candidat         clasa        rol       xlmr        e5     labse     medie   sus
  extratrees       FAMILIE      arb    +0.0065   +0.0093   +0.0116   +0.0091   3/3
  cat-d3           FAMILIE      arb    +0.0054   +0.0102   +0.0109   +0.0088   3/3
  orde-hgb-k5      INCADRARE    arb    +0.0086   +0.0068   +0.0095   +0.0083   3/3
  rf-n300          FAMILIE      arb    +0.0075   +0.0074   +0.0080   +0.0076   3/3
  lasso-a3e-3      REGULARIZARE tri    +0.0049   +0.0075   +0.0081   +0.0068   3/3
  lasso-a1e-3      REGULARIZARE tri    +0.0034   +0.0074   +0.0082   +0.0063   3/3
  elasticnet       REGULARIZARE tri    +0.0053   +0.0055   +0.0078   +0.0062   3/3
  lgbmlin-l8       FAMILIE      arb    +0.0058   +0.0088   +0.0033   +0.0060   3/3
  ord-hgb-k5       INCADRARE    arb    +0.0058   +0.0052   +0.0058   +0.0056   3/3
  lasso            REGULARIZARE tri    +0.0047   +0.0014   +0.0072   +0.0044   3/3
  lgbm-l8          FAMILIE      arb    +0.0009   +0.0047   +0.0041   +0.0032   3/3
  lasso-a3e-4      REGULARIZARE tri    +0.0006   +0.0035   +0.0054   +0.0032   3/3
  clf-hgb-k5       INCADRARE    arb    +0.0030         -         -   +0.0030   1/1
  ord-hgb-k10      INCADRARE    arb    +0.0027         -         -   +0.0027   1/1
  orde-lin-k5      INCADRARE    tri    +0.0019   +0.0023   +0.0029   +0.0024   3/3
  ard              REGULARIZARE tri    -0.0007   +0.0041   +0.0031   +0.0021   2/3
  ridge-a1000      REGULARIZARE tri    +0.0001   +0.0014   +0.0033   +0.0016   3/3
  ridge-a3000      REGULARIZARE tri    -0.0012   +0.0020   +0.0041   +0.0016   2/3
  bayesridge       REGULARIZARE tri    -0.0001   +0.0012   +0.0028   +0.0013   2/3
  krr-rbf          FAMILIE      tri    +0.0015   +0.0028   -0.0009   +0.0011   2/3
  lasso-a1e-4      REGULARIZARE tri    -0.0002   +0.0006   +0.0024   +0.0009   2/3
  tt-logit2-ridge  TINTA        tri    -0.0004   +0.0008   +0.0020   +0.0008   2/3
  pls-k16          FAMILIE      tri    +0.0003   +0.0001   +0.0016   +0.0007   3/3
  ridge-a10000     REGULARIZARE tri    -0.0025   +0.0014   +0.0032   +0.0007   2/3
  huber            LOSS         tri    -0.0016   +0.0004   +0.0020   +0.0003   2/3
  clf-lin-k5       INCADRARE    tri    +0.0000         -         -   +0.0000   1/1
  ord-lin-k5       INCADRARE    tri    +0.0000         -         -   +0.0000   1/1
  ridge-a100       REGULARIZARE tri    -0.0005   -0.0003   +0.0009   +0.0000   1/3
  rs-ridge-f10-n1  CONTROL      lin    +0.0000         -         -   +0.0000   1/1
  tt-id-ridge      CONTROL      lin    +0.0000         -         -   +0.0000   0/1
  ridge            REGULARIZARE tri    +0.0000   +0.0000   +0.0000   +0.0000   <- controlul
  pls-k8           FAMILIE      tri    -0.0025   -0.0010   +0.0028   -0.0002   1/3
  ridge-a30        REGULARIZARE tri    -0.0009   -0.0007   +0.0005   -0.0003   1/3
  pls-k64          FAMILIE      tri    -0.0011   -0.0008   +0.0003   -0.0005   1/3
  pls-k32          FAMILIE      tri    -0.0010   -0.0008   -0.0002   -0.0007   0/3
  ord-lin-k10      INCADRARE    tri    -0.0009         -         -   -0.0009   0/1
  hgb-abs          LOSS         arb    -0.0017   -0.0026   +0.0012   -0.0010   1/3
  tt-logit005-ridge TINTA        lin    -0.0011         -         -   -0.0011   0/1
  svr-lin          LOSS         tri    -0.0038   +0.0007   -0.0004   -0.0011   1/3
  ridge-a30000     REGULARIZARE tri    -0.0045   -0.0004   +0.0013   -0.0012   1/3
  w-ridge-c1       INFORMATIE   lin    -0.0016         -         -   -0.0016   0/1
  ttz-rank-ridge   TINTA        lin    -0.0016         -         -   -0.0016   0/1
  hgb-q50          LOSS         arb    -0.0017         -         -   -0.0017   0/1
  rs-hgb-f3-n10    INFORMATIE   tri    -0.0017         -         -   -0.0017   0/1
  w-hgb-c1         INFORMATIE   arb    -0.0022         -         -   -0.0022   0/1
  tt-rank-hgb      TINTA        arb    -0.0024         -         -   -0.0024   0/1
  pls-k4           FAMILIE      tri    -0.0063   -0.0010   -0.0011   -0.0028   0/3
  tt-logit2-hgb    TINTA        arb    -0.0051         -         -   -0.0051   0/1
  lasso-a3e-2      REGULARIZARE tri    -0.0082   -0.0060   -0.0021   -0.0054   0/3
  ttz-rank-hgb     TINTA        arb    -0.0055         -         -   -0.0055   0/1
  rs-ridge-f3-n10  INFORMATIE   tri    -0.0062         -         -   -0.0062   0/1
  hgb-adanc        FAMILIE      tri    -0.0062         -         -   -0.0062   0/1
  mlp-h128         FAMILIE      tri    -0.0065         -         -   -0.0065   0/1
  tt-rank-ridge    TINTA        tri    -0.0080         -         -   -0.0080   0/1
  knn-k50          FAMILIE      tri    -0.0288         -         -   -0.0288   0/1
```

## Clasa de mecanism: intrebarea de research

`slack` e cat rho i-ar fi fost PERMIS candidatului ca sa lege la egalitate cu controlul, la r-ul lui, minus cat rho are. Pozitiv inseamna sub curba de compromis. Iese direct din identitatea de frontiera, deci nu are niciun parametru potrivit, si e formulat in exact unitatile in care e pusa intrebarea: rho, la r comparabil.

`REGULARIZARE` e norul de referinta: pierdere patratica, liniar dens, numai penalizarea variaza.

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

Raspunsul direct: clasele care schimba OBIECTIVUL (`LOSS`, `TINTA`, `INCADRARE`, n=19) au slack mediu **-0.0019**; clasa `FAMILIE` (n=14) **-0.0046**; norul de referinta `REGULARIZARE` (n=15) **+0.0139**. Diferenta obiectiv minus familie e **+0.0026**, iar imprastierea in interiorul norului de referinta e de la -0.0088 la +0.0441.

Candidatii pozitivi pe TOATE encoderele pe care s-au rulat:

```
  extratrees       medie +0.0091   fuziune implicata +0.0024 (optimist)
  cat-d3           medie +0.0088   fuziune implicata +0.0023 (optimist)
  orde-hgb-k5      medie +0.0083   fuziune implicata +0.0022 (optimist)
  rf-n300          medie +0.0076   fuziune implicata +0.0020 (optimist)
  lasso-a3e-3      medie +0.0068   fuziune implicata +0.0018 (optimist)
  lasso-a1e-3      medie +0.0063   fuziune implicata +0.0016 (optimist)
  elasticnet       medie +0.0062   fuziune implicata +0.0016 (optimist)
  lgbmlin-l8       medie +0.0060   fuziune implicata +0.0015 (optimist)
  ord-hgb-k5       medie +0.0056   fuziune implicata +0.0014 (optimist)
  lasso            medie +0.0044   fuziune implicata +0.0012 (optimist)
  lgbm-l8          medie +0.0032   fuziune implicata +0.0008 (optimist)
  lasso-a3e-4      medie +0.0032   fuziune implicata +0.0008 (optimist)
  clf-hgb-k5       medie +0.0030   fuziune implicata +0.0008 (optimist)
  ord-hgb-k10      medie +0.0027   fuziune implicata +0.0007 (optimist)
  orde-lin-k5      medie +0.0024   fuziune implicata +0.0006 (optimist)
  ridge-a1000      medie +0.0016   fuziune implicata +0.0004 (optimist)
  pls-k16          medie +0.0007   fuziune implicata +0.0002 (optimist)
  clf-lin-k5       medie +0.0000   fuziune implicata +0.0000 (optimist)
  ord-lin-k5       medie +0.0000   fuziune implicata +0.0000 (optimist)
  rs-ridge-f10-n1  medie +0.0000   fuziune implicata +0.0000 (optimist)
```

Bara e +0.0045 pe fuziune. Cei care o trec chiar si pe estimarea optimista: **niciunul**.

## rho fata de AMBII membri, per encoder

Conteaza amandoua, si care anume depinde de rol: `rho(X, hgb)` decide daca X poate lua locul jumatatii LINIARE, `rho(X, ridge)` daca poate lua locul celei de ARBORI, si amandoua daca intra ca al treilea. Reperul e `rho(ridge, hgb)`, adica exact cat de decorelati sunt cei doi membri de acum.

```
  candidat         clasa          xlmr ri     e5 ri  labse ri   xlmr hgb     e5 hgb  labse hgb
  ridge            REGULARIZARE     1.000     1.000     1.000      0.811      0.799      0.770   <- reperul, rho(ridge,hgb) e coloana hgb
  ard              REGULARIZARE     0.812     0.793     0.835      0.787      0.776      0.775
  bayesridge       REGULARIZARE     0.997     0.996     0.997      0.822      0.804      0.776
  cat-d3           FAMILIE          0.820     0.814     0.798      0.965      0.945      0.948
  clf-hgb-k5       INCADRARE        0.826         -         -      0.930          -          -
  clf-lin-k5       INCADRARE        0.887         -         -      0.724          -          -
  elasticnet       REGULARIZARE     0.890     0.877     0.879      0.870      0.852      0.823
  extratrees       FAMILIE          0.858     0.837     0.837      0.914      0.884      0.866
  hgb-abs          LOSS             0.787     0.772     0.750      0.950      0.942      0.941
  hgb-adanc        FAMILIE          0.800         -         -      0.951          -          -
  hgb-q50          LOSS             0.787         -         -      0.950          -          -
  huber            LOSS             0.980     0.983     0.981      0.801      0.797      0.760
  knn-k50          FAMILIE          0.518         -         -      0.501          -          -
  krr-rbf          FAMILIE          0.880     0.892     0.902      0.771      0.748      0.726
  lasso            REGULARIZARE     0.863     0.838     0.852      0.855      0.824      0.815
  lasso-a1e-3      REGULARIZARE     0.959     0.957     0.958      0.858      0.846      0.814
  lasso-a1e-4      REGULARIZARE     0.998     0.998     0.998      0.813      0.805      0.774
  lasso-a3e-2      REGULARIZARE     0.757     0.802     0.799      0.739      0.783      0.778
  lasso-a3e-3      REGULARIZARE     0.909     0.907     0.908      0.871      0.857      0.827
  lasso-a3e-4      REGULARIZARE     0.992     0.991     0.989      0.831      0.823      0.791
  lgbm-l8          FAMILIE          0.821     0.819     0.794      0.977      0.969      0.968
  lgbmlin-l8       FAMILIE          0.824     0.813     0.792      0.876      0.862      0.851
  mlp-h128         FAMILIE          0.791         -         -      0.673          -          -
  ord-hgb-k10      INCADRARE        0.825         -         -      0.951          -          -
  ord-hgb-k5       INCADRARE        0.819     0.817     0.816      0.945      0.932      0.916
  ord-lin-k10      INCADRARE        0.940         -         -      0.760          -          -
  ord-lin-k5       INCADRARE        0.929         -         -      0.755          -          -
  orde-hgb-k5      INCADRARE        0.828     0.825     0.819      0.946      0.934      0.919
  orde-lin-k5      INCADRARE        0.926     0.935     0.936      0.747      0.768      0.725
  pls-k16          FAMILIE          0.996     0.997     0.996      0.804      0.793      0.767
  pls-k32          FAMILIE          0.998     0.998     0.996      0.799      0.793      0.758
  pls-k4           FAMILIE          0.901     0.878     0.898      0.803      0.745      0.731
  pls-k64          FAMILIE          0.998     0.998     0.996      0.799      0.793      0.758
  pls-k8           FAMILIE          0.969     0.961     0.960      0.799      0.775      0.755
  rf-n300          FAMILIE          0.827     0.802     0.793      0.918      0.897      0.873
  ridge-a100       REGULARIZARE     0.999     0.999     0.999      0.804      0.796      0.764
  ridge-a1000      REGULARIZARE     0.996     0.995     0.995      0.822      0.803      0.777
  ridge-a10000     REGULARIZARE     0.930     0.924     0.930      0.829      0.782      0.759
  ridge-a30        REGULARIZARE     0.998     0.998     0.997      0.800      0.794      0.760
  ridge-a3000      REGULARIZARE     0.976     0.973     0.974      0.830      0.799      0.774
  ridge-a30000     REGULARIZARE     0.877     0.872     0.881      0.815      0.759      0.736
  rs-hgb-f3-n10    INFORMATIE       0.827         -         -      0.853          -          -
  rs-ridge-f10-n1  CONTROL          1.000         -         -      0.811          -          -
  rs-ridge-f3-n10  INFORMATIE       0.866         -         -      0.801          -          -
  svr-lin          LOSS             0.960     0.960     0.960      0.793      0.783      0.747
  tt-id-ridge      CONTROL          1.000         -         -      0.811          -          -
  tt-logit005-ridge TINTA            0.984         -         -      0.794          -          -
  tt-logit2-hgb    TINTA            0.794         -         -      0.967          -          -
  tt-logit2-ridge  TINTA            0.986     0.987     0.987      0.796      0.784      0.752
  tt-rank-hgb      TINTA            0.784         -         -      0.963          -          -
  tt-rank-ridge    TINTA            0.921         -         -      0.729          -          -
  ttz-rank-hgb     TINTA            0.780         -         -      0.960          -          -
  ttz-rank-ridge   TINTA            0.984         -         -      0.801          -          -
  w-hgb-c1         INFORMATIE       0.802         -         -      0.971          -          -
  w-ridge-c1       INFORMATIE       0.992         -         -      0.799          -          -
```

`rho(ridge, hgb)` e 0.811, 0.799, 0.770 pe cele 3 encodere. Candidati cu rho STRICT mai mic pe toate: `huber`, `krr-rbf`, `orde-lin-k5`, `pls-k16`, `pls-k32`, `pls-k4`, `pls-k64`, `pls-k8`, `ridge-a100`, `ridge-a30`, `svr-lin`, `tt-logit2-ridge`.

## Grilele parametrice, punctul cel mai bun pe fiecare encoder

Aici e doar cine iese in fata pe fiecare encoder, ca sa se vada daca optimul e STABIL. Selectia onesta, leave-one-language-out, plus latimea criteriului, e in rapoartele per encoder (`e_regresor_a.md`, `e_regresor_a_e5.md`, `e_regresor_a_labse.md`).

```
  ridge (alpha)
    xlmr   cel mai bun `ridge-a1000` la +0.0001   ridge-a30=-0.0009 ridge-a100=-0.0005 ridge=+0.0000 ridge-a1000=+0.0001 ridge-a3000=-0.0012 ridge-a10000=-0.0025 ridge-a30000=-0.0045
    e5     cel mai bun `ridge-a3000` la +0.0020   ridge-a30=-0.0007 ridge-a100=-0.0003 ridge=+0.0000 ridge-a1000=+0.0014 ridge-a3000=+0.0020 ridge-a10000=+0.0014 ridge-a30000=-0.0004
    labse  cel mai bun `ridge-a3000` la +0.0041   ridge-a30=+0.0005 ridge-a100=+0.0009 ridge=+0.0000 ridge-a1000=+0.0033 ridge-a3000=+0.0041 ridge-a10000=+0.0032 ridge-a30000=+0.0013
  lasso (alpha)
    xlmr   cel mai bun `lasso-a3e-3` la +0.0049   lasso-a1e-4=-0.0002 lasso-a3e-4=+0.0006 lasso-a1e-3=+0.0034 lasso-a3e-3=+0.0049 lasso=+0.0047 lasso-a3e-2=-0.0082
    e5     cel mai bun `lasso-a3e-3` la +0.0075   lasso-a1e-4=+0.0006 lasso-a3e-4=+0.0035 lasso-a1e-3=+0.0074 lasso-a3e-3=+0.0075 lasso=+0.0014 lasso-a3e-2=-0.0060
    labse  cel mai bun `lasso-a1e-3` la +0.0082   lasso-a1e-4=+0.0024 lasso-a3e-4=+0.0054 lasso-a1e-3=+0.0082 lasso-a3e-3=+0.0081 lasso=+0.0072 lasso-a3e-2=-0.0021
  pls (k)
    xlmr   cel mai bun `pls-k16` la +0.0003   pls-k4=-0.0063 pls-k8=-0.0025 pls-k16=+0.0003 pls-k32=-0.0010 pls-k64=-0.0011
    e5     cel mai bun `pls-k16` la +0.0001   pls-k4=-0.0010 pls-k8=-0.0010 pls-k16=+0.0001 pls-k32=-0.0008 pls-k64=-0.0008
    labse  cel mai bun `pls-k8` la +0.0028   pls-k4=-0.0011 pls-k8=+0.0028 pls-k16=+0.0016 pls-k32=-0.0002 pls-k64=+0.0003
```

## Cele doua brate ale lui A sunt INDEPENDENTE

Tot ce e mai sus e pe `p_multi`. Dar semnalul A al sistemului nu e `p_multi`, e `z(w_src . z(p_en) + (1 - w_src) . z(p_multi))`, cu `w_src` ales LOLO. Deci un candidat trebuie sa tina pe AMBELE coloane. Cati tin se CALCULEAZA mai jos si nu se afirma aici: propozitia care spunea `si aici nu tine niciunul` era corecta pe axa liniara din 26 august si a devenit FALSA cand s-au adaugat inlocuitorii jumatatii de arbori, fara sa crape nimic. Exact tiparul `constante-hardcodate-mint-dupa-renumerotare`.

`p_en` e o SINGURA potrivire care prezice zece limbi nevazute; `p_multi` e o potrivire per limba, cu noua limbi de test in antrenare. Doua regimuri diferite, deci nu e de la sine inteles ca vor acelasi regresor, si masuratoarea de mai jos spune ca intr-adevar nu se informeaza reciproc.

```
  candidat            p_multi   sus         p_en   sus
  extratrees          +0.0091   3/3      +0.0064   3/3
  cat-d3              +0.0088   3/3      +0.0028   3/3
  orde-hgb-k5         +0.0083   3/3      +0.0064   3/3
  rf-n300             +0.0076   3/3      +0.0030   3/3
  lasso-a3e-3         +0.0068   3/3      +0.0003   2/3
  lasso-a1e-3         +0.0063   3/3      -0.0010   0/3
  elasticnet          +0.0062   3/3      -0.0004   1/3
  lgbmlin-l8          +0.0060   3/3      -0.0014   1/3
  ord-hgb-k5          +0.0056   3/3      +0.0049   3/3
  lasso               +0.0044   3/3      -0.0024   0/3
  lgbm-l8             +0.0032   3/3      -0.0000   2/3
  lasso-a3e-4         +0.0032   3/3      -0.0006   1/3
  clf-hgb-k5          +0.0030   1/1      +0.0057   1/1
  ord-hgb-k10         +0.0027   1/1      +0.0060   1/1
  orde-lin-k5         +0.0024   3/3      -0.0002   2/3
  ard                 +0.0021   2/3      -0.0023   0/3
  ridge-a1000         +0.0016   3/3      +0.0035   3/3
  ridge-a3000         +0.0016   2/3      +0.0045   3/3
  bayesridge          +0.0013   2/3      +0.0026   3/3
  krr-rbf             +0.0011   2/3      +0.0046   3/3
  lasso-a1e-4         +0.0009   2/3      -0.0024   0/3
  tt-logit2-ridge     +0.0008   2/3      -0.0013   0/3
  pls-k16             +0.0007   3/3      -0.0021   1/3
  ridge-a10000        +0.0007   2/3      +0.0024   3/3
  huber               +0.0003   2/3      -0.0069   0/3
  clf-lin-k5          +0.0000   1/1      -0.0070   0/1
  ord-lin-k5          +0.0000   1/1      -0.0060   0/1
  ridge-a100          +0.0000   1/3      -0.0027   0/3
  rs-ridge-f10-n1     +0.0000   1/1      +0.0000   1/1
  tt-id-ridge         +0.0000   0/1      +0.0000   0/1
  ridge               +0.0000   0/3      +0.0000   0/3   <- controlul
  pls-k8              -0.0002   1/3      +0.0007   1/3
  ridge-a30           -0.0003   1/3      -0.0043   0/3
  pls-k64             -0.0005   1/3      -0.0051   0/3
  pls-k32             -0.0007   0/3      -0.0052   0/3
  ord-lin-k10         -0.0009   0/1      -0.0002   0/1
  hgb-abs             -0.0010   1/3      +0.0027   2/3
  tt-logit005-ridge    -0.0011   0/1      -0.0027   0/1
  svr-lin             -0.0011   1/3      -0.0114   0/3
  ridge-a30000        -0.0012   1/3      +0.0015   3/3
  w-ridge-c1          -0.0016   0/1      -0.0011   0/1
  ttz-rank-ridge      -0.0016   0/1      +0.0001   1/1
  hgb-q50             -0.0017   0/1      +0.0055   1/1
  rs-hgb-f3-n10       -0.0017   0/1      +0.0026   1/1
  w-hgb-c1            -0.0022   0/1      -0.0002   0/1
  tt-rank-hgb         -0.0024   0/1      +0.0040   1/1
  pls-k4              -0.0028   0/3      -0.0006   1/3
  tt-logit2-hgb       -0.0051   0/1      +0.0022   1/1
  lasso-a3e-2         -0.0054   0/3      +0.0004   3/3
  ttz-rank-hgb        -0.0055   0/1      +0.0037   1/1
  rs-ridge-f3-n10     -0.0062   0/1      -0.0016   0/1
  hgb-adanc           -0.0062   0/1      +0.0026   1/1
  mlp-h128            -0.0065   0/1      -0.0157   0/1
  tt-rank-ridge       -0.0080   0/1      -0.0133   0/1
  knn-k50             -0.0288   0/1      -0.0112   0/1
```

Corelatia intre cele doua coloane de delta, peste 55 candidati: **+0.476**. Dar cifra asta e inselatoare: candidatii catastrofali sunt prosti pe AMBELE brate si fabrica singuri o corelatie pozitiva care spune numai `prost e prost peste tot`. Restransa la banda in care s-ar putea alege ceva:

```
  |delta| <= 0.010   n=51   pearson +0.201
  |delta| <= 0.005   n=29   pearson -0.103
```

Adica in banda utila cele doua brate sunt in mare masura **independente**: cat ajuta un candidat pe un brat nu spune mult despre celalalt. Exemplul canonic, de pe axa liniara, e `lasso-a1e-3`, cel mai bun pe `p_multi` si negativ pe `p_en`. Cifrele concrete se citesc din tabelul de deasupra, nu de aici: cand s-au adaugat rulari noi, o pereche de cifre scrisa in propozitie a incetat sa mai fie perechea extrema si propozitia a devenit inselatoare fara sa crape nimic.

Pozitivi pe 3/3 encodere pe AMBELE brate: `cat-d3`, `clf-hgb-k5`, `extratrees`, `ord-hgb-k10`, `ord-hgb-k5`, `orde-hgb-k5`, `rf-n300`, `ridge-a1000`.

Consecinta practica, si e parghia pe care nicio configuratie de pana acum n-o foloseste: `p_en` si `p_multi` sunt COLOANE separate in CSV, deci alpha se poate alege pe brat, nu pe model. Asta se masoara mai jos ca `lin_A7` si `lin_A8`.

## Fuziunea REALA cu semnalul B, pentru ansamblurile de top

`--arm lolo --fit test --pick-split test`, acelasi B (M3K) peste tot, numai A variaza. Diferenta e PEREACHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste control.

```
  ce                                       spatiu      control     nou    delta   P(>0)
  mean(lasso-a1e-3, hgb)                   xlmr         0.6828  0.6834  +0.0006   60.6%
  mean(hgb, extratrees, pls-k16)           xlmr         0.6828  0.6839  +0.0011   68.5%
  mean(lasso-a1e-3, lasso-a3e-4, hgb)      xlmr         0.6828  0.6828  +0.0000   51.3%
  mean(lasso-a1e-3, hgb, tabfm@256)        hibrid       0.6827  0.6830  +0.0003   58.1%
  encmean(mean(lasso-a1e-3, hgb)) + ens    3 encodere   0.6900  0.6887  -0.0013   28.0%
  encmean(mean(ridge-a1000, hgb)) + ens    3 encodere   0.6900  0.6896  -0.0004   53.8%
  p_en de la ridge-a3000, p_multi neatins  3 encodere   0.6900  0.6900  -0.0000   60.7%
  p_en ridge-a3000 + p_multi lasso-a1e-3   3 encodere   0.6900  0.6904  +0.0004   67.2%
  mean(ridge, orde-hgb-k5)                 xlmr         0.6828  0.6834  +0.0007   47.3%
  mean(ridge, hgb, orde-hgb-k5)            xlmr         0.6828  0.6839  +0.0011   69.6%
  mean(rf-n300, orde-lin-k5, orde-hgb-k5) [ales pe test] xlmr         0.6828  0.6848  +0.0020   61.7%
  encmean(mean(ridge, hgb, orde-hgb-k5)) + ens 3 encodere   0.6900  0.6902  +0.0002   58.1%
  encmean(mean(ridge, orde-hgb-k5)) + ens  3 encodere   0.6900  0.6895  -0.0005   42.0%
  encmean(mean(ridge, hgb, rf-n300)) + ens 3 encodere   0.6900  0.6895  -0.0005   40.0%
  encmean(mean(ridge, cat-d3)) + ens       3 encodere   0.6900  0.6896  -0.0004   36.1%
  encmean(mean(ridge, hgb, cat-d3)) + ens  3 encodere   0.6900  0.6901  +0.0001   52.8%
  encmean(mean(ridge, extratrees)) + ens   3 encodere   0.6900  0.6881  -0.0019   30.2%
  encmean(mean(ridge, hgb, extratrees)) + ens 3 encodere   0.6900  0.6893  -0.0007   42.2%
```

Bara pe fuziune e +0.0045. **Niciuna nu o trece.** Cea mai mare diferenta e +0.0020 (`mean(rf-n300, orde-lin-k5, orde-hgb-k5) [ales pe test]`), la P(>0) 61.7%, adica o moneda.

Pe drumul care conteaza pentru sistem, media a trei encodere cu `--ens`, 3 din 11 configuratii ies peste controlul adoptat, si cea mai buna dintre ele e +0.0004 la P(>0) 67.2%. Nicio adoptare nu se sprijina pe asta.

Cifra care duce concluzia nu e nici una din diferentele de fuziune, e raportul dintre ele si castigul pe A. Reperul, masurat pe axa LINIARA in sesiunea din 26 august si citabil din `e_regresor_liniar.md`: A a urcat de la 0.5993 la 0.6023, adica +0.0030 constant si reproductibil pe toate trei encoderele, si fuziunea nu s-a miscat, deci transmisia pe acea axa a ieșit **~zero** fata de 0.09-0.26 masurat in general. Cele doua cifre 0.5993 si 0.6023 sunt ale acelei sesiuni si NU se recalculeaza aici; sunt scrise ca reper istoric, nu ca rezultat al tabelului de mai sus. Raportul de transmisie al sesiunii CURENTE se citeste din coloanele `delta` de mai sus impartite la delta pe A al configuratiei corespunzatoare.

