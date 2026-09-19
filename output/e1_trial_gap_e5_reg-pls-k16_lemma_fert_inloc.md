# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:40:12 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4365 | [+0.3381, +0.5202] | 30 | 11 | +0.3676 | [-0.0039, +0.6410] | -0.0688 | [-0.4554, +0.2195] |
| de | 570 | 193 | +0.5831 | [+0.5227, +0.6381] | 23 | 11 | +0.8279 | [+0.6104, +0.9283] | +0.2448 | [+0.0249, +0.3637] |
| en | 570 | 190 | +0.7734 | [+0.7344, +0.8097] | 30 | 10 | +0.6698 | [+0.4012, +0.8520] | -0.1037 | [-0.3755, +0.0817] |
| es | 593 | 208 | +0.6857 | [+0.6419, +0.7242] | 30 | 10 | +0.6450 | [+0.2826, +0.8717] | -0.0407 | [-0.3960, +0.1944] |
| fil | 570 | 555 | +0.4112 | [+0.3382, +0.4783] | 30 | 30 | +0.5440 | [+0.2754, +0.7498] | +0.1328 | [-0.1406, +0.3491] |
| fr | 569 | 191 | +0.5309 | [+0.4688, +0.5924] | 30 | 11 | +0.3146 | [+0.0965, +0.5268] | -0.2163 | [-0.4472, +0.0000] |
| it | 570 | 192 | +0.6108 | [+0.5570, +0.6643] | 30 | 10 | +0.5899 | [+0.3333, +0.7867] | -0.0209 | [-0.2862, +0.1846] |
| ja | 570 | 190 | +0.5953 | [+0.5288, +0.6576] | 30 | 10 | +0.7358 | [+0.5553, +0.8609] | +0.1405 | [-0.0538, +0.2811] |
| pt | 567 | 562 | +0.7115 | [+0.6596, +0.7562] | 30 | 30 | +0.6807 | [+0.4690, +0.8341] | -0.0307 | [-0.2487, +0.1282] |
| si | 600 | 578 | +0.1912 | [+0.1210, +0.2644] | 30 | 30 | +0.3542 | [+0.1436, +0.5986] | +0.1629 | [-0.0583, +0.4266] |
| **medie** | | | **+0.5530** | | | | **+0.5729** | | **+0.0200** | |

**Δ split mediu +0.0200**, sd intre limbi 0.1434, interval -0.2163 pana la +0.2448. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3676 | +0.3676 | +0.0000 |
| de | +0.8279 | +0.8279 | +0.0000 |
| en | +0.6698 | +0.6698 | +0.0000 |
| es | +0.6450 | +0.6450 | +0.0000 |
| fil | +0.5440 | +0.5440 | +0.0000 |
| fr | +0.3146 | +0.3146 | +0.0000 |
| it | +0.5899 | +0.5899 | +0.0000 |
| ja | +0.7358 | +0.7358 | +0.0000 |
| pt | +0.6807 | +0.6807 | +0.0000 |
| si | +0.3542 | +0.3542 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4206 | +0.4252 | +0.0159 | -0.0576 |
| de | +0.6285 | +0.8380 | -0.0454 | -0.0101 |
| en | +0.7581 | +0.5711 | +0.0153 | +0.0987 |
| es | +0.6571 | +0.6119 | +0.0286 | +0.0331 |
| fil | +0.4022 | +0.5531 | +0.0090 | -0.0091 |
| fr | +0.5137 | +0.2294 | +0.0172 | +0.0852 |
| it | +0.5993 | +0.6551 | +0.0115 | -0.0652 |
| ja | +0.5002 | +0.6324 | +0.0951 | +0.1034 |
| pt | +0.7323 | +0.7274 | -0.0208 | -0.0467 |
| si | +0.1985 | +0.2193 | -0.0073 | +0.1349 |
