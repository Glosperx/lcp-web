# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 15:37:03 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4115 | [+0.3356, +0.4769] | 30 | 11 | +0.3106 | [-0.2192, +0.6893] | -0.1009 | [-0.6321, +0.2914] |
| de | 570 | 193 | +0.6414 | [+0.5889, +0.6893] | 23 | 11 | +0.7363 | [+0.3580, +0.8936] | +0.0949 | [-0.2861, +0.2677] |
| en | 570 | 190 | +0.8128 | [+0.7760, +0.8445] | 30 | 10 | +0.6943 | [+0.5635, +0.8337] | -0.1185 | [-0.2514, +0.0284] |
| es | 593 | 208 | +0.6751 | [+0.6264, +0.7188] | 30 | 10 | +0.6762 | [+0.3469, +0.8670] | +0.0010 | [-0.3354, +0.1971] |
| fil | 570 | 555 | +0.3927 | [+0.3184, +0.4609] | 30 | 30 | +0.6079 | [+0.3796, +0.7960] | +0.2152 | [-0.0303, +0.4159] |
| fr | 569 | 191 | +0.5371 | [+0.4653, +0.6011] | 30 | 11 | +0.3965 | [+0.0289, +0.6632] | -0.1405 | [-0.5172, +0.1448] |
| it | 570 | 192 | +0.5974 | [+0.5363, +0.6569] | 30 | 10 | +0.6954 | [+0.4975, +0.8460] | +0.0980 | [-0.1104, +0.2654] |
| ja | 570 | 190 | +0.5650 | [+0.5054, +0.6214] | 30 | 10 | +0.6878 | [+0.5051, +0.8401] | +0.1228 | [-0.0685, +0.2854] |
| pt | 567 | 562 | +0.7581 | [+0.7202, +0.7946] | 30 | 30 | +0.8040 | [+0.6393, +0.9104] | +0.0459 | [-0.1242, +0.1530] |
| si | 600 | 578 | +0.2122 | [+0.1393, +0.2857] | 30 | 30 | +0.2827 | [-0.1789, +0.7270] | +0.0705 | [-0.4027, +0.5203] |
| **medie** | | | **+0.5603** | | | | **+0.5892** | | **+0.0288** | |

**Δ split mediu +0.0288**, sd intre limbi 0.1168, interval -0.1405 pana la +0.2152. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3106 | +0.3676 | +0.0570 |
| de | +0.7363 | +0.7376 | +0.0013 |
| en | +0.6943 | +0.6983 | +0.0040 |
| es | +0.6762 | +0.6600 | -0.0162 |
| fil | +0.6079 | +0.5767 | -0.0312 |
| fr | +0.3965 | +0.4033 | +0.0068 |
| it | +0.6954 | +0.6964 | +0.0010 |
| ja | +0.6878 | +0.5744 | -0.1134 |
| pt | +0.8040 | +0.8158 | +0.0118 |
| si | +0.2827 | +0.2550 | -0.0277 |

**Diferenta medie -0.0107**, interval -0.1134 pana la +0.0570.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3801 | +0.2573 | +0.0314 | +0.0533 |
| de | +0.6640 | +0.8703 | -0.0226 | -0.1340 |
| en | +0.8187 | +0.6997 | -0.0059 | -0.0054 |
| es | +0.6525 | +0.6857 | +0.0226 | -0.0095 |
| fil | +0.4095 | +0.5660 | -0.0168 | +0.0419 |
| fr | +0.4981 | +0.3858 | +0.0390 | +0.0107 |
| it | +0.6170 | +0.7312 | -0.0196 | -0.0358 |
| ja | +0.6201 | +0.5774 | -0.0551 | +0.1104 |
| pt | +0.7752 | +0.7684 | -0.0171 | +0.0356 |
| si | +0.1766 | -0.0519 | +0.0356 | +0.3346 |
