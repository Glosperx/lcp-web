# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:58:48 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4416 | [+0.3549, +0.5187] | 30 | 11 | +0.2577 | [-0.2717, +0.6492] | -0.1839 | [-0.7190, +0.2242] |
| de | 570 | 193 | +0.6639 | [+0.6106, +0.7124] | 23 | 11 | +0.8024 | [+0.5142, +0.9215] | +0.1385 | [-0.1615, +0.2702] |
| en | 570 | 190 | +0.8136 | [+0.7748, +0.8455] | 30 | 10 | +0.7048 | [+0.4431, +0.8523] | -0.1088 | [-0.3728, +0.0460] |
| es | 593 | 208 | +0.6671 | [+0.6202, +0.7089] | 30 | 10 | +0.6938 | [+0.3893, +0.8609] | +0.0267 | [-0.2727, +0.1991] |
| fil | 570 | 555 | +0.3986 | [+0.3263, +0.4630] | 30 | 30 | +0.6087 | [+0.3729, +0.7811] | +0.2100 | [-0.0393, +0.3962] |
| fr | 569 | 191 | +0.5316 | [+0.4642, +0.5912] | 30 | 11 | +0.3484 | [-0.0397, +0.6470] | -0.1832 | [-0.5873, +0.1299] |
| it | 570 | 192 | +0.6431 | [+0.5898, +0.6966] | 30 | 10 | +0.6467 | [+0.4208, +0.8076] | +0.0037 | [-0.2291, +0.1834] |
| ja | 570 | 190 | +0.6282 | [+0.5599, +0.6873] | 30 | 10 | +0.5498 | [+0.3601, +0.6859] | -0.0784 | [-0.2751, +0.0697] |
| pt | 567 | 562 | +0.7637 | [+0.7237, +0.7994] | 30 | 30 | +0.7956 | [+0.6431, +0.9086] | +0.0320 | [-0.1228, +0.1493] |
| si | 600 | 578 | +0.2733 | [+0.2010, +0.3416] | 30 | 30 | -0.0437 | [-0.4074, +0.3805] | -0.3171 | [-0.6806, +0.1141] |
| **medie** | | | **+0.5825** | | | | **+0.5364** | | **-0.0461** | |

**Δ split mediu -0.0461**, sd intre limbi 0.1598, interval -0.3171 pana la +0.2100. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2577 | +0.2197 | -0.0380 |
| de | +0.8024 | +0.8121 | +0.0097 |
| en | +0.7048 | +0.6845 | -0.0203 |
| es | +0.6938 | +0.6851 | -0.0087 |
| fil | +0.6087 | +0.6144 | +0.0057 |
| fr | +0.3484 | +0.3180 | -0.0304 |
| it | +0.6467 | +0.6290 | -0.0177 |
| ja | +0.5498 | +0.5204 | -0.0294 |
| pt | +0.7956 | +0.7963 | +0.0007 |
| si | -0.0437 | -0.0304 | +0.0133 |

**Diferenta medie -0.0115**, interval -0.0380 pana la +0.0133.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4162 | +0.2369 | +0.0254 | +0.0208 |
| de | +0.6623 | +0.8200 | +0.0016 | -0.0176 |
| en | +0.8077 | +0.6797 | +0.0059 | +0.0251 |
| es | +0.6520 | +0.6824 | +0.0151 | +0.0114 |
| fil | +0.4115 | +0.5577 | -0.0129 | +0.0510 |
| fr | +0.5274 | +0.3432 | +0.0042 | +0.0052 |
| it | +0.6245 | +0.6814 | +0.0186 | -0.0347 |
| ja | +0.6004 | +0.4658 | +0.0278 | +0.0840 |
| pt | +0.7672 | +0.7801 | -0.0035 | +0.0155 |
| si | +0.2879 | -0.0162 | -0.0146 | -0.0275 |
