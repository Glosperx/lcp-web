# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-19 01:15:42 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4714 | [+0.3896, +0.5399] | 30 | 11 | +0.4163 | [+0.0097, +0.7197] | -0.0551 | [-0.4751, +0.2603] |
| de | 570 | 193 | +0.6230 | [+0.5685, +0.6757] | 23 | 11 | +0.8225 | [+0.5957, +0.9394] | +0.1995 | [-0.0345, +0.3359] |
| en | 570 | 190 | +0.8169 | [+0.7826, +0.8476] | 30 | 10 | +0.7265 | [+0.4265, +0.8731] | -0.0904 | [-0.4027, +0.0635] |
| es | 593 | 208 | +0.7069 | [+0.6658, +0.7425] | 30 | 10 | +0.7198 | [+0.4525, +0.8828] | +0.0128 | [-0.2511, +0.1800] |
| fil | 570 | 555 | +0.4099 | [+0.3395, +0.4769] | 30 | 30 | +0.5611 | [+0.2923, +0.7648] | +0.1512 | [-0.1278, +0.3704] |
| fr | 569 | 191 | +0.5508 | [+0.4889, +0.6092] | 30 | 11 | +0.3547 | [+0.0978, +0.5838] | -0.1961 | [-0.4584, +0.0455] |
| it | 570 | 192 | +0.6283 | [+0.5776, +0.6787] | 30 | 10 | +0.6965 | [+0.5048, +0.8330] | +0.0683 | [-0.1345, +0.2222] |
| ja | 570 | 190 | +0.5609 | [+0.4941, +0.6263] | 30 | 10 | +0.7087 | [+0.4717, +0.8541] | +0.1477 | [-0.0972, +0.3091] |
| pt | 567 | 562 | +0.7657 | [+0.7208, +0.8038] | 30 | 30 | +0.7454 | [+0.5585, +0.8769] | -0.0203 | [-0.2061, +0.1168] |
| si | 600 | 578 | +0.2172 | [+0.1486, +0.2851] | 30 | 30 | +0.1948 | [-0.0845, +0.4791] | -0.0224 | [-0.3167, +0.2762] |
| **medie** | | | **+0.5751** | | | | **+0.5946** | | **+0.0195** | |

**Δ split mediu +0.0195**, sd intre limbi 0.1230, interval -0.1961 pana la +0.1995. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4163 | +0.3909 | -0.0254 |
| de | +0.8225 | +0.8169 | -0.0056 |
| en | +0.7265 | +0.7274 | +0.0009 |
| es | +0.7198 | +0.7073 | -0.0125 |
| fil | +0.5611 | +0.5672 | +0.0061 |
| fr | +0.3547 | +0.3418 | -0.0129 |
| it | +0.6965 | +0.6946 | -0.0019 |
| ja | +0.7087 | +0.6603 | -0.0484 |
| pt | +0.7454 | +0.7545 | +0.0091 |
| si | +0.1948 | +0.2979 | +0.1031 |

**Diferenta medie +0.0012**, interval -0.0484 pana la +0.1031.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4563 | +0.4084 | +0.0151 | +0.0079 |
| de | +0.6647 | +0.8674 | -0.0417 | -0.0449 |
| en | +0.8019 | +0.6779 | +0.0150 | +0.0486 |
| es | +0.6981 | +0.7042 | +0.0088 | +0.0156 |
| fil | +0.4110 | +0.5740 | -0.0011 | -0.0129 |
| fr | +0.5399 | +0.2626 | +0.0109 | +0.0921 |
| it | +0.6330 | +0.7180 | -0.0047 | -0.0215 |
| ja | +0.5707 | +0.6054 | -0.0098 | +0.1033 |
| pt | +0.7752 | +0.7533 | -0.0095 | -0.0079 |
| si | +0.1787 | +0.2761 | +0.0385 | -0.0813 |
