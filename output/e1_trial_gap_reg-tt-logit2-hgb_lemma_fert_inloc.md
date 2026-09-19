# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:45:10 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3977 | [+0.3164, +0.4750] | 30 | 11 | +0.4338 | [-0.0525, +0.7550] | +0.0362 | [-0.4701, +0.3636] |
| de | 570 | 193 | +0.6200 | [+0.5664, +0.6697] | 23 | 11 | +0.7332 | [+0.4370, +0.8791] | +0.1132 | [-0.1924, +0.2709] |
| en | 570 | 190 | +0.8223 | [+0.7830, +0.8554] | 30 | 10 | +0.7127 | [+0.4830, +0.8753] | -0.1096 | [-0.3447, +0.0591] |
| es | 593 | 208 | +0.6596 | [+0.6155, +0.6997] | 30 | 10 | +0.6894 | [+0.4087, +0.8571] | +0.0298 | [-0.2487, +0.2011] |
| fil | 570 | 555 | +0.4174 | [+0.3462, +0.4841] | 30 | 30 | +0.5740 | [+0.3254, +0.8056] | +0.1566 | [-0.1039, +0.3953] |
| fr | 569 | 191 | +0.5407 | [+0.4724, +0.6014] | 30 | 11 | +0.3952 | [+0.0418, +0.6528] | -0.1455 | [-0.5070, +0.1272] |
| it | 570 | 192 | +0.6047 | [+0.5482, +0.6613] | 30 | 10 | +0.6612 | [+0.4142, +0.8342] | +0.0565 | [-0.1979, +0.2492] |
| ja | 570 | 190 | +0.3553 | [+0.2803, +0.4272] | 30 | 10 | +0.3598 | [-0.0110, +0.5953] | +0.0045 | [-0.3733, +0.2432] |
| pt | 567 | 562 | +0.7563 | [+0.7166, +0.7931] | 30 | 30 | +0.7858 | [+0.6118, +0.9041] | +0.0295 | [-0.1495, +0.1522] |
| si | 600 | 578 | +0.1538 | [+0.0864, +0.2264] | 30 | 30 | -0.1098 | [-0.4633, +0.3128] | -0.2637 | [-0.6255, +0.1544] |
| **medie** | | | **+0.5328** | | | | **+0.5235** | | **-0.0092** | |

**Δ split mediu -0.0092**, sd intre limbi 0.1271, interval -0.2637 pana la +0.1566. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4338 | +0.2439 | -0.1899 |
| de | +0.7332 | +0.7177 | -0.0155 |
| en | +0.7127 | +0.6735 | -0.0392 |
| es | +0.6894 | +0.6898 | +0.0004 |
| fil | +0.5740 | +0.5725 | -0.0015 |
| fr | +0.3952 | +0.3445 | -0.0507 |
| it | +0.6612 | +0.6828 | +0.0216 |
| ja | +0.3598 | +0.2371 | -0.1227 |
| pt | +0.7858 | +0.7781 | -0.0077 |
| si | -0.1098 | -0.1107 | -0.0009 |

**Diferenta medie -0.0406**, interval -0.1899 pana la +0.0216.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4085 | +0.2590 | -0.0108 | +0.1748 |
| de | +0.6362 | +0.8102 | -0.0162 | -0.0770 |
| en | +0.8098 | +0.6963 | +0.0125 | +0.0164 |
| es | +0.6574 | +0.6894 | +0.0022 | +0.0000 |
| fil | +0.4051 | +0.5901 | +0.0123 | -0.0161 |
| fr | +0.5302 | +0.3608 | +0.0105 | +0.0344 |
| it | +0.6118 | +0.7601 | -0.0071 | -0.0989 |
| ja | +0.6003 | +0.4764 | -0.2450 | -0.1166 |
| pt | +0.7689 | +0.7780 | -0.0126 | +0.0078 |
| si | +0.2161 | -0.0936 | -0.0623 | -0.0162 |
