# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:02:46 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4526 | [+0.3650, +0.5312] | 30 | 11 | +0.3791 | [+0.0536, +0.6022] | -0.0735 | [-0.4025, +0.1658] |
| de | 570 | 193 | +0.5668 | [+0.5057, +0.6249] | 23 | 11 | +0.7836 | [+0.4675, +0.9159] | +0.2168 | [-0.1036, +0.3635] |
| en | 570 | 190 | +0.7676 | [+0.7275, +0.8031] | 30 | 10 | +0.6492 | [+0.5067, +0.7936] | -0.1184 | [-0.2657, +0.0379] |
| es | 593 | 208 | +0.6282 | [+0.5743, +0.6769] | 30 | 10 | +0.6454 | [+0.3706, +0.8214] | +0.0172 | [-0.2557, +0.2035] |
| fil | 570 | 555 | +0.3831 | [+0.3119, +0.4538] | 30 | 30 | +0.4804 | [+0.2084, +0.6908] | +0.0973 | [-0.1807, +0.3208] |
| fr | 569 | 191 | +0.5079 | [+0.4455, +0.5652] | 30 | 11 | +0.4632 | [+0.2502, +0.6704] | -0.0447 | [-0.2650, +0.1609] |
| it | 570 | 192 | +0.5954 | [+0.5400, +0.6516] | 30 | 10 | +0.6796 | [+0.4689, +0.8249] | +0.0841 | [-0.1283, +0.2481] |
| ja | 570 | 190 | +0.5534 | [+0.4801, +0.6207] | 30 | 10 | +0.6693 | [+0.3860, +0.8279] | +0.1159 | [-0.1775, +0.2912] |
| pt | 567 | 562 | +0.7157 | [+0.6736, +0.7535] | 30 | 30 | +0.6944 | [+0.4513, +0.8815] | -0.0212 | [-0.2619, +0.1657] |
| si | 600 | 578 | +0.3400 | [+0.2619, +0.4132] | 30 | 30 | +0.2835 | [-0.2018, +0.5790] | -0.0565 | [-0.5506, +0.2454] |
| **medie** | | | **+0.5511** | | | | **+0.5728** | | **+0.0217** | |

**Δ split mediu +0.0217**, sd intre limbi 0.1041, interval -0.1184 pana la +0.2168. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3791 | +0.3791 | +0.0000 |
| de | +0.7836 | +0.7836 | +0.0000 |
| en | +0.6492 | +0.6492 | +0.0000 |
| es | +0.6454 | +0.6454 | +0.0000 |
| fil | +0.4804 | +0.4804 | +0.0000 |
| fr | +0.4632 | +0.4632 | +0.0000 |
| it | +0.6796 | +0.6796 | +0.0000 |
| ja | +0.6693 | +0.6693 | +0.0000 |
| pt | +0.6944 | +0.6944 | +0.0000 |
| si | +0.2835 | +0.2835 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4046 | +0.3011 | +0.0480 | +0.0780 |
| de | +0.6138 | +0.8394 | -0.0470 | -0.0558 |
| en | +0.7553 | +0.6604 | +0.0123 | -0.0112 |
| es | +0.6305 | +0.5482 | -0.0023 | +0.0972 |
| fil | +0.3908 | +0.4752 | -0.0077 | +0.0052 |
| fr | +0.4422 | +0.2244 | +0.0657 | +0.2388 |
| it | +0.5987 | +0.6779 | -0.0033 | +0.0017 |
| ja | +0.5143 | +0.5167 | +0.0391 | +0.1526 |
| pt | +0.7209 | +0.7522 | -0.0052 | -0.0578 |
| si | +0.2597 | +0.2844 | +0.0803 | -0.0009 |
