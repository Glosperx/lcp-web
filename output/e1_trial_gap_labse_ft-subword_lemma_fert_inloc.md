# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:09:50 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4512 | [+0.3674, +0.5257] | 30 | 11 | +0.3740 | [-0.0489, +0.6852] | -0.0772 | [-0.5087, +0.2512] |
| de | 570 | 193 | +0.6326 | [+0.5808, +0.6823] | 23 | 11 | +0.8638 | [+0.6101, +0.9611] | +0.2311 | [-0.0260, +0.3487] |
| en | 570 | 190 | +0.8068 | [+0.7719, +0.8387] | 30 | 10 | +0.7034 | [+0.5449, +0.8280] | -0.1035 | [-0.2642, +0.0263] |
| es | 593 | 208 | +0.6676 | [+0.6215, +0.7089] | 30 | 10 | +0.7050 | [+0.4500, +0.8603] | +0.0374 | [-0.2092, +0.1977] |
| fil | 570 | 555 | +0.3498 | [+0.2739, +0.4178] | 30 | 30 | +0.5317 | [+0.2727, +0.7486] | +0.1820 | [-0.0837, +0.4149] |
| fr | 569 | 191 | +0.5499 | [+0.4895, +0.6068] | 30 | 11 | +0.4653 | [+0.1996, +0.6707] | -0.0846 | [-0.3609, +0.1318] |
| it | 570 | 192 | +0.6327 | [+0.5802, +0.6829] | 30 | 10 | +0.7006 | [+0.5335, +0.8289] | +0.0679 | [-0.1104, +0.2093] |
| ja | 570 | 190 | +0.5797 | [+0.5003, +0.6500] | 30 | 10 | +0.6277 | [+0.3291, +0.8095] | +0.0480 | [-0.2645, +0.2494] |
| pt | 567 | 562 | +0.7602 | [+0.7186, +0.7968] | 30 | 30 | +0.7429 | [+0.5525, +0.8913] | -0.0173 | [-0.2127, +0.1346] |
| si | 600 | 578 | +0.3056 | [+0.2409, +0.3670] | 30 | 30 | +0.0720 | [-0.2320, +0.3565] | -0.2336 | [-0.5432, +0.0588] |
| **medie** | | | **+0.5736** | | | | **+0.5786** | | **+0.0050** | |

**Δ split mediu +0.0050**, sd intre limbi 0.1388, interval -0.2336 pana la +0.2311. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3740 | +0.3484 | -0.0256 |
| de | +0.8638 | +0.8512 | -0.0126 |
| en | +0.7034 | +0.7023 | -0.0011 |
| es | +0.7050 | +0.6879 | -0.0171 |
| fil | +0.5317 | +0.5441 | +0.0124 |
| fr | +0.4653 | +0.4627 | -0.0026 |
| it | +0.7006 | +0.7069 | +0.0063 |
| ja | +0.6277 | +0.6221 | -0.0056 |
| pt | +0.7429 | +0.7436 | +0.0007 |
| si | +0.0720 | +0.0936 | +0.0216 |

**Diferenta medie -0.0024**, interval -0.0256 pana la +0.0216.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4313 | +0.4211 | +0.0199 | -0.0471 |
| de | +0.6567 | +0.8861 | -0.0241 | -0.0223 |
| en | +0.8055 | +0.7044 | +0.0013 | -0.0010 |
| es | +0.6848 | +0.6430 | -0.0172 | +0.0620 |
| fil | +0.3912 | +0.5631 | -0.0414 | -0.0314 |
| fr | +0.5107 | +0.3288 | +0.0392 | +0.1365 |
| it | +0.6289 | +0.7304 | +0.0038 | -0.0298 |
| ja | +0.5791 | +0.5001 | +0.0006 | +0.1276 |
| pt | +0.7636 | +0.7735 | -0.0034 | -0.0306 |
| si | +0.2859 | +0.0924 | +0.0197 | -0.0204 |
