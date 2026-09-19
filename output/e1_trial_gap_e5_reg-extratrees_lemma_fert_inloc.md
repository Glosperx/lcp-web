# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:58:06 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4222 | [+0.3434, +0.4936] | 30 | 11 | +0.4446 | [+0.0033, +0.7321] | +0.0224 | [-0.4255, +0.3288] |
| de | 570 | 193 | +0.5967 | [+0.5419, +0.6488] | 23 | 11 | +0.7347 | [+0.3871, +0.9260] | +0.1380 | [-0.2136, +0.3447] |
| en | 570 | 190 | +0.7989 | [+0.7627, +0.8323] | 30 | 10 | +0.6889 | [+0.4660, +0.8225] | -0.1100 | [-0.3344, +0.0328] |
| es | 593 | 208 | +0.6691 | [+0.6242, +0.7102] | 30 | 10 | +0.6734 | [+0.4066, +0.8423] | +0.0043 | [-0.2643, +0.1784] |
| fil | 570 | 555 | +0.4154 | [+0.3459, +0.4808] | 30 | 30 | +0.6245 | [+0.4012, +0.8249] | +0.2091 | [-0.0171, +0.4207] |
| fr | 569 | 191 | +0.5520 | [+0.4895, +0.6106] | 30 | 11 | +0.3235 | [-0.0292, +0.5901] | -0.2286 | [-0.5766, +0.0526] |
| it | 570 | 192 | +0.5971 | [+0.5426, +0.6529] | 30 | 10 | +0.7170 | [+0.5571, +0.8363] | +0.1198 | [-0.0546, +0.2554] |
| ja | 570 | 190 | +0.6036 | [+0.5394, +0.6631] | 30 | 10 | +0.6437 | [+0.3481, +0.8499] | +0.0401 | [-0.2606, +0.2550] |
| pt | 567 | 562 | +0.7665 | [+0.7269, +0.8026] | 30 | 30 | +0.7576 | [+0.5772, +0.8969] | -0.0089 | [-0.1948, +0.1325] |
| si | 600 | 578 | +0.2248 | [+0.1565, +0.2895] | 30 | 30 | +0.2366 | [-0.0610, +0.4850] | +0.0118 | [-0.2860, +0.2832] |
| **medie** | | | **+0.5646** | | | | **+0.5845** | | **+0.0198** | |

**Δ split mediu +0.0198**, sd intre limbi 0.1247, interval -0.2286 pana la +0.2091. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4446 | +0.4169 | -0.0277 |
| de | +0.7347 | +0.7267 | -0.0080 |
| en | +0.6889 | +0.6930 | +0.0041 |
| es | +0.6734 | +0.6561 | -0.0173 |
| fil | +0.6245 | +0.6236 | -0.0009 |
| fr | +0.3235 | +0.3352 | +0.0117 |
| it | +0.7170 | +0.7234 | +0.0064 |
| ja | +0.6437 | +0.6108 | -0.0329 |
| pt | +0.7576 | +0.7359 | -0.0217 |
| si | +0.2366 | +0.2749 | +0.0383 |

**Diferenta medie -0.0048**, interval -0.0329 pana la +0.0383.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4113 | +0.4791 | +0.0109 | -0.0345 |
| de | +0.6110 | +0.7856 | -0.0143 | -0.0509 |
| en | +0.8045 | +0.7001 | -0.0056 | -0.0112 |
| es | +0.6781 | +0.6837 | -0.0090 | -0.0103 |
| fil | +0.4346 | +0.6343 | -0.0192 | -0.0098 |
| fr | +0.5442 | +0.3000 | +0.0078 | +0.0235 |
| it | +0.6091 | +0.7191 | -0.0120 | -0.0021 |
| ja | +0.5942 | +0.5679 | +0.0094 | +0.0758 |
| pt | +0.7739 | +0.7689 | -0.0074 | -0.0113 |
| si | +0.2068 | -0.0588 | +0.0180 | +0.2954 |
