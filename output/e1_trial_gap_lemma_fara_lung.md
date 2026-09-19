# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-18 12:06:11 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4437 | [+0.3634, +0.5165] | 30 | 11 | +0.2901 | [-0.2504, +0.6859] | -0.1535 | [-0.6919, +0.2550] |
| de | 570 | 193 | +0.6541 | [+0.6003, +0.7034] | 23 | 11 | +0.7892 | [+0.5318, +0.9086] | +0.1351 | [-0.1368, +0.2684] |
| en | 570 | 190 | +0.8153 | [+0.7768, +0.8476] | 30 | 10 | +0.7249 | [+0.4845, +0.8523] | -0.0904 | [-0.3310, +0.0467] |
| es | 593 | 208 | +0.6649 | [+0.6180, +0.7078] | 28 | 10 | +0.7890 | [+0.6251, +0.8952] | +0.1241 | [-0.0400, +0.2373] |
| fil | 568 | 553 | +0.4065 | [+0.3362, +0.4737] | 30 | 30 | +0.5910 | [+0.3525, +0.7664] | +0.1845 | [-0.0670, +0.3725] |
| fr | 566 | 191 | +0.5360 | [+0.4688, +0.5962] | 30 | 11 | +0.2912 | [-0.1098, +0.6278] | -0.2447 | [-0.6620, +0.1076] |
| it | 562 | 192 | +0.6323 | [+0.5781, +0.6876] | 29 | 10 | +0.6646 | [+0.4308, +0.8229] | +0.0323 | [-0.2045, +0.2061] |
| ja | 570 | 190 | +0.5988 | [+0.5349, +0.6553] | 30 | 10 | +0.4987 | [+0.3057, +0.6327] | -0.1001 | [-0.2956, +0.0430] |
| pt | 562 | 557 | +0.7719 | [+0.7306, +0.8077] | 30 | 30 | +0.8016 | [+0.6484, +0.9134] | +0.0297 | [-0.1268, +0.1521] |
| si | 600 | 578 | +0.2191 | [+0.1540, +0.2880] | 30 | 30 | -0.1096 | [-0.4795, +0.3045] | -0.3287 | [-0.7018, +0.0902] |
| **medie** | | | **+0.5743** | | | | **+0.5331** | | **-0.0412** | |

**Δ split mediu -0.0412**, sd intre limbi 0.1707, interval -0.3287 pana la +0.1845. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2901 | +0.2855 | -0.0046 |
| de | +0.7892 | +0.7885 | -0.0007 |
| en | +0.7249 | +0.7135 | -0.0114 |
| es | +0.7890 | +0.7908 | +0.0018 |
| fil | +0.5910 | +0.5930 | +0.0020 |
| fr | +0.2912 | +0.2755 | -0.0157 |
| it | +0.6646 | +0.6656 | +0.0010 |
| ja | +0.4987 | +0.4894 | -0.0093 |
| pt | +0.8016 | +0.8022 | +0.0006 |
| si | -0.1096 | -0.1135 | -0.0039 |

**Diferenta medie -0.0040**, interval -0.0157 pana la +0.0020.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4148 | +0.2310 | +0.0289 | +0.0591 |
| de | +0.6622 | +0.8270 | -0.0081 | -0.0378 |
| en | +0.8061 | +0.6765 | +0.0092 | +0.0484 |
| es | +0.6544 | +0.7652 | +0.0105 | +0.0238 |
| fil | +0.4152 | +0.5632 | -0.0087 | +0.0278 |
| fr | +0.5331 | +0.3317 | +0.0029 | -0.0405 |
| it | +0.6243 | +0.6881 | +0.0080 | -0.0235 |
| ja | +0.5995 | +0.4704 | -0.0007 | +0.0283 |
| pt | +0.7786 | +0.7855 | -0.0067 | +0.0161 |
| si | +0.2623 | -0.0666 | -0.0432 | -0.0430 |
