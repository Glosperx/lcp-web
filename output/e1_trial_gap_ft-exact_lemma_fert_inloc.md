# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:58:07 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4499 | [+0.3680, +0.5248] | 30 | 11 | +0.2277 | [-0.3002, +0.6495] | -0.2223 | [-0.7603, +0.2114] |
| de | 570 | 193 | +0.6552 | [+0.6011, +0.7037] | 23 | 11 | +0.8018 | [+0.5204, +0.9236] | +0.1466 | [-0.1484, +0.2818] |
| en | 570 | 190 | +0.8166 | [+0.7780, +0.8486] | 30 | 10 | +0.7024 | [+0.4335, +0.8508] | -0.1142 | [-0.3897, +0.0431] |
| es | 593 | 208 | +0.6651 | [+0.6188, +0.7063] | 30 | 10 | +0.6853 | [+0.3851, +0.8527] | +0.0202 | [-0.2785, +0.1921] |
| fil | 570 | 555 | +0.4065 | [+0.3340, +0.4749] | 30 | 30 | +0.5929 | [+0.3465, +0.7723] | +0.1864 | [-0.0670, +0.3788] |
| fr | 569 | 191 | +0.5287 | [+0.4605, +0.5890] | 30 | 11 | +0.3438 | [-0.0409, +0.6488] | -0.1849 | [-0.5864, +0.1335] |
| it | 570 | 192 | +0.6369 | [+0.5821, +0.6919] | 30 | 10 | +0.6490 | [+0.4054, +0.8177] | +0.0121 | [-0.2336, +0.1949] |
| ja | 570 | 190 | +0.6283 | [+0.5613, +0.6870] | 30 | 10 | +0.5756 | [+0.3852, +0.7088] | -0.0527 | [-0.2518, +0.0968] |
| pt | 567 | 562 | +0.7613 | [+0.7201, +0.7985] | 30 | 30 | +0.7979 | [+0.6429, +0.9116] | +0.0366 | [-0.1227, +0.1538] |
| si | 600 | 578 | +0.2452 | [+0.1762, +0.3163] | 30 | 30 | -0.0940 | [-0.4195, +0.3105] | -0.3392 | [-0.6713, +0.0716] |
| **medie** | | | **+0.5794** | | | | **+0.5282** | | **-0.0511** | |

**Δ split mediu -0.0511**, sd intre limbi 0.1655, interval -0.3392 pana la +0.1864. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2277 | +0.2155 | -0.0122 |
| de | +0.8018 | +0.8032 | +0.0014 |
| en | +0.7024 | +0.6805 | -0.0219 |
| es | +0.6853 | +0.6821 | -0.0032 |
| fil | +0.5929 | +0.5933 | +0.0004 |
| fr | +0.3438 | +0.3091 | -0.0347 |
| it | +0.6490 | +0.6348 | -0.0142 |
| ja | +0.5756 | +0.5348 | -0.0408 |
| pt | +0.7979 | +0.8013 | +0.0034 |
| si | -0.0940 | -0.0795 | +0.0145 |

**Diferenta medie -0.0107**, interval -0.0408 pana la +0.0145.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4162 | +0.2369 | +0.0337 | -0.0092 |
| de | +0.6623 | +0.8200 | -0.0071 | -0.0182 |
| en | +0.8077 | +0.6797 | +0.0089 | +0.0227 |
| es | +0.6520 | +0.6824 | +0.0131 | +0.0029 |
| fil | +0.4229 | +0.5577 | -0.0164 | +0.0352 |
| fr | +0.5274 | +0.3432 | +0.0013 | +0.0006 |
| it | +0.6245 | +0.6814 | +0.0124 | -0.0324 |
| ja | +0.6004 | +0.4658 | +0.0279 | +0.1098 |
| pt | +0.7672 | +0.7801 | -0.0059 | +0.0178 |
| si | +0.2481 | -0.0862 | -0.0029 | -0.0078 |
