# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:00:16 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4605 | [+0.3759, +0.5378] | 30 | 11 | +0.3827 | [+0.0816, +0.6559] | -0.0778 | [-0.3911, +0.2114] |
| de | 570 | 193 | +0.5615 | [+0.5022, +0.6156] | 23 | 11 | +0.7942 | [+0.4885, +0.9231] | +0.2327 | [-0.0773, +0.3792] |
| en | 570 | 190 | +0.7838 | [+0.7468, +0.8175] | 30 | 10 | +0.6639 | [+0.5620, +0.8224] | -0.1200 | [-0.2304, +0.0477] |
| es | 593 | 208 | +0.6473 | [+0.5991, +0.6910] | 30 | 10 | +0.7029 | [+0.5494, +0.8204] | +0.0555 | [-0.1064, +0.1825] |
| fil | 570 | 555 | +0.4080 | [+0.3353, +0.4760] | 30 | 30 | +0.4575 | [+0.1891, +0.6746] | +0.0495 | [-0.2272, +0.2764] |
| fr | 569 | 191 | +0.5379 | [+0.4762, +0.5959] | 30 | 11 | +0.5323 | [+0.2976, +0.7087] | -0.0057 | [-0.2409, +0.1804] |
| it | 570 | 192 | +0.5714 | [+0.5160, +0.6277] | 30 | 10 | +0.6907 | [+0.4826, +0.8286] | +0.1193 | [-0.0961, +0.2760] |
| ja | 570 | 190 | +0.5611 | [+0.4862, +0.6289] | 30 | 10 | +0.6582 | [+0.3963, +0.8083] | +0.0971 | [-0.1792, +0.2613] |
| pt | 567 | 562 | +0.7180 | [+0.6752, +0.7564] | 30 | 30 | +0.6940 | [+0.4814, +0.8828] | -0.0240 | [-0.2349, +0.1639] |
| si | 600 | 578 | +0.3562 | [+0.2851, +0.4253] | 30 | 30 | +0.3211 | [-0.1807, +0.6042] | -0.0351 | [-0.5356, +0.2602] |
| **medie** | | | **+0.5606** | | | | **+0.5898** | | **+0.0291** | |

**Δ split mediu +0.0291**, sd intre limbi 0.1039, interval -0.1200 pana la +0.2327. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3827 | +0.3827 | +0.0000 |
| de | +0.7942 | +0.7942 | +0.0000 |
| en | +0.6639 | +0.6639 | +0.0000 |
| es | +0.7029 | +0.7029 | +0.0000 |
| fil | +0.4575 | +0.4575 | +0.0000 |
| fr | +0.5323 | +0.5322 | -0.0001 |
| it | +0.6907 | +0.6907 | +0.0000 |
| ja | +0.6582 | +0.6582 | +0.0000 |
| pt | +0.6940 | +0.6940 | +0.0000 |
| si | +0.3211 | +0.3211 | +0.0000 |

**Diferenta medie -0.0000**, interval -0.0001 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4413 | +0.4979 | +0.0192 | -0.1152 |
| de | +0.6187 | +0.8403 | -0.0572 | -0.0461 |
| en | +0.7881 | +0.6730 | -0.0043 | -0.0091 |
| es | +0.6643 | +0.6321 | -0.0170 | +0.0708 |
| fil | +0.4283 | +0.4965 | -0.0203 | -0.0390 |
| fr | +0.5032 | +0.4678 | +0.0347 | +0.0645 |
| it | +0.5737 | +0.6980 | -0.0023 | -0.0073 |
| ja | +0.5529 | +0.5872 | +0.0082 | +0.0710 |
| pt | +0.7248 | +0.7231 | -0.0068 | -0.0291 |
| si | +0.3208 | +0.3208 | +0.0354 | +0.0003 |
