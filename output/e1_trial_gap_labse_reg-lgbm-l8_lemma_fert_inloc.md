# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:41:50 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3726 | [+0.2940, +0.4467] | 30 | 11 | +0.3362 | [-0.0580, +0.6588] | -0.0364 | [-0.4424, +0.2985] |
| de | 570 | 193 | +0.5993 | [+0.5492, +0.6468] | 23 | 11 | +0.7672 | [+0.5303, +0.8852] | +0.1679 | [-0.0831, +0.3027] |
| en | 570 | 190 | +0.8063 | [+0.7697, +0.8382] | 30 | 10 | +0.7006 | [+0.5219, +0.8481] | -0.1057 | [-0.2867, +0.0483] |
| es | 593 | 208 | +0.6596 | [+0.6163, +0.7006] | 30 | 10 | +0.6753 | [+0.4245, +0.8387] | +0.0157 | [-0.2456, +0.1860] |
| fil | 570 | 555 | +0.3934 | [+0.3195, +0.4589] | 30 | 30 | +0.5428 | [+0.2681, +0.7787] | +0.1494 | [-0.1208, +0.4010] |
| fr | 569 | 191 | +0.5327 | [+0.4652, +0.5950] | 30 | 11 | +0.4684 | [+0.1334, +0.6885] | -0.0643 | [-0.4078, +0.1633] |
| it | 570 | 192 | +0.6025 | [+0.5514, +0.6564] | 30 | 10 | +0.7516 | [+0.6190, +0.8548] | +0.1491 | [+0.0004, +0.2654] |
| ja | 570 | 190 | +0.4448 | [+0.3710, +0.5134] | 30 | 10 | +0.5323 | [+0.1947, +0.7545] | +0.0875 | [-0.2538, +0.3170] |
| pt | 567 | 562 | +0.7666 | [+0.7283, +0.8029] | 30 | 30 | +0.7477 | [+0.5685, +0.8856] | -0.0189 | [-0.2005, +0.1255] |
| si | 600 | 578 | +0.2527 | [+0.1837, +0.3167] | 30 | 30 | +0.0680 | [-0.2068, +0.3853] | -0.1847 | [-0.4715, +0.1390] |
| **medie** | | | **+0.5430** | | | | **+0.5590** | | **+0.0160** | |

**Δ split mediu +0.0160**, sd intre limbi 0.1198, interval -0.1847 pana la +0.1679. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3362 | +0.2325 | -0.1037 |
| de | +0.7672 | +0.7291 | -0.0381 |
| en | +0.7006 | +0.7451 | +0.0445 |
| es | +0.6753 | +0.6530 | -0.0223 |
| fil | +0.5428 | +0.5957 | +0.0529 |
| fr | +0.4684 | +0.3901 | -0.0783 |
| it | +0.7516 | +0.7437 | -0.0079 |
| ja | +0.5323 | +0.3734 | -0.1589 |
| pt | +0.7477 | +0.7476 | -0.0001 |
| si | +0.0680 | +0.2114 | +0.1434 |

**Diferenta medie -0.0168**, interval -0.1589 pana la +0.1434.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3941 | +0.3759 | -0.0215 | -0.0397 |
| de | +0.6335 | +0.8673 | -0.0342 | -0.1001 |
| en | +0.8045 | +0.6627 | +0.0018 | +0.0379 |
| es | +0.6631 | +0.6453 | -0.0035 | +0.0300 |
| fil | +0.3939 | +0.5950 | -0.0005 | -0.0522 |
| fr | +0.5098 | +0.2950 | +0.0229 | +0.1734 |
| it | +0.6224 | +0.7418 | -0.0199 | +0.0098 |
| ja | +0.5695 | +0.4395 | -0.1247 | +0.0928 |
| pt | +0.7528 | +0.7782 | +0.0138 | -0.0305 |
| si | +0.1135 | +0.1144 | +0.1392 | -0.0464 |
