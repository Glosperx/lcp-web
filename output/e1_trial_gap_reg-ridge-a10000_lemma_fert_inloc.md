# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:32:32 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3955 | [+0.3038, +0.4826] | 30 | 11 | +0.1835 | [-0.1859, +0.5965] | -0.2120 | [-0.5987, +0.2029] |
| de | 570 | 193 | +0.6087 | [+0.5481, +0.6642] | 23 | 11 | +0.6519 | [+0.3967, +0.8391] | +0.0432 | [-0.2191, +0.2387] |
| en | 570 | 190 | +0.7748 | [+0.7274, +0.8144] | 30 | 10 | +0.6351 | [+0.4577, +0.8175] | -0.1397 | [-0.3222, +0.0475] |
| es | 593 | 208 | +0.6279 | [+0.5792, +0.6727] | 30 | 10 | +0.6953 | [+0.4022, +0.8592] | +0.0673 | [-0.2243, +0.2355] |
| fil | 570 | 555 | +0.3767 | [+0.3069, +0.4410] | 30 | 30 | +0.4369 | [+0.1407, +0.6617] | +0.0602 | [-0.2388, +0.3013] |
| fr | 569 | 191 | +0.4917 | [+0.4225, +0.5536] | 30 | 11 | +0.2750 | [-0.0714, +0.5983] | -0.2166 | [-0.5662, +0.1105] |
| it | 570 | 192 | +0.5832 | [+0.5240, +0.6439] | 30 | 10 | +0.6327 | [+0.3631, +0.8206] | +0.0495 | [-0.2162, +0.2507] |
| ja | 570 | 190 | +0.6021 | [+0.5386, +0.6609] | 30 | 10 | +0.4769 | [+0.2797, +0.6392] | -0.1252 | [-0.3352, +0.0425] |
| pt | 567 | 562 | +0.7080 | [+0.6583, +0.7537] | 30 | 30 | +0.7549 | [+0.5729, +0.8845] | +0.0469 | [-0.1389, +0.1860] |
| si | 600 | 578 | +0.2415 | [+0.1808, +0.3054] | 30 | 30 | +0.0739 | [-0.2644, +0.4027] | -0.1676 | [-0.5161, +0.1682] |
| **medie** | | | **+0.5410** | | | | **+0.4816** | | **-0.0594** | |

**Δ split mediu -0.0594**, sd intre limbi 0.1223, interval -0.2166 pana la +0.0673. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1835 | +0.1835 | +0.0000 |
| de | +0.6519 | +0.6519 | +0.0000 |
| en | +0.6351 | +0.6351 | +0.0000 |
| es | +0.6953 | +0.6953 | +0.0000 |
| fil | +0.4369 | +0.4369 | +0.0000 |
| fr | +0.2750 | +0.2750 | +0.0000 |
| it | +0.6327 | +0.6327 | +0.0000 |
| ja | +0.4769 | +0.4769 | +0.0000 |
| pt | +0.7549 | +0.7549 | +0.0000 |
| si | +0.0739 | +0.0739 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3730 | +0.1843 | +0.0225 | -0.0008 |
| de | +0.6247 | +0.7261 | -0.0160 | -0.0742 |
| en | +0.7740 | +0.6234 | +0.0008 | +0.0117 |
| es | +0.6174 | +0.7257 | +0.0105 | -0.0304 |
| fil | +0.3816 | +0.4271 | -0.0049 | +0.0098 |
| fr | +0.5058 | +0.3523 | -0.0141 | -0.0773 |
| it | +0.5905 | +0.6540 | -0.0073 | -0.0213 |
| ja | +0.5647 | +0.4304 | +0.0374 | +0.0465 |
| pt | +0.7185 | +0.7516 | -0.0105 | +0.0033 |
| si | +0.2461 | +0.1494 | -0.0046 | -0.0755 |
