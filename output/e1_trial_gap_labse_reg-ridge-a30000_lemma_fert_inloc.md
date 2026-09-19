# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:34:31 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4330 | [+0.3457, +0.5126] | 30 | 11 | +0.2633 | [-0.0706, +0.6241] | -0.1698 | [-0.5084, +0.2003] |
| de | 570 | 193 | +0.5344 | [+0.4703, +0.5916] | 23 | 11 | +0.7564 | [+0.5016, +0.9046] | +0.2220 | [-0.0383, +0.3910] |
| en | 570 | 190 | +0.7542 | [+0.7128, +0.7921] | 30 | 10 | +0.6242 | [+0.5183, +0.8140] | -0.1300 | [-0.2439, +0.0716] |
| es | 593 | 208 | +0.6016 | [+0.5476, +0.6484] | 30 | 10 | +0.6131 | [+0.4061, +0.7947] | +0.0116 | [-0.2009, +0.1985] |
| fil | 570 | 555 | +0.3742 | [+0.2990, +0.4399] | 30 | 30 | +0.3531 | [+0.0612, +0.5854] | -0.0211 | [-0.3239, +0.2259] |
| fr | 569 | 191 | +0.5324 | [+0.4689, +0.5967] | 30 | 11 | +0.5179 | [+0.2488, +0.7279] | -0.0145 | [-0.2863, +0.2054] |
| it | 570 | 192 | +0.5082 | [+0.4471, +0.5667] | 30 | 10 | +0.6551 | [+0.4486, +0.8069] | +0.1468 | [-0.0680, +0.3169] |
| ja | 570 | 190 | +0.5183 | [+0.4452, +0.5852] | 30 | 10 | +0.5531 | [+0.3025, +0.7319] | +0.0348 | [-0.2283, +0.2269] |
| pt | 567 | 562 | +0.6814 | [+0.6370, +0.7216] | 30 | 30 | +0.6578 | [+0.4495, +0.8516] | -0.0236 | [-0.2405, +0.1740] |
| si | 600 | 578 | +0.3276 | [+0.2528, +0.4005] | 30 | 30 | +0.3838 | [-0.0494, +0.6200] | +0.0563 | [-0.3802, +0.3142] |
| **medie** | | | **+0.5265** | | | | **+0.5378** | | **+0.0113** | |

**Δ split mediu +0.0113**, sd intre limbi 0.1160, interval -0.1698 pana la +0.2220. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2633 | +0.2633 | +0.0000 |
| de | +0.7564 | +0.7564 | +0.0000 |
| en | +0.6242 | +0.6242 | +0.0000 |
| es | +0.6131 | +0.6131 | +0.0000 |
| fil | +0.3531 | +0.3531 | +0.0000 |
| fr | +0.5179 | +0.5179 | +0.0000 |
| it | +0.6551 | +0.6551 | +0.0000 |
| ja | +0.5531 | +0.5531 | +0.0000 |
| pt | +0.6578 | +0.6578 | +0.0000 |
| si | +0.3838 | +0.3838 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4153 | +0.3133 | +0.0177 | -0.0500 |
| de | +0.5629 | +0.7727 | -0.0285 | -0.0163 |
| en | +0.7580 | +0.6076 | -0.0038 | +0.0166 |
| es | +0.5956 | +0.5431 | +0.0060 | +0.0700 |
| fil | +0.3942 | +0.3641 | -0.0200 | -0.0110 |
| fr | +0.4962 | +0.4979 | +0.0362 | +0.0200 |
| it | +0.5073 | +0.6305 | +0.0009 | +0.0246 |
| ja | +0.5085 | +0.4797 | +0.0098 | +0.0734 |
| pt | +0.6744 | +0.6567 | +0.0070 | +0.0011 |
| si | +0.2954 | +0.3400 | +0.0322 | +0.0438 |
