# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:43:12 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4230 | [+0.3357, +0.5026] | 30 | 11 | +0.2403 | [-0.2198, +0.6391] | -0.1827 | [-0.6544, +0.2306] |
| de | 570 | 193 | +0.6511 | [+0.5982, +0.6981] | 23 | 11 | +0.6897 | [+0.4241, +0.8661] | +0.0386 | [-0.2345, +0.2211] |
| en | 570 | 190 | +0.8084 | [+0.7665, +0.8423] | 30 | 10 | +0.6752 | [+0.2356, +0.8425] | -0.1332 | [-0.5807, +0.0436] |
| es | 593 | 208 | +0.6659 | [+0.6185, +0.7077] | 30 | 10 | +0.6589 | [+0.3521, +0.8277] | -0.0070 | [-0.3084, +0.1737] |
| fil | 570 | 555 | +0.3940 | [+0.3235, +0.4620] | 30 | 30 | +0.5701 | [+0.3126, +0.7663] | +0.1761 | [-0.0827, +0.3842] |
| fr | 569 | 191 | +0.5523 | [+0.4881, +0.6112] | 30 | 11 | +0.3788 | [-0.0659, +0.7115] | -0.1734 | [-0.6257, +0.1639] |
| it | 570 | 192 | +0.5868 | [+0.5288, +0.6478] | 30 | 10 | +0.6662 | [+0.4503, +0.8402] | +0.0794 | [-0.1484, +0.2665] |
| ja | 570 | 190 | +0.5699 | [+0.5078, +0.6245] | 30 | 10 | +0.5102 | [+0.2842, +0.6698] | -0.0597 | [-0.2924, +0.1185] |
| pt | 567 | 562 | +0.7449 | [+0.7002, +0.7828] | 30 | 30 | +0.7726 | [+0.5905, +0.8922] | +0.0277 | [-0.1626, +0.1561] |
| si | 600 | 578 | +0.2109 | [+0.1451, +0.2769] | 30 | 30 | +0.0302 | [-0.4160, +0.5403] | -0.1806 | [-0.6351, +0.3369] |
| **medie** | | | **+0.5607** | | | | **+0.5192** | | **-0.0415** | |

**Δ split mediu -0.0415**, sd intre limbi 0.1246, interval -0.1827 pana la +0.1761. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2403 | +0.2033 | -0.0370 |
| de | +0.6897 | +0.6808 | -0.0089 |
| en | +0.6752 | +0.6515 | -0.0237 |
| es | +0.6589 | +0.6642 | +0.0053 |
| fil | +0.5701 | +0.5872 | +0.0171 |
| fr | +0.3788 | +0.3590 | -0.0198 |
| it | +0.6662 | +0.6676 | +0.0014 |
| ja | +0.5102 | +0.4884 | -0.0218 |
| pt | +0.7726 | +0.7712 | -0.0014 |
| si | +0.0302 | +0.0703 | +0.0401 |

**Diferenta medie -0.0049**, interval -0.0370 pana la +0.0401.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4114 | +0.2856 | +0.0116 | -0.0453 |
| de | +0.6423 | +0.7959 | +0.0088 | -0.1062 |
| en | +0.7959 | +0.6613 | +0.0125 | +0.0139 |
| es | +0.6283 | +0.6150 | +0.0376 | +0.0439 |
| fil | +0.3926 | +0.4425 | +0.0014 | +0.1276 |
| fr | +0.5231 | +0.3487 | +0.0292 | +0.0301 |
| it | +0.6023 | +0.6313 | -0.0155 | +0.0349 |
| ja | +0.5192 | +0.4126 | +0.0507 | +0.0976 |
| pt | +0.7462 | +0.7671 | -0.0013 | +0.0055 |
| si | +0.1772 | +0.2242 | +0.0337 | -0.1940 |
