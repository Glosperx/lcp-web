# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:04:22 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4606 | [+0.3733, +0.5398] | 30 | 11 | +0.3870 | [+0.0747, +0.6337] | -0.0736 | [-0.4056, +0.1923] |
| de | 570 | 193 | +0.5701 | [+0.5110, +0.6259] | 23 | 11 | +0.7954 | [+0.4755, +0.9235] | +0.2253 | [-0.1006, +0.3679] |
| en | 570 | 190 | +0.7824 | [+0.7447, +0.8163] | 30 | 10 | +0.6639 | [+0.5454, +0.8037] | -0.1185 | [-0.2398, +0.0296] |
| es | 593 | 208 | +0.6441 | [+0.5947, +0.6894] | 30 | 10 | +0.6890 | [+0.4810, +0.8351] | +0.0449 | [-0.1644, +0.1998] |
| fil | 570 | 555 | +0.3944 | [+0.3228, +0.4640] | 30 | 30 | +0.4848 | [+0.2129, +0.6923] | +0.0904 | [-0.1820, +0.3152] |
| fr | 569 | 191 | +0.5287 | [+0.4679, +0.5857] | 30 | 11 | +0.5143 | [+0.2990, +0.6933] | -0.0144 | [-0.2310, +0.1751] |
| it | 570 | 192 | +0.5925 | [+0.5380, +0.6470] | 30 | 10 | +0.6823 | [+0.4770, +0.8226] | +0.0898 | [-0.1213, +0.2478] |
| ja | 570 | 190 | +0.5655 | [+0.4910, +0.6325] | 30 | 10 | +0.6649 | [+0.3850, +0.8184] | +0.0994 | [-0.1912, +0.2717] |
| pt | 567 | 562 | +0.7241 | [+0.6812, +0.7618] | 30 | 30 | +0.7015 | [+0.4879, +0.8836] | -0.0226 | [-0.2395, +0.1609] |
| si | 600 | 578 | +0.3567 | [+0.2851, +0.4248] | 30 | 30 | +0.2937 | [-0.2017, +0.5891] | -0.0629 | [-0.5647, +0.2388] |
| **medie** | | | **+0.5619** | | | | **+0.5877** | | **+0.0258** | |

**Δ split mediu +0.0258**, sd intre limbi 0.1035, interval -0.1185 pana la +0.2253. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3870 | +0.3870 | +0.0000 |
| de | +0.7954 | +0.7954 | +0.0000 |
| en | +0.6639 | +0.6639 | +0.0000 |
| es | +0.6890 | +0.6890 | +0.0000 |
| fil | +0.4848 | +0.4848 | +0.0000 |
| fr | +0.5143 | +0.5143 | +0.0000 |
| it | +0.6823 | +0.6823 | +0.0000 |
| ja | +0.6649 | +0.6649 | +0.0000 |
| pt | +0.7015 | +0.7015 | +0.0000 |
| si | +0.2937 | +0.2937 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4258 | +0.4579 | +0.0348 | -0.0709 |
| de | +0.6294 | +0.8520 | -0.0593 | -0.0566 |
| en | +0.7798 | +0.6761 | +0.0026 | -0.0122 |
| es | +0.6657 | +0.6069 | -0.0216 | +0.0821 |
| fil | +0.4137 | +0.5111 | -0.0193 | -0.0263 |
| fr | +0.4802 | +0.3669 | +0.0485 | +0.1474 |
| it | +0.5983 | +0.6846 | -0.0058 | -0.0023 |
| ja | +0.5422 | +0.5497 | +0.0233 | +0.1152 |
| pt | +0.7321 | +0.7443 | -0.0080 | -0.0428 |
| si | +0.3078 | +0.3055 | +0.0489 | -0.0118 |
