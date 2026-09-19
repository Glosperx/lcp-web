# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 11:55:48 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4210 | [+0.3331, +0.5032] | 30 | 11 | +0.3503 | [-0.0227, +0.6593] | -0.0707 | [-0.4440, +0.2488] |
| de | 570 | 193 | +0.6240 | [+0.5655, +0.6768] | 23 | 11 | +0.7353 | [+0.4369, +0.8783] | +0.1113 | [-0.1952, +0.2661] |
| en | 570 | 190 | +0.7986 | [+0.7565, +0.8340] | 30 | 10 | +0.6700 | [+0.4732, +0.8457] | -0.1287 | [-0.3402, +0.0560] |
| es | 593 | 208 | +0.6370 | [+0.5868, +0.6816] | 30 | 10 | +0.6624 | [+0.3526, +0.8336] | +0.0254 | [-0.2871, +0.2067] |
| fil | 570 | 555 | +0.3755 | [+0.3037, +0.4424] | 30 | 30 | +0.4798 | [+0.2019, +0.6933] | +0.1043 | [-0.1815, +0.3283] |
| fr | 569 | 191 | +0.5052 | [+0.4358, +0.5697] | 30 | 11 | +0.3072 | [-0.1102, +0.6354] | -0.1980 | [-0.6096, +0.1436] |
| it | 570 | 192 | +0.5852 | [+0.5287, +0.6443] | 30 | 10 | +0.6221 | [+0.3672, +0.8077] | +0.0369 | [-0.2215, +0.2368] |
| ja | 570 | 190 | +0.5788 | [+0.5159, +0.6367] | 30 | 10 | +0.6409 | [+0.4270, +0.7696] | +0.0621 | [-0.1499, +0.2037] |
| pt | 567 | 562 | +0.7236 | [+0.6797, +0.7632] | 30 | 30 | +0.7532 | [+0.5867, +0.8787] | +0.0296 | [-0.1441, +0.1646] |
| si | 600 | 578 | +0.2865 | [+0.2278, +0.3477] | 30 | 30 | +0.0419 | [-0.3381, +0.4551] | -0.2446 | [-0.6288, +0.1687] |
| **medie** | | | **+0.5535** | | | | **+0.5263** | | **-0.0272** | |

**Δ split mediu -0.0272**, sd intre limbi 0.1261, interval -0.2446 pana la +0.1113. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3503 | +0.2990 | -0.0513 |
| de | +0.7353 | +0.7403 | +0.0050 |
| en | +0.6700 | +0.6526 | -0.0174 |
| es | +0.6624 | +0.6551 | -0.0073 |
| fil | +0.4798 | +0.4924 | +0.0126 |
| fr | +0.3072 | +0.2604 | -0.0468 |
| it | +0.6221 | +0.6240 | +0.0019 |
| ja | +0.6409 | +0.5998 | -0.0411 |
| pt | +0.7532 | +0.7599 | +0.0067 |
| si | +0.0419 | +0.0693 | +0.0274 |

**Diferenta medie -0.0110**, interval -0.0513 pana la +0.0274.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3824 | +0.3904 | +0.0386 | -0.0401 |
| de | +0.6033 | +0.7906 | +0.0207 | -0.0553 |
| en | +0.7816 | +0.6250 | +0.0170 | +0.0450 |
| es | +0.6037 | +0.6470 | +0.0333 | +0.0154 |
| fil | +0.3497 | +0.3579 | +0.0258 | +0.1219 |
| fr | +0.4992 | +0.2595 | +0.0060 | +0.0477 |
| it | +0.5374 | +0.6401 | +0.0478 | -0.0180 |
| ja | +0.4890 | +0.5888 | +0.0898 | +0.0521 |
| pt | +0.7208 | +0.7477 | +0.0028 | +0.0055 |
| si | +0.2518 | +0.0752 | +0.0347 | -0.0333 |
