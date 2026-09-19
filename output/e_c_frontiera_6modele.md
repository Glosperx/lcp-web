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

### `aya-expanse-8b-4bit`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0690  0.0485  0.0799  0.0772  0.5566   0.0314  0.0854  0.5572  0.0006  0.045
de    570          0  0.1839  0.0478  0.0294  0.0394  0.7468   0.2325  0.1235  0.7627  0.0158  0.175
en    570          0  0.0265 -0.0075  0.0272  0.0156  0.8700   0.0262  0.1797  0.8701  0.0001  0.015
es    593          0 -0.0162 -0.0749 -0.0860 -0.0856  0.7641   0.0765  0.1287  0.7657  0.0016  0.060
fil   570          2  0.0787  0.3309  0.2591  0.3109  0.5091  -0.0973  0.0788  0.5159  0.0068 -0.195
fr    569          3 -0.0366  0.0014  0.0330  0.0217  0.6590  -0.0677  0.1026  0.6610  0.0020 -0.085
it    570          8  0.0046 -0.0523  0.0068 -0.0146  0.6750   0.0196  0.1058  0.6752  0.0002  0.020
ja    570          0 -0.1172 -0.1587 -0.1285 -0.1552  0.7877   0.0082  0.1369  0.7877  0.0000  0.005
pt    567          5 -0.0578 -0.0703 -0.0762 -0.0768  0.8450   0.0134  0.1633  0.8450  0.0000  0.010
si    600          0  0.1873  0.1965  0.2915  0.3035  0.4251   0.0676  0.0685  0.4295  0.0044  0.135
```

r_C mediu **+0.0322**, rho cu fuziunea **+0.0436**, rho cu A **+0.0262**, rho cu B **+0.0436**.
Corelatie partiala medie **+0.0310**, prag **0.1173**; trece pe **2 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.687001**, adica **+0.003152** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

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

### `qwen3-8b-8bit`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.1132  0.2107  0.1399  0.1844  0.5566   0.0129  0.0854  0.5567  0.0001  0.020
de    570          0  0.2688  0.1667  0.1174  0.1478  0.7468   0.2408  0.1235  0.7638  0.0170  0.185
en    570          0 -0.0546 -0.1065 -0.0587 -0.0782  0.8700   0.0273  0.1797  0.8701  0.0001  0.015
es    593          0  0.0639  0.0652  0.0546  0.0608  0.7641   0.0271  0.1287  0.7643  0.0002  0.020
fil   570          2  0.0508  0.3996  0.2648  0.3443  0.5091  -0.1541  0.0788  0.5261  0.0170 -0.340
fr    569          3  0.0739  0.1088  0.1142  0.1192  0.6590  -0.0062  0.1026  0.6590  0.0000 -0.005
it    570          8  0.1800  0.1972  0.2003  0.2101  0.6750   0.0529  0.1058  0.6761  0.0011  0.055
ja    570         10  0.0105 -0.0513  0.0125 -0.0144  0.7877   0.0353  0.1369  0.7880  0.0003  0.025
pt    567          5  0.0694  0.0661  0.0405  0.0512  0.8450   0.0489  0.1633  0.8454  0.0004  0.030
si    600          0  0.2522  0.1879  0.3144  0.3174  0.4251   0.1365  0.0685  0.4427  0.0176  0.255
```

r_C mediu **+0.1028**, rho cu fuziunea **+0.1343**, rho cu A **+0.1244**, rho cu B **+0.1200**.
Corelatie partiala medie **+0.0422**, prag **0.1173**; trece pe **3 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.689232**, adica **+0.005383** peste fuziune.
**Verdict: TRECE plafonul si semnul e consistent.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `qwen35-9b-4bit`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0174  0.0669  0.0147  0.0369  0.5566  -0.0038  0.0854  0.5566  0.0000 -0.005
de    570          0  0.1335  0.0066  0.0080  0.0082  0.7468   0.1915  0.1235  0.7576  0.0108  0.145
en    570          0 -0.0451 -0.0923 -0.0682 -0.0795  0.8700   0.0489  0.1797  0.8704  0.0003  0.025
es    593          0 -0.0529 -0.1194 -0.1177 -0.1233  0.7641   0.0646  0.1287  0.7652  0.0011  0.050
fil   570          2  0.0389  0.3040  0.2180  0.2727  0.5091  -0.1207  0.0788  0.5196  0.0105 -0.250
fr    569          3 -0.0485 -0.0525 -0.0270 -0.0396  0.6590  -0.0298  0.1026  0.6594  0.0004 -0.035
it    570          8  0.0062 -0.0989 -0.0132 -0.0455  0.6750   0.0501  0.1058  0.6760  0.0010  0.050
ja    570         20 -0.1164 -0.1441 -0.1057 -0.1336  0.7877  -0.0183  0.1369  0.7878  0.0001 -0.015
pt    567          5 -0.0790 -0.1135 -0.1179 -0.1205  0.8450   0.0430  0.1633  0.8453  0.0003  0.025
si    600          0  0.1694  0.1975  0.2770  0.2928  0.4251   0.0518  0.0685  0.4277  0.0026  0.105
```

r_C mediu **+0.0023**, rho cu fuziunea **+0.0069**, rho cu A **-0.0046**, rho cu B **+0.0068**.
Corelatie partiala medie **+0.0277**, prag **0.1173**; trece pe **2 limbi din 10**, semn consistent pe **6/10**.
Plafon peste orice u, mediat pe limbi: **0.686560**, adica **+0.002712** peste fuziune.
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

### `medie`  (derivat din 6 membri)

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0807  0.1383  0.0888  0.1189  0.5566   0.0176  0.0854  0.5568  0.0002  0.025
de    570          0  0.2152  0.0870  0.0546  0.0724  0.7468   0.2430  0.1235  0.7641  0.0173  0.180
en    570          0 -0.0395 -0.0865 -0.0494 -0.0647  0.8700   0.0341  0.1797  0.8702  0.0002  0.020
es    593          0  0.0129 -0.0227 -0.0324 -0.0302  0.7641   0.0558  0.1287  0.7649  0.0008  0.045
fil   570         12  0.0453  0.3937  0.2727  0.3468  0.5091  -0.1627  0.0788  0.5280  0.0189 -0.365
fr    569         18  0.0077  0.0355  0.0510  0.0477  0.6590  -0.0315  0.1026  0.6594  0.0004 -0.035
it    570         48  0.0868  0.0442  0.0911  0.0787  0.6750   0.0458  0.1058  0.6759  0.0008  0.050
ja    570         61 -0.0790 -0.1246 -0.0841 -0.1107  0.7877   0.0134  0.1369  0.7878  0.0000  0.010
pt    567         30  0.0007 -0.0169 -0.0332 -0.0285  0.8450   0.0463  0.1633  0.8454  0.0004  0.030
si    600          0  0.2171  0.1981  0.3209  0.3266  0.4251   0.0914  0.0685  0.4331  0.0080  0.180
```

