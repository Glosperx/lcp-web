# Axa regresorului pe semnalul A

Generat de `analysis_regresor.py`. Coloana `p_multi`, splitul test, encoder xlmr, configuratia `--lemma-freq --afeat fert_inloc`, spatiu `labse`.

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
ca     0.4728  0.4577  0.3787      0.4212  0.3858      0.4061     0.4532      0.4547       0.4616       0.4605        0.4508        0.4330       0.4554       0.4561       0.4506       0.4254       0.3216  0.4403  0.4391   0.4574   0.4501   0.4526  0.4501      0.4606  0.3665   0.4134   0.4264
de     0.6163  0.5698  0.6001      0.5946  0.5874      0.5974     0.5672      0.5682       0.5695       0.5615        0.5462        0.5344       0.5759       0.5925       0.6044       0.6069       0.4109  0.5064  0.5481   0.5742   0.5644   0.5668  0.5683      0.5701  0.5920   0.5315   0.5474
en     0.8131  0.7776  0.8075      0.7946  0.7609      0.7668     0.7694      0.7723       0.7839       0.7838        0.7724        0.7542       0.7767       0.7846       0.7802       0.7724       0.6846  0.7572  0.7746   0.7749   0.7681   0.7676  0.7700      0.7824  0.7368   0.7785   0.7637
es     0.6713  0.6387  0.6537      0.6313  0.6325      0.6431     0.6298      0.6329       0.6466       0.6473        0.6330        0.6016       0.6453       0.6606       0.6721       0.6601       0.6085  0.6289  0.6323   0.6369   0.6254   0.6282  0.6463      0.6441  0.6245   0.6097   0.6341
fil    0.3950  0.3916  0.3876      0.4236  0.4000      0.3949     0.3842      0.3866       0.4013       0.4080        0.3987        0.3742       0.3871       0.3903       0.3918       0.3912       0.4317  0.3817  0.4197   0.3905   0.3840   0.3831  0.3873      0.3944  0.3914   0.3600   0.3994
fr     0.5460  0.5224  0.5276      0.5475  0.5588      0.5550     0.5103      0.5146       0.5327       0.5379        0.5374        0.5324       0.5268       0.5443       0.5625       0.5599       0.5393  0.4908  0.5182   0.5220   0.5082   0.5079  0.4956      0.5287  0.5488   0.5049   0.4644
it     0.6149  0.5953  0.5985      0.5856  0.6006      0.6077     0.5956      0.5958       0.5894       0.5714        0.5389        0.5082       0.6020       0.6110       0.6167       0.6137       0.5280  0.5186  0.5776   0.5957   0.5937   0.5954  0.6056      0.5925  0.5958   0.5321   0.5907
ja     0.5282  0.5612  0.3407      0.5897  0.5670      0.5763     0.5546      0.5569       0.5661       0.5611        0.5407        0.5183       0.5670       0.5837       0.6012       0.5850       0.5044  0.5102  0.5297   0.5570   0.5526   0.5534  0.5504      0.5655  0.5694   0.4810   0.5275
pt     0.7647  0.7221  0.7651      0.7641  0.7448      0.7529     0.7167      0.7187       0.7241       0.7180        0.7014        0.6814       0.7273       0.7387       0.7504       0.7562       0.6987  0.6753  0.6995   0.7230   0.7143   0.7157  0.7315      0.7241  0.7375   0.6968   0.7308
si     0.3580  0.3490  0.2327      0.3232  0.3045      0.3247     0.3412      0.3437       0.3563       0.3562        0.3435        0.3276       0.3449       0.3484       0.3425       0.3260          NaN  0.3143  0.3655   0.3374   0.3364   0.3400  0.3293      0.3567  0.1698   0.3207   0.3168
MEDIE  0.5780  0.5585  0.5292      0.5675  0.5542      0.5625     0.5522      0.5544       0.5631       0.5606        0.5463        0.5265       0.5608       0.5710       0.5772       0.5697       0.5253  0.5224  0.5504   0.5569   0.5497   0.5511  0.5534      0.5619  0.5332   0.5229   0.5401
```

Fata de incumbentul `blend` (Ridge300 + HGB), pe medie:

```
  lasso-a1e-3  -0.0008
  lasso-a3e-4  -0.0070
  lasso-a3e-3  -0.0083
  extratrees   -0.0105
  ridge-a1000  -0.0149
  elasticnet   -0.0155
  bayesridge   -0.0161
  lasso-a1e-4  -0.0172
  ridge-a3000  -0.0175
  ridge        -0.0195
  pls-k16      -0.0211
  ridge-a100   -0.0236
  lasso        -0.0238
  huber        -0.0246
  ridge-a30    -0.0258
  pls-k64      -0.0270
  pls-k8       -0.0276
  pls-k32      -0.0283
  ridge-a10000 -0.0317
  svr-lin      -0.0379
  ard          -0.0448
  hgb          -0.0488
  ridge-a30000 -0.0515
  lasso-a3e-2  -0.0527
  krr-rbf      -0.0552
  pls-k4       -0.0556
