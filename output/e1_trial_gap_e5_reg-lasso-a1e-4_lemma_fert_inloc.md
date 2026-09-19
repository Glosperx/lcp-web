# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:21:06 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4360 | [+0.3351, +0.5224] | 30 | 11 | +0.3789 | [+0.0320, +0.6454] | -0.0572 | [-0.4344, +0.2182] |
| de | 570 | 193 | +0.5918 | [+0.5312, +0.6465] | 23 | 11 | +0.8347 | [+0.6169, +0.9332] | +0.2429 | [+0.0190, +0.3621] |
| en | 570 | 190 | +0.7838 | [+0.7457, +0.8183] | 30 | 10 | +0.6654 | [+0.4204, +0.8494] | -0.1185 | [-0.3722, +0.0677] |
| es | 593 | 208 | +0.6905 | [+0.6456, +0.7285] | 30 | 10 | +0.6587 | [+0.3004, +0.8831] | -0.0319 | [-0.3842, +0.1977] |
| fil | 570 | 555 | +0.3997 | [+0.3276, +0.4677] | 30 | 30 | +0.5399 | [+0.2723, +0.7366] | +0.1401 | [-0.1332, +0.3490] |
| fr | 569 | 191 | +0.5367 | [+0.4745, +0.5967] | 30 | 11 | +0.3086 | [+0.0917, +0.5189] | -0.2282 | [-0.4563, -0.0029] |
| it | 570 | 192 | +0.6174 | [+0.5649, +0.6699] | 30 | 10 | +0.6108 | [+0.3589, +0.7999] | -0.0067 | [-0.2680, +0.1928] |
| ja | 570 | 190 | +0.5964 | [+0.5279, +0.6585] | 30 | 10 | +0.7343 | [+0.5505, +0.8576] | +0.1379 | [-0.0552, +0.2796] |
| pt | 567 | 562 | +0.7259 | [+0.6758, +0.7686] | 30 | 30 | +0.6909 | [+0.4833, +0.8434] | -0.0350 | [-0.2562, +0.1230] |
| si | 600 | 578 | +0.1945 | [+0.1274, +0.2660] | 30 | 30 | +0.3792 | [+0.1709, +0.6162] | +0.1847 | [-0.0350, +0.4390] |
| **medie** | | | **+0.5573** | | | | **+0.5801** | | **+0.0228** | |

**Δ split mediu +0.0228**, sd intre limbi 0.1484, interval -0.2282 pana la +0.2429. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3789 | +0.3789 | +0.0000 |
| de | +0.8347 | +0.8347 | +0.0000 |
| en | +0.6654 | +0.6654 | +0.0000 |
| es | +0.6587 | +0.6587 | +0.0000 |
| fil | +0.5399 | +0.5399 | +0.0000 |
| fr | +0.3086 | +0.3086 | +0.0000 |
| it | +0.6108 | +0.6108 | +0.0000 |
| ja | +0.7343 | +0.7343 | +0.0000 |
| pt | +0.6909 | +0.6909 | +0.0000 |
| si | +0.3792 | +0.3792 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4201 | +0.4213 | +0.0159 | -0.0424 |
| de | +0.6406 | +0.8415 | -0.0488 | -0.0068 |
| en | +0.7663 | +0.5876 | +0.0175 | +0.0778 |
| es | +0.6590 | +0.6323 | +0.0315 | +0.0264 |
| fil | +0.3988 | +0.5260 | +0.0009 | +0.0139 |
| fr | +0.5194 | +0.2218 | +0.0173 | +0.0868 |
| it | +0.6054 | +0.6507 | +0.0120 | -0.0399 |
| ja | +0.5053 | +0.6339 | +0.0911 | +0.1004 |
| pt | +0.7414 | +0.7206 | -0.0155 | -0.0297 |
| si | +0.1863 | +0.2414 | +0.0082 | +0.1378 |
