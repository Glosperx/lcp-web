# Semnalul C ca al treilea termen: `dezacord`

Generat de `analysis_c_fuse.py`, directoare ['bakeoff_test_Text', 'surprisal_test'], grila lui u [-0.30, +0.30] cu 13 puncte. Fuziunea de referinta e inghetata din `fusion_preds_lolo_adoptat_temp.csv`.

## Rezultatul pe test, cu u ales LOLO

```
        n  n_ctx    u     r_azi     r_nou  delta  d_lo  d_hi  d_p    latime
lang                                                                       
ca    445    150 -0.0  0.556579  0.556579    0.0   0.0   0.0  0.0  0.063614
de    570    193 -0.0  0.746827  0.746827    0.0   0.0   0.0  0.0  0.055094
en    570    190 -0.0  0.870037  0.870037    0.0   0.0   0.0  0.0  0.056477
es    593    208 -0.0  0.764081  0.764081    0.0   0.0   0.0  0.0  0.061181
fil   570    555 -0.0  0.509095  0.509095    0.0   0.0   0.0  0.0  0.064904
fr    569    191 -0.0  0.658991  0.658991    0.0   0.0   0.0  0.0  0.060519
it    570    192 -0.0  0.675010  0.675010    0.0   0.0   0.0  0.0  0.059338
ja    570    190 -0.0  0.787713  0.787713    0.0   0.0   0.0  0.0  0.058947
pt    567    562 -0.0  0.845018  0.845018    0.0   0.0   0.0  0.0  0.059801
si    600    578 -0.0  0.425137  0.425137    0.0   0.0   0.0  0.0  0.064137
```

Media pe limbi: azi **0.683849**, cu C **0.683849**, diferenta **+0.000000**, interval PERECHE [+0.000000, +0.000000], P(>0) = 0.0%.

## Conditia care se citeste INAINTEA mediei

**Nicio limba stricata cu interval care exclude zero.**

Fata de bara de +0.0045: **NU trece**.

## Cat de plat e criteriul

Latimea curbei lui u pe limbile de potrivire, adica r maxim minus r minim peste grila: medie **0.060401**, interval [0.055094, 0.064904]. u ales: {'ca': -0.0, 'de': -0.0, 'en': -0.0, 'es': -0.0, 'fil': -0.0, 'fr': -0.0, 'it': -0.0, 'ja': -0.0, 'pt': -0.0, 'si': -0.0}.

