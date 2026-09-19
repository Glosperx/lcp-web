# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:37:24 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4329 | [+0.3337, +0.5186] | 30 | 11 | +0.3522 | [-0.0070, +0.6235] | -0.0807 | [-0.4543, +0.2023] |
| de | 570 | 193 | +0.5842 | [+0.5232, +0.6402] | 23 | 11 | +0.8250 | [+0.5976, +0.9281] | +0.2408 | [+0.0039, +0.3615] |
| en | 570 | 190 | +0.7781 | [+0.7388, +0.8133] | 30 | 10 | +0.6478 | [+0.3810, +0.8389] | -0.1303 | [-0.4007, +0.0629] |
| es | 593 | 208 | +0.6855 | [+0.6410, +0.7244] | 30 | 10 | +0.6489 | [+0.2773, +0.8839] | -0.0366 | [-0.4009, +0.2052] |
| fil | 570 | 555 | +0.4004 | [+0.3283, +0.4682] | 30 | 30 | +0.5376 | [+0.2696, +0.7381] | +0.1372 | [-0.1367, +0.3513] |
| fr | 569 | 191 | +0.5301 | [+0.4679, +0.5919] | 30 | 11 | +0.3150 | [+0.0822, +0.5293] | -0.2151 | [-0.4562, +0.0143] |
| it | 570 | 192 | +0.6112 | [+0.5580, +0.6642] | 30 | 10 | +0.5979 | [+0.3409, +0.7954] | -0.0133 | [-0.2799, +0.1942] |
| ja | 570 | 190 | +0.5921 | [+0.5257, +0.6537] | 30 | 10 | +0.7401 | [+0.5675, +0.8549] | +0.1480 | [-0.0355, +0.2851] |
| pt | 567 | 562 | +0.7153 | [+0.6634, +0.7591] | 30 | 30 | +0.6757 | [+0.4601, +0.8323] | -0.0397 | [-0.2640, +0.1212] |
| si | 600 | 578 | +0.1851 | [+0.1167, +0.2562] | 30 | 30 | +0.3746 | [+0.1797, +0.6142] | +0.1895 | [-0.0174, +0.4445] |
| **medie** | | | **+0.5515** | | | | **+0.5715** | | **+0.0200** | |

**Δ split mediu +0.0200**, sd intre limbi 0.1504, interval -0.2151 pana la +0.2408. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3522 | +0.3522 | +0.0000 |
| de | +0.8250 | +0.8250 | +0.0000 |
| en | +0.6478 | +0.6478 | +0.0000 |
| es | +0.6489 | +0.6489 | +0.0000 |
| fil | +0.5376 | +0.5376 | +0.0000 |
| fr | +0.3150 | +0.3150 | +0.0000 |
| it | +0.5979 | +0.5979 | +0.0000 |
| ja | +0.7401 | +0.7401 | +0.0000 |
| pt | +0.6757 | +0.6757 | +0.0000 |
| si | +0.3746 | +0.3746 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4162 | +0.3978 | +0.0167 | -0.0456 |
| de | +0.6340 | +0.8422 | -0.0498 | -0.0172 |
| en | +0.7575 | +0.5618 | +0.0206 | +0.0860 |
| es | +0.6421 | +0.6147 | +0.0434 | +0.0342 |
| fil | +0.3986 | +0.5197 | +0.0018 | +0.0179 |
| fr | +0.5159 | +0.1824 | +0.0142 | +0.1326 |
| it | +0.5888 | +0.6450 | +0.0224 | -0.0471 |
| ja | +0.4899 | +0.6454 | +0.1022 | +0.0947 |
| pt | +0.7315 | +0.7140 | -0.0162 | -0.0383 |
| si | +0.1766 | +0.2456 | +0.0085 | +0.1290 |
