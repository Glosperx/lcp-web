# Axa regresorului pe semnalul A

Generat de `analysis_regresor.py`. Coloana `p_multi`, splitul test, encoder xlmr, configuratia `--lemma-freq --afeat fert_inloc`, embedding plin.

Toate cifrele vin din predictiile de pe disc. Bratul B nu intra nicaieri: aici se masoara numai A.

## r pe test, per limba

```
        blend  blend-lasso   ridge     hgb  hgb-adanc  extratrees  blend-et   lasso  elasticnet  ridge-a30  ridge-a100  ridge-a1000  ridge-a3000  ridge-a10000  ridge-a30000  lasso-a1e-4  lasso-a3e-4  lasso-a1e-3  lasso-a3e-3  lasso-a3e-2  pls-k4  pls-k8  pls-k16  pls-k32  pls-k64   huber  bayesridge     ard  krr-rbf  svr-lin
ca     0.4426       0.4330  0.4167  0.4097     0.3948      0.4005    0.4277  0.3717      0.3776     0.4140      0.4150       0.4173       0.4116        0.3955        0.3741       0.4132       0.4140       0.4094       0.3888       0.2890  0.3851  0.3945   0.4154   0.4149   0.4133  0.3973      0.4175  0.3323   0.3788   0.3807
de     0.6540       0.6526  0.6151  0.6347     0.6434      0.6438    0.6505  0.6490      0.6520     0.6076      0.6101       0.6213       0.6206        0.6087        0.5906       0.6134       0.6208       0.6283       0.6491       0.5450  0.5913  0.6015   0.6150   0.6056   0.6064  0.5946      0.6217  0.6082   0.5647   0.5861
en     0.8173       0.8196  0.7719  0.8179     0.8225      0.8065    0.8103  0.7698      0.7756     0.7669      0.7685       0.7783       0.7822        0.7748        0.7530       0.7750       0.7863       0.7944       0.7787       0.6486  0.7637  0.7623   0.7599   0.7660   0.7662  0.7632      0.7775  0.7472   0.7773   0.7396
es     0.6665       0.6772  0.6227  0.6638     0.6595      0.6355    0.6496  0.6315      0.6425     0.6174      0.6192       0.6279       0.6306        0.6279        0.6158       0.6286       0.6465       0.6648       0.6544       0.5291  0.6152  0.6020   0.6187   0.6163   0.6167  0.6207      0.6265  0.6260   0.6213   0.6152
fil    0.4083       0.4074  0.3962  0.4085     0.4127      0.4249    0.4107  0.3901      0.3940     0.3879      0.3904       0.4061       0.4057        0.3767        0.3324       0.3890       0.3929       0.3955       0.3922       0.3727  0.3562  0.4243   0.4026   0.3865   0.3866  0.3851      0.4004  0.3879   0.3832   0.3851
fr     0.5372       0.5489  0.4960  0.5401     0.5252      0.5666    0.5477  0.5685      0.5632     0.4963      0.4963       0.4941       0.4912        0.4917        0.4972       0.5002       0.5093       0.5353       0.5555       0.5618  0.4368  0.4821   0.4865   0.4958   0.4962  0.4961      0.4950  0.5503   0.4789   0.4810
it     0.6301       0.6315  0.6079  0.6115     0.6131      0.6093    0.6259  0.6226      0.6288     0.6062      0.6069       0.6066       0.5989        0.5832        0.5659       0.6096       0.6147       0.6259       0.6292       0.5321  0.5647  0.5780   0.6094   0.6058   0.6057  0.6049      0.6073  0.6131   0.5309   0.5917
ja     0.6011       0.5947  0.6068  0.4312     0.3300      0.6350    0.6361  0.5866      0.5963     0.5984      0.6014       0.6141       0.6159        0.6021        0.5750       0.6094       0.6178       0.6165       0.6021       0.5150  0.5819  0.6169   0.6016   0.5995   0.5964  0.5923      0.6139  0.5735   0.6100   0.5839
pt     0.7621       0.7659  0.7253  0.7562     0.7569      0.7586    0.7613  0.7297      0.7417     0.7259      0.7258       0.7227       0.7172        0.7080        0.6943       0.7309       0.7379       0.7481       0.7477       0.6312  0.6817  0.6926   0.7182   0.7260   0.7258  0.7395      0.7232  0.7343   0.6796   0.7314
si     0.2586       0.2505  0.2609  0.1983     0.1629      0.2099    0.2622  0.2215      0.2585     0.2545      0.2566       0.2654       0.2599        0.2415        0.2248       0.2542       0.2533       0.2704       0.2611       0.1211  0.2152  0.2660   0.2760   0.2527   0.2534  0.2658      0.2653  0.0472   0.2974   0.2562
MEDIE  0.5778       0.5781  0.5519  0.5472     0.5321      0.5691    0.5782  0.5541      0.5630     0.5475      0.5490       0.5554       0.5534        0.5410        0.5223       0.5523       0.5593       0.5689       0.5659       0.4746  0.5192  0.5420   0.5503   0.5469   0.5467  0.5460      0.5548  0.5220   0.5322   0.5351
```

