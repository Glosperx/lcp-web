# Semnalul C prin frontiera, ca poarta

**Excluse ca degenerate pe text brut, prin `analysis_c_sanatate.py`: ['gemma4-12b-4bit'].**
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

### `entropie`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.2466  0.3216  0.5126  0.4992  0.5566  -0.0434  0.0854  0.5577  0.0012 -0.080
de    570          0  0.1340 -0.0048  0.0152  0.0090  0.7468   0.1913  0.1235  0.7576  0.0108  0.145
en    570          0  0.6384  0.6909  0.7792  0.7759  0.8700  -0.1178  0.1797  0.8720  0.0019 -0.110
es    593          0  0.4251  0.4973  0.6257  0.6055  0.7641  -0.0731  0.1287  0.7655  0.0015 -0.080
fil   570          0  0.3607  0.6251  0.7473  0.7545  0.5091  -0.0414  0.0788  0.5103  0.0012 -0.110
fr    569          0  0.4985  0.5428  0.6824  0.6670  0.6590   0.1052  0.1026  0.6637  0.0047  0.155
it    570          0  0.2220  0.3217  0.4685  0.4398  0.6750  -0.1129  0.1058  0.6801  0.0051 -0.150
ja    570          0  0.1717  0.2547  0.2999  0.3111  0.7877  -0.1252  0.1369  0.7915  0.0038 -0.110
pt    567          0  0.5371  0.6261  0.6760  0.6821  0.8450  -0.1006  0.1633  0.8467  0.0017 -0.090
si    600          0  0.0233  0.1328  0.1566  0.1743  0.4251  -0.0570  0.0685  0.4283  0.0031 -0.135
```

r_C mediu **+0.3257**, rho cu fuziunea **+0.4918**, rho cu A **+0.4008**, rho cu B **+0.4964**.
Corelatie partiala medie **-0.0375**, prag **0.1173**; trece pe **3 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.687350**, adica **+0.003502** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `dezacord_B`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0462  0.0545  0.0047  0.0248  0.5566   0.0391  0.0854  0.5575  0.0009  0.055
de    570          0 -0.2568 -0.2146 -0.1943 -0.2212  0.7468  -0.1413  0.1235  0.7527  0.0059 -0.155
en    570          0 -0.1818 -0.1948 -0.1325 -0.1600  0.8700  -0.0875  0.1797  0.8711  0.0011 -0.055
es    593          0 -0.1689 -0.2415 -0.2770 -0.2758  0.7641   0.0675  0.1287  0.7653  0.0012  0.055
fil   570          0  0.0957  0.0651  0.1019  0.0942  0.5091   0.0557  0.0788  0.5113  0.0023  0.085
fr    569          0 -0.0110  0.0108  0.0052  0.0079  0.6590  -0.0216  0.1026  0.6592  0.0002 -0.025
it    570          0 -0.1937 -0.2404 -0.2558 -0.2641  0.6750  -0.0217  0.1058  0.6752  0.0002 -0.025
ja    570          0 -0.2190 -0.2316 -0.2681 -0.2798  0.7877   0.0025  0.1369  0.7877  0.0000  0.000
pt    567          0 -0.1328 -0.2260 -0.1569 -0.1875  0.8450   0.0489  0.1633  0.8454  0.0004  0.030
si    600          0 -0.0198 -0.0523 -0.1090 -0.1048  0.4251   0.0274  0.0685  0.4259  0.0007  0.055
```

