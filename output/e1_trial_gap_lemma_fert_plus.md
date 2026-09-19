# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-18 12:04:37 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4467 | [+0.3655, +0.5206] | 30 | 11 | +0.3245 | [-0.2010, +0.7141] | -0.1222 | [-0.6597, +0.2757] |
| de | 570 | 193 | +0.6503 | [+0.5970, +0.6986] | 23 | 11 | +0.7852 | [+0.5073, +0.9035] | +0.1349 | [-0.1570, +0.2702] |
| en | 570 | 190 | +0.8148 | [+0.7761, +0.8456] | 30 | 10 | +0.7164 | [+0.4763, +0.8558] | -0.0983 | [-0.3403, +0.0507] |
| es | 593 | 208 | +0.6683 | [+0.6226, +0.7088] | 28 | 10 | +0.7964 | [+0.6495, +0.8962] | +0.1281 | [-0.0181, +0.2342] |
| fil | 568 | 553 | +0.4174 | [+0.3478, +0.4848] | 30 | 30 | +0.6007 | [+0.3624, +0.7772] | +0.1833 | [-0.0668, +0.3705] |
| fr | 566 | 191 | +0.5385 | [+0.4722, +0.5982] | 30 | 11 | +0.3256 | [-0.0577, +0.6304] | -0.2128 | [-0.6083, +0.1042] |
| it | 562 | 192 | +0.6253 | [+0.5702, +0.6794] | 29 | 10 | +0.6634 | [+0.4356, +0.8189] | +0.0381 | [-0.1950, +0.2091] |
| ja | 570 | 190 | +0.5015 | [+0.4280, +0.5669] | 30 | 10 | +0.4230 | [+0.1671, +0.6067] | -0.0785 | [-0.3466, +0.1194] |
| pt | 562 | 557 | +0.7703 | [+0.7288, +0.8059] | 30 | 30 | +0.7897 | [+0.6338, +0.9056] | +0.0193 | [-0.1418, +0.1440] |
| si | 600 | 578 | +0.2326 | [+0.1709, +0.2964] | 30 | 30 | +0.0131 | [-0.4209, +0.4949] | -0.2194 | [-0.6544, +0.2626] |
| **medie** | | | **+0.5666** | | | | **+0.5438** | | **-0.0227** | |

**Δ split mediu -0.0227**, sd intre limbi 0.1449, interval -0.2194 pana la +0.1833. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3245 | +0.2400 | -0.0845 |
| de | +0.7852 | +0.7795 | -0.0057 |
| en | +0.7164 | +0.6959 | -0.0205 |
| es | +0.7964 | +0.7907 | -0.0057 |
| fil | +0.6007 | +0.6017 | +0.0010 |
| fr | +0.3256 | +0.2991 | -0.0265 |
| it | +0.6634 | +0.6615 | -0.0019 |
| ja | +0.4230 | +0.4007 | -0.0223 |
| pt | +0.7897 | +0.7842 | -0.0055 |
| si | +0.0131 | +0.0433 | +0.0302 |

**Diferenta medie -0.0141**, interval -0.0845 pana la +0.0302.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4166 | +0.2390 | +0.0301 | +0.0855 |
| de | +0.6613 | +0.8257 | -0.0110 | -0.0405 |
| en | +0.8094 | +0.6851 | +0.0054 | +0.0313 |
| es | +0.6564 | +0.7794 | +0.0119 | +0.0170 |
| fil | +0.4154 | +0.5486 | +0.0020 | +0.0521 |
| fr | +0.5294 | +0.3273 | +0.0091 | -0.0017 |
| it | +0.6264 | +0.6863 | -0.0011 | -0.0229 |
| ja | +0.5387 | +0.3885 | -0.0372 | +0.0345 |
| pt | +0.7791 | +0.7919 | -0.0088 | -0.0022 |
| si | +0.2657 | -0.0992 | -0.0331 | +0.1123 |