Fata de incumbentul `blend` (Ridge300 + HGB), pe medie:

```
  blend-et     +0.0004
  blend-lasso  +0.0003
  extratrees   -0.0087
  lasso-a1e-3  -0.0089
  lasso-a3e-3  -0.0119
  elasticnet   -0.0148
  lasso-a3e-4  -0.0184
  ridge-a1000  -0.0224
  bayesridge   -0.0230
  lasso        -0.0237
  ridge-a3000  -0.0244
  lasso-a1e-4  -0.0254
  ridge        -0.0258
  pls-k16      -0.0274
  ridge-a100   -0.0288
  ridge-a30    -0.0303
  hgb          -0.0306
  pls-k32      -0.0309
  pls-k64      -0.0311
  huber        -0.0318
  pls-k8       -0.0358
  ridge-a10000 -0.0368
  svr-lin      -0.0427
  krr-rbf      -0.0456
  hgb-adanc    -0.0457
  ridge-a30000 -0.0555
  ard          -0.0558
  pls-k4       -0.0586
  lasso-a3e-2  -0.1032
```

## rho intre estimatori, mediat pe limbi

```
              blend  blend-lasso  ridge    hgb  hgb-adanc  extratrees  blend-et  lasso  elasticnet  ridge-a30  ridge-a100  ridge-a1000  ridge-a3000  ridge-a10000  ridge-a30000  lasso-a1e-4  lasso-a3e-4  lasso-a1e-3  lasso-a3e-3  lasso-a3e-2  pls-k4  pls-k8  pls-k16  pls-k32  pls-k64  huber  bayesridge    ard  krr-rbf  svr-lin
blend         1.000        0.986  0.960  0.940      0.908       0.931     0.983  0.905       0.927      0.954       0.956        0.963        0.955         0.929         0.892        0.960        0.966        0.961        0.938        0.788   0.899   0.936    0.955    0.953    0.953  0.944       0.963  0.842    0.871    0.929
blend-lasso   0.986        1.000  0.919  0.960      0.925       0.949     0.963  0.927       0.950      0.910       0.913        0.926        0.926         0.911         0.885        0.923        0.942        0.966        0.960        0.794   0.883   0.899    0.912    0.909    0.909  0.910       0.927  0.863    0.848    0.899
ridge         0.960        0.919  1.000  0.811      0.800       0.858     0.978  0.863       0.890      0.998       0.999        0.996        0.976         0.930         0.877        0.998        0.992        0.959        0.909        0.757   0.901   0.969    0.996    0.998    0.998  0.980       0.997  0.812    0.880    0.960
hgb           0.940        0.960  0.811  1.000      0.951       0.914     0.880  0.855       0.870      0.800       0.804        0.822        0.830         0.829         0.815        0.813        0.831        0.858        0.871        0.739   0.803   0.799    0.804    0.799    0.799  0.801       0.822  0.787    0.771    0.793
hgb-adanc     0.908        0.925  0.800  0.951      1.000       0.889     0.864  0.830       0.848      0.791       0.794        0.809        0.814         0.811         0.796        0.802        0.819        0.844        0.851        0.719   0.786   0.785    0.792    0.790    0.790  0.789       0.809  0.774    0.752    0.781
extratrees    0.931        0.949  0.858  0.914      0.889       1.000     0.944  0.932       0.938      0.847       0.851        0.870        0.879         0.882         0.874        0.860        0.879        0.910        0.933        0.839   0.844   0.842    0.849    0.846    0.846  0.846       0.870  0.856    0.809    0.835
blend-et      0.983        0.963  0.978  0.880      0.864       0.944     1.000  0.921       0.940      0.973       0.975        0.980        0.971         0.944         0.907        0.978        0.982        0.974        0.950        0.817   0.910   0.951    0.972    0.973    0.972  0.961       0.981  0.858    0.882    0.944
lasso         0.905        0.927  0.863  0.855      0.830       0.932     0.921  1.000       0.984      0.855       0.858        0.870        0.871         0.864         0.851        0.869        0.891        0.928        0.966        0.888   0.820   0.837    0.856    0.855    0.854  0.857       0.872  0.898    0.810    0.847
elasticnet    0.927        0.950  0.890  0.870      0.848       0.938     0.940  0.984       1.000      0.882       0.884        0.897        0.899         0.891         0.875        0.896        0.918        0.957        0.993        0.845   0.851   0.866    0.883    0.881    0.880  0.885       0.898  0.898    0.829    0.876
ridge-a30     0.954        0.910  0.998  0.800      0.791       0.847     0.973  0.855       0.882      1.000       1.000        0.988        0.962         0.911         0.855        0.998        0.989        0.953        0.901        0.746   0.880   0.955    0.995    1.000    1.000  0.984       0.990  0.815    0.864    0.964
ridge-a100    0.956        0.913  0.999  0.804      0.794       0.851     0.975  0.858       0.884      1.000       1.000        0.991        0.966         0.917         0.862        0.999        0.990        0.955        0.904        0.750   0.886   0.960    0.996    1.000    1.000  0.983       0.993  0.814    0.869    0.963
ridge-a1000   0.963        0.926  0.996  0.822      0.809       0.870     0.980  0.870       0.897      0.988       0.991        1.000        0.992         0.958         0.910        0.991        0.988        0.962        0.916        0.771   0.931   0.983    0.990    0.987    0.987  0.967       1.000  0.804    0.900    0.948
ridge-a3000   0.955        0.926  0.976  0.830      0.814       0.879     0.971  0.871       0.899      0.962       0.966        0.992        1.000         0.986         0.951        0.967        0.970        0.954        0.915        0.785   0.965   0.984    0.967    0.960    0.960  0.937       0.989  0.786    0.916    0.919
ridge-a10000  0.929        0.911  0.930  0.829      0.811       0.882     0.944  0.864       0.891      0.911       0.917        0.958        0.986         1.000         0.988        0.919        0.929        0.928        0.904        0.798   0.983   0.953    0.916    0.909    0.908  0.884       0.952  0.759    0.912    0.869
ridge-a30000  0.892        0.885  0.877  0.815      0.796       0.874     0.907  0.851       0.875      0.855       0.862        0.910        0.951         0.988         1.000        0.865        0.879        0.892        0.883        0.804   0.967   0.900    0.860    0.853    0.852  0.829       0.904  0.732    0.886    0.817
lasso-a1e-4   0.960        0.923  0.998  0.813      0.802       0.860     0.978  0.869       0.896      0.998       0.999        0.991        0.967         0.919         0.865        1.000        0.996        0.966        0.916        0.755   0.889   0.959    0.995    0.998    0.998  0.985       0.992  0.826    0.869    0.965
lasso-a3e-4   0.966        0.942  0.992  0.831      0.819       0.879     0.982  0.891       0.918      0.989       0.990        0.988        0.970         0.929         0.879        0.996        1.000        0.982        0.937        0.769   0.900   0.960    0.987    0.989    0.989  0.979       0.990  0.843    0.874    0.962
lasso-a1e-3   0.961        0.966  0.959  0.858      0.844       0.910     0.974  0.928       0.957      0.953       0.955        0.962        0.954         0.928         0.892        0.966        0.982        1.000        0.976        0.793   0.901   0.934    0.953    0.953    0.952  0.950       0.963  0.873    0.867    0.937
lasso-a3e-3   0.938        0.960  0.909  0.871      0.851       0.933     0.950  0.966       0.993      0.901       0.904        0.916        0.915         0.904         0.883        0.916        0.937        0.976        1.000        0.824   0.870   0.885    0.902    0.901    0.900  0.904       0.917  0.894    0.840    0.895
lasso-a3e-2   0.788        0.794  0.757  0.739      0.719       0.839     0.817  0.888       0.845      0.746       0.750        0.771        0.785         0.798         0.804        0.755        0.769        0.793        0.824        1.000   0.748   0.741    0.744    0.746    0.744  0.727       0.770  0.781    0.747    0.715
pls-k4        0.899        0.883  0.901  0.803      0.786       0.844     0.910  0.820       0.851      0.880       0.886        0.931        0.965         0.983         0.967        0.889        0.900        0.901        0.870        0.748   1.000   0.930    0.884    0.878    0.877  0.854       0.925  0.724    0.890    0.838
pls-k8        0.936        0.899  0.969  0.799      0.785       0.842     0.951  0.837       0.866      0.955       0.960        0.983        0.984         0.953         0.900        0.959        0.960        0.934        0.885        0.741   0.930   1.000    0.961    0.954    0.953  0.927       0.980  0.764    0.897    0.907
pls-k16       0.955        0.912  0.996  0.804      0.792       0.849     0.972  0.856       0.883      0.995       0.996        0.990        0.967         0.916         0.860        0.995        0.987        0.953        0.902        0.744   0.884   0.961    1.000    0.994    0.994  0.977       0.992  0.806    0.870    0.958
pls-k32       0.953        0.909  0.998  0.799      0.790       0.846     0.973  0.855       0.881      1.000       1.000        0.987        0.960         0.909         0.853        0.998        0.989        0.953        0.901        0.746   0.878   0.954    0.994    1.000    1.000  0.984       0.990  0.815    0.862    0.964
pls-k64       0.953        0.909  0.998  0.799      0.790       0.846     0.972  0.854       0.880      1.000       1.000        0.987        0.960         0.908         0.852        0.998        0.989        0.952        0.900        0.744   0.877   0.953    0.994    1.000    1.000  0.984       0.989  0.815    0.862    0.964
huber         0.944        0.910  0.980  0.801      0.789       0.846     0.961  0.857       0.885      0.984       0.983        0.967        0.937         0.884         0.829        0.985        0.979        0.950        0.904        0.727   0.854   0.927    0.977    0.984    0.984  1.000       0.970  0.827    0.836    0.986
bayesridge    0.963        0.927  0.997  0.822      0.809       0.870     0.981  0.872       0.898      0.990       0.993        1.000        0.989         0.952         0.904        0.992        0.990        0.963        0.917        0.770   0.925   0.980    0.992    0.990    0.989  0.970       1.000  0.807    0.896    0.951
ard           0.842        0.863  0.812  0.787      0.774       0.856     0.858  0.898       0.898      0.815       0.814        0.804        0.786         0.759         0.732        0.826        0.843        0.873        0.894        0.781   0.724   0.764    0.806    0.815    0.815  0.827       0.807  1.000    0.702    0.817
krr-rbf       0.871        0.848  0.880  0.771      0.752       0.809     0.882  0.810       0.829      0.864       0.869        0.900        0.916         0.912         0.886        0.869        0.874        0.867        0.840        0.747   0.890   0.897    0.870    0.862    0.862  0.836       0.896  0.702    1.000    0.819
svr-lin       0.929        0.899  0.960  0.793      0.781       0.835     0.944  0.847       0.876      0.964       0.963        0.948        0.919         0.869         0.817        0.965        0.962        0.937        0.895        0.715   0.838   0.907    0.958    0.964    0.964  0.986       0.951  0.817    0.819    1.000
```

