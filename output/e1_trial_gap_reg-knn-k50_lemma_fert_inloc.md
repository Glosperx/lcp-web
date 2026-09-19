# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:41:16 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.2842 | [+0.1896, +0.3792] | 30 | 11 | -0.0746 | [-0.4447, +0.3004] | -0.3588 | [-0.7486, +0.0301] |
| de | 570 | 193 | +0.2921 | [+0.2205, +0.3648] | 23 | 11 | -0.0715 | [-0.5609, +0.4913] | -0.3636 | [-0.8599, +0.2000] |
| en | 570 | 190 | +0.5075 | [+0.4238, +0.5862] | 30 | 10 | +0.3707 | [+0.0086, +0.6492] | -0.1367 | [-0.4996, +0.1400] |
| es | 593 | 208 | +0.3646 | [+0.2973, +0.4300] | 30 | 10 | +0.2466 | [-0.2122, +0.5627] | -0.1180 | [-0.5625, +0.2079] |
| fil | 570 | 555 | +0.0984 | [+0.0193, +0.1795] | 30 | 30 | +0.3764 | [+0.0065, +0.6634] | +0.2780 | [-0.0903, +0.5823] |
| fr | 569 | 191 | +0.3242 | [+0.2504, +0.3949] | 30 | 11 | +0.3285 | [-0.0436, +0.6095] | +0.0042 | [-0.3795, +0.2952] |
| it | 570 | 192 | +0.3241 | [+0.2530, +0.3915] | 30 | 10 | +0.2904 | [-0.0868, +0.6834] | -0.0337 | [-0.4246, +0.3641] |
| ja | 570 | 190 | +0.3001 | [+0.2250, +0.3748] | 30 | 10 | +0.0042 | [-0.4218, +0.4202] | -0.2960 | [-0.7327, +0.1108] |
| pt | 567 | 562 | +0.4693 | [+0.4069, +0.5304] | 30 | 30 | +0.5054 | [+0.2413, +0.7086] | +0.0362 | [-0.2369, +0.2462] |
| si | 600 | 578 | +0.2014 | [+0.1288, +0.2723] | 30 | 30 | -0.1268 | [-0.4789, +0.3210] | -0.3281 | [-0.6853, +0.1253] |
| **medie** | | | **+0.3166** | | | | **+0.1849** | | **-0.1316** | |

**Δ split mediu -0.1316**, sd intre limbi 0.2096, interval -0.3636 pana la +0.2780. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | -0.0746 | -0.0550 | +0.0196 |
| de | -0.0715 | -0.1155 | -0.0440 |
| en | +0.3707 | +0.4793 | +0.1086 |
| es | +0.2466 | +0.3287 | +0.0821 |
| fil | +0.3764 | +0.3589 | -0.0175 |
| fr | +0.3285 | +0.2707 | -0.0578 |
| it | +0.2904 | +0.3407 | +0.0503 |
| ja | +0.0042 | +0.0038 | -0.0004 |
| pt | +0.5054 | +0.4388 | -0.0666 |
| si | -0.1268 | -0.0091 | +0.1177 |

**Diferenta medie +0.0192**, interval -0.0666 pana la +0.1177.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.2926 | +0.1167 | -0.0084 | -0.1913 |
| de | +0.4639 | +0.3818 | -0.1718 | -0.4533 |
| en | +0.6405 | +0.5434 | -0.1330 | -0.1727 |
| es | +0.4572 | +0.5119 | -0.0926 | -0.2653 |
| fil | +0.2014 | +0.0347 | -0.1030 | +0.3417 |
| fr | +0.4170 | +0.4539 | -0.0928 | -0.1254 |
| it | +0.4710 | +0.5747 | -0.1469 | -0.2843 |
| ja | +0.4784 | +0.1702 | -0.1783 | -0.1660 |
| pt | +0.5698 | +0.7462 | -0.1005 | -0.2408 |
| si | +0.1258 | +0.1163 | +0.0756 | -0.2431 |
