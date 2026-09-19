# Predictii scrise INAINTE de a instala sau rula orice

Pasul 1 al cererii din `PROMPT_sesiune_gbdt.md`. Scris pe 26 august 2026, inainte de
`pip install lightgbm catboost` si inainte de orice modificare de cod. Nu se rescrie; raportul final
citeaza de aici si spune explicit unde am greșit.

Motivul disciplinei, in cuvintele cererii: pe axa asta diferentele sunt de ordinul 0.001, iar o
explicatie construita dupa ce ai vazut cifra se potriveste pe orice cifra.

## Reperele fata de care prezic, toate pe xlmr, `--frozentrial --lemma-freq --afeat fert_inloc`

```
  ridge         r_A 0.5519   rho fata de hgb 0.811
  hgb           r_A 0.5472
  extratrees    r_A 0.5691   rho fata de ridge 0.858   cel mai bun al treilea membru masurat
  control ridge+hgb, media celor 10 r pe limba          0.575296
  bara pe fuziune  +0.0045, transmisie 0.259 mediu / 0.091 marginal
  deci A trebuie sa urce cu +0.0174 (optimist) .. +0.0495 (pesimist)
```

## Testul liber pe care ipoteza l-a primit deja, si care schimba forma sesiunii

Cererea spune ca axa loss-ului e complet neatinsa. Nu e: `huber` e un M-estimator robust si `svr-lin`
minimizeaza o pierdere insensibila la epsilon, amandoi in familia liniara, deci amandoi sunt exact
experimentul "acelasi model, alt loss". Din matricea rho de pe disc, `output/e_regresor_a.md`:

```
  loss schimbat, familie fixa      rho(ridge, huber)        0.980   Delta 0.020
                                   rho(ridge, svr-lin)      0.960   Delta 0.040
  familie schimbata, loss fix      rho(ridge, hgb)          0.811   Delta 0.189
                                   rho(ridge, extratrees)   0.858   Delta 0.142
                                   rho(ridge, krr-rbf)      0.880   Delta 0.120
  regularizare schimbata           rho(ridge, ridge-a30000) 0.877   Delta 0.123
  penalizare schimbata             rho(ridge, lasso-a3e-2)  0.757   Delta 0.243
```

Ordinea parghiilor, masurata: penalizare 0.24, familie 0.19, regularizare 0.12, **loss 0.02-0.04**.
Loss-ul e cea mai slaba parghie din tabel. Exista si un motiv mecanic: `r` e invariant la transformari
afine, iar pentru un model liniar directia care minimizeaza eroarea patratica e chiar directia care
maximizeaza corelatia, deci "alinierea loss-ului cu metrica" e aproape un no-op prin construcie in
familia liniara. La arbori loss-ul schimba forma functiei ne-afin, deci acolo se poate sa conteze.

Verificat si cu al doilea instrument, exact si fara nicio potrivire: `slack` = rho de care ar avea nevoie
candidatul ca sa lege la egalitate cu controlul, la r-ul lui, minus rho pe care il are. Media pe 3
encodere: `huber` +0.0122, `svr-lin` -0.0092, adica in mijlocul norului liniarilor L2 slab regularizati
(`ridge-a30` +0.0132, `ridge-a100` +0.0160). Cei doi candidati cu loss schimbat sunt nedistinsi de un
ridge cu alt alpha.

**Ipoteza ascutita, si e ea cea care se testeaza.** Nu forma functiei si nu robustetea pierderii muta
rho. Ce a rămas neatins e CE se prezice: alt functional al tintei (mediana, rang, scala marginita) si
alta incadrare (ordinal plus valoare asteptata).

## Clasele de mecanism, fixate ACUM ca sa nu poata fi atribuite dupa ce se vad reziduurile