## r al mediei standardizate, pe toate submultimile estimatorilor de baza

`blend` si `blend-et` sunt excluse din combinatii: sunt ele insele medii, deci ar intra de doua ori.

Enumerate submultimile de pana la **3** membri (3303 din 134217727 posibile). Motivul e cost, dar si sens: cu grila de alpha pe disc, combinatiile mari sunt in majoritate doua puncte ale ACELEIASI familii puse impreuna, ceea ce nu e un ansamblu de biasuri diferite.

```
  hgb+extratrees+pls-k16                   0.582387
  extratrees+lasso-a1e-3+krr-rbf           0.582052
  ridge+hgb+extratrees                     0.581763
  hgb+extratrees+ridge-a100                0.581657
  hgb+extratrees+ridge-a30                 0.581558
  extratrees+elasticnet+pls-k16            0.581557
  extratrees+lasso-a3e-3+pls-k16           0.581506
  hgb+extratrees+lasso-a1e-4               0.581504
  hgb+extratrees+pls-k32                   0.581497
  hgb+extratrees+pls-k64                   0.581486
```

Calculate toate **3303** submultimile, listate primele 10. Cea mai slaba e `lasso-a3e-2` la 0.474560.

Identitatea de frontiera, verificata pe fiecare limba pentru `ridge+hgb`: eroarea maxima **2.22e-16**. Nu e o aproximare buna, e o identitate algebrica.