```

## rho intre estimatori, mediat pe limbi

```
              blend  ridge    hgb  extratrees  lasso  elasticnet  ridge-a30  ridge-a100  ridge-a1000  ridge-a3000  ridge-a10000  ridge-a30000  lasso-a1e-4  lasso-a3e-4  lasso-a1e-3  lasso-a3e-3  lasso-a3e-2  pls-k4  pls-k8  pls-k16  pls-k32  pls-k64  huber  bayesridge    ard  krr-rbf  svr-lin
blend         1.000  0.950  0.926       0.906  0.888       0.908      0.943       0.946        0.950        0.937         0.904         0.864        0.951        0.955        0.949        0.927        0.828   0.871   0.919    0.947    0.942    0.942  0.934       0.951  0.859    0.870    0.916
ridge         0.950  1.000  0.770       0.837  0.852       0.879      0.997       0.999        0.995        0.974         0.930         0.881        0.998        0.989        0.958        0.908        0.799   0.898   0.960    0.996    0.996    0.996  0.981       0.997  0.835    0.902    0.960
hgb           0.926  0.770  1.000       0.866  0.815       0.823      0.760       0.764        0.777        0.774         0.759         0.736        0.774        0.791        0.814        0.827        0.778   0.731   0.755    0.767    0.758    0.758  0.760       0.776  0.775    0.726    0.747
extratrees    0.906  0.837  0.866       1.000  0.920       0.921      0.826       0.830        0.847        0.848         0.838         0.821        0.843        0.862        0.890        0.915        0.885   0.796   0.821    0.833    0.823    0.824  0.823       0.846  0.874    0.789    0.810
lasso         0.888  0.852  0.815       0.920  1.000       0.988      0.842       0.845        0.860        0.859         0.844         0.824        0.860        0.884        0.924        0.969        0.930   0.802   0.832    0.849    0.838    0.840  0.843       0.861  0.935    0.787    0.831
elasticnet    0.908  0.879  0.823       0.921  0.988       1.000      0.867       0.872        0.888        0.887         0.874         0.854        0.886        0.910        0.949        0.990        0.909   0.834   0.858    0.875    0.864    0.865  0.866       0.888  0.934    0.816    0.853
ridge-a30     0.943  0.997  0.760       0.826  0.842       0.867      1.000       1.000        0.985        0.957         0.908         0.856        0.996        0.982        0.947        0.896        0.788   0.874   0.942    0.993    1.000    1.000  0.986       0.989  0.830    0.886    0.964
ridge-a100    0.946  0.999  0.764       0.830  0.845       0.872      1.000       1.000        0.989        0.962         0.915         0.864        0.997        0.985        0.951        0.900        0.792   0.882   0.948    0.995    0.999    0.999  0.985       0.992  0.832    0.891    0.963
ridge-a1000   0.950  0.995  0.777       0.847  0.860       0.888      0.985       0.989        1.000        0.991         0.959         0.915        0.991        0.989        0.965        0.917        0.811   0.931   0.977    0.989    0.983    0.983  0.966       0.999  0.834    0.919    0.946
ridge-a3000   0.937  0.974  0.774       0.848  0.859       0.887      0.957       0.962        0.991        1.000         0.987         0.954        0.967        0.972        0.958        0.915        0.816   0.964   0.981    0.963    0.954    0.954  0.935       0.987  0.820    0.931    0.916
ridge-a10000  0.904  0.930  0.759       0.838  0.844       0.874      0.908       0.915        0.959        0.987         1.000         0.988        0.920        0.932        0.931        0.898        0.809   0.979   0.953    0.914    0.904    0.904  0.883       0.950  0.790    0.926    0.866
ridge-a30000  0.864  0.881  0.736       0.821  0.824       0.854      0.856       0.864        0.915        0.954         0.988         1.000        0.870        0.884        0.893        0.873        0.791   0.958   0.904    0.861    0.853    0.853  0.830       0.904  0.759    0.901    0.816
lasso-a1e-4   0.951  0.998  0.774       0.843  0.860       0.886      0.996       0.997        0.991        0.967         0.920         0.870        1.000        0.993        0.964        0.915        0.802   0.888   0.953    0.995    0.995    0.995  0.982       0.994  0.848    0.893    0.961
lasso-a3e-4   0.955  0.989  0.791       0.862  0.884       0.910      0.982       0.985        0.989        0.972         0.932         0.884        0.993        1.000        0.983        0.939        0.819   0.902   0.958    0.987    0.980    0.980  0.970       0.990  0.869    0.897    0.948
lasso-a1e-3   0.949  0.958  0.814       0.890  0.924       0.949      0.947       0.951        0.965        0.958         0.931         0.893        0.964        0.983        1.000        0.975        0.850   0.904   0.937    0.954    0.944    0.944  0.939       0.965  0.898    0.882    0.921
lasso-a3e-3   0.927  0.908  0.827       0.915  0.969       0.990      0.896       0.900        0.917        0.915         0.898         0.873        0.915        0.939        0.975        1.000        0.890   0.863   0.888    0.904    0.893    0.894  0.894       0.917  0.925    0.841    0.879
lasso-a3e-2   0.828  0.799  0.778       0.885  0.930       0.909      0.788       0.792        0.811        0.816         0.809         0.791        0.802        0.819        0.850        0.890        1.000   0.775   0.793    0.790    0.785    0.786  0.784       0.808  0.863    0.752    0.773
pls-k4        0.871  0.898  0.731       0.796  0.802       0.834      0.874       0.882        0.931        0.964         0.979         0.958        0.888        0.902        0.904        0.863        0.775   1.000   0.927    0.880    0.870    0.870  0.848       0.921  0.749    0.906    0.831
pls-k8        0.919  0.960  0.755       0.821  0.832       0.858      0.942       0.948        0.977        0.981         0.953         0.904        0.953        0.958        0.937        0.888        0.793   0.927   1.000    0.949    0.939    0.939  0.921       0.972  0.800    0.908    0.904
pls-k16       0.947  0.996  0.767       0.833  0.849       0.875      0.993       0.995        0.989        0.963         0.914         0.861        0.995        0.987        0.954        0.904        0.790   0.880   0.949    1.000    0.992    0.991  0.978       0.992  0.838    0.889    0.957
pls-k32       0.942  0.996  0.758       0.823  0.838       0.864      1.000       0.999        0.983        0.954         0.904         0.853        0.995        0.980        0.944        0.893        0.785   0.870   0.939    0.992    1.000    0.999  0.985       0.988  0.827    0.884    0.963
pls-k64       0.942  0.996  0.758       0.824  0.840       0.865      1.000       0.999        0.983        0.954         0.904         0.853        0.995        0.980        0.944        0.894        0.786   0.870   0.939    0.991    0.999    1.000  0.986       0.988  0.829    0.883    0.964
huber         0.934  0.981  0.760       0.823  0.843       0.866      0.986       0.985        0.966        0.935         0.883         0.830        0.982        0.970        0.939        0.894        0.784   0.848   0.921    0.978    0.985    0.986  1.000       0.971  0.835    0.860    0.983
bayesridge    0.951  0.997  0.776       0.846  0.861       0.888      0.989       0.992        0.999        0.987         0.950         0.904        0.994        0.990        0.965        0.917        0.808   0.921   0.972    0.992    0.988    0.988  0.971       1.000  0.837    0.915    0.951
ard           0.859  0.835  0.775       0.874  0.935       0.934      0.830       0.832        0.834        0.820         0.790         0.759        0.848        0.869        0.898        0.925        0.863   0.749   0.800    0.838    0.827    0.829  0.835       0.837  1.000    0.744    0.822
krr-rbf       0.870  0.902  0.726       0.789  0.787       0.816      0.886       0.891        0.919        0.931         0.926         0.901        0.893        0.897        0.882        0.841        0.752   0.906   0.908    0.889    0.884    0.883  0.860       0.915  0.744    1.000    0.841
svr-lin       0.916  0.960  0.747       0.810  0.831       0.853      0.964       0.963        0.946        0.916         0.866         0.816        0.961        0.948        0.921        0.879        0.773   0.831   0.904    0.957    0.963    0.964  0.983       0.951  0.822    0.841    1.000
```

## r al mediei standardizate, pe toate submultimile estimatorilor de baza

`blend` si `blend-et` sunt excluse din combinatii: sunt ele insele medii, deci ar intra de doua ori.

Enumerate submultimile de pana la **3** membri (2951 din 67108863 posibile). Motivul e cost, dar si sens: cu grila de alpha pe disc, combinatiile mari sunt in majoritate doua puncte ale ACELEIASI familii puse impreuna, ceea ce nu e un ansamblu de biasuri diferite.

```
  extratrees+lasso-a3e-4                   0.588674
  extratrees+lasso-a1e-3                   0.587629
  ridge+extratrees+lasso-a1e-3             0.587578
  extratrees+ridge-a1000                   0.587088
  ridge+extratrees+lasso-a3e-3             0.586631
  extratrees+bayesridge                    0.586626
  extratrees+lasso-a1e-4                   0.586492
  ridge+extratrees                         0.586141
  extratrees+pls-k16                       0.585964
  ridge+extratrees+elasticnet              0.585656
