# Axa regresorului pe semnalul A

Generat de `analysis_regresor.py`. Coloana `p_multi`, splitul test, encoder xlmr, configuratia `--lemma-freq --afeat fert_inloc`, spatiu `e5`.

Toate cifrele vin din predictiile de pe disc. Bratul B nu intra nicaieri: aici se masoara numai A.

## Predictii degenerate

Candidati care dau o predictie CONSTANTA pe o limba, deci `r` nu e definit acolo si standardizarea ar da `inf`. Se trateaza ca zero, adica media limbii, exact conventia lui `fuse_ab.zscore`. Pe limba respectiva ansamblul e deci partenerul SINGUR, si cifrele care il includ trebuie citite cu asta in minte.

```
  lasso-a3e-2      si    1 valoare unica pe si
```

Mecanismul, cand candidatul e `lasso` cu alpha mare: penalizarea L1 zeroeste TOTI coeficientii si ramane doar interceptul. Nu e o eroare numerica, e regresorul care renunta.

## r pe test, per limba

```
        blend   ridge     hgb  extratrees   lasso  elasticnet  ridge-a30  ridge-a100  ridge-a1000  ridge-a3000  ridge-a10000  ridge-a30000  lasso-a1e-4  lasso-a3e-4  lasso-a1e-3  lasso-a3e-3  lasso-a3e-2  pls-k4  pls-k8  pls-k16  pls-k32  pls-k64   huber  bayesridge     ard  krr-rbf  svr-lin
ca     0.4714  0.4358  0.4251      0.4222  0.3711      0.4045     0.4329      0.4339       0.4363       0.4282        0.4094        0.3921       0.4360       0.4434       0.4451       0.4243       0.3043  0.3887  0.3946   0.4365   0.4328   0.4327  0.4258      0.4366  0.3295   0.4245   0.4200
de     0.6230  0.5838  0.6077      0.5967  0.5870      0.6039     0.5842      0.5844       0.5781       0.5642        0.5434        0.5231       0.5918       0.6043       0.6150       0.6115       0.4216  0.5228  0.5570   0.5831   0.5845   0.5843  0.5835      0.5783  0.5846   0.4931   0.5710
en     0.8169  0.7819  0.8113      0.7989  0.7516      0.7776     0.7781      0.7794       0.7859       0.7864        0.7770        0.7561       0.7838       0.7909       0.7982       0.7895       0.6833  0.7671  0.7649   0.7734   0.7774   0.7776  0.7760      0.7855  0.7424   0.7836   0.7619
es     0.7069  0.6908  0.6776      0.6691  0.6491      0.6727     0.6855      0.6873       0.6951       0.6949        0.6882        0.6753       0.6905       0.6999       0.7071       0.6954       0.6036  0.6852  0.6513   0.6857   0.6852   0.6842  0.6904      0.6945  0.6151   0.6878   0.6808
fil    0.4099  0.4097  0.3975      0.4154  0.3909      0.3916     0.4004      0.4032       0.4228       0.4299        0.4080        0.3649       0.3997       0.4002       0.3972       0.3931       0.4185  0.3881  0.4320   0.4112   0.3995   0.3991  0.3995      0.4156  0.3818   0.3883   0.3935
fr     0.5508  0.5329  0.5367      0.5520  0.5677      0.5677     0.5301      0.5312       0.5341       0.5310        0.5240        0.5193       0.5367       0.5430       0.5532       0.5569       0.5376  0.4755  0.5364   0.5309   0.5295   0.5298  0.5317      0.5341  0.5564   0.5052   0.5280
it     0.6283  0.6109  0.6098      0.5971  0.6046      0.6206     0.6112      0.6113       0.6057       0.5919        0.5704        0.5525       0.6174       0.6264       0.6372       0.6312       0.5282  0.5383  0.5661   0.6108   0.6107   0.6105  0.6155      0.6073  0.5857   0.5449   0.6111
ja     0.5609  0.5946  0.3587      0.6036  0.5644      0.5714     0.5921      0.5932       0.5922       0.5776        0.5439        0.5105       0.5964       0.5995       0.5936       0.5815       0.5209  0.4832  0.5807   0.5953   0.5923   0.5913  0.5857      0.5923  0.5552   0.5414   0.5832
pt     0.7657  0.7190  0.7683      0.7665  0.7307      0.7487     0.7153      0.7166       0.7223       0.7230        0.7172        0.7037       0.7259       0.7411       0.7543       0.7569       0.6882  0.6956  0.7098   0.7115   0.7146   0.7145  0.7263      0.7219  0.7238   0.7206   0.7157
si     0.2172  0.1960  0.1793      0.2248  0.1246      0.2098     0.1851      0.1883       0.2112       0.2250        0.2297        0.2237       0.1945       0.2214       0.2581       0.2480          NaN  0.2336  0.2053   0.1912   0.1826   0.1827  0.1860      0.2144  0.1799   0.2296   0.1950
MEDIE  0.5751  0.5555  0.5372      0.5646  0.5342      0.5569     0.5515      0.5529       0.5584       0.5552        0.5411        0.5221       0.5573       0.5670       0.5759       0.5688       0.5229  0.5178  0.5398   0.5530   0.5509   0.5507  0.5520      0.5580  0.5254   0.5319   0.5460
```

