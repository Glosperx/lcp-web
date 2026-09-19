# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:40:42 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4328 | [+0.3347, +0.5180] | 30 | 11 | +0.3530 | [-0.0048, +0.6222] | -0.0798 | [-0.4534, +0.1995] |
| de | 570 | 193 | +0.5845 | [+0.5240, +0.6404] | 23 | 11 | +0.8257 | [+0.5956, +0.9290] | +0.2411 | [+0.0026, +0.3618] |
| en | 570 | 190 | +0.7774 | [+0.7380, +0.8122] | 30 | 10 | +0.6464 | [+0.3733, +0.8384] | -0.1310 | [-0.4075, +0.0635] |
| es | 593 | 208 | +0.6852 | [+0.6410, +0.7241] | 30 | 10 | +0.6468 | [+0.2756, +0.8842] | -0.0384 | [-0.4059, +0.2047] |
| fil | 570 | 555 | +0.3995 | [+0.3274, +0.4675] | 30 | 30 | +0.5367 | [+0.2665, +0.7358] | +0.1371 | [-0.1355, +0.3516] |
| fr | 569 | 191 | +0.5295 | [+0.4669, +0.5916] | 30 | 11 | +0.3121 | [+0.0807, +0.5299] | -0.2174 | [-0.4578, +0.0117] |
| it | 570 | 192 | +0.6107 | [+0.5576, +0.6638] | 30 | 10 | +0.5968 | [+0.3370, +0.7934] | -0.0139 | [-0.2782, +0.1936] |
| ja | 570 | 190 | +0.5923 | [+0.5265, +0.6538] | 30 | 10 | +0.7367 | [+0.5646, +0.8526] | +0.1444 | [-0.0415, +0.2814] |
| pt | 567 | 562 | +0.7146 | [+0.6627, +0.7584] | 30 | 30 | +0.6739 | [+0.4572, +0.8309] | -0.0407 | [-0.2657, +0.1204] |
| si | 600 | 578 | +0.1826 | [+0.1143, +0.2542] | 30 | 30 | +0.3717 | [+0.1796, +0.6134] | +0.1890 | [-0.0189, +0.4480] |
| **medie** | | | **+0.5509** | | | | **+0.5700** | | **+0.0190** | |

**Δ split mediu +0.0190**, sd intre limbi 0.1506, interval -0.2174 pana la +0.2411. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3530 | +0.3530 | +0.0000 |
| de | +0.8257 | +0.8257 | +0.0000 |
| en | +0.6464 | +0.6464 | +0.0000 |
| es | +0.6468 | +0.6468 | +0.0000 |
| fil | +0.5367 | +0.5367 | +0.0000 |
| fr | +0.3121 | +0.3121 | +0.0000 |
| it | +0.5968 | +0.5968 | +0.0000 |
| ja | +0.7367 | +0.7367 | +0.0000 |
| pt | +0.6739 | +0.6739 | +0.0000 |
| si | +0.3717 | +0.3717 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4150 | +0.3952 | +0.0178 | -0.0422 |
| de | +0.6335 | +0.8435 | -0.0490 | -0.0178 |
| en | +0.7560 | +0.5579 | +0.0214 | +0.0885 |
| es | +0.6375 | +0.6070 | +0.0477 | +0.0398 |
| fil | +0.3970 | +0.5173 | +0.0025 | +0.0194 |
| fr | +0.5141 | +0.1774 | +0.0154 | +0.1347 |
| it | +0.5857 | +0.6421 | +0.0250 | -0.0453 |
| ja | +0.4848 | +0.6386 | +0.1075 | +0.0981 |
| pt | +0.7298 | +0.7142 | -0.0152 | -0.0403 |
| si | +0.1697 | +0.2415 | +0.0129 | +0.1302 |
