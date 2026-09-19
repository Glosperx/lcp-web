# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:53:11 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4251 | [+0.3484, +0.4929] | 30 | 11 | +0.4248 | [-0.0181, +0.7515] | -0.0003 | [-0.4544, +0.3380] |
| de | 570 | 193 | +0.6077 | [+0.5570, +0.6579] | 23 | 11 | +0.7498 | [+0.4748, +0.9019] | +0.1421 | [-0.1413, +0.3072] |
| en | 570 | 190 | +0.8113 | [+0.7746, +0.8430] | 30 | 10 | +0.7128 | [+0.3896, +0.8533] | -0.0985 | [-0.4287, +0.0503] |
| es | 593 | 208 | +0.6776 | [+0.6337, +0.7170] | 30 | 10 | +0.7410 | [+0.5321, +0.8735] | +0.0634 | [-0.1436, +0.2044] |
| fil | 570 | 555 | +0.3975 | [+0.3289, +0.4648] | 30 | 30 | +0.5466 | [+0.2421, +0.8024] | +0.1491 | [-0.1642, +0.4146] |
| fr | 569 | 191 | +0.5367 | [+0.4707, +0.5965] | 30 | 11 | +0.3493 | [+0.0189, +0.6153] | -0.1874 | [-0.5217, +0.0815] |
| it | 570 | 192 | +0.6098 | [+0.5582, +0.6610] | 30 | 10 | +0.7490 | [+0.6029, +0.8490] | +0.1392 | [-0.0216, +0.2550] |
| ja | 570 | 190 | +0.3587 | [+0.2811, +0.4330] | 30 | 10 | +0.4588 | [+0.0266, +0.7467] | +0.1002 | [-0.3309, +0.3953] |
| pt | 567 | 562 | +0.7683 | [+0.7276, +0.8050] | 30 | 30 | +0.7631 | [+0.5871, +0.8916] | -0.0051 | [-0.1786, +0.1250] |
| si | 600 | 578 | +0.1793 | [+0.1071, +0.2482] | 30 | 30 | -0.0859 | [-0.3780, +0.1888] | -0.2652 | [-0.5736, +0.0159] |
| **medie** | | | **+0.5372** | | | | **+0.5409** | | **+0.0038** | |

**Δ split mediu +0.0038**, sd intre limbi 0.1456, interval -0.2652 pana la +0.1491. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4248 | +0.3414 | -0.0834 |
| de | +0.7498 | +0.7264 | -0.0234 |
| en | +0.7128 | +0.7279 | +0.0151 |
| es | +0.7410 | +0.7219 | -0.0191 |
| fil | +0.5466 | +0.5686 | +0.0220 |
| fr | +0.3493 | +0.3266 | -0.0227 |
| it | +0.7490 | +0.7459 | -0.0031 |
| ja | +0.4588 | +0.2532 | -0.2056 |
| pt | +0.7631 | +0.7818 | +0.0187 |
| si | -0.0859 | +0.1282 | +0.2141 |

**Diferenta medie -0.0087**, interval -0.2056 pana la +0.2141.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4397 | +0.3284 | -0.0146 | +0.0964 |
| de | +0.6424 | +0.8520 | -0.0347 | -0.1022 |
| en | +0.7994 | +0.7013 | +0.0119 | +0.0115 |
| es | +0.6840 | +0.7364 | -0.0064 | +0.0046 |
| fil | +0.4013 | +0.5722 | -0.0038 | -0.0256 |
| fr | +0.5292 | +0.2809 | +0.0075 | +0.0684 |
| it | +0.6192 | +0.7454 | -0.0094 | +0.0036 |
| ja | +0.5680 | +0.5337 | -0.2093 | -0.0749 |
| pt | +0.7742 | +0.7563 | -0.0059 | +0.0068 |
| si | +0.1138 | +0.2270 | +0.0655 | -0.3129 |
