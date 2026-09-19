# Semnalul C prin frontiera, ca poarta

**Excluse ca degenerate pe text brut, prin `analysis_c_sanatate.py`: ['gemma4-12b-4bit'].**
Generat de `analysis_c_frontiera.py`, directoare ['bakeoff_test_Text', 'surprisal_test']. Splitul e test, n = 5624. Fuziunea de referinta e `fusion_preds_lolo_adoptat_temp.csv`, r mediu pe limbi **0.683849**.

## Poarta, scrisa inainte de a citi vreo cifra a candidatilor

Bara e +0.0045. Din `R_max^2 = r_F^2 + partial^2 * (1 - r_F^2)`, conditia `R_max >= r_F + bara` cere, la r_F = 0.683849:

> **|corelatia partiala a lui C cu y, controland pe fuziune| >= 0.1077**

Echivalent, ce r_C ii trebuie unui candidat in functie de cat de corelat e cu fuziunea. Ramura de jos e cea de SUPRESOR: un semnal care coreleaza cu fuziunea dar NU cu eticheta corecteaza scazandu-se.

```
rho cu fuziunea   r_C minim (normala)   r_C maxim (supresor)
0.00              +0.0786               -0.0786
0.05              +0.1127               -0.0443
0.10              +0.1466               -0.0098
0.15              +0.1803               +0.0249
0.20              +0.2138               +0.0598
0.30              +0.2801               +0.1302
0.40              +0.3456               +0.2015
0.50              +0.4100               +0.2739
```

Praguri pentru alte ambitii, ca sa nu se citeasca doar bara:

```
castig tinta   |partial| necesar
+0.0022         0.0752
+0.0045         0.1077
+0.0089         0.1517
```

## Candidati, fiecare cu tabelul lui pe limba

### `llama31-8b-4bit`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0741  0.1136  0.0534  0.0834  0.5566   0.0334  0.0854  0.5573  0.0007  0.050
de    570          0  0.1959  0.0909  0.0266  0.0539  0.7468   0.2343  0.1235  0.7629  0.0161  0.175
en    570          0 -0.0489 -0.0894 -0.0512 -0.0670  0.8700   0.0190  0.1797  0.8701  0.0001  0.010
es    593          0  0.0433  0.0445  0.0297  0.0363  0.7641   0.0240  0.1287  0.7642  0.0002  0.020
fil   570          2 -0.0096  0.3137  0.1954  0.2622  0.5091  -0.1723  0.0788  0.5303  0.0212 -0.390
fr    569          3  0.0382  0.1049  0.0872  0.1004  0.6590  -0.0373  0.1026  0.6596  0.0006 -0.045
it    570          8  0.1123  0.1208  0.1337  0.1362  0.6750   0.0279  0.1058  0.6753  0.0003  0.030
ja    570          1 -0.0637 -0.0727 -0.1034 -0.1006  0.7877   0.0254  0.1369  0.7879  0.0002  0.020
pt    567          5  0.0666  0.0645  0.0333  0.0458  0.8450   0.0523  0.1633  0.8455  0.0005  0.030
si    600          0  0.1029  0.0239  0.1709  0.1404  0.4251   0.0482  0.0685  0.4274  0.0022  0.095
```

r_C mediu **+0.0511**, rho cu fuziunea **+0.0691**, rho cu A **+0.0715**, rho cu B **+0.0576**.
Corelatie partiala medie **+0.0255**, prag **0.1173**; trece pe **2 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.688039**, adica **+0.004190** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `qwen3-8b-4bit`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.1318  0.2169  0.1548  0.1977  0.5566   0.0268  0.0854  0.5570  0.0004  0.040
de    570          0  0.2647  0.1659  0.1156  0.1463  0.7468   0.2364  0.1235  0.7632  0.0164  0.180
en    570          0 -0.0550 -0.1078 -0.0604 -0.0798  0.8700   0.0294  0.1797  0.8702  0.0001  0.015
es    593          0  0.0735  0.0686  0.0534  0.0612  0.7641   0.0415  0.1287  0.7645  0.0005  0.035
fil   570          2  0.0446  0.3924  0.2681  0.3434  0.5091  -0.1611  0.0788  0.5276  0.0185 -0.360
fr    569          3  0.0610  0.0899  0.0970  0.1002  0.6590  -0.0067  0.1026  0.6590  0.0000 -0.010
it    570          8  0.1611  0.1734  0.1739  0.1832  0.6750   0.0516  0.1058  0.6761  0.0011  0.055
ja    570         10 -0.0064 -0.0721 -0.0068 -0.0363  0.7877   0.0361  0.1369  0.7880  0.0003  0.025
pt    567          5  0.0808  0.0726  0.0575  0.0650  0.8450   0.0484  0.1633  0.8454  0.0004  0.030
si    600          0  0.1860  0.1735  0.2605  0.2704  0.4251   0.0815  0.0685  0.4315  0.0064  0.160
```

