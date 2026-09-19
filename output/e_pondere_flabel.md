# Ponderare per limba fara etichete

Generat de `analysis_pondere_flabel.py`. Zero inferenta.

## Cei trei candidati de pondere, langa calitatea adevarata

```
             r_adevarat    fert    zipf   acord
lang membru                                    
ca   xlmr        0.4426  2.6090  0.6983  0.8823
     labse       0.4728  2.5079  0.6788  0.8782
     e5          0.4714  2.6090  0.6594  0.8901
de   xlmr        0.6540  2.5632  0.7345  0.9031
     labse       0.6163  2.3895  0.7156  0.9031
     e5          0.6230  2.5632  0.6974  0.9070
en   xlmr        0.8173  1.8842  0.8466  0.9388
     labse       0.8131  1.4333  0.8639  0.9361
     e5          0.8169  1.8842  0.8509  0.9399
es   xlmr        0.6665  1.9646  0.8353  0.9371
     labse       0.6713  1.7066  0.8334  0.9354
     e5          0.7069  1.9646  0.8168  0.9408
fil  xlmr        0.4083  2.3719  0.8820  0.9617
     labse       0.3950  1.9526  0.8793  0.9634
     e5          0.4099  2.3719  0.8784  0.9675
fr   xlmr        0.5372  2.0176  0.8073  0.9151
     labse       0.5460  1.6555  0.8278  0.9178
     e5          0.5508  2.0176  0.8149  0.9229
it   xlmr        0.6301  2.3614  0.7724  0.9209
     labse       0.6149  2.1491  0.7862  0.9316
     e5          0.6283  2.3614  0.7656  0.9305
ja   xlmr        0.6011  3.3702  0.7183  0.8273
     labse       0.5282  2.9421  0.6988  0.8260
     e5          0.5609  3.3702  0.7031  0.8388
pt   xlmr        0.7621  2.0829  0.8699  0.9452
     labse       0.7647  1.7884  0.8474  0.9452
     e5          0.7657  2.0829  0.8554  0.9421
si   xlmr        0.2586  3.3200  0.3791  0.5491
     labse       0.3580  3.2617  0.2865  0.5571
     e5          0.2172  3.3200  0.2914  0.5730
```

## Prezic ceva? Validare pe limba, nu pe medie

Trei niveluri, si numai al treilea autorizeaza o procedura care alege per limba:

```
         pe_medii  pooled_30  in_limba_spearman  n_limbi_utile
pondere                                                       
fert      -0.5643    -0.6356             0.2598             10
zipf       0.7561     0.6680            -0.2500             10
acord     -0.9687     0.6512             0.0500             10
```

`pe_medii` e corelatia peste cei 3 membri, dupa mediere pe limbi: 3 puncte, deci nu inseamna nimic singura. `pooled_30` e peste toate cele 30 de perechi (limba, membru). **`in_limba_spearman` e cifra care conteaza**: cat de bine ordoneaza ponderea membrii INAUNTRUL unei limbi, mediat peste limbi. O procedura care alege per limba are nevoie exact de asta.

## Cazul care a pus intrebarea: sinhaleza

```
       lang  r_adevarat    fert    zipf   acord
membru                                         
xlmr     si      0.2586  3.3200  0.3791  0.5491
labse    si      0.3580  3.2617  0.2865  0.5571
e5       si      0.2172  3.3200  0.2914  0.5730
```

- pondere `fert` (sens min) ar alege **labse**; adevaratul castigator e **labse**. NIMERESTE.
- pondere `zipf` (sens max) ar alege **xlmr**; adevaratul castigator e **labse**. greseste.
- pondere `acord` (sens min) ar alege **xlmr**; adevaratul castigator e **labse**. greseste.

## Ponderarea efectiva, cu exponentul ales LOLO

Ponderea unui membru pe limba L e `p_i ∝ exp(beta * s_i)`, unde `s_i` e proxy-ul standardizat in interiorul limbii. `beta = 0` e medierea uniforma de acum. `beta` se alege leave-one-language-out, ca orice alt hiperparametru.

```
         r_uniform  r_ponderat  beta_mediu  r_oracol  castig_A
pondere                                                       
fert      0.597992    0.595132       0.025  0.603016 -0.002860
zipf      0.597992    0.597163      -0.025  0.601464 -0.000828
acord     0.597992    0.597290       0.100  0.599927 -0.000701
```

`r_uniform` e medierea de acum (beta = 0). `r_oracol` foloseste etichetele limbii tinute deoparte, deci e un plafon, nu o optiune.

