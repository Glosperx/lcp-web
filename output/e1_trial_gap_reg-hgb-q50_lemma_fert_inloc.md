# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:42:25 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4097 | [+0.3301, +0.4805] | 30 | 11 | +0.3336 | [-0.1615, +0.6953] | -0.0761 | [-0.5732, +0.2869] |
| de | 570 | 193 | +0.6096 | [+0.5573, +0.6590] | 23 | 11 | +0.7332 | [+0.4416, +0.8880] | +0.1237 | [-0.1778, +0.2892] |
| en | 570 | 190 | +0.8118 | [+0.7713, +0.8458] | 30 | 10 | +0.6876 | [+0.3966, +0.8814] | -0.1242 | [-0.4167, +0.0690] |
| es | 593 | 208 | +0.6609 | [+0.6185, +0.7006] | 30 | 10 | +0.6708 | [+0.4071, +0.8438] | +0.0098 | [-0.2539, +0.1866] |
| fil | 570 | 555 | +0.4053 | [+0.3346, +0.4727] | 30 | 30 | +0.5872 | [+0.3298, +0.8149] | +0.1818 | [-0.0817, +0.4207] |
| fr | 569 | 191 | +0.5581 | [+0.4939, +0.6170] | 30 | 11 | +0.4398 | [+0.1089, +0.6646] | -0.1183 | [-0.4524, +0.1153] |
| it | 570 | 192 | +0.6001 | [+0.5452, +0.6565] | 30 | 10 | +0.6792 | [+0.4503, +0.8312] | +0.0791 | [-0.1648, +0.2468] |
| ja | 570 | 190 | +0.3343 | [+0.2516, +0.4085] | 30 | 10 | +0.3981 | [+0.0280, +0.6488] | +0.0637 | [-0.3190, +0.3239] |
| pt | 567 | 562 | +0.7626 | [+0.7242, +0.7988] | 30 | 30 | +0.7278 | [+0.5276, +0.8754] | -0.0349 | [-0.2393, +0.1154] |
| si | 600 | 578 | +0.2101 | [+0.1414, +0.2820] | 30 | 30 | -0.1551 | [-0.4959, +0.2696] | -0.3652 | [-0.7113, +0.0616] |
| **medie** | | | **+0.5363** | | | | **+0.5102** | | **-0.0261** | |

**Δ split mediu -0.0261**, sd intre limbi 0.1570, interval -0.3652 pana la +0.1818. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3336 | +0.2102 | -0.1234 |
| de | +0.7332 | +0.7311 | -0.0021 |
| en | +0.6876 | +0.6750 | -0.0126 |
| es | +0.6708 | +0.6868 | +0.0160 |
| fil | +0.5872 | +0.6169 | +0.0297 |
| fr | +0.4398 | +0.3774 | -0.0624 |
| it | +0.6792 | +0.6673 | -0.0119 |
| ja | +0.3981 | +0.3691 | -0.0290 |
| pt | +0.7278 | +0.7292 | +0.0014 |
| si | -0.1551 | -0.0909 | +0.0642 |

**Diferenta medie -0.0130**, interval -0.1234 pana la +0.0642.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4053 | +0.1891 | +0.0044 | +0.1445 |
| de | +0.6481 | +0.8025 | -0.0385 | -0.0693 |
| en | +0.8150 | +0.7369 | -0.0032 | -0.0493 |
| es | +0.6640 | +0.6726 | -0.0031 | -0.0018 |
| fil | +0.4060 | +0.5665 | -0.0007 | +0.0207 |
| fr | +0.5454 | +0.3148 | +0.0127 | +0.1250 |
| it | +0.6138 | +0.7205 | -0.0137 | -0.0413 |
| ja | +0.6100 | +0.5091 | -0.2757 | -0.1110 |
| pt | +0.7644 | +0.7932 | -0.0018 | -0.0654 |
| si | +0.2181 | -0.1283 | -0.0080 | -0.0268 |