## Ce i-ar trebui unui al treilea estimator. Scris inainte de a-l cauta

Blend-ul de acum, prin frontiera: r_ridge 0.5519, r_hgb 0.5472, rho 0.8105, deci **0.577613**.

Bara pe fuziune e +0.0045, iar factorul de transmisie A -> fuziune e 0.259 mediu si 0.091 marginal (`e_frontiera_enc.md`). Deci blend-ul trebuie sa urce cu +0.0174 (optimist) pana la +0.0495 (pesimist).

rho mediu MAXIM admis fata de `ridge` si `hgb`:

```
    r3    rho max optimist    rho max pesimist
 0.350               0.328               0.180
 0.400               0.432               0.274
 0.450               0.539               0.371
 0.500               0.651               0.471
 0.550               0.765               0.574
 0.580               0.836               0.637
 0.620               0.932               0.724
 0.650               orice               0.790
```

Candidatii masurati, rho mediu fata de cei doi membri:

```
  blend-lasso  r 0.5781  rho 0.940  prag optimist 0.831  ->  CADE
  hgb-adanc    r 0.5321  rho 0.875  prag optimist 0.724  ->  CADE
  extratrees   r 0.5691  rho 0.886  prag optimist 0.810  ->  CADE
  lasso        r 0.5541  rho 0.859  prag optimist 0.775  ->  CADE
  elasticnet   r 0.5630  rho 0.880  prag optimist 0.796  ->  CADE
  ridge-a30    r 0.5475  rho 0.899  prag optimist 0.760  ->  CADE
  ridge-a100   r 0.5490  rho 0.901  prag optimist 0.763  ->  CADE
  ridge-a1000  r 0.5554  rho 0.909  prag optimist 0.778  ->  CADE
  ridge-a3000  r 0.5534  rho 0.903  prag optimist 0.773  ->  CADE
  ridge-a10000 r 0.5410  rho 0.880  prag optimist 0.744  ->  CADE
  ridge-a30000 r 0.5223  rho 0.846  prag optimist 0.701  ->  CADE
  lasso-a1e-4  r 0.5523  rho 0.905  prag optimist 0.771  ->  CADE
  lasso-a3e-4  r 0.5593  rho 0.911  prag optimist 0.787  ->  CADE
  lasso-a1e-3  r 0.5689  rho 0.909  prag optimist 0.810  ->  CADE
  lasso-a3e-3  r 0.5659  rho 0.890  prag optimist 0.803  ->  CADE
  lasso-a3e-2  r 0.4746  rho 0.748  prag optimist 0.594  ->  CADE
  pls-k4       r 0.5192  rho 0.852  prag optimist 0.694  ->  CADE
  pls-k8       r 0.5420  rho 0.884  prag optimist 0.747  ->  CADE
  pls-k16      r 0.5503  rho 0.900  prag optimist 0.766  ->  CADE
  pls-k32      r 0.5469  rho 0.898  prag optimist 0.758  ->  CADE
  pls-k64      r 0.5467  rho 0.898  prag optimist 0.758  ->  CADE
  huber        r 0.5460  rho 0.890  prag optimist 0.756  ->  CADE
  bayesridge   r 0.5548  rho 0.909  prag optimist 0.777  ->  CADE
  ard          r 0.5220  rho 0.800  prag optimist 0.701  ->  CADE
  krr-rbf      r 0.5322  rho 0.825  prag optimist 0.724  ->  CADE
  svr-lin      r 0.5351  rho 0.877  prag optimist 0.731  ->  CADE
```

