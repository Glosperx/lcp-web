# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:57:25 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3798 | [+0.2898, +0.4692] | 30 | 11 | +0.2289 | [-0.1198, +0.6307] | -0.1509 | [-0.5155, +0.2598] |
| de | 570 | 193 | +0.5836 | [+0.5187, +0.6421] | 23 | 11 | +0.6381 | [+0.3845, +0.7895] | +0.0545 | [-0.2009, +0.2220] |
| en | 570 | 190 | +0.7731 | [+0.7258, +0.8137] | 30 | 10 | +0.6028 | [+0.3918, +0.8164] | -0.1702 | [-0.3806, +0.0554] |
| es | 593 | 208 | +0.6049 | [+0.5543, +0.6509] | 30 | 10 | +0.5978 | [+0.2532, +0.7784] | -0.0070 | [-0.3508, +0.1830] |
| fil | 570 | 555 | +0.4060 | [+0.3370, +0.4687] | 30 | 30 | +0.4153 | [+0.1267, +0.6661] | +0.0093 | [-0.2909, +0.2746] |
| fr | 569 | 191 | +0.4820 | [+0.4128, +0.5480] | 30 | 11 | +0.3287 | [-0.0234, +0.6084] | -0.1532 | [-0.5100, +0.1337] |
| it | 570 | 192 | +0.5474 | [+0.4857, +0.6095] | 30 | 10 | +0.5993 | [+0.3146, +0.8067] | +0.0518 | [-0.2379, +0.2697] |
| ja | 570 | 190 | +0.5798 | [+0.5163, +0.6386] | 30 | 10 | +0.5079 | [+0.3462, +0.6509] | -0.0719 | [-0.2422, +0.0790] |
| pt | 567 | 562 | +0.6832 | [+0.6349, +0.7267] | 30 | 30 | +0.7340 | [+0.5667, +0.8680] | +0.0508 | [-0.1199, +0.1893] |
| si | 600 | 578 | +0.2829 | [+0.2261, +0.3391] | 30 | 30 | +0.0898 | [-0.2778, +0.4499] | -0.1931 | [-0.5608, +0.1772] |
| **medie** | | | **+0.5323** | | | | **+0.4743** | | **-0.0580** | |

**Δ split mediu -0.0580**, sd intre limbi 0.1013, interval -0.1931 pana la +0.0545. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2289 | +0.2138 | -0.0151 |
| de | +0.6381 | +0.6363 | -0.0018 |
| en | +0.6028 | +0.5996 | -0.0032 |
| es | +0.5978 | +0.6005 | +0.0027 |
| fil | +0.4153 | +0.4277 | +0.0124 |
| fr | +0.3287 | +0.2796 | -0.0491 |
| it | +0.5993 | +0.6066 | +0.0073 |
| ja | +0.5079 | +0.4793 | -0.0286 |
| pt | +0.7340 | +0.7378 | +0.0038 |
| si | +0.0898 | +0.1356 | +0.0458 |

**Diferenta medie -0.0026**, interval -0.0491 pana la +0.0458.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3395 | +0.2472 | +0.0403 | -0.0183 |
| de | +0.5259 | +0.5908 | +0.0577 | +0.0473 |
| en | +0.7650 | +0.5697 | +0.0081 | +0.0331 |
| es | +0.5869 | +0.6699 | +0.0180 | -0.0721 |
| fil | +0.4293 | +0.3456 | -0.0233 | +0.0697 |
| fr | +0.4643 | +0.3520 | +0.0177 | -0.0233 |
| it | +0.5028 | +0.6029 | +0.0446 | -0.0036 |
| ja | +0.5260 | +0.3727 | +0.0538 | +0.1352 |
| pt | +0.6708 | +0.6795 | +0.0124 | +0.0545 |
| si | +0.2956 | +0.2325 | -0.0127 | -0.1427 |
