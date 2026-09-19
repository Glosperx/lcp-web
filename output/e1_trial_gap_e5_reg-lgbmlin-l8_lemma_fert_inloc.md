# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:24:00 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4271 | [+0.3548, +0.4919] | 30 | 11 | +0.4322 | [+0.0051, +0.7501] | +0.0052 | [-0.4390, +0.3368] |
| de | 570 | 193 | +0.6123 | [+0.5581, +0.6645] | 23 | 11 | +0.7414 | [+0.4881, +0.8991] | +0.1290 | [-0.1405, +0.3031] |
| en | 570 | 190 | +0.8115 | [+0.7746, +0.8431] | 30 | 10 | +0.7369 | [+0.3616, +0.8762] | -0.0746 | [-0.4474, +0.0751] |
| es | 593 | 208 | +0.6826 | [+0.6398, +0.7216] | 30 | 10 | +0.7559 | [+0.5372, +0.8916] | +0.0733 | [-0.1382, +0.2170] |
| fil | 570 | 555 | +0.3963 | [+0.3259, +0.4657] | 30 | 30 | +0.5459 | [+0.2679, +0.7857] | +0.1497 | [-0.1415, +0.4057] |
| fr | 569 | 191 | +0.5342 | [+0.4678, +0.5950] | 30 | 11 | +0.3672 | [+0.0268, +0.6211] | -0.1670 | [-0.5071, +0.1003] |
| it | 570 | 192 | +0.6231 | [+0.5725, +0.6730] | 30 | 10 | +0.7516 | [+0.6002, +0.8569] | +0.1285 | [-0.0335, +0.2480] |
| ja | 570 | 190 | +0.5298 | [+0.4659, +0.5918] | 30 | 10 | +0.6200 | [+0.3157, +0.8215] | +0.0902 | [-0.2304, +0.3043] |
| pt | 567 | 562 | +0.7722 | [+0.7304, +0.8094] | 30 | 30 | +0.7862 | [+0.6090, +0.9236] | +0.0140 | [-0.1703, +0.1520] |
| si | 600 | 578 | +0.1819 | [+0.1278, +0.2324] | 30 | 30 | +0.0760 | [-0.2924, +0.3919] | -0.1058 | [-0.4677, +0.2138] |
| **medie** | | | **+0.5571** | | | | **+0.5813** | | **+0.0243** | |

**Δ split mediu +0.0243**, sd intre limbi 0.1096, interval -0.1670 pana la +0.1497. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4322 | +0.3332 | -0.0990 |
| de | +0.7414 | +0.7588 | +0.0174 |
| en | +0.7369 | +0.7247 | -0.0122 |
| es | +0.7559 | +0.7245 | -0.0314 |
| fil | +0.5459 | +0.5521 | +0.0062 |
| fr | +0.3672 | +0.2992 | -0.0680 |
| it | +0.7516 | +0.7393 | -0.0123 |
| ja | +0.6200 | +0.6168 | -0.0032 |
| pt | +0.7862 | +0.7786 | -0.0076 |
| si | +0.0760 | +0.1003 | +0.0243 |

**Diferenta medie -0.0186**, interval -0.0990 pana la +0.0243.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4311 | +0.3926 | -0.0040 | +0.0396 |
| de | +0.6642 | +0.8411 | -0.0519 | -0.0997 |
| en | +0.7992 | +0.6624 | +0.0123 | +0.0745 |
| es | +0.6892 | +0.7086 | -0.0066 | +0.0473 |
| fil | +0.3963 | +0.5386 | +0.0000 | +0.0073 |
| fr | +0.5157 | +0.2934 | +0.0185 | +0.0738 |
| it | +0.6439 | +0.7182 | -0.0208 | +0.0334 |
| ja | +0.5570 | +0.5490 | -0.0272 | +0.0710 |
| pt | +0.7789 | +0.7598 | -0.0067 | +0.0264 |
| si | +0.0844 | +0.2830 | +0.0975 | -0.2070 |
