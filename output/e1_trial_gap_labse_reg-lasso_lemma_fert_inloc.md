# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:58:29 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3858 | [+0.2953, +0.4675] | 30 | 11 | +0.4015 | [-0.0391, +0.7006] | +0.0157 | [-0.4433, +0.3213] |
| de | 570 | 193 | +0.5874 | [+0.5343, +0.6380] | 23 | 11 | +0.8131 | [+0.5442, +0.9457] | +0.2257 | [-0.0392, +0.3690] |
| en | 570 | 190 | +0.7609 | [+0.7245, +0.7956] | 30 | 10 | +0.5830 | [+0.4794, +0.7346] | -0.1779 | [-0.2870, -0.0165] |
| es | 593 | 208 | +0.6325 | [+0.5834, +0.6778] | 30 | 10 | +0.6277 | [+0.4060, +0.7849] | -0.0047 | [-0.2369, +0.1611] |
| fil | 570 | 555 | +0.4000 | [+0.3285, +0.4684] | 30 | 30 | +0.5550 | [+0.3313, +0.7323] | +0.1550 | [-0.0720, +0.3420] |
| fr | 569 | 191 | +0.5588 | [+0.4999, +0.6138] | 30 | 11 | +0.4259 | [+0.0653, +0.6832] | -0.1329 | [-0.4970, +0.1282] |
| it | 570 | 192 | +0.6006 | [+0.5450, +0.6506] | 30 | 10 | +0.6515 | [+0.4693, +0.8031] | +0.0509 | [-0.1302, +0.2175] |
| ja | 570 | 190 | +0.5670 | [+0.4968, +0.6327] | 30 | 10 | +0.6020 | [+0.2429, +0.8362] | +0.0350 | [-0.3327, +0.2822] |
| pt | 567 | 562 | +0.7448 | [+0.7077, +0.7796] | 30 | 30 | +0.7301 | [+0.5440, +0.8883] | -0.0147 | [-0.2023, +0.1442] |
| si | 600 | 578 | +0.3045 | [+0.2261, +0.3788] | 30 | 30 | +0.3610 | [+0.0541, +0.6231] | +0.0565 | [-0.2526, +0.3316] |
| **medie** | | | **+0.5542** | | | | **+0.5751** | | **+0.0209** | |

**Δ split mediu +0.0209**, sd intre limbi 0.1190, interval -0.1779 pana la +0.2257. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4015 | +0.4015 | +0.0000 |
| de | +0.8131 | +0.8131 | +0.0000 |
| en | +0.5830 | +0.5830 | +0.0000 |
| es | +0.6277 | +0.6277 | +0.0000 |
| fil | +0.5550 | +0.5550 | +0.0000 |
| fr | +0.4259 | +0.4259 | +0.0000 |
| it | +0.6515 | +0.6515 | +0.0000 |
| ja | +0.6020 | +0.6020 | +0.0000 |
| pt | +0.7301 | +0.7301 | +0.0000 |
| si | +0.3610 | +0.3610 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3484 | +0.3303 | +0.0374 | +0.0712 |
| de | +0.6374 | +0.8389 | -0.0500 | -0.0258 |
| en | +0.7533 | +0.5966 | +0.0076 | -0.0136 |
| es | +0.6284 | +0.5802 | +0.0041 | +0.0475 |
| fil | +0.3843 | +0.5774 | +0.0157 | -0.0224 |
| fr | +0.5273 | +0.2881 | +0.0315 | +0.1378 |
| it | +0.6070 | +0.6266 | -0.0064 | +0.0249 |
| ja | +0.5270 | +0.5126 | +0.0400 | +0.0894 |
| pt | +0.7476 | +0.7309 | -0.0028 | -0.0008 |
| si | +0.1257 | +0.1358 | +0.1788 | +0.2252 |
