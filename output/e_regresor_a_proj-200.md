# Axa regresorului pe semnalul A

Generat de `analysis_regresor.py`. Coloana `p_multi`, splitul test, encoder xlmr, configuratia `--lemma-freq --afeat fert_inloc`, spatiu `tf-proj-200`.

Toate cifrele vin din predictiile de pe disc. Bratul B nu intra nicaieri: aici se masoara numai A.

## r pe test, per limba

```
        blend   ridge     hgb   tabfm
ca     0.4289  0.4077  0.3979  0.3953
de     0.6463  0.6235  0.6212  0.5869
en     0.8145  0.7825  0.8161  0.7741
es     0.6850  0.6701  0.6686  0.6877
fil    0.4224  0.4084  0.4282  0.3665
fr     0.5486  0.5297  0.5400  0.4870
it     0.6292  0.6213  0.6083  0.5421
ja     0.5948  0.6192  0.3987  0.5443
pt     0.7656  0.7429  0.7566  0.7334
si     0.1619  0.2075  0.0877  0.0049
MEDIE  0.5697  0.5613  0.5323  0.5122
```

Fata de incumbentul `blend` (Ridge300 + HGB), pe medie:

```
  ridge        -0.0084
  hgb          -0.0374
  tabfm        -0.0575
```

## rho intre estimatori, mediat pe limbi

```
       blend  ridge    hgb  tabfm
blend  1.000  0.958  0.952  0.870
ridge  0.958  1.000  0.829  0.839
hgb    0.952  0.829  1.000  0.820
tabfm  0.870  0.839  0.820  1.000
```

## r al mediei standardizate, pe toate submultimile estimatorilor de baza

`blend` si `blend-et` sunt excluse din combinatii: sunt ele insele medii, deci ar intra de doua ori.

```
  ridge+hgb                          0.567845
  ridge+hgb+tabfm                    0.564577
  ridge                              0.561288
  ridge+tabfm                        0.556991
  hgb+tabfm                          0.544833
  hgb                                0.532335
  tabfm                              0.512234
```

Identitatea de frontiera, verificata pe fiecare limba pentru `ridge+hgb`: eroarea maxima **2.22e-16**. Nu e o aproximare buna, e o identitate algebrica.

## Ce i-ar trebui unui al treilea estimator. Scris inainte de a-l cauta

Blend-ul de acum, prin frontiera: r_ridge 0.5613, r_hgb 0.5323, rho 0.8292, deci **0.571770**.

Bara pe fuziune e +0.0045, iar factorul de transmisie A -> fuziune e 0.259 mediu si 0.091 marginal (`e_frontiera_enc.md`). Deci blend-ul trebuie sa urce cu +0.0174 (optimist) pana la +0.0495 (pesimist).

rho mediu MAXIM admis fata de `ridge` si `hgb`:

```
    r3    rho max optimist    rho max pesimist
 0.350               0.336               0.185
 0.400               0.442               0.281
 0.450               0.552               0.379
 0.500               0.665               0.481
 0.550               0.781               0.585
 0.580               0.853               0.650
 0.620               0.950               0.738
 0.650               orice               0.805
```

Candidatii masurati, rho mediu fata de cei doi membri:

```
  tabfm        r 0.5122  rho 0.829  prag optimist 0.693  ->  CADE
```

