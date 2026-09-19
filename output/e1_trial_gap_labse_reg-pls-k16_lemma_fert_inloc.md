# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:01:46 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4574 | [+0.3680, +0.5371] | 30 | 11 | +0.3508 | [+0.0027, +0.6108] | -0.1067 | [-0.4694, +0.1712] |
| de | 570 | 193 | +0.5742 | [+0.5143, +0.6300] | 23 | 11 | +0.7892 | [+0.4717, +0.9175] | +0.2150 | [-0.1139, +0.3596] |
| en | 570 | 190 | +0.7749 | [+0.7365, +0.8101] | 30 | 10 | +0.6663 | [+0.5313, +0.7891] | -0.1086 | [-0.2523, +0.0236] |
| es | 593 | 208 | +0.6369 | [+0.5853, +0.6840] | 30 | 10 | +0.6850 | [+0.4390, +0.8487] | +0.0482 | [-0.1905, +0.2239] |
| fil | 570 | 555 | +0.3905 | [+0.3193, +0.4610] | 30 | 30 | +0.4993 | [+0.2341, +0.7050] | +0.1088 | [-0.1653, +0.3241] |
| fr | 569 | 191 | +0.5220 | [+0.4615, +0.5781] | 30 | 11 | +0.5084 | [+0.2979, +0.6889] | -0.0136 | [-0.2361, +0.1758] |
| it | 570 | 192 | +0.5957 | [+0.5402, +0.6499] | 30 | 10 | +0.6685 | [+0.4553, +0.8157] | +0.0728 | [-0.1467, +0.2364] |
| ja | 570 | 190 | +0.5570 | [+0.4831, +0.6238] | 30 | 10 | +0.6539 | [+0.3672, +0.8109] | +0.0969 | [-0.1976, +0.2689] |
| pt | 567 | 562 | +0.7230 | [+0.6799, +0.7612] | 30 | 30 | +0.7006 | [+0.4815, +0.8751] | -0.0224 | [-0.2452, +0.1556] |
| si | 600 | 578 | +0.3374 | [+0.2616, +0.4093] | 30 | 30 | +0.2541 | [-0.2438, +0.5632] | -0.0833 | [-0.5787, +0.2327] |
| **medie** | | | **+0.5569** | | | | **+0.5776** | | **+0.0207** | |

**Δ split mediu +0.0207**, sd intre limbi 0.1062, interval -0.1086 pana la +0.2150. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3508 | +0.3508 | +0.0000 |
| de | +0.7892 | +0.7892 | +0.0000 |
| en | +0.6663 | +0.6663 | +0.0000 |
| es | +0.6850 | +0.6850 | +0.0000 |
| fil | +0.4993 | +0.4993 | +0.0000 |
| fr | +0.5084 | +0.5084 | +0.0000 |
| it | +0.6685 | +0.6685 | +0.0000 |
| ja | +0.6539 | +0.6539 | +0.0000 |
| pt | +0.7006 | +0.7006 | +0.0000 |
| si | +0.2541 | +0.2541 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4008 | +0.4083 | +0.0566 | -0.0575 |
| de | +0.6274 | +0.8453 | -0.0532 | -0.0561 |
| en | +0.7658 | +0.6752 | +0.0091 | -0.0089 |
| es | +0.6505 | +0.6056 | -0.0136 | +0.0794 |
| fil | +0.3969 | +0.5126 | -0.0064 | -0.0133 |
| fr | +0.4514 | +0.2959 | +0.0706 | +0.2125 |
| it | +0.6049 | +0.6538 | -0.0092 | +0.0147 |
| ja | +0.5071 | +0.5095 | +0.0499 | +0.1444 |
| pt | +0.7239 | +0.7385 | -0.0009 | -0.0379 |
| si | +0.2532 | +0.2941 | +0.0842 | -0.0400 |
