# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:11:22 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4193 | [+0.3471, +0.4879] | 30 | 11 | +0.4558 | [-0.0013, +0.7873] | +0.0365 | [-0.4254, +0.3864] |
| de | 570 | 193 | +0.6066 | [+0.5564, +0.6555] | 23 | 11 | +0.7806 | [+0.5438, +0.9031] | +0.1740 | [-0.0687, +0.3118] |
| en | 570 | 190 | +0.8021 | [+0.7663, +0.8362] | 30 | 10 | +0.7184 | [+0.3935, +0.8742] | -0.0837 | [-0.4144, +0.0765] |
| es | 593 | 208 | +0.6898 | [+0.6478, +0.7282] | 30 | 10 | +0.7119 | [+0.4698, +0.8736] | +0.0221 | [-0.2208, +0.1904] |
| fil | 570 | 555 | +0.4016 | [+0.3345, +0.4669] | 30 | 30 | +0.5484 | [+0.2596, +0.8029] | +0.1468 | [-0.1474, +0.4081] |
| fr | 569 | 191 | +0.5633 | [+0.4975, +0.6219] | 30 | 11 | +0.3296 | [-0.0134, +0.5966] | -0.2337 | [-0.5772, +0.0474] |
| it | 570 | 192 | +0.6042 | [+0.5525, +0.6576] | 30 | 10 | +0.7164 | [+0.5453, +0.8412] | +0.1121 | [-0.0644, +0.2535] |
| ja | 570 | 190 | +0.4902 | [+0.4166, +0.5585] | 30 | 10 | +0.5723 | [+0.2745, +0.7880] | +0.0821 | [-0.2253, +0.3083] |
| pt | 567 | 562 | +0.7705 | [+0.7320, +0.8071] | 30 | 30 | +0.7895 | [+0.6168, +0.9194] | +0.0191 | [-0.1639, +0.1504] |
| si | 600 | 578 | +0.2054 | [+0.1385, +0.2684] | 30 | 30 | +0.2931 | [-0.0780, +0.5633] | +0.0877 | [-0.2701, +0.3586] |
| **medie** | | | **+0.5553** | | | | **+0.5916** | | **+0.0363** | |

**Δ split mediu +0.0363**, sd intre limbi 0.1199, interval -0.2337 pana la +0.1740. Trial-ul e mai mare pe 8 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4558 | +0.4100 | -0.0458 |
| de | +0.7806 | +0.7892 | +0.0086 |
| en | +0.7184 | +0.7286 | +0.0102 |
| es | +0.7119 | +0.7166 | +0.0047 |
| fil | +0.5484 | +0.5677 | +0.0193 |
| fr | +0.3296 | +0.3162 | -0.0134 |
| it | +0.7164 | +0.7248 | +0.0084 |
| ja | +0.5723 | +0.5686 | -0.0037 |
| pt | +0.7895 | +0.7946 | +0.0051 |
| si | +0.2931 | +0.3381 | +0.0450 |

**Diferenta medie +0.0038**, interval -0.0458 pana la +0.0450.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4222 | +0.4698 | -0.0029 | -0.0140 |
| de | +0.6316 | +0.8147 | -0.0250 | -0.0341 |
| en | +0.8046 | +0.7046 | -0.0025 | +0.0138 |
| es | +0.7057 | +0.6637 | -0.0159 | +0.0482 |
| fil | +0.4186 | +0.5536 | -0.0170 | -0.0052 |
| fr | +0.5298 | +0.2573 | +0.0335 | +0.0723 |
| it | +0.6211 | +0.7192 | -0.0169 | -0.0028 |
| ja | +0.5713 | +0.4977 | -0.0811 | +0.0746 |
| pt | +0.7783 | +0.7923 | -0.0078 | -0.0028 |
| si | +0.2118 | +0.1373 | -0.0064 | +0.1558 |
