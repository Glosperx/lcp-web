# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:23:14 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4561 | [+0.3670, +0.5350] | 30 | 11 | +0.3470 | [-0.0285, +0.6196] | -0.1091 | [-0.4938, +0.1767] |
| de | 570 | 193 | +0.5925 | [+0.5332, +0.6470] | 23 | 11 | +0.8033 | [+0.5156, +0.9282] | +0.2108 | [-0.0940, +0.3481] |
| en | 570 | 190 | +0.7846 | [+0.7464, +0.8188] | 30 | 10 | +0.6625 | [+0.5572, +0.7925] | -0.1220 | [-0.2342, +0.0179] |
| es | 593 | 208 | +0.6606 | [+0.6112, +0.7037] | 30 | 10 | +0.6939 | [+0.4747, +0.8501] | +0.0334 | [-0.1894, +0.1962] |
| fil | 570 | 555 | +0.3903 | [+0.3201, +0.4589] | 30 | 30 | +0.5036 | [+0.2390, +0.7035] | +0.1133 | [-0.1572, +0.3370] |
| fr | 569 | 191 | +0.5443 | [+0.4856, +0.5990] | 30 | 11 | +0.4943 | [+0.2715, +0.6772] | -0.0501 | [-0.2854, +0.1432] |
| it | 570 | 192 | +0.6110 | [+0.5583, +0.6628] | 30 | 10 | +0.6719 | [+0.4633, +0.8207] | +0.0609 | [-0.1493, +0.2266] |
| ja | 570 | 190 | +0.5837 | [+0.5114, +0.6480] | 30 | 10 | +0.6682 | [+0.4083, +0.8146] | +0.0845 | [-0.1891, +0.2523] |
| pt | 567 | 562 | +0.7387 | [+0.6962, +0.7770] | 30 | 30 | +0.7101 | [+0.5039, +0.8861] | -0.0286 | [-0.2407, +0.1492] |
| si | 600 | 578 | +0.3484 | [+0.2773, +0.4143] | 30 | 30 | +0.3168 | [-0.1361, +0.6026] | -0.0317 | [-0.4809, +0.2604] |
| **medie** | | | **+0.5710** | | | | **+0.5872** | | **+0.0161** | |

**Δ split mediu +0.0161**, sd intre limbi 0.1042, interval -0.1220 pana la +0.2108. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3470 | +0.3470 | +0.0000 |
| de | +0.8033 | +0.8033 | +0.0000 |
| en | +0.6625 | +0.6625 | +0.0000 |
| es | +0.6939 | +0.6939 | +0.0000 |
| fil | +0.5036 | +0.5036 | +0.0000 |
| fr | +0.4943 | +0.4943 | +0.0000 |
| it | +0.6719 | +0.6719 | +0.0000 |
| ja | +0.6682 | +0.6682 | +0.0000 |
| pt | +0.7101 | +0.7101 | +0.0000 |
| si | +0.3168 | +0.3168 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4140 | +0.4263 | +0.0421 | -0.0793 |
| de | +0.6408 | +0.8417 | -0.0483 | -0.0384 |
| en | +0.7754 | +0.6650 | +0.0092 | -0.0025 |
| es | +0.6650 | +0.5937 | -0.0044 | +0.1002 |
| fil | +0.4017 | +0.5325 | -0.0114 | -0.0289 |
| fr | +0.4969 | +0.3127 | +0.0474 | +0.1816 |
| it | +0.6128 | +0.6752 | -0.0018 | -0.0033 |
| ja | +0.5450 | +0.5647 | +0.0387 | +0.1035 |
| pt | +0.7464 | +0.7394 | -0.0077 | -0.0293 |
| si | +0.2675 | +0.3083 | +0.0809 | +0.0085 |
