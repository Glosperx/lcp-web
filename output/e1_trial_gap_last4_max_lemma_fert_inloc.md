# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:04:07 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4268 | [+0.3428, +0.5034] | 30 | 11 | +0.2610 | [-0.1980, +0.6623] | -0.1658 | [-0.6348, +0.2514] |
| de | 570 | 193 | +0.6610 | [+0.6091, +0.7100] | 23 | 11 | +0.7650 | [+0.4769, +0.8955] | +0.1039 | [-0.1944, +0.2507] |
| en | 570 | 190 | +0.8098 | [+0.7696, +0.8444] | 30 | 10 | +0.7097 | [+0.4371, +0.8428] | -0.1001 | [-0.3752, +0.0395] |
| es | 593 | 208 | +0.6596 | [+0.6133, +0.7017] | 30 | 10 | +0.6799 | [+0.3958, +0.8409] | +0.0203 | [-0.2536, +0.1890] |
| fil | 570 | 555 | +0.3998 | [+0.3276, +0.4678] | 30 | 30 | +0.6075 | [+0.3764, +0.7801] | +0.2076 | [-0.0284, +0.3990] |
| fr | 569 | 191 | +0.5361 | [+0.4674, +0.6002] | 30 | 11 | +0.3622 | [-0.0204, +0.6693] | -0.1740 | [-0.5541, +0.1376] |
| it | 570 | 192 | +0.6263 | [+0.5715, +0.6811] | 30 | 10 | +0.6589 | [+0.4093, +0.8325] | +0.0326 | [-0.2287, +0.2209] |
| ja | 570 | 190 | +0.5894 | [+0.5246, +0.6464] | 30 | 10 | +0.4848 | [+0.2294, +0.6654] | -0.1046 | [-0.3754, +0.0798] |
| pt | 567 | 562 | +0.7558 | [+0.7134, +0.7930] | 30 | 30 | +0.8154 | [+0.6537, +0.9187] | +0.0596 | [-0.1058, +0.1718] |
| si | 600 | 578 | +0.2378 | [+0.1726, +0.3056] | 30 | 30 | +0.1051 | [-0.2789, +0.5366] | -0.1327 | [-0.5263, +0.3060] |
| **medie** | | | **+0.5702** | | | | **+0.5450** | | **-0.0253** | |

**Δ split mediu -0.0253**, sd intre limbi 0.1286, interval -0.1740 pana la +0.2076. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2610 | +0.2201 | -0.0409 |
| de | +0.7650 | +0.7692 | +0.0042 |
| en | +0.7097 | +0.7024 | -0.0073 |
| es | +0.6799 | +0.6847 | +0.0048 |
| fil | +0.6075 | +0.6097 | +0.0022 |
| fr | +0.3622 | +0.3416 | -0.0206 |
| it | +0.6589 | +0.6661 | +0.0072 |
| ja | +0.4848 | +0.4639 | -0.0209 |
| pt | +0.8154 | +0.8162 | +0.0008 |
| si | +0.1051 | +0.1754 | +0.0703 |

**Diferenta medie -0.0000**, interval -0.0409 pana la +0.0703.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4238 | +0.2722 | +0.0030 | -0.0112 |
| de | +0.6753 | +0.8295 | -0.0143 | -0.0645 |
| en | +0.8005 | +0.7413 | +0.0093 | -0.0316 |
| es | +0.6568 | +0.6573 | +0.0028 | +0.0226 |
| fil | +0.4140 | +0.5695 | -0.0142 | +0.0380 |
| fr | +0.5386 | +0.3930 | -0.0025 | -0.0308 |
| it | +0.6269 | +0.6338 | -0.0006 | +0.0251 |
| ja | +0.5936 | +0.4667 | -0.0042 | +0.0181 |
| pt | +0.7629 | +0.7902 | -0.0071 | +0.0252 |
| si | +0.1934 | +0.1680 | +0.0444 | -0.0629 |