r_C mediu **+0.0942**, rho cu fuziunea **+0.1251**, rho cu A **+0.1173**, rho cu B **+0.1114**.
Corelatie partiala medie **+0.0384**, prag **0.1173**; trece pe **3 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.688258**, adica **+0.004410** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `qwen35-9b-8bit`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0233  0.0780  0.0294  0.0520  0.5566  -0.0068  0.0854  0.5566  0.0000 -0.010
de    570          0  0.1264 -0.0039  0.0006 -0.0010  0.7468   0.1912  0.1235  0.7576  0.0107  0.145
en    570          0 -0.0481 -0.0900 -0.0700 -0.0799  0.8700   0.0435  0.1797  0.8703  0.0003  0.025
es    593          0 -0.0425 -0.1059 -0.1075 -0.1115  0.7641   0.0666  0.1287  0.7653  0.0012  0.055
fil   570          2  0.0355  0.3367  0.2334  0.2968  0.5091  -0.1406  0.0788  0.5233  0.0142 -0.300
fr    569          3 -0.0462 -0.0600 -0.0276 -0.0432  0.6590  -0.0236  0.1026  0.6592  0.0002 -0.030
it    570          8  0.0020 -0.1031 -0.0123 -0.0465  0.6750   0.0453  0.1058  0.6758  0.0008  0.045
ja    570         20 -0.1151 -0.1449 -0.1023 -0.1318  0.7877  -0.0185  0.1369  0.7878  0.0001 -0.015
pt    567          5 -0.0765 -0.1099 -0.1150 -0.1173  0.8450   0.0425  0.1633  0.8453  0.0003  0.025
si    600          0  0.1761  0.2006  0.2734  0.2914  0.4251   0.0603  0.0685  0.4286  0.0035  0.125
```

r_C mediu **+0.0035**, rho cu fuziunea **+0.0109**, rho cu A **-0.0002**, rho cu B **+0.0102**.
Corelatie partiala medie **+0.0260**, prag **0.1173**; trece pe **2 limbi din 10**, semn consistent pe **6/10**.
Plafon peste orice u, mediat pe limbi: **0.686987**, adica **+0.003138** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `medie`  (derivat din 3 membri)

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0830  0.1479  0.0860  0.1206  0.5566   0.0192  0.0854  0.5568  0.0002  0.030
de    570          0  0.2105  0.0907  0.0512  0.0714  0.7468   0.2369  0.1235  0.7633  0.0164  0.175
en    570          0 -0.0526 -0.0994 -0.0628 -0.0784  0.8700   0.0318  0.1797  0.8702  0.0001  0.020
es    593          0  0.0271  0.0026 -0.0089 -0.0051  0.7641   0.0480  0.1287  0.7647  0.0006  0.040
fil   570          6  0.0259  0.3838  0.2565  0.3321  0.5091  -0.1763  0.0788  0.5312  0.0221 -0.400
fr    569          9  0.0191  0.0486  0.0564  0.0567  0.6590  -0.0243  0.1026  0.6592  0.0003 -0.030
it    570         24  0.1001  0.0694  0.1073  0.0992  0.6750   0.0451  0.1058  0.6758  0.0008  0.045
ja    570         31 -0.0709 -0.1110 -0.0816 -0.1030  0.7877   0.0168  0.1369  0.7878  0.0001  0.015
pt    567         15  0.0259  0.0100 -0.0089 -0.0024  0.8450   0.0522  0.1633  0.8455  0.0005  0.030
si    600          0  0.1821  0.1559  0.2761  0.2750  0.4251   0.0749  0.0685  0.4305  0.0054  0.150
```

