# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:34:07 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4508 | [+0.3651, +0.5293] | 30 | 11 | +0.3411 | [+0.0283, +0.6475] | -0.1097 | [-0.4285, +0.2173] |
| de | 570 | 193 | +0.5462 | [+0.4834, +0.6009] | 23 | 11 | +0.7830 | [+0.5070, +0.9159] | +0.2368 | [-0.0459, +0.3920] |
| en | 570 | 190 | +0.7724 | [+0.7341, +0.8080] | 30 | 10 | +0.6511 | [+0.5455, +0.8336] | -0.1213 | [-0.2338, +0.0728] |
| es | 593 | 208 | +0.6330 | [+0.5824, +0.6778] | 30 | 10 | +0.6693 | [+0.5023, +0.8038] | +0.0363 | [-0.1348, +0.1794] |
| fil | 570 | 555 | +0.3987 | [+0.3250, +0.4656] | 30 | 30 | +0.4065 | [+0.1298, +0.6306] | +0.0079 | [-0.2793, +0.2473] |
| fr | 569 | 191 | +0.5374 | [+0.4754, +0.5983] | 30 | 11 | +0.5260 | [+0.2756, +0.7154] | -0.0114 | [-0.2675, +0.1898] |
| it | 570 | 192 | +0.5389 | [+0.4804, +0.5962] | 30 | 10 | +0.6834 | [+0.4750, +0.8240] | +0.1445 | [-0.0684, +0.3065] |
| ja | 570 | 190 | +0.5407 | [+0.4667, +0.6082] | 30 | 10 | +0.6225 | [+0.3805, +0.7787] | +0.0818 | [-0.1863, +0.2582] |
| pt | 567 | 562 | +0.7014 | [+0.6574, +0.7402] | 30 | 30 | +0.6787 | [+0.4695, +0.8724] | -0.0227 | [-0.2356, +0.1706] |
| si | 600 | 578 | +0.3435 | [+0.2713, +0.4151] | 30 | 30 | +0.3623 | [-0.1089, +0.6209] | +0.0188 | [-0.4556, +0.2969] |
| **medie** | | | **+0.5463** | | | | **+0.5724** | | **+0.0261** | |

**Δ split mediu +0.0261**, sd intre limbi 0.1085, interval -0.1213 pana la +0.2368. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3411 | +0.3411 | +0.0000 |
| de | +0.7830 | +0.7830 | +0.0000 |
| en | +0.6511 | +0.6511 | +0.0000 |
| es | +0.6693 | +0.6693 | +0.0000 |
| fil | +0.4065 | +0.4065 | +0.0000 |
| fr | +0.5260 | +0.5260 | +0.0000 |
| it | +0.6834 | +0.6834 | +0.0000 |
| ja | +0.6225 | +0.6225 | +0.0000 |
| pt | +0.6787 | +0.6787 | +0.0000 |
| si | +0.3623 | +0.3623 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4371 | +0.4325 | +0.0137 | -0.0914 |
| de | +0.5915 | +0.8145 | -0.0453 | -0.0315 |
| en | +0.7791 | +0.6497 | -0.0067 | +0.0014 |
| es | +0.6368 | +0.6018 | -0.0038 | +0.0675 |
| fil | +0.4204 | +0.4379 | -0.0217 | -0.0314 |
| fr | +0.5068 | +0.5025 | +0.0306 | +0.0235 |
| it | +0.5394 | +0.6816 | -0.0005 | +0.0018 |
| ja | +0.5371 | +0.5631 | +0.0036 | +0.0594 |
| pt | +0.7043 | +0.6942 | -0.0029 | -0.0155 |
| si | +0.3094 | +0.3324 | +0.0341 | +0.0299 |
