# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:25:18 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4350 | [+0.3638, +0.5004] | 30 | 11 | +0.4321 | [+0.0036, +0.7569] | -0.0029 | [-0.4366, +0.3288] |
| de | 570 | 193 | +0.6093 | [+0.5564, +0.6615] | 23 | 11 | +0.7386 | [+0.4570, +0.8989] | +0.1293 | [-0.1596, +0.3030] |
| en | 570 | 190 | +0.8118 | [+0.7751, +0.8440] | 30 | 10 | +0.7517 | [+0.3907, +0.8781] | -0.0601 | [-0.4281, +0.0765] |
| es | 593 | 208 | +0.6754 | [+0.6312, +0.7155] | 30 | 10 | +0.7635 | [+0.5785, +0.8923] | +0.0881 | [-0.0968, +0.2248] |
| fil | 570 | 555 | +0.4043 | [+0.3367, +0.4688] | 30 | 30 | +0.5382 | [+0.2541, +0.7867] | +0.1339 | [-0.1660, +0.3913] |
| fr | 569 | 191 | +0.5367 | [+0.4706, +0.5972] | 30 | 11 | +0.3636 | [+0.0346, +0.6131] | -0.1731 | [-0.5052, +0.0861] |
| it | 570 | 192 | +0.6169 | [+0.5670, +0.6665] | 30 | 10 | +0.7545 | [+0.6137, +0.8538] | +0.1376 | [-0.0157, +0.2512] |
| ja | 570 | 190 | +0.4602 | [+0.3832, +0.5308] | 30 | 10 | +0.5592 | [+0.2586, +0.7681] | +0.0990 | [-0.2191, +0.3137] |
| pt | 567 | 562 | +0.7727 | [+0.7311, +0.8099] | 30 | 30 | +0.7706 | [+0.6011, +0.8975] | -0.0021 | [-0.1808, +0.1264] |
| si | 600 | 578 | +0.1850 | [+0.1093, +0.2534] | 30 | 30 | +0.1840 | [-0.2424, +0.5126] | -0.0010 | [-0.4328, +0.3261] |
| **medie** | | | **+0.5507** | | | | **+0.5856** | | **+0.0349** | |

**Δ split mediu +0.0349**, sd intre limbi 0.1014, interval -0.1731 pana la +0.1376. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4321 | +0.3462 | -0.0859 |
| de | +0.7386 | +0.7429 | +0.0043 |
| en | +0.7517 | +0.7609 | +0.0092 |
| es | +0.7635 | +0.7467 | -0.0168 |
| fil | +0.5382 | +0.5666 | +0.0284 |
| fr | +0.3636 | +0.2734 | -0.0902 |
| it | +0.7545 | +0.7345 | -0.0200 |
| ja | +0.5592 | +0.4221 | -0.1371 |
| pt | +0.7706 | +0.7783 | +0.0077 |
| si | +0.1840 | +0.2411 | +0.0571 |

**Diferenta medie -0.0243**, interval -0.1371 pana la +0.0571.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4376 | +0.3586 | -0.0026 | +0.0735 |
| de | +0.6450 | +0.8336 | -0.0357 | -0.0950 |
| en | +0.8020 | +0.6829 | +0.0098 | +0.0688 |
| es | +0.6862 | +0.7160 | -0.0108 | +0.0475 |
| fil | +0.4042 | +0.5494 | +0.0001 | -0.0112 |
| fr | +0.5280 | +0.2933 | +0.0087 | +0.0703 |
| it | +0.6260 | +0.7354 | -0.0091 | +0.0191 |
| ja | +0.5671 | +0.5365 | -0.1069 | +0.0227 |
| pt | +0.7758 | +0.7629 | -0.0031 | +0.0077 |
| si | +0.1182 | +0.1667 | +0.0668 | +0.0173 |
