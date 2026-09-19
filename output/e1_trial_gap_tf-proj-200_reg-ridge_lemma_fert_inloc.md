# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 13:15:27 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4077 | [+0.3193, +0.4896] | 30 | 11 | +0.1705 | [-0.2993, +0.5518] | -0.2372 | [-0.7214, +0.1585] |
| de | 570 | 193 | +0.6235 | [+0.5692, +0.6749] | 23 | 11 | +0.7942 | [+0.5492, +0.8995] | +0.1707 | [-0.0827, +0.2868] |
| en | 570 | 190 | +0.7825 | [+0.7415, +0.8166] | 30 | 10 | +0.5832 | [+0.3667, +0.7483] | -0.1993 | [-0.4214, -0.0306] |
| es | 593 | 208 | +0.6701 | [+0.6282, +0.7095] | 30 | 10 | +0.6810 | [+0.2992, +0.8907] | +0.0110 | [-0.3694, +0.2229] |
| fil | 570 | 555 | +0.4084 | [+0.3395, +0.4745] | 30 | 30 | +0.5788 | [+0.3461, +0.7492] | +0.1704 | [-0.0623, +0.3576] |
| fr | 569 | 191 | +0.5297 | [+0.4677, +0.5857] | 30 | 11 | +0.3294 | [-0.0520, +0.6635] | -0.2003 | [-0.5798, +0.1457] |
| it | 570 | 192 | +0.6213 | [+0.5649, +0.6752] | 30 | 10 | +0.6016 | [+0.3742, +0.8087] | -0.0197 | [-0.2543, +0.1981] |
| ja | 570 | 190 | +0.6192 | [+0.5575, +0.6773] | 30 | 10 | +0.5839 | [+0.3746, +0.7342] | -0.0353 | [-0.2482, +0.1212] |
| pt | 567 | 562 | +0.7429 | [+0.6992, +0.7807] | 30 | 30 | +0.7833 | [+0.6148, +0.8985] | +0.0405 | [-0.1348, +0.1617] |
| si | 600 | 578 | +0.2075 | [+0.1449, +0.2715] | 30 | 30 | +0.1577 | [-0.2447, +0.5723] | -0.0499 | [-0.4495, +0.3737] |
| **medie** | | | **+0.5613** | | | | **+0.5264** | | **-0.0349** | |

**Δ split mediu -0.0349**, sd intre limbi 0.1445, interval -0.2372 pana la +0.1707. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1705 | +0.1705 | +0.0000 |
| de | +0.7942 | +0.7942 | +0.0000 |
| en | +0.5832 | +0.5832 | +0.0000 |
| es | +0.6810 | +0.6810 | +0.0000 |
| fil | +0.5788 | +0.5788 | +0.0000 |
| fr | +0.3294 | +0.3294 | +0.0000 |
| it | +0.6016 | +0.6016 | +0.0000 |
| ja | +0.5839 | +0.5839 | +0.0000 |
| pt | +0.7833 | +0.7833 | +0.0000 |
| si | +0.1577 | +0.1577 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3699 | +0.1815 | +0.0378 | -0.0110 |
| de | +0.6675 | +0.8119 | -0.0440 | -0.0177 |
| en | +0.7733 | +0.5473 | +0.0092 | +0.0359 |
| es | +0.6338 | +0.6963 | +0.0363 | -0.0153 |
| fil | +0.4033 | +0.5527 | +0.0051 | +0.0261 |
| fr | +0.5324 | +0.3361 | -0.0027 | -0.0067 |
| it | +0.6233 | +0.6249 | -0.0020 | -0.0233 |
| ja | +0.5722 | +0.5657 | +0.0470 | +0.0182 |
| pt | +0.7514 | +0.7988 | -0.0085 | -0.0155 |
| si | +0.2364 | +0.1646 | -0.0289 | -0.0069 |
