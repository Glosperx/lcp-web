# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 11:56:42 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4674 | [+0.3812, +0.5427] | 30 | 11 | +0.5518 | [+0.3621, +0.7175] | +0.0844 | [-0.1207, +0.2730] |
| de | 570 | 193 | +0.5742 | [+0.5155, +0.6308] | 23 | 11 | +0.8426 | [+0.5655, +0.9562] | +0.2684 | [-0.0146, +0.4049] |
| en | 570 | 190 | +0.7829 | [+0.7450, +0.8164] | 30 | 10 | +0.6523 | [+0.5479, +0.8188] | -0.1306 | [-0.2405, +0.0388] |
| es | 593 | 208 | +0.6358 | [+0.5878, +0.6805] | 30 | 10 | +0.6633 | [+0.4255, +0.8206] | +0.0275 | [-0.2260, +0.1911] |
| fil | 570 | 555 | +0.3628 | [+0.2894, +0.4320] | 30 | 30 | +0.4379 | [+0.1656, +0.6677] | +0.0752 | [-0.2102, +0.3148] |
| fr | 569 | 191 | +0.5223 | [+0.4577, +0.5820] | 30 | 11 | +0.5320 | [+0.2663, +0.7403] | +0.0097 | [-0.2543, +0.2224] |
| it | 570 | 192 | +0.5480 | [+0.4888, +0.6075] | 30 | 10 | +0.7064 | [+0.5254, +0.8364] | +0.1585 | [-0.0288, +0.3083] |
| ja | 570 | 190 | +0.4785 | [+0.4075, +0.5464] | 30 | 10 | +0.6194 | [+0.3068, +0.7950] | +0.1408 | [-0.1805, +0.3222] |
| pt | 567 | 562 | +0.7215 | [+0.6795, +0.7594] | 30 | 30 | +0.6957 | [+0.4708, +0.8902] | -0.0258 | [-0.2519, +0.1626] |
| si | 600 | 578 | +0.3453 | [+0.2874, +0.3997] | 30 | 30 | +0.2369 | [-0.1501, +0.4859] | -0.1084 | [-0.4883, +0.1414] |
| **medie** | | | **+0.5439** | | | | **+0.5938** | | **+0.0500** | |

**Δ split mediu +0.0500**, sd intre limbi 0.1225, interval -0.1306 pana la +0.2684. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.5518 | +0.5779 | +0.0261 |
| de | +0.8426 | +0.8265 | -0.0161 |
| en | +0.6523 | +0.6555 | +0.0032 |
| es | +0.6633 | +0.6492 | -0.0141 |
| fil | +0.4379 | +0.4674 | +0.0295 |
| fr | +0.5320 | +0.5301 | -0.0019 |
| it | +0.7064 | +0.6941 | -0.0123 |
| ja | +0.6194 | +0.5628 | -0.0566 |
| pt | +0.6957 | +0.7121 | +0.0164 |
| si | +0.2369 | +0.2590 | +0.0221 |

**Diferenta medie -0.0004**, interval -0.0566 pana la +0.0295.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4120 | +0.5830 | +0.0554 | -0.0312 |
| de | +0.6101 | +0.8568 | -0.0359 | -0.0142 |
| en | +0.7714 | +0.6431 | +0.0115 | +0.0092 |
| es | +0.6361 | +0.5670 | -0.0003 | +0.0963 |
| fil | +0.3326 | +0.4105 | +0.0302 | +0.0274 |
| fr | +0.4920 | +0.2671 | +0.0303 | +0.2649 |
| it | +0.5394 | +0.6891 | +0.0086 | +0.0173 |
| ja | +0.4366 | +0.5491 | +0.0419 | +0.0703 |
| pt | +0.7225 | +0.7307 | -0.0010 | -0.0350 |
| si | +0.2706 | +0.1554 | +0.0747 | +0.0815 |
