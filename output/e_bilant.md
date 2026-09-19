# Bilantul sesiunii pe semnalul A

Generat de `analysis_bilant.py`. Toate cifrele vin din fisiere, niciuna nu e scrisa de mana.

Referinta pentru candidatii care schimba UN encoder e **xlmr singur la `last4`, 0.679888**. Sistemul adoptat, media a trei encodere, e **0.683849**. Bara e **+0.0045**.

```
                                               familie       r_A     r_fuz    d_fuz    d_lo    d_hi      P  stricate    fuz_si   fuz_fil  minute
candidat                                                                                                                                        
xlmr singur, last4 (REFERINTA)               referinta  0.583566  0.679888 -0.00395 -0.0066 -0.0011    0.3         3  0.409545  0.513283     NaN
sistemul: media a 3 encodere                 referinta  0.601072  0.683849  0.00395  0.0011  0.0066   99.7         0  0.425137  0.509095     NaN
labse singur                                   encoder  0.580552  0.680685  0.00079 -0.0035  0.0052   64.6         0  0.420285  0.507414     NaN
e5 singur                                      encoder  0.580393  0.680172  0.00028 -0.0035  0.0037   55.5         0  0.395992  0.512560     NaN
xlmr-large singur                              encoder  0.591469  0.679209 -0.00070 -0.0044  0.0029   34.8         1  0.403440  0.502018     NaN
Glot500 singur                                 encoder  0.572907  0.678388 -0.00148 -0.0046  0.0017   17.4         2  0.399427  0.515081     3.0
e5 cu prefixul lui                             encoder  0.581834  0.680511  0.00061 -0.0031  0.0041   63.6         1  0.400533  0.511511     2.8
pooling first                                extractie  0.584829  0.681023  0.00114 -0.0013  0.0036   81.6         0  0.416573  0.512007     2.9
pooling max                                  extractie  0.577536  0.678561 -0.00133 -0.0032  0.0006    8.6         1  0.390855  0.514733     2.8
pooling last                                 extractie  0.560944  0.675408 -0.00447 -0.0072 -0.0019    0.1         2  0.389891  0.515316     2.8
straturi mid                                 extractie  0.578452  0.678182 -0.00171 -0.0039  0.0005    6.1         0  0.397236  0.510841     2.8
straturi concat4                             extractie  0.582067  0.679309 -0.00057 -0.0026  0.0014   26.7         1  0.411463  0.517652     4.2
straturi last1                               extractie  0.576144  0.678939 -0.00095 -0.0032  0.0013   19.8         1  0.413417  0.510316     3.0
cel mai bun din grila (concat4_first)        extractie  0.578288  0.681353  0.00146 -0.0017  0.0046   82.2         0  0.413653  0.514858     3.9
contextual ++ izolat                      reprezentare  0.568508  0.676265 -0.00363 -0.0057 -0.0017    0.1         3  0.388736  0.513404     4.9
numai vectorul izolat                     reprezentare  0.509553  0.666778 -0.01311 -0.0172 -0.0090    0.0         5  0.362234  0.511863     2.5
izotropie: -1 componenta                     izotropie  0.570960  0.679120 -0.00075 -0.0022  0.0007   15.1         2  0.406543  0.515244     0.8
izotropie: -5 componente                     izotropie  0.544371  0.670542 -0.00935 -0.0124 -0.0062    0.0         3  0.381161  0.511786     0.7
izotropie: albire ZCA                        izotropie  0.574156  0.678351 -0.00155 -0.0034  0.0002    5.0         3  0.417058  0.514088     0.7
ablatie: fara frecventa                          coada  0.522624  0.674770 -0.00511 -0.0092 -0.0013    0.4         4  0.404714  0.535740     0.7
frecventa de coada, exact                        coada  0.581176  0.677790 -0.00211 -0.0053  0.0010   10.0         2  0.388145  0.516198     0.7
frecventa de coada, prefix                       coada  0.581350  0.678952 -0.00093 -0.0040  0.0021   27.3         1  0.402482  0.516293     0.7
frecventa de coada, subword                      coada  0.581329  0.678949 -0.00094 -0.0041  0.0021   27.5         1  0.402137  0.514727     0.7
indicator OOV per token                          coada  0.579190  0.678914 -0.00097 -0.0019 -0.0001    1.6         1  0.407081  0.514504     0.7
ansamblu 4, cu vectorul izolat                ansamblu  0.591655  0.681752 -0.00209 -0.0034 -0.0008    0.1         5  0.414712  0.511042     NaN
ansamblu 3, pooling first                     ansamblu  0.606299  0.686010  0.00610  0.0026  0.0095  100.0         1  0.440567  0.506283     NaN
ansamblu 3, frecventa exact                   ansamblu  0.593013  0.681283  0.00140 -0.0020  0.0050   78.4         0  0.391315  0.513950     NaN
ansamblu 3, frecventa prefix                  ansamblu  0.593992  0.682255  0.00238 -0.0010  0.0058   91.1         0  0.404370  0.514135     NaN
ansamblu 3, frecventa subword                 ansamblu  0.592254  0.682081  0.00220 -0.0013  0.0058   88.4         0  0.404930  0.512580     NaN
ansamblu 3, indicator OOV                     ansamblu  0.597198  0.683647  0.00377  0.0006  0.0068   99.0         0  0.423819  0.513553     NaN
ansamblu 3 pooling first, fata de SISTEM      ansamblu  0.606299  0.686010  0.00216  0.0004  0.0039   99.0         1  0.440567  0.506283     NaN
```

`d_fuz` e diferenta PERECHE fata de referinta proprie a rularii, cu `d_lo`/`d_hi` intervalul mediei si `P` procentul de reesantionari peste zero. `stricate` numara limbile al caror interval pereche exclude zero IN JOS; conditia se citeste INAINTEA mediei. `minute` e timpul de rulare masurat, nu estimat.

## Ce trece bara

Niciun candidat nu trece bara de +0.0045 cu zero limbi stricate.

Candidati cu semn pozitiv si nicio limba stricata, in ordine descrescatoare:

```
                                         d_fuz    d_lo    d_hi     P
candidat                                                            
sistemul: media a 3 encodere           0.00395  0.0011  0.0066  99.7
ansamblu 3, indicator OOV              0.00377  0.0006  0.0068  99.0
ansamblu 3, frecventa prefix           0.00238 -0.0010  0.0058  91.1
ansamblu 3, frecventa subword          0.00220 -0.0013  0.0058  88.4
cel mai bun din grila (concat4_first)  0.00146 -0.0017  0.0046  82.2
ansamblu 3, frecventa exact            0.00140 -0.0020  0.0050  78.4
pooling first                          0.00114 -0.0013  0.0036  81.6
labse singur                           0.00079 -0.0035  0.0052  64.6
e5 singur                              0.00028 -0.0035  0.0037  55.5
```

