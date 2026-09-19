# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:02:13 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4501 | [+0.3620, +0.5285] | 30 | 11 | +0.3748 | [+0.0395, +0.6008] | -0.0753 | [-0.4072, +0.1709] |
| de | 570 | 193 | +0.5644 | [+0.5029, +0.6230] | 23 | 11 | +0.7860 | [+0.4721, +0.9153] | +0.2216 | [-0.0960, +0.3668] |
| en | 570 | 190 | +0.7681 | [+0.7278, +0.8030] | 30 | 10 | +0.6467 | [+0.5049, +0.7892] | -0.1213 | [-0.2714, +0.0307] |
| es | 593 | 208 | +0.6254 | [+0.5716, +0.6753] | 30 | 10 | +0.6400 | [+0.3588, +0.8192] | +0.0147 | [-0.2586, +0.2022] |
| fil | 570 | 555 | +0.3840 | [+0.3122, +0.4543] | 30 | 30 | +0.4765 | [+0.2003, +0.6887] | +0.0926 | [-0.1857, +0.3175] |
| fr | 569 | 191 | +0.5082 | [+0.4456, +0.5648] | 30 | 11 | +0.4642 | [+0.2531, +0.6659] | -0.0440 | [-0.2617, +0.1640] |
| it | 570 | 192 | +0.5937 | [+0.5385, +0.6497] | 30 | 10 | +0.6750 | [+0.4684, +0.8215] | +0.0814 | [-0.1326, +0.2471] |
| ja | 570 | 190 | +0.5526 | [+0.4786, +0.6200] | 30 | 10 | +0.6672 | [+0.3831, +0.8264] | +0.1146 | [-0.1833, +0.2918] |
| pt | 567 | 562 | +0.7143 | [+0.6721, +0.7525] | 30 | 30 | +0.6995 | [+0.4589, +0.8830] | -0.0149 | [-0.2541, +0.1693] |
| si | 600 | 578 | +0.3364 | [+0.2585, +0.4083] | 30 | 30 | +0.2775 | [-0.2170, +0.5768] | -0.0589 | [-0.5575, +0.2441] |
| **medie** | | | **+0.5497** | | | | **+0.5707** | | **+0.0210** | |

**Δ split mediu +0.0210**, sd intre limbi 0.1050, interval -0.1213 pana la +0.2216. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3748 | +0.3748 | +0.0000 |
| de | +0.7860 | +0.7860 | +0.0000 |
| en | +0.6467 | +0.6467 | +0.0000 |
| es | +0.6400 | +0.6400 | +0.0000 |
| fil | +0.4765 | +0.4765 | +0.0000 |
| fr | +0.4642 | +0.4642 | +0.0000 |
| it | +0.6750 | +0.6750 | +0.0000 |
| ja | +0.6672 | +0.6672 | +0.0000 |
| pt | +0.6995 | +0.6995 | +0.0000 |
| si | +0.2775 | +0.2775 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4047 | +0.3194 | +0.0454 | +0.0554 |
| de | +0.6134 | +0.8443 | -0.0490 | -0.0583 |
| en | +0.7584 | +0.6659 | +0.0097 | -0.0192 |
| es | +0.6331 | +0.5410 | -0.0077 | +0.0990 |
| fil | +0.3916 | +0.4690 | -0.0076 | +0.0075 |
| fr | +0.4429 | +0.2266 | +0.0653 | +0.2376 |
| it | +0.5982 | +0.6654 | -0.0045 | +0.0096 |
| ja | +0.5142 | +0.5182 | +0.0384 | +0.1490 |
| pt | +0.7194 | +0.7521 | -0.0051 | -0.0526 |
| si | +0.2591 | +0.2934 | +0.0773 | -0.0159 |