Fata de incumbentul `blend` (Ridge300 + HGB), pe medie:

```
  lasso-a1e-3  +0.0008
  lasso-a3e-3  -0.0063
  lasso-a3e-4  -0.0081
  extratrees   -0.0105
  ridge-a1000  -0.0167
  bayesridge   -0.0171
  lasso-a1e-4  -0.0178
  elasticnet   -0.0182
  ridge        -0.0196
  ridge-a3000  -0.0199
  pls-k16      -0.0221
  ridge-a100   -0.0222
  huber        -0.0231
  ridge-a30    -0.0236
  pls-k32      -0.0242
  pls-k64      -0.0244
  svr-lin      -0.0291
  ridge-a10000 -0.0340
  pls-k8       -0.0353
  hgb          -0.0379
  lasso        -0.0409
  krr-rbf      -0.0432
  ard          -0.0497
  lasso-a3e-2  -0.0522
  ridge-a30000 -0.0530
  pls-k4       -0.0573
```

## rho intre estimatori, mediat pe limbi

```
              blend  ridge    hgb  extratrees  lasso  elasticnet  ridge-a30  ridge-a100  ridge-a1000  ridge-a3000  ridge-a10000  ridge-a30000  lasso-a1e-4  lasso-a3e-4  lasso-a1e-3  lasso-a3e-3  lasso-a3e-2  pls-k4  pls-k8  pls-k16  pls-k32  pls-k64  huber  bayesridge    ard  krr-rbf  svr-lin
blend         1.000  0.957  0.936       0.906  0.877       0.914      0.954       0.955        0.957        0.942         0.905         0.864        0.960        0.964        0.957        0.933        0.830   0.861   0.923    0.953    0.953    0.953  0.947       0.957  0.827    0.869    0.926
ridge         0.957  1.000  0.799       0.837  0.838       0.877      0.998       0.999        0.995        0.973         0.924         0.872        0.998        0.991        0.957        0.907        0.802   0.878   0.961    0.997    0.998    0.998  0.983       0.996  0.793    0.892    0.960
hgb           0.936  0.799  1.000       0.884  0.824       0.852      0.794       0.796        0.803        0.799         0.782         0.759        0.805        0.823        0.846        0.857        0.783   0.745   0.775    0.793    0.793    0.793  0.797       0.804  0.776    0.748    0.783
extratrees    0.906  0.837  0.884       1.000  0.910       0.915      0.830       0.832        0.842        0.841         0.826         0.810        0.842        0.860        0.888        0.910        0.882   0.767   0.818    0.829    0.829    0.829  0.829       0.844  0.882    0.784    0.813
lasso         0.877  0.838  0.824       0.910  1.000       0.979      0.834       0.836        0.836        0.823         0.796         0.775        0.849        0.871        0.911        0.955        0.935   0.726   0.804    0.833    0.834    0.834  0.839       0.839  0.953    0.751    0.823
elasticnet    0.914  0.877  0.852       0.915  0.979       1.000      0.872       0.874        0.880        0.873         0.850         0.829        0.887        0.911        0.951        0.991        0.910   0.792   0.846    0.872    0.871    0.871  0.876       0.883  0.932    0.800    0.860
ridge-a30     0.954  0.998  0.794       0.830  0.834       0.872      1.000       1.000        0.988        0.959         0.904         0.849        0.998        0.988        0.950        0.900        0.799   0.856   0.948    0.996    1.000    1.000  0.985       0.990  0.794    0.877    0.963
ridge-a100    0.955  0.999  0.796       0.832  0.836       0.874      1.000       1.000        0.991        0.964         0.910         0.856        0.998        0.989        0.952        0.902        0.800   0.862   0.952    0.996    1.000    1.000  0.985       0.992  0.794    0.881    0.962
ridge-a1000   0.957  0.995  0.803       0.842  0.836       0.880      0.988       0.991        1.000        0.990         0.954         0.908        0.991        0.989        0.962        0.912        0.802   0.912   0.977    0.990    0.987    0.987  0.972       1.000  0.786    0.912    0.950
ridge-a3000   0.942  0.973  0.799       0.841  0.823       0.873      0.959       0.964        0.990        1.000         0.985         0.952        0.965        0.970        0.954        0.906        0.790   0.951   0.982    0.964    0.957    0.957  0.942       0.988  0.765    0.928    0.921
ridge-a10000  0.905  0.924  0.782       0.826  0.796       0.850      0.904       0.910        0.954        0.985         1.000         0.989        0.913        0.925        0.924        0.884        0.764   0.975   0.954    0.909    0.901    0.901  0.886       0.950  0.731    0.924    0.868
ridge-a30000  0.864  0.872  0.759       0.810  0.775       0.829      0.849       0.856        0.908        0.952         0.989         1.000        0.860        0.875        0.886        0.858        0.744   0.962   0.907    0.854    0.846    0.846  0.832       0.903  0.704    0.901    0.816
lasso-a1e-4   0.960  0.998  0.805       0.842  0.849       0.887      0.998       0.998        0.991        0.965         0.913         0.860        1.000        0.995        0.963        0.915        0.810   0.867   0.953    0.996    0.998    0.998  0.985       0.992  0.808    0.882    0.963
lasso-a3e-4   0.964  0.991  0.823       0.860  0.871       0.911      0.988       0.989        0.989        0.970         0.925         0.875        0.995        1.000        0.981        0.939        0.827   0.881   0.956    0.987    0.987    0.987  0.978       0.990  0.828    0.887    0.957
lasso-a1e-3   0.957  0.957  0.846       0.888  0.911       0.951      0.950       0.952        0.962        0.954         0.924         0.886        0.963        0.981        1.000        0.977        0.857   0.883   0.934    0.951    0.949    0.949  0.946       0.963  0.867    0.875    0.926
lasso-a3e-3   0.933  0.907  0.857       0.910  0.955       0.991      0.900       0.902        0.912        0.906         0.884         0.858        0.915        0.939        0.977        1.000        0.891   0.835   0.879    0.900    0.899    0.899  0.903       0.914  0.911    0.831    0.886
lasso-a3e-2   0.830  0.802  0.783       0.882  0.935       0.910      0.799       0.800        0.802        0.790         0.764         0.744        0.810        0.827        0.857        0.891        1.000   0.690   0.787    0.798    0.799    0.799  0.801       0.803  0.910    0.728    0.785
pls-k4        0.861  0.878  0.745       0.767  0.726       0.792      0.856       0.862        0.912        0.951         0.975         0.962        0.867        0.881        0.883        0.835        0.690   1.000   0.910    0.861    0.853    0.852  0.841       0.907  0.661    0.896    0.824
pls-k8        0.923  0.961  0.775       0.818  0.804       0.846      0.948       0.952        0.977        0.982         0.954         0.907        0.953        0.956        0.934        0.879        0.787   0.910   1.000    0.953    0.946    0.945  0.927       0.975  0.756    0.903    0.905
pls-k16       0.953  0.997  0.793       0.829  0.833       0.872      0.996       0.996        0.990        0.964         0.909         0.854        0.996        0.987        0.951        0.900        0.798   0.861   0.953    1.000    0.995    0.995  0.980       0.992  0.789    0.882    0.958
pls-k32       0.953  0.998  0.793       0.829  0.834       0.871      1.000       1.000        0.987        0.957         0.901         0.846        0.998        0.987        0.949        0.899        0.799   0.853   0.946    0.995    1.000    1.000  0.985       0.989  0.795    0.875    0.963
pls-k64       0.953  0.998  0.793       0.829  0.834       0.871      1.000       1.000        0.987        0.957         0.901         0.846        0.998        0.987        0.949        0.899        0.799   0.852   0.945    0.995    1.000    1.000  0.986       0.988  0.794    0.874    0.963
huber         0.947  0.983  0.797       0.829  0.839       0.876      0.985       0.985        0.972        0.942         0.886         0.832        0.985        0.978        0.946        0.903        0.801   0.841   0.927    0.980    0.985    0.986  1.000       0.973  0.799    0.856    0.984
bayesridge    0.957  0.996  0.804       0.844  0.839       0.883      0.990       0.992        1.000        0.988         0.950         0.903        0.992        0.990        0.963        0.914        0.803   0.907   0.975    0.992    0.989    0.988  0.973       1.000  0.790    0.908    0.951
ard           0.827  0.793  0.776       0.882  0.953       0.932      0.794       0.794        0.786        0.765         0.731         0.704        0.808        0.828        0.867        0.911        0.910   0.661   0.756    0.789    0.795    0.794  0.799       0.790  1.000    0.693    0.789
krr-rbf       0.869  0.892  0.748       0.784  0.751       0.800      0.877       0.881        0.912        0.928         0.924         0.901        0.882        0.887        0.875        0.831        0.728   0.896   0.903    0.882    0.875    0.874  0.856       0.908  0.693    1.000    0.836
svr-lin       0.926  0.960  0.783       0.813  0.823       0.860      0.963       0.962        0.950        0.921         0.868         0.816        0.963        0.957        0.926        0.886        0.785   0.824   0.905    0.958    0.963    0.963  0.984       0.951  0.789    0.836    1.000
```

