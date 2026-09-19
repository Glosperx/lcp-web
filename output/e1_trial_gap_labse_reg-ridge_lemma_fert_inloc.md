# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:12:50 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4577 | [+0.3687, +0.5370] | 30 | 11 | +0.3832 | [+0.0557, +0.6232] | -0.0745 | [-0.4033, +0.1838] |
| de | 570 | 193 | +0.5698 | [+0.5099, +0.6266] | 23 | 11 | +0.7923 | [+0.4707, +0.9202] | +0.2224 | [-0.0996, +0.3645] |
| en | 570 | 190 | +0.7776 | [+0.7393, +0.8117] | 30 | 10 | +0.6586 | [+0.5282, +0.7959] | -0.1189 | [-0.2538, +0.0282] |
| es | 593 | 208 | +0.6387 | [+0.5874, +0.6852] | 30 | 10 | +0.6737 | [+0.4346, +0.8318] | +0.0349 | [-0.1993, +0.1996] |
| fil | 570 | 555 | +0.3916 | [+0.3204, +0.4620] | 30 | 30 | +0.4846 | [+0.2126, +0.6930] | +0.0930 | [-0.1788, +0.3161] |
| fr | 569 | 191 | +0.5224 | [+0.4613, +0.5786] | 30 | 11 | +0.4992 | [+0.2870, +0.6840] | -0.0233 | [-0.2398, +0.1703] |
| it | 570 | 192 | +0.5953 | [+0.5392, +0.6502] | 30 | 10 | +0.6788 | [+0.4720, +0.8208] | +0.0835 | [-0.1277, +0.2435] |
| ja | 570 | 190 | +0.5612 | [+0.4869, +0.6282] | 30 | 10 | +0.6657 | [+0.3832, +0.8236] | +0.1045 | [-0.1907, +0.2798] |
| pt | 567 | 562 | +0.7221 | [+0.6805, +0.7599] | 30 | 30 | +0.7009 | [+0.4723, +0.8815] | -0.0211 | [-0.2461, +0.1627] |
| si | 600 | 578 | +0.3490 | [+0.2732, +0.4202] | 30 | 30 | +0.2812 | [-0.2185, +0.5807] | -0.0678 | [-0.5668, +0.2399] |
| **medie** | | | **+0.5585** | | | | **+0.5818** | | **+0.0233** | |

**Δ split mediu +0.0233**, sd intre limbi 0.1039, interval -0.1189 pana la +0.2224. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3832 | +0.3832 | +0.0000 |
| de | +0.7923 | +0.7923 | +0.0000 |
| en | +0.6586 | +0.6586 | +0.0000 |
| es | +0.6737 | +0.6737 | +0.0000 |
| fil | +0.4846 | +0.4846 | +0.0000 |
| fr | +0.4992 | +0.4992 | +0.0000 |
| it | +0.6788 | +0.6788 | +0.0000 |
| ja | +0.6657 | +0.6657 | +0.0000 |
| pt | +0.7009 | +0.7009 | +0.0000 |
| si | +0.2812 | +0.2812 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4181 | +0.4161 | +0.0396 | -0.0329 |
| de | +0.6266 | +0.8518 | -0.0568 | -0.0595 |
| en | +0.7732 | +0.6731 | +0.0044 | -0.0145 |
| es | +0.6583 | +0.5870 | -0.0196 | +0.0867 |
| fil | +0.4062 | +0.5025 | -0.0146 | -0.0179 |
| fr | +0.4686 | +0.3188 | +0.0538 | +0.1804 |
| it | +0.6010 | +0.6774 | -0.0057 | +0.0014 |
| ja | +0.5333 | +0.5362 | +0.0279 | +0.1295 |
| pt | +0.7300 | +0.7491 | -0.0079 | -0.0482 |
| si | +0.2936 | +0.2997 | +0.0554 | -0.0185 |
