# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:31:19 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4292 | [+0.3439, +0.5031] | 30 | 11 | +0.2209 | [-0.3040, +0.6703] | -0.2083 | [-0.7331, +0.2526] |
| de | 570 | 193 | +0.6365 | [+0.5803, +0.6848] | 23 | 11 | +0.7813 | [+0.5333, +0.8984] | +0.1448 | [-0.1128, +0.2774] |
| en | 570 | 190 | +0.8054 | [+0.7659, +0.8382] | 30 | 10 | +0.6727 | [+0.4386, +0.8379] | -0.1328 | [-0.3642, +0.0353] |
| es | 593 | 208 | +0.6667 | [+0.6230, +0.7049] | 30 | 10 | +0.6771 | [+0.3439, +0.8586] | +0.0104 | [-0.3260, +0.1940] |
| fil | 570 | 555 | +0.4211 | [+0.3497, +0.4877] | 30 | 30 | +0.5110 | [+0.2492, +0.7245] | +0.0899 | [-0.1692, +0.3098] |
| fr | 569 | 191 | +0.5552 | [+0.4885, +0.6147] | 30 | 11 | +0.3774 | [-0.0321, +0.6840] | -0.1778 | [-0.5974, +0.1405] |
| it | 570 | 192 | +0.6005 | [+0.5444, +0.6565] | 30 | 10 | +0.7110 | [+0.5171, +0.8483] | +0.1104 | [-0.0852, +0.2594] |
| ja | 570 | 190 | +0.5548 | [+0.4898, +0.6138] | 30 | 10 | +0.5221 | [+0.3240, +0.6533] | -0.0327 | [-0.2350, +0.1102] |
| pt | 567 | 562 | +0.7526 | [+0.7096, +0.7904] | 30 | 30 | +0.7663 | [+0.5772, +0.8975] | +0.0137 | [-0.1796, +0.1459] |
| si | 600 | 578 | +0.2864 | [+0.2249, +0.3487] | 30 | 30 | -0.0556 | [-0.4325, +0.3656] | -0.3420 | [-0.7135, +0.0815] |
| **medie** | | | **+0.5708** | | | | **+0.5184** | | **-0.0524** | |

**Δ split mediu -0.0524**, sd intre limbi 0.1580, interval -0.3420 pana la +0.1448. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2209 | +0.2160 | -0.0049 |
| de | +0.7813 | +0.7756 | -0.0057 |
| en | +0.6727 | +0.6683 | -0.0044 |
| es | +0.6771 | +0.6828 | +0.0057 |
| fil | +0.5110 | +0.5428 | +0.0318 |
| fr | +0.3774 | +0.3473 | -0.0301 |
| it | +0.7110 | +0.7069 | -0.0041 |
| ja | +0.5221 | +0.5114 | -0.0107 |
| pt | +0.7663 | +0.7644 | -0.0019 |
| si | -0.0556 | +0.0421 | +0.0977 |

**Diferenta medie +0.0073**, interval -0.0301 pana la +0.0977.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4097 | +0.2652 | +0.0195 | -0.0443 |
| de | +0.6589 | +0.8234 | -0.0224 | -0.0421 |
| en | +0.8091 | +0.6533 | -0.0037 | +0.0194 |
| es | +0.6472 | +0.6793 | +0.0195 | -0.0022 |
| fil | +0.4233 | +0.3793 | -0.0022 | +0.1317 |
| fr | +0.5085 | +0.3093 | +0.0467 | +0.0681 |
| it | +0.6052 | +0.7230 | -0.0047 | -0.0120 |
| ja | +0.5794 | +0.5022 | -0.0246 | +0.0199 |
| pt | +0.7486 | +0.7628 | +0.0040 | +0.0035 |
| si | +0.2812 | +0.1072 | +0.0052 | -0.1628 |