## r al mediei standardizate, pe toate submultimile estimatorilor de baza

`blend` si `blend-et` sunt excluse din combinatii: sunt ele insele medii, deci ar intra de doua ori.

Enumerate submultimile de pana la **3** membri (2951 din 67108863 posibile). Motivul e cost, dar si sens: cu grila de alpha pe disc, combinatiile mari sunt in majoritate doua puncte ale ACELEIASI familii puse impreuna, ceea ce nu e un ansamblu de biasuri diferite.

```
  extratrees+lasso-a1e-3                   0.584520
  ridge+extratrees+lasso-a1e-3             0.583724
  extratrees+lasso-a3e-4                   0.583708
  ridge+extratrees+lasso-a3e-3             0.582943
  extratrees+ridge-a1000                   0.582070
  extratrees+bayesridge                    0.581856
  ridge+extratrees                         0.581234
  extratrees+lasso-a1e-4                   0.581220
  hgb+extratrees+lasso-a3e-4               0.581022
  extratrees+pls-k16                       0.581019
```

Calculate toate **2951** submultimile, listate primele 10. Cea mai slaba e `lasso+lasso-a3e-2` la 0.516658.

Identitatea de frontiera, verificata pe fiecare limba pentru `ridge+hgb`: eroarea maxima **2.22e-16**. Nu e o aproximare buna, e o identitate algebrica.