r_C mediu **+0.0548**, rho cu fuziunea **+0.0757**, rho cu A **+0.0646**, rho cu B **+0.0680**.
Corelatie partiala medie **+0.0353**, prag **0.1173**; trece pe **3 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.688552**, adica **+0.004703** peste fuziune.
**Verdict: TRECE plafonul si semnul e consistent.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `dezacord`  (derivat din 6 membri)

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0341  0.0109  0.0175  0.0170  0.5566   0.0297  0.0854  0.5571  0.0005  0.040
de    570          0 -0.0276 -0.1393 -0.1085 -0.1309  0.7468   0.1065  0.1235  0.7502  0.0034  0.085
en    570          0  0.0269  0.0056  0.0352  0.0257  0.8700   0.0091  0.1797  0.8700  0.0000  0.005
es    593          0 -0.1141 -0.1700 -0.1610 -0.1711  0.7641   0.0263  0.1287  0.7643  0.0002  0.020
fil   570         12 -0.0378  0.0256  0.0361  0.0345  0.5091  -0.0643  0.0788  0.5121  0.0030 -0.120
fr    569         18 -0.1004 -0.1329 -0.0915 -0.1150  0.6590  -0.0329  0.1026  0.6595  0.0005 -0.040
it    570         48 -0.0771 -0.2215 -0.1092 -0.1566  0.6750   0.0392  0.1058  0.6756  0.0006  0.040
ja    570         61 -0.1950 -0.2514 -0.2473 -0.2748  0.7877   0.0364  0.1369  0.7880  0.0003  0.030
pt    567         30 -0.1195 -0.1605 -0.1719 -0.1739  0.8450   0.0522  0.1633  0.8455  0.0005  0.030
si    600          0  0.1300  0.0809  0.0964  0.1069  0.4251   0.0940  0.0685  0.4336  0.0084  0.170
```

r_C mediu **-0.0480**, rho cu fuziunea **-0.0838**, rho cu A **-0.0953**, rho cu B **-0.0704**.
Corelatie partiala medie **+0.0296**, prag **0.1173**; trece pe **1 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.685588**, adica **+0.001739** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

## Sinteza, ordonata dupa plafon

```
                          r_C     rho_F   partial      prag     R_max        dR  limbi_trec  semn
candidat                                                                                         
qwen3-8b-8bit        0.102795  0.134273  0.042157  0.117318  0.689232  0.005383           3     8
medie                0.054779  0.075704  0.035309  0.117318  0.688552  0.004703           3     8
qwen3-8b-4bit        0.094217  0.125115  0.038398  0.117318  0.688258  0.004410           3     8
llama31-8b-4bit      0.051102  0.069106  0.025489  0.117318  0.688039  0.004190           2     8
aya-expanse-8b-4bit  0.032224  0.043613  0.031048  0.117318  0.687001  0.003152           2     8
qwen35-9b-8bit       0.003491  0.010913  0.025986  0.117318  0.686987  0.003138           2     6
qwen35-9b-4bit       0.002345  0.006860  0.027743  0.117318  0.686560  0.002712           2     6
dezacord            -0.048024 -0.083829  0.029614  0.117318  0.685588  0.001739           1     8
```

Bara e +0.0045. Coloana `dR` e plafonul, nu castigul: cu u optim in-sample per limba. Coloana `semn` e numarul de limbi pe care corelatia partiala are semnul majoritar; sub 8 din 10, selectia LOLO a unui u global il duce la zero indiferent ce spune media.

