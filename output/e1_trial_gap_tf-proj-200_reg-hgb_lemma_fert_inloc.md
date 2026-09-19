# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 13:16:04 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3979 | [+0.3186, +0.4699] | 30 | 11 | +0.3946 | [-0.1193, +0.7704] | -0.0033 | [-0.5265, +0.3787] |
| de | 570 | 193 | +0.6212 | [+0.5699, +0.6705] | 23 | 11 | +0.7276 | [+0.5186, +0.8473] | +0.1063 | [-0.1026, +0.2422] |
| en | 570 | 190 | +0.8161 | [+0.7780, +0.8496] | 30 | 10 | +0.7597 | [+0.4959, +0.8819] | -0.0564 | [-0.3251, +0.0744] |
| es | 593 | 208 | +0.6686 | [+0.6236, +0.7103] | 30 | 10 | +0.6924 | [+0.4331, +0.8589] | +0.0238 | [-0.2343, +0.1932] |
| fil | 570 | 555 | +0.4282 | [+0.3584, +0.4949] | 30 | 30 | +0.5880 | [+0.3374, +0.8016] | +0.1599 | [-0.1019, +0.3834] |
| fr | 569 | 191 | +0.5400 | [+0.4690, +0.6041] | 30 | 11 | +0.4118 | [+0.0770, +0.6706] | -0.1282 | [-0.4748, +0.1352] |
| it | 570 | 192 | +0.6083 | [+0.5546, +0.6635] | 30 | 10 | +0.6818 | [+0.4499, +0.8352] | +0.0736 | [-0.1641, +0.2427] |
| ja | 570 | 190 | +0.3987 | [+0.3273, +0.4638] | 30 | 10 | +0.4306 | [+0.0199, +0.7010] | +0.0318 | [-0.3837, +0.3084] |
| pt | 567 | 562 | +0.7566 | [+0.7181, +0.7932] | 30 | 30 | +0.7695 | [+0.5985, +0.8861] | +0.0129 | [-0.1673, +0.1312] |
| si | 600 | 578 | +0.0877 | [+0.0209, +0.1556] | 30 | 30 | -0.0598 | [-0.3402, +0.2780] | -0.1474 | [-0.4366, +0.1919] |
| **medie** | | | **+0.5323** | | | | **+0.5396** | | **+0.0073** | |

**Δ split mediu +0.0073**, sd intre limbi 0.0971, interval -0.1474 pana la +0.1599. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3946 | +0.3120 | -0.0826 |
| de | +0.7276 | +0.7474 | +0.0198 |
| en | +0.7597 | +0.7525 | -0.0072 |
| es | +0.6924 | +0.6875 | -0.0049 |
| fil | +0.5880 | +0.6283 | +0.0403 |
| fr | +0.4118 | +0.3597 | -0.0521 |
| it | +0.6818 | +0.6827 | +0.0009 |
| ja | +0.4306 | +0.3767 | -0.0539 |
| pt | +0.7695 | +0.7817 | +0.0122 |
| si | -0.0598 | +0.0463 | +0.1061 |

**Diferenta medie -0.0021**, interval -0.0826 pana la +0.1061.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3847 | +0.2159 | +0.0132 | +0.1787 |
| de | +0.6523 | +0.8487 | -0.0311 | -0.1211 |
| en | +0.8244 | +0.7149 | -0.0083 | +0.0448 |
| es | +0.6609 | +0.6648 | +0.0077 | +0.0276 |
| fil | +0.4050 | +0.5914 | +0.0232 | -0.0034 |
| fr | +0.5145 | +0.3415 | +0.0255 | +0.0703 |
| it | +0.6036 | +0.7328 | +0.0047 | -0.0510 |
| ja | +0.6023 | +0.5108 | -0.2036 | -0.0802 |
| pt | +0.7628 | +0.7860 | -0.0062 | -0.0165 |
| si | +0.0415 | -0.1270 | +0.0462 | +0.0672 |