```

Calculate toate **2951** submultimile, listate primele 10. Cea mai slaba e `pls-k4` la 0.522388.

Identitatea de frontiera, verificata pe fiecare limba pentru `ridge+hgb`: eroarea maxima **1.11e-16**. Nu e o aproximare buna, e o identitate algebrica.

## Ce i-ar trebui unui al treilea estimator. Scris inainte de a-l cauta

Blend-ul de acum, prin frontiera: r_ridge 0.5585, r_hgb 0.5292, rho 0.7697, deci **0.578187**.

Bara pe fuziune e +0.0045, iar factorul de transmisie A -> fuziune e 0.259 mediu si 0.091 marginal (`e_frontiera_enc.md`). Deci blend-ul trebuie sa urce cu +0.0174 (optimist) pana la +0.0495 (pesimist).

rho mediu MAXIM admis fata de `ridge` si `hgb`:

```
    r3    rho max optimist    rho max pesimist
 0.350               0.322               0.177
 0.400               0.425               0.270
 0.450               0.532               0.366
 0.500               0.642               0.465
 0.550               0.756               0.567
 0.580               0.826               0.630
 0.620               0.921               0.716
 0.650               0.994               0.782
```

Candidatii masurati, rho mediu fata de cei doi membri:

```
  extratrees   r 0.5675  rho 0.852  prag optimist 0.796  ->  CADE
  lasso        r 0.5542  rho 0.834  prag optimist 0.765  ->  CADE
  elasticnet   r 0.5625  rho 0.851  prag optimist 0.785  ->  CADE
  ridge-a30    r 0.5522  rho 0.879  prag optimist 0.761  ->  CADE
  ridge-a100   r 0.5544  rho 0.881  prag optimist 0.766  ->  CADE
  ridge-a1000  r 0.5631  rho 0.886  prag optimist 0.786  ->  CADE
  ridge-a3000  r 0.5606  rho 0.874  prag optimist 0.780  ->  CADE
  ridge-a10000 r 0.5463  rho 0.845  prag optimist 0.747  ->  CADE
  ridge-a30000 r 0.5265  rho 0.809  prag optimist 0.702  ->  CADE
  lasso-a1e-4  r 0.5608  rho 0.886  prag optimist 0.781  ->  CADE
  lasso-a3e-4  r 0.5710  rho 0.890  prag optimist 0.805  ->  CADE
  lasso-a1e-3  r 0.5772  rho 0.886  prag optimist 0.819  ->  CADE
  lasso-a3e-3  r 0.5697  rho 0.867  prag optimist 0.801  ->  CADE
  lasso-a3e-2  r 0.5253  rho 0.788  prag optimist 0.699  ->  CADE
  pls-k4       r 0.5224  rho 0.815  prag optimist 0.692  ->  CADE
  pls-k8       r 0.5504  rho 0.857  prag optimist 0.757  ->  CADE
  pls-k16      r 0.5569  rho 0.882  prag optimist 0.772  ->  CADE
  pls-k32      r 0.5497  rho 0.877  prag optimist 0.755  ->  CADE
  pls-k64      r 0.5511  rho 0.877  prag optimist 0.758  ->  CADE
  huber        r 0.5534  rho 0.871  prag optimist 0.764  ->  CADE
  bayesridge   r 0.5619  rho 0.887  prag optimist 0.783  ->  CADE
  ard          r 0.5332  rho 0.805  prag optimist 0.717  ->  CADE
  krr-rbf      r 0.5229  rho 0.814  prag optimist 0.694  ->  CADE
  svr-lin      r 0.5401  rho 0.853  prag optimist 0.733  ->  CADE
