# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:00:38 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4506 | [+0.3599, +0.5294] | 30 | 11 | +0.3426 | [-0.0610, +0.6501] | -0.1080 | [-0.5147, +0.2196] |
| de | 570 | 193 | +0.6044 | [+0.5487, +0.6565] | 23 | 11 | +0.8298 | [+0.5605, +0.9498] | +0.2254 | [-0.0407, +0.3608] |
| en | 570 | 190 | +0.7802 | [+0.7439, +0.8131] | 30 | 10 | +0.6464 | [+0.5463, +0.7914] | -0.1338 | [-0.2383, +0.0192] |
| es | 593 | 208 | +0.6721 | [+0.6252, +0.7117] | 30 | 10 | +0.6867 | [+0.4896, +0.8208] | +0.0146 | [-0.1898, +0.1558] |
| fil | 570 | 555 | +0.3918 | [+0.3199, +0.4606] | 30 | 30 | +0.5189 | [+0.2532, +0.7248] | +0.1272 | [-0.1452, +0.3482] |
| fr | 569 | 191 | +0.5625 | [+0.5047, +0.6164] | 30 | 11 | +0.4755 | [+0.2200, +0.6816] | -0.0870 | [-0.3498, +0.1289] |
| it | 570 | 192 | +0.6167 | [+0.5654, +0.6669] | 30 | 10 | +0.6735 | [+0.4936, +0.8221] | +0.0568 | [-0.1269, +0.2154] |
| ja | 570 | 190 | +0.6012 | [+0.5322, +0.6632] | 30 | 10 | +0.6676 | [+0.4144, +0.8180] | +0.0664 | [-0.2015, +0.2330] |
| pt | 567 | 562 | +0.7504 | [+0.7085, +0.7875] | 30 | 30 | +0.7146 | [+0.5218, +0.8834] | -0.0358 | [-0.2317, +0.1331] |
| si | 600 | 578 | +0.3425 | [+0.2717, +0.4087] | 30 | 30 | +0.3662 | [-0.0253, +0.6252] | +0.0236 | [-0.3707, +0.3011] |
| **medie** | | | **+0.5772** | | | | **+0.5922** | | **+0.0149** | |

**Δ split mediu +0.0149**, sd intre limbi 0.1113, interval -0.1338 pana la +0.2254. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3426 | +0.3426 | +0.0000 |
| de | +0.8298 | +0.8298 | +0.0000 |
| en | +0.6464 | +0.6464 | +0.0000 |
| es | +0.6867 | +0.6867 | +0.0000 |
| fil | +0.5189 | +0.5189 | +0.0000 |
| fr | +0.4755 | +0.4755 | +0.0000 |
| it | +0.6735 | +0.6735 | +0.0000 |
| ja | +0.6676 | +0.6676 | +0.0000 |
| pt | +0.7146 | +0.7146 | +0.0000 |
| si | +0.3662 | +0.3662 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3941 | +0.4155 | +0.0565 | -0.0729 |
| de | +0.6441 | +0.8393 | -0.0397 | -0.0095 |
| en | +0.7761 | +0.6533 | +0.0041 | -0.0069 |
| es | +0.6638 | +0.5910 | +0.0083 | +0.0957 |
| fil | +0.3975 | +0.5410 | -0.0057 | -0.0221 |
| fr | +0.5147 | +0.2989 | +0.0478 | +0.1766 |
| it | +0.6156 | +0.6551 | +0.0011 | +0.0184 |
| ja | +0.5566 | +0.5890 | +0.0446 | +0.0786 |
| pt | +0.7537 | +0.7292 | -0.0033 | -0.0146 |
| si | +0.2332 | +0.2819 | +0.1093 | +0.0843 |
