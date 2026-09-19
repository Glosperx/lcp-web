# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:12:28 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4264 | [+0.3429, +0.5029] | 30 | 11 | +0.3611 | [+0.0355, +0.5848] | -0.0653 | [-0.3934, +0.1769] |
| de | 570 | 193 | +0.5474 | [+0.4804, +0.6085] | 23 | 11 | +0.7555 | [+0.4222, +0.9063] | +0.2081 | [-0.1326, +0.3750] |
| en | 570 | 190 | +0.7637 | [+0.7245, +0.7989] | 30 | 10 | +0.6450 | [+0.5036, +0.7738] | -0.1186 | [-0.2641, +0.0205] |
| es | 593 | 208 | +0.6341 | [+0.5873, +0.6780] | 30 | 10 | +0.6822 | [+0.4030, +0.8547] | +0.0480 | [-0.2320, +0.2291] |
| fil | 570 | 555 | +0.3994 | [+0.3287, +0.4676] | 30 | 30 | +0.5112 | [+0.2482, +0.7122] | +0.1118 | [-0.1568, +0.3246] |
| fr | 569 | 191 | +0.4644 | [+0.3960, +0.5258] | 30 | 11 | +0.4538 | [+0.2152, +0.6594] | -0.0106 | [-0.2535, +0.2024] |
| it | 570 | 192 | +0.5907 | [+0.5347, +0.6446] | 30 | 10 | +0.6661 | [+0.4810, +0.7988] | +0.0754 | [-0.1134, +0.2197] |
| ja | 570 | 190 | +0.5275 | [+0.4518, +0.5959] | 30 | 10 | +0.6122 | [+0.2766, +0.8145] | +0.0847 | [-0.2599, +0.2949] |
| pt | 567 | 562 | +0.7308 | [+0.6897, +0.7677] | 30 | 30 | +0.6833 | [+0.4233, +0.8799] | -0.0475 | [-0.3085, +0.1521] |
| si | 600 | 578 | +0.3168 | [+0.2391, +0.3875] | 30 | 30 | +0.3262 | [-0.1385, +0.6423] | +0.0094 | [-0.4619, +0.3365] |
| **medie** | | | **+0.5401** | | | | **+0.5697** | | **+0.0295** | |

**Δ split mediu +0.0295**, sd intre limbi 0.0960, interval -0.1186 pana la +0.2081. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3611 | +0.3611 | +0.0000 |
| de | +0.7555 | +0.7555 | +0.0000 |
| en | +0.6450 | +0.6450 | +0.0000 |
| es | +0.6822 | +0.6822 | +0.0000 |
| fil | +0.5112 | +0.5112 | +0.0000 |
| fr | +0.4538 | +0.4538 | +0.0000 |
| it | +0.6661 | +0.6661 | +0.0000 |
| ja | +0.6122 | +0.6122 | +0.0000 |
| pt | +0.6833 | +0.6833 | +0.0000 |
| si | +0.3262 | +0.3262 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4048 | +0.0343 | +0.0216 | +0.3268 |
| de | +0.6034 | +0.8200 | -0.0560 | -0.0645 |
| en | +0.7458 | +0.6691 | +0.0179 | -0.0241 |
| es | +0.5783 | +0.5554 | +0.0558 | +0.1268 |
| fil | +0.4035 | +0.3846 | -0.0041 | +0.1266 |
| fr | +0.4093 | +0.2711 | +0.0551 | +0.1827 |
| it | +0.5738 | +0.6553 | +0.0169 | +0.0108 |
| ja | +0.4689 | +0.4855 | +0.0586 | +0.1267 |
| pt | +0.7057 | +0.7414 | +0.0251 | -0.0581 |
| si | +0.2499 | +0.2436 | +0.0669 | +0.0826 |
