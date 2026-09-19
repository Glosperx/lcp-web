# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:21:30 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3978 | [+0.3147, +0.4729] | 30 | 11 | +0.3261 | [-0.1325, +0.6505] | -0.0717 | [-0.5403, +0.2609] |
| de | 570 | 193 | +0.6421 | [+0.5896, +0.6918] | 23 | 11 | +0.7392 | [+0.4893, +0.8406] | +0.0971 | [-0.1637, +0.2145] |
| en | 570 | 190 | +0.8145 | [+0.7788, +0.8436] | 30 | 10 | +0.7037 | [+0.5422, +0.8566] | -0.1109 | [-0.2762, +0.0453] |
| es | 593 | 208 | +0.6807 | [+0.6380, +0.7213] | 30 | 10 | +0.6707 | [+0.3651, +0.8513] | -0.0100 | [-0.3096, +0.1741] |
| fil | 570 | 555 | +0.4082 | [+0.3349, +0.4766] | 30 | 30 | +0.5928 | [+0.3842, +0.7752] | +0.1845 | [-0.0274, +0.3793] |
| fr | 569 | 191 | +0.5694 | [+0.5076, +0.6254] | 30 | 11 | +0.3903 | [+0.0400, +0.6709] | -0.1791 | [-0.5377, +0.1040] |
| it | 570 | 192 | +0.6197 | [+0.5665, +0.6706] | 30 | 10 | +0.6502 | [+0.4458, +0.8081] | +0.0305 | [-0.1798, +0.2019] |
| ja | 570 | 190 | +0.5528 | [+0.4842, +0.6139] | 30 | 10 | +0.4936 | [+0.2759, +0.6421] | -0.0592 | [-0.2933, +0.0946] |
| pt | 567 | 562 | +0.7648 | [+0.7238, +0.8025] | 30 | 30 | +0.8169 | [+0.6762, +0.9116] | +0.0521 | [-0.0950, +0.1538] |
| si | 600 | 578 | +0.2676 | [+0.1939, +0.3406] | 30 | 30 | -0.0372 | [-0.4042, +0.3723] | -0.3048 | [-0.6829, +0.1166] |
| **medie** | | | **+0.5718** | | | | **+0.5346** | | **-0.0372** | |

**Δ split mediu -0.0372**, sd intre limbi 0.1412, interval -0.3048 pana la +0.1845. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3261 | +0.2825 | -0.0436 |
| de | +0.7392 | +0.7419 | +0.0027 |
| en | +0.7037 | +0.6984 | -0.0053 |
| es | +0.6707 | +0.6528 | -0.0179 |
| fil | +0.5928 | +0.5923 | -0.0005 |
| fr | +0.3903 | +0.3747 | -0.0156 |
| it | +0.6502 | +0.6476 | -0.0026 |
| ja | +0.4936 | +0.4849 | -0.0087 |
| pt | +0.8169 | +0.8104 | -0.0065 |
| si | -0.0372 | +0.0315 | +0.0687 |

**Diferenta medie -0.0029**, interval -0.0436 pana la +0.0687.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3659 | +0.2913 | +0.0319 | +0.0348 |
| de | +0.6541 | +0.7933 | -0.0120 | -0.0541 |
| en | +0.8055 | +0.6391 | +0.0090 | +0.0646 |
| es | +0.6534 | +0.6247 | +0.0273 | +0.0460 |
| fil | +0.3946 | +0.4596 | +0.0136 | +0.1332 |
| fr | +0.5416 | +0.3986 | +0.0278 | -0.0083 |
| it | +0.6326 | +0.6400 | -0.0129 | +0.0102 |
| ja | +0.5460 | +0.4350 | +0.0068 | +0.0586 |
| pt | +0.7533 | +0.8056 | +0.0115 | +0.0113 |
| si | +0.2112 | +0.0443 | +0.0564 | -0.0815 |
