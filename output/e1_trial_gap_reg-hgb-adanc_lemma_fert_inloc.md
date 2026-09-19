# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 12:43:22 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3948 | [+0.3136, +0.4686] | 30 | 11 | +0.3412 | [-0.2131, +0.7304] | -0.0536 | [-0.6178, +0.3504] |
| de | 570 | 193 | +0.6434 | [+0.5902, +0.6938] | 23 | 11 | +0.8107 | [+0.5802, +0.9205] | +0.1674 | [-0.0771, +0.2910] |
| en | 570 | 190 | +0.8225 | [+0.7851, +0.8558] | 30 | 10 | +0.7065 | [+0.4358, +0.8688] | -0.1160 | [-0.3969, +0.0495] |
| es | 593 | 208 | +0.6595 | [+0.6142, +0.6994] | 30 | 10 | +0.7123 | [+0.4468, +0.8684] | +0.0528 | [-0.2126, +0.2108] |
| fil | 570 | 555 | +0.4127 | [+0.3431, +0.4774] | 30 | 30 | +0.5709 | [+0.3138, +0.7844] | +0.1582 | [-0.1000, +0.3804] |
| fr | 569 | 191 | +0.5252 | [+0.4571, +0.5873] | 30 | 11 | +0.4141 | [+0.0448, +0.6670] | -0.1111 | [-0.4798, +0.1520] |
| it | 570 | 192 | +0.6131 | [+0.5580, +0.6697] | 30 | 10 | +0.6964 | [+0.4884, +0.8364] | +0.0833 | [-0.1288, +0.2403] |
| ja | 570 | 190 | +0.3300 | [+0.2507, +0.4060] | 30 | 10 | +0.2628 | [-0.1202, +0.4764] | -0.0672 | [-0.4547, +0.1626] |
| pt | 567 | 562 | +0.7569 | [+0.7181, +0.7940] | 30 | 30 | +0.7757 | [+0.5887, +0.9069] | +0.0187 | [-0.1758, +0.1529] |
| si | 600 | 578 | +0.1629 | [+0.0956, +0.2357] | 30 | 30 | -0.1107 | [-0.4833, +0.2703] | -0.2735 | [-0.6576, +0.1156] |
| **medie** | | | **+0.5321** | | | | **+0.5180** | | **-0.0141** | |

**Δ split mediu -0.0141**, sd intre limbi 0.1371, interval -0.2735 pana la +0.1674. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3412 | +0.2692 | -0.0720 |
| de | +0.8107 | +0.8200 | +0.0093 |
| en | +0.7065 | +0.6727 | -0.0338 |
| es | +0.7123 | +0.6810 | -0.0313 |
| fil | +0.5709 | +0.6228 | +0.0519 |
| fr | +0.4141 | +0.3768 | -0.0373 |
| it | +0.6964 | +0.6610 | -0.0354 |
| ja | +0.2628 | +0.1307 | -0.1321 |
| pt | +0.7757 | +0.7723 | -0.0034 |
| si | -0.1107 | -0.0438 | +0.0669 |

**Diferenta medie -0.0217**, interval -0.1321 pana la +0.0669.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4085 | +0.2405 | -0.0137 | +0.1007 |
| de | +0.6406 | +0.8434 | +0.0028 | -0.0327 |
| en | +0.8176 | +0.6569 | +0.0049 | +0.0496 |
| es | +0.6689 | +0.6907 | -0.0094 | +0.0216 |
| fil | +0.3887 | +0.5296 | +0.0240 | +0.0413 |
| fr | +0.5263 | +0.4131 | -0.0011 | +0.0010 |
| it | +0.6081 | +0.7873 | +0.0050 | -0.0909 |
| ja | +0.5986 | +0.4965 | -0.2686 | -0.2337 |
| pt | +0.7630 | +0.7854 | -0.0061 | -0.0097 |
| si | +0.2056 | -0.1623 | -0.0427 | +0.0516 |
