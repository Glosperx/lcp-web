# Semnalul C ca al treilea termen: `ens6`

Generat de `analysis_c_fuse.py`, directoare ['bakeoff_test_Text', 'surprisal_test'], grila lui u [-0.30, +0.30] cu 13 puncte. Fuziunea de referinta e inghetata din `fusion_preds_lolo_adoptat_temp.csv`.

## Rezultatul pe test, cu u ales LOLO

```
        n  n_ctx     u     r_azi     r_nou     delta      d_lo      d_hi     d_p    latime
lang                                                                                      
ca    445    150  0.05  0.556579  0.556589  0.000010 -0.003548  0.003748  0.5100  0.045403
de    570    193 -0.00  0.746827  0.746827  0.000000  0.000000  0.000000  0.0000  0.049611
en    570    190  0.05  0.870037  0.869715 -0.000322 -0.002637  0.001760  0.3995  0.041919
es    593    208  0.05  0.764081  0.764915  0.000835 -0.001616  0.003398  0.7400  0.043795
fil   570    555  0.05  0.509095  0.501718 -0.007377 -0.011363 -0.003451  0.0000  0.041820
fr    569    191  0.05  0.658991  0.656845 -0.002147 -0.005233  0.001130  0.0950  0.042832
it    570    192  0.05  0.675010  0.675852  0.000842 -0.001813  0.003593  0.7475  0.044967
ja    570    190  0.05  0.787713  0.787060 -0.000653 -0.003469  0.001847  0.3145  0.042138
pt    567    562  0.05  0.845018  0.845149  0.000131 -0.002298  0.002413  0.5435  0.042641
si    600    578 -0.00  0.425137  0.425137  0.000000  0.000000  0.000000  0.0000  0.049413
```

Media pe limbi: azi **0.683849**, cu C **0.682981**, diferenta **-0.000868**, interval PERECHE [-0.001657, -0.000084], P(>0) = 1.6%.

## Conditia care se citeste INAINTEA mediei

**1 limbi stricate cu interval care exclude zero: ['fil'].**

Fata de bara de +0.0045: **NU trece**.

## Cat de plat e criteriul

Latimea curbei lui u pe limbile de potrivire, adica r maxim minus r minim peste grila: medie **0.044454**, interval [0.041820, 0.049611]. u ales: {'ca': 0.05, 'de': -0.0, 'en': 0.05, 'es': 0.05, 'fil': 0.05, 'fr': 0.05, 'it': 0.05, 'ja': 0.05, 'pt': 0.05, 'si': -0.0}.

## Podeaua de zgomot

Aceeasi grila si acelasi criteriu, cu C inlocuit de o coloana aleatoare. Spune cat scoate procedura cand semnalul nu contine nimic.

```
samanta   delta pe medie   u ales
1         -0.000081        [-0.05, -0.0]
2         +0.000000        [-0.0]
3         +0.000000        [-0.0]
4         -0.000199        [-0.0, 0.05]
5         -0.000455        [-0.05, -0.0]
```

Podeaua: medie **-0.000147**, maxim **+0.000000** pe 5 seminte. Castigul peste podea al candidatului: **-0.000721**.

