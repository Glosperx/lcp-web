# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:52:04 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4564 | [+0.3706, +0.5360] | 30 | 11 | +0.4592 | [+0.2241, +0.7010] | +0.0028 | [-0.2566, +0.2575] |
| de | 570 | 193 | +0.5303 | [+0.4661, +0.5855] | 23 | 11 | +0.7502 | [+0.4582, +0.8927] | +0.2199 | [-0.0578, +0.3809] |
| en | 570 | 190 | +0.7931 | [+0.7565, +0.8267] | 30 | 10 | +0.6994 | [+0.5848, +0.8604] | -0.0938 | [-0.2166, +0.0752] |
| es | 593 | 208 | +0.6344 | [+0.5873, +0.6771] | 30 | 10 | +0.6793 | [+0.4594, +0.8154] | +0.0449 | [-0.1809, +0.1863] |
| fil | 570 | 555 | +0.3878 | [+0.3173, +0.4577] | 30 | 30 | +0.4412 | [+0.2004, +0.6637] | +0.0534 | [-0.2025, +0.2783] |
| fr | 569 | 191 | +0.5241 | [+0.4634, +0.5845] | 30 | 11 | +0.5863 | [+0.3581, +0.7543] | +0.0622 | [-0.1716, +0.2394] |
| it | 570 | 192 | +0.5489 | [+0.4888, +0.6081] | 30 | 10 | +0.7117 | [+0.5387, +0.8295] | +0.1628 | [-0.0177, +0.3017] |
| ja | 570 | 190 | +0.5288 | [+0.4557, +0.5960] | 30 | 10 | +0.6062 | [+0.2928, +0.7952] | +0.0774 | [-0.2429, +0.2782] |
| pt | 567 | 562 | +0.7315 | [+0.6902, +0.7679] | 30 | 30 | +0.7102 | [+0.4901, +0.9070] | -0.0212 | [-0.2395, +0.1712] |
| si | 600 | 578 | +0.3607 | [+0.2853, +0.4291] | 30 | 30 | +0.3381 | [-0.1192, +0.6010] | -0.0226 | [-0.4711, +0.2581] |
| **medie** | | | **+0.5496** | | | | **+0.5982** | | **+0.0486** | |

**Δ split mediu +0.0486**, sd intre limbi 0.0917, interval -0.0938 pana la +0.2199. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4592 | +0.4616 | +0.0024 |
| de | +0.7502 | +0.7330 | -0.0172 |
| en | +0.6994 | +0.6928 | -0.0066 |
| es | +0.6793 | +0.6993 | +0.0200 |
| fil | +0.4412 | +0.4584 | +0.0172 |
| fr | +0.5863 | +0.5920 | +0.0057 |
| it | +0.7117 | +0.7229 | +0.0112 |
| ja | +0.6062 | +0.5666 | -0.0396 |
| pt | +0.7102 | +0.7059 | -0.0043 |
| si | +0.3381 | +0.3713 | +0.0332 |

**Diferenta medie +0.0022**, interval -0.0396 pana la +0.0332.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4251 | +0.4731 | +0.0313 | -0.0139 |
| de | +0.5203 | +0.7553 | +0.0100 | -0.0051 |
| en | +0.7956 | +0.6980 | -0.0025 | +0.0014 |
| es | +0.6519 | +0.6576 | -0.0175 | +0.0217 |
| fil | +0.4480 | +0.4912 | -0.0602 | -0.0500 |
| fr | +0.4836 | +0.4800 | +0.0405 | +0.1063 |
| it | +0.5248 | +0.6679 | +0.0241 | +0.0438 |
| ja | +0.5077 | +0.4983 | +0.0211 | +0.1079 |
| pt | +0.7069 | +0.7175 | +0.0246 | -0.0073 |
| si | +0.3447 | +0.3910 | +0.0160 | -0.0529 |
