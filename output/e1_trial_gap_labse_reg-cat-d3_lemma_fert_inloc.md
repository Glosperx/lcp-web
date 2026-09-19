# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:39:21 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3882 | [+0.3092, +0.4631] | 30 | 11 | +0.3822 | [-0.0554, +0.7207] | -0.0061 | [-0.4514, +0.3394] |
| de | 570 | 193 | +0.6040 | [+0.5538, +0.6509] | 23 | 11 | +0.8040 | [+0.5498, +0.9266] | +0.2000 | [-0.0682, +0.3386] |
| en | 570 | 190 | +0.8025 | [+0.7665, +0.8344] | 30 | 10 | +0.7200 | [+0.5894, +0.8554] | -0.0824 | [-0.2159, +0.0602] |
| es | 593 | 208 | +0.6594 | [+0.6164, +0.6992] | 30 | 10 | +0.6083 | [+0.3555, +0.7991] | -0.0512 | [-0.3107, +0.1469] |
| fil | 570 | 555 | +0.3834 | [+0.3094, +0.4503] | 30 | 30 | +0.5514 | [+0.2807, +0.7819] | +0.1680 | [-0.1046, +0.4126] |
| fr | 569 | 191 | +0.5437 | [+0.4803, +0.6031] | 30 | 11 | +0.4318 | [+0.1169, +0.6672] | -0.1119 | [-0.4411, +0.1326] |
| it | 570 | 192 | +0.5974 | [+0.5463, +0.6511] | 30 | 10 | +0.7297 | [+0.5684, +0.8424] | +0.1322 | [-0.0420, +0.2615] |
| ja | 570 | 190 | +0.5011 | [+0.4359, +0.5639] | 30 | 10 | +0.4679 | [+0.0725, +0.7486] | -0.0332 | [-0.4327, +0.2525] |
| pt | 567 | 562 | +0.7636 | [+0.7258, +0.8002] | 30 | 30 | +0.7417 | [+0.5519, +0.8988] | -0.0219 | [-0.2124, +0.1367] |
| si | 600 | 578 | +0.3195 | [+0.2434, +0.3853] | 30 | 30 | +0.0986 | [-0.1779, +0.3986] | -0.2209 | [-0.5117, +0.0852] |
| **medie** | | | **+0.5563** | | | | **+0.5536** | | **-0.0027** | |

**Δ split mediu -0.0027**, sd intre limbi 0.1325, interval -0.2209 pana la +0.2000. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3822 | +0.3051 | -0.0771 |
| de | +0.8040 | +0.7806 | -0.0234 |
| en | +0.7200 | +0.7283 | +0.0083 |
| es | +0.6083 | +0.6136 | +0.0053 |
| fil | +0.5514 | +0.5813 | +0.0299 |
| fr | +0.4318 | +0.4253 | -0.0065 |
| it | +0.7297 | +0.7316 | +0.0019 |
| ja | +0.4679 | +0.4610 | -0.0069 |
| pt | +0.7417 | +0.7443 | +0.0026 |
| si | +0.0986 | +0.2512 | +0.1526 |

**Diferenta medie +0.0087**, interval -0.0771 pana la +0.1526.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4069 | +0.3181 | -0.0187 | +0.0641 |
| de | +0.6358 | +0.8646 | -0.0318 | -0.0606 |
| en | +0.8025 | +0.7283 | +0.0000 | -0.0083 |
| es | +0.6724 | +0.5965 | -0.0130 | +0.0118 |
| fil | +0.4002 | +0.5631 | -0.0168 | -0.0117 |
| fr | +0.5174 | +0.2617 | +0.0263 | +0.1701 |
| it | +0.6156 | +0.7332 | -0.0182 | -0.0035 |
| ja | +0.5695 | +0.4798 | -0.0684 | -0.0119 |
| pt | +0.7591 | +0.7369 | +0.0045 | +0.0048 |
| si | +0.1526 | +0.1693 | +0.1669 | -0.0707 |
