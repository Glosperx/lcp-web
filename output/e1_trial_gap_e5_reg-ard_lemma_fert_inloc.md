# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:43:30 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3295 | [+0.2353, +0.4122] | 30 | 11 | +0.3603 | [-0.0290, +0.6446] | +0.0309 | [-0.3708, +0.3329] |
| de | 570 | 193 | +0.5846 | [+0.5291, +0.6389] | 23 | 11 | +0.7960 | [+0.5223, +0.9306] | +0.2115 | [-0.0708, +0.3575] |
| en | 570 | 190 | +0.7424 | [+0.7012, +0.7787] | 30 | 10 | +0.6077 | [+0.4658, +0.7363] | -0.1347 | [-0.2817, +0.0039] |
| es | 593 | 208 | +0.6151 | [+0.5674, +0.6611] | 30 | 10 | +0.5948 | [+0.2748, +0.8375] | -0.0203 | [-0.3404, +0.2309] |
| fil | 570 | 555 | +0.3818 | [+0.3099, +0.4516] | 30 | 30 | +0.6043 | [+0.4278, +0.7802] | +0.2225 | [+0.0314, +0.4158] |
| fr | 569 | 191 | +0.5564 | [+0.4986, +0.6107] | 30 | 11 | +0.3870 | [+0.0364, +0.6433] | -0.1693 | [-0.5267, +0.0871] |
| it | 570 | 192 | +0.5857 | [+0.5261, +0.6377] | 30 | 10 | +0.6149 | [+0.4594, +0.7740] | +0.0292 | [-0.1358, +0.2018] |
| ja | 570 | 190 | +0.5552 | [+0.4819, +0.6264] | 30 | 10 | +0.6063 | [+0.2928, +0.8374] | +0.0512 | [-0.2775, +0.2902] |
| pt | 567 | 562 | +0.7238 | [+0.6855, +0.7599] | 30 | 30 | +0.7236 | [+0.5099, +0.8818] | -0.0002 | [-0.2128, +0.1627] |
| si | 600 | 578 | +0.1799 | [+0.1182, +0.2368] | 30 | 30 | +0.0386 | [-0.3615, +0.4537] | -0.1414 | [-0.5419, +0.2766] |
| **medie** | | | **+0.5254** | | | | **+0.5334** | | **+0.0079** | |

**Δ split mediu +0.0079**, sd intre limbi 0.1355, interval -0.1693 pana la +0.2225. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3603 | +0.3603 | +0.0000 |
| de | +0.7960 | +0.7960 | +0.0000 |
| en | +0.6077 | +0.6077 | +0.0000 |
| es | +0.5948 | +0.5948 | +0.0000 |
| fil | +0.6043 | +0.6043 | +0.0000 |
| fr | +0.3870 | +0.3870 | +0.0000 |
| it | +0.6149 | +0.6149 | +0.0000 |
| ja | +0.6063 | +0.6063 | +0.0000 |
| pt | +0.7236 | +0.7236 | +0.0000 |
| si | +0.0386 | +0.0386 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3432 | +0.3111 | -0.0137 | +0.0492 |
| de | +0.6278 | +0.8598 | -0.0432 | -0.0638 |
| en | +0.7395 | +0.6229 | +0.0029 | -0.0152 |
| es | +0.6114 | +0.6086 | +0.0037 | -0.0138 |
| fil | +0.3795 | +0.5967 | +0.0023 | +0.0076 |
| fr | +0.5750 | +0.4209 | -0.0186 | -0.0339 |
| it | +0.6039 | +0.6121 | -0.0182 | +0.0028 |
| ja | +0.5435 | +0.5852 | +0.0117 | +0.0211 |
| pt | +0.7272 | +0.7257 | -0.0034 | -0.0021 |
| si | +0.0337 | -0.1489 | +0.1462 | +0.1875 |
