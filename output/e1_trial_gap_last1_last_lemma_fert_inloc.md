# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:24:18 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4055 | [+0.3265, +0.4791] | 30 | 11 | +0.2203 | [-0.3320, +0.6466] | -0.1852 | [-0.7375, +0.2543] |
| de | 570 | 193 | +0.6034 | [+0.5487, +0.6559] | 23 | 11 | +0.7429 | [+0.5144, +0.8688] | +0.1395 | [-0.0958, +0.2741] |
| en | 570 | 190 | +0.7943 | [+0.7527, +0.8293] | 30 | 10 | +0.6530 | [+0.4086, +0.8615] | -0.1413 | [-0.3917, +0.0652] |
| es | 593 | 208 | +0.6638 | [+0.6193, +0.7022] | 30 | 10 | +0.6388 | [+0.3272, +0.8479] | -0.0250 | [-0.3286, +0.1881] |
| fil | 570 | 555 | +0.3999 | [+0.3288, +0.4676] | 30 | 30 | +0.5533 | [+0.2819, +0.7756] | +0.1533 | [-0.1235, +0.3913] |
| fr | 569 | 191 | +0.5244 | [+0.4554, +0.5853] | 30 | 11 | +0.2436 | [-0.1594, +0.5738] | -0.2808 | [-0.6799, +0.0578] |
| it | 570 | 192 | +0.5996 | [+0.5430, +0.6535] | 30 | 10 | +0.7321 | [+0.5737, +0.8604] | +0.1325 | [-0.0373, +0.2741] |
| ja | 570 | 190 | +0.5329 | [+0.4596, +0.5960] | 30 | 10 | +0.4804 | [+0.2072, +0.6562] | -0.0525 | [-0.3233, +0.1301] |
| pt | 567 | 562 | +0.7374 | [+0.6981, +0.7750] | 30 | 30 | +0.7535 | [+0.5808, +0.8832] | +0.0161 | [-0.1602, +0.1516] |
| si | 600 | 578 | +0.1439 | [+0.0766, +0.2067] | 30 | 30 | +0.1241 | [-0.1995, +0.5187] | -0.0198 | [-0.3539, +0.3818] |
| **medie** | | | **+0.5405** | | | | **+0.5142** | | **-0.0263** | |

**Δ split mediu -0.0263**, sd intre limbi 0.1456, interval -0.2808 pana la +0.1533. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2203 | +0.2277 | +0.0074 |
| de | +0.7429 | +0.7344 | -0.0085 |
| en | +0.6530 | +0.6418 | -0.0112 |
| es | +0.6388 | +0.6329 | -0.0059 |
| fil | +0.5533 | +0.5851 | +0.0318 |
| fr | +0.2436 | +0.2436 | +0.0000 |
| it | +0.7321 | +0.7302 | -0.0019 |
| ja | +0.4804 | +0.5003 | +0.0199 |
| pt | +0.7535 | +0.7470 | -0.0065 |
| si | +0.1241 | +0.1203 | -0.0038 |

**Diferenta medie +0.0021**, interval -0.0112 pana la +0.0318.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3565 | +0.2700 | +0.0490 | -0.0497 |
| de | +0.6479 | +0.8182 | -0.0445 | -0.0753 |
| en | +0.7979 | +0.6800 | -0.0036 | -0.0270 |
| es | +0.6291 | +0.6420 | +0.0347 | -0.0032 |
| fil | +0.4009 | +0.5998 | -0.0010 | -0.0465 |
| fr | +0.5285 | +0.2822 | -0.0041 | -0.0386 |
| it | +0.6160 | +0.7105 | -0.0164 | +0.0216 |
| ja | +0.5717 | +0.5100 | -0.0388 | -0.0296 |
| pt | +0.7471 | +0.7424 | -0.0097 | +0.0111 |
| si | +0.1498 | +0.1142 | -0.0059 | +0.0099 |
