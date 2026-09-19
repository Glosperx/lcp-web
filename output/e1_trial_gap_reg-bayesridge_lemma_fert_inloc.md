# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:27:20 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4175 | [+0.3291, +0.5004] | 30 | 11 | +0.1649 | [-0.2633, +0.5923] | -0.2526 | [-0.6906, +0.1874] |
| de | 570 | 193 | +0.6217 | [+0.5635, +0.6736] | 23 | 11 | +0.7146 | [+0.4877, +0.8384] | +0.0929 | [-0.1435, +0.2263] |
| en | 570 | 190 | +0.7775 | [+0.7346, +0.8134] | 30 | 10 | +0.6726 | [+0.4427, +0.8135] | -0.1049 | [-0.3369, +0.0457] |
| es | 593 | 208 | +0.6265 | [+0.5746, +0.6721] | 30 | 10 | +0.6322 | [+0.2933, +0.8105] | +0.0057 | [-0.3404, +0.1901] |
| fil | 570 | 555 | +0.4004 | [+0.3301, +0.4666] | 30 | 30 | +0.5688 | [+0.3163, +0.7378] | +0.1684 | [-0.0946, +0.3533] |
| fr | 569 | 191 | +0.4950 | [+0.4302, +0.5559] | 30 | 11 | +0.2344 | [-0.1506, +0.5889] | -0.2606 | [-0.6657, +0.0992] |
| it | 570 | 192 | +0.6073 | [+0.5523, +0.6618] | 30 | 10 | +0.5997 | [+0.3536, +0.7908] | -0.0076 | [-0.2596, +0.1918] |
| ja | 570 | 190 | +0.6139 | [+0.5534, +0.6693] | 30 | 10 | +0.5713 | [+0.4054, +0.6807] | -0.0426 | [-0.2229, +0.0798] |
| pt | 567 | 562 | +0.7232 | [+0.6754, +0.7641] | 30 | 30 | +0.7765 | [+0.6084, +0.9012] | +0.0532 | [-0.1222, +0.1823] |
| si | 600 | 578 | +0.2653 | [+0.2064, +0.3284] | 30 | 30 | +0.0551 | [-0.3202, +0.4664] | -0.2102 | [-0.5932, +0.2031] |
| **medie** | | | **+0.5548** | | | | **+0.4990** | | **-0.0558** | |

**Δ split mediu -0.0558**, sd intre limbi 0.1481, interval -0.2606 pana la +0.1684. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1649 | +0.1649 | +0.0000 |
| de | +0.7146 | +0.7146 | +0.0000 |
| en | +0.6726 | +0.6726 | +0.0000 |
| es | +0.6322 | +0.6322 | +0.0000 |
| fil | +0.5688 | +0.5688 | +0.0000 |
| fr | +0.2344 | +0.2344 | +0.0000 |
| it | +0.5997 | +0.5997 | +0.0000 |
| ja | +0.5713 | +0.5713 | +0.0000 |
| pt | +0.7765 | +0.7765 | +0.0000 |
| si | +0.0551 | +0.0551 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3878 | +0.1603 | +0.0297 | +0.0046 |
| de | +0.6361 | +0.7912 | -0.0144 | -0.0766 |
| en | +0.7790 | +0.6225 | -0.0015 | +0.0501 |
| es | +0.6170 | +0.6978 | +0.0095 | -0.0656 |
| fil | +0.4135 | +0.5060 | -0.0131 | +0.0628 |
| fr | +0.4944 | +0.2811 | +0.0006 | -0.0467 |
| it | +0.5997 | +0.6042 | +0.0076 | -0.0045 |
| ja | +0.5698 | +0.4433 | +0.0441 | +0.1280 |
| pt | +0.7346 | +0.7746 | -0.0114 | +0.0019 |
| si | +0.2799 | +0.1327 | -0.0146 | -0.0776 |