r_C mediu **-0.1042**, rho cu fuziunea **-0.1366**, rho cu A **-0.1271**, rho cu B **-0.1282**.
Corelatie partiala medie **-0.0031**, prag **0.1173**; trece pe **1 limbi din 10**, semn consistent pe **6/10**.
Plafon peste orice u, mediat pe limbi: **0.685140**, adica **+0.001291** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `vecinatate`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0173  0.0119  0.0788  0.0620  0.5566  -0.0208  0.0854  0.5568  0.0003 -0.030
de    570          0  0.1017  0.2939  0.2988  0.3262  0.7468  -0.2256  0.1235  0.7618  0.0149 -0.250
en    570          0  0.1592  0.2014  0.1480  0.1728  0.8700   0.0182  0.1797  0.8701  0.0000  0.010
es    593          0  0.1172  0.1644  0.1688  0.1744  0.7641  -0.0253  0.1287  0.7643  0.0002 -0.020
fil   570          0  0.1777  0.3306  0.2688  0.3171  0.5091   0.0199  0.0788  0.5094  0.0003  0.035
fr    569          0  0.0711  0.2294  0.1905  0.2194  0.6590  -0.1002  0.1026  0.6633  0.0043 -0.130
it    570          0  0.1117  0.2676  0.2065  0.2403  0.6750  -0.0705  0.1058  0.6770  0.0020 -0.085
ja    570          0  0.1077  0.1472  0.1057  0.1350  0.7877   0.0022  0.1369  0.7877  0.0000  0.000
pt    567          0  0.3147  0.4114  0.3928  0.4136  0.8450  -0.0715  0.1633  0.8459  0.0009 -0.050
si    600          0  0.1691 -0.0306  0.1674  0.1153  0.4251   0.1336  0.0685  0.4420  0.0169  0.230
```

r_C mediu **+0.1347**, rho cu fuziunea **+0.2176**, rho cu A **+0.2027**, rho cu B **+0.2026**.
Corelatie partiala medie **-0.0340**, prag **0.1173**; trece pe **2 limbi din 10**, semn consistent pe **6/10**.
Plafon peste orice u, mediat pe limbi: **0.687822**, adica **+0.003973** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `resid_lolo`

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0 -0.5222 -0.7773 -0.8856 -0.9493  0.5566   0.0236  0.0854  0.5569  0.0003  0.090
de    570          0 -0.6446 -0.8133 -0.7800 -0.8691  0.7468   0.0137  0.1235  0.7469  0.0001  0.025
en    570          0 -0.8237 -0.8918 -0.9445 -0.9601  0.8700   0.0845  0.1797  0.8710  0.0010  0.130
es    593          0 -0.7220 -0.8912 -0.9340 -0.9581  0.7641   0.0544  0.1287  0.7649  0.0008  0.120
fil   570          0 -0.6115 -0.7216 -0.9098 -0.9015  0.5091  -0.4096  0.0788  0.6192  0.1101 -0.600
fr    569          0 -0.6400 -0.8313 -0.9419 -0.9556  0.6590  -0.0463  0.1026  0.6599  0.0009 -0.275
it    570          0 -0.6408 -0.8702 -0.9368 -0.9633  0.6750   0.0477  0.1058  0.6759  0.0009  0.140
ja    570          0 -0.6723 -0.7131 -0.8583 -0.8834  0.7877   0.0816  0.1369  0.7893  0.0016  0.110
pt    567          0 -0.8028 -0.8858 -0.9312 -0.9480  0.8450  -0.0102  0.1633  0.8450  0.0000 -0.020
si    600          0 -0.3484 -0.4286 -0.8977 -0.8620  0.4251   0.0394  0.0685  0.4266  0.0015  0.125
```

r_C mediu **-0.6428**, rho cu fuziunea **-0.9250**, rho cu A **-0.7824**, rho cu B **-0.9020**.
Corelatie partiala medie **-0.0121**, prag **0.1173**; trece pe **1 limbi din 10**, semn consistent pe **7/10**.
Plafon peste orice u, mediat pe limbi: **0.695578**, adica **+0.011730** peste fuziune.
**Verdict: trece plafonul dar SEMNUL SE SCHIMBA (7 pozitive, 3 negative), deci u ales LOLO va fi ~0.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `medie`  (derivat din 2 membri)

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0836  0.1589  0.0992  0.1345  0.5566   0.0106  0.0854  0.5566  0.0001  0.015
de    570          0  0.2095  0.0868  0.0623  0.0778  0.7468   0.2284  0.1235  0.7621  0.0153  0.170
en    570          0 -0.0531 -0.1018 -0.0671 -0.0822  0.8700   0.0375  0.1797  0.8702  0.0002  0.020
es    593          0  0.0167 -0.0201 -0.0293 -0.0272  0.7641   0.0582  0.1287  0.7650  0.0009  0.045
fil   570          4  0.0433  0.3939  0.2709  0.3458  0.5091  -0.1644  0.0788  0.5284  0.0193 -0.365
fr    569          6  0.0079  0.0159  0.0369  0.0303  0.6590  -0.0161  0.1026  0.6591  0.0001 -0.020
it    570         16  0.0889  0.0383  0.0881  0.0745  0.6750   0.0524  0.1058  0.6761  0.0011  0.055
ja    570         30 -0.0662 -0.1185 -0.0595 -0.0917  0.7877   0.0099  0.1369  0.7877  0.0000  0.010
pt    567         10  0.0023 -0.0203 -0.0313 -0.0284  0.8450   0.0493  0.1633  0.8454  0.0004  0.030
si    600          0  0.2054  0.2122  0.3029  0.3186  0.4251   0.0815  0.0685  0.4315  0.0064  0.165
```

r_C mediu **+0.0538**, rho cu fuziunea **+0.0752**, rho cu A **+0.0645**, rho cu B **+0.0673**.
Corelatie partiala medie **+0.0347**, prag **0.1173**; trece pe **3 limbi din 10**, semn consistent pe **8/10**.
Plafon peste orice u, mediat pe limbi: **0.688227**, adica **+0.004378** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

### `dezacord`  (derivat din 2 membri)

```
        n  n_nefinit     r_C   rho_A   rho_B   rho_F     r_F  partial    prag   R_max      dR  u_opt
