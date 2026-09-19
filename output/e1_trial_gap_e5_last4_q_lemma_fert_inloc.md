# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:53:43 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4726 | [+0.3913, +0.5416] | 30 | 11 | +0.3910 | [-0.0283, +0.6960] | -0.0816 | [-0.5194, +0.2394] |
| de | 570 | 193 | +0.6295 | [+0.5759, +0.6815] | 23 | 11 | +0.8028 | [+0.5860, +0.9161] | +0.1733 | [-0.0448, +0.3057] |
| en | 570 | 190 | +0.8160 | [+0.7823, +0.8460] | 30 | 10 | +0.7236 | [+0.3601, +0.8796] | -0.0924 | [-0.4634, +0.0686] |
| es | 593 | 208 | +0.6936 | [+0.6514, +0.7297] | 30 | 10 | +0.7314 | [+0.4660, +0.8925] | +0.0378 | [-0.2202, +0.2051] |
| fil | 570 | 555 | +0.4091 | [+0.3372, +0.4756] | 30 | 30 | +0.5551 | [+0.2660, +0.7740] | +0.1460 | [-0.1563, +0.3770] |
| fr | 569 | 191 | +0.5496 | [+0.4874, +0.6089] | 30 | 11 | +0.3613 | [+0.0792, +0.5931] | -0.1883 | [-0.4766, +0.0580] |
| it | 570 | 192 | +0.6244 | [+0.5731, +0.6766] | 30 | 10 | +0.7079 | [+0.5293, +0.8345] | +0.0834 | [-0.1012, +0.2251] |
| ja | 570 | 190 | +0.5547 | [+0.4872, +0.6184] | 30 | 10 | +0.6824 | [+0.4241, +0.8561] | +0.1277 | [-0.1465, +0.3108] |
| pt | 567 | 562 | +0.7665 | [+0.7222, +0.8053] | 30 | 30 | +0.7380 | [+0.5383, +0.8816] | -0.0285 | [-0.2283, +0.1194] |
| si | 600 | 578 | +0.2313 | [+0.1649, +0.2960] | 30 | 30 | +0.2329 | [-0.0453, +0.5389] | +0.0016 | [-0.2794, +0.3200] |
| **medie** | | | **+0.5747** | | | | **+0.5926** | | **+0.0179** | |

**Δ split mediu +0.0179**, sd intre limbi 0.1175, interval -0.1883 pana la +0.1733. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3910 | +0.3885 | -0.0025 |
| de | +0.8028 | +0.8055 | +0.0027 |
| en | +0.7236 | +0.7245 | +0.0009 |
| es | +0.7314 | +0.7329 | +0.0015 |
| fil | +0.5551 | +0.5789 | +0.0238 |
| fr | +0.3613 | +0.3141 | -0.0472 |
| it | +0.7079 | +0.7041 | -0.0038 |
| ja | +0.6824 | +0.6564 | -0.0260 |
| pt | +0.7380 | +0.7367 | -0.0013 |
| si | +0.2329 | +0.2979 | +0.0650 |

**Diferenta medie +0.0013**, interval -0.0472 pana la +0.0650.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4531 | +0.4175 | +0.0195 | -0.0265 |
| de | +0.6606 | +0.8259 | -0.0311 | -0.0231 |
| en | +0.8083 | +0.6743 | +0.0077 | +0.0493 |
| es | +0.6924 | +0.7365 | +0.0012 | -0.0051 |
| fil | +0.4079 | +0.5700 | +0.0012 | -0.0149 |
| fr | +0.5466 | +0.3024 | +0.0030 | +0.0589 |
| it | +0.6375 | +0.7291 | -0.0131 | -0.0212 |
| ja | +0.5713 | +0.6015 | -0.0166 | +0.0809 |
| pt | +0.7736 | +0.7684 | -0.0071 | -0.0304 |
| si | +0.2106 | +0.3153 | +0.0207 | -0.0824 |