```
  FAMILIE      alta forma de functie, acelasi loss, aceeasi tinta
               lgbm-l8, lgbmlin-l8, cat-d3, rf-n300, mlp-h128, knn-k50
               deja pe disc: hgb, hgb-adanc, extratrees, krr-rbf, pls-k*
  LOSS         acelasi obiectiv de locatie, alta pierdere; aceeasi tinta
               hgb-abs, hgb-q50
               deja pe disc: huber, svr-lin
  TINTA        se prezice alt functional al aceleiasi etichete
               tt-rank-*, ttz-rank-*, tt-logit2-*, tt-logit005-*
  INCADRARE    problema nu mai e regresie: clase plus valoare asteptata
               ord-lin-k5, ord-hgb-k5, ord-lin-k10, ord-hgb-k10, clf-hgb-k5
  INFORMATIE   acelasi obiectiv si aceeasi familie, dar model potrivit pe altceva
               rs-ridge-f3-n10, rs-hgb-f3-n10, w-ridge-c1, w-hgb-c1
               deja pe disc: extratrees, prin max_features=0.3
```

## Predictia pe fiecare candidat

`rho vs ridge` conteaza pentru rolul "X in locul lui hgb" (poarta cererii: sub 0.811 cu r_A peste 0.53).
`rho vs hgb` conteaza pentru rolul "X in locul lui ridge". Amandoua conteaza pentru rolul de al treilea
membru. `ca baza` inseamna ca prezic aceeasi cifra ca regresorul de baza al invelisului.

```
  candidat          rho vs ridge  rho vs hgb   r_A            verdict  mecanismul
  --- FAMILIE ---
  lgbm-l8            0.80-0.83    0.93-0.97   0.545-0.555      CADE   leaf-wise e o reparametrizare a
                                                                      aceleiasi familii axis-aligned
  cat-d3             0.83-0.87    0.90-0.95   0.545-0.560      CADE   arbori oblivious de adancime
                                                                      mica sunt aproape aditivi, deci
                                                                      se APROPIE de ridge
  rf-n300            0.86-0.89    0.90-0.94   0.560-0.570      CADE   un extratrees mai slab:
                                                                      bootstrap randomizeaza mai putin
  lgbmlin-l8         0.90-0.94    0.88-0.93   0.565-0.580      CADE   hibrid liniar-arbore, deci sta
                                                                      INTRE cei doi membri
  mlp-h128           0.88-0.94    0.85-0.92   0.535-0.565      CADE   dens si neted, aproximeaza
                                                                      aceeasi medie conditionala
  knn-k50            0.60-0.75    0.60-0.75   0.40-0.48        CADE   control al portii, nu speranta:
                                                                      decorelare care vine din zgomot
  --- LOSS ---
  hgb-abs            0.79-0.82    0.93-0.97   0.530-0.550      CADE   singura celula unde loss-ul mai
                                                                      poate conta: la arbori e ne-afin
  hgb-q50            0.79-0.82    0.93-0.97   0.530-0.550      CADE   duplicat al lui hgb-abs, la 0.01
  --- TINTA ---
  tt-rank-ridge      0.95-0.99    ca baza     +-0.005 de baza  CADE   rangul e monoton dar nu afin,
  tt-rank-hgb        ca baza      0.93-0.98   +-0.005 de baza  CADE   deci aproape un no-op pentru r
  ttz-rank-ridge     0.95-0.99    ca baza     +-0.005 de baza  CADE   la fel, fara inversa
  ttz-rank-hgb       ca baza      0.93-0.98   +-0.005 de baza  CADE
  tt-logit2-ridge    0.94-0.98    ca baza     +-0.005 de baza  CADE   eps 0.02 pune cele 28 de zerouri
  tt-logit2-hgb      ca baza      0.92-0.97   +-0.005 de baza  CADE   la z -2.66, deci e neutru
  tt-logit005-ridge  0.94-0.98    ca baza     -0.020..-0.005   CADE   eps 0.005 le pune la z -3.85,
                                                                      adica 28 de puncte de parghie
  --- INCADRARE ---
  ord-lin-k5         0.93-0.97      -         0.52-0.55        CADE   caroul care decide ipoteza
  ord-hgb-k5           -          0.92-0.96   0.53-0.56        CADE   acelasi, cu baza de arbori
  ord-lin-k10        0.93-0.97      -         +0.005 fata k5   CADE   mai multa rezolutie, acelasi
  ord-hgb-k10          -          0.92-0.96   +0.005 fata k5   CADE   obiectiv
  clf-hgb-k5           -          0.90-0.95   0.51-0.55        CADE   versiunea literala din cerere
  --- INFORMATIE ---
  rs-ridge-f3-n10    0.90-0.96    ca baza     +-0.005 de baza  CADE   alta informatie, nu alt obiectiv
  rs-hgb-f3-n10      ca baza      0.90-0.96   +-0.005 de baza  CADE   exact mecanismul care face
                                                                      extratrees cel mai bun al treilea
  w-ridge-c1         0.92-0.97    ca baza     -0.010..0.000    CADE   muta LOCUL erorilor direct, prin
  w-hgb-c1           ca baza      0.92-0.97   -0.010..0.000    CADE   unde e cheltuita capacitatea
```

