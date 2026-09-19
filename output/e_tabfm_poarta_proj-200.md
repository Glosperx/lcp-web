# Poarta de frontiera pentru TabFM

Generat de `analysis_tabfm_poarta.py`, spatiu `tf-proj-200`, 10/10 limbi gata. Citit direct din `data/tabfm_preds_proj200`.

```
           n  r_tabfm  r_ridge  rho_ridge   r_hgb  rho_hgb  r_blend    ens3    ens2
lang                                                                               
ca     445.0   0.3953   0.4077     0.8869  0.3979   0.8202   0.4289  0.4261  0.4288
de     570.0   0.5869   0.6235     0.8106  0.6212   0.8663   0.6463  0.6450  0.6463
en     570.0   0.7741   0.7825     0.9208  0.8161   0.9138   0.8145  0.8128  0.8145
es     593.0   0.6877   0.6701     0.8920  0.6686   0.9428   0.6850  0.6957  0.6854
fil    570.0   0.3665   0.4084     0.9488  0.4282   0.9250   0.4224  0.4093  0.4240
fr     569.0   0.4870   0.5297     0.8655  0.5400   0.9246   0.5486  0.5376  0.5484
it     570.0   0.5421   0.6213     0.8231  0.6083   0.8399   0.6292  0.6210  0.6296
ja     570.0   0.5443   0.6192     0.7738  0.3987   0.3956   0.5948  0.6113  0.5697
pt     567.0   0.7334   0.7429     0.8693  0.7566   0.9072   0.7656  0.7707  0.7651
si     600.0   0.0049   0.2075     0.5979  0.0877   0.6624   0.1619  0.1164  0.1668
MEDIE  562.4   0.5122   0.5613     0.8389  0.5323   0.8198   0.5697  0.5646  0.5678
```

TabFM singur: **0.512234**, fata de ridge 0.561288 si hgb 0.532335 pe acelasi spatiu.

rho mediu fata de cei doi membri: **0.8293**. Pentru scara, rho(ridge, hgb) e 0.811 si membrii encoderelor stau la 0.846-0.887.

Blend de doi (ridge+hgb): 0.567845. Cu TabFM ca al treilea: **0.564577**, adica **-0.003267**.

Bara ceruta pe brat, ca fuziunea sa urce cu +0.0045: +0.0174 (optimist) pana la +0.0495 (pesimist).

**VERDICT: CADE** chiar si la factorul optimist de transmisie.

