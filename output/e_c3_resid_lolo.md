# Semnalul C ca al treilea termen: `resid_lolo`

Generat de `analysis_c_fuse.py`, directoare ['bakeoff_test_Text', 'surprisal_test'], grila lui u [-0.30, +0.30] cu 13 puncte. Fuziunea de referinta e inghetata din `fusion_preds_lolo_adoptat_temp.csv`.

## Rezultatul pe test, cu u ales LOLO

```
        n  n_ctx     u     r_azi     r_nou     delta      d_lo      d_hi     d_p    latime
lang                                                                                      
ca    445    150 -0.10  0.556579  0.555871 -0.000708 -0.002715  0.001303  0.2480  0.029672
de    570    193 -0.15  0.746827  0.745050 -0.001777 -0.005246  0.001643  0.1610  0.026758
en    570    190 -0.15  0.870037  0.868231 -0.001805 -0.003663  0.000156  0.0370  0.029782
es    593    208 -0.15  0.764081  0.762493 -0.001588 -0.003336  0.000306  0.0525  0.029788
fil   570    555  0.05  0.509095  0.500523 -0.008571 -0.010726 -0.006479  0.0000  0.016803
fr    569    191 -0.10  0.658991  0.659650  0.000659 -0.001225  0.002629  0.7525  0.028143
it    570    192 -0.15  0.675010  0.673589 -0.001421 -0.003663  0.000807  0.1080  0.030111
ja    570    190 -0.20  0.787713  0.782479 -0.005234 -0.009917 -0.000963  0.0080  0.028529
pt    567    562 -0.10  0.845018  0.844864 -0.000154 -0.001645  0.001317  0.4090  0.028145
si    600    578 -0.15  0.425137  0.422270 -0.002867 -0.006938  0.001259  0.0810  0.029636
```

Media pe limbi: azi **0.683849**, cu C **0.681502**, diferenta **-0.002347**, interval PERECHE [-0.003243, -0.001498], P(>0) = 0.0%.

## Conditia care se citeste INAINTEA mediei

**2 limbi stricate cu interval care exclude zero: ['fil', 'ja'].**

Fata de bara de +0.0045: **NU trece**.

## Cat de plat e criteriul

Latimea curbei lui u pe limbile de potrivire, adica r maxim minus r minim peste grila: medie **0.027737**, interval [0.016803, 0.030111]. u ales: {'ca': -0.1, 'de': -0.15, 'en': -0.15, 'es': -0.15, 'fil': 0.05, 'fr': -0.1, 'it': -0.15, 'ja': -0.2, 'pt': -0.1, 'si': -0.15}.

## Podeaua de zgomot

Aceeasi grila si acelasi criteriu, cu C inlocuit de o coloana aleatoare. Spune cat scoate procedura cand semnalul nu contine nimic.

```
samanta   delta pe medie   u ales
1         +0.000000        [-0.0]
2         +0.000000        [-0.0]
3         +0.000000        [-0.0]
4         +0.000000        [-0.0]
5         +0.000000        [-0.0]
```

Podeaua: medie **+0.000000**, maxim **+0.000000** pe 5 seminte. Castigul peste podea al candidatului: **-0.002347**.

