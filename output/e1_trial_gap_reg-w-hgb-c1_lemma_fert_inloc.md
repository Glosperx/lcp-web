# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:04:48 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3992 | [+0.3187, +0.4714] | 30 | 11 | +0.4027 | [-0.1874, +0.7572] | +0.0035 | [-0.6026, +0.3668] |
| de | 570 | 193 | +0.6363 | [+0.5829, +0.6854] | 23 | 11 | +0.7732 | [+0.4741, +0.9084] | +0.1369 | [-0.1714, +0.2884] |
| en | 570 | 190 | +0.8111 | [+0.7733, +0.8444] | 30 | 10 | +0.7130 | [+0.4793, +0.8955] | -0.0980 | [-0.3399, +0.0887] |
| es | 593 | 208 | +0.6403 | [+0.5935, +0.6820] | 30 | 10 | +0.7063 | [+0.4660, +0.8623] | +0.0660 | [-0.1770, +0.2264] |
| fil | 570 | 555 | +0.4300 | [+0.3614, +0.4951] | 30 | 30 | +0.5721 | [+0.3199, +0.7839] | +0.1421 | [-0.1156, +0.3665] |
| fr | 569 | 191 | +0.5341 | [+0.4636, +0.5952] | 30 | 11 | +0.3574 | [+0.0166, +0.6205] | -0.1767 | [-0.5188, +0.1016] |
| it | 570 | 192 | +0.6134 | [+0.5571, +0.6685] | 30 | 10 | +0.7128 | [+0.4936, +0.8594] | +0.0993 | [-0.1308, +0.2603] |
| ja | 570 | 190 | +0.3650 | [+0.2889, +0.4350] | 30 | 10 | +0.1325 | [-0.1885, +0.4048] | -0.2325 | [-0.5519, +0.0459] |
| pt | 567 | 562 | +0.7565 | [+0.7178, +0.7922] | 30 | 30 | +0.7935 | [+0.6382, +0.9056] | +0.0370 | [-0.1255, +0.1547] |
| si | 600 | 578 | +0.2157 | [+0.1490, +0.2844] | 30 | 30 | -0.1366 | [-0.5743, +0.3984] | -0.3523 | [-0.7855, +0.1843] |
| **medie** | | | **+0.5402** | | | | **+0.5027** | | **-0.0375** | |

**Δ split mediu -0.0375**, sd intre limbi 0.1698, interval -0.3523 pana la +0.1421. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4027 | +0.3566 | -0.0461 |
| de | +0.7732 | +0.7840 | +0.0108 |
| en | +0.7130 | +0.6840 | -0.0290 |
| es | +0.7063 | +0.7036 | -0.0027 |
| fil | +0.5721 | +0.6135 | +0.0414 |
| fr | +0.3574 | +0.3400 | -0.0174 |
| it | +0.7128 | +0.6966 | -0.0162 |
| ja | +0.1325 | +0.0991 | -0.0334 |
| pt | +0.7935 | +0.7969 | +0.0034 |
| si | -0.1366 | -0.0128 | +0.1238 |

**Diferenta medie +0.0035**, interval -0.0461 pana la +0.1238.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4081 | +0.3086 | -0.0089 | +0.0941 |
| de | +0.6283 | +0.8251 | +0.0080 | -0.0519 |
| en | +0.8108 | +0.7304 | +0.0003 | -0.0174 |
| es | +0.6510 | +0.6880 | -0.0107 | +0.0183 |
| fil | +0.4148 | +0.5648 | +0.0152 | +0.0073 |
| fr | +0.5266 | +0.3799 | +0.0075 | -0.0225 |
| it | +0.6061 | +0.7433 | +0.0073 | -0.0305 |
| ja | +0.6005 | +0.4700 | -0.2355 | -0.3375 |
| pt | +0.7652 | +0.7681 | -0.0087 | +0.0254 |
| si | +0.1442 | -0.3577 | +0.0715 | +0.2211 |
