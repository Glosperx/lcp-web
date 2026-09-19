# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:54:16 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3941 | [+0.3201, +0.4613] | 30 | 11 | +0.3611 | [-0.2072, +0.7751] | -0.0330 | [-0.6092, +0.3947] |
| de | 570 | 193 | +0.6234 | [+0.5711, +0.6721] | 23 | 11 | +0.7473 | [+0.4693, +0.8941] | +0.1238 | [-0.1645, +0.2765] |
| en | 570 | 190 | +0.8018 | [+0.7621, +0.8352] | 30 | 10 | +0.7024 | [+0.4641, +0.8881] | -0.0994 | [-0.3439, +0.0890] |
| es | 593 | 208 | +0.6705 | [+0.6268, +0.7106] | 30 | 10 | +0.6883 | [+0.4171, +0.8617] | +0.0179 | [-0.2526, +0.1939] |
| fil | 570 | 555 | +0.4085 | [+0.3388, +0.4730] | 30 | 30 | +0.5948 | [+0.3435, +0.8031] | +0.1863 | [-0.0697, +0.4049] |
| fr | 569 | 191 | +0.5572 | [+0.4891, +0.6173] | 30 | 11 | +0.3662 | [+0.0161, +0.6238] | -0.1910 | [-0.5399, +0.0757] |
| it | 570 | 192 | +0.6017 | [+0.5474, +0.6569] | 30 | 10 | +0.6891 | [+0.4886, +0.8300] | +0.0875 | [-0.1270, +0.2396] |
| ja | 570 | 190 | +0.5770 | [+0.5103, +0.6352] | 30 | 10 | +0.5832 | [+0.3693, +0.7416] | +0.0061 | [-0.2118, +0.1765] |
| pt | 567 | 562 | +0.7598 | [+0.7209, +0.7966] | 30 | 30 | +0.7783 | [+0.6012, +0.9114] | +0.0185 | [-0.1642, +0.1540] |
| si | 600 | 578 | +0.2845 | [+0.2146, +0.3531] | 30 | 30 | -0.0915 | [-0.4588, +0.2829] | -0.3759 | [-0.7450, +0.0008] |
| **medie** | | | **+0.5678** | | | | **+0.5419** | | **-0.0259** | |

**Δ split mediu -0.0259**, sd intre limbi 0.1634, interval -0.3759 pana la +0.1863. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3611 | +0.3408 | -0.0203 |
| de | +0.7473 | +0.7324 | -0.0149 |
| en | +0.7024 | +0.7021 | -0.0003 |
| es | +0.6883 | +0.6994 | +0.0111 |
| fil | +0.5948 | +0.6329 | +0.0381 |
| fr | +0.3662 | +0.3434 | -0.0228 |
| it | +0.6891 | +0.6898 | +0.0007 |
| ja | +0.5832 | +0.5107 | -0.0725 |
| pt | +0.7783 | +0.7800 | +0.0017 |
| si | -0.0915 | +0.0132 | +0.1047 |

**Diferenta medie +0.0025**, interval -0.0725 pana la +0.1047.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3804 | +0.3042 | +0.0137 | +0.0569 |
| de | +0.6388 | +0.8080 | -0.0154 | -0.0607 |
| en | +0.8048 | +0.6825 | -0.0030 | +0.0199 |
| es | +0.6681 | +0.6622 | +0.0024 | +0.0261 |
| fil | +0.4077 | +0.5851 | +0.0008 | +0.0097 |
| fr | +0.5546 | +0.3641 | +0.0026 | +0.0021 |
| it | +0.6100 | +0.7323 | -0.0083 | -0.0432 |
| ja | +0.6009 | +0.5302 | -0.0239 | +0.0530 |
| pt | +0.7770 | +0.7653 | -0.0172 | +0.0130 |
| si | +0.2478 | -0.2227 | +0.0367 | +0.1312 |
