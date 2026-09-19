# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:06:04 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4134 | [+0.3223, +0.4957] | 30 | 11 | +0.4757 | [+0.1984, +0.6884] | +0.0623 | [-0.2298, +0.2891] |
| de | 570 | 193 | +0.5315 | [+0.4649, +0.5915] | 23 | 11 | +0.7802 | [+0.5639, +0.9067] | +0.2487 | [+0.0287, +0.3898] |
| en | 570 | 190 | +0.7785 | [+0.7343, +0.8182] | 30 | 10 | +0.6152 | [+0.4998, +0.8351] | -0.1633 | [-0.2861, +0.0608] |
| es | 593 | 208 | +0.6097 | [+0.5548, +0.6591] | 30 | 10 | +0.7266 | [+0.5938, +0.8481] | +0.1169 | [-0.0233, +0.2461] |
| fil | 570 | 555 | +0.3600 | [+0.2846, +0.4350] | 30 | 30 | +0.2607 | [-0.0416, +0.5307] | -0.0993 | [-0.4115, +0.1894] |
| fr | 569 | 191 | +0.5049 | [+0.4361, +0.5691] | 30 | 11 | +0.4246 | [+0.1294, +0.6687] | -0.0802 | [-0.3927, +0.1705] |
| it | 570 | 192 | +0.5321 | [+0.4688, +0.5942] | 30 | 10 | +0.6541 | [+0.4503, +0.8028] | +0.1219 | [-0.0888, +0.2878] |
| ja | 570 | 190 | +0.4810 | [+0.4031, +0.5540] | 30 | 10 | +0.6275 | [+0.3663, +0.7794] | +0.1465 | [-0.1241, +0.3152] |
| pt | 567 | 562 | +0.6968 | [+0.6472, +0.7409] | 30 | 30 | +0.7097 | [+0.4908, +0.8965] | +0.0128 | [-0.2085, +0.1991] |
| si | 600 | 578 | +0.3207 | [+0.2429, +0.3958] | 30 | 30 | +0.4367 | [-0.0283, +0.7194] | +0.1160 | [-0.3584, +0.4111] |
| **medie** | | | **+0.5229** | | | | **+0.5711** | | **+0.0482** | |

**Δ split mediu +0.0482**, sd intre limbi 0.1287, interval -0.1633 pana la +0.2487. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4757 | +0.4610 | -0.0147 |
| de | +0.7802 | +0.7997 | +0.0195 |
| en | +0.6152 | +0.6216 | +0.0064 |
| es | +0.7266 | +0.7513 | +0.0247 |
| fil | +0.2607 | +0.2660 | +0.0053 |
| fr | +0.4246 | +0.5302 | +0.1056 |
| it | +0.6541 | +0.6719 | +0.0178 |
| ja | +0.6275 | +0.6402 | +0.0127 |
| pt | +0.7097 | +0.6960 | -0.0137 |
| si | +0.4367 | +0.4198 | -0.0169 |

**Diferenta medie +0.0147**, interval -0.0169 pana la +0.1056.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4189 | +0.5507 | -0.0055 | -0.0750 |
| de | +0.6063 | +0.8838 | -0.0748 | -0.1036 |
| en | +0.7913 | +0.6705 | -0.0128 | -0.0553 |
| es | +0.6244 | +0.7170 | -0.0147 | +0.0096 |
| fil | +0.3695 | +0.2947 | -0.0095 | -0.0340 |
| fr | +0.5169 | +0.3227 | -0.0120 | +0.1019 |
| it | +0.5556 | +0.7025 | -0.0235 | -0.0484 |
| ja | +0.5680 | +0.6169 | -0.0870 | +0.0106 |
| pt | +0.7225 | +0.6989 | -0.0257 | +0.0108 |
| si | +0.2790 | +0.3994 | +0.0417 | +0.0373 |
