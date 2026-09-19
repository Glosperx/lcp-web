# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:26:18 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4248 | [+0.3241, +0.5142] | 30 | 11 | +0.3484 | [-0.0023, +0.6107] | -0.0764 | [-0.4469, +0.2012] |
| de | 570 | 193 | +0.5666 | [+0.5037, +0.6250] | 23 | 11 | +0.8340 | [+0.5959, +0.9340] | +0.2673 | [+0.0141, +0.3891] |
| en | 570 | 190 | +0.7836 | [+0.7458, +0.8200] | 30 | 10 | +0.6511 | [+0.3492, +0.8594] | -0.1326 | [-0.4355, +0.0797] |
| es | 593 | 208 | +0.6995 | [+0.6537, +0.7396] | 30 | 10 | +0.6820 | [+0.3363, +0.8881] | -0.0175 | [-0.3492, +0.1988] |
| fil | 570 | 555 | +0.4136 | [+0.3432, +0.4816] | 30 | 30 | +0.5115 | [+0.2256, +0.7241] | +0.0978 | [-0.1859, +0.3252] |
| fr | 569 | 191 | +0.5186 | [+0.4539, +0.5841] | 30 | 11 | +0.3279 | [+0.1038, +0.5244] | -0.1907 | [-0.4307, +0.0156] |
| it | 570 | 192 | +0.6090 | [+0.5546, +0.6637] | 30 | 10 | +0.5626 | [+0.2898, +0.7829] | -0.0464 | [-0.3175, +0.1830] |
| ja | 570 | 190 | +0.5912 | [+0.5217, +0.6556] | 30 | 10 | +0.7546 | [+0.5824, +0.8779] | +0.1634 | [-0.0233, +0.3032] |
| pt | 567 | 562 | +0.7123 | [+0.6624, +0.7566] | 30 | 30 | +0.6696 | [+0.4349, +0.8413] | -0.0428 | [-0.2878, +0.1294] |
| si | 600 | 578 | +0.1953 | [+0.1320, +0.2627] | 30 | 30 | +0.4079 | [+0.2039, +0.6430] | +0.2125 | [+0.0023, +0.4604] |
| **medie** | | | **+0.5514** | | | | **+0.5750** | | **+0.0235** | |

**Δ split mediu +0.0235**, sd intre limbi 0.1533, interval -0.1907 pana la +0.2673. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3484 | +0.3487 | +0.0003 |
| de | +0.8340 | +0.8349 | +0.0009 |
| en | +0.6511 | +0.6520 | +0.0009 |
| es | +0.6820 | +0.6817 | -0.0003 |
| fil | +0.5115 | +0.5061 | -0.0054 |
| fr | +0.3279 | +0.3279 | +0.0000 |
| it | +0.5626 | +0.5625 | -0.0001 |
| ja | +0.7546 | +0.7539 | -0.0007 |
| pt | +0.6696 | +0.6700 | +0.0004 |
| si | +0.4079 | +0.4082 | +0.0003 |

**Diferenta medie -0.0004**, interval -0.0054 pana la +0.0009.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4127 | +0.4632 | +0.0121 | -0.1148 |
| de | +0.6297 | +0.8416 | -0.0631 | -0.0076 |
| en | +0.7683 | +0.5770 | +0.0153 | +0.0741 |
| es | +0.6684 | +0.6461 | +0.0311 | +0.0359 |
| fil | +0.4127 | +0.5347 | +0.0009 | -0.0232 |
| fr | +0.4977 | +0.1648 | +0.0209 | +0.1631 |
| it | +0.6010 | +0.6584 | +0.0080 | -0.0958 |
| ja | +0.4905 | +0.6163 | +0.1007 | +0.1383 |
| pt | +0.7346 | +0.7032 | -0.0223 | -0.0336 |
| si | +0.1990 | +0.2260 | -0.0037 | +0.1819 |
