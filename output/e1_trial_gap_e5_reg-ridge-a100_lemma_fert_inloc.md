# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:37:47 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4339 | [+0.3350, +0.5196] | 30 | 11 | +0.3585 | [+0.0037, +0.6270] | -0.0754 | [-0.4478, +0.2056] |
| de | 570 | 193 | +0.5844 | [+0.5235, +0.6400] | 23 | 11 | +0.8256 | [+0.5997, +0.9285] | +0.2411 | [+0.0087, +0.3622] |
| en | 570 | 190 | +0.7794 | [+0.7404, +0.8143] | 30 | 10 | +0.6520 | [+0.3857, +0.8429] | -0.1275 | [-0.3963, +0.0650] |
| es | 593 | 208 | +0.6873 | [+0.6432, +0.7260] | 30 | 10 | +0.6515 | [+0.2811, +0.8847] | -0.0359 | [-0.3973, +0.2045] |
| fil | 570 | 555 | +0.4032 | [+0.3308, +0.4711] | 30 | 30 | +0.5392 | [+0.2719, +0.7381] | +0.1360 | [-0.1349, +0.3474] |
| fr | 569 | 191 | +0.5312 | [+0.4687, +0.5926] | 30 | 11 | +0.3156 | [+0.0878, +0.5255] | -0.2156 | [-0.4504, +0.0103] |
| it | 570 | 192 | +0.6113 | [+0.5590, +0.6642] | 30 | 10 | +0.5996 | [+0.3406, +0.7949] | -0.0117 | [-0.2774, +0.1957] |
| ja | 570 | 190 | +0.5932 | [+0.5267, +0.6548] | 30 | 10 | +0.7397 | [+0.5673, +0.8560] | +0.1465 | [-0.0383, +0.2849] |
| pt | 567 | 562 | +0.7166 | [+0.6649, +0.7604] | 30 | 30 | +0.6769 | [+0.4608, +0.8334] | -0.0397 | [-0.2642, +0.1202] |
| si | 600 | 578 | +0.1883 | [+0.1200, +0.2594] | 30 | 30 | +0.3766 | [+0.1797, +0.6127] | +0.1883 | [-0.0203, +0.4409] |
| **medie** | | | **+0.5529** | | | | **+0.5735** | | **+0.0206** | |

**Δ split mediu +0.0206**, sd intre limbi 0.1493, interval -0.2156 pana la +0.2411. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3585 | +0.3585 | +0.0000 |
| de | +0.8256 | +0.8256 | +0.0000 |
| en | +0.6520 | +0.6520 | +0.0000 |
| es | +0.6515 | +0.6515 | +0.0000 |
| fil | +0.5392 | +0.5392 | +0.0000 |
| fr | +0.3156 | +0.3156 | +0.0000 |
| it | +0.5996 | +0.5996 | +0.0000 |
| ja | +0.7397 | +0.7397 | +0.0000 |
| pt | +0.6769 | +0.6769 | +0.0000 |
| si | +0.3766 | +0.3766 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4188 | +0.4124 | +0.0151 | -0.0539 |
| de | +0.6343 | +0.8417 | -0.0499 | -0.0161 |
| en | +0.7610 | +0.5713 | +0.0184 | +0.0807 |
| es | +0.6494 | +0.6207 | +0.0379 | +0.0308 |
| fil | +0.4006 | +0.5270 | +0.0026 | +0.0122 |
| fr | +0.5176 | +0.1928 | +0.0136 | +0.1228 |
| it | +0.5929 | +0.6506 | +0.0184 | -0.0510 |
| ja | +0.4947 | +0.6391 | +0.0985 | +0.1006 |
| pt | +0.7338 | +0.7152 | -0.0172 | -0.0383 |
| si | +0.1833 | +0.2548 | +0.0050 | +0.1218 |
