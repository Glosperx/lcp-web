# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:22:59 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4094 | [+0.3175, +0.4915] | 30 | 11 | +0.1863 | [-0.2699, +0.5761] | -0.2231 | [-0.6834, +0.1773] |
| de | 570 | 193 | +0.6283 | [+0.5727, +0.6804] | 23 | 11 | +0.7906 | [+0.5591, +0.9046] | +0.1623 | [-0.0805, +0.2880] |
| en | 570 | 190 | +0.7944 | [+0.7533, +0.8281] | 30 | 10 | +0.6739 | [+0.4224, +0.8241] | -0.1205 | [-0.3758, +0.0339] |
| es | 593 | 208 | +0.6648 | [+0.6173, +0.7070] | 30 | 10 | +0.6560 | [+0.3192, +0.8426] | -0.0088 | [-0.3321, +0.1836] |
| fil | 570 | 555 | +0.3955 | [+0.3236, +0.4641] | 30 | 30 | +0.6016 | [+0.3926, +0.7593] | +0.2061 | [-0.0077, +0.3854] |
| fr | 569 | 191 | +0.5353 | [+0.4714, +0.5932] | 30 | 11 | +0.3587 | [-0.0112, +0.6595] | -0.1767 | [-0.5514, +0.1260] |
| it | 570 | 192 | +0.6259 | [+0.5724, +0.6781] | 30 | 10 | +0.6072 | [+0.3561, +0.8002] | -0.0187 | [-0.2757, +0.1876] |
| ja | 570 | 190 | +0.6165 | [+0.5535, +0.6751] | 30 | 10 | +0.5757 | [+0.3844, +0.7180] | -0.0408 | [-0.2368, +0.1187] |
| pt | 567 | 562 | +0.7481 | [+0.7043, +0.7855] | 30 | 30 | +0.8088 | [+0.6586, +0.9179] | +0.0607 | [-0.0970, +0.1754] |
| si | 600 | 578 | +0.2704 | [+0.2086, +0.3361] | 30 | 30 | -0.0087 | [-0.4175, +0.4584] | -0.2792 | [-0.6925, +0.1842] |
| **medie** | | | **+0.5689** | | | | **+0.5250** | | **-0.0439** | |

**Δ split mediu -0.0439**, sd intre limbi 0.1594, interval -0.2792 pana la +0.2061. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1863 | +0.1863 | +0.0000 |
| de | +0.7906 | +0.7906 | +0.0000 |
| en | +0.6739 | +0.6739 | +0.0000 |
| es | +0.6560 | +0.6560 | +0.0000 |
| fil | +0.6016 | +0.6016 | +0.0000 |
| fr | +0.3587 | +0.3587 | +0.0000 |
| it | +0.6072 | +0.6072 | +0.0000 |
| ja | +0.5757 | +0.5757 | +0.0000 |
| pt | +0.8088 | +0.8088 | +0.0000 |
| si | -0.0087 | -0.0087 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3676 | +0.1007 | +0.0418 | +0.0856 |
| de | +0.6641 | +0.8072 | -0.0358 | -0.0166 |
| en | +0.7743 | +0.6403 | +0.0201 | +0.0336 |
| es | +0.6209 | +0.6437 | +0.0439 | +0.0123 |
| fil | +0.3915 | +0.5476 | +0.0040 | +0.0540 |
| fr | +0.5486 | +0.3712 | -0.0133 | -0.0125 |
| it | +0.6117 | +0.6224 | +0.0142 | -0.0152 |
| ja | +0.5528 | +0.5128 | +0.0637 | +0.0629 |
| pt | +0.7591 | +0.8055 | -0.0110 | +0.0033 |
| si | +0.2380 | +0.0247 | +0.0324 | -0.0334 |