Plafonul de cuantizare pentru axa INCADRARE e masurat, nu presupus, si NU leaga: o citire perfecta pe 5
clase de cuantile da r 0.9437 pe media celor 10 limbi, pe 10 clase 0.9815, iar incumbentul e la 0.5553.
Deci pierderea de rezolutie nu e obiectia care se poate ridica impotriva axei 3.

## Cei mai promitatori, in ordine

1. **rs-hgb-f3-n10**, clasa INFORMATIE. Singurul candidat al carui mecanism e deja masurat in proiect:
   `extratrees` e cel mai bun al treilea membru (+0.0080 pe A) si singura lui diferenta relevanta fata
   de un arbore obisnuit e `max_features=0.3`, adica exact subspatiul aleator de coloane.
2. **ord-lin-k5**, clasa INCADRARE. Singurul care schimba ce se prezice si nu doar cum, in familia in
   care celelalte parghii sunt provat inerte.
3. **rf-n300**, clasa FAMILIE. Cel mai apropiat de `extratrees`, care e incumbentul rolului de al
   treilea membru.

## Predictiile globale, si sunt cele care conteaza

1. **Niciun candidat nu trece bara.** Nimic nu urca A cu +0.0174. Cel mai bun `delta` in rolul de al
   treilea membru va fi intre +0.004 si +0.009, adica sub `extratrees` sau la egalitate cu el.
2. **La intrebarea de research raspunsul va fi NU.** Media lui `slack` pentru clasele LOSS, TINTA si
   INCADRARE va cadea la +-0.010 de media clasei FAMILIE, si amandoua in interiorul imprastierii norului
   L2 existent, care merge de la -0.107 la +0.037. Adica schimbarea obiectivului nu coboara rho
   sistematic la r comparabil.
3. **Predictia numerica pe care vreau cel mai mult sa fie testata.** `1 - rho(hgb-abs, hgb)` va ieși mai
   mare decat `1 - rho(ridge, huber) = 0.020`, fiindca la arbori loss-ul schimba forma functiei ne-afin
   iar la liniari nu. Daca iese sub 0.020, loss-ul nu conteaza nici la arbori si axa 2 se inchide
   complet, cu mecanismul explicat.
4. **Predictia care ma poate face de rusine cel mai frumos.** `cat-d3` cu rho fata de ridge SUB 0.811.
   Daca iese asa, argumentul meu despre arborii oblivious e greșit si axa 1 nu era epuizata.
5. **Prezic si o greseala de proces care NU e a mea, ca sa se vada daca a fost prinsa.** Cu codul de
   dinaintea acestei sesiuni, `analysis_regresor.py` compara fiecare candidat numai ca `X + hgb`, adica
   il pune in locul jumatatii LINIARE. Pe `extratrees`, media pe 3 encodere, cele trei roluri dau
   -0.0079 / +0.0086 / +0.0080. Deci un tabel cu un singur rol ar fi scorat toti arborii noi intr-un rol
   in care niciun arbore nu poate trece. Prezic ca fara cele doua perechiri adaugate acum, sesiunea s-ar
   fi inchis pe o cifra care nu masoara ce spune.

## Ce declar ca nefacut inainte de a incepe

Standardizarea tintei PE LIMBA in bazinul de antrenare ar fi cel mai curat candidat de clasa TINTA,
fiindca embeddingul e deja centrat pe limba dar scala lui `y` nu e. Semnatura pe care o primeste orice
regresor e insa `reg(Xtr, ytr, Xpredict)`, fara identitatea limbii, iar trecerea ei ar atinge calea
adoptata a lui A in `frozen_trial_gap`. Rămâne in afara scopului.
