# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:24:18 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4154 | [+0.3291, +0.4951] | 30 | 11 | +0.1414 | [-0.2677, +0.5314] | -0.2740 | [-0.6856, +0.1246] |
| de | 570 | 193 | +0.6150 | [+0.5558, +0.6690] | 23 | 11 | +0.7015 | [+0.4399, +0.8227] | +0.0865 | [-0.1829, +0.2200] |
| en | 570 | 190 | +0.7599 | [+0.7155, +0.7970] | 30 | 10 | +0.6648 | [+0.4020, +0.8079] | -0.0951 | [-0.3588, +0.0544] |
| es | 593 | 208 | +0.6187 | [+0.5661, +0.6642] | 30 | 10 | +0.5854 | [+0.2306, +0.7825] | -0.0333 | [-0.3936, +0.1734] |
| fil | 570 | 555 | +0.4026 | [+0.3313, +0.4694] | 30 | 30 | +0.5884 | [+0.3450, +0.7558] | +0.1858 | [-0.0714, +0.3658] |
| fr | 569 | 191 | +0.4865 | [+0.4214, +0.5465] | 30 | 11 | +0.2044 | [-0.2040, +0.5707] | -0.2821 | [-0.6996, +0.0796] |
| it | 570 | 192 | +0.6094 | [+0.5554, +0.6643] | 30 | 10 | +0.5799 | [+0.3339, +0.7882] | -0.0295 | [-0.2838, +0.1882] |
| ja | 570 | 190 | +0.6016 | [+0.5413, +0.6582] | 30 | 10 | +0.6011 | [+0.4291, +0.7108] | -0.0005 | [-0.1814, +0.1229] |
| pt | 567 | 562 | +0.7182 | [+0.6708, +0.7588] | 30 | 30 | +0.7804 | [+0.6123, +0.9063] | +0.0622 | [-0.1117, +0.1943] |
| si | 600 | 578 | +0.2760 | [+0.2153, +0.3399] | 30 | 30 | +0.0156 | [-0.3603, +0.4715] | -0.2604 | [-0.6405, +0.1958] |
| **medie** | | | **+0.5503** | | | | **+0.4863** | | **-0.0640** | |

**Δ split mediu -0.0640**, sd intre limbi 0.1627, interval -0.2821 pana la +0.1858. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1414 | +0.1414 | +0.0000 |
| de | +0.7015 | +0.7015 | +0.0000 |
| en | +0.6648 | +0.6648 | +0.0000 |
| es | +0.5854 | +0.5854 | +0.0000 |
| fil | +0.5884 | +0.5884 | +0.0000 |
| fr | +0.2044 | +0.2044 | +0.0000 |
| it | +0.5799 | +0.5799 | +0.0000 |
| ja | +0.6011 | +0.6011 | +0.0000 |
| pt | +0.7804 | +0.7804 | +0.0000 |
| si | +0.0156 | +0.0156 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3843 | +0.1313 | +0.0311 | +0.0101 |
| de | +0.6201 | +0.7895 | -0.0051 | -0.0880 |
| en | +0.7591 | +0.6163 | +0.0008 | +0.0485 |
| es | +0.6008 | +0.6617 | +0.0179 | -0.0763 |
| fil | +0.4127 | +0.5288 | -0.0101 | +0.0596 |
| fr | +0.4740 | +0.2429 | +0.0125 | -0.0385 |
| it | +0.5877 | +0.5649 | +0.0217 | +0.0150 |
| ja | +0.5535 | +0.4457 | +0.0481 | +0.1554 |
| pt | +0.7246 | +0.7813 | -0.0064 | -0.0009 |
| si | +0.2889 | +0.0778 | -0.0129 | -0.0622 |
