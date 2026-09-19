# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:21:17 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4140 | [+0.3266, +0.4952] | 30 | 11 | +0.1625 | [-0.2830, +0.5873] | -0.2515 | [-0.7021, +0.1854] |
| de | 570 | 193 | +0.6076 | [+0.5481, +0.6619] | 23 | 11 | +0.7466 | [+0.4950, +0.8591] | +0.1390 | [-0.1256, +0.2678] |
| en | 570 | 190 | +0.7669 | [+0.7229, +0.8034] | 30 | 10 | +0.6518 | [+0.4038, +0.7858] | -0.1151 | [-0.3698, +0.0309] |
| es | 593 | 208 | +0.6174 | [+0.5643, +0.6628] | 30 | 10 | +0.5822 | [+0.2183, +0.7850] | -0.0352 | [-0.3992, +0.1782] |
| fil | 570 | 555 | +0.3879 | [+0.3180, +0.4554] | 30 | 30 | +0.5889 | [+0.3549, +0.7470] | +0.2010 | [-0.0466, +0.3766] |
| fr | 569 | 191 | +0.4963 | [+0.4323, +0.5562] | 30 | 11 | +0.2300 | [-0.1712, +0.5903] | -0.2663 | [-0.6808, +0.0933] |
| it | 570 | 192 | +0.6062 | [+0.5511, +0.6602] | 30 | 10 | +0.5941 | [+0.3691, +0.7906] | -0.0121 | [-0.2473, +0.1916] |
| ja | 570 | 190 | +0.5984 | [+0.5394, +0.6537] | 30 | 10 | +0.5949 | [+0.4369, +0.6972] | -0.0035 | [-0.1746, +0.1085] |
| pt | 567 | 562 | +0.7259 | [+0.6814, +0.7658] | 30 | 30 | +0.7801 | [+0.6104, +0.9025] | +0.0542 | [-0.1162, +0.1819] |
| si | 600 | 578 | +0.2545 | [+0.1914, +0.3196] | 30 | 30 | +0.0296 | [-0.3243, +0.4630] | -0.2249 | [-0.5889, +0.2131] |
| **medie** | | | **+0.5475** | | | | **+0.4961** | | **-0.0514** | |

**Δ split mediu -0.0514**, sd intre limbi 0.1618, interval -0.2663 pana la +0.2010. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1625 | +0.1625 | +0.0000 |
| de | +0.7466 | +0.7466 | +0.0000 |
| en | +0.6518 | +0.6518 | +0.0000 |
| es | +0.5822 | +0.5822 | +0.0000 |
| fil | +0.5889 | +0.5889 | +0.0000 |
| fr | +0.2300 | +0.2300 | +0.0000 |
| it | +0.5941 | +0.5941 | +0.0000 |
| ja | +0.5949 | +0.5949 | +0.0000 |
| pt | +0.7801 | +0.7801 | +0.0000 |
| si | +0.0296 | +0.0296 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3769 | +0.1471 | +0.0371 | +0.0154 |
| de | +0.6170 | +0.7936 | -0.0094 | -0.0470 |
| en | +0.7570 | +0.6055 | +0.0099 | +0.0463 |
| es | +0.5951 | +0.6421 | +0.0223 | -0.0599 |
| fil | +0.4024 | +0.5152 | -0.0145 | +0.0737 |
| fr | +0.4756 | +0.2109 | +0.0207 | +0.0191 |
| it | +0.5803 | +0.5743 | +0.0259 | +0.0198 |
| ja | +0.5304 | +0.3638 | +0.0680 | +0.2311 |
| pt | +0.7304 | +0.7843 | -0.0045 | -0.0042 |
| si | +0.2486 | -0.0031 | +0.0059 | +0.0327 |
