# Atribuire pe sistemul multilingv, si reziduul semnat

Generat de `analysis_shap_multi.py`. Splitul e test, n = 5624. **Nimic din `output/shap/` nu se citeste aici**: acele artefacte sunt pe CompLex EN si pe conducta romaneasca.

## Blocul 1. Ce duce predictia, pe fiecare limba

Surogat HGB care prezice `p_fuz` din trasaturi numite, potrivit si citit PE LIMBA, cu 80/20 in interiorul limbii. Doua importante, fiindca pe trasaturi corelate nu sunt de acord.

### 1a. Surogat pe trasaturi lexicale, fara A si fara B

`r_surogat` e cat din `p_fuz` se reconstruieste din lexical singur. Cu cat e mai mare, cu atat sistemul se comporta mai mult ca un model lexical pe limba aia.

**Importanta prin PERMUTARE marginala:**

```
      r_surogat    zipf  length  syllables  capital    nsub
lang                                                       
ca       0.6850  0.5576 -0.0177     0.0111   0.0000  0.0216
de       0.7387  0.7114 -0.0026    -0.0025   0.0002  0.0616
en       0.8586  0.8064  0.0251     0.0166      NaN  0.0032
es       0.8757  0.6755  0.0153     0.0000   0.0000  0.0257
fil      0.8670  0.8608  0.0156    -0.0009   0.0000  0.0188
fr       0.8570  0.8280  0.0108    -0.0019      NaN  0.0129
it       0.9010  0.9064  0.0156    -0.0004      NaN  0.0100
ja       0.7725  0.6048 -0.0026        NaN      NaN  0.0790
pt       0.9174  0.7741  0.0083    -0.0002   0.0000  0.0067
si       0.4115     NaN  0.2317        NaN      NaN  0.3309
```

**Importanta prin REANTRENARE fara coloana**, adica ce recomanda Hooker, Mentch si Zhou in locul permutarii:

```
      r_surogat    zipf  length  syllables  capital    nsub
lang                                                       
ca       0.6850  0.3121 -0.0160    -0.0010   0.0000  0.0200
de       0.7387  0.3658 -0.0117    -0.0057  -0.0003  0.0064
en       0.8586  0.3932  0.0092     0.0021      NaN  0.0065
es       0.8757  0.2195  0.0037    -0.0010   0.0000  0.0212
fil      0.8670  0.2487  0.0107    -0.0001   0.0000  0.0084
fr       0.8570  0.2562 -0.0041    -0.0056      NaN -0.0017
it       0.9010  0.3020  0.0106    -0.0006      NaN  0.0080
ja       0.7725  0.2878 -0.0053        NaN      NaN -0.0008
pt       0.9174  0.2629  0.0045    -0.0012   0.0000  0.0019
si       0.4115     NaN  0.1652        NaN      NaN  0.2968
```

Media pe limbi, permutare: `zipf` +0.7472, `nsub` +0.0570, `length` +0.0300, `syllables` +0.0027, `capital` +0.0000

Media pe limbi, reantrenare: `zipf` +0.2942, `nsub` +0.0367, `length` +0.0167, `capital` -0.0001, `syllables` -0.0016

Coloane scoase per limba, constante sau integral NaN acolo: `ca` ['freq_na', 'surface_na']; `de` ['freq_na', 'surface_na']; `en` ['capital', 'freq_na', 'surface_na']; `es` ['freq_na', 'surface_na']; `fil` ['freq_na', 'surface_na']; `fr` ['capital', 'freq_na', 'surface_na']; `it` ['capital', 'freq_na', 'surface_na']; `ja` ['syllables', 'capital', 'freq_na', 'surface_na']; `pt` ['freq_na', 'surface_na']; `si` ['zipf', 'syllables', 'capital', 'freq_na', 'surface_na'].

### 1b. Control de fidelitate: acelasi surogat, dar cu A si B in set

Amestecul e liniar in `zA` si `zB`, deci surogatul trebuie sa-l recupereze aproape exact. E controlul care spune ca importantele de mai sus masoara datele, nu neputinta modelului.

