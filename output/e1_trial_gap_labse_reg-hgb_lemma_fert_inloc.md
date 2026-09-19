# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:13:34 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3787 | [+0.3013, +0.4492] | 30 | 11 | +0.3161 | [-0.1185, +0.6675] | -0.0626 | [-0.5112, +0.2971] |
| de | 570 | 193 | +0.6001 | [+0.5509, +0.6475] | 23 | 11 | +0.7720 | [+0.4809, +0.9126] | +0.1719 | [-0.1214, +0.3253] |
| en | 570 | 190 | +0.8075 | [+0.7725, +0.8395] | 30 | 10 | +0.7053 | [+0.5409, +0.8368] | -0.1022 | [-0.2719, +0.0334] |
| es | 593 | 208 | +0.6537 | [+0.6090, +0.6945] | 30 | 10 | +0.6740 | [+0.4440, +0.8304] | +0.0203 | [-0.2156, +0.1811] |
| fil | 570 | 555 | +0.3876 | [+0.3148, +0.4535] | 30 | 30 | +0.5802 | [+0.3230, +0.8074] | +0.1926 | [-0.0612, +0.4306] |
| fr | 569 | 191 | +0.5276 | [+0.4613, +0.5881] | 30 | 11 | +0.4496 | [+0.1234, +0.6772] | -0.0780 | [-0.4147, +0.1501] |
| it | 570 | 192 | +0.5985 | [+0.5462, +0.6529] | 30 | 10 | +0.7363 | [+0.5971, +0.8386] | +0.1378 | [-0.0172, +0.2563] |
| ja | 570 | 190 | +0.3407 | [+0.2618, +0.4169] | 30 | 10 | +0.5006 | [+0.0821, +0.7543] | +0.1599 | [-0.2817, +0.4235] |
| pt | 567 | 562 | +0.7651 | [+0.7272, +0.8008] | 30 | 30 | +0.7536 | [+0.5837, +0.8857] | -0.0115 | [-0.1870, +0.1264] |
| si | 600 | 578 | +0.2327 | [+0.1569, +0.3056] | 30 | 30 | +0.1082 | [-0.1980, +0.4255] | -0.1245 | [-0.4430, +0.2034] |
| **medie** | | | **+0.5292** | | | | **+0.5596** | | **+0.0304** | |

**Δ split mediu +0.0304**, sd intre limbi 0.1240, interval -0.1245 pana la +0.1926. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3161 | +0.1913 | -0.1248 |
| de | +0.7720 | +0.7391 | -0.0329 |
| en | +0.7053 | +0.7115 | +0.0062 |
| es | +0.6740 | +0.6441 | -0.0299 |
| fil | +0.5802 | +0.6013 | +0.0211 |
| fr | +0.4496 | +0.4364 | -0.0132 |
| it | +0.7363 | +0.7526 | +0.0163 |
| ja | +0.5006 | +0.3512 | -0.1494 |
| pt | +0.7536 | +0.7510 | -0.0026 |
| si | +0.1082 | +0.1863 | +0.0781 |

**Diferenta medie -0.0231**, interval -0.1494 pana la +0.0781.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4022 | +0.3638 | -0.0235 | -0.0477 |
| de | +0.6318 | +0.8754 | -0.0317 | -0.1034 |
| en | +0.8067 | +0.6708 | +0.0008 | +0.0345 |
| es | +0.6671 | +0.6569 | -0.0134 | +0.0171 |
| fil | +0.3912 | +0.5837 | -0.0036 | -0.0035 |
| fr | +0.5119 | +0.3072 | +0.0157 | +0.1424 |
| it | +0.6165 | +0.7476 | -0.0180 | -0.0113 |
| ja | +0.5757 | +0.4560 | -0.2350 | +0.0446 |
| pt | +0.7590 | +0.7797 | +0.0061 | -0.0261 |
| si | +0.1390 | +0.1399 | +0.0937 | -0.0317 |
