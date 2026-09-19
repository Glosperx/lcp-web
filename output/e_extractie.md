# Sweep-ul de extractie: straturi x pooling

Generat de `analysis_extractie.py`.

Referinta e **xlmr SINGUR la `last4`**, nu sistemul: sistemul are trei encodere, deci o comparatie directa ar amesteca doua schimbari. Diferentele si intervalele sunt perechi fata de `enc_xlmr_now`.

> Sarite, fiindca n-au acelasi numar de randuri ca referinta: `ctxiso (4457 randuri fata de 5624)`.

## Rezultatul, toate configuratiile

```
                    r_A     r_fuz    d_fuz    d_lo    d_hi     P  limbi_sus  limbi_stricate
cfg                                                                                        
concat4_first  0.568050  0.681353  0.00146 -0.0017  0.0046  82.2        7.0             0.0
last4_first    0.579642  0.681023  0.00114 -0.0013  0.0036  81.6        7.0             0.0
last1_first    0.571760  0.680772  0.00089 -0.0025  0.0041  70.9        6.0             1.0
mid_first      0.575848  0.680544  0.00067 -0.0021  0.0036  66.8        7.0             0.0
last4          0.577785  0.679888      NaN     NaN     NaN   NaN        NaN             NaN
concat4        0.570836  0.679309 -0.00057 -0.0026  0.0014  26.7        6.0             1.0
last1          0.569098  0.678939 -0.00095 -0.0032  0.0013  19.8        5.0             1.0
last4_max      0.570243  0.678561 -0.00133 -0.0032  0.0006   8.6        6.0             1.0
mid            0.571962  0.678182 -0.00171 -0.0039  0.0005   6.1        3.0             0.0
concat4_max    0.560706  0.678023 -0.00186 -0.0046  0.0008   8.3        3.0             2.0
mid_max        0.567846  0.677782 -0.00210 -0.0044  0.0002   3.7        7.0             1.0
last1_max      0.559711  0.675879 -0.00400 -0.0069 -0.0012   0.2        3.0             3.0
last4_last     0.554301  0.675408 -0.00447 -0.0072 -0.0019   0.1        2.0             2.0
mid_last       0.549192  0.672912 -0.00697 -0.0100 -0.0041   0.0        2.0             2.0
concat4_last   0.536967  0.672476 -0.00741 -0.0107 -0.0042   0.0        3.0             3.0
last1_last     0.540515  0.672377 -0.00750 -0.0109 -0.0044   0.0        1.0             3.0
```

`d_fuz` e diferenta PERECHE pe fuziune fata de referinta; `limbi_stricate` numara limbile al caror interval pereche exclude zero IN JOS, adica sunt stricate cu semnificatie. Conditia din protocol se citeste INAINTEA mediei.

## Predictiile literaturii, verificate una cate una

Brat A (`p_multi`), mediat pe cele zece limbi:

```
            mean   first    last     max
straturi                                
last4     0.5778  0.5796  0.5543  0.5702
mid       0.5720  0.5758  0.5492  0.5678
concat4   0.5708  0.5680  0.5370  0.5607
last1     0.5691  0.5718  0.5405  0.5597
```

**P1, `last` bate `first`:** diferenta pe cele 4 familii de straturi: last4 -0.0253, mid -0.0267, concat4 -0.0311, last1 -0.0312. Media **-0.0286**. Predictia **CADE**.

**P2, `mean` sta intre ele:** adevarat pe 3 din 4 familii.

**P3, efectul de pooling creste cu fertilitatea.** `efect` e |`last` − `first`| pe bratul A al limbii:

```
      fertilitate   efect
lang                     
en         1.8842  0.0102
es         1.9646  0.0201
fr         2.0176  0.0166
pt         2.0829  0.0111
it         2.3614  0.0150
fil        2.3719  0.0022
de         2.5632  0.0363
ca         2.6090  0.0027
si         3.3200  0.0970
ja         3.3702  0.0420
```

Corelatia intre fertilitate si marimea efectului: **+0.726** (p = 0.017). Predictia **se confirma**.

## Mecanismul din spatele inversarii fata de literatura

`first` − `last`, pe bratul A. 950 din 5624 de tinte (16.9%) au UN singur subword, unde cele patru strategii de pooling coincid, deci efectul poate veni numai de la restul:

```
      pct_1sub  n_multi  dif_toate  dif_multi
lang                                         
ca      5.8427      419     0.0027    -0.0044
de     10.1754      512     0.0363     0.0443
en     30.8772      394     0.0102     0.0138
es     32.2091      402     0.0201     0.0176
fil    11.9298      502     0.0022     0.0067
fr     28.4710      407     0.0166     0.0372
it     14.2105      489     0.0150     0.0151
ja      0.0000      570     0.0420     0.0420
pt     28.5714      405     0.0111     0.0143
si      4.3333      574     0.0970     0.1126
```

`first` castiga pe **10 din 10** limbi. Efectul e mai mare pe tintele multi-subword (+0.0299) decat pe toate (+0.0253), si coreleaza **-0.457** cu cat de PUTINE tinte de un subword are limba, adica exact cum ar trebui daca ar veni din segmentare.

