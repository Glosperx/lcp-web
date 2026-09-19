# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 13:54:18 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4280 | [+0.3483, +0.5015] | 30 | 11 | +0.2855 | [-0.2770, +0.7166] | -0.1425 | [-0.7107, +0.3061] |
| de | 570 | 193 | +0.6505 | [+0.5982, +0.6991] | 23 | 11 | +0.7799 | [+0.5827, +0.8776] | +0.1294 | [-0.0776, +0.2441] |
| en | 570 | 190 | +0.8249 | [+0.7884, +0.8550] | 30 | 10 | +0.7095 | [+0.4336, +0.8460] | -0.1154 | [-0.3869, +0.0300] |
| es | 593 | 208 | +0.6774 | [+0.6326, +0.7168] | 30 | 10 | +0.7101 | [+0.4228, +0.8842] | +0.0328 | [-0.2564, +0.2110] |
| fil | 570 | 555 | +0.4178 | [+0.3468, +0.4834] | 30 | 30 | +0.6071 | [+0.3874, +0.7777] | +0.1893 | [-0.0389, +0.3764] |
| fr | 569 | 191 | +0.5313 | [+0.4628, +0.5944] | 30 | 11 | +0.3562 | [-0.0310, +0.6532] | -0.1751 | [-0.5770, +0.1401] |
| it | 570 | 192 | +0.6245 | [+0.5690, +0.6774] | 30 | 10 | +0.6475 | [+0.4109, +0.8150] | +0.0231 | [-0.2196, +0.2080] |
| ja | 570 | 190 | +0.6062 | [+0.5482, +0.6584] | 30 | 10 | +0.5763 | [+0.3476, +0.7149] | -0.0299 | [-0.2652, +0.1228] |
| pt | 567 | 562 | +0.7724 | [+0.7336, +0.8076] | 30 | 30 | +0.8080 | [+0.6528, +0.9155] | +0.0356 | [-0.1285, +0.1465] |
| si | 600 | 578 | +0.2158 | [+0.1530, +0.2835] | 30 | 30 | -0.0541 | [-0.4311, +0.3877] | -0.2699 | [-0.6472, +0.1718] |
| **medie** | | | **+0.5749** | | | | **+0.5426** | | **-0.0323** | |

**Δ split mediu -0.0323**, sd intre limbi 0.1426, interval -0.2699 pana la +0.1893. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2855 | +0.2181 | -0.0674 |
| de | +0.7799 | +0.7938 | +0.0139 |
| en | +0.7095 | +0.7093 | -0.0002 |
| es | +0.7101 | +0.7020 | -0.0081 |
| fil | +0.6071 | +0.6274 | +0.0203 |
| fr | +0.3562 | +0.3238 | -0.0324 |
| it | +0.6475 | +0.6422 | -0.0053 |
| ja | +0.5763 | +0.5496 | -0.0267 |
| pt | +0.8080 | +0.8060 | -0.0020 |
| si | -0.0541 | -0.0012 | +0.0529 |

**Diferenta medie -0.0055**, interval -0.0674 pana la +0.0529.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3971 | +0.2062 | +0.0309 | +0.0793 |
| de | +0.6743 | +0.8378 | -0.0238 | -0.0579 |
| en | +0.8178 | +0.6556 | +0.0071 | +0.0539 |
| es | +0.6592 | +0.6757 | +0.0182 | +0.0344 |
| fil | +0.4056 | +0.5842 | +0.0122 | +0.0229 |
| fr | +0.5209 | +0.3623 | +0.0104 | -0.0061 |
| it | +0.6204 | +0.6662 | +0.0041 | -0.0187 |
| ja | +0.6085 | +0.4806 | -0.0023 | +0.0957 |
| pt | +0.7740 | +0.8095 | -0.0016 | -0.0015 |
| si | +0.2063 | -0.0232 | +0.0095 | -0.0309 |
