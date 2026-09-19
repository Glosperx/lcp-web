# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:58:07 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3647 | [+0.2729, +0.4574] | 30 | 11 | +0.2229 | [-0.1294, +0.6155] | -0.1418 | [-0.5146, +0.2725] |
| de | 570 | 193 | +0.5924 | [+0.5265, +0.6518] | 23 | 11 | +0.5885 | [+0.2530, +0.8032] | -0.0039 | [-0.3467, +0.2109] |
| en | 570 | 190 | +0.7666 | [+0.7190, +0.8075] | 30 | 10 | +0.5543 | [+0.3573, +0.8181] | -0.2123 | [-0.4062, +0.0567] |
| es | 593 | 208 | +0.6225 | [+0.5724, +0.6698] | 30 | 10 | +0.6412 | [+0.3130, +0.8343] | +0.0187 | [-0.3108, +0.2166] |
| fil | 570 | 555 | +0.3711 | [+0.3012, +0.4373] | 30 | 30 | +0.3638 | [+0.0793, +0.6135] | -0.0073 | [-0.3117, +0.2478] |
| fr | 569 | 191 | +0.5182 | [+0.4457, +0.5815] | 30 | 11 | +0.4141 | [+0.0566, +0.6704] | -0.1041 | [-0.4668, +0.1599] |
| it | 570 | 192 | +0.5563 | [+0.4897, +0.6229] | 30 | 10 | +0.6367 | [+0.3481, +0.8443] | +0.0804 | [-0.2094, +0.3056] |
| ja | 570 | 190 | +0.5480 | [+0.4794, +0.6114] | 30 | 10 | +0.4217 | [+0.2184, +0.5690] | -0.1263 | [-0.3414, +0.0379] |
| pt | 567 | 562 | +0.6877 | [+0.6394, +0.7325] | 30 | 30 | +0.7140 | [+0.5300, +0.8561] | +0.0262 | [-0.1639, +0.1732] |
| si | 600 | 578 | +0.2489 | [+0.1862, +0.3124] | 30 | 30 | +0.0936 | [-0.2146, +0.3988] | -0.1554 | [-0.4661, +0.1565] |
| **medie** | | | **+0.5276** | | | | **+0.4651** | | **-0.0626** | |

**Δ split mediu -0.0626**, sd intre limbi 0.0969, interval -0.2123 pana la +0.0804. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2229 | +0.1645 | -0.0584 |
| de | +0.5885 | +0.5849 | -0.0036 |
| en | +0.5543 | +0.5448 | -0.0095 |
| es | +0.6412 | +0.6348 | -0.0064 |
| fil | +0.3638 | +0.3868 | +0.0230 |
| fr | +0.4141 | +0.4086 | -0.0055 |
| it | +0.6367 | +0.6239 | -0.0128 |
| ja | +0.4217 | +0.4062 | -0.0155 |
| pt | +0.7140 | +0.7144 | +0.0004 |
| si | +0.0936 | +0.0759 | -0.0177 |

**Diferenta medie -0.0106**, interval -0.0584 pana la +0.0230.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3345 | +0.3017 | +0.0302 | -0.0788 |
| de | +0.5684 | +0.5254 | +0.0240 | +0.0631 |
| en | +0.7684 | +0.5520 | -0.0018 | +0.0023 |
| es | +0.6341 | +0.6681 | -0.0116 | -0.0269 |
| fil | +0.3770 | +0.3607 | -0.0059 | +0.0031 |
| fr | +0.4931 | +0.4636 | +0.0251 | -0.0495 |
| it | +0.5450 | +0.6514 | +0.0113 | -0.0147 |
| ja | +0.5344 | +0.3990 | +0.0136 | +0.0227 |
| pt | +0.6817 | +0.6956 | +0.0060 | +0.0184 |
| si | +0.2674 | +0.1797 | -0.0185 | -0.0861 |
