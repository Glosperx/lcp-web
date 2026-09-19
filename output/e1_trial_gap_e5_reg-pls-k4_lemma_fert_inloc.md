# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:21:56 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3887 | [+0.2936, +0.4791] | 30 | 11 | +0.4704 | [+0.1765, +0.7120] | +0.0817 | [-0.2222, +0.3422] |
| de | 570 | 193 | +0.5228 | [+0.4571, +0.5848] | 23 | 11 | +0.7334 | [+0.5500, +0.8695] | +0.2106 | [+0.0211, +0.3611] |
| en | 570 | 190 | +0.7671 | [+0.7290, +0.8028] | 30 | 10 | +0.6453 | [+0.4372, +0.8360] | -0.1218 | [-0.3305, +0.0785] |
| es | 593 | 208 | +0.6852 | [+0.6361, +0.7270] | 30 | 10 | +0.7000 | [+0.3876, +0.8990] | +0.0148 | [-0.3044, +0.2267] |
| fil | 570 | 555 | +0.3881 | [+0.3190, +0.4540] | 30 | 30 | +0.4504 | [+0.1362, +0.6988] | +0.0624 | [-0.2563, +0.3152] |
| fr | 569 | 191 | +0.4755 | [+0.4108, +0.5409] | 30 | 11 | +0.3078 | [-0.0235, +0.5762] | -0.1678 | [-0.5082, +0.1076] |
| it | 570 | 192 | +0.5383 | [+0.4818, +0.5967] | 30 | 10 | +0.6299 | [+0.3491, +0.8295] | +0.0916 | [-0.1955, +0.3084] |
| ja | 570 | 190 | +0.4832 | [+0.4083, +0.5505] | 30 | 10 | +0.5714 | [+0.2936, +0.7489] | +0.0881 | [-0.1989, +0.2851] |
| pt | 567 | 562 | +0.6956 | [+0.6379, +0.7429] | 30 | 30 | +0.6660 | [+0.4496, +0.8267] | -0.0295 | [-0.2501, +0.1409] |
| si | 600 | 578 | +0.2336 | [+0.1706, +0.2951] | 30 | 30 | +0.2925 | [-0.0619, +0.5724] | +0.0588 | [-0.2973, +0.3397] |
| **medie** | | | **+0.5178** | | | | **+0.5467** | | **+0.0289** | |

**Δ split mediu +0.0289**, sd intre limbi 0.1107, interval -0.1678 pana la +0.2106. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4704 | +0.4704 | +0.0000 |
| de | +0.7334 | +0.7334 | +0.0000 |
| en | +0.6453 | +0.6453 | +0.0000 |
| es | +0.7000 | +0.7000 | +0.0000 |
| fil | +0.4504 | +0.4504 | +0.0000 |
| fr | +0.3078 | +0.3078 | +0.0000 |
| it | +0.6299 | +0.6299 | +0.0000 |
| ja | +0.5714 | +0.5714 | +0.0000 |
| pt | +0.6660 | +0.6660 | +0.0000 |
| si | +0.2925 | +0.2925 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3740 | +0.4689 | +0.0147 | +0.0015 |
| de | +0.5562 | +0.7615 | -0.0334 | -0.0281 |
| en | +0.7631 | +0.6025 | +0.0040 | +0.0428 |
| es | +0.6752 | +0.7109 | +0.0100 | -0.0109 |
| fil | +0.4029 | +0.4601 | -0.0148 | -0.0097 |
| fr | +0.4771 | +0.2518 | -0.0016 | +0.0560 |
| it | +0.5564 | +0.6281 | -0.0181 | +0.0018 |
| ja | +0.4399 | +0.4071 | +0.0433 | +0.1643 |
| pt | +0.7209 | +0.6922 | -0.0253 | -0.0262 |
| si | +0.2554 | +0.2958 | -0.0218 | -0.0033 |