**De ce se inverseaza fata de Acs, Kadar si Kornai.** Ei probeaza trasaturi MORFOLOGICE, caz, gen, forma verbala, care traiesc in sufix; acolo ultimul subword E raspunsul, si `first` il arunca. Noi prezicem o proprietate LEXICALA, care tine de identitatea cuvantului. Ultimele bucati sunt fragmente scurte si foarte frecvente, impartite de mii de cuvinte (`ts`, `es`, `a` in exemplele catalane), deci nu identifica lexemul; prima bucata poarta materialul initial, care il identifica. Aceeasi segmentare, semnal opus, fiindca sarcina e alta. Nu contrazice lucrarea lor, ii delimiteaza domeniul.

Nuanta de onestitate: segmentarea lui XLM-R nu e morfologica, `controvertits` da `['controvertits' -> contro, verti, ts]`, deci propozitia corecta nu e "prima bucata e lema", ci "ultima bucata e un fragment impartit, prima nu".

## Corelatia cu `last4`, adica: merita mediat?

Frontiera cere rho <= 0.78 in varianta optimista pentru un membru de calitate egala. Configuratiile ACELUIASI model sunt mult peste, cu o exceptie:

```
               rho_la_last4  rho_min limba_min
cfg                                           
concat4_last         0.9069   0.7206        si
last1_last           0.9198   0.7509        si
concat4_first        0.9217   0.8049        si
last1_first          0.9235   0.7870        si
concat4_max          0.9271   0.7921        si
mid_last             0.9290   0.7787        si
last1_max            0.9300   0.7549        si
mid_first            0.9398   0.8363        si
last4_last           0.9437   0.7620        si
mid_max              0.9463   0.8206        si
last1                0.9577   0.9019        si
last4_first          0.9578   0.8599        si
concat4              0.9590   0.9271        si
mid                  0.9653   0.9043        si
last4_max            0.9676   0.8857        si
```

## Podeaua de zgomot a selectiei

Selectia LOLO peste cele 16 configuratii da **0.576355** pe bratul A, fata de **0.577785** la `last4`, adica **-0.001429**.

Podeaua: 20 bazine de cate 16 candidati ALEATORI, generati perturband predictiile de referinta cu zgomot calibrat sa reproduca imprastierea reala intre configuri (sd real intre configuri, mediat pe limbi: 0.0172), trecuti prin selectia LOLO identica.

Podea **-0.001592**, interval [-0.014831, +0.009376].
Excesul peste podea: **+0.000162** pe bratul A.
Prin factorul de transmisie (0.09 marginal, 0.26 mediu), asta ar fi **+0.000015 .. +0.000042** pe fuziune.

**Ce spune si ce NU spune cifra asta.** Spune ca a ALEGE configuratia din grila de 16, leave-one-language-out, nu valoreaza nimic: criteriul nu separa, exact ca la selectia de encodere. Nu spune ca poolingul n-ar conta. Cele doua axe ale grilei se comporta complet diferit, si se vede masurand fiecare separat:

```
                                                        candidati r_selectat  vs_last4 latime_pe_limba latime_pe_medie                     contrast sd_intre_limbi acelasi_semn
numai poolingul (4 candidati, straturi fixate la last4)         4   0.576355 -0.001429          0.0296          0.0253     last4_first - last4_last         0.0269        10/10
numai straturile (4 candidati, pooling fixat la mean)           4   0.577785       0.0          0.0287          0.0087                last4 - last1         0.0152         7/10
numai straturile, pooling fixat la first                        4   0.579642  0.001858          0.0236          0.0116  last4_first - concat4_first         0.0157         8/10
```

Cele doua latimi spun lucruri diferite si nu trebuie confundate. `latime_pe_limba` e media, peste limbi, a distantei dintre cel mai bun si cel mai slab candidat IN acea limba, si e aproape egala pe cele doua axe (~0.029): dupa ea, ar parea la fel de importante. `latime_pe_medie` e distanta DUPA medierea pe limbi, si acolo se despart. Diferenta dintre cele doua latimi e exact partea care se anuleaza la mediere, adica zgomotul per limba.

Ce separa cu adevarat axele e **constanta semnului**, coloana `acelasi_semn`. Un contrast care merge in aceeasi directie pe toate limbile e un efect; unul care isi schimba semnul e zgomot cu amplitudine mare. Numai axa de pooling e in primul caz.

Consecinta pentru protocol: `first` **nu** e argmaxul unei grile plate. E capatul unei axe cu efect sistematic, confirmat pe 10 limbi din 10, pe toate cele 4 familii de straturi, monoton cu fertilitatea (r = +0.726, p = 0.017) si cu mecanism verificat pe tintele multi-subword. Axa de straturi se lasa la valoarea mostenita, fiindca nimic din ea nu supravietuieste medierii pe limbi.

Multiplicitatea sesiunii se declara: 16 configuratii de extractie, 3 structurale, 3 de izotropie, 4 de frecventa, 2 encodere noi. Jurnalul avea deja 102 randuri plus 84 in arhiva.