## Ce i-ar trebui unui al treilea estimator. Scris inainte de a-l cauta

Blend-ul de acum, prin frontiera: r_ridge 0.5555, r_hgb 0.5372, rho 0.7993, deci **0.576030**.

Bara pe fuziune e +0.0045, iar factorul de transmisie A -> fuziune e 0.259 mediu si 0.091 marginal (`e_frontiera_enc.md`). Deci blend-ul trebuie sa urce cu +0.0174 (optimist) pana la +0.0495 (pesimist).

rho mediu MAXIM admis fata de `ridge` si `hgb`:

```
    r3    rho max optimist    rho max pesimist
 0.350               0.328               0.180
 0.400               0.432               0.274
 0.450               0.540               0.371
 0.500               0.651               0.471
 0.550               0.766               0.575
 0.580               0.837               0.638
 0.620               0.933               0.725
 0.650               orice               0.791
```

Candidatii masurati, rho mediu fata de cei doi membri:

```
  extratrees   r 0.5646  rho 0.860  prag optimist 0.801  ->  CADE
  lasso        r 0.5342  rho 0.831  prag optimist 0.730  ->  CADE
  elasticnet   r 0.5569  rho 0.865  prag optimist 0.782  ->  CADE
  ridge-a30    r 0.5515  rho 0.896  prag optimist 0.770  ->  CADE
  ridge-a100   r 0.5529  rho 0.897  prag optimist 0.773  ->  CADE
  ridge-a1000  r 0.5584  rho 0.899  prag optimist 0.786  ->  CADE
  ridge-a3000  r 0.5552  rho 0.886  prag optimist 0.778  ->  CADE
  ridge-a10000 r 0.5411  rho 0.853  prag optimist 0.746  ->  CADE
  ridge-a30000 r 0.5221  rho 0.816  prag optimist 0.702  ->  CADE
  lasso-a1e-4  r 0.5573  rho 0.902  prag optimist 0.783  ->  CADE
  lasso-a3e-4  r 0.5670  rho 0.907  prag optimist 0.806  ->  CADE
  lasso-a1e-3  r 0.5759  rho 0.902  prag optimist 0.827  ->  CADE
  lasso-a3e-3  r 0.5688  rho 0.882  prag optimist 0.810  ->  CADE
  lasso-a3e-2  r 0.5229  rho 0.793  prag optimist 0.704  ->  CADE
  pls-k4       r 0.5178  rho 0.812  prag optimist 0.692  ->  CADE
  pls-k8       r 0.5398  rho 0.868  prag optimist 0.743  ->  CADE
  pls-k16      r 0.5530  rho 0.895  prag optimist 0.773  ->  CADE
  pls-k32      r 0.5509  rho 0.896  prag optimist 0.768  ->  CADE
  pls-k64      r 0.5507  rho 0.895  prag optimist 0.768  ->  CADE
  huber        r 0.5520  rho 0.890  prag optimist 0.771  ->  CADE
  bayesridge   r 0.5580  rho 0.900  prag optimist 0.785  ->  CADE
  ard          r 0.5254  rho 0.784  prag optimist 0.709  ->  CADE
  krr-rbf      r 0.5319  rho 0.820  prag optimist 0.724  ->  CADE
  svr-lin      r 0.5460  rho 0.872  prag optimist 0.757  ->  CADE
```

