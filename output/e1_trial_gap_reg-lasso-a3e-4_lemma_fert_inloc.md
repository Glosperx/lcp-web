# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:19:49 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4140 | [+0.3253, +0.4955] | 30 | 11 | +0.1375 | [-0.3072, +0.5656] | -0.2765 | [-0.7216, +0.1616] |
| de | 570 | 193 | +0.6208 | [+0.5632, +0.6736] | 23 | 11 | +0.7831 | [+0.5540, +0.8890] | +0.1623 | [-0.0680, +0.2814] |
| en | 570 | 190 | +0.7863 | [+0.7452, +0.8212] | 30 | 10 | +0.6650 | [+0.4143, +0.8078] | -0.1213 | [-0.3687, +0.0309] |
| es | 593 | 208 | +0.6465 | [+0.5952, +0.6904] | 30 | 10 | +0.6118 | [+0.2570, +0.8038] | -0.0346 | [-0.3866, +0.1675] |
| fil | 570 | 555 | +0.3929 | [+0.3220, +0.4601] | 30 | 30 | +0.5890 | [+0.3724, +0.7471] | +0.1961 | [-0.0303, +0.3741] |
| fr | 569 | 191 | +0.5093 | [+0.4475, +0.5664] | 30 | 11 | +0.2841 | [-0.1188, +0.6352] | -0.2252 | [-0.6427, +0.1305] |
| it | 570 | 192 | +0.6147 | [+0.5604, +0.6680] | 30 | 10 | +0.5840 | [+0.3459, +0.7853] | -0.0306 | [-0.2709, +0.1817] |
| ja | 570 | 190 | +0.6178 | [+0.5561, +0.6731] | 30 | 10 | +0.5656 | [+0.4009, +0.6775] | -0.0522 | [-0.2328, +0.0709] |
| pt | 567 | 562 | +0.7379 | [+0.6929, +0.7766] | 30 | 30 | +0.7876 | [+0.6147, +0.9139] | +0.0497 | [-0.1284, +0.1831] |
| si | 600 | 578 | +0.2533 | [+0.1917, +0.3188] | 30 | 30 | -0.0102 | [-0.4094, +0.4586] | -0.2636 | [-0.6691, +0.2088] |
| **medie** | | | **+0.5594** | | | | **+0.4998** | | **-0.0596** | |

**Δ split mediu -0.0596**, sd intre limbi 0.1660, interval -0.2765 pana la +0.1961. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1375 | +0.1375 | +0.0000 |
| de | +0.7831 | +0.7831 | +0.0000 |
| en | +0.6650 | +0.6650 | +0.0000 |
| es | +0.6118 | +0.6118 | +0.0000 |
| fil | +0.5890 | +0.5890 | +0.0000 |
| fr | +0.2841 | +0.2841 | +0.0000 |
| it | +0.5840 | +0.5840 | +0.0000 |
| ja | +0.5656 | +0.5656 | +0.0000 |
| pt | +0.7876 | +0.7876 | +0.0000 |
| si | -0.0102 | -0.0102 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3732 | +0.0933 | +0.0408 | +0.0442 |
| de | +0.6472 | +0.8059 | -0.0264 | -0.0228 |
| en | +0.7761 | +0.6257 | +0.0102 | +0.0393 |
| es | +0.6105 | +0.6364 | +0.0360 | -0.0246 |
| fil | +0.3942 | +0.5529 | -0.0013 | +0.0361 |
| fr | +0.5202 | +0.2953 | -0.0109 | -0.0112 |
| it | +0.6062 | +0.5924 | +0.0085 | -0.0084 |
| ja | +0.5544 | +0.5018 | +0.0634 | +0.0638 |
| pt | +0.7499 | +0.8043 | -0.0120 | -0.0167 |
| si | +0.2526 | +0.0315 | +0.0007 | -0.0417 |