```

## Inlocuirea jumatatii liniare a blend-ului

Controlul e `ridge+hgb` = **0.574504**, adica blend-ul de acum scris ca media standardizata a celor doua jumatati ale lui. Fiecare candidat X e pus in locul lui `ridge`, cu ACELASI partener `hgb`, deci diferenta e a jumatatii liniare si a nimic altceva.

De ce 0.574504 aici si 0.578187 la punctul 4, pentru acelasi `ridge+hgb`. Identitatea de frontiera e exacta PE LIMBA, si asta s-a verificat mai sus la ordinul 1e-16. Punctul 4 o aplica insa pe `r` si `rho` deja MEDIATE peste limbi, ca sa poata desena o curba de prag cu un singur numar, iar media unei functii neliniare nu e functia mediei: iese cu +0.0037 pe langa. Cifra care se compara cu punctul 3 si intre candidati e cea de aici, media celor zece r pe limba. Cea de la punctul 4 ramane buna pentru ce face ea, curba de prag, fiindca acolo conteaza diferenta fata de ea insasi, nu nivelul.

`castig fuziune` e diferenta pe A inmultita cu factorul de transmisie (0.259 mediu, 0.091 marginal). Verdictul e fata de bara de +0.0045 pe fuziune, luata pe estimarea OPTIMISTA, deci un `CADE` e un cade si pe cea mai buna ipoteza.

```
  candidat             r_A  rho(X,hgb)   r(X+hgb)   delta_A   fuz.opt   fuz.pes  verdict
  lasso-a3e-4       0.5710       0.791   0.577591   +0.0031   +0.0008   +0.0003  CADE
  lasso-a1e-3       0.5772       0.814   0.577274   +0.0028   +0.0007   +0.0003  CADE
  ridge-a1000       0.5631       0.777   0.575908   +0.0014   +0.0004   +0.0001  CADE
  bayesridge        0.5619       0.776   0.575346   +0.0008   +0.0002   +0.0001  CADE
  ridge-a3000       0.5606       0.774   0.574942   +0.0004   +0.0001   +0.0000  CADE
  lasso-a1e-4       0.5608       0.774   0.574906   +0.0004   +0.0001   +0.0000  CADE
  pls-k16           0.5569       0.767   0.573901   -0.0006   -0.0002   -0.0001  CADE
  ridge-a100        0.5544       0.764   0.573292   -0.0012   -0.0003   -0.0001  CADE
  huber             0.5534       0.760   0.573184   -0.0013   -0.0003   -0.0001  CADE
  ridge-a30         0.5522       0.760   0.572660   -0.0018   -0.0005   -0.0002  CADE
  pls-k8            0.5504       0.755   0.572591   -0.0019   -0.0005   -0.0002  CADE
  pls-k64           0.5511       0.758   0.572360   -0.0021   -0.0006   -0.0002  CADE
  pls-k32           0.5497       0.758   0.571693   -0.0028   -0.0007   -0.0003  CADE
  lasso-a3e-3       0.5697       0.827   0.571259   -0.0032   -0.0008   -0.0003  CADE
  ridge-a10000      0.5463       0.759   0.569857   -0.0046   -0.0012   -0.0004  CADE
  elasticnet        0.5625       0.823   0.568047   -0.0065   -0.0017   -0.0006  CADE
  svr-lin           0.5401       0.747   0.568007   -0.0065   -0.0017   -0.0006  CADE
  lasso             0.5542       0.815   0.564713   -0.0098   -0.0025   -0.0009  CADE
  extratrees        0.5675       0.866   0.564302   -0.0102   -0.0026   -0.0009  CADE
  ridge-a30000      0.5265       0.736   0.562910   -0.0116   -0.0030   -0.0011  CADE
  krr-rbf           0.5229       0.726   0.562333   -0.0122   -0.0032   -0.0011  CADE
  pls-k4            0.5224       0.731   0.561533   -0.0130   -0.0034   -0.0012  CADE
  ard               0.5332       0.775   0.558568   -0.0159   -0.0041   -0.0015  CADE
  lasso-a3e-2       0.5253       0.778   0.540113   -0.0344   -0.0089   -0.0031  CADE