## Inlocuirea jumatatii liniare a blend-ului

Controlul e `ridge+hgb` = **0.575296**, adica blend-ul de acum scris ca media standardizata a celor doua jumatati ale lui. Fiecare candidat X e pus in locul lui `ridge`, cu ACELASI partener `hgb`, deci diferenta e a jumatatii liniare si a nimic altceva.

De ce 0.575296 aici si 0.577613 la punctul 4, pentru acelasi `ridge+hgb`. Identitatea de frontiera e exacta PE LIMBA, si asta s-a verificat mai sus la ordinul 1e-16. Punctul 4 o aplica insa pe `r` si `rho` deja MEDIATE peste limbi, ca sa poata desena o curba de prag cu un singur numar, iar media unei functii neliniare nu e functia mediei: iese cu +0.0023 pe langa. Cifra care se compara cu punctul 3 si intre candidati e cea de aici, media celor zece r pe limba. Cea de la punctul 4 ramane buna pentru ce face ea, curba de prag, fiindca acolo conteaza diferenta fata de ea insasi, nu nivelul.

`castig fuziune` e diferenta pe A inmultita cu factorul de transmisie (0.259 mediu, 0.091 marginal). Verdictul e fata de bara de +0.0045 pe fuziune, luata pe estimarea OPTIMISTA, deci un `CADE` e un cade si pe cea mai buna ipoteza.

