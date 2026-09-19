# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 13:13:38 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4289 | [+0.3511, +0.5001] | 30 | 11 | +0.3218 | [-0.1928, +0.7261] | -0.1070 | [-0.6304, +0.3068] |
| de | 570 | 193 | +0.6463 | [+0.5937, +0.6956] | 23 | 11 | +0.7957 | [+0.5991, +0.8944] | +0.1494 | [-0.0516, +0.2617] |
| en | 570 | 190 | +0.8145 | [+0.7755, +0.8466] | 30 | 10 | +0.6939 | [+0.4412, +0.8306] | -0.1206 | [-0.3739, +0.0268] |
| es | 593 | 208 | +0.6850 | [+0.6424, +0.7234] | 30 | 10 | +0.7058 | [+0.3916, +0.8879] | +0.0208 | [-0.2998, +0.2066] |
| fil | 570 | 555 | +0.4224 | [+0.3522, +0.4898] | 30 | 30 | +0.5993 | [+0.3728, +0.7749] | +0.1769 | [-0.0582, +0.3731] |
| fr | 569 | 191 | +0.5486 | [+0.4834, +0.6079] | 30 | 11 | +0.3907 | [+0.0486, +0.6688] | -0.1579 | [-0.5094, +0.1351] |
| it | 570 | 192 | +0.6292 | [+0.5751, +0.6821] | 30 | 10 | +0.6517 | [+0.4204, +0.8230] | +0.0226 | [-0.2096, +0.2083] |
| ja | 570 | 190 | +0.5948 | [+0.5334, +0.6502] | 30 | 10 | +0.5749 | [+0.3530, +0.7199] | -0.0198 | [-0.2462, +0.1376] |
| pt | 567 | 562 | +0.7656 | [+0.7252, +0.8021] | 30 | 30 | +0.7872 | [+0.6232, +0.8974] | +0.0216 | [-0.1504, +0.1385] |
| si | 600 | 578 | +0.1619 | [+0.0939, +0.2307] | 30 | 30 | +0.0405 | [-0.3435, +0.4805] | -0.1214 | [-0.5177, +0.3227] |
| **medie** | | | **+0.5697** | | | | **+0.5561** | | **-0.0135** | |

**Δ split mediu -0.0135**, sd intre limbi 0.1151, interval -0.1579 pana la +0.1769. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3218 | +0.2709 | -0.0509 |
| de | +0.7957 | +0.8070 | +0.0113 |
| en | +0.6939 | +0.6960 | +0.0021 |
| es | +0.7058 | +0.7030 | -0.0028 |
| fil | +0.5993 | +0.6143 | +0.0150 |
| fr | +0.3907 | +0.3560 | -0.0347 |
| it | +0.6517 | +0.6521 | +0.0004 |
| ja | +0.5749 | +0.5584 | -0.0165 |
| pt | +0.7872 | +0.7957 | +0.0085 |
| si | +0.0405 | +0.1053 | +0.0648 |

**Diferenta medie -0.0003**, interval -0.0509 pana la +0.0648.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3929 | +0.2096 | +0.0360 | +0.1122 |
| de | +0.6814 | +0.8429 | -0.0351 | -0.0472 |
| en | +0.8123 | +0.6498 | +0.0022 | +0.0441 |
| es | +0.6595 | +0.6899 | +0.0255 | +0.0159 |
| fil | +0.4090 | +0.5837 | +0.0134 | +0.0156 |
| fr | +0.5347 | +0.3494 | +0.0139 | +0.0413 |
| it | +0.6277 | +0.6854 | +0.0015 | -0.0337 |
| ja | +0.6017 | +0.5430 | -0.0069 | +0.0319 |
| pt | +0.7712 | +0.8013 | -0.0056 | -0.0141 |
| si | +0.1713 | +0.0284 | -0.0094 | +0.0121 |
