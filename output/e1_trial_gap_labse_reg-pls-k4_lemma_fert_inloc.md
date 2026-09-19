# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:23:38 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4403 | [+0.3547, +0.5170] | 30 | 11 | +0.4332 | [+0.1577, +0.6985] | -0.0071 | [-0.2946, +0.2808] |
| de | 570 | 193 | +0.5064 | [+0.4406, +0.5641] | 23 | 11 | +0.8098 | [+0.5879, +0.9320] | +0.3034 | [+0.0624, +0.4472] |
| en | 570 | 190 | +0.7572 | [+0.7163, +0.7948] | 30 | 10 | +0.6194 | [+0.4726, +0.8390] | -0.1378 | [-0.2902, +0.0958] |
| es | 593 | 208 | +0.6289 | [+0.5796, +0.6739] | 30 | 10 | +0.6545 | [+0.4758, +0.7802] | +0.0256 | [-0.1510, +0.1586] |
| fil | 570 | 555 | +0.3817 | [+0.3074, +0.4492] | 30 | 30 | +0.3975 | [+0.1233, +0.6319] | +0.0158 | [-0.2647, +0.2634] |
| fr | 569 | 191 | +0.4908 | [+0.4283, +0.5525] | 30 | 11 | +0.5112 | [+0.2477, +0.7025] | +0.0204 | [-0.2481, +0.2258] |
| it | 570 | 192 | +0.5186 | [+0.4593, +0.5774] | 30 | 10 | +0.7022 | [+0.5015, +0.8427] | +0.1836 | [-0.0246, +0.3452] |
| ja | 570 | 190 | +0.5102 | [+0.4363, +0.5815] | 30 | 10 | +0.6378 | [+0.3961, +0.7958] | +0.1276 | [-0.1419, +0.3039] |
| pt | 567 | 562 | +0.6753 | [+0.6285, +0.7164] | 30 | 30 | +0.6589 | [+0.4385, +0.8604] | -0.0164 | [-0.2405, +0.1914] |
| si | 600 | 578 | +0.3143 | [+0.2421, +0.3854] | 30 | 30 | +0.3769 | [-0.1269, +0.6395] | +0.0625 | [-0.4351, +0.3477] |
| **medie** | | | **+0.5224** | | | | **+0.5801** | | **+0.0578** | |

**Δ split mediu +0.0578**, sd intre limbi 0.1217, interval -0.1378 pana la +0.3034. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4332 | +0.4332 | +0.0000 |
| de | +0.8098 | +0.8098 | +0.0000 |
| en | +0.6194 | +0.6194 | +0.0000 |
| es | +0.6545 | +0.6545 | +0.0000 |
| fil | +0.3975 | +0.3975 | +0.0000 |
| fr | +0.5112 | +0.5112 | +0.0000 |
| it | +0.7022 | +0.7022 | +0.0000 |
| ja | +0.6378 | +0.6378 | +0.0000 |
| pt | +0.6589 | +0.6589 | +0.0000 |
| si | +0.3769 | +0.3769 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4406 | +0.4895 | -0.0003 | -0.0563 |
| de | +0.5385 | +0.8173 | -0.0321 | -0.0075 |
| en | +0.7616 | +0.6055 | -0.0044 | +0.0139 |
| es | +0.6228 | +0.5700 | +0.0061 | +0.0845 |
| fil | +0.4087 | +0.4245 | -0.0270 | -0.0270 |
| fr | +0.4596 | +0.4808 | +0.0312 | +0.0304 |
| it | +0.5130 | +0.6984 | +0.0056 | +0.0038 |
| ja | +0.5008 | +0.6010 | +0.0094 | +0.0368 |
| pt | +0.6771 | +0.6606 | -0.0018 | -0.0017 |
| si | +0.2782 | +0.3051 | +0.0361 | +0.0718 |