```
  candidat             r_A  rho(X,hgb)   r(X+hgb)   delta_A   fuz.opt   fuz.pes  verdict
  lasso-a1e-3       0.5689       0.858   0.576797   +0.0015   +0.0004   +0.0001  CADE
  lasso-a3e-4       0.5593       0.831   0.575926   +0.0006   +0.0002   +0.0001  CADE
  pls-k16           0.5503       0.804   0.575602   +0.0003   +0.0001   +0.0000  CADE
  ridge-a1000       0.5554       0.822   0.575392   +0.0001   +0.0000   +0.0000  CADE
  bayesridge        0.5548       0.822   0.575228   -0.0001   -0.0000   -0.0000  CADE
  lasso-a1e-4       0.5523       0.813   0.575078   -0.0002   -0.0001   -0.0000  CADE
  ridge-a100        0.5490       0.804   0.574767   -0.0005   -0.0001   -0.0000  CADE
  ridge-a30         0.5475       0.800   0.574443   -0.0009   -0.0002   -0.0001  CADE
  pls-k32           0.5469       0.799   0.574288   -0.0010   -0.0003   -0.0001  CADE
  pls-k64           0.5467       0.799   0.574244   -0.0011   -0.0003   -0.0001  CADE
  huber             0.5460       0.801   0.573743   -0.0016   -0.0004   -0.0001  CADE
  lasso-a3e-3       0.5659       0.871   0.573408   -0.0019   -0.0005   -0.0002  CADE
  ridge-a3000       0.5534       0.830   0.573118   -0.0022   -0.0006   -0.0002  CADE
  pls-k8            0.5420       0.799   0.572165   -0.0031   -0.0008   -0.0003  CADE
  elasticnet        0.5630       0.870   0.572056   -0.0032   -0.0008   -0.0003  CADE
  krr-rbf           0.5322       0.771   0.570317   -0.0050   -0.0013   -0.0005  CADE
  svr-lin           0.5351       0.793   0.569594   -0.0057   -0.0015   -0.0005  CADE
  lasso             0.5541       0.855   0.569243   -0.0061   -0.0016   -0.0006  CADE
  extratrees        0.5691       0.914   0.569214   -0.0061   -0.0016   -0.0006  CADE
  blend-lasso       0.5781       0.960   0.567646   -0.0077   -0.0020   -0.0007  CADE
  ridge-a10000      0.5410       0.829   0.566752   -0.0085   -0.0022   -0.0008  CADE
  ard               0.5220       0.787   0.559373   -0.0159   -0.0041   -0.0014  CADE
  pls-k4            0.5192       0.803   0.559373   -0.0159   -0.0041   -0.0014  CADE
  ridge-a30000      0.5223       0.815   0.558956   -0.0163   -0.0042   -0.0015  CADE
  hgb-adanc         0.5321       0.951   0.544372   -0.0309   -0.0080   -0.0028  CADE
  lasso-a3e-2       0.4746       0.739   0.543633   -0.0317   -0.0082   -0.0029  CADE
```

