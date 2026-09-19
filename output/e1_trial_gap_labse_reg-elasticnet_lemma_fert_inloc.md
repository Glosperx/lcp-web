# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:58:51 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4061 | [+0.3135, +0.4858] | 30 | 11 | +0.4202 | [+0.0251, +0.7202] | +0.0141 | [-0.4023, +0.3271] |
| de | 570 | 193 | +0.5974 | [+0.5452, +0.6468] | 23 | 11 | +0.8222 | [+0.5619, +0.9532] | +0.2248 | [-0.0481, +0.3680] |
| en | 570 | 190 | +0.7668 | [+0.7309, +0.8009] | 30 | 10 | +0.6213 | [+0.5221, +0.7602] | -0.1455 | [-0.2515, +0.0021] |
| es | 593 | 208 | +0.6431 | [+0.5935, +0.6861] | 30 | 10 | +0.6120 | [+0.3871, +0.7745] | -0.0311 | [-0.2709, +0.1436] |
| fil | 570 | 555 | +0.3949 | [+0.3230, +0.4642] | 30 | 30 | +0.5381 | [+0.2939, +0.7302] | +0.1432 | [-0.1118, +0.3395] |
| fr | 569 | 191 | +0.5550 | [+0.4955, +0.6107] | 30 | 11 | +0.4483 | [+0.1185, +0.6944] | -0.1067 | [-0.4460, +0.1475] |
| it | 570 | 192 | +0.6077 | [+0.5541, +0.6590] | 30 | 10 | +0.6421 | [+0.4658, +0.7961] | +0.0344 | [-0.1427, +0.2037] |
| ja | 570 | 190 | +0.5763 | [+0.5060, +0.6402] | 30 | 10 | +0.6001 | [+0.2403, +0.8386] | +0.0238 | [-0.3384, +0.2710] |
| pt | 567 | 562 | +0.7529 | [+0.7152, +0.7871] | 30 | 30 | +0.7233 | [+0.5402, +0.8853] | -0.0296 | [-0.2177, +0.1345] |
| si | 600 | 578 | +0.3247 | [+0.2429, +0.3990] | 30 | 30 | +0.4168 | [+0.1430, +0.6576] | +0.0921 | [-0.1829, +0.3491] |
| **medie** | | | **+0.5625** | | | | **+0.5844** | | **+0.0220** | |

**Δ split mediu +0.0220**, sd intre limbi 0.1111, interval -0.1455 pana la +0.2248. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4202 | +0.4202 | +0.0000 |
| de | +0.8222 | +0.8222 | +0.0000 |
| en | +0.6213 | +0.6213 | +0.0000 |
| es | +0.6120 | +0.6120 | +0.0000 |
| fil | +0.5381 | +0.5381 | +0.0000 |
| fr | +0.4483 | +0.4483 | +0.0000 |
| it | +0.6421 | +0.6421 | +0.0000 |
| ja | +0.6001 | +0.6001 | +0.0000 |
| pt | +0.7233 | +0.7233 | +0.0000 |
| si | +0.4168 | +0.4168 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3657 | +0.3270 | +0.0404 | +0.0932 |
| de | +0.6396 | +0.8473 | -0.0422 | -0.0251 |
| en | +0.7600 | +0.6193 | +0.0068 | +0.0020 |
| es | +0.6362 | +0.5749 | +0.0069 | +0.0371 |
| fil | +0.3844 | +0.5505 | +0.0105 | -0.0124 |
| fr | +0.5292 | +0.3174 | +0.0258 | +0.1309 |
| it | +0.6125 | +0.6212 | -0.0048 | +0.0209 |
| ja | +0.5415 | +0.5135 | +0.0348 | +0.0866 |
| pt | +0.7573 | +0.7365 | -0.0044 | -0.0132 |
| si | +0.1668 | +0.1501 | +0.1579 | +0.2667 |
