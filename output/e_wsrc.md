# `w_src`: de ce bratul EN-only cantareste mai mult

Generat de `analysis_wsrc.py`. Zero inferenta.

## H1: cat de plata e alegerea lui `w_src`

Curba ADEVARATA, adica r al fuziunii pe testul limbii L, pentru fiecare `w_src` de pe grila.
`w` e ales LOLO la fiecare punct, deci singura variabila e `w_src`.

```
       0.000   0.125   0.250   0.375   0.500   0.625   0.750   0.875   1.000
lang                                                                        
ca    0.5598  0.5596  0.5592  0.5588  0.5582  0.5574  0.5566  0.5556  0.5545
de    0.7357  0.7383  0.7407  0.7429  0.7450  0.7468  0.7485  0.7500  0.7513
en    0.8729  0.8728  0.8725  0.8722  0.8718  0.8713  0.8707  0.8700  0.8693
es    0.7608  0.7616  0.7623  0.7628  0.7633  0.7637  0.7639  0.7641  0.7641
fil   0.5090  0.5096  0.5073  0.5079  0.5085  0.5091  0.5096  0.5128  0.5132
fr    0.6681  0.6674  0.6633  0.6623  0.6613  0.6602  0.6590  0.6577  0.6606
it    0.6720  0.6728  0.6735  0.6741  0.6746  0.6750  0.6753  0.6755  0.6755
ja    0.7817  0.7801  0.7831  0.7853  0.7869  0.7877  0.7878  0.7871  0.7901
pt    0.8425  0.8431  0.8436  0.8440  0.8444  0.8447  0.8449  0.8450  0.8451
si    0.4180  0.4202  0.4221  0.4235  0.4246  0.4251  0.4251  0.4247  0.4239
```

Curba de CRITERIU, adica exact ce vede `fit_choice` cand alege (media imbricata pe celelalte noua limbi):

```
       0.000   0.125   0.250   0.375   0.500   0.625   0.750   0.875   1.000
lang                                                                        
ca    0.6948  0.6962  0.6976  0.6976  0.6981  0.6985  0.6986  0.6983  0.6985
de    0.6750  0.6761  0.6771  0.6779  0.6782  0.6782  0.6777  0.6772  0.6764
en    0.6604  0.6619  0.6624  0.6627  0.6630  0.6633  0.6637  0.6645  0.6636
es    0.6727  0.6731  0.6739  0.6746  0.6750  0.6753  0.6753  0.6754  0.6750
fil   0.7004  0.7012  0.7021  0.7028  0.7034  0.7036  0.7034  0.7033  0.7029
fr    0.6827  0.6837  0.6847  0.6859  0.6865  0.6869  0.6870  0.6868  0.6865
it    0.6824  0.6836  0.6844  0.6855  0.6860  0.6862  0.6856  0.6854  0.6851
ja    0.6700  0.6708  0.6716  0.6723  0.6726  0.6727  0.6727  0.6724  0.6721
pt    0.6637  0.6640  0.6649  0.6656  0.6660  0.6663  0.6663  0.6664  0.6660
si    0.7109  0.7122  0.7124  0.7123  0.7127  0.7129  0.7132  0.7131  0.7131
```

Comparatia, per limba:

```
      latime adevarata  latime criteriu  argmax adevarat  argmax criteriu  r la argmax criteriu  r la optim  cost al alegerii
lang                                                                                                                         
ca              0.0053           0.0038             0.00            0.750                0.5566      0.5598           -0.0032
de              0.0155           0.0032             1.00            0.625                0.7468      0.7513           -0.0045
en              0.0036           0.0041             0.00            0.875                0.8700      0.8729           -0.0029
es              0.0033           0.0026             1.00            0.875                0.7641      0.7641           -0.0000
fil             0.0059           0.0032             1.00            0.625                0.5091      0.5132           -0.0041
fr              0.0104           0.0043             0.00            0.750                0.6590      0.6681           -0.0091
it              0.0035           0.0038             1.00            0.625                0.6750      0.6755           -0.0005
ja              0.0100           0.0027             1.00            0.625                0.7877      0.7901           -0.0024
pt              0.0026           0.0027             1.00            0.875                0.8450      0.8451           -0.0001
si              0.0071           0.0023             0.75            0.750                0.4251      0.4251            0.0000
```

Latimea medie a curbei adevarate: **0.0067**. A criteriului: **0.0033**.
Argmax-ul criteriului nimereste argmax-ul adevarat pe **1 din 10** limbi.
Costul mediu al alegerii, fata de optimul care foloseste etichetele lui L: **-0.0027**.

## `w_src` FIXAT, ca alternativa la selectie

Media pe cele zece limbi a lui r al fuziunii, cu `w_src` aceeasi constanta peste tot:

```
w_src   r mediu
0.000   0.682053
0.125   0.682549
0.250   0.682751
0.375   0.683402
0.500   0.683855
0.625   0.684101
0.750   0.684142   <- ales LOLO in medie
0.875   0.684250
1.000   0.684764
```

