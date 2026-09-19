# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:46:25 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4326 | [+0.3513, +0.5125] | 30 | 11 | +0.3048 | [-0.1563, +0.7079] | -0.1278 | [-0.5988, +0.2884] |
| de | 570 | 193 | +0.6283 | [+0.5720, +0.6809] | 23 | 11 | +0.7062 | [+0.4410, +0.8364] | +0.0779 | [-0.1949, +0.2248] |
| en | 570 | 190 | +0.8128 | [+0.7732, +0.8456] | 30 | 10 | +0.7153 | [+0.4687, +0.8726] | -0.0974 | [-0.3461, +0.0651] |
| es | 593 | 208 | +0.6458 | [+0.5999, +0.6879] | 30 | 10 | +0.6863 | [+0.4064, +0.8409] | +0.0405 | [-0.2335, +0.2008] |
| fil | 570 | 555 | +0.4270 | [+0.3573, +0.4908] | 30 | 30 | +0.5298 | [+0.2720, +0.7226] | +0.1028 | [-0.1636, +0.3190] |
| fr | 569 | 191 | +0.5221 | [+0.4518, +0.5828] | 30 | 11 | +0.3281 | [-0.0513, +0.6316] | -0.1940 | [-0.5820, +0.1189] |
| it | 570 | 192 | +0.5988 | [+0.5411, +0.6589] | 30 | 10 | +0.6458 | [+0.3907, +0.8203] | +0.0470 | [-0.2170, +0.2363] |
| ja | 570 | 190 | +0.6369 | [+0.5756, +0.6896] | 30 | 10 | +0.5827 | [+0.4201, +0.7088] | -0.0541 | [-0.2259, +0.0818] |
| pt | 567 | 562 | +0.7381 | [+0.6929, +0.7765] | 30 | 30 | +0.7888 | [+0.6379, +0.9049] | +0.0507 | [-0.1087, +0.1721] |
| si | 600 | 578 | +0.2815 | [+0.2249, +0.3396] | 30 | 30 | +0.0478 | [-0.3280, +0.4440] | -0.2336 | [-0.6229, +0.1690] |
| **medie** | | | **+0.5724** | | | | **+0.5336** | | **-0.0388** | |

**Δ split mediu -0.0388**, sd intre limbi 0.1197, interval -0.2336 pana la +0.1028. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3048 | +0.2749 | -0.0299 |
| de | +0.7062 | +0.6971 | -0.0091 |
| en | +0.7153 | +0.7002 | -0.0151 |
| es | +0.6863 | +0.6832 | -0.0031 |
| fil | +0.5298 | +0.5383 | +0.0085 |
| fr | +0.3281 | +0.3015 | -0.0266 |
| it | +0.6458 | +0.6480 | +0.0022 |
| ja | +0.5827 | +0.5622 | -0.0205 |
| pt | +0.7888 | +0.7907 | +0.0019 |
| si | +0.0478 | +0.0802 | +0.0324 |

**Diferenta medie -0.0059**, interval -0.0299 pana la +0.0324.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4000 | +0.2944 | +0.0326 | +0.0104 |
| de | +0.5936 | +0.6464 | +0.0347 | +0.0598 |
| en | +0.8020 | +0.6690 | +0.0108 | +0.0463 |
| es | +0.6384 | +0.7323 | +0.0074 | -0.0460 |
| fil | +0.4114 | +0.4482 | +0.0156 | +0.0816 |
| fr | +0.5044 | +0.3493 | +0.0177 | -0.0212 |
| it | +0.5756 | +0.6628 | +0.0232 | -0.0170 |
| ja | +0.6085 | +0.4552 | +0.0284 | +0.1275 |
| pt | +0.7320 | +0.7469 | +0.0061 | +0.0419 |
| si | +0.2925 | +0.1357 | -0.0110 | -0.0879 |