```

Ca sa treaca bara, un candidat trebuie sa urce A cu +0.0174 (optimist) pana la +0.0495 (pesimist). Cifra care decide e `rho`, nu `r`: un candidat cu r mai bun dar rho mai mare pierde, si s-a intamplat de trei ori in proiect.

## Grila `ridge (alpha)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  ridge-a30              30   0.5522
  ridge-a100            100   0.5544
  ridge                 300   0.5585
  ridge-a1000          1000   0.5631   <- cel mai bun pe test
  ridge-a3000          3000   0.5606
  ridge-a10000        10000   0.5463
  ridge-a30000        30000   0.5265
```

```
  selectie LOLO                0.563146
  media predictiilor grilei    0.562846
  cel mai bun punct fix        0.563146   (ridge-a1000, dar e ales PE TEST)
  latimea criteriului          0.0366
  LOLO a nimerit optimul       5/10 limbi
```

Punctul ales per limba: ca=ridge-a1000, de=ridge-a1000, en=ridge-a1000, es=ridge-a1000, fil=ridge-a1000, fr=ridge-a1000, it=ridge-a1000, ja=ridge-a1000, pt=ridge-a1000, si=ridge-a1000.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `ridge-a1000`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

Medierea grilei iese cu -0.000300 sub punctul unic, ceea ce e de asteptat: grila contine si puncte clar proaste, iar medierea le tine pe toate cu pondere egala. Medierea e raspunsul cand nu se poate ALEGE, nu cand se poate.

## Grila `lasso (alpha)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  lasso-a1e-4        0.0001   0.5608
  lasso-a3e-4        0.0003   0.5710
  lasso-a1e-3         0.001   0.5772   <- cel mai bun pe test
  lasso-a3e-3         0.003   0.5697
  lasso                0.01   0.5542
  lasso-a3e-2          0.03   0.5253