## Inlocuirea jumatatii liniare a blend-ului

Controlul e `ridge+hgb` = **0.571931**, adica blend-ul de acum scris ca media standardizata a celor doua jumatati ale lui. Fiecare candidat X e pus in locul lui `ridge`, cu ACELASI partener `hgb`, deci diferenta e a jumatatii liniare si a nimic altceva.

De ce 0.571931 aici si 0.576030 la punctul 4, pentru acelasi `ridge+hgb`. Identitatea de frontiera e exacta PE LIMBA, si asta s-a verificat mai sus la ordinul 1e-16. Punctul 4 o aplica insa pe `r` si `rho` deja MEDIATE peste limbi, ca sa poata desena o curba de prag cu un singur numar, iar media unei functii neliniare nu e functia mediei: iese cu +0.0041 pe langa. Cifra care se compara cu punctul 3 si intre candidati e cea de aici, media celor zece r pe limba. Cea de la punctul 4 ramane buna pentru ce face ea, curba de prag, fiindca acolo conteaza diferenta fata de ea insasi, nu nivelul.

`castig fuziune` e diferenta pe A inmultita cu factorul de transmisie (0.259 mediu, 0.091 marginal). Verdictul e fata de bara de +0.0045 pe fuziune, luata pe estimarea OPTIMISTA, deci un `CADE` e un cade si pe cea mai buna ipoteza.

```
  candidat             r_A  rho(X,hgb)   r(X+hgb)   delta_A   fuz.opt   fuz.pes  verdict
  lasso-a1e-3       0.5759       0.846   0.576235   +0.0043   +0.0011   +0.0004  CADE
  lasso-a3e-4       0.5670       0.823   0.574680   +0.0027   +0.0007   +0.0003  CADE
  ridge-a1000       0.5584       0.803   0.572984   +0.0011   +0.0003   +0.0001  CADE
  bayesridge        0.5580       0.804   0.572767   +0.0008   +0.0002   +0.0001  CADE
  ridge-a3000       0.5552       0.799   0.572006   +0.0001   +0.0000   +0.0000  CADE
  lasso-a1e-4       0.5573       0.805   0.571896   -0.0000   -0.0000   -0.0000  CADE
  pls-k16           0.5530       0.793   0.571572   -0.0004   -0.0001   -0.0000  CADE
  lasso-a3e-3       0.5688       0.857   0.571158   -0.0008   -0.0002   -0.0001  CADE
  ridge-a100        0.5529       0.796   0.570992   -0.0009   -0.0002   -0.0001  CADE
  huber             0.5520       0.797   0.570538   -0.0014   -0.0004   -0.0001  CADE
  ridge-a30         0.5515       0.794   0.570516   -0.0014   -0.0004   -0.0001  CADE
  pls-k32           0.5509       0.793   0.570255   -0.0017   -0.0004   -0.0002  CADE
  pls-k64           0.5507       0.793   0.570217   -0.0017   -0.0004   -0.0002  CADE
  svr-lin           0.5460       0.783   0.569666   -0.0023   -0.0006   -0.0002  CADE
  krr-rbf           0.5319       0.748   0.567603   -0.0043   -0.0011   -0.0004  CADE
  pls-k8            0.5398       0.775   0.567465   -0.0045   -0.0012   -0.0004  CADE
  ridge-a10000      0.5411       0.782   0.567123   -0.0048   -0.0012   -0.0004  CADE
  elasticnet        0.5569       0.852   0.565667   -0.0063   -0.0016   -0.0006  CADE
  extratrees        0.5646       0.884   0.564449   -0.0075   -0.0019   -0.0007  CADE
  pls-k4            0.5178       0.745   0.560615   -0.0113   -0.0029   -0.0010  CADE
  ridge-a30000      0.5221       0.759   0.560267   -0.0117   -0.0030   -0.0011  CADE
  ard               0.5254       0.776   0.558395   -0.0135   -0.0035   -0.0012  CADE
  lasso             0.5342       0.824   0.556825   -0.0151   -0.0039   -0.0014  CADE
  lasso-a3e-2       0.5229       0.783   0.540305   -0.0316   -0.0082   -0.0029  CADE
```

