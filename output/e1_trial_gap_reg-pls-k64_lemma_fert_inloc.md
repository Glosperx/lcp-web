# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:25:26 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4133 | [+0.3256, +0.4948] | 30 | 11 | +0.1623 | [-0.2853, +0.5865] | -0.2510 | [-0.7042, +0.1859] |
| de | 570 | 193 | +0.6064 | [+0.5468, +0.6609] | 23 | 11 | +0.7483 | [+0.4958, +0.8617] | +0.1419 | [-0.1266, +0.2712] |
| en | 570 | 190 | +0.7662 | [+0.7222, +0.8028] | 30 | 10 | +0.6504 | [+0.3984, +0.7830] | -0.1159 | [-0.3715, +0.0299] |
| es | 593 | 208 | +0.6167 | [+0.5635, +0.6621] | 30 | 10 | +0.5788 | [+0.2126, +0.7845] | -0.0379 | [-0.4025, +0.1790] |
| fil | 570 | 555 | +0.3866 | [+0.3164, +0.4545] | 30 | 30 | +0.5898 | [+0.3564, +0.7474] | +0.2032 | [-0.0426, +0.3777] |
| fr | 569 | 191 | +0.4962 | [+0.4322, +0.5559] | 30 | 11 | +0.2296 | [-0.1718, +0.5894] | -0.2665 | [-0.6797, +0.0929] |
| it | 570 | 192 | +0.6057 | [+0.5507, +0.6600] | 30 | 10 | +0.5939 | [+0.3704, +0.7906] | -0.0118 | [-0.2450, +0.1926] |
| ja | 570 | 190 | +0.5964 | [+0.5374, +0.6516] | 30 | 10 | +0.5969 | [+0.4384, +0.6980] | +0.0005 | [-0.1702, +0.1110] |
| pt | 567 | 562 | +0.7258 | [+0.6816, +0.7657] | 30 | 30 | +0.7799 | [+0.6098, +0.9023] | +0.0541 | [-0.1177, +0.1815] |
| si | 600 | 578 | +0.2534 | [+0.1902, +0.3185] | 30 | 30 | +0.0290 | [-0.3232, +0.4625] | -0.2245 | [-0.5856, +0.2127] |
| **medie** | | | **+0.5467** | | | | **+0.4959** | | **-0.0508** | |

**Δ split mediu -0.0508**, sd intre limbi 0.1626, interval -0.2665 pana la +0.2032. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1623 | +0.1623 | +0.0000 |
| de | +0.7483 | +0.7483 | +0.0000 |
| en | +0.6504 | +0.6504 | +0.0000 |
| es | +0.5788 | +0.5788 | +0.0000 |
| fil | +0.5898 | +0.5898 | +0.0000 |
| fr | +0.2296 | +0.2296 | +0.0000 |
| it | +0.5939 | +0.5939 | +0.0000 |
| ja | +0.5969 | +0.5969 | +0.0000 |
| pt | +0.7799 | +0.7799 | +0.0000 |
| si | +0.0290 | +0.0290 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3758 | +0.1448 | +0.0375 | +0.0175 |
| de | +0.6147 | +0.7937 | -0.0083 | -0.0454 |
| en | +0.7549 | +0.6031 | +0.0113 | +0.0473 |
| es | +0.5931 | +0.6372 | +0.0236 | -0.0584 |
| fil | +0.4013 | +0.5150 | -0.0147 | +0.0748 |
| fr | +0.4740 | +0.2050 | +0.0222 | +0.0246 |
| it | +0.5783 | +0.5726 | +0.0274 | +0.0213 |
| ja | +0.5264 | +0.3538 | +0.0700 | +0.2431 |
| pt | +0.7298 | +0.7842 | -0.0040 | -0.0043 |
| si | +0.2426 | -0.0134 | +0.0108 | +0.0424 |