```

```
  selectie LOLO                0.577229
  media predictiilor grilei    0.577332
  cel mai bun punct fix        0.577229   (lasso-a1e-3, dar e ales PE TEST)
  latimea criteriului          0.0287
  LOLO a nimerit optimul       4/10 limbi
```

Punctul ales per limba: ca=lasso-a1e-3, de=lasso-a1e-3, en=lasso-a1e-3, es=lasso-a1e-3, fil=lasso-a1e-3, fr=lasso-a1e-3, it=lasso-a1e-3, ja=lasso-a1e-3, pt=lasso-a1e-3, si=lasso-a1e-3.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `lasso-a1e-3`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

## Grila `pls (k)`, aleasa leave-one-language-out

```
  punct           parametru      r_A
  pls-k4                  4   0.5224
  pls-k8                  8   0.5504
  pls-k16                16   0.5569   <- cel mai bun pe test
  pls-k32                32   0.5497
  pls-k64                64   0.5511
```

```
  selectie LOLO                0.556908
  media predictiilor grilei    0.560281
  cel mai bun punct fix        0.556908   (pls-k16, dar e ales PE TEST)
  latimea criteriului          0.0345
  LOLO a nimerit optimul       8/10 limbi
```

Punctul ales per limba: ca=pls-k16, de=pls-k16, en=pls-k16, es=pls-k16, fil=pls-k16, fr=pls-k16, it=pls-k16, ja=pls-k16, pt=pls-k16, si=pls-k16.

**Criteriul e UNANIM**: toate cele 10 taieri LOLO aleg `pls-k16`. Deci aici nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se citeste cifra:

- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare deloc.
- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. Coincidenta e un semn bun, nu o scurgere.

