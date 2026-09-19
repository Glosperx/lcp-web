# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:12:01 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4625 | [+0.3722, +0.5393] | 30 | 11 | +0.3404 | [-0.0780, +0.6708] | -0.1221 | [-0.5520, +0.2182] |
| de | 570 | 193 | +0.6378 | [+0.5822, +0.6907] | 23 | 11 | +0.8399 | [+0.6370, +0.9452] | +0.2022 | [-0.0139, +0.3246] |
| en | 570 | 190 | +0.8155 | [+0.7803, +0.8468] | 30 | 10 | +0.7074 | [+0.4316, +0.8628] | -0.1081 | [-0.3935, +0.0558] |
| es | 593 | 208 | +0.7029 | [+0.6606, +0.7398] | 30 | 10 | +0.7274 | [+0.4657, +0.8859] | +0.0245 | [-0.2323, +0.1905] |
| fil | 570 | 555 | +0.3564 | [+0.2860, +0.4249] | 30 | 30 | +0.5524 | [+0.2615, +0.7712] | +0.1959 | [-0.1001, +0.4237] |
| fr | 569 | 191 | +0.5487 | [+0.4849, +0.6094] | 30 | 11 | +0.3818 | [+0.1175, +0.6030] | -0.1669 | [-0.4333, +0.0642] |
| it | 570 | 192 | +0.6474 | [+0.5977, +0.6970] | 30 | 10 | +0.6750 | [+0.4706, +0.8244] | +0.0276 | [-0.1851, +0.1940] |
| ja | 570 | 190 | +0.5940 | [+0.5206, +0.6594] | 30 | 10 | +0.7026 | [+0.4789, +0.8715] | +0.1086 | [-0.1256, +0.2936] |
| pt | 567 | 562 | +0.7649 | [+0.7187, +0.8034] | 30 | 30 | +0.7428 | [+0.5569, +0.8762] | -0.0222 | [-0.2124, +0.1166] |
| si | 600 | 578 | +0.2534 | [+0.1806, +0.3209] | 30 | 30 | +0.0603 | [-0.2602, +0.4081] | -0.1930 | [-0.5128, +0.1686] |
| **medie** | | | **+0.5784** | | | | **+0.5730** | | **-0.0054** | |

**Δ split mediu -0.0054**, sd intre limbi 0.1431, interval -0.1930 pana la +0.2022. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3404 | +0.2994 | -0.0410 |
| de | +0.8399 | +0.8424 | +0.0025 |
| en | +0.7074 | +0.7218 | +0.0144 |
| es | +0.7274 | +0.7149 | -0.0125 |
| fil | +0.5524 | +0.5454 | -0.0070 |
| fr | +0.3818 | +0.3614 | -0.0204 |
| it | +0.6750 | +0.6661 | -0.0089 |
| ja | +0.7026 | +0.6882 | -0.0144 |
| pt | +0.7428 | +0.7557 | +0.0129 |
| si | +0.0603 | +0.0842 | +0.0239 |

**Diferenta medie -0.0050**, interval -0.0410 pana la +0.0239.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4563 | +0.4084 | +0.0062 | -0.0680 |
| de | +0.6647 | +0.8674 | -0.0269 | -0.0275 |
| en | +0.8019 | +0.6779 | +0.0136 | +0.0295 |
| es | +0.6981 | +0.7042 | +0.0048 | +0.0232 |
| fil | +0.3932 | +0.5784 | -0.0368 | -0.0260 |
| fr | +0.5399 | +0.2626 | +0.0088 | +0.1192 |
| it | +0.6330 | +0.7180 | +0.0144 | -0.0430 |
| ja | +0.5707 | +0.6054 | +0.0233 | +0.0972 |
| pt | +0.7752 | +0.7533 | -0.0103 | -0.0105 |
| si | +0.2606 | +0.0658 | -0.0072 | -0.0055 |
