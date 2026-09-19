# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 11:57:37 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4437 | [+0.3524, +0.5245] | 30 | 11 | +0.5295 | [+0.2898, +0.7232] | +0.0859 | [-0.1813, +0.3042] |
| de | 570 | 193 | +0.5742 | [+0.5108, +0.6349] | 23 | 11 | +0.8140 | [+0.5797, +0.9338] | +0.2398 | [-0.0057, +0.3780] |
| en | 570 | 190 | +0.7913 | [+0.7526, +0.8274] | 30 | 10 | +0.6572 | [+0.3948, +0.8406] | -0.1341 | [-0.3985, +0.0522] |
| es | 593 | 208 | +0.6788 | [+0.6326, +0.7184] | 30 | 10 | +0.6952 | [+0.3956, +0.8828] | +0.0164 | [-0.2818, +0.2107] |
| fil | 570 | 555 | +0.3753 | [+0.3048, +0.4438] | 30 | 30 | +0.4847 | [+0.1748, +0.7214] | +0.1095 | [-0.2178, +0.3636] |
| fr | 569 | 191 | +0.5275 | [+0.4643, +0.5903] | 30 | 11 | +0.3339 | [+0.0965, +0.5535] | -0.1936 | [-0.4453, +0.0354] |
| it | 570 | 192 | +0.5742 | [+0.5195, +0.6297] | 30 | 10 | +0.6600 | [+0.4431, +0.8228] | +0.0859 | [-0.1312, +0.2649] |
| ja | 570 | 190 | +0.5498 | [+0.4880, +0.6083] | 30 | 10 | +0.6682 | [+0.4226, +0.8186] | +0.1184 | [-0.1302, +0.2820] |
| pt | 567 | 562 | +0.7285 | [+0.6814, +0.7706] | 30 | 30 | +0.6931 | [+0.4827, +0.8423] | -0.0354 | [-0.2517, +0.1234] |
| si | 600 | 578 | +0.2653 | [+0.2036, +0.3255] | 30 | 30 | +0.2318 | [-0.0959, +0.5307] | -0.0335 | [-0.3615, +0.2730] |
| **medie** | | | **+0.5509** | | | | **+0.5768** | | **+0.0259** | |

**Δ split mediu +0.0259**, sd intre limbi 0.1290, interval -0.1936 pana la +0.2398. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.5295 | +0.5140 | -0.0155 |
| de | +0.8140 | +0.8183 | +0.0043 |
| en | +0.6572 | +0.6759 | +0.0187 |
| es | +0.6952 | +0.6658 | -0.0294 |
| fil | +0.4847 | +0.5099 | +0.0252 |
| fr | +0.3339 | +0.3029 | -0.0310 |
| it | +0.6600 | +0.6571 | -0.0029 |
| ja | +0.6682 | +0.6575 | -0.0107 |
| pt | +0.6931 | +0.7009 | +0.0078 |
| si | +0.2318 | +0.2475 | +0.0157 |

**Diferenta medie -0.0018**, interval -0.0310 pana la +0.0252.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4183 | +0.5486 | +0.0254 | -0.0191 |
| de | +0.6182 | +0.8396 | -0.0440 | -0.0256 |
| en | +0.7762 | +0.6099 | +0.0151 | +0.0473 |
| es | +0.6541 | +0.6660 | +0.0247 | +0.0292 |
| fil | +0.3412 | +0.4338 | +0.0341 | +0.0509 |
| fr | +0.5243 | +0.1697 | +0.0032 | +0.1642 |
| it | +0.5554 | +0.6794 | +0.0188 | -0.0194 |
| ja | +0.4358 | +0.5798 | +0.1140 | +0.0884 |
| pt | +0.7386 | +0.7169 | -0.0101 | -0.0238 |
| si | +0.2451 | +0.1245 | +0.0202 | +0.1073 |
