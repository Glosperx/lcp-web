# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:52:21 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4358 | [+0.3367, +0.5215] | 30 | 11 | +0.3701 | [+0.0200, +0.6361] | -0.0657 | [-0.4318, +0.2155] |
| de | 570 | 193 | +0.5838 | [+0.5226, +0.6397] | 23 | 11 | +0.8261 | [+0.6008, +0.9290] | +0.2423 | [+0.0149, +0.3635] |
| en | 570 | 190 | +0.7819 | [+0.7433, +0.8167] | 30 | 10 | +0.6605 | [+0.3958, +0.8504] | -0.1214 | [-0.3930, +0.0698] |
| es | 593 | 208 | +0.6908 | [+0.6462, +0.7293] | 30 | 10 | +0.6578 | [+0.2904, +0.8857] | -0.0330 | [-0.3885, +0.2016] |
| fil | 570 | 555 | +0.4097 | [+0.3372, +0.4769] | 30 | 30 | +0.5419 | [+0.2770, +0.7405] | +0.1322 | [-0.1428, +0.3418] |
| fr | 569 | 191 | +0.5329 | [+0.4708, +0.5942] | 30 | 11 | +0.3151 | [+0.0921, +0.5157] | -0.2178 | [-0.4488, -0.0010] |
| it | 570 | 192 | +0.6109 | [+0.5589, +0.6638] | 30 | 10 | +0.6045 | [+0.3457, +0.7980] | -0.0064 | [-0.2699, +0.2001] |
| ja | 570 | 190 | +0.5946 | [+0.5283, +0.6571] | 30 | 10 | +0.7387 | [+0.5625, +0.8586] | +0.1441 | [-0.0445, +0.2826] |
| pt | 567 | 562 | +0.7190 | [+0.6679, +0.7627] | 30 | 30 | +0.6795 | [+0.4668, +0.8366] | -0.0394 | [-0.2611, +0.1223] |
| si | 600 | 578 | +0.1960 | [+0.1286, +0.2667] | 30 | 30 | +0.3781 | [+0.1783, +0.6077] | +0.1821 | [-0.0269, +0.4249] |
| **medie** | | | **+0.5555** | | | | **+0.5772** | | **+0.0217** | |

**Δ split mediu +0.0217**, sd intre limbi 0.1470, interval -0.2178 pana la +0.2423. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3701 | +0.3701 | +0.0000 |
| de | +0.8261 | +0.8261 | +0.0000 |
| en | +0.6605 | +0.6605 | +0.0000 |
| es | +0.6578 | +0.6578 | +0.0000 |
| fil | +0.5419 | +0.5419 | +0.0000 |
| fr | +0.3151 | +0.3151 | +0.0000 |
| it | +0.6045 | +0.6045 | +0.0000 |
| ja | +0.7387 | +0.7387 | +0.0000 |
| pt | +0.6795 | +0.6795 | +0.0000 |
| si | +0.3781 | +0.3781 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4223 | +0.4388 | +0.0135 | -0.0687 |
| de | +0.6331 | +0.8404 | -0.0493 | -0.0143 |
| en | +0.7672 | +0.5878 | +0.0147 | +0.0727 |
| es | +0.6619 | +0.6334 | +0.0289 | +0.0244 |
| fil | +0.4053 | +0.5371 | +0.0044 | +0.0048 |
| fr | +0.5200 | +0.2129 | +0.0129 | +0.1022 |
| it | +0.5997 | +0.6604 | +0.0112 | -0.0559 |
| ja | +0.5023 | +0.6268 | +0.0923 | +0.1119 |
| pt | +0.7377 | +0.7165 | -0.0187 | -0.0370 |
| si | +0.1966 | +0.2692 | -0.0006 | +0.1089 |
