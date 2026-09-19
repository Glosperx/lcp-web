# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:26:52 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3973 | [+0.3093, +0.4788] | 30 | 11 | +0.1374 | [-0.3328, +0.5145] | -0.2599 | [-0.7323, +0.1365] |
| de | 570 | 193 | +0.5946 | [+0.5340, +0.6515] | 23 | 11 | +0.7789 | [+0.5488, +0.8855] | +0.1843 | [-0.0551, +0.3081] |
| en | 570 | 190 | +0.7632 | [+0.7173, +0.8012] | 30 | 10 | +0.6146 | [+0.3745, +0.7566] | -0.1486 | [-0.3841, +0.0040] |
| es | 593 | 208 | +0.6207 | [+0.5685, +0.6667] | 30 | 10 | +0.5636 | [+0.1993, +0.7784] | -0.0571 | [-0.4179, +0.1681] |
| fil | 570 | 555 | +0.3851 | [+0.3142, +0.4552] | 30 | 30 | +0.6059 | [+0.4005, +0.7606] | +0.2208 | [+0.0033, +0.3961] |
| fr | 569 | 191 | +0.4961 | [+0.4337, +0.5558] | 30 | 11 | +0.2402 | [-0.2124, +0.6244] | -0.2559 | [-0.7133, +0.1339] |
| it | 570 | 192 | +0.6049 | [+0.5511, +0.6576] | 30 | 10 | +0.5868 | [+0.3666, +0.7979] | -0.0181 | [-0.2461, +0.2036] |
| ja | 570 | 190 | +0.5923 | [+0.5319, +0.6488] | 30 | 10 | +0.5322 | [+0.3650, +0.6268] | -0.0602 | [-0.2369, +0.0543] |
| pt | 567 | 562 | +0.7395 | [+0.6927, +0.7796] | 30 | 30 | +0.7774 | [+0.6049, +0.9059] | +0.0378 | [-0.1417, +0.1716] |
| si | 600 | 578 | +0.2658 | [+0.2067, +0.3268] | 30 | 30 | +0.0166 | [-0.3453, +0.4660] | -0.2492 | [-0.6153, +0.2086] |
| **medie** | | | **+0.5459** | | | | **+0.4854** | | **-0.0606** | |

**Δ split mediu -0.0606**, sd intre limbi 0.1738, interval -0.2599 pana la +0.2208. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1374 | +0.1374 | +0.0000 |
| de | +0.7789 | +0.7789 | +0.0000 |
| en | +0.6146 | +0.6146 | +0.0000 |
| es | +0.5636 | +0.5636 | +0.0000 |
| fil | +0.6059 | +0.6059 | +0.0000 |
| fr | +0.2402 | +0.2402 | +0.0000 |
| it | +0.5868 | +0.5868 | +0.0000 |
| ja | +0.5322 | +0.5322 | +0.0000 |
| pt | +0.7774 | +0.7774 | +0.0000 |
| si | +0.0166 | +0.0166 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3513 | +0.1049 | +0.0460 | +0.0325 |
| de | +0.6156 | +0.8139 | -0.0210 | -0.0350 |
| en | +0.7433 | +0.5864 | +0.0199 | +0.0282 |
| es | +0.5750 | +0.6091 | +0.0457 | -0.0455 |
| fil | +0.3939 | +0.5043 | -0.0088 | +0.1016 |
| fr | +0.4694 | +0.2022 | +0.0267 | +0.0380 |
| it | +0.5629 | +0.5790 | +0.0420 | +0.0078 |
| ja | +0.5016 | +0.3168 | +0.0907 | +0.2154 |
| pt | +0.7261 | +0.7710 | +0.0134 | +0.0064 |
| si | +0.2426 | +0.0174 | +0.0232 | -0.0008 |
