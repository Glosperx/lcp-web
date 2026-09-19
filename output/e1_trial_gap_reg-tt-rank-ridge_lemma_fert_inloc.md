# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:42:47 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3280 | [+0.2344, +0.4236] | 30 | 11 | +0.1447 | [-0.2971, +0.5493] | -0.1833 | [-0.6390, +0.2307] |
| de | 570 | 193 | +0.5488 | [+0.4866, +0.6122] | 23 | 11 | +0.6678 | [+0.5049, +0.8491] | +0.1190 | [-0.0609, +0.3093] |
| en | 570 | 190 | +0.7302 | [+0.6798, +0.7806] | 30 | 10 | +0.6865 | [+0.3759, +0.8320] | -0.0437 | [-0.3543, +0.1078] |
| es | 593 | 208 | +0.5737 | [+0.4780, +0.6574] | 30 | 10 | +0.6282 | [+0.3625, +0.7763] | +0.0545 | [-0.2304, +0.2419] |
| fil | 570 | 555 | +0.3478 | [+0.2733, +0.4222] | 30 | 30 | +0.4808 | [+0.3305, +0.6830] | +0.1331 | [-0.0223, +0.3423] |
| fr | 569 | 191 | +0.4421 | [+0.3699, +0.5144] | 30 | 11 | +0.2967 | [-0.0987, +0.6464] | -0.1454 | [-0.5505, +0.2052] |
| it | 570 | 192 | +0.5749 | [+0.5167, +0.6375] | 30 | 10 | +0.5254 | [+0.3164, +0.7495] | -0.0496 | [-0.2645, +0.1862] |
| ja | 570 | 190 | +0.5977 | [+0.5451, +0.6481] | 30 | 10 | +0.5774 | [+0.3730, +0.7001] | -0.0204 | [-0.2299, +0.1114] |
| pt | 567 | 562 | +0.6980 | [+0.6478, +0.7412] | 30 | 30 | +0.7191 | [+0.5254, +0.8595] | +0.0210 | [-0.1743, +0.1666] |
| si | 600 | 578 | +0.1979 | [+0.1221, +0.2771] | 30 | 30 | +0.1171 | [-0.2007, +0.5450] | -0.0808 | [-0.4178, +0.3564] |
| **medie** | | | **+0.5039** | | | | **+0.4844** | | **-0.0196** | |

**Δ split mediu -0.0196**, sd intre limbi 0.1041, interval -0.1833 pana la +0.1331. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1447 | +0.1419 | -0.0028 |
| de | +0.6678 | +0.6519 | -0.0159 |
| en | +0.6865 | +0.6895 | +0.0030 |
| es | +0.6282 | +0.6227 | -0.0055 |
| fil | +0.4808 | +0.4824 | +0.0016 |
| fr | +0.2967 | +0.2908 | -0.0059 |
| it | +0.5254 | +0.5376 | +0.0122 |
| ja | +0.5774 | +0.5604 | -0.0170 |
| pt | +0.7191 | +0.7421 | +0.0230 |
| si | +0.1171 | +0.1442 | +0.0271 |

**Diferenta medie +0.0020**, interval -0.0170 pana la +0.0271.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3094 | +0.0981 | +0.0186 | +0.0466 |
| de | +0.5512 | +0.7152 | -0.0024 | -0.0474 |
| en | +0.7190 | +0.6342 | +0.0112 | +0.0523 |
| es | +0.5232 | +0.6076 | +0.0505 | +0.0206 |
| fil | +0.3737 | +0.4486 | -0.0259 | +0.0322 |
| fr | +0.4182 | +0.2714 | +0.0239 | +0.0253 |
| it | +0.5254 | +0.4476 | +0.0495 | +0.0778 |
| ja | +0.4550 | +0.4849 | +0.1427 | +0.0925 |
| pt | +0.6451 | +0.7289 | +0.0529 | -0.0098 |
| si | +0.2498 | +0.1615 | -0.0519 | -0.0444 |
