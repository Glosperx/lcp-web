# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:22:49 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4554 | [+0.3676, +0.5336] | 30 | 11 | +0.3674 | [+0.0271, +0.6049] | -0.0881 | [-0.4286, +0.1669] |
| de | 570 | 193 | +0.5759 | [+0.5154, +0.6326] | 23 | 11 | +0.7946 | [+0.4851, +0.9233] | +0.2187 | [-0.0989, +0.3616] |
| en | 570 | 190 | +0.7767 | [+0.7378, +0.8113] | 30 | 10 | +0.6528 | [+0.5206, +0.7874] | -0.1238 | [-0.2619, +0.0208] |
| es | 593 | 208 | +0.6453 | [+0.5943, +0.6910] | 30 | 10 | +0.6681 | [+0.4081, +0.8415] | +0.0228 | [-0.2381, +0.2011] |
| fil | 570 | 555 | +0.3871 | [+0.3159, +0.4577] | 30 | 30 | +0.4838 | [+0.2103, +0.6914] | +0.0967 | [-0.1793, +0.3180] |
| fr | 569 | 191 | +0.5268 | [+0.4662, +0.5817] | 30 | 11 | +0.4848 | [+0.2675, +0.6739] | -0.0421 | [-0.2631, +0.1511] |
| it | 570 | 192 | +0.6020 | [+0.5473, +0.6556] | 30 | 10 | +0.6734 | [+0.4641, +0.8220] | +0.0714 | [-0.1405, +0.2341] |
| ja | 570 | 190 | +0.5670 | [+0.4938, +0.6337] | 30 | 10 | +0.6689 | [+0.3907, +0.8262] | +0.1020 | [-0.1860, +0.2770] |
| pt | 567 | 562 | +0.7273 | [+0.6851, +0.7651] | 30 | 30 | +0.7057 | [+0.4776, +0.8857] | -0.0217 | [-0.2465, +0.1578] |
| si | 600 | 578 | +0.3449 | [+0.2698, +0.4153] | 30 | 30 | +0.2900 | [-0.1816, +0.5799] | -0.0549 | [-0.5281, +0.2409] |
| **medie** | | | **+0.5608** | | | | **+0.5790** | | **+0.0181** | |

**Δ split mediu +0.0181**, sd intre limbi 0.1045, interval -0.1238 pana la +0.2187. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3674 | +0.3674 | +0.0000 |
| de | +0.7946 | +0.7946 | +0.0000 |
| en | +0.6528 | +0.6528 | +0.0000 |
| es | +0.6681 | +0.6681 | +0.0000 |
| fil | +0.4838 | +0.4838 | +0.0000 |
| fr | +0.4848 | +0.4848 | +0.0000 |
| it | +0.6734 | +0.6734 | +0.0000 |
| ja | +0.6689 | +0.6689 | +0.0000 |
| pt | +0.7057 | +0.7057 | +0.0000 |
| si | +0.2900 | +0.2900 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4114 | +0.3766 | +0.0440 | -0.0092 |
| de | +0.6295 | +0.8473 | -0.0536 | -0.0527 |
| en | +0.7670 | +0.6617 | +0.0097 | -0.0089 |
| es | +0.6523 | +0.5644 | -0.0070 | +0.1037 |
| fil | +0.3982 | +0.4974 | -0.0111 | -0.0136 |
| fr | +0.4648 | +0.2698 | +0.0620 | +0.2150 |
| it | +0.6063 | +0.6778 | -0.0043 | -0.0044 |
| ja | +0.5255 | +0.5322 | +0.0415 | +0.1367 |
| pt | +0.7317 | +0.7490 | -0.0044 | -0.0433 |
| si | +0.2739 | +0.3078 | +0.0710 | -0.0178 |
