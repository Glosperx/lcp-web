# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:07:47 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4646 | [+0.3835, +0.5334] | 30 | 11 | +0.4463 | [+0.0346, +0.7432] | -0.0183 | [-0.4397, +0.2863] |
| de | 570 | 193 | +0.6191 | [+0.5625, +0.6737] | 23 | 11 | +0.8146 | [+0.5840, +0.9219] | +0.1955 | [-0.0414, +0.3257] |
| en | 570 | 190 | +0.8170 | [+0.7850, +0.8477] | 30 | 10 | +0.7297 | [+0.4731, +0.8527] | -0.0873 | [-0.3484, +0.0453] |
| es | 593 | 208 | +0.7117 | [+0.6717, +0.7467] | 30 | 10 | +0.7041 | [+0.4173, +0.8760] | -0.0075 | [-0.2879, +0.1690] |
| fil | 570 | 555 | +0.3974 | [+0.3262, +0.4655] | 30 | 30 | +0.5575 | [+0.2894, +0.7648] | +0.1601 | [-0.1071, +0.3792] |
| fr | 569 | 191 | +0.5532 | [+0.4873, +0.6148] | 30 | 11 | +0.2993 | [+0.0139, +0.5599] | -0.2539 | [-0.5410, +0.0079] |
| it | 570 | 192 | +0.6299 | [+0.5804, +0.6814] | 30 | 10 | +0.7167 | [+0.5293, +0.8409] | +0.0868 | [-0.1081, +0.2268] |
| ja | 570 | 190 | +0.5196 | [+0.4505, +0.5827] | 30 | 10 | +0.6383 | [+0.3513, +0.8355] | +0.1187 | [-0.1826, +0.3279] |
| pt | 567 | 562 | +0.7643 | [+0.7200, +0.8027] | 30 | 30 | +0.7494 | [+0.5661, +0.8823] | -0.0149 | [-0.2035, +0.1216] |
| si | 600 | 578 | +0.3288 | [+0.2630, +0.3941] | 30 | 30 | +0.2556 | [-0.0687, +0.5503] | -0.0732 | [-0.4018, +0.2322] |
| **medie** | | | **+0.5806** | | | | **+0.5912** | | **+0.0106** | |

**Δ split mediu +0.0106**, sd intre limbi 0.1343, interval -0.2539 pana la +0.1955. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4463 | +0.4346 | -0.0117 |
| de | +0.8146 | +0.8269 | +0.0123 |
| en | +0.7297 | +0.7313 | +0.0016 |
| es | +0.7041 | +0.7101 | +0.0060 |
| fil | +0.5575 | +0.5900 | +0.0325 |
| fr | +0.2993 | +0.2932 | -0.0061 |
| it | +0.7167 | +0.7238 | +0.0071 |
| ja | +0.6383 | +0.6092 | -0.0291 |
| pt | +0.7494 | +0.7596 | +0.0102 |
| si | +0.2556 | +0.2500 | -0.0056 |

**Diferenta medie +0.0017**, interval -0.0291 pana la +0.0325.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4409 | +0.4230 | +0.0237 | +0.0233 |
| de | +0.6487 | +0.8479 | -0.0296 | -0.0333 |
| en | +0.8034 | +0.7134 | +0.0136 | +0.0163 |
| es | +0.7058 | +0.6650 | +0.0059 | +0.0391 |
| fil | +0.3997 | +0.5636 | -0.0023 | -0.0061 |
| fr | +0.5432 | +0.1929 | +0.0100 | +0.1064 |
| it | +0.6338 | +0.6972 | -0.0039 | +0.0195 |
| ja | +0.5401 | +0.5484 | -0.0205 | +0.0899 |
| pt | +0.7760 | +0.7683 | -0.0117 | -0.0189 |
| si | +0.2564 | +0.2886 | +0.0724 | -0.0330 |
