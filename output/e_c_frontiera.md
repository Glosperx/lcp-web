# Semnalul C prin frontiera, ca poarta

Generat de `analysis_c_frontiera.py`, directoare ['bakeoff_test_Text']. Splitul e test, n = 5624. Fuziunea de referinta e `fusion_preds_lolo_adoptat_temp.csv`, r mediu pe limbi **0.683849**.

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

### `gemma4-12b-4bit`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0 -0.0391 -0.0987 -0.0861 -0.1014  0.5566   0.0210  0.0854  0.5569  0.0003  0.030
de    570          0 -0.1175 -0.1659 -0.1361 -0.1609  0.7468   0.0040  0.1235  0.7468  0.0000  0.005
en    570          0  0.0432  0.0653  0.0803  0.0778  0.8700  -0.0497  0.1797  0.8704  0.0003 -0.030
es    593          0 -0.0016 -0.0743 -0.0811 -0.0821  0.7641   0.0950  0.1287  0.7665  0.0025  0.075
fil   570          2 -0.1358 -0.2031 -0.1762 -0.2020  0.5091  -0.0391  0.0788  0.5102  0.0011 -0.075
fr    569          3 -0.1158 -0.1327 -0.0704 -0.1015  0.6590  -0.0654  0.1026  0.6608  0.0018 -0.080
it    570          8 -0.1122 -0.1900 -0.1406 -0.1664  0.6750   0.0002  0.1058  0.6750  0.0000  0.000
ja    570         13 -0.1410 -0.1237 -0.1064 -0.1251  0.7877  -0.0695  0.1369  0.7889  0.0012 -0.060
pt    567          5 -0.0227 -0.0475 -0.0704 -0.0646  0.8450   0.0597  0.1633  0.8456  0.0006  0.035
si    600          0 -0.0040 -0.0905 -0.0451 -0.0717  0.4251   0.0293  0.0685  0.4260  0.0008  0.060
```

r_C mediu **-0.0647**, rho cu fuziunea **-0.0998**, rho cu A **-0.1061**, rho cu B **-0.0832**.
Corelatie partiala medie **-0.0014**, prag **0.1173**; trece pe **0 limbi din 10**, semn consistent pe **6/10**.
Plafon peste orice u, mediat pe limbi: **0.684710**, adica **+0.000861** peste fuziune.
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
ca    445          0  0.0524  0.0886  0.0443  0.0670  0.5566   0.0182  0.0854  0.5568  0.0002  0.025
de    570          0  0.1192 -0.0017 -0.0087 -0.0068  0.7468   0.1869  0.1235  0.7571  0.0103  0.145
en    570          0 -0.0257 -0.0569 -0.0215 -0.0352  0.8700   0.0099  0.1797  0.8701  0.0000  0.005
es    593          0  0.0130 -0.0492 -0.0597 -0.0584  0.7641   0.0894  0.1287  0.7663  0.0022  0.070
fil   570          6 -0.0246  0.2323  0.1436  0.1935  0.5091  -0.1458  0.0788  0.5243  0.0152 -0.315
fr    569          9 -0.0447 -0.0455 -0.0005 -0.0197  0.6590  -0.0421  0.1026  0.6598  0.0008 -0.050
it    570         24  0.0226 -0.0531  0.0094 -0.0132  0.6750   0.0427  0.1058  0.6757  0.0007  0.045
ja    570         43 -0.1149 -0.1492 -0.0943 -0.1283  0.7877  -0.0225  0.1369  0.7878  0.0001 -0.020
pt    567         15 -0.0078 -0.0359 -0.0542 -0.0495  0.8450   0.0637  0.1633  0.8457  0.0007  0.040
si    600          0  0.1735  0.1374  0.2369  0.2375  0.4251   0.0825  0.0685  0.4316  0.0065  0.160
```

r_C mediu **+0.0163**, rho cu fuziunea **+0.0187**, rho cu A **+0.0067**, rho cu B **+0.0195**.
Corelatie partiala medie **+0.0283**, prag **0.1173**; trece pe **3 limbi din 10**, semn consistent pe **7/10**.
Plafon peste orice u, mediat pe limbi: **0.687521**, adica **+0.003672** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `dezacord`  (derivat din 3 membri)

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0 -0.0138  0.0290 -0.0136  0.0015  0.5566  -0.0176  0.0854  0.5568  0.0002 -0.025
de    570          0 -0.0309 -0.1168 -0.0944 -0.1122  0.7468   0.0801  0.1235  0.7487  0.0019  0.065
en    570          0 -0.0196 -0.0276 -0.0307 -0.0307  0.8700   0.0145  0.1797  0.8701  0.0000  0.010
es    593          0 -0.0762 -0.1523 -0.1318 -0.1449  0.7641   0.0541  0.1287  0.7649  0.0008  0.045
fil   570          6 -0.0534 -0.0168  0.0036 -0.0049  0.5091  -0.0591  0.0788  0.5116  0.0025 -0.110
fr    569          9 -0.1535 -0.1383 -0.1493 -0.1542  0.6590  -0.0698  0.1026  0.6611  0.0021 -0.090
it    570         24 -0.0897 -0.1790 -0.1061 -0.1388  0.6750   0.0055  0.1058  0.6750  0.0000  0.005
ja    570         43 -0.1423 -0.1645 -0.1402 -0.1655  0.7877  -0.0196  0.1369  0.7878  0.0001 -0.015
pt    567         15 -0.1589 -0.1963 -0.2189 -0.2185  0.8450   0.0493  0.1633  0.8454  0.0004  0.030
si    600          0  0.1089  0.1213  0.0651  0.0996  0.4251   0.0739  0.0685  0.4304  0.0052  0.140
```

r_C mediu **-0.0629**, rho cu fuziunea **-0.0869**, rho cu A **-0.0841**, rho cu B **-0.0816**.
Corelatie partiala medie **+0.0111**, prag **0.1173**; trece pe **1 limbi din 10**, semn consistent pe **6/10**.
Plafon peste orice u, mediat pe limbi: **0.685177**, adica **+0.001328** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

## Sinteza, ordonata dupa plafon

```
                      r_C     rho_F   partial      prag     R_max        dR  limbi_trec  semn
candidat                                                                                     
qwen3-8b-4bit    0.094217  0.125115  0.038398  0.117318  0.688258  0.004410           3     8
medie            0.016304  0.018681  0.028299  0.117318  0.687521  0.003672           3     7
qwen35-9b-8bit   0.003491  0.010913  0.025986  0.117318  0.686987  0.003138           2     6
dezacord        -0.062930 -0.086866  0.011124  0.117318  0.685177  0.001328           1     6
gemma4-12b-4bit -0.064651 -0.099777 -0.001450  0.117318  0.684710  0.000861           0     6
```

Bara e +0.0045. Coloana `dR` e plafonul, nu castigul: cu u optim in-sample per limba. Coloana `semn` e numarul de limbi pe care corelatia partiala are semnul majoritar; sub 8 din 10, selectia LOLO a unui u global il duce la zero indiferent ce spune media.

