# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:36:35 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3711 | [+0.2805, +0.4511] | 30 | 11 | +0.4815 | [+0.0628, +0.7526] | +0.1104 | [-0.3245, +0.3968] |
| de | 570 | 193 | +0.5870 | [+0.5311, +0.6428] | 23 | 11 | +0.7990 | [+0.5027, +0.9405] | +0.2120 | [-0.0868, +0.3669] |
| en | 570 | 190 | +0.7516 | [+0.7120, +0.7876] | 30 | 10 | +0.6011 | [+0.4967, +0.7413] | -0.1505 | [-0.2600, -0.0055] |
| es | 593 | 208 | +0.6491 | [+0.6047, +0.6893] | 30 | 10 | +0.6316 | [+0.3262, +0.8268] | -0.0175 | [-0.3321, +0.1805] |
| fil | 570 | 555 | +0.3909 | [+0.3200, +0.4601] | 30 | 30 | +0.5958 | [+0.4120, +0.7662] | +0.2049 | [+0.0151, +0.3924] |
| fr | 569 | 191 | +0.5677 | [+0.5099, +0.6221] | 30 | 11 | +0.3591 | [-0.0077, +0.6195] | -0.2087 | [-0.5776, +0.0628] |
| it | 570 | 192 | +0.6046 | [+0.5479, +0.6546] | 30 | 10 | +0.6583 | [+0.4977, +0.7997] | +0.0537 | [-0.1160, +0.2079] |
| ja | 570 | 190 | +0.5644 | [+0.4909, +0.6339] | 30 | 10 | +0.6162 | [+0.2801, +0.8534] | +0.0518 | [-0.2966, +0.3008] |
| pt | 567 | 562 | +0.7307 | [+0.6903, +0.7667] | 30 | 30 | +0.7088 | [+0.5041, +0.8656] | -0.0219 | [-0.2259, +0.1404] |
| si | 600 | 578 | +0.1246 | [+0.0569, +0.1907] | 30 | 30 | +0.0402 | [-0.3301, +0.4772] | -0.0844 | [-0.4679, +0.3565] |
| **medie** | | | **+0.5342** | | | | **+0.5492** | | **+0.0150** | |

**Δ split mediu +0.0150**, sd intre limbi 0.1401, interval -0.2087 pana la +0.2120. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4815 | +0.4815 | +0.0000 |
| de | +0.7990 | +0.7990 | +0.0000 |
| en | +0.6011 | +0.6011 | +0.0000 |
| es | +0.6316 | +0.6316 | +0.0000 |
| fil | +0.5958 | +0.5958 | +0.0000 |
| fr | +0.3591 | +0.3591 | +0.0000 |
| it | +0.6583 | +0.6583 | +0.0000 |
| ja | +0.6162 | +0.6162 | +0.0000 |
| pt | +0.7088 | +0.7088 | +0.0000 |
| si | +0.0402 | +0.0402 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3469 | +0.3333 | +0.0242 | +0.1482 |
| de | +0.6401 | +0.8277 | -0.0531 | -0.0287 |
| en | +0.7433 | +0.6154 | +0.0083 | -0.0143 |
| es | +0.6218 | +0.5877 | +0.0273 | +0.0439 |
| fil | +0.3846 | +0.5795 | +0.0063 | +0.0163 |
| fr | +0.5436 | +0.2950 | +0.0241 | +0.0641 |
| it | +0.6167 | +0.6400 | -0.0121 | +0.0183 |
| ja | +0.5353 | +0.5750 | +0.0291 | +0.0412 |
| pt | +0.7462 | +0.7326 | -0.0155 | -0.0238 |
| si | +0.0774 | -0.0785 | +0.0472 | +0.1187 |
