# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:45:01 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4245 | [+0.3334, +0.5065] | 30 | 11 | +0.4947 | [+0.2183, +0.7055] | +0.0702 | [-0.2222, +0.2987] |
| de | 570 | 193 | +0.4931 | [+0.4289, +0.5543] | 23 | 11 | +0.7531 | [+0.5559, +0.8997] | +0.2600 | [+0.0520, +0.4188] |
| en | 570 | 190 | +0.7836 | [+0.7426, +0.8215] | 30 | 10 | +0.6356 | [+0.3276, +0.8531] | -0.1480 | [-0.4548, +0.0726] |
| es | 593 | 208 | +0.6878 | [+0.6409, +0.7309] | 30 | 10 | +0.6953 | [+0.3328, +0.8981] | +0.0075 | [-0.3644, +0.2159] |
| fil | 570 | 555 | +0.3883 | [+0.3157, +0.4590] | 30 | 30 | +0.4127 | [+0.0902, +0.6550] | +0.0243 | [-0.3095, +0.2891] |
| fr | 569 | 191 | +0.5052 | [+0.4384, +0.5709] | 30 | 11 | +0.3471 | [+0.1016, +0.6057] | -0.1581 | [-0.4185, +0.1150] |
| it | 570 | 192 | +0.5449 | [+0.4850, +0.6052] | 30 | 10 | +0.6117 | [+0.3105, +0.8173] | +0.0668 | [-0.2360, +0.2837] |
| ja | 570 | 190 | +0.5414 | [+0.4693, +0.6083] | 30 | 10 | +0.6780 | [+0.4502, +0.8324] | +0.1366 | [-0.1002, +0.2970] |
| pt | 567 | 562 | +0.7206 | [+0.6681, +0.7646] | 30 | 30 | +0.6803 | [+0.4745, +0.8248] | -0.0403 | [-0.2477, +0.1106] |
| si | 600 | 578 | +0.2296 | [+0.1657, +0.2952] | 30 | 30 | +0.2706 | [+0.0564, +0.5046] | +0.0410 | [-0.1741, +0.2908] |
| **medie** | | | **+0.5319** | | | | **+0.5579** | | **+0.0260** | |

**Δ split mediu +0.0260**, sd intre limbi 0.1246, interval -0.1581 pana la +0.2600. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4947 | +0.4966 | +0.0019 |
| de | +0.7531 | +0.7385 | -0.0146 |
| en | +0.6356 | +0.6597 | +0.0241 |
| es | +0.6953 | +0.6784 | -0.0169 |
| fil | +0.4127 | +0.4392 | +0.0265 |
| fr | +0.3471 | +0.3400 | -0.0071 |
| it | +0.6117 | +0.6390 | +0.0273 |
| ja | +0.6780 | +0.6866 | +0.0086 |
| pt | +0.6803 | +0.6947 | +0.0144 |
| si | +0.2706 | +0.2472 | -0.0234 |

**Diferenta medie +0.0041**, interval -0.0234 pana la +0.0273.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3944 | +0.6160 | +0.0301 | -0.1213 |
| de | +0.5132 | +0.7543 | -0.0201 | -0.0012 |
| en | +0.7677 | +0.5814 | +0.0159 | +0.0542 |
| es | +0.6658 | +0.6794 | +0.0220 | +0.0159 |
| fil | +0.3873 | +0.4473 | +0.0010 | -0.0346 |
| fr | +0.4784 | +0.2550 | +0.0268 | +0.0921 |
| it | +0.5504 | +0.6303 | -0.0055 | -0.0186 |
| ja | +0.4533 | +0.3867 | +0.0881 | +0.2913 |
| pt | +0.7255 | +0.7051 | -0.0049 | -0.0248 |
| si | +0.2340 | +0.2011 | -0.0044 | +0.0695 |
