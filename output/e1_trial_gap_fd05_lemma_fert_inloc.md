# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:51:13 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4072 | [+0.3216, +0.4885] | 30 | 11 | +0.3086 | [-0.0636, +0.6868] | -0.0986 | [-0.4839, +0.2855] |
| de | 570 | 193 | +0.6041 | [+0.5450, +0.6584] | 23 | 11 | +0.6630 | [+0.3946, +0.8100] | +0.0589 | [-0.2162, +0.2220] |
| en | 570 | 190 | +0.8020 | [+0.7609, +0.8374] | 30 | 10 | +0.6822 | [+0.4537, +0.8525] | -0.1198 | [-0.3517, +0.0569] |
| es | 593 | 208 | +0.6301 | [+0.5815, +0.6735] | 30 | 10 | +0.6571 | [+0.3398, +0.8298] | +0.0270 | [-0.2874, +0.2048] |
| fil | 570 | 555 | +0.4114 | [+0.3407, +0.4749] | 30 | 30 | +0.4502 | [+0.1766, +0.6791] | +0.0388 | [-0.2411, +0.2798] |
| fr | 569 | 191 | +0.5052 | [+0.4347, +0.5692] | 30 | 11 | +0.3124 | [-0.0496, +0.6042] | -0.1928 | [-0.5592, +0.1049] |
| it | 570 | 192 | +0.5763 | [+0.5160, +0.6383] | 30 | 10 | +0.6181 | [+0.3388, +0.8139] | +0.0418 | [-0.2449, +0.2480] |
| ja | 570 | 190 | +0.6059 | [+0.5442, +0.6627] | 30 | 10 | +0.5387 | [+0.3831, +0.6755] | -0.0673 | [-0.2366, +0.0839] |
| pt | 567 | 562 | +0.7195 | [+0.6748, +0.7596] | 30 | 30 | +0.7734 | [+0.6178, +0.8950] | +0.0538 | [-0.1076, +0.1851] |
| si | 600 | 578 | +0.2736 | [+0.2174, +0.3299] | 30 | 30 | +0.1006 | [-0.2462, +0.4516] | -0.1730 | [-0.5266, +0.1827] |
| **medie** | | | **+0.5535** | | | | **+0.5104** | | **-0.0431** | |

**Δ split mediu -0.0431**, sd intre limbi 0.0986, interval -0.1928 pana la +0.0589. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3086 | +0.3090 | +0.0004 |
| de | +0.6630 | +0.6638 | +0.0008 |
| en | +0.6822 | +0.6940 | +0.0118 |
| es | +0.6571 | +0.6616 | +0.0045 |
| fil | +0.4502 | +0.4696 | +0.0194 |
| fr | +0.3124 | +0.2668 | -0.0456 |
| it | +0.6181 | +0.6187 | +0.0006 |
| ja | +0.5387 | +0.4969 | -0.0418 |
| pt | +0.7734 | +0.7689 | -0.0045 |
| si | +0.1006 | +0.1139 | +0.0133 |

**Diferenta medie -0.0041**, interval -0.0456 pana la +0.0194.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3739 | +0.3046 | +0.0333 | +0.0040 |
| de | +0.5734 | +0.6263 | +0.0307 | +0.0367 |
| en | +0.7883 | +0.6232 | +0.0137 | +0.0590 |
| es | +0.6210 | +0.7121 | +0.0091 | -0.0550 |
| fil | +0.4388 | +0.4143 | -0.0274 | +0.0359 |
| fr | +0.4916 | +0.3586 | +0.0136 | -0.0462 |
| it | +0.5475 | +0.6275 | +0.0288 | -0.0094 |
| ja | +0.5681 | +0.4368 | +0.0378 | +0.1019 |
| pt | +0.7076 | +0.7012 | +0.0119 | +0.0722 |
| si | +0.3005 | +0.1906 | -0.0269 | -0.0900 |
