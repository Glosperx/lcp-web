# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:13:42 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4407 | [+0.3644, +0.5116] | 30 | 11 | +0.3160 | [-0.2265, +0.7086] | -0.1247 | [-0.6690, +0.2775] |
| de | 570 | 193 | +0.6419 | [+0.5863, +0.6931] | 23 | 11 | +0.7594 | [+0.4844, +0.8899] | +0.1175 | [-0.1668, +0.2659] |
| en | 570 | 190 | +0.8155 | [+0.7763, +0.8477] | 30 | 10 | +0.7028 | [+0.4898, +0.8458] | -0.1127 | [-0.3328, +0.0381] |
| es | 593 | 208 | +0.6660 | [+0.6208, +0.7072] | 30 | 10 | +0.6887 | [+0.3892, +0.8611] | +0.0227 | [-0.2774, +0.1999] |
| fil | 570 | 555 | +0.4078 | [+0.3356, +0.4743] | 30 | 30 | +0.6129 | [+0.3821, +0.7826] | +0.2051 | [-0.0402, +0.3925] |
| fr | 569 | 191 | +0.5406 | [+0.4742, +0.6005] | 30 | 11 | +0.3490 | [-0.0462, +0.6498] | -0.1916 | [-0.5920, +0.1253] |
| it | 570 | 192 | +0.6198 | [+0.5645, +0.6780] | 30 | 10 | +0.6532 | [+0.4277, +0.8155] | +0.0334 | [-0.1997, +0.2078] |
| ja | 570 | 190 | +0.6118 | [+0.5500, +0.6657] | 30 | 10 | +0.5289 | [+0.3317, +0.6558] | -0.0829 | [-0.2862, +0.0572] |
| pt | 567 | 562 | +0.7635 | [+0.7245, +0.7997] | 30 | 30 | +0.8095 | [+0.6573, +0.9164] | +0.0459 | [-0.1101, +0.1596] |
| si | 600 | 578 | +0.2581 | [+0.1958, +0.3250] | 30 | 30 | -0.0951 | [-0.5346, +0.4514] | -0.3532 | [-0.8015, +0.1884] |
| **medie** | | | **+0.5766** | | | | **+0.5325** | | **-0.0440** | |

**Δ split mediu -0.0440**, sd intre limbi 0.1622, interval -0.3532 pana la +0.2051. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3160 | +0.2807 | -0.0353 |
| de | +0.7594 | +0.7526 | -0.0068 |
| en | +0.7028 | +0.6879 | -0.0149 |
| es | +0.6887 | +0.6761 | -0.0126 |
| fil | +0.6129 | +0.6090 | -0.0039 |
| fr | +0.3490 | +0.3125 | -0.0365 |
| it | +0.6532 | +0.6495 | -0.0037 |
| ja | +0.5289 | +0.4971 | -0.0318 |
| pt | +0.8095 | +0.8086 | -0.0009 |
| si | -0.0951 | -0.0385 | +0.0566 |

**Diferenta medie -0.0090**, interval -0.0365 pana la +0.0566.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4219 | +0.2360 | +0.0188 | +0.0800 |
| de | +0.6550 | +0.8099 | -0.0131 | -0.0505 |
| en | +0.8087 | +0.6800 | +0.0068 | +0.0228 |
| es | +0.6506 | +0.6822 | +0.0154 | +0.0065 |
| fil | +0.4161 | +0.5584 | -0.0083 | +0.0545 |
| fr | +0.5277 | +0.3432 | +0.0129 | +0.0058 |
| it | +0.6176 | +0.6812 | +0.0022 | -0.0280 |
| ja | +0.6007 | +0.4657 | +0.0111 | +0.0632 |
| pt | +0.7663 | +0.7800 | -0.0028 | +0.0295 |
| si | +0.2757 | -0.0215 | -0.0176 | -0.0736 |
