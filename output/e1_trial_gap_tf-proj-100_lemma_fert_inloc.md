# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 13:13:00 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4110 | [+0.3269, +0.4846] | 30 | 11 | +0.4244 | [-0.0540, +0.7580] | +0.0134 | [-0.4614, +0.3577] |
| de | 570 | 193 | +0.6370 | [+0.5838, +0.6868] | 23 | 11 | +0.7987 | [+0.5637, +0.8975] | +0.1617 | [-0.0758, +0.2753] |
| en | 570 | 190 | +0.8086 | [+0.7706, +0.8414] | 30 | 10 | +0.6966 | [+0.5272, +0.8470] | -0.1120 | [-0.2859, +0.0444] |
| es | 593 | 208 | +0.6852 | [+0.6414, +0.7256] | 30 | 10 | +0.7016 | [+0.3967, +0.8744] | +0.0164 | [-0.2960, +0.1928] |
| fil | 570 | 555 | +0.4157 | [+0.3450, +0.4830] | 30 | 30 | +0.5987 | [+0.3726, +0.7854] | +0.1830 | [-0.0480, +0.3863] |
| fr | 569 | 191 | +0.5432 | [+0.4749, +0.6020] | 30 | 11 | +0.3646 | [+0.0015, +0.6515] | -0.1786 | [-0.5526, +0.1256] |
| it | 570 | 192 | +0.6315 | [+0.5777, +0.6834] | 30 | 10 | +0.6705 | [+0.4164, +0.8436] | +0.0390 | [-0.2164, +0.2273] |
| ja | 570 | 190 | +0.5631 | [+0.4973, +0.6234] | 30 | 10 | +0.5673 | [+0.3461, +0.7285] | +0.0043 | [-0.2241, +0.1776] |
| pt | 567 | 562 | +0.7697 | [+0.7319, +0.8036] | 30 | 30 | +0.7912 | [+0.6155, +0.9169] | +0.0215 | [-0.1597, +0.1495] |
| si | 600 | 578 | +0.1630 | [+0.0916, +0.2386] | 30 | 30 | -0.0131 | [-0.3568, +0.4035] | -0.1761 | [-0.5221, +0.2497] |
| **medie** | | | **+0.5628** | | | | **+0.5601** | | **-0.0027** | |

**Δ split mediu -0.0027**, sd intre limbi 0.1236, interval -0.1786 pana la +0.1830. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4244 | +0.3649 | -0.0595 |
| de | +0.7987 | +0.8112 | +0.0125 |
| en | +0.6966 | +0.6945 | -0.0021 |
| es | +0.7016 | +0.6994 | -0.0022 |
| fil | +0.5987 | +0.6174 | +0.0187 |
| fr | +0.3646 | +0.3150 | -0.0496 |
| it | +0.6705 | +0.6697 | -0.0008 |
| ja | +0.5673 | +0.5405 | -0.0268 |
| pt | +0.7912 | +0.7934 | +0.0022 |
| si | -0.0131 | +0.0881 | +0.1012 |

**Diferenta medie -0.0006**, interval -0.0595 pana la +0.1012.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3910 | +0.2838 | +0.0200 | +0.1406 |
| de | +0.6773 | +0.8365 | -0.0403 | -0.0378 |
| en | +0.8110 | +0.6740 | -0.0024 | +0.0226 |
| es | +0.6750 | +0.6894 | +0.0102 | +0.0122 |
| fil | +0.3991 | +0.5875 | +0.0166 | +0.0112 |
| fr | +0.5363 | +0.3365 | +0.0069 | +0.0281 |
| it | +0.6314 | +0.7019 | +0.0001 | -0.0314 |
| ja | +0.5895 | +0.5051 | -0.0264 | +0.0622 |
| pt | +0.7702 | +0.7816 | -0.0005 | +0.0096 |
| si | +0.1221 | -0.0715 | +0.0409 | +0.0584 |
