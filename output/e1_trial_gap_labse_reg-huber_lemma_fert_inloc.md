# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:03:58 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4501 | [+0.3641, +0.5275] | 30 | 11 | +0.3657 | [+0.0272, +0.5908] | -0.0844 | [-0.4234, +0.1617] |
| de | 570 | 193 | +0.5683 | [+0.5041, +0.6277] | 23 | 11 | +0.8027 | [+0.5439, +0.9178] | +0.2344 | [-0.0368, +0.3696] |
| en | 570 | 190 | +0.7700 | [+0.7305, +0.8054] | 30 | 10 | +0.6620 | [+0.5097, +0.7862] | -0.1080 | [-0.2682, +0.0266] |
| es | 593 | 208 | +0.6463 | [+0.5986, +0.6908] | 30 | 10 | +0.6697 | [+0.4012, +0.8431] | +0.0235 | [-0.2429, +0.2078] |
| fil | 570 | 555 | +0.3873 | [+0.3157, +0.4577] | 30 | 30 | +0.4987 | [+0.2257, +0.7016] | +0.1114 | [-0.1612, +0.3244] |
| fr | 569 | 191 | +0.4956 | [+0.4312, +0.5532] | 30 | 11 | +0.4623 | [+0.2431, +0.6653] | -0.0334 | [-0.2578, +0.1786] |
| it | 570 | 192 | +0.6056 | [+0.5522, +0.6573] | 30 | 10 | +0.6662 | [+0.4669, +0.8124] | +0.0606 | [-0.1470, +0.2202] |
| ja | 570 | 190 | +0.5504 | [+0.4756, +0.6182] | 30 | 10 | +0.6471 | [+0.3376, +0.8247] | +0.0967 | [-0.2256, +0.2861] |
| pt | 567 | 562 | +0.7315 | [+0.6915, +0.7679] | 30 | 30 | +0.7051 | [+0.4554, +0.8894] | -0.0263 | [-0.2729, +0.1608] |
| si | 600 | 578 | +0.3293 | [+0.2501, +0.4004] | 30 | 30 | +0.3259 | [-0.1675, +0.6076] | -0.0035 | [-0.5009, +0.2899] |
| **medie** | | | **+0.5534** | | | | **+0.5805** | | **+0.0271** | |

**Δ split mediu +0.0271**, sd intre limbi 0.1023, interval -0.1080 pana la +0.2344. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3657 | +0.3657 | +0.0000 |
| de | +0.8027 | +0.8027 | +0.0000 |
| en | +0.6620 | +0.6620 | +0.0000 |
| es | +0.6697 | +0.6697 | +0.0000 |
| fil | +0.4987 | +0.4987 | +0.0000 |
| fr | +0.4623 | +0.4623 | +0.0000 |
| it | +0.6662 | +0.6662 | +0.0000 |
| ja | +0.6471 | +0.6471 | +0.0000 |
| pt | +0.7051 | +0.7051 | +0.0000 |
| si | +0.3259 | +0.3259 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4107 | +0.2424 | +0.0394 | +0.1233 |
| de | +0.6130 | +0.8382 | -0.0447 | -0.0355 |
| en | +0.7537 | +0.6585 | +0.0163 | +0.0035 |
| es | +0.6218 | +0.5687 | +0.0245 | +0.1010 |
| fil | +0.3977 | +0.4642 | -0.0104 | +0.0345 |
| fr | +0.4350 | +0.2748 | +0.0606 | +0.1875 |
| it | +0.5931 | +0.6626 | +0.0125 | +0.0036 |
| ja | +0.4962 | +0.4955 | +0.0542 | +0.1516 |
| pt | +0.7175 | +0.7493 | +0.0140 | -0.0442 |
| si | +0.2505 | +0.2575 | +0.0788 | +0.0684 |
