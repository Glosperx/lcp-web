# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:12:10 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4004 | [+0.3068, +0.4803] | 30 | 11 | +0.3882 | [+0.0409, +0.6515] | -0.0122 | [-0.3624, +0.2669] |
| de | 570 | 193 | +0.5703 | [+0.5102, +0.6267] | 23 | 11 | +0.8380 | [+0.6580, +0.9306] | +0.2677 | [+0.0759, +0.3769] |
| en | 570 | 190 | +0.7800 | [+0.7370, +0.8189] | 30 | 10 | +0.5976 | [+0.2407, +0.8388] | -0.1823 | [-0.5503, +0.0639] |
| es | 593 | 208 | +0.6913 | [+0.6472, +0.7308] | 30 | 10 | +0.7154 | [+0.4292, +0.8817] | +0.0241 | [-0.2668, +0.1977] |
| fil | 570 | 555 | +0.4073 | [+0.3364, +0.4716] | 30 | 30 | +0.5073 | [+0.1755, +0.7675] | +0.1000 | [-0.2344, +0.3572] |
| fr | 569 | 191 | +0.5272 | [+0.4593, +0.5908] | 30 | 11 | +0.3349 | [+0.1083, +0.5424] | -0.1923 | [-0.4329, +0.0235] |
| it | 570 | 192 | +0.6010 | [+0.5423, +0.6593] | 30 | 10 | +0.5650 | [+0.2877, +0.7927] | -0.0361 | [-0.3175, +0.2003] |
| ja | 570 | 190 | +0.5447 | [+0.4707, +0.6115] | 30 | 10 | +0.5832 | [+0.4105, +0.7657] | +0.0384 | [-0.1484, +0.2366] |
| pt | 567 | 562 | +0.7306 | [+0.6861, +0.7718] | 30 | 30 | +0.6939 | [+0.4711, +0.8560] | -0.0367 | [-0.2640, +0.1332] |
| si | 600 | 578 | +0.1990 | [+0.1464, +0.2497] | 30 | 30 | +0.2470 | [-0.1642, +0.5456] | +0.0480 | [-0.3743, +0.3634] |
| **medie** | | | **+0.5452** | | | | **+0.5471** | | **+0.0019** | |

**Δ split mediu +0.0019**, sd intre limbi 0.1329, interval -0.1923 pana la +0.2677. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3882 | +0.3914 | +0.0032 |
| de | +0.8380 | +0.8382 | +0.0002 |
| en | +0.5976 | +0.5970 | -0.0006 |
| es | +0.7154 | +0.7132 | -0.0022 |
| fil | +0.5073 | +0.4918 | -0.0155 |
| fr | +0.3349 | +0.3371 | +0.0022 |
| it | +0.5650 | +0.5621 | -0.0029 |
| ja | +0.5832 | +0.5782 | -0.0050 |
| pt | +0.6939 | +0.6933 | -0.0006 |
| si | +0.2470 | +0.2291 | -0.0179 |

**Diferenta medie -0.0039**, interval -0.0179 pana la +0.0032.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3976 | +0.3752 | +0.0028 | +0.0130 |
| de | +0.6026 | +0.8348 | -0.0323 | +0.0032 |
| en | +0.7673 | +0.5937 | +0.0127 | +0.0039 |
| es | +0.6584 | +0.5736 | +0.0329 | +0.1418 |
| fil | +0.4196 | +0.4802 | -0.0123 | +0.0271 |
| fr | +0.5105 | +0.1698 | +0.0167 | +0.1651 |
| it | +0.5856 | +0.6479 | +0.0154 | -0.0829 |
| ja | +0.4793 | +0.4684 | +0.0654 | +0.1148 |
| pt | +0.7384 | +0.7126 | -0.0078 | -0.0187 |
| si | +0.2371 | +0.1014 | -0.0381 | +0.1456 |
