# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:06:57 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4464 | [+0.3655, +0.5212] | 30 | 11 | +0.2471 | [-0.3186, +0.6992] | -0.1993 | [-0.7663, +0.2764] |
| de | 570 | 193 | +0.6361 | [+0.5821, +0.6871] | 23 | 11 | +0.7420 | [+0.5158, +0.8811] | +0.1060 | [-0.1296, +0.2543] |
| en | 570 | 190 | +0.8242 | [+0.7890, +0.8545] | 30 | 10 | +0.7010 | [+0.4290, +0.8298] | -0.1232 | [-0.3995, +0.0118] |
| es | 593 | 208 | +0.6678 | [+0.6208, +0.7113] | 30 | 10 | +0.7207 | [+0.4455, +0.8741] | +0.0529 | [-0.2194, +0.2102] |
| fil | 570 | 555 | +0.4087 | [+0.3355, +0.4751] | 30 | 30 | +0.6196 | [+0.4033, +0.7816] | +0.2109 | [-0.0111, +0.3885] |
| fr | 569 | 191 | +0.5336 | [+0.4673, +0.5951] | 30 | 11 | +0.3999 | [+0.0331, +0.6870] | -0.1337 | [-0.5131, +0.1694] |
| it | 570 | 192 | +0.6234 | [+0.5697, +0.6783] | 30 | 10 | +0.6380 | [+0.4052, +0.8075] | +0.0146 | [-0.2186, +0.1962] |
| ja | 570 | 190 | +0.5940 | [+0.5363, +0.6474] | 30 | 10 | +0.4438 | [+0.2643, +0.5964] | -0.1502 | [-0.3290, +0.0081] |
| pt | 567 | 562 | +0.7731 | [+0.7323, +0.8091] | 30 | 30 | +0.8119 | [+0.6624, +0.9205] | +0.0388 | [-0.1140, +0.1536] |
| si | 600 | 578 | +0.2125 | [+0.1449, +0.2833] | 30 | 30 | -0.1806 | [-0.5217, +0.2740] | -0.3931 | [-0.7525, +0.0627] |
| **medie** | | | **+0.5720** | | | | **+0.5143** | | **-0.0576** | |

**Δ split mediu -0.0576**, sd intre limbi 0.1754, interval -0.3931 pana la +0.2109. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2471 | +0.2317 | -0.0154 |
| de | +0.7420 | +0.7509 | +0.0089 |
| en | +0.7010 | +0.6997 | -0.0013 |
| es | +0.7207 | +0.7290 | +0.0083 |
| fil | +0.6196 | +0.6283 | +0.0087 |
| fr | +0.3999 | +0.3714 | -0.0285 |
| it | +0.6380 | +0.6346 | -0.0034 |
| ja | +0.4438 | +0.4094 | -0.0344 |
| pt | +0.8119 | +0.8149 | +0.0030 |
| si | -0.1806 | -0.1296 | +0.0510 |

**Diferenta medie -0.0003**, interval -0.0344 pana la +0.0510.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4185 | +0.1687 | +0.0279 | +0.0784 |
| de | +0.6634 | +0.8166 | -0.0273 | -0.0746 |
| en | +0.8184 | +0.6298 | +0.0058 | +0.0712 |
| es | +0.6442 | +0.7382 | +0.0236 | -0.0175 |
| fil | +0.4053 | +0.5667 | +0.0034 | +0.0529 |
| fr | +0.5258 | +0.4024 | +0.0078 | -0.0025 |
| it | +0.6360 | +0.6691 | -0.0126 | -0.0311 |
| ja | +0.5969 | +0.4289 | -0.0029 | +0.0149 |
| pt | +0.7767 | +0.7862 | -0.0036 | +0.0257 |
| si | +0.2532 | -0.1935 | -0.0407 | +0.0129 |
