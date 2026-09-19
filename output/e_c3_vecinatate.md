# Semnalul C ca al treilea termen: `vecinatate`

Generat de `analysis_c_fuse.py`, directoare ['bakeoff_test_Text', 'surprisal_test'], grila lui u [-0.30, +0.30] cu 13 puncte. Fuziunea de referinta e inghetata din `fusion_preds_lolo_adoptat_temp.csv`.

## Rezultatul pe test, cu u ales LOLO

```
        n  n_ctx     u     r_azi     r_nou     delta      d_lo      d_hi     d_p    latime
lang                                                                                      
ca    445    150 -0.05  0.556579  0.556769  0.000190 -0.003210  0.003665  0.5665  0.051515
de    570    193 -0.00  0.746827  0.746827  0.000000  0.000000  0.000000  0.0000  0.046471
en    570    190 -0.05  0.870037  0.868642 -0.001395 -0.003458  0.000549  0.0800  0.050851
es    593    208 -0.05  0.764081  0.763999 -0.000082 -0.002288  0.002177  0.4865  0.050503
fil   570    555 -0.05  0.509095  0.507775 -0.001320 -0.003972  0.001103  0.1365  0.054513
fr    569    191 -0.00  0.658991  0.658991  0.000000  0.000000  0.000000  0.0000  0.049033
it    570    192 -0.00  0.675010  0.675010  0.000000  0.000000  0.000000  0.0000  0.049981
ja    570    190 -0.05  0.787713  0.786761 -0.000952 -0.003426  0.001373  0.2005  0.050894
pt    567    562 -0.05  0.845018  0.845881  0.000863 -0.001430  0.003020  0.7690  0.050831
si    600    578 -0.05  0.425137  0.418911 -0.006226 -0.009020 -0.003251  0.0000  0.059309
```

Media pe limbi: azi **0.683849**, cu C **0.682957**, diferenta **-0.000892**, interval PERECHE [-0.001587, -0.000202], P(>0) = 0.7%.

## Conditia care se citeste INAINTEA mediei

**1 limbi stricate cu interval care exclude zero: ['si'].**

Fata de bara de +0.0045: **NU trece**.

## Cat de plat e criteriul

Latimea curbei lui u pe limbile de potrivire, adica r maxim minus r minim peste grila: medie **0.051390**, interval [0.046471, 0.059309]. u ales: {'ca': -0.05, 'de': -0.0, 'en': -0.05, 'es': -0.05, 'fil': -0.05, 'fr': -0.0, 'it': -0.0, 'ja': -0.05, 'pt': -0.05, 'si': -0.05}.

