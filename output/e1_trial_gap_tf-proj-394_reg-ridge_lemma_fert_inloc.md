# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 13:54:50 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4136 | [+0.3228, +0.4969] | 30 | 11 | +0.1715 | [-0.3498, +0.6118] | -0.2421 | [-0.7805, +0.2174] |
| de | 570 | 193 | +0.6253 | [+0.5676, +0.6772] | 23 | 11 | +0.7810 | [+0.5718, +0.8851] | +0.1557 | [-0.0579, +0.2683] |
| en | 570 | 190 | +0.7952 | [+0.7551, +0.8300] | 30 | 10 | +0.6460 | [+0.3674, +0.7893] | -0.1492 | [-0.4280, +0.0035] |
| es | 593 | 208 | +0.6575 | [+0.6082, +0.6999] | 30 | 10 | +0.6540 | [+0.2852, +0.8630] | -0.0035 | [-0.3780, +0.2071] |
| fil | 570 | 555 | +0.3939 | [+0.3232, +0.4610] | 30 | 30 | +0.5829 | [+0.3596, +0.7431] | +0.1890 | [-0.0384, +0.3680] |
| fr | 569 | 191 | +0.4931 | [+0.4257, +0.5568] | 30 | 11 | +0.2867 | [-0.1159, +0.6447] | -0.2064 | [-0.6113, +0.1610] |
| it | 570 | 192 | +0.6122 | [+0.5559, +0.6661] | 30 | 10 | +0.5796 | [+0.3377, +0.7770] | -0.0326 | [-0.2853, +0.1778] |
| ja | 570 | 190 | +0.6341 | [+0.5791, +0.6853] | 30 | 10 | +0.5966 | [+0.4055, +0.7290] | -0.0375 | [-0.2315, +0.0979] |
| pt | 567 | 562 | +0.7448 | [+0.7028, +0.7825] | 30 | 30 | +0.8276 | [+0.6924, +0.9209] | +0.0828 | [-0.0591, +0.1854] |
| si | 600 | 578 | +0.2576 | [+0.1999, +0.3168] | 30 | 30 | +0.0973 | [-0.3041, +0.5632] | -0.1603 | [-0.5655, +0.3029] |
| **medie** | | | **+0.5627** | | | | **+0.5223** | | **-0.0404** | |

**Δ split mediu -0.0404**, sd intre limbi 0.1499, interval -0.2421 pana la +0.1890. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1715 | +0.1715 | +0.0000 |
| de | +0.7810 | +0.7810 | +0.0000 |
| en | +0.6460 | +0.6460 | +0.0000 |
| es | +0.6540 | +0.6540 | +0.0000 |
| fil | +0.5829 | +0.5829 | +0.0000 |
| fr | +0.2867 | +0.2867 | +0.0000 |
| it | +0.5796 | +0.5796 | +0.0000 |
| ja | +0.5966 | +0.5966 | +0.0000 |
| pt | +0.8276 | +0.8276 | +0.0000 |
| si | +0.0973 | +0.0973 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3758 | +0.1824 | +0.0378 | -0.0109 |
| de | +0.6472 | +0.8134 | -0.0219 | -0.0324 |
| en | +0.7811 | +0.5484 | +0.0141 | +0.0976 |
| es | +0.6248 | +0.6526 | +0.0327 | +0.0014 |
| fil | +0.3983 | +0.5384 | -0.0044 | +0.0445 |
| fr | +0.5001 | +0.3114 | -0.0070 | -0.0247 |
| it | +0.6096 | +0.5960 | +0.0026 | -0.0164 |
| ja | +0.5811 | +0.4727 | +0.0530 | +0.1239 |
| pt | +0.7561 | +0.8255 | -0.0113 | +0.0021 |
| si | +0.2670 | +0.0759 | -0.0094 | +0.0214 |
