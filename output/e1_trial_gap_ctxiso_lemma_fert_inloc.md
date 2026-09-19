# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:48:24 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4394 | [+0.3559, +0.5134] | 30 | 11 | +0.2925 | [-0.2598, +0.7005] | -0.1469 | [-0.6950, +0.2759] |
| de | 570 | 193 | +0.6264 | [+0.5720, +0.6767] | 23 | 11 | +0.7307 | [+0.4561, +0.8742] | +0.1043 | [-0.1881, +0.2596] |
| en | 570 | 190 | +0.8097 | [+0.7707, +0.8427] | 30 | 10 | +0.7008 | [+0.4408, +0.8440] | -0.1090 | [-0.3832, +0.0401] |
| es | 593 | 208 | +0.6673 | [+0.6206, +0.7086] | 30 | 10 | +0.6854 | [+0.4019, +0.8415] | +0.0181 | [-0.2577, +0.1797] |
| fil | 570 | 555 | +0.3995 | [+0.3280, +0.4676] | 30 | 30 | +0.6064 | [+0.3742, +0.7692] | +0.2069 | [-0.0340, +0.3867] |
| fr | 569 | 191 | +0.5320 | [+0.4627, +0.5953] | 30 | 11 | +0.3256 | [-0.0389, +0.6184] | -0.2064 | [-0.5922, +0.0968] |
| it | 570 | 192 | +0.6132 | [+0.5593, +0.6679] | 30 | 10 | +0.6597 | [+0.4285, +0.8238] | +0.0465 | [-0.1831, +0.2235] |
| ja | 570 | 190 | +0.5539 | [+0.4871, +0.6136] | 30 | 10 | +0.4379 | [+0.2797, +0.5533] | -0.1160 | [-0.2848, +0.0082] |
| pt | 567 | 562 | +0.7535 | [+0.7121, +0.7910] | 30 | 30 | +0.8010 | [+0.6479, +0.9102] | +0.0475 | [-0.1116, +0.1580] |
| si | 600 | 578 | +0.2146 | [+0.1523, +0.2793] | 30 | 30 | -0.0202 | [-0.4461, +0.4806] | -0.2349 | [-0.6678, +0.2748] |
| **medie** | | | **+0.5609** | | | | **+0.5220** | | **-0.0390** | |

**Δ split mediu -0.0390**, sd intre limbi 0.1445, interval -0.2349 pana la +0.2069. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2925 | +0.2501 | -0.0424 |
| de | +0.7307 | +0.7259 | -0.0048 |
| en | +0.7008 | +0.6949 | -0.0059 |
| es | +0.6854 | +0.6870 | +0.0016 |
| fil | +0.6064 | +0.6075 | +0.0011 |
| fr | +0.3256 | +0.2897 | -0.0359 |
| it | +0.6597 | +0.6568 | -0.0029 |
| ja | +0.4379 | +0.4047 | -0.0332 |
| pt | +0.8010 | +0.7958 | -0.0052 |
| si | -0.0202 | +0.0245 | +0.0447 |

**Diferenta medie -0.0083**, interval -0.0424 pana la +0.0447.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4045 | +0.2166 | +0.0349 | +0.0759 |
| de | +0.6540 | +0.7696 | -0.0276 | -0.0389 |
| en | +0.7930 | +0.7443 | +0.0167 | -0.0435 |
| es | +0.6456 | +0.6382 | +0.0217 | +0.0472 |
| fil | +0.4092 | +0.5591 | -0.0097 | +0.0473 |
| fr | +0.5297 | +0.3301 | +0.0023 | -0.0045 |
| it | +0.6079 | +0.6871 | +0.0053 | -0.0274 |
| ja | +0.5735 | +0.4390 | -0.0196 | -0.0011 |
| pt | +0.7600 | +0.7863 | -0.0065 | +0.0147 |
| si | +0.2117 | +0.0330 | +0.0029 | -0.0532 |
