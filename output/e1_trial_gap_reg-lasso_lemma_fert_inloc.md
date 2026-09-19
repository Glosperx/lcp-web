# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:20:27 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3717 | [+0.2786, +0.4548] | 30 | 11 | +0.4239 | [+0.0547, +0.6848] | +0.0522 | [-0.3273, +0.3320] |
| de | 570 | 193 | +0.6490 | [+0.6017, +0.6951] | 23 | 11 | +0.7921 | [+0.5305, +0.9183] | +0.1431 | [-0.1270, +0.2788] |
| en | 570 | 190 | +0.7698 | [+0.7288, +0.8055] | 30 | 10 | +0.6521 | [+0.5655, +0.7848] | -0.1177 | [-0.2095, +0.0229] |
| es | 593 | 208 | +0.6315 | [+0.5830, +0.6756] | 30 | 10 | +0.6715 | [+0.4233, +0.8389] | +0.0399 | [-0.2147, +0.2094] |
| fil | 570 | 555 | +0.3901 | [+0.3182, +0.4595] | 30 | 30 | +0.5713 | [+0.3679, +0.7453] | +0.1812 | [-0.0377, +0.3712] |
| fr | 569 | 191 | +0.5685 | [+0.5096, +0.6249] | 30 | 11 | +0.3728 | [-0.0033, +0.6538] | -0.1957 | [-0.5833, +0.0899] |
| it | 570 | 192 | +0.6226 | [+0.5661, +0.6730] | 30 | 10 | +0.6254 | [+0.4208, +0.7914] | +0.0027 | [-0.2137, +0.1821] |
| ja | 570 | 190 | +0.5866 | [+0.5199, +0.6494] | 30 | 10 | +0.5769 | [+0.3173, +0.7799] | -0.0097 | [-0.2828, +0.2083] |
| pt | 567 | 562 | +0.7297 | [+0.6895, +0.7662] | 30 | 30 | +0.7222 | [+0.5169, +0.8781] | -0.0075 | [-0.2137, +0.1522] |
| si | 600 | 578 | +0.2215 | [+0.1611, +0.2809] | 30 | 30 | -0.0564 | [-0.3636, +0.2871] | -0.2779 | [-0.5961, +0.0628] |
| **medie** | | | **+0.5541** | | | | **+0.5352** | | **-0.0189** | |

**Δ split mediu -0.0189**, sd intre limbi 0.1428, interval -0.2779 pana la +0.1812. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4239 | +0.4239 | +0.0000 |
| de | +0.7921 | +0.7921 | +0.0000 |
| en | +0.6521 | +0.6521 | +0.0000 |
| es | +0.6715 | +0.6715 | +0.0000 |
| fil | +0.5713 | +0.5713 | +0.0000 |
| fr | +0.3728 | +0.3728 | +0.0000 |
| it | +0.6254 | +0.6254 | +0.0000 |
| ja | +0.5769 | +0.5769 | +0.0000 |
| pt | +0.7222 | +0.7222 | +0.0000 |
| si | -0.0564 | -0.0564 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3389 | +0.3159 | +0.0328 | +0.1080 |
| de | +0.6669 | +0.8375 | -0.0179 | -0.0454 |
| en | +0.7588 | +0.6545 | +0.0110 | -0.0024 |
| es | +0.5950 | +0.6209 | +0.0365 | +0.0506 |
| fil | +0.3858 | +0.5842 | +0.0043 | -0.0129 |
| fr | +0.5650 | +0.3596 | +0.0035 | +0.0132 |
| it | +0.6206 | +0.6397 | +0.0020 | -0.0143 |
| ja | +0.5681 | +0.5065 | +0.0185 | +0.0704 |
| pt | +0.7470 | +0.7482 | -0.0173 | -0.0260 |
| si | +0.1423 | -0.0642 | +0.0792 | +0.0078 |
