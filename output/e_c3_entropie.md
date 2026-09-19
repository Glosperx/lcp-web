# Semnalul C ca al treilea termen: `entropie`

Generat de `analysis_c_fuse.py`, directoare ['bakeoff_test_Text', 'surprisal_test'], grila lui u [-0.30, +0.30] cu 13 puncte. Fuziunea de referinta e inghetata din `fusion_preds_lolo_adoptat_temp.csv`.

## Rezultatul pe test, cu u ales LOLO

```
        n  n_ctx     u     r_azi     r_nou     delta      d_lo      d_hi     d_p    latime
lang                                                                                      
ca    445    150 -0.05  0.556579  0.557604  0.001025 -0.001959  0.004116  0.7310  0.034982
de    570    193 -0.10  0.746827  0.732229 -0.014599 -0.021098 -0.008417  0.0000  0.038729
en    570    190 -0.05  0.870037  0.871425  0.001388 -0.000231  0.003185  0.9610  0.035604
es    593    208 -0.05  0.764081  0.765337  0.001257 -0.001123  0.003263  0.8645  0.034513
fil   570    555 -0.05  0.509095  0.509983  0.000889 -0.001150  0.002947  0.8035  0.036814
fr    569    191 -0.05  0.658991  0.655651 -0.003340 -0.005886 -0.000886  0.0035  0.039305
it    570    192 -0.05  0.675010  0.678004  0.002993  0.000575  0.005368  0.9930  0.032139
ja    570    190 -0.05  0.787713  0.790421  0.002709  0.000216  0.005072  0.9865  0.030616
pt    567    562 -0.05  0.845018  0.846405  0.001388 -0.000220  0.002965  0.9515  0.034766
si    600    578 -0.05  0.425137  0.427100  0.001963 -0.001333  0.005095  0.8870  0.033390
```

Media pe limbi: azi **0.683849**, cu C **0.683416**, diferenta **-0.000433**, interval PERECHE [-0.001417, +0.000512], P(>0) = 21.0%.

## Conditia care se citeste INAINTEA mediei

**2 limbi stricate cu interval care exclude zero: ['de', 'fr'].**

Fata de bara de +0.0045: **NU trece**.

## Cat de plat e criteriul

Latimea curbei lui u pe limbile de potrivire, adica r maxim minus r minim peste grila: medie **0.035086**, interval [0.030616, 0.039305]. u ales: {'ca': -0.05, 'de': -0.1, 'en': -0.05, 'es': -0.05, 'fil': -0.05, 'fr': -0.05, 'it': -0.05, 'ja': -0.05, 'pt': -0.05, 'si': -0.05}.

