# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:59:33 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4547 | [+0.3667, +0.5334] | 30 | 11 | +0.3804 | [+0.0521, +0.6105] | -0.0743 | [-0.4013, +0.1745] |
| de | 570 | 193 | +0.5682 | [+0.5078, +0.6261] | 23 | 11 | +0.7880 | [+0.4691, +0.9185] | +0.2198 | [-0.1049, +0.3646] |
| en | 570 | 190 | +0.7723 | [+0.7336, +0.8071] | 30 | 10 | +0.6531 | [+0.5154, +0.7928] | -0.1192 | [-0.2623, +0.0297] |
| es | 593 | 208 | +0.6329 | [+0.5796, +0.6805] | 30 | 10 | +0.6579 | [+0.3968, +0.8269] | +0.0250 | [-0.2285, +0.2028] |
| fil | 570 | 555 | +0.3866 | [+0.3150, +0.4572] | 30 | 30 | +0.4826 | [+0.2097, +0.6914] | +0.0960 | [-0.1809, +0.3189] |
| fr | 569 | 191 | +0.5146 | [+0.4525, +0.5713] | 30 | 11 | +0.4799 | [+0.2669, +0.6764] | -0.0348 | [-0.2525, +0.1655] |
| it | 570 | 192 | +0.5958 | [+0.5407, +0.6512] | 30 | 10 | +0.6780 | [+0.4686, +0.8226] | +0.0822 | [-0.1291, +0.2448] |
| ja | 570 | 190 | +0.5569 | [+0.4836, +0.6237] | 30 | 10 | +0.6674 | [+0.3833, +0.8261] | +0.1105 | [-0.1862, +0.2856] |
| pt | 567 | 562 | +0.7187 | [+0.6773, +0.7565] | 30 | 30 | +0.6981 | [+0.4642, +0.8815] | -0.0206 | [-0.2539, +0.1641] |
| si | 600 | 578 | +0.3437 | [+0.2674, +0.4160] | 30 | 30 | +0.2810 | [-0.2098, +0.5808] | -0.0627 | [-0.5607, +0.2440] |
| **medie** | | | **+0.5544** | | | | **+0.5766** | | **+0.0222** | |

**Δ split mediu +0.0222**, sd intre limbi 0.1041, interval -0.1192 pana la +0.2198. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3804 | +0.3804 | +0.0000 |
| de | +0.7880 | +0.7880 | +0.0000 |
| en | +0.6531 | +0.6531 | +0.0000 |
| es | +0.6579 | +0.6579 | +0.0000 |
| fil | +0.4826 | +0.4826 | +0.0000 |
| fr | +0.4799 | +0.4799 | +0.0000 |
| it | +0.6780 | +0.6780 | +0.0000 |
| ja | +0.6674 | +0.6674 | +0.0000 |
| pt | +0.6981 | +0.6981 | +0.0000 |
| si | +0.2810 | +0.2810 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4105 | +0.3589 | +0.0442 | +0.0215 |
| de | +0.6209 | +0.8476 | -0.0527 | -0.0596 |
| en | +0.7647 | +0.6678 | +0.0076 | -0.0147 |
| es | +0.6459 | +0.5646 | -0.0130 | +0.0933 |
| fil | +0.3980 | +0.4885 | -0.0114 | -0.0059 |
| fr | +0.4551 | +0.2669 | +0.0595 | +0.2130 |
| it | +0.6008 | +0.6737 | -0.0050 | +0.0043 |
| ja | +0.5234 | +0.5251 | +0.0335 | +0.1423 |
| pt | +0.7257 | +0.7526 | -0.0070 | -0.0545 |
| si | +0.2756 | +0.2931 | +0.0681 | -0.0121 |
