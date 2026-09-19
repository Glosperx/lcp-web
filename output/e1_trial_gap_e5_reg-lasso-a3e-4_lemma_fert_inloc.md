# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:21:31 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4434 | [+0.3461, +0.5290] | 30 | 11 | +0.3992 | [+0.0353, +0.6615] | -0.0443 | [-0.4339, +0.2314] |
| de | 570 | 193 | +0.6043 | [+0.5454, +0.6589] | 23 | 11 | +0.8462 | [+0.6546, +0.9386] | +0.2419 | [+0.0403, +0.3545] |
| en | 570 | 190 | +0.7909 | [+0.7533, +0.8260] | 30 | 10 | +0.6895 | [+0.4587, +0.8599] | -0.1015 | [-0.3400, +0.0706] |
| es | 593 | 208 | +0.6999 | [+0.6551, +0.7376] | 30 | 10 | +0.6649 | [+0.3139, +0.8772] | -0.0350 | [-0.3779, +0.1873] |
| fil | 570 | 555 | +0.4002 | [+0.3284, +0.4681] | 30 | 30 | +0.5382 | [+0.2621, +0.7384] | +0.1380 | [-0.1378, +0.3539] |
| fr | 569 | 191 | +0.5430 | [+0.4824, +0.6028] | 30 | 11 | +0.3197 | [+0.0975, +0.5361] | -0.2234 | [-0.4490, +0.0088] |
| it | 570 | 192 | +0.6264 | [+0.5747, +0.6779] | 30 | 10 | +0.6345 | [+0.3946, +0.8114] | +0.0081 | [-0.2416, +0.1954] |
| ja | 570 | 190 | +0.5995 | [+0.5326, +0.6622] | 30 | 10 | +0.7147 | [+0.5075, +0.8604] | +0.1152 | [-0.1081, +0.2791] |
| pt | 567 | 562 | +0.7411 | [+0.6935, +0.7822] | 30 | 30 | +0.7070 | [+0.4953, +0.8595] | -0.0341 | [-0.2491, +0.1246] |
| si | 600 | 578 | +0.2214 | [+0.1560, +0.2892] | 30 | 30 | +0.3916 | [+0.1616, +0.6128] | +0.1702 | [-0.0664, +0.4088] |
| **medie** | | | **+0.5670** | | | | **+0.5906** | | **+0.0235** | |

**Δ split mediu +0.0235**, sd intre limbi 0.1410, interval -0.2234 pana la +0.2419. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3992 | +0.3992 | +0.0000 |
| de | +0.8462 | +0.8462 | +0.0000 |
| en | +0.6895 | +0.6895 | +0.0000 |
| es | +0.6649 | +0.6649 | +0.0000 |
| fil | +0.5382 | +0.5382 | +0.0000 |
| fr | +0.3197 | +0.3197 | +0.0000 |
| it | +0.6345 | +0.6345 | +0.0000 |
| ja | +0.7147 | +0.7147 | +0.0000 |
| pt | +0.7070 | +0.7070 | +0.0000 |
| si | +0.3916 | +0.3916 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4216 | +0.4602 | +0.0218 | -0.0610 |
| de | +0.6507 | +0.8388 | -0.0464 | +0.0074 |
| en | +0.7760 | +0.6159 | +0.0149 | +0.0736 |
| es | +0.6807 | +0.6508 | +0.0192 | +0.0141 |
| fil | +0.3987 | +0.5381 | +0.0015 | +0.0001 |
| fr | +0.5244 | +0.2804 | +0.0186 | +0.0393 |
| it | +0.6242 | +0.6597 | +0.0022 | -0.0252 |
| ja | +0.5212 | +0.6190 | +0.0783 | +0.0957 |
| pt | +0.7542 | +0.7179 | -0.0131 | -0.0109 |
| si | +0.1916 | +0.3123 | +0.0298 | +0.0793 |
