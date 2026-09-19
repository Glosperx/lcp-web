# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:28:09 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3891 | [+0.3108, +0.4607] | 30 | 11 | +0.3586 | [-0.1121, +0.7177] | -0.0305 | [-0.5107, +0.3361] |
| de | 570 | 193 | +0.6080 | [+0.5589, +0.6553] | 23 | 11 | +0.7872 | [+0.5316, +0.9118] | +0.1792 | [-0.0761, +0.3207] |
| en | 570 | 190 | +0.7998 | [+0.7638, +0.8327] | 30 | 10 | +0.6807 | [+0.4784, +0.8269] | -0.1191 | [-0.3217, +0.0329] |
| es | 593 | 208 | +0.6496 | [+0.6048, +0.6904] | 30 | 10 | +0.6378 | [+0.4124, +0.8168] | -0.0119 | [-0.2449, +0.1680] |
| fil | 570 | 555 | +0.4063 | [+0.3364, +0.4709] | 30 | 30 | +0.5525 | [+0.2874, +0.7869] | +0.1462 | [-0.1267, +0.3877] |
| fr | 569 | 191 | +0.5522 | [+0.4869, +0.6122] | 30 | 11 | +0.4644 | [+0.1680, +0.6842] | -0.0877 | [-0.3930, +0.1426] |
| it | 570 | 192 | +0.5910 | [+0.5366, +0.6451] | 30 | 10 | +0.7045 | [+0.5491, +0.8212] | +0.1135 | [-0.0530, +0.2462] |
| ja | 570 | 190 | +0.5126 | [+0.4437, +0.5758] | 30 | 10 | +0.5234 | [+0.1674, +0.7533] | +0.0108 | [-0.3566, +0.2359] |
| pt | 567 | 562 | +0.7689 | [+0.7319, +0.8037] | 30 | 30 | +0.7709 | [+0.5866, +0.9103] | +0.0019 | [-0.1831, +0.1442] |
| si | 600 | 578 | +0.3112 | [+0.2398, +0.3777] | 30 | 30 | +0.4557 | [+0.0747, +0.6996] | +0.1445 | [-0.2404, +0.3937] |
| **medie** | | | **+0.5589** | | | | **+0.5936** | | **+0.0347** | |

**Δ split mediu +0.0347**, sd intre limbi 0.1045, interval -0.1191 pana la +0.1792. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3586 | +0.2990 | -0.0596 |
| de | +0.7872 | +0.7753 | -0.0119 |
| en | +0.6807 | +0.6885 | +0.0078 |
| es | +0.6378 | +0.6250 | -0.0128 |
| fil | +0.5525 | +0.5780 | +0.0255 |
| fr | +0.4644 | +0.4405 | -0.0239 |
| it | +0.7045 | +0.7126 | +0.0081 |
| ja | +0.5234 | +0.4621 | -0.0613 |
| pt | +0.7709 | +0.7795 | +0.0086 |
| si | +0.4557 | +0.5331 | +0.0774 |

**Diferenta medie -0.0042**, interval -0.0613 pana la +0.0774.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4080 | +0.3934 | -0.0189 | -0.0348 |
| de | +0.6335 | +0.8170 | -0.0255 | -0.0298 |
| en | +0.8075 | +0.6782 | -0.0077 | +0.0025 |
| es | +0.6700 | +0.6026 | -0.0204 | +0.0352 |
| fil | +0.4063 | +0.5817 | +0.0000 | -0.0292 |
| fr | +0.5195 | +0.3701 | +0.0327 | +0.0943 |
| it | +0.5995 | +0.7076 | -0.0085 | -0.0031 |
| ja | +0.5831 | +0.4932 | -0.0705 | +0.0302 |
| pt | +0.7653 | +0.7522 | +0.0036 | +0.0187 |
| si | +0.2121 | +0.2504 | +0.0991 | +0.2053 |
