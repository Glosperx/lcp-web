# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:20:52 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3776 | [+0.2852, +0.4610] | 30 | 11 | +0.3987 | [-0.0011, +0.6740] | +0.0211 | [-0.3942, +0.3119] |
| de | 570 | 193 | +0.6520 | [+0.6036, +0.6994] | 23 | 11 | +0.7995 | [+0.5314, +0.9200] | +0.1474 | [-0.1293, +0.2768] |
| en | 570 | 190 | +0.7756 | [+0.7335, +0.8114] | 30 | 10 | +0.6560 | [+0.5368, +0.8077] | -0.1197 | [-0.2443, +0.0443] |
| es | 593 | 208 | +0.6425 | [+0.5949, +0.6857] | 30 | 10 | +0.6822 | [+0.4262, +0.8448] | +0.0397 | [-0.2206, +0.2075] |
| fil | 570 | 555 | +0.3940 | [+0.3225, +0.4618] | 30 | 30 | +0.5878 | [+0.3923, +0.7548] | +0.1938 | [-0.0135, +0.3794] |
| fr | 569 | 191 | +0.5632 | [+0.5030, +0.6202] | 30 | 11 | +0.3646 | [-0.0014, +0.6542] | -0.1987 | [-0.5695, +0.1013] |
| it | 570 | 192 | +0.6288 | [+0.5736, +0.6778] | 30 | 10 | +0.6465 | [+0.4351, +0.8106] | +0.0178 | [-0.2016, +0.1987] |
| ja | 570 | 190 | +0.5963 | [+0.5306, +0.6593] | 30 | 10 | +0.5513 | [+0.3163, +0.7385] | -0.0450 | [-0.2887, +0.1591] |
| pt | 567 | 562 | +0.7417 | [+0.7022, +0.7767] | 30 | 30 | +0.7668 | [+0.5901, +0.8979] | +0.0251 | [-0.1592, +0.1621] |
| si | 600 | 578 | +0.2585 | [+0.1959, +0.3220] | 30 | 30 | +0.0016 | [-0.3493, +0.3828] | -0.2568 | [-0.6151, +0.1300] |
| **medie** | | | **+0.5630** | | | | **+0.5455** | | **-0.0175** | |

**Δ split mediu -0.0175**, sd intre limbi 0.1418, interval -0.2568 pana la +0.1938. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3987 | +0.3987 | +0.0000 |
| de | +0.7995 | +0.7995 | +0.0000 |
| en | +0.6560 | +0.6560 | +0.0000 |
| es | +0.6822 | +0.6822 | +0.0000 |
| fil | +0.5878 | +0.5878 | +0.0000 |
| fr | +0.3646 | +0.3646 | +0.0000 |
| it | +0.6465 | +0.6465 | +0.0000 |
| ja | +0.5513 | +0.5513 | +0.0000 |
| pt | +0.7668 | +0.7668 | +0.0000 |
| si | +0.0016 | +0.0016 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3510 | +0.2985 | +0.0266 | +0.1002 |
| de | +0.6712 | +0.8193 | -0.0192 | -0.0198 |
| en | +0.7672 | +0.6626 | +0.0084 | -0.0066 |
| es | +0.6138 | +0.6576 | +0.0287 | +0.0246 |
| fil | +0.3831 | +0.5627 | +0.0109 | +0.0251 |
| fr | +0.5734 | +0.3692 | -0.0102 | -0.0046 |
| it | +0.6281 | +0.6470 | +0.0007 | -0.0005 |
| ja | +0.5647 | +0.5009 | +0.0316 | +0.0504 |
| pt | +0.7552 | +0.7695 | -0.0135 | -0.0027 |
| si | +0.1716 | +0.0113 | +0.0869 | -0.0097 |