Ca sa treaca bara, un candidat trebuie sa urce A cu +0.0174 (optimist) pana la +0.0495 (pesimist). Cifra care decide e `rho`, nu `r`: un candidat cu r mai bun dar rho mai mare pierde, si s-a intamplat de trei ori in proiect.

## Grila `ridge (alpha)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  ridge-a30              30   0.5515
  ridge-a100            100   0.5529
  ridge                 300   0.5555
  ridge-a1000          1000   0.5584   <- cel mai bun pe test
  ridge-a3000          3000   0.5552
  ridge-a10000        10000   0.5411
  ridge-a30000        30000   0.5221
```

```
  selectie LOLO                0.558377
  media predictiilor grilei    0.558975
  cel mai bun punct fix        0.558377   (ridge-a1000, dar e ales PE TEST)
  latimea criteriului          0.0362
  LOLO a nimerit optimul       3/10 limbi
```

Punctul ales per limba: ca=ridge-a1000, de=ridge-a1000, en=ridge-a1000, es=ridge-a1000, fil=ridge-a1000, fr=ridge-a1000, it=ridge-a1000, ja=ridge-a1000, pt=ridge-a1000, si=ridge-a1000.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `ridge-a1000`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

## Grila `lasso (alpha)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  lasso-a1e-4        0.0001   0.5573
  lasso-a3e-4        0.0003   0.5670
  lasso-a1e-3         0.001   0.5759   <- cel mai bun pe test
  lasso-a3e-3         0.003   0.5688
  lasso                0.01   0.5342
  lasso-a3e-2          0.03   0.5229
```

```
  selectie LOLO                0.575911
  media predictiilor grilei    0.569479
  cel mai bun punct fix        0.575911   (lasso-a1e-3, dar e ales PE TEST)
  latimea criteriului          0.0474
  LOLO a nimerit optimul       6/10 limbi
```

Punctul ales per limba: ca=lasso-a1e-3, de=lasso-a1e-3, en=lasso-a1e-3, es=lasso-a1e-3, fil=lasso-a1e-3, fr=lasso-a1e-3, it=lasso-a1e-3, ja=lasso-a1e-3, pt=lasso-a1e-3, si=lasso-a1e-3.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `lasso-a1e-3`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

Medierea grilei iese cu -0.006431 sub punctul unic, ceea ce e de asteptat: grila contine si puncte clar proaste, iar medierea le tine pe toate cu pondere egala. Medierea e raspunsul cand nu se poate ALEGE, nu cand se poate.

## Grila `pls (k)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  pls-k4                  4   0.5178
  pls-k8                  8   0.5398
  pls-k16                16   0.5530   <- cel mai bun pe test
  pls-k32                32   0.5509
  pls-k64                64   0.5507
```

```
  selectie LOLO                0.552959
  media predictiilor grilei    0.556906
  cel mai bun punct fix        0.552959   (pls-k16, dar e ales PE TEST)
  latimea criteriului          0.0351
  LOLO a nimerit optimul       4/10 limbi
```

Punctul ales per limba: ca=pls-k16, de=pls-k16, en=pls-k16, es=pls-k16, fil=pls-k16, fr=pls-k16, it=pls-k16, ja=pls-k16, pt=pls-k16, si=pls-k16.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `pls-k16`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

