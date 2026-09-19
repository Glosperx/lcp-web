# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 12:00:15 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4740 | [+0.3906, +0.5438] | 30 | 11 | +0.4310 | [+0.0449, +0.7230] | -0.0430 | [-0.4443, +0.2558] |
| de | 570 | 193 | +0.6204 | [+0.5655, +0.6745] | 23 | 11 | +0.8423 | [+0.6469, +0.9477] | +0.2218 | [+0.0186, +0.3464] |
| en | 570 | 190 | +0.8162 | [+0.7812, +0.8477] | 30 | 10 | +0.7137 | [+0.4160, +0.8715] | -0.1025 | [-0.4121, +0.0612] |
| es | 593 | 208 | +0.7038 | [+0.6624, +0.7398] | 30 | 10 | +0.7300 | [+0.4567, +0.8922] | +0.0262 | [-0.2402, +0.1922] |
| fil | 570 | 555 | +0.4080 | [+0.3364, +0.4759] | 30 | 30 | +0.5657 | [+0.2906, +0.7727] | +0.1576 | [-0.1253, +0.3795] |
| fr | 569 | 191 | +0.5543 | [+0.4927, +0.6138] | 30 | 11 | +0.3580 | [+0.0921, +0.5829] | -0.1963 | [-0.4638, +0.0392] |
| it | 570 | 192 | +0.6314 | [+0.5818, +0.6819] | 30 | 10 | +0.6901 | [+0.4951, +0.8308] | +0.0588 | [-0.1432, +0.2153] |
| ja | 570 | 190 | +0.5698 | [+0.5043, +0.6334] | 30 | 10 | +0.7043 | [+0.4417, +0.8615] | +0.1345 | [-0.1362, +0.3046] |
| pt | 567 | 562 | +0.7646 | [+0.7197, +0.8029] | 30 | 30 | +0.7406 | [+0.5538, +0.8706] | -0.0240 | [-0.2117, +0.1135] |
| si | 600 | 578 | +0.2259 | [+0.1583, +0.2950] | 30 | 30 | +0.2301 | [-0.0614, +0.5181] | +0.0042 | [-0.2967, +0.3037] |
| **medie** | | | **+0.5768** | | | | **+0.6006** | | **+0.0237** | |

**Δ split mediu +0.0237**, sd intre limbi 0.1257, interval -0.1963 pana la +0.2218. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4310 | +0.3972 | -0.0338 |
| de | +0.8423 | +0.8359 | -0.0064 |
| en | +0.7137 | +0.7177 | +0.0040 |
| es | +0.7300 | +0.7114 | -0.0186 |
| fil | +0.5657 | +0.5760 | +0.0103 |
| fr | +0.3580 | +0.3496 | -0.0084 |
| it | +0.6901 | +0.6972 | +0.0071 |
| ja | +0.7043 | +0.6704 | -0.0339 |
| pt | +0.7406 | +0.7501 | +0.0095 |
| si | +0.2301 | +0.3063 | +0.0762 |

**Diferenta medie +0.0006**, interval -0.0339 pana la +0.0762.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4619 | +0.4074 | +0.0121 | +0.0236 |
| de | +0.6604 | +0.8625 | -0.0400 | -0.0202 |
| en | +0.8027 | +0.6647 | +0.0135 | +0.0490 |
| es | +0.6961 | +0.6919 | +0.0077 | +0.0381 |
| fil | +0.4100 | +0.5730 | -0.0020 | -0.0073 |
| fr | +0.5406 | +0.2462 | +0.0137 | +0.1118 |
| it | +0.6294 | +0.7119 | +0.0020 | -0.0218 |
| ja | +0.5894 | +0.6452 | -0.0196 | +0.0591 |
| pt | +0.7726 | +0.7525 | -0.0080 | -0.0119 |
| si | +0.2011 | +0.2382 | +0.0248 | -0.0081 |