Ca sa treaca bara, un candidat trebuie sa urce A cu +0.0174 (optimist) pana la +0.0495 (pesimist). Cifra care decide e `rho`, nu `r`: un candidat cu r mai bun dar rho mai mare pierde, si s-a intamplat de trei ori in proiect.

## Grila `ridge (alpha)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  ridge-a30              30   0.5475
  ridge-a100            100   0.5490
  ridge                 300   0.5519
  ridge-a1000          1000   0.5554   <- cel mai bun pe test
  ridge-a3000          3000   0.5534
  ridge-a10000        10000   0.5410
  ridge-a30000        30000   0.5223
```

```
  selectie LOLO                0.555374
  media predictiilor grilei    0.556656
  cel mai bun punct fix        0.555374   (ridge-a1000, dar e ales PE TEST)
  latimea criteriului          0.0331
  LOLO a nimerit optimul       4/10 limbi
```

Punctul ales per limba: ca=ridge-a1000, de=ridge-a1000, en=ridge-a1000, es=ridge-a1000, fil=ridge-a1000, fr=ridge-a1000, it=ridge-a1000, ja=ridge-a1000, pt=ridge-a1000, si=ridge-a1000.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `ridge-a1000`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

## Grila `lasso (alpha)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  lasso-a1e-4        0.0001   0.5523
  lasso-a3e-4        0.0003   0.5593
  lasso-a1e-3         0.001   0.5689   <- cel mai bun pe test
  lasso-a3e-3         0.003   0.5659
  lasso                0.01   0.5541
  lasso-a3e-2          0.03   0.4746
```

```
  selectie LOLO                0.568870
  media predictiilor grilei    0.569636
  cel mai bun punct fix        0.568870   (lasso-a1e-3, dar e ales PE TEST)
  latimea criteriului          0.0943
  LOLO a nimerit optimul       5/10 limbi
```

Punctul ales per limba: ca=lasso-a1e-3, de=lasso-a1e-3, en=lasso-a1e-3, es=lasso-a1e-3, fil=lasso-a1e-3, fr=lasso-a1e-3, it=lasso-a1e-3, ja=lasso-a1e-3, pt=lasso-a1e-3, si=lasso-a1e-3.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `lasso-a1e-3`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

## Grila `pls (k)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  pls-k4                  4   0.5192
  pls-k8                  8   0.5420
  pls-k16                16   0.5503   <- cel mai bun pe test
  pls-k32                32   0.5469
  pls-k64                64   0.5467
```

```
  selectie LOLO                0.550337
  media predictiilor grilei    0.553401
  cel mai bun punct fix        0.550337   (pls-k16, dar e ales PE TEST)
  latimea criteriului          0.0312
  LOLO a nimerit optimul       5/10 limbi
```

Punctul ales per limba: ca=pls-k16, de=pls-k16, en=pls-k16, es=pls-k16, fil=pls-k16, fr=pls-k16, it=pls-k16, ja=pls-k16, pt=pls-k16, si=pls-k16.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `pls-k16`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

