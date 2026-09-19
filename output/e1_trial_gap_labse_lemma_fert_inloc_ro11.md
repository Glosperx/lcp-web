# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-29 20:56:01 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4699 | [+0.3890, +0.5439] | 30 | 11 | +0.4374 | [+0.0861, +0.7031] | -0.0325 | [-0.3869, +0.2423] |
| de | 570 | 193 | +0.6279 | [+0.5748, +0.6792] | 23 | 11 | +0.8706 | [+0.6560, +0.9539] | +0.2426 | [+0.0282, +0.3501] |
| en | 570 | 190 | +0.8109 | [+0.7774, +0.8406] | 30 | 10 | +0.6970 | [+0.5689, +0.8271] | -0.1139 | [-0.2475, +0.0200] |
| es | 593 | 208 | +0.6955 | [+0.6529, +0.7341] | 30 | 10 | +0.7212 | [+0.4679, +0.8785] | +0.0257 | [-0.2340, +0.1936] |
| fil | 570 | 555 | +0.3914 | [+0.3205, +0.4597] | 30 | 30 | +0.5589 | [+0.3158, +0.7545] | +0.1675 | [-0.0854, +0.3816] |
| fr | 569 | 191 | +0.5254 | [+0.4633, +0.5845] | 30 | 11 | +0.4743 | [+0.2084, +0.6849] | -0.0511 | [-0.3230, +0.1702] |
| it | 570 | 192 | +0.6252 | [+0.5740, +0.6773] | 30 | 10 | +0.7328 | [+0.5667, +0.8426] | +0.1076 | [-0.0612, +0.2326] |
| ja | 570 | 190 | +0.5139 | [+0.4451, +0.5792] | 30 | 10 | +0.6463 | [+0.3465, +0.8252] | +0.1324 | [-0.1766, +0.3180] |
| pt | 567 | 562 | +0.7651 | [+0.7246, +0.8010] | 30 | 30 | +0.7392 | [+0.5508, +0.8910] | -0.0258 | [-0.2203, +0.1297] |
| ro | 1587 | 274 | +0.6985 | [+0.6637, +0.7316] | 0 | 0 | +nan | [+nan, +nan] | +nan | [+nan, +nan] |
| si | 600 | 578 | +0.3154 | [+0.2317, +0.3937] | 30 | 30 | +0.3102 | [-0.1671, +0.6495] | -0.0052 | [-0.4807, +0.3406] |
| **medie** | | | **+0.5854** | | | | **+0.6188** | | **+nan** | |

**Δ split mediu +nan**, sd intre limbi nan, interval +nan pana la +nan. Trial-ul e mai mare pe 5 din 11 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4374 | +0.4011 | -0.0363 |
| de | +0.8706 | +0.8533 | -0.0173 |
| en | +0.6970 | +0.7015 | +0.0045 |
| es | +0.7212 | +0.7149 | -0.0063 |
| fil | +0.5589 | +0.5767 | +0.0178 |
| fr | +0.4743 | +0.4679 | -0.0064 |
| it | +0.7328 | +0.7382 | +0.0054 |
| ja | +0.6463 | +0.5927 | -0.0536 |
| pt | +0.7392 | +0.7468 | +0.0076 |
| ro | +nan | +nan | +nan |
| si | +0.3102 | +0.3503 | +0.0401 |

**Diferenta medie +nan**, interval +nan pana la +nan.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4317 | +0.4129 | +0.0382 | +0.0245 |
| de | +0.6576 | +0.8882 | -0.0297 | -0.0176 |
| en | +0.8028 | +0.6958 | +0.0081 | +0.0012 |
| es | +0.6814 | +0.6302 | +0.0141 | +0.0910 |
| fil | +0.4089 | +0.5620 | -0.0175 | -0.0031 |
| fr | +0.5103 | +0.3291 | +0.0151 | +0.1452 |
| it | +0.6302 | +0.7313 | -0.0050 | +0.0015 |
| ja | +0.5803 | +0.5048 | -0.0664 | +0.1415 |
| pt | +0.7626 | +0.7791 | +0.0025 | -0.0399 |
| ro | +0.7104 | +nan | -0.0119 | +nan |
| si | +0.2605 | +0.2359 | +0.0549 | +0.0743 |
