# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:24:02 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4391 | [+0.3535, +0.5182] | 30 | 11 | +0.4132 | [+0.0809, +0.6666] | -0.0259 | [-0.3639, +0.2492] |
| de | 570 | 193 | +0.5481 | [+0.4885, +0.6035] | 23 | 11 | +0.7634 | [+0.3742, +0.9172] | +0.2153 | [-0.1712, +0.3879] |
| en | 570 | 190 | +0.7746 | [+0.7368, +0.8097] | 30 | 10 | +0.6426 | [+0.5185, +0.8190] | -0.1320 | [-0.2625, +0.0536] |
| es | 593 | 208 | +0.6323 | [+0.5814, +0.6772] | 30 | 10 | +0.6749 | [+0.5151, +0.8100] | +0.0427 | [-0.1286, +0.1889] |
| fil | 570 | 555 | +0.4197 | [+0.3475, +0.4868] | 30 | 30 | +0.4624 | [+0.1981, +0.6837] | +0.0427 | [-0.2360, +0.2740] |
| fr | 569 | 191 | +0.5182 | [+0.4557, +0.5767] | 30 | 11 | +0.4203 | [+0.1442, +0.6385] | -0.0978 | [-0.3799, +0.1325] |
| it | 570 | 192 | +0.5776 | [+0.5230, +0.6321] | 30 | 10 | +0.6859 | [+0.4873, +0.8232] | +0.1083 | [-0.1037, +0.2637] |
| ja | 570 | 190 | +0.5297 | [+0.4527, +0.6027] | 30 | 10 | +0.6388 | [+0.3905, +0.7816] | +0.1092 | [-0.1524, +0.2702] |
| pt | 567 | 562 | +0.6995 | [+0.6546, +0.7415] | 30 | 30 | +0.6833 | [+0.4816, +0.8585] | -0.0162 | [-0.2192, +0.1604] |
| si | 600 | 578 | +0.3655 | [+0.2966, +0.4314] | 30 | 30 | +0.2519 | [-0.2463, +0.5513] | -0.1136 | [-0.6045, +0.1978] |
| **medie** | | | **+0.5504** | | | | **+0.5637** | | **+0.0133** | |

**Δ split mediu +0.0133**, sd intre limbi 0.1119, interval -0.1320 pana la +0.2153. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4132 | +0.4132 | +0.0000 |
| de | +0.7634 | +0.7634 | +0.0000 |
| en | +0.6426 | +0.6426 | +0.0000 |
| es | +0.6749 | +0.6749 | +0.0000 |
| fil | +0.4624 | +0.4624 | +0.0000 |
| fr | +0.4203 | +0.4203 | +0.0000 |
| it | +0.6859 | +0.6859 | +0.0000 |
| ja | +0.6388 | +0.6388 | +0.0000 |
| pt | +0.6833 | +0.6833 | +0.0000 |
| si | +0.2519 | +0.2519 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4316 | +0.5684 | +0.0075 | -0.1552 |
| de | +0.6091 | +0.8128 | -0.0610 | -0.0494 |
| en | +0.7823 | +0.6676 | -0.0077 | -0.0250 |
| es | +0.6557 | +0.6347 | -0.0234 | +0.0402 |
| fil | +0.4371 | +0.5175 | -0.0174 | -0.0551 |
| fr | +0.4924 | +0.3746 | +0.0258 | +0.0457 |
| it | +0.5785 | +0.7140 | -0.0009 | -0.0281 |
| ja | +0.5269 | +0.5741 | +0.0028 | +0.0647 |
| pt | +0.7157 | +0.7292 | -0.0162 | -0.0459 |
| si | +0.3217 | +0.2831 | +0.0438 | -0.0312 |
