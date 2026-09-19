# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:04:46 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3665 | [+0.2805, +0.4461] | 30 | 11 | +0.2083 | [-0.4003, +0.6165] | -0.1582 | [-0.7723, +0.2685] |
| de | 570 | 193 | +0.5920 | [+0.5394, +0.6454] | 23 | 11 | +0.8146 | [+0.5756, +0.9350] | +0.2227 | [-0.0169, +0.3546] |
| en | 570 | 190 | +0.7368 | [+0.6961, +0.7743] | 30 | 10 | +0.6049 | [+0.4250, +0.7375] | -0.1319 | [-0.3154, +0.0066] |
| es | 593 | 208 | +0.6245 | [+0.5730, +0.6710] | 30 | 10 | +0.5769 | [+0.3474, +0.7644] | -0.0475 | [-0.2828, +0.1495] |
| fil | 570 | 555 | +0.3914 | [+0.3203, +0.4600] | 30 | 30 | +0.5431 | [+0.2978, +0.7369] | +0.1517 | [-0.0967, +0.3600] |
| fr | 569 | 191 | +0.5488 | [+0.4912, +0.6049] | 30 | 11 | +0.4705 | [+0.1685, +0.6915] | -0.0783 | [-0.3827, +0.1477] |
| it | 570 | 192 | +0.5958 | [+0.5408, +0.6489] | 30 | 10 | +0.6493 | [+0.4648, +0.8107] | +0.0535 | [-0.1382, +0.2260] |
| ja | 570 | 190 | +0.5694 | [+0.4932, +0.6402] | 30 | 10 | +0.5558 | [+0.3143, +0.7517] | -0.0135 | [-0.2765, +0.1980] |
| pt | 567 | 562 | +0.7375 | [+0.7001, +0.7733] | 30 | 30 | +0.7231 | [+0.5258, +0.8716] | -0.0144 | [-0.2205, +0.1388] |
| si | 600 | 578 | +0.1698 | [+0.0878, +0.2501] | 30 | 30 | +0.3802 | [+0.0569, +0.6066] | +0.2104 | [-0.1179, +0.4515] |
| **medie** | | | **+0.5333** | | | | **+0.5527** | | **+0.0195** | |

**Δ split mediu +0.0195**, sd intre limbi 0.1363, interval -0.1582 pana la +0.2227. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2083 | +0.2083 | +0.0000 |
| de | +0.8146 | +0.8146 | +0.0000 |
| en | +0.6049 | +0.6049 | +0.0000 |
| es | +0.5769 | +0.5769 | +0.0000 |
| fil | +0.5431 | +0.5431 | +0.0000 |
| fr | +0.4705 | +0.4705 | +0.0000 |
| it | +0.6493 | +0.6493 | +0.0000 |
| ja | +0.5558 | +0.5558 | +0.0000 |
| pt | +0.7231 | +0.7231 | +0.0000 |
| si | +0.3802 | +0.3802 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3318 | +0.2238 | +0.0347 | -0.0155 |
| de | +0.6095 | +0.7959 | -0.0175 | +0.0187 |
| en | +0.7259 | +0.5402 | +0.0109 | +0.0647 |
| es | +0.5975 | +0.5017 | +0.0270 | +0.0752 |
| fil | +0.3949 | +0.5725 | -0.0035 | -0.0294 |
| fr | +0.5398 | +0.3606 | +0.0090 | +0.1099 |
| it | +0.5995 | +0.6272 | -0.0037 | +0.0221 |
| ja | +0.4939 | +0.5157 | +0.0755 | +0.0401 |
| pt | +0.7314 | +0.7384 | +0.0061 | -0.0153 |
| si | +0.0689 | -0.0160 | +0.1009 | +0.3962 |
