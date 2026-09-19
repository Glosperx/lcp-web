# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 11:58:31 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4474 | [+0.3664, +0.5233] | 30 | 11 | +0.3141 | [-0.1982, +0.6855] | -0.1333 | [-0.6482, +0.2533] |
| de | 570 | 193 | +0.6536 | [+0.6001, +0.7030] | 23 | 11 | +0.8033 | [+0.5446, +0.9128] | +0.1498 | [-0.1227, +0.2761] |
| en | 570 | 190 | +0.8164 | [+0.7787, +0.8479] | 30 | 10 | +0.7044 | [+0.4734, +0.8498] | -0.1121 | [-0.3470, +0.0406] |
| es | 593 | 208 | +0.6640 | [+0.6185, +0.7062] | 30 | 10 | +0.6981 | [+0.4087, +0.8559] | +0.0341 | [-0.2463, +0.1980] |
| fil | 570 | 555 | +0.4079 | [+0.3363, +0.4752] | 30 | 30 | +0.6096 | [+0.3799, +0.7830] | +0.2017 | [-0.0409, +0.3870] |
| fr | 569 | 191 | +0.5340 | [+0.4665, +0.5940] | 30 | 11 | +0.3373 | [-0.0531, +0.6449] | -0.1968 | [-0.5942, +0.1234] |
| it | 570 | 192 | +0.6316 | [+0.5769, +0.6855] | 30 | 10 | +0.6509 | [+0.4225, +0.8127] | +0.0193 | [-0.2122, +0.1961] |
| ja | 570 | 190 | +0.6022 | [+0.5385, +0.6576] | 30 | 10 | +0.5012 | [+0.2981, +0.6281] | -0.1011 | [-0.3110, +0.0395] |
| pt | 567 | 562 | +0.7620 | [+0.7219, +0.7989] | 30 | 30 | +0.7971 | [+0.6468, +0.9090] | +0.0350 | [-0.1224, +0.1503] |
| si | 600 | 578 | +0.2727 | [+0.2100, +0.3404] | 30 | 30 | -0.0445 | [-0.4648, +0.4466] | -0.3172 | [-0.7374, +0.1727] |
| **medie** | | | **+0.5792** | | | | **+0.5372** | | **-0.0421** | |

**Δ split mediu -0.0421**, sd intre limbi 0.1592, interval -0.3172 pana la +0.2017. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3141 | +0.2808 | -0.0333 |
| de | +0.8033 | +0.7914 | -0.0119 |
| en | +0.7044 | +0.6868 | -0.0176 |
| es | +0.6981 | +0.6962 | -0.0019 |
| fil | +0.6096 | +0.6165 | +0.0069 |
| fr | +0.3373 | +0.2852 | -0.0521 |
| it | +0.6509 | +0.6483 | -0.0026 |
| ja | +0.5012 | +0.4775 | -0.0237 |
| pt | +0.7971 | +0.7961 | -0.0010 |
| si | -0.0445 | +0.0181 | +0.0626 |

**Diferenta medie -0.0075**, interval -0.0521 pana la +0.0626.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4178 | +0.2556 | +0.0296 | +0.0585 |
| de | +0.6579 | +0.8171 | -0.0043 | -0.0138 |
| en | +0.8071 | +0.6765 | +0.0093 | +0.0279 |
| es | +0.6486 | +0.6802 | +0.0154 | +0.0179 |
| fil | +0.4121 | +0.5397 | -0.0042 | +0.0699 |
| fr | +0.5319 | +0.3383 | +0.0021 | -0.0010 |
| it | +0.6198 | +0.6749 | +0.0118 | -0.0240 |
| ja | +0.6340 | +0.5884 | -0.0318 | -0.0872 |
| pt | +0.7642 | +0.7809 | -0.0022 | +0.0162 |
| si | +0.2982 | +0.0298 | -0.0255 | -0.0743 |
