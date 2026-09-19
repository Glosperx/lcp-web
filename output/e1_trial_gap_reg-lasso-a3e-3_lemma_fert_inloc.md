# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:23:24 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3888 | [+0.2953, +0.4718] | 30 | 11 | +0.3384 | [-0.1225, +0.6619] | -0.0504 | [-0.5075, +0.2901] |
| de | 570 | 193 | +0.6491 | [+0.5993, +0.6961] | 23 | 11 | +0.8058 | [+0.5459, +0.9220] | +0.1568 | [-0.1094, +0.2837] |
| en | 570 | 190 | +0.7787 | [+0.7348, +0.8142] | 30 | 10 | +0.6597 | [+0.4951, +0.8270] | -0.1190 | [-0.2888, +0.0495] |
| es | 593 | 208 | +0.6544 | [+0.6081, +0.6973] | 30 | 10 | +0.6789 | [+0.3973, +0.8486] | +0.0245 | [-0.2540, +0.1992] |
| fil | 570 | 555 | +0.3922 | [+0.3205, +0.4601] | 30 | 30 | +0.5871 | [+0.3887, +0.7516] | +0.1949 | [-0.0125, +0.3813] |
| fr | 569 | 191 | +0.5555 | [+0.4925, +0.6127] | 30 | 11 | +0.3585 | [-0.0113, +0.6565] | -0.1970 | [-0.5717, +0.1083] |
| it | 570 | 192 | +0.6292 | [+0.5740, +0.6796] | 30 | 10 | +0.6421 | [+0.4184, +0.8117] | +0.0129 | [-0.2148, +0.1965] |
| ja | 570 | 190 | +0.6021 | [+0.5357, +0.6657] | 30 | 10 | +0.5607 | [+0.3389, +0.7394] | -0.0414 | [-0.2691, +0.1509] |
| pt | 567 | 562 | +0.7477 | [+0.7082, +0.7832] | 30 | 30 | +0.7915 | [+0.6296, +0.9087] | +0.0438 | [-0.1247, +0.1644] |
| si | 600 | 578 | +0.2611 | [+0.1982, +0.3267] | 30 | 30 | +0.0383 | [-0.3297, +0.4203] | -0.2228 | [-0.5830, +0.1664] |
| **medie** | | | **+0.5659** | | | | **+0.5461** | | **-0.0198** | |

**Δ split mediu -0.0198**, sd intre limbi 0.1367, interval -0.2228 pana la +0.1949. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3384 | +0.3384 | +0.0000 |
| de | +0.8058 | +0.8058 | +0.0000 |
| en | +0.6597 | +0.6597 | +0.0000 |
| es | +0.6789 | +0.6789 | +0.0000 |
| fil | +0.5871 | +0.5871 | +0.0000 |
| fr | +0.3585 | +0.3585 | +0.0000 |
| it | +0.6421 | +0.6421 | +0.0000 |
| ja | +0.5607 | +0.5607 | +0.0000 |
| pt | +0.7915 | +0.7915 | +0.0000 |
| si | +0.0383 | +0.0383 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3548 | +0.2135 | +0.0340 | +0.1249 |
| de | +0.6712 | +0.8161 | -0.0221 | -0.0103 |
| en | +0.7701 | +0.6654 | +0.0086 | -0.0057 |
| es | +0.6234 | +0.6380 | +0.0310 | +0.0409 |
| fil | +0.3845 | +0.5510 | +0.0077 | +0.0361 |
| fr | +0.5742 | +0.3700 | -0.0187 | -0.0115 |
| it | +0.6235 | +0.6475 | +0.0057 | -0.0054 |
| ja | +0.5616 | +0.5134 | +0.0405 | +0.0473 |
| pt | +0.7598 | +0.7827 | -0.0121 | +0.0088 |
| si | +0.2211 | +0.0430 | +0.0400 | -0.0047 |
