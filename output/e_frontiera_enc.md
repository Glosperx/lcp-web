# Frontiera de decorelare pe membrii semnalului A

Generat de `analysis_frontiera_enc.py`. Coloana e `p_multi`, splitul e test.

## Identitatea se verifica pe fiecare limba, nu doar pe medie

```
        n    prezis   masurat  eroare   rho_med    r_xlmr   r_labse      r_e5
lang                                                                         
ca    445  0.481350  0.481350     0.0  0.883522  0.442613  0.472848  0.471389
de    570  0.652220  0.652220    -0.0  0.904403  0.653969  0.616309  0.623006
en    570  0.833083  0.833083    -0.0  0.938259  0.817290  0.813078  0.816906
es    593  0.696165  0.696165    -0.0  0.937788  0.666483  0.671297  0.706946
fil   570  0.409303  0.409303    -0.0  0.964215  0.408300  0.395005  0.409869
fr    569  0.560082  0.560082     0.0  0.918592  0.537178  0.546024  0.550812
it    570  0.640060  0.640060    -0.0  0.927643  0.630129  0.614900  0.628264
ja    570  0.598210  0.598210    -0.0  0.830679  0.601143  0.528221  0.560944
pt    567  0.778801  0.778801     0.0  0.944166  0.762129  0.764665  0.765713
si    600  0.330644  0.330644     0.0  0.559747  0.258612  0.357966  0.217175
```

Eroarea maxima in valoare absoluta: **1.11e-16**. Nu e o aproximare buna, e o identitate algebrica.

Media pe limbi: prezis 0.597992, masurat 0.597992.

## Factorul de transmisie A -> fuziune, citit din rapoarte

Cele trei rulari au acelasi brat B si acelasi protocol, deci singura diferenta e A.

```
    sursa      r_A    r_fuz      d_A    d_fuz   factor
  un xlmr 0.580723 0.669591 0.000000 0.000000      NaN
media a 3 0.601244 0.675391 0.020521 0.005799 0.282594
media a 4 0.607890 0.675996 0.027167 0.006405 0.235754
```

Factor mediu **0.259**, factor MARGINAL de la media a 3 la media a 4 **0.091**.
Factorul scade pe masura ce A se imbunatateste, deci cel marginal e cel care guverneaza urmatorul pas.

Ca fuziunea sa urce cu bara de +0.0045, bratul A trebuie sa urce cu **+0.0174** (optimist, factorul mediu) pana la **+0.0494** (pesimist, factorul marginal).

## Ce r si ce rho ar trebui sa aiba un membru NOU. Scris inainte de a-l cauta

Membrii de acum: k = 3, suma r = 1.7309, suma rho pe perechi = 2.6427, media lor = 0.597992.

Rho maxim admis, ca sa treaca bara, pentru fiecare calitate a membrului nou:

```
r al membrului nou   rho max (optimist)   rho max (pesimist)
0.450                0.546                0.344
0.500                0.643                0.432
0.550                0.742                0.521
0.578                0.799                0.573
0.600                0.844                0.613
0.620                0.885                0.650
0.650                0.948                0.707
0.700                orice                0.802
```

Membrii de acum sunt la rho 0.846-0.887. Citind tabelul: **un membru din aceeasi familie, cu aceeasi calitate, e mort inainte de a fi rulat.** Ce trebuie cautat nu e un encoder mai bun, e unul structural diferit.

## Candidati evaluati

### `glot500`

```
       r_nou  rho_la_ceilalti  ens_prezis  ens_masurat  ens_acum  castig_A
lang                                                                      
ca    0.4249           0.8831      0.4742       0.4742    0.4813   -0.0072
de    0.6106           0.9093      0.6490       0.6490    0.6522   -0.0032
en    0.8173           0.9397      0.8355       0.8355    0.8331    0.0024
es    0.6586           0.9386      0.6921       0.6921    0.6962   -0.0041
fil   0.3945           0.9648      0.4074       0.4074    0.4093   -0.0019
fr    0.5668           0.9188      0.5678       0.5678    0.5601    0.0077
it    0.6129           0.9323      0.6385       0.6385    0.6401   -0.0015
ja    0.5466           0.8312      0.5985       0.5985    0.5982    0.0002
pt    0.7459           0.9392      0.7768       0.7768    0.7788   -0.0020
si    0.2468           0.6419      0.3227       0.3227    0.3306   -0.0079
```

r mediu al membrului nou **0.5625**, rho mediu fata de cei trei **0.8899**.
Castig pe bratul A: **-0.0018**. Prin factorul de transmisie, castig prezis pe fuziune intre **-0.0002** si **-0.0005**.
Verdict fata de bara de +0.0045: **NU trece**.

Cifra de mai sus e o PREDICTIE a frontierei plus a transmisiei. Nu inlocuieste rularea fuziunii cu interval pereche.

