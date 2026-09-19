# Semnalul C ca al treilea termen: `qwen3-8b-4bit`

Generat de `analysis_c_fuse.py`, directoare ['bakeoff_test_Text', 'surprisal_test'], grila lui u [-0.30, +0.30] cu 13 puncte. Fuziunea de referinta e inghetata din `fusion_preds_lolo_adoptat_temp.csv`.

## Rezultatul pe test, cu u ales LOLO

```
        n  n_ctx     u     r_azi     r_nou     delta      d_lo      d_hi     d_p    latime
lang                                                                                      
ca    445    150  0.05  0.556579  0.556988  0.000410 -0.003412  0.004275  0.5955  0.042546
de    570    193 -0.00  0.746827  0.746827  0.000000  0.000000  0.000000  0.0000  0.046051
en    570    190  0.05  0.870037  0.869595 -0.000442 -0.002727  0.001671  0.3505  0.038312
es    593    208  0.05  0.764081  0.764434  0.000354 -0.002032  0.002880  0.6015  0.040443
fil   570    555  0.05  0.509095  0.501786 -0.007308 -0.011196 -0.003476  0.0000  0.038411
fr    569    191  0.05  0.658991  0.657842 -0.001150 -0.004206  0.002057  0.2400  0.040368
it    570    192  0.05  0.675010  0.676074  0.001064 -0.001641  0.003717  0.7935  0.042205
ja    570    190  0.05  0.787713  0.787801  0.000089 -0.002512  0.002394  0.5340  0.039690
pt    567    562  0.05  0.845018  0.845220  0.000202 -0.002188  0.002453  0.5690  0.039803
si    600    578  0.05  0.425137  0.428290  0.003153 -0.000725  0.006793  0.9470  0.045435
```

Media pe limbi: azi **0.683849**, cu C **0.683486**, diferenta **-0.000363**, interval PERECHE [-0.001264, +0.000517], P(>0) = 21.0%.

## Conditia care se citeste INAINTEA mediei

**1 limbi stricate cu interval care exclude zero: ['fil'].**

Fata de bara de +0.0045: **NU trece**.

## Cat de plat e criteriul

Latimea curbei lui u pe limbile de potrivire, adica r maxim minus r minim peste grila: medie **0.041326**, interval [0.038312, 0.046051]. u ales: {'ca': 0.05, 'de': -0.0, 'en': 0.05, 'es': 0.05, 'fil': 0.05, 'fr': 0.05, 'it': 0.05, 'ja': 0.05, 'pt': 0.05, 'si': 0.05}.

## Podeaua de zgomot

Aceeasi grila si acelasi criteriu, cu C inlocuit de o coloana aleatoare. Spune cat scoate procedura cand semnalul nu contine nimic.

```
samanta   delta pe medie   u ales
1         +0.000000        [-0.0]
2         +0.000000        [-0.0]
3         -0.000699        [-0.0, 0.05]
4         +0.000000        [-0.0]
5         +0.000000        [-0.0]
```

Podeaua: medie **-0.000140**, maxim **+0.000000** pe 5 seminte. Castigul peste podea al candidatului: **-0.000223**.

