# Axa regresorului pe semnalul A

Generat de `analysis_regresor.py`. Coloana `p_multi`, splitul test, encoder xlmr, configuratia `--lemma-freq --afeat fert_inloc`, spatiu `tf-proj-394`.

Toate cifrele vin din predictiile de pe disc. Bratul B nu intra nicaieri: aici se masoara numai A.

## r pe test, per limba

```
        blend   ridge     hgb   tabfm
ca     0.4280  0.4136  0.3824  0.3965
de     0.6505  0.6253  0.6206  0.6577
en     0.8249  0.7952  0.8120  0.8184
es     0.6774  0.6575  0.6611  0.6463
fil    0.4178  0.3939  0.4349  0.3840
fr     0.5313  0.4931  0.5360  0.5390
it     0.6245  0.6122  0.6038  0.5665
ja     0.6062  0.6341  0.3885  0.5952
pt     0.7724  0.7448  0.7596  0.7501
si     0.2158  0.2576  0.1275  0.1873
MEDIE  0.5749  0.5627  0.5326  0.5541
```

Fata de incumbentul `blend` (Ridge300 + HGB), pe medie:

```
  ridge        -0.0121
  tabfm        -0.0208
  hgb          -0.0422
```

## rho intre estimatori, mediat pe limbi

```
       blend  ridge    hgb  tabfm
blend  1.000  0.958  0.944  0.909
ridge  0.958  1.000  0.815  0.877
hgb    0.944  0.815  1.000  0.851
tabfm  0.909  0.877  0.851  1.000
```

## r al mediei standardizate, pe toate submultimile estimatorilor de baza

`blend` si `blend-et` sunt excluse din combinatii: sunt ele insele medii, deci ar intra de doua ori.

```
  ridge+hgb+tabfm                    0.576436
  ridge+tabfm                        0.574716
  ridge+hgb                          0.571835
  ridge                              0.562733
  hgb+tabfm                          0.560798
  tabfm                              0.554091
  hgb                                0.532643
```

Identitatea de frontiera, verificata pe fiecare limba pentru `ridge+hgb`: eroarea maxima **2.22e-16**. Nu e o aproximare buna, e o identitate algebrica.

## Ce i-ar trebui unui al treilea estimator. Scris inainte de a-l cauta

Blend-ul de acum, prin frontiera: r_ridge 0.5627, r_hgb 0.5326, rho 0.8152, deci **0.574891**.

Bara pe fuziune e +0.0045, iar factorul de transmisie A -> fuziune e 0.259 mediu si 0.091 marginal (`e_frontiera_enc.md`). Deci blend-ul trebuie sa urce cu +0.0174 (optimist) pana la +0.0495 (pesimist).

rho mediu MAXIM admis fata de `ridge` si `hgb`:

```
    r3    rho max optimist    rho max pesimist
 0.350               0.331               0.182
 0.400               0.436               0.277
 0.450               0.544               0.374
 0.500               0.656               0.475
 0.550               0.772               0.579
 0.580               0.843               0.643
 0.620               0.940               0.730
 0.650               orice               0.796
```

Candidatii masurati, rho mediu fata de cei doi membri:

```
  tabfm        r 0.5541  rho 0.864  prag optimist 0.781  ->  CADE
```

