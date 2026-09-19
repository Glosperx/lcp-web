# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:38:55 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3999 | [+0.3209, +0.4740] | 30 | 11 | +0.3541 | [-0.2142, +0.7305] | -0.0458 | [-0.6245, +0.3407] |
| de | 570 | 193 | +0.6390 | [+0.5871, +0.6849] | 23 | 11 | +0.7231 | [+0.4045, +0.8927] | +0.0842 | [-0.2524, +0.2602] |
| en | 570 | 190 | +0.8135 | [+0.7738, +0.8460] | 30 | 10 | +0.7102 | [+0.4308, +0.8780] | -0.1033 | [-0.3896, +0.0681] |
| es | 593 | 208 | +0.6419 | [+0.5964, +0.6833] | 30 | 10 | +0.6829 | [+0.4137, +0.8440] | +0.0411 | [-0.2266, +0.2078] |
| fil | 570 | 555 | +0.4125 | [+0.3417, +0.4786] | 30 | 30 | +0.5401 | [+0.2733, +0.7840] | +0.1276 | [-0.1403, +0.3817] |
| fr | 569 | 191 | +0.5679 | [+0.5011, +0.6262] | 30 | 11 | +0.3610 | [+0.0119, +0.6384] | -0.2068 | [-0.5710, +0.0732] |
| it | 570 | 192 | +0.6091 | [+0.5537, +0.6651] | 30 | 10 | +0.7116 | [+0.5392, +0.8347] | +0.1025 | [-0.0843, +0.2435] |
| ja | 570 | 190 | +0.6337 | [+0.5783, +0.6860] | 30 | 10 | +0.5425 | [+0.2625, +0.7486] | -0.0912 | [-0.3750, +0.1193] |
| pt | 567 | 562 | +0.7542 | [+0.7161, +0.7907] | 30 | 30 | +0.7585 | [+0.5863, +0.8905] | +0.0043 | [-0.1719, +0.1370] |
| si | 600 | 578 | +0.1864 | [+0.1177, +0.2508] | 30 | 30 | -0.1406 | [-0.4628, +0.2289] | -0.3270 | [-0.6466, +0.0427] |
| **medie** | | | **+0.5658** | | | | **+0.5243** | | **-0.0414** | |

**Δ split mediu -0.0414**, sd intre limbi 0.1450, interval -0.3270 pana la +0.1276. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3541 | +0.3657 | +0.0116 |
| de | +0.7231 | +0.7349 | +0.0118 |
| en | +0.7102 | +0.7035 | -0.0067 |
| es | +0.6829 | +0.7032 | +0.0203 |
| fil | +0.5401 | +0.5664 | +0.0263 |
| fr | +0.3610 | +0.3668 | +0.0058 |
| it | +0.7116 | +0.7158 | +0.0042 |
| ja | +0.5425 | +0.5579 | +0.0154 |
| pt | +0.7585 | +0.7541 | -0.0044 |
| si | -0.1406 | -0.1399 | +0.0007 |

**Diferenta medie +0.0085**, interval -0.0067 pana la +0.0263.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3871 | +0.4146 | +0.0128 | -0.0605 |
| de | +0.6426 | +0.7785 | -0.0036 | -0.0554 |
| en | +0.8167 | +0.7205 | -0.0032 | -0.0103 |
| es | +0.6681 | +0.6694 | -0.0262 | +0.0135 |
| fil | +0.4155 | +0.5622 | -0.0030 | -0.0221 |
| fr | +0.5455 | +0.3557 | +0.0224 | +0.0053 |
| it | +0.6003 | +0.7323 | +0.0088 | -0.0207 |
| ja | +0.6111 | +0.5529 | +0.0226 | -0.0104 |
| pt | +0.7651 | +0.7622 | -0.0109 | -0.0037 |
| si | +0.1684 | -0.1425 | +0.0180 | +0.0019 |
