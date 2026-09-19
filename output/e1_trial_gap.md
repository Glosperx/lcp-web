# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-18 10:13:16 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

Poarta de reproducere a trecut: `r_test_multi` reproduce `r_multi` din `output/e1_lolo_frozen.csv` pe toate limbile, deci e acelasi brat, nu unul refacut.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4281 | [+0.3425, +0.5055] | 30 | 11 | +0.2585 | [-0.2813, +0.6773] | -0.1696 | [-0.7131, +0.2517] |
| de | 570 | 193 | +0.6314 | [+0.5746, +0.6847] | 23 | 11 | +0.7959 | [+0.5087, +0.9239] | +0.1645 | [-0.1328, +0.3068] |
| en | 570 | 190 | +0.8197 | [+0.7831, +0.8502] | 30 | 10 | +0.7070 | [+0.4705, +0.8541] | -0.1127 | [-0.3502, +0.0414] |
| es | 593 | 208 | +0.6341 | [+0.5848, +0.6777] | 28 | 10 | +0.7708 | [+0.5840, +0.8920] | +0.1367 | [-0.0583, +0.2599] |
| fil | 568 | 553 | +0.4047 | [+0.3347, +0.4729] | 30 | 30 | +0.5893 | [+0.3472, +0.7681] | +0.1845 | [-0.0706, +0.3786] |
| fr | 566 | 191 | +0.5153 | [+0.4499, +0.5764] | 30 | 11 | +0.2981 | [-0.1246, +0.6396] | -0.2172 | [-0.6424, +0.1308] |
| it | 562 | 192 | +0.6136 | [+0.5587, +0.6674] | 29 | 10 | +0.6813 | [+0.4441, +0.8380] | +0.0677 | [-0.1773, +0.2405] |
| ja | 570 | 190 | +0.4880 | [+0.4162, +0.5501] | 30 | 10 | +0.3581 | [+0.0497, +0.6009] | -0.1299 | [-0.4464, +0.1262] |
| pt | 562 | 557 | +0.7663 | [+0.7246, +0.8029] | 30 | 30 | +0.8034 | [+0.6615, +0.9145] | +0.0371 | [-0.1103, +0.1553] |
| si | 600 | 578 | +0.2216 | [+0.1575, +0.2923] | 30 | 30 | -0.0463 | [-0.4041, +0.3480] | -0.2680 | [-0.6350, +0.1316] |
| **medie** | | | **+0.5523** | | | | **+0.5216** | | **-0.0307** | |

**Δ split mediu -0.0307**, sd intre limbi 0.1679, interval -0.2680 pana la +0.1845. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2585 | +0.2576 | -0.0009 |
| de | +0.7959 | +0.7931 | -0.0028 |
| en | +0.7070 | +0.6953 | -0.0117 |
| es | +0.7708 | +0.7727 | +0.0019 |
| fil | +0.5893 | +0.5817 | -0.0076 |
| fr | +0.2981 | +0.2903 | -0.0078 |
| it | +0.6813 | +0.6800 | -0.0013 |
| ja | +0.3581 | +0.3536 | -0.0045 |
| pt | +0.8034 | +0.8105 | +0.0071 |
| si | -0.0463 | -0.0563 | -0.0100 |

**Diferenta medie -0.0038**, interval -0.0117 pana la +0.0071.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3932 | +0.1829 | +0.0349 | +0.0756 |
| de | +0.6359 | +0.8377 | -0.0045 | -0.0418 |
| en | +0.8221 | +0.6805 | -0.0024 | +0.0265 |
| es | +0.5981 | +0.7549 | +0.0360 | +0.0159 |
| fil | +0.4158 | +0.5479 | -0.0111 | +0.0414 |
| fr | +0.5145 | +0.3960 | +0.0008 | -0.0979 |
| it | +0.5850 | +0.6948 | +0.0286 | -0.0135 |
| ja | +0.5776 | +0.4300 | -0.0896 | -0.0719 |
| pt | +0.7748 | +0.8065 | -0.0085 | -0.0031 |
| si | +0.2507 | -0.0011 | -0.0291 | -0.0452 |
