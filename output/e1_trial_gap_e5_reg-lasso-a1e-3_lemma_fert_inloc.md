# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:38:59 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4451 | [+0.3515, +0.5263] | 30 | 11 | +0.4334 | [+0.0488, +0.7022] | -0.0117 | [-0.4070, +0.2687] |
| de | 570 | 193 | +0.6150 | [+0.5579, +0.6691] | 23 | 11 | +0.8410 | [+0.6636, +0.9375] | +0.2260 | [+0.0419, +0.3375] |
| en | 570 | 190 | +0.7982 | [+0.7608, +0.8316] | 30 | 10 | +0.6969 | [+0.4675, +0.8523] | -0.1014 | [-0.3386, +0.0580] |
| es | 593 | 208 | +0.7071 | [+0.6635, +0.7436] | 30 | 10 | +0.6836 | [+0.3862, +0.8642] | -0.0236 | [-0.3171, +0.1675] |
| fil | 570 | 555 | +0.3972 | [+0.3257, +0.4650] | 30 | 30 | +0.5379 | [+0.2737, +0.7309] | +0.1408 | [-0.1158, +0.3493] |
| fr | 569 | 191 | +0.5532 | [+0.4928, +0.6104] | 30 | 11 | +0.3420 | [+0.0841, +0.5747] | -0.2113 | [-0.4773, +0.0340] |
| it | 570 | 192 | +0.6372 | [+0.5850, +0.6881] | 30 | 10 | +0.6791 | [+0.4728, +0.8312] | +0.0419 | [-0.1689, +0.2096] |
| ja | 570 | 190 | +0.5936 | [+0.5216, +0.6605] | 30 | 10 | +0.6617 | [+0.3871, +0.8646] | +0.0681 | [-0.2117, +0.2862] |
| pt | 567 | 562 | +0.7543 | [+0.7077, +0.7940] | 30 | 30 | +0.7198 | [+0.5174, +0.8712] | -0.0345 | [-0.2366, +0.1210] |
| si | 600 | 578 | +0.2581 | [+0.1968, +0.3173] | 30 | 30 | +0.3822 | [+0.0714, +0.6397] | +0.1241 | [-0.1962, +0.3982] |
| **medie** | | | **+0.5759** | | | | **+0.5978** | | **+0.0218** | |

**Δ split mediu +0.0218**, sd intre limbi 0.1268, interval -0.2113 pana la +0.2260. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4334 | +0.4334 | +0.0000 |
| de | +0.8410 | +0.8410 | +0.0000 |
| en | +0.6969 | +0.6969 | +0.0000 |
| es | +0.6836 | +0.6836 | +0.0000 |
| fil | +0.5379 | +0.5379 | +0.0000 |
| fr | +0.3420 | +0.3420 | +0.0000 |
| it | +0.6791 | +0.6791 | +0.0000 |
| ja | +0.6617 | +0.6617 | +0.0000 |
| pt | +0.7198 | +0.7198 | +0.0000 |
| si | +0.3822 | +0.3822 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4104 | +0.4527 | +0.0347 | -0.0193 |
| de | +0.6559 | +0.8348 | -0.0409 | +0.0062 |
| en | +0.7790 | +0.6411 | +0.0192 | +0.0558 |
| es | +0.6923 | +0.6415 | +0.0148 | +0.0421 |
| fil | +0.3965 | +0.5530 | +0.0007 | -0.0151 |
| fr | +0.5318 | +0.3259 | +0.0214 | +0.0161 |
| it | +0.6362 | +0.6703 | +0.0010 | +0.0088 |
| ja | +0.5226 | +0.5632 | +0.0710 | +0.0985 |
| pt | +0.7600 | +0.6996 | -0.0057 | +0.0202 |
| si | +0.1961 | +0.2935 | +0.0620 | +0.0887 |
