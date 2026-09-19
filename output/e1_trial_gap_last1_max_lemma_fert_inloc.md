# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:27:10 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3925 | [+0.3050, +0.4741] | 30 | 11 | +0.1684 | [-0.3592, +0.5625] | -0.2240 | [-0.7592, +0.1846] |
| de | 570 | 193 | +0.6421 | [+0.5918, +0.6916] | 23 | 11 | +0.7406 | [+0.4898, +0.8829] | +0.0985 | [-0.1538, +0.2498] |
| en | 570 | 190 | +0.8121 | [+0.7721, +0.8461] | 30 | 10 | +0.7131 | [+0.5173, +0.8566] | -0.0990 | [-0.2999, +0.0510] |
| es | 593 | 208 | +0.6760 | [+0.6302, +0.7167] | 30 | 10 | +0.6510 | [+0.3487, +0.8318] | -0.0250 | [-0.3313, +0.1571] |
| fil | 570 | 555 | +0.4029 | [+0.3323, +0.4679] | 30 | 30 | +0.6162 | [+0.4003, +0.7959] | +0.2133 | [-0.0120, +0.4026] |
| fr | 569 | 191 | +0.5571 | [+0.4909, +0.6171] | 30 | 11 | +0.3390 | [-0.0423, +0.6532] | -0.2181 | [-0.6086, +0.0984] |
| it | 570 | 192 | +0.5950 | [+0.5365, +0.6545] | 30 | 10 | +0.6529 | [+0.4193, +0.8264] | +0.0578 | [-0.1852, +0.2445] |
| ja | 570 | 190 | +0.5764 | [+0.5159, +0.6315] | 30 | 10 | +0.5808 | [+0.3446, +0.7515] | +0.0044 | [-0.2370, +0.1757] |
| pt | 567 | 562 | +0.7481 | [+0.7071, +0.7850] | 30 | 30 | +0.8052 | [+0.6479, +0.9123] | +0.0571 | [-0.1052, +0.1715] |
| si | 600 | 578 | +0.1950 | [+0.1280, +0.2625] | 30 | 30 | -0.0533 | [-0.4012, +0.3399] | -0.2483 | [-0.6143, +0.1525] |
| **medie** | | | **+0.5597** | | | | **+0.5214** | | **-0.0383** | |

**Δ split mediu -0.0383**, sd intre limbi 0.1553, interval -0.2483 pana la +0.2133. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1684 | +0.1230 | -0.0454 |
| de | +0.7406 | +0.7474 | +0.0068 |
| en | +0.7131 | +0.7071 | -0.0060 |
| es | +0.6510 | +0.6577 | +0.0067 |
| fil | +0.6162 | +0.6298 | +0.0136 |
| fr | +0.3390 | +0.2993 | -0.0397 |
| it | +0.6529 | +0.6500 | -0.0029 |
| ja | +0.5808 | +0.5914 | +0.0106 |
| pt | +0.8052 | +0.8039 | -0.0013 |
| si | -0.0533 | -0.0043 | +0.0490 |

**Diferenta medie -0.0009**, interval -0.0454 pana la +0.0490.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3669 | +0.1252 | +0.0256 | +0.0432 |
| de | +0.6525 | +0.8250 | -0.0104 | -0.0844 |
| en | +0.8033 | +0.6219 | +0.0088 | +0.0912 |
| es | +0.6562 | +0.6343 | +0.0198 | +0.0167 |
| fil | +0.3969 | +0.5783 | +0.0060 | +0.0379 |
| fr | +0.5314 | +0.3510 | +0.0257 | -0.0120 |
| it | +0.6162 | +0.6363 | -0.0212 | +0.0166 |
| ja | +0.5681 | +0.4808 | +0.0083 | +0.1000 |
| pt | +0.7540 | +0.7830 | -0.0059 | +0.0222 |
| si | +0.1547 | +0.0741 | +0.0403 | -0.1274 |
