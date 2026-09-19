# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:40:53 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3428 | [+0.2527, +0.4276] | 30 | 11 | -0.0689 | [-0.3056, +0.2214] | -0.4117 | [-0.6680, -0.1172] |
| de | 570 | 193 | +0.5039 | [+0.4397, +0.5626] | 23 | 11 | +0.5656 | [+0.2420, +0.7625] | +0.0618 | [-0.2611, +0.2641] |
| en | 570 | 190 | +0.6875 | [+0.6312, +0.7361] | 30 | 10 | +0.5772 | [+0.0474, +0.8031] | -0.1103 | [-0.6273, +0.1282] |
| es | 593 | 208 | +0.5397 | [+0.4792, +0.5972] | 30 | 10 | +0.4861 | [-0.0019, +0.8109] | -0.0536 | [-0.5516, +0.2779] |
| fil | 570 | 555 | +0.3690 | [+0.2939, +0.4378] | 30 | 30 | +0.4230 | [+0.1052, +0.6324] | +0.0540 | [-0.2719, +0.2763] |
| fr | 569 | 191 | +0.3911 | [+0.3067, +0.4670] | 30 | 11 | +0.1514 | [-0.2228, +0.5090] | -0.2397 | [-0.6243, +0.1250] |
| it | 570 | 192 | +0.4743 | [+0.4103, +0.5396] | 30 | 10 | +0.5870 | [+0.3371, +0.7866] | +0.1127 | [-0.1553, +0.3211] |
| ja | 570 | 190 | +0.5175 | [+0.4504, +0.5805] | 30 | 10 | +0.4823 | [+0.2730, +0.6071] | -0.0352 | [-0.2525, +0.1038] |
| pt | 567 | 562 | +0.6367 | [+0.5882, +0.6845] | 30 | 30 | +0.5413 | [+0.2568, +0.7662] | -0.0954 | [-0.3838, +0.1431] |
| si | 600 | 578 | +0.2311 | [+0.1679, +0.2955] | 30 | 30 | +0.1305 | [-0.1020, +0.4343] | -0.1006 | [-0.3393, +0.2105] |
| **medie** | | | **+0.4694** | | | | **+0.3875** | | **-0.0818** | |

**Δ split mediu -0.0818**, sd intre limbi 0.1546, interval -0.4117 pana la +0.1127. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | -0.0689 | +0.0168 | +0.0857 |
| de | +0.5656 | +0.5578 | -0.0078 |
| en | +0.5772 | +0.5663 | -0.0109 |
| es | +0.4861 | +0.5028 | +0.0167 |
| fil | +0.4230 | +0.3672 | -0.0558 |
| fr | +0.1514 | +0.0322 | -0.1192 |
| it | +0.5870 | +0.5894 | +0.0024 |
| ja | +0.4823 | +0.4984 | +0.0161 |
| pt | +0.5413 | +0.5258 | -0.0155 |
| si | +0.1305 | +0.1301 | -0.0004 |

**Diferenta medie -0.0089**, interval -0.1192 pana la +0.0857.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3137 | +0.1176 | +0.0291 | -0.1865 |
| de | +0.4918 | +0.6682 | +0.0121 | -0.1026 |
| en | +0.6863 | +0.5371 | +0.0012 | +0.0401 |
| es | +0.5350 | +0.4308 | +0.0047 | +0.0553 |
| fil | +0.3778 | +0.4051 | -0.0088 | +0.0179 |
| fr | +0.3885 | +0.1482 | +0.0026 | +0.0032 |
| it | +0.4486 | +0.5972 | +0.0257 | -0.0102 |
| ja | +0.4328 | +0.4385 | +0.0847 | +0.0438 |
| pt | +0.6496 | +0.5475 | -0.0129 | -0.0062 |
| si | +0.2042 | +0.2170 | +0.0269 | -0.0865 |
