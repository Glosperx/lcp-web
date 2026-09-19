# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:09:08 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4557 | [+0.3717, +0.5294] | 30 | 11 | +0.3812 | [-0.0574, +0.6961] | -0.0745 | [-0.5249, +0.2560] |
| de | 570 | 193 | +0.6319 | [+0.5808, +0.6815] | 23 | 11 | +0.8655 | [+0.6158, +0.9601] | +0.2336 | [-0.0172, +0.3490] |
| en | 570 | 190 | +0.8048 | [+0.7696, +0.8369] | 30 | 10 | +0.7002 | [+0.5523, +0.8304] | -0.1046 | [-0.2529, +0.0290] |
| es | 593 | 208 | +0.6687 | [+0.6217, +0.7096] | 30 | 10 | +0.7031 | [+0.4372, +0.8613] | +0.0344 | [-0.2242, +0.2004] |
| fil | 570 | 555 | +0.3536 | [+0.2768, +0.4230] | 30 | 30 | +0.5301 | [+0.2664, +0.7481] | +0.1765 | [-0.0920, +0.4129] |
| fr | 569 | 191 | +0.5446 | [+0.4836, +0.6020] | 30 | 11 | +0.4700 | [+0.2081, +0.6712] | -0.0746 | [-0.3496, +0.1384] |
| it | 570 | 192 | +0.6320 | [+0.5786, +0.6827] | 30 | 10 | +0.7037 | [+0.5377, +0.8314] | +0.0718 | [-0.0999, +0.2139] |
| ja | 570 | 190 | +0.5776 | [+0.5002, +0.6452] | 30 | 10 | +0.6446 | [+0.3625, +0.8165] | +0.0670 | [-0.2206, +0.2584] |
| pt | 567 | 562 | +0.7614 | [+0.7209, +0.7970] | 30 | 30 | +0.7387 | [+0.5415, +0.8870] | -0.0227 | [-0.2170, +0.1272] |
| si | 600 | 578 | +0.3007 | [+0.2350, +0.3621] | 30 | 30 | +0.0656 | [-0.2377, +0.3510] | -0.2351 | [-0.5462, +0.0603] |
| **medie** | | | **+0.5731** | | | | **+0.5803** | | **+0.0072** | |

**Δ split mediu +0.0072**, sd intre limbi 0.1390, interval -0.2351 pana la +0.2336. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3812 | +0.3386 | -0.0426 |
| de | +0.8655 | +0.8565 | -0.0090 |
| en | +0.7002 | +0.6998 | -0.0004 |
| es | +0.7031 | +0.6874 | -0.0157 |
| fil | +0.5301 | +0.5347 | +0.0046 |
| fr | +0.4700 | +0.4744 | +0.0044 |
| it | +0.7037 | +0.7070 | +0.0033 |
| ja | +0.6446 | +0.6271 | -0.0175 |
| pt | +0.7387 | +0.7399 | +0.0012 |
| si | +0.0656 | +0.0785 | +0.0129 |

**Diferenta medie -0.0059**, interval -0.0426 pana la +0.0129.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4313 | +0.4211 | +0.0244 | -0.0399 |
| de | +0.6567 | +0.8861 | -0.0248 | -0.0206 |
| en | +0.8055 | +0.7044 | -0.0007 | -0.0042 |
| es | +0.6848 | +0.6430 | -0.0161 | +0.0601 |
| fil | +0.4002 | +0.5631 | -0.0466 | -0.0330 |
| fr | +0.5107 | +0.3288 | +0.0339 | +0.1412 |
| it | +0.6289 | +0.7304 | +0.0031 | -0.0267 |
| ja | +0.5791 | +0.5001 | -0.0015 | +0.1445 |
| pt | +0.7636 | +0.7735 | -0.0022 | -0.0348 |
| si | +0.2834 | +0.0924 | +0.0173 | -0.0268 |
