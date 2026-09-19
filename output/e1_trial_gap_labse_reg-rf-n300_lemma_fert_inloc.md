# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:38:46 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3858 | [+0.3111, +0.4581] | 30 | 11 | +0.3883 | [-0.0711, +0.7287] | +0.0024 | [-0.4691, +0.3533] |
| de | 570 | 193 | +0.5764 | [+0.5245, +0.6262] | 23 | 11 | +0.7316 | [+0.3750, +0.9132] | +0.1552 | [-0.2091, +0.3485] |
| en | 570 | 190 | +0.7885 | [+0.7504, +0.8235] | 30 | 10 | +0.6706 | [+0.4786, +0.8184] | -0.1179 | [-0.3099, +0.0366] |
| es | 593 | 208 | +0.6321 | [+0.5859, +0.6738] | 30 | 10 | +0.6355 | [+0.3921, +0.8109] | +0.0033 | [-0.2444, +0.1845] |
| fil | 570 | 555 | +0.4122 | [+0.3432, +0.4781] | 30 | 30 | +0.5666 | [+0.3175, +0.7934] | +0.1543 | [-0.1067, +0.3897] |
| fr | 569 | 191 | +0.5393 | [+0.4755, +0.5992] | 30 | 11 | +0.4148 | [+0.0924, +0.6498] | -0.1244 | [-0.4549, +0.1169] |
| it | 570 | 192 | +0.5928 | [+0.5385, +0.6481] | 30 | 10 | +0.7087 | [+0.5658, +0.8148] | +0.1159 | [-0.0340, +0.2413] |
| ja | 570 | 190 | +0.5898 | [+0.5286, +0.6491] | 30 | 10 | +0.6469 | [+0.2908, +0.8653] | +0.0571 | [-0.2949, +0.2861] |
| pt | 567 | 562 | +0.7544 | [+0.7166, +0.7912] | 30 | 30 | +0.7529 | [+0.5649, +0.8952] | -0.0015 | [-0.1902, +0.1410] |
| si | 600 | 578 | +0.2225 | [+0.1245, +0.3131] | 30 | 30 | +0.3160 | [-0.1970, +0.6403] | +0.0935 | [-0.4171, +0.4311] |
| **medie** | | | **+0.5494** | | | | **+0.5832** | | **+0.0338** | |

**Δ split mediu +0.0338**, sd intre limbi 0.1007, interval -0.1244 pana la +0.1552. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3883 | +0.3118 | -0.0765 |
| de | +0.7316 | +0.7227 | -0.0089 |
| en | +0.6706 | +0.6888 | +0.0182 |
| es | +0.6355 | +0.6467 | +0.0112 |
| fil | +0.5666 | +0.6050 | +0.0384 |
| fr | +0.4148 | +0.4207 | +0.0059 |
| it | +0.7087 | +0.6988 | -0.0099 |
| ja | +0.6469 | +0.6311 | -0.0158 |
| pt | +0.7529 | +0.7498 | -0.0031 |
| si | +0.3160 | +0.3116 | -0.0044 |

**Diferenta medie -0.0045**, interval -0.0765 pana la +0.0384.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3814 | +0.4306 | +0.0044 | -0.0423 |
| de | +0.6103 | +0.8072 | -0.0339 | -0.0756 |
| en | +0.7923 | +0.7129 | -0.0038 | -0.0423 |
| es | +0.6569 | +0.5991 | -0.0248 | +0.0364 |
| fil | +0.4089 | +0.5822 | +0.0033 | -0.0156 |
| fr | +0.5133 | +0.3765 | +0.0260 | +0.0383 |
| it | +0.5928 | +0.7168 | +0.0000 | -0.0081 |
| ja | +0.5707 | +0.5162 | +0.0191 | +0.1307 |
| pt | +0.7497 | +0.7483 | +0.0047 | +0.0046 |
| si | +0.2227 | +0.2441 | -0.0002 | +0.0719 |
