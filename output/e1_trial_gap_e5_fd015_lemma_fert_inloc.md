# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:48:02 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4474 | [+0.3665, +0.5197] | 30 | 11 | +0.4191 | [+0.0503, +0.7076] | -0.0283 | [-0.4062, +0.2726] |
| de | 570 | 193 | +0.5756 | [+0.5173, +0.6312] | 23 | 11 | +0.7779 | [+0.5453, +0.8945] | +0.2023 | [-0.0270, +0.3391] |
| en | 570 | 190 | +0.8069 | [+0.7722, +0.8388] | 30 | 10 | +0.7303 | [+0.4236, +0.8886] | -0.0766 | [-0.3908, +0.0881] |
| es | 593 | 208 | +0.6928 | [+0.6495, +0.7303] | 30 | 10 | +0.7279 | [+0.4453, +0.8952] | +0.0351 | [-0.2476, +0.2096] |
| fil | 570 | 555 | +0.4127 | [+0.3450, +0.4793] | 30 | 30 | +0.5404 | [+0.2605, +0.7488] | +0.1276 | [-0.1482, +0.3530] |
| fr | 569 | 191 | +0.5397 | [+0.4784, +0.5993] | 30 | 11 | +0.3748 | [+0.1235, +0.5872] | -0.1649 | [-0.4259, +0.0575] |
| it | 570 | 192 | +0.5912 | [+0.5395, +0.6460] | 30 | 10 | +0.6888 | [+0.4662, +0.8374] | +0.0976 | [-0.1311, +0.2638] |
| ja | 570 | 190 | +0.5917 | [+0.5229, +0.6567] | 30 | 10 | +0.6763 | [+0.4509, +0.8333] | +0.0846 | [-0.1495, +0.2520] |
| pt | 567 | 562 | +0.7510 | [+0.7041, +0.7900] | 30 | 30 | +0.7308 | [+0.5508, +0.8648] | -0.0202 | [-0.2044, +0.1199] |
| si | 600 | 578 | +0.2498 | [+0.1893, +0.3076] | 30 | 30 | +0.2856 | [+0.0113, +0.5584] | +0.0357 | [-0.2501, +0.3183] |
| **medie** | | | **+0.5659** | | | | **+0.5952** | | **+0.0293** | |

**Δ split mediu +0.0293**, sd intre limbi 0.1065, interval -0.1649 pana la +0.2023. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4191 | +0.4185 | -0.0006 |
| de | +0.7779 | +0.7757 | -0.0022 |
| en | +0.7303 | +0.7423 | +0.0120 |
| es | +0.7279 | +0.7026 | -0.0253 |
| fil | +0.5404 | +0.5577 | +0.0173 |
| fr | +0.3748 | +0.3711 | -0.0037 |
| it | +0.6888 | +0.6860 | -0.0028 |
| ja | +0.6763 | +0.6708 | -0.0055 |
| pt | +0.7308 | +0.7364 | +0.0056 |
| si | +0.2856 | +0.2904 | +0.0048 |

**Diferenta medie -0.0000**, interval -0.0253 pana la +0.0173.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4233 | +0.4876 | +0.0241 | -0.0685 |
| de | +0.5703 | +0.7526 | +0.0053 | +0.0253 |
| en | +0.7934 | +0.6477 | +0.0135 | +0.0826 |
| es | +0.6887 | +0.7409 | +0.0041 | -0.0130 |
| fil | +0.3794 | +0.5470 | +0.0333 | -0.0066 |
| fr | +0.5270 | +0.2878 | +0.0127 | +0.0870 |
| it | +0.5788 | +0.7015 | +0.0124 | -0.0127 |
| ja | +0.5569 | +0.5664 | +0.0348 | +0.1099 |
| pt | +0.7469 | +0.7280 | +0.0041 | +0.0028 |
| si | +0.2402 | +0.2886 | +0.0096 | -0.0030 |
