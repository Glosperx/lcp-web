# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:30:39 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4016 | [+0.3199, +0.4731] | 30 | 11 | +0.3834 | [-0.1246, +0.7330] | -0.0182 | [-0.5316, +0.3438] |
| de | 570 | 193 | +0.6375 | [+0.5858, +0.6869] | 23 | 11 | +0.7673 | [+0.4679, +0.9148] | +0.1298 | [-0.1698, +0.2849] |
| en | 570 | 190 | +0.8149 | [+0.7752, +0.8482] | 30 | 10 | +0.7062 | [+0.5146, +0.8914] | -0.1087 | [-0.3033, +0.0789] |
| es | 593 | 208 | +0.6621 | [+0.6176, +0.7028] | 30 | 10 | +0.6830 | [+0.4490, +0.8384] | +0.0210 | [-0.2166, +0.1808] |
| fil | 570 | 555 | +0.4148 | [+0.3444, +0.4819] | 30 | 30 | +0.5737 | [+0.3109, +0.8075] | +0.1589 | [-0.1054, +0.4040] |
| fr | 569 | 191 | +0.5528 | [+0.4847, +0.6143] | 30 | 11 | +0.3811 | [+0.0348, +0.6464] | -0.1717 | [-0.5291, +0.1059] |
| it | 570 | 192 | +0.6106 | [+0.5533, +0.6681] | 30 | 10 | +0.7074 | [+0.5123, +0.8438] | +0.0967 | [-0.1142, +0.2490] |
| ja | 570 | 190 | +0.5368 | [+0.4665, +0.5990] | 30 | 10 | +0.3492 | [+0.1090, +0.5570] | -0.1876 | [-0.4306, +0.0225] |
| pt | 567 | 562 | +0.7608 | [+0.7218, +0.7983] | 30 | 30 | +0.7649 | [+0.5845, +0.9001] | +0.0041 | [-0.1819, +0.1437] |
| si | 600 | 578 | +0.2178 | [+0.1551, +0.2794] | 30 | 30 | -0.1413 | [-0.5008, +0.3203] | -0.3590 | [-0.7272, +0.0963] |
| **medie** | | | **+0.5610** | | | | **+0.5175** | | **-0.0435** | |

**Δ split mediu -0.0435**, sd intre limbi 0.1629, interval -0.3590 pana la +0.1589. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3834 | +0.3018 | -0.0816 |
| de | +0.7673 | +0.7634 | -0.0039 |
| en | +0.7062 | +0.6831 | -0.0231 |
| es | +0.6830 | +0.6895 | +0.0065 |
| fil | +0.5737 | +0.6207 | +0.0470 |
| fr | +0.3811 | +0.3532 | -0.0279 |
| it | +0.7074 | +0.6947 | -0.0127 |
| ja | +0.3492 | +0.3120 | -0.0372 |
| pt | +0.7649 | +0.7630 | -0.0019 |
| si | -0.1413 | -0.0458 | +0.0955 |

**Diferenta medie -0.0039**, interval -0.0816 pana la +0.0955.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4145 | +0.3096 | -0.0129 | +0.0738 |
| de | +0.6471 | +0.8022 | -0.0096 | -0.0349 |
| en | +0.8092 | +0.7088 | +0.0057 | -0.0026 |
| es | +0.6656 | +0.7080 | -0.0035 | -0.0250 |
| fil | +0.4122 | +0.5548 | +0.0026 | +0.0189 |
| fr | +0.5352 | +0.3635 | +0.0176 | +0.0176 |
| it | +0.6100 | +0.7425 | +0.0006 | -0.0351 |
| ja | +0.6050 | +0.4745 | -0.0682 | -0.1253 |
| pt | +0.7695 | +0.7588 | -0.0087 | +0.0061 |
| si | +0.1704 | -0.0635 | +0.0474 | -0.0778 |
