# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:39:11 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4305 | [+0.3491, +0.5072] | 30 | 11 | +0.1093 | [-0.4954, +0.6209] | -0.3212 | [-0.9506, +0.2038] |
| de | 570 | 193 | +0.5747 | [+0.5137, +0.6299] | 23 | 11 | +0.6055 | [+0.3086, +0.7924] | +0.0308 | [-0.2625, +0.2268] |
| en | 570 | 190 | +0.7955 | [+0.7538, +0.8314] | 30 | 10 | +0.6582 | [+0.4950, +0.8580] | -0.1373 | [-0.3085, +0.0627] |
| es | 593 | 208 | +0.6564 | [+0.6075, +0.6977] | 30 | 10 | +0.6602 | [+0.3408, +0.8515] | +0.0039 | [-0.3155, +0.1960] |
| fil | 570 | 555 | +0.4021 | [+0.3301, +0.4704] | 30 | 30 | +0.4858 | [+0.1932, +0.7261] | +0.0836 | [-0.2147, +0.3443] |
| fr | 569 | 191 | +0.5258 | [+0.4566, +0.5848] | 30 | 11 | +0.2920 | [-0.1231, +0.5995] | -0.2338 | [-0.6519, +0.0815] |
| it | 570 | 192 | +0.6010 | [+0.5482, +0.6568] | 30 | 10 | +0.6790 | [+0.4983, +0.8341] | +0.0780 | [-0.1095, +0.2464] |
| ja | 570 | 190 | +0.5262 | [+0.4640, +0.5884] | 30 | 10 | +0.4965 | [+0.2084, +0.6745] | -0.0297 | [-0.3140, +0.1534] |
| pt | 567 | 562 | +0.7488 | [+0.7065, +0.7863] | 30 | 30 | +0.7288 | [+0.5418, +0.8790] | -0.0200 | [-0.2094, +0.1306] |
| si | 600 | 578 | +0.1086 | [+0.0359, +0.1758] | 30 | 30 | +0.0063 | [-0.2763, +0.3632] | -0.1024 | [-0.3869, +0.2529] |
| **medie** | | | **+0.5370** | | | | **+0.4722** | | **-0.0648** | |

**Δ split mediu -0.0648**, sd intre limbi 0.1335, interval -0.3212 pana la +0.0836. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1093 | +0.0965 | -0.0128 |
| de | +0.6055 | +0.5954 | -0.0101 |
| en | +0.6582 | +0.6588 | +0.0006 |
| es | +0.6602 | +0.6574 | -0.0028 |
| fil | +0.4858 | +0.5437 | +0.0579 |
| fr | +0.2920 | +0.2844 | -0.0076 |
| it | +0.6790 | +0.6735 | -0.0055 |
| ja | +0.4965 | +0.5086 | +0.0121 |
| pt | +0.7288 | +0.7309 | +0.0021 |
| si | +0.0063 | +0.0155 | +0.0092 |

**Diferenta medie +0.0043**, interval -0.0128 pana la +0.0579.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3763 | +0.1890 | +0.0542 | -0.0797 |
| de | +0.6288 | +0.7887 | -0.0541 | -0.1832 |
| en | +0.7938 | +0.6853 | +0.0017 | -0.0271 |
| es | +0.6403 | +0.6086 | +0.0161 | +0.0516 |
| fil | +0.4184 | +0.5344 | -0.0163 | -0.0486 |
| fr | +0.5109 | +0.2487 | +0.0149 | +0.0433 |
| it | +0.5888 | +0.7030 | +0.0122 | -0.0240 |
| ja | +0.5740 | +0.4954 | -0.0478 | +0.0011 |
| pt | +0.7500 | +0.7854 | -0.0012 | -0.0566 |
| si | +0.1318 | -0.0075 | -0.0232 | +0.0138 |
