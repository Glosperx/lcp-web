# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:59:30 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4386 | [+0.3496, +0.5167] | 30 | 11 | +0.2487 | [-0.2908, +0.6357] | -0.1899 | [-0.7347, +0.2196] |
| de | 570 | 193 | +0.6648 | [+0.6112, +0.7133] | 23 | 11 | +0.8054 | [+0.5166, +0.9256] | +0.1406 | [-0.1583, +0.2740] |
| en | 570 | 190 | +0.8124 | [+0.7731, +0.8446] | 30 | 10 | +0.7147 | [+0.4636, +0.8512] | -0.0977 | [-0.3577, +0.0479] |
| es | 593 | 208 | +0.6666 | [+0.6195, +0.7088] | 30 | 10 | +0.6939 | [+0.3934, +0.8590] | +0.0273 | [-0.2694, +0.1976] |
| fil | 570 | 555 | +0.3892 | [+0.3175, +0.4541] | 30 | 30 | +0.6067 | [+0.3715, +0.7780] | +0.2175 | [-0.0338, +0.4048] |
| fr | 569 | 191 | +0.5345 | [+0.4674, +0.5939] | 30 | 11 | +0.3416 | [-0.0512, +0.6475] | -0.1928 | [-0.5986, +0.1263] |
| it | 570 | 192 | +0.6418 | [+0.5883, +0.6959] | 30 | 10 | +0.6385 | [+0.4068, +0.8049] | -0.0033 | [-0.2403, +0.1792] |
| ja | 570 | 190 | +0.6272 | [+0.5572, +0.6880] | 30 | 10 | +0.5583 | [+0.3545, +0.7043] | -0.0689 | [-0.2786, +0.0861] |
| pt | 567 | 562 | +0.7649 | [+0.7252, +0.8006] | 30 | 30 | +0.8008 | [+0.6518, +0.9083] | +0.0359 | [-0.1156, +0.1485] |
| si | 600 | 578 | +0.2728 | [+0.1989, +0.3412] | 30 | 30 | -0.0412 | [-0.4014, +0.3732] | -0.3140 | [-0.6749, +0.1066] |
| **medie** | | | **+0.5813** | | | | **+0.5367** | | **-0.0445** | |

**Δ split mediu -0.0445**, sd intre limbi 0.1617, interval -0.3140 pana la +0.2175. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2487 | +0.2433 | -0.0054 |
| de | +0.8054 | +0.8077 | +0.0023 |
| en | +0.7147 | +0.6901 | -0.0246 |
| es | +0.6939 | +0.6955 | +0.0016 |
| fil | +0.6067 | +0.6048 | -0.0019 |
| fr | +0.3416 | +0.3129 | -0.0287 |
| it | +0.6385 | +0.6234 | -0.0151 |
| ja | +0.5583 | +0.5215 | -0.0368 |
| pt | +0.8008 | +0.7966 | -0.0042 |
| si | -0.0412 | -0.0303 | +0.0109 |

**Diferenta medie -0.0102**, interval -0.0368 pana la +0.0109.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4162 | +0.2369 | +0.0224 | +0.0118 |
| de | +0.6623 | +0.8200 | +0.0025 | -0.0146 |
| en | +0.8077 | +0.6797 | +0.0047 | +0.0350 |
| es | +0.6520 | +0.6824 | +0.0146 | +0.0115 |
| fil | +0.4017 | +0.5577 | -0.0125 | +0.0490 |
| fr | +0.5274 | +0.3432 | +0.0071 | -0.0016 |
| it | +0.6245 | +0.6814 | +0.0173 | -0.0429 |
| ja | +0.6004 | +0.4658 | +0.0268 | +0.0925 |
| pt | +0.7672 | +0.7801 | -0.0023 | +0.0207 |
| si | +0.2906 | -0.0162 | -0.0178 | -0.0250 |
