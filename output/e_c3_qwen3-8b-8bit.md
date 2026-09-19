# Semnalul C ca al treilea termen: `qwen3-8b-8bit`

Generat de `analysis_c_fuse.py`, directoare ['bakeoff_test_Text', 'surprisal_test'], grila lui u [-0.30, +0.30] cu 13 puncte. Fuziunea de referinta e inghetata din `fusion_preds_lolo_adoptat_temp.csv`.

## Rezultatul pe test, cu u ales LOLO

```
        n  n_ctx     u     r_azi     r_nou     delta      d_lo      d_hi     d_p    latime
lang                                                                                      
ca    445    150  0.05  0.556579  0.556398 -0.000181 -0.004160  0.003611  0.4645  0.040648
de    570    193 -0.00  0.746827  0.746827  0.000000  0.000000  0.000000  0.0000  0.044536
en    570    190  0.05  0.870037  0.869539 -0.000497 -0.002818  0.001684  0.3395  0.036834
es    593    208  0.05  0.764081  0.763949 -0.000132 -0.002500  0.002310  0.4440  0.038653
fil   570    555  0.05  0.509095  0.502080 -0.007015 -0.010981 -0.003096  0.0000  0.037161
fr    569    191  0.05  0.658991  0.657868 -0.001123 -0.004373  0.002246  0.2615  0.039033
it    570    192  0.05  0.675010  0.676121  0.001111 -0.001573  0.003900  0.8065  0.040918
ja    570    190  0.05  0.787713  0.787777  0.000064 -0.002524  0.002434  0.5230  0.038331
pt    567    562  0.05  0.845018  0.845233  0.000215 -0.002130  0.002544  0.5805  0.038291
si    600    578 -0.00  0.425137  0.425137  0.000000  0.000000  0.000000  0.0000  0.045710
```

Media pe limbi: azi **0.683849**, cu C **0.683093**, diferenta **-0.000756**, interval PERECHE [-0.001585, +0.000042], P(>0) = 3.0%.

## Conditia care se citeste INAINTEA mediei

**1 limbi stricate cu interval care exclude zero: ['fil'].**

Fata de bara de +0.0045: **NU trece**.

## Cat de plat e criteriul

Latimea curbei lui u pe limbile de potrivire, adica r maxim minus r minim peste grila: medie **0.040011**, interval [0.036834, 0.045710]. u ales: {'ca': 0.05, 'de': -0.0, 'en': 0.05, 'es': 0.05, 'fil': 0.05, 'fr': 0.05, 'it': 0.05, 'ja': 0.05, 'pt': 0.05, 'si': -0.0}.