Selectia LOLO a lui `w_src` da **0.683849**. Cel mai bun `w_src` FIX da **0.684764** la 1.000, dar acela e ales pe test, deci nu e o optiune.

Ce conteaza: intre `w_src = 0` (numai bratul multilingv) si selectia LOLO sunt **+0.001796**, iar intre `w_src = 1` (numai bratul englez) si selectia LOLO **-0.000915**.

## H2 si H4: cele doua brate, masurate separat

`p_en` e antrenat NUMAI pe CompLex EN. `p_multi` vede in plus randurile de TEST ale celorlalte noua limbi, deci ar TREBUI sa fie mai bun. H4 spune ca daca nu e, aia e chiar rezultatul.

```
        n   r_pen  r_pmulti  rho_brate  avantaj_pen
lang                                               
ca    445  0.4504    0.4813     0.9567      -0.0310
de    570  0.6828    0.6522     0.9555       0.0306
en    570  0.8225    0.8331     0.9769      -0.0106
es    593  0.6991    0.6962     0.9652       0.0029
fil   570  0.4174    0.4093     0.9845       0.0081
fr    569  0.5421    0.5601     0.9728      -0.0180
it    570  0.6464    0.6401     0.9680       0.0063
ja    570  0.6031    0.5982     0.8303       0.0049
pt    567  0.7843    0.7788     0.9775       0.0055
si    600  0.2965    0.3306     0.8087      -0.0341
```

Media: `p_en` **0.5945**, `p_multi` **0.5980**, avantajul lui `p_en` **-0.0035**.
`p_en` castiga pe **6 din 10** limbi.
Corelatia dintre brate, mediata pe limbi: **0.9396** (minim 0.8087 pe si).

Frontiera aplicata celor doua brate, adica ce ar da un amestec 50/50 standardizat:

```
       r_pen  r_pmulti  rho_brate  frontiera_50_50
lang                                              
ca    0.4504    0.4813     0.9567           0.4710
de    0.6828    0.6522     0.9555           0.6751
en    0.8225    0.8331     0.9769           0.8326
es    0.6991    0.6962     0.9652           0.7038
fil   0.4174    0.4093     0.9845           0.4150
fr    0.5421    0.5601     0.9728           0.5549
it    0.6464    0.6401     0.9680           0.6484
ja    0.6031    0.5982     0.8303           0.6279
pt    0.7843    0.7788     0.9775           0.7860
si    0.2965    0.3306     0.8087           0.3297
```

Media frontierei 50/50: **0.6044**, fata de 0.5945 la `p_en` singur si 0.5980 la `p_multi` singur. Amestecul castiga fiindca bratele sunt decorelate, nu fiindca unul ar fi mai bun.

## Mecanismul: `p_en` nu e mai BUN, e mai DECORELAT de semnalul B

Curba adevarata urca cu `w_src` desi `p_en` singur e mai slab decat `p_multi`. Singura explicatie compatibila cu amandoua e ca `p_en` aduce mai mult IN AMESTEC fiindca e mai putin corelat cu semnalul B. Se masoara direct, nu se presupune:

```
      r_A_pmulti  r_A_pen  rho_pmulti_B  rho_pen_B     r_B  mai_decorelat  front_pmulti  front_pen
lang                                                                                              
ca        0.4813   0.4504        0.5824     0.5393  0.5159         0.0431        0.5606     0.5507
de        0.6522   0.6828        0.6305     0.6121  0.6812         0.0185        0.7384     0.7596
en        0.8331   0.8225        0.8454     0.8444  0.8463         0.0010        0.8741     0.8689
es        0.6962   0.6991        0.8318     0.8198  0.7499         0.0120        0.7555     0.7595
fil       0.4093   0.4174        0.7045     0.6961  0.5082         0.0084        0.4969     0.5025
fr        0.5601   0.5421        0.7480     0.7525  0.6655        -0.0045        0.6555     0.6450
it        0.6401   0.6464        0.7770     0.7703  0.6354         0.0067        0.6766     0.6812
ja        0.5982   0.6031        0.6197     0.5895  0.7715         0.0302        0.7610     0.7709
pt        0.7788   0.7843        0.8513     0.8485  0.8322         0.0029        0.8372     0.8407
si        0.3306   0.2965        0.4930     0.3410  0.3860         0.1521        0.4147     0.4168
```

Corelatia cu B: `p_multi` **0.7084**, `p_en` **0.6813**. `p_en` e mai decorelat pe **9 din 10** limbi, cu o diferenta medie de **+0.0270**.
Frontiera A+B la 50/50: cu `p_multi` **0.6771**, cu `p_en` **0.6796**, diferenta **+0.0025**.

**Asta raspunde la intrebare.** `w_src` mare nu inseamna ca transferul din engleza e mai bun. Inseamna ca bratul englez, nevazand niciun rand de MLSP, face alte greseli decat un LLM care vede propozitia, iar fuziunea plateste pentru greseli diferite, nu pentru greseli mai putine. E acelasi mecanism ca la ansamblul de encodere, la alt nivel.