lang                                                                                                
ca    445          0  0.0597  0.0381  0.0740  0.0688  0.5566   0.0258  0.0854  0.5570  0.0004  0.035
de    570          0 -0.0429 -0.1223 -0.0818 -0.1054  0.7468   0.0541  0.1235  0.7477  0.0009  0.045
en    570          0 -0.0351 -0.0606 -0.0335 -0.0446  0.8700   0.0076  0.1797  0.8700  0.0000  0.005
es    593          0 -0.1406 -0.1772 -0.1801 -0.1867  0.7641   0.0031  0.1287  0.7641  0.0000  0.005
fil   570          4 -0.0409  0.0229  0.0144  0.0192  0.5091  -0.0589  0.0788  0.5116  0.0025 -0.110
fr    569          6 -0.0480 -0.1272 -0.0950 -0.1148  0.6590   0.0371  0.1026  0.6596  0.0006  0.040
it    570         16 -0.0464 -0.1852 -0.0871 -0.1281  0.6750   0.0547  0.1058  0.6762  0.0012  0.055
ja    570         30 -0.1389 -0.1843 -0.1725 -0.1956  0.7877   0.0251  0.1369  0.7879  0.0002  0.020
pt    567         10 -0.1064 -0.1551 -0.1456 -0.1543  0.8450   0.0453  0.1633  0.8454  0.0003  0.030
si    600          0  0.0987  0.0474  0.0708  0.0736  0.4251   0.0747  0.0685  0.4305  0.0053  0.140
```

r_C mediu **-0.0441**, rho cu fuziunea **-0.0768**, rho cu A **-0.0904**, rho cu B **-0.0636**.
Corelatie partiala medie **+0.0269**, prag **0.1173**; trece pe **1 limbi din 10**, semn consistent pe **9/10**.
Plafon peste orice u, mediat pe limbi: **0.684993**, adica **+0.001144** peste fuziune.
**Verdict: NU trece plafonul.**

Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.

## Sinteza, ordonata dupa plafon

```
                     r_C     rho_F   partial      prag     R_max        dR  limbi_trec  semn
candidat                                                                                    
resid_lolo     -0.642824 -0.925046 -0.012112  0.117318  0.695578  0.011730           1     7
qwen3-8b-4bit   0.094217  0.125115  0.038398  0.117318  0.688258  0.004410           3     8
medie           0.053833  0.075209  0.034726  0.117318  0.688227  0.004378           3     8
vecinatate      0.134741  0.217603 -0.033991  0.117318  0.687822  0.003973           2     6
entropie        0.325741  0.491833 -0.037490  0.117318  0.687350  0.003502           3     8
qwen35-9b-8bit  0.003491  0.010913  0.025986  0.117318  0.686987  0.003138           2     6
dezacord_B     -0.104188 -0.136630 -0.003106  0.117318  0.685140  0.001291           1     6
dezacord       -0.044078 -0.076781  0.026872  0.117318  0.684993  0.001144           1     9
```

Bara e +0.0045. Coloana `dR` e plafonul, nu castigul: cu u optim in-sample per limba. Coloana `semn` e numarul de limbi pe care corelatia partiala are semnul majoritar; sub 8 din 10, selectia LOLO a unui u global il duce la zero indiferent ce spune media.

