# Coada: frecventa pentru sinhaleza si filipineza

Generat de `analysis_coada.py`. Referinta e xlmr SINGUR la `last4`, adica `e1_frozen_preds_lemma_fert_inloc.csv`, ca diferenta sa fie curat efectul frecventei.

## 1. Plafonul: cat valoreaza coloana de frecventa acolo unde exista

`plafon_freq` e cat pierde bratul A cand coloana de frecventa se anuleaza. Pe `si` cifra e aproape zero PRIN CONSTRUCTIE, fiindca acolo coloana era deja goala; tocmai asta o face masura a ceea ce lipseste.

```
     referinta  nofreq  plafon_freq
ca      0.4426  0.3798       0.0628
de      0.6540  0.5836       0.0703
en      0.8173  0.7731       0.0442
es      0.6665  0.6049       0.0616
fil     0.4083  0.4060       0.0023
fr      0.5372  0.4820       0.0552
it      0.6301  0.5474       0.0827
ja      0.6011  0.5798       0.0214
pt      0.7621  0.6832       0.0789
si      0.2586  0.2829      -0.0243
```

Pe cele opt limbi cu frecventa reala, pierderea medie e **+0.0597**; pe `si` **-0.0243** si pe `fil` **+0.0023**.

## 2. Castigul, pe cele trei trepte de backoff

Brat A (`p_multi`) per limba:

```
     referinta  ft_exact  ft_prefix  ft_subword
ca      0.4426    0.4499     0.4416      0.4386
de      0.6540    0.6552     0.6639      0.6648
en      0.8173    0.8166     0.8136      0.8124
es      0.6665    0.6651     0.6671      0.6666
fil     0.4083    0.4065     0.3986      0.3892
fr      0.5372    0.5287     0.5316      0.5345
it      0.6301    0.6369     0.6431      0.6418
ja      0.6011    0.6283     0.6282      0.6272
pt      0.7621    0.7613     0.7637      0.7649
si      0.2586    0.2452     0.2733      0.2728
```

Diferenta fata de referinta:

```
     ft_exact  ft_prefix  ft_subword
ca     0.0073    -0.0010     -0.0040
de     0.0012     0.0100      0.0108
en    -0.0007    -0.0037     -0.0049
es    -0.0014     0.0006      0.0001
fil   -0.0018    -0.0097     -0.0191
fr    -0.0085    -0.0056     -0.0027
it     0.0067     0.0129      0.0117
ja     0.0271     0.0271      0.0261
pt    -0.0008     0.0015      0.0028
si    -0.0135     0.0147      0.0142
```

- `ft_exact`: si **-0.0135**, fil **-0.0018**, celelalte opt (efect indirect, prin datele de antrenare) **+0.0039**, media pe zece **+0.0016**
- `ft_prefix`: si **+0.0147**, fil **-0.0097**, celelalte opt (efect indirect, prin datele de antrenare) **+0.0052**, media pe zece **+0.0047**
- `ft_subword`: si **+0.0142**, fil **-0.0191**, celelalte opt (efect indirect, prin datele de antrenare) **+0.0050**, media pe zece **+0.0035**

Pe celelalte opt limbi diferenta NU e zero si nici nu trebuie sa fie: sub LOLO modelul care prezice limba L se antreneaza pe celelalte noua, ale caror trasaturi s-au schimbat. E efect indirect prin datele de antrenare, curat de orice efect direct, exact ca la fixul de lema.

## Fuziunea, adica cifra care conteaza

```
               r_fuz    fuz_si   fuz_fil    d_fuz  limbi_stricate
varianta                                                         
referinta   0.679888  0.409545  0.513283      NaN             NaN
nofreq      0.674770  0.404714  0.535740 -0.00511             4.0
ft_exact    0.677790  0.388145  0.516198 -0.00211             2.0
ft_prefix   0.678952  0.402482  0.516293 -0.00093             1.0
ft_subword  0.678949  0.402137  0.514727 -0.00094             1.0
```

`d_fuz` e diferenta PERECHE fata de xlmr singur. `limbi_stricate` numara limbile al caror interval pereche exclude zero in jos.

## 3. Controlul: celelalte opt limbi

Verificat separat, cu comparatie constienta de NaN (coloanele de suprafata sunt NaN pe `ja` si `si`, iar `!=` le-ar raporta ca schimbate la fiecare rulare): **0 randuri schimbate din 14082** in celelalte opt limbi, pe toate cele trei trepte. Se schimba numai `si` (600 din 600 pe test, fiindca se muta si indicatorul `freq_na`) si `fil` (105 la `exact`, 145 la `prefix`, 152 la `subword`).

## Limita de resursa, si se declara

Corpusul sinhalez are 8.03 milioane de tokeni, deci un cuvant care apare O SINGURA data primeste zipf 2.10. Aia e o PODEA: sub ea nu se poate distinge nimic, in timp ce celelalte opt limbi, servite de `wordfreq`, coboara pana la 0. Distributia lui `si` e prin urmare comprimata (sd 0.80, cea mai mica din set, fata de 0.86-1.14 la celelalte). Nu e un defect de metoda, e marimea corpusului disponibil, si e chiar observatia care merita scrisa: pe limba pe care mergem cel mai prost, rezolutia frecventei e limitata de cat text exista.

## Encoderele monolingve nu sunt compatibile cu protocolul, si de ce

Planul prevedea SinBERT si RoBERTa-Tagalog ca membri suplimentari acolo unde exista. Ideea cade pe un motiv STRUCTURAL, nu pe un scor prost, si merita scris fiindca e o limitare a protocolului nostru, nu a modelelor lor.

Sub LOLO, regresorul care prezice limba L se antreneaza pe CompLex EN plus celelalte noua limbi, embedate cu ACELASI encoder. Un encoder monolingv sinhalez nu are cum sa reprezinte franceza sau japoneza, deci antrenarea s-ar face pe reprezentari fara continut. Iar varianta cealalta, sa antrenam pe etichete sinhaleze, rupe proprietatea zero-label, care e jumatate din contributia lucrarii.

Cat de rau, masurat, ca sa nu ramana un argument teoretic. Fertilitate, adica subword-uri per tinta:

```
limba   xlmr   sinbert   roberta-tagalog
si      3.32   5.19      21.24
fil     2.37   8.61      1.66
fr      2.02   9.76      3.33
ja      3.37   5.08      9.77
en      1.88   8.93      2.22
```

SinBERT sparge celelalte noua limbi in 4.15 ori mai multe bucati decat XLM-R (mediana), iar RoBERTa-Tagalog in 1.65 ori, si pe sinhaleza cade in fallback pe octeti, 21.24 bucati per tinta. **Cifra care surprinde:** SinBERT fragmenteaza sinhaleza mai rau decat XLM-R (5.19 fata de 3.32), desi e monolingv, fiindca are un vocabular de 52.000 fata de 250.000. Deci nici macar avantajul de tokenizare pe limba proprie nu e garantat.

Ce ramane utilizabil dintr-un model monolingv, fara sa strice protocolul: un scalar per item care nu cere regresor cross-lingual, de exemplu surprisal-ul din capul de MLM. Nu s-a rulat in sesiunea asta si ramane declarat ca directie.

Contrastul cu Glot500 e exact aici: Glot500 e UN singur model aplicat la toate cele zece limbi, deci intra in protocol fara nicio regula per limba, si tokenizeaza si si fil la nivel de cuvant intreg.