r_C mediu **+0.0550**, rho cu fuziunea **+0.0766**, rho cu A **+0.0699**, rho cu B **+0.0671**.
Corelatie partiala medie **+0.0324**, prag **0.1173**; trece pe **3 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.688504**, adica **+0.004655** peste fuziune.
**Verdict: TRECE plafonul si semnul e consistent.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `dezacord`  (derivat din 3 membri)

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0540  0.0227  0.0145  0.0195  0.5566   0.0519  0.0854  0.5582  0.0017  0.070
de    570          0 -0.0435 -0.1475 -0.0980 -0.1266  0.7468   0.0774  0.1235  0.7486  0.0018  0.065
en    570          0 -0.0513 -0.0701 -0.0185 -0.0379  0.8700  -0.0372  0.1797  0.8702  0.0002 -0.020
es    593          0 -0.1136 -0.1618 -0.1614 -0.1684  0.7641   0.0237  0.1287  0.7642  0.0002  0.020
fil   570          6 -0.0407  0.0283  0.0222  0.0266  0.5091  -0.0630  0.0788  0.5120  0.0029 -0.120
fr    569          9 -0.0767 -0.1347 -0.1148 -0.1307  0.6590   0.0126  0.1026  0.6591  0.0001  0.015
it    570         24 -0.0787 -0.2002 -0.1066 -0.1470  0.6750   0.0281  0.1058  0.6753  0.0003  0.030
ja    570         31 -0.1610 -0.2049 -0.2195 -0.2359  0.7877   0.0414  0.1369  0.7881  0.0004  0.030
pt    567         15 -0.1191 -0.1620 -0.1582 -0.1653  0.8450   0.0390  0.1633  0.8453  0.0003  0.025
si    600          0  0.0884  0.0377  0.0589  0.0605  0.4251   0.0694  0.0685  0.4298  0.0046  0.130
```

r_C mediu **-0.0542**, rho cu fuziunea **-0.0905**, rho cu A **-0.0992**, rho cu B **-0.0781**.
Corelatie partiala medie **+0.0243**, prag **0.1173**; trece pe **1 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.685083**, adica **+0.001235** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

## Sinteza, ordonata dupa plafon

```
                      r_C     rho_F   partial      prag     R_max        dR  limbi_trec  semn
candidat                                                                                     
medie            0.055025  0.076616  0.032434  0.117318  0.688504  0.004655           3     8
qwen3-8b-4bit    0.094217  0.125115  0.038398  0.117318  0.688258  0.004410           3     8
llama31-8b-4bit  0.051102  0.069106  0.025489  0.117318  0.688039  0.004190           2     8
qwen35-9b-8bit   0.003491  0.010913  0.025986  0.117318  0.686987  0.003138           2     6
dezacord        -0.054217 -0.090507  0.024333  0.117318  0.685083  0.001235           1     8
```

Bara e +0.0045. Coloana `dR` e plafonul, nu castigul: cu u optim in-sample per limba. Coloana `semn` e numarul de limbi pe care corelatia partiala are semnul majoritar; sub 8 din 10, selectia LOLO a unui u global il duce la zero indiferent ce spune media.

