# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:20:13 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3851 | [+0.2897, +0.4755] | 30 | 11 | +0.1503 | [-0.1968, +0.5770] | -0.2348 | [-0.6017, +0.2012] |
| de | 570 | 193 | +0.5913 | [+0.5281, +0.6499] | 23 | 11 | +0.6267 | [+0.3879, +0.8179] | +0.0353 | [-0.2122, +0.2402] |
| en | 570 | 190 | +0.7637 | [+0.7129, +0.8070] | 30 | 10 | +0.5943 | [+0.4295, +0.7820] | -0.1694 | [-0.3381, +0.0258] |
| es | 593 | 208 | +0.6152 | [+0.5656, +0.6627] | 30 | 10 | +0.7205 | [+0.4234, +0.8773] | +0.1053 | [-0.1802, +0.2718] |
| fil | 570 | 555 | +0.3562 | [+0.2827, +0.4211] | 30 | 30 | +0.4530 | [+0.1739, +0.6679] | +0.0968 | [-0.1975, +0.3315] |
| fr | 569 | 191 | +0.4368 | [+0.3619, +0.5049] | 30 | 11 | +0.1804 | [-0.1358, +0.5029] | -0.2564 | [-0.5882, +0.0721] |
| it | 570 | 192 | +0.5647 | [+0.5025, +0.6279] | 30 | 10 | +0.6113 | [+0.3214, +0.8193] | +0.0466 | [-0.2435, +0.2698] |
| ja | 570 | 190 | +0.5819 | [+0.5155, +0.6400] | 30 | 10 | +0.3372 | [+0.0437, +0.5285] | -0.2447 | [-0.5415, -0.0525] |
| pt | 567 | 562 | +0.6817 | [+0.6246, +0.7337] | 30 | 30 | +0.7533 | [+0.5624, +0.8884] | +0.0716 | [-0.1264, +0.2118] |
| si | 600 | 578 | +0.2152 | [+0.1498, +0.2839] | 30 | 30 | +0.0604 | [-0.3023, +0.4262] | -0.1547 | [-0.5236, +0.2077] |
| **medie** | | | **+0.5192** | | | | **+0.4487** | | **-0.0704** | |

**Δ split mediu -0.0704**, sd intre limbi 0.1538, interval -0.2564 pana la +0.1053. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1503 | +0.1503 | +0.0000 |
| de | +0.6267 | +0.6267 | +0.0000 |
| en | +0.5943 | +0.5943 | +0.0000 |
| es | +0.7205 | +0.7205 | +0.0000 |
| fil | +0.4530 | +0.4530 | +0.0000 |
| fr | +0.1804 | +0.1804 | +0.0000 |
| it | +0.6113 | +0.6113 | +0.0000 |
| ja | +0.3372 | +0.3372 | +0.0000 |
| pt | +0.7533 | +0.7533 | +0.0000 |
| si | +0.0604 | +0.0604 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3544 | +0.1480 | +0.0307 | +0.0023 |
| de | +0.6124 | +0.7048 | -0.0211 | -0.0781 |
| en | +0.7686 | +0.6166 | -0.0049 | -0.0223 |
| es | +0.6017 | +0.7251 | +0.0135 | -0.0046 |
| fil | +0.3675 | +0.4408 | -0.0113 | +0.0122 |
| fr | +0.4780 | +0.3106 | -0.0412 | -0.1302 |
| it | +0.5809 | +0.6560 | -0.0162 | -0.0447 |
| ja | +0.5422 | +0.3360 | +0.0397 | +0.0012 |
| pt | +0.7090 | +0.7506 | -0.0273 | +0.0027 |
| si | +0.2148 | +0.0777 | +0.0004 | -0.0173 |