```
      r_surogat       A       B     dif  abs_dif
lang                                            
ca       0.9899  0.1499  0.6062  0.0005   0.0004
de       0.9985  0.1306  0.7427  0.0003   0.0004
en       0.9969  0.1102  0.6739  0.0007  -0.0000
es       0.9984  0.0970  0.6532  0.0010   0.0002
fil      0.9984  0.1672  0.6098  0.0007   0.0003
fr       0.9973  0.1157  0.6775  0.0010   0.0003
it       0.9979  0.1140  0.6684  0.0005   0.0002
ja       0.9972  0.2297  0.5288  0.0016   0.0003
pt       0.9983  0.0811  0.6391  0.0002   0.0009
si       0.9973  0.2142  0.6190 -0.0001  -0.0000
```

`r_surogat` mediu **0.9970**. Raportul importantelor `B` / `A` = 0.6419 / 0.1410 = **4.6x**.

### 1c. Itemii pe care A si B gresesc AMANDOUA in acelasi sens

Definitie: `sign(z_y - zA) == sign(z_y - zB)` si amandoua abaterile peste o deviatie standard. `semn_pozitiv` e cate din ele sunt SUBevaluate de ambele semnale.

```
          n  n_ambele     pct  zipf_in  zipf_afara  nsub_in  nsub_afara  semn_pozitiv
lang                                                                                 
ca    445.0      64.0  14.382    2.931       3.137    2.609       2.609          30.0
de    570.0      35.0   6.140    3.337       3.307    2.457       2.570          20.0
en    570.0      15.0   2.632    3.443       4.016    2.267       1.874           9.0
es    593.0      41.0   6.914    3.421       3.975    2.317       1.938          20.0
fil   570.0     104.0  18.246    2.730       3.175    2.500       2.343          60.0
fr    569.0      71.0  12.478    3.751       4.175    2.338       1.972          40.0
it    570.0      63.0  11.053    2.834       3.536    2.651       2.325          30.0
ja    570.0      26.0   4.561    3.482       4.031    3.885       3.346          13.0
pt    567.0      16.0   2.822    3.648       3.849    2.062       2.083          10.0
si    600.0      91.0  15.167    0.000       0.000    3.736       3.246          44.0
```

Pe total **526 itemi din 5624**, adica 9.4%. Coada: si 15.2%, fil 18.2%, ca 14.4%, fata de en 2.6%.

## Blocul 2. Reziduul semnat, prezis leave-one-language-out

Antrenat pe randurile de test ale celorlalte noua limbi, aplicat pe a zecea. Zero etichete in limba evaluata, exact protocolul semnalului A.

```
        n   r_rez     r_C   rho_F  partial    prag   R_max      dR
lang                                                              
ca    445  0.4535 -0.5222 -0.9493   0.0236  0.0854  0.5569  0.0003
de    570  0.3156 -0.6446 -0.8691   0.0137  0.1235  0.7469  0.0001
en    570  0.2676 -0.8237 -0.9601   0.0845  0.1797  0.8710  0.0010
es    593  0.3437 -0.7220 -0.9581   0.0544  0.1287  0.7649  0.0008
fil   570  0.2927 -0.6115 -0.9015  -0.4096  0.0788  0.6192  0.1101
fr    569  0.3821 -0.6400 -0.9556  -0.0463  0.1026  0.6599  0.0009
it    570  0.4000 -0.6408 -0.9633   0.0477  0.1058  0.6759  0.0009
ja    570  0.3240 -0.6723 -0.8834   0.0816  0.1369  0.7893  0.0016
pt    567  0.2608 -0.8028 -0.9480  -0.0102  0.1633  0.8450  0.0000
si    600  0.4790 -0.3484 -0.8620   0.0394  0.0685  0.4266  0.0015
```

`r_rez` e corelatia out-of-fold cu reziduul insusi, medie **+0.3519**. Corelatie partiala cu eticheta, controland pe fuziune: medie **-0.0121**, prag **0.1173**, trece pe **1 limbi din 10**, semn consistent pe **7/10**.
Plafon peste orice u: **0.695578**, adica **+0.011730** peste fuziune.

**Verdict: NU trece poarta.**

