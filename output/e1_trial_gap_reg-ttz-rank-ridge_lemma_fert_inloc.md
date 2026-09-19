# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:43:42 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4053 | [+0.3218, +0.4825] | 30 | 11 | +0.1658 | [-0.2905, +0.5905] | -0.2395 | [-0.6917, +0.1992] |
| de | 570 | 193 | +0.5928 | [+0.5319, +0.6486] | 23 | 11 | +0.7551 | [+0.5003, +0.8708] | +0.1623 | [-0.1035, +0.2935] |
| en | 570 | 190 | +0.7666 | [+0.7241, +0.8015] | 30 | 10 | +0.6565 | [+0.4035, +0.7891] | -0.1101 | [-0.3627, +0.0320] |
| es | 593 | 208 | +0.6174 | [+0.5679, +0.6613] | 30 | 10 | +0.6330 | [+0.3379, +0.8011] | +0.0156 | [-0.2818, +0.1941] |
| fil | 570 | 555 | +0.3976 | [+0.3271, +0.4663] | 30 | 30 | +0.5799 | [+0.3399, +0.7456] | +0.1823 | [-0.0637, +0.3678] |
| fr | 569 | 191 | +0.4926 | [+0.4292, +0.5524] | 30 | 11 | +0.2686 | [-0.1208, +0.6215] | -0.2240 | [-0.6165, +0.1321] |
| it | 570 | 192 | +0.5971 | [+0.5443, +0.6495] | 30 | 10 | +0.5921 | [+0.3862, +0.7902] | -0.0050 | [-0.2140, +0.2041] |
| ja | 570 | 190 | +0.6115 | [+0.5559, +0.6651] | 30 | 10 | +0.5927 | [+0.4241, +0.6970] | -0.0188 | [-0.1971, +0.0967] |
| pt | 567 | 562 | +0.7213 | [+0.6742, +0.7617] | 30 | 30 | +0.7276 | [+0.5306, +0.8703] | +0.0063 | [-0.1876, +0.1553] |
| si | 600 | 578 | +0.2589 | [+0.1962, +0.3242] | 30 | 30 | +0.0891 | [-0.3090, +0.5443] | -0.1699 | [-0.5813, +0.2927] |
| **medie** | | | **+0.5461** | | | | **+0.5060** | | **-0.0401** | |

**Δ split mediu -0.0401**, sd intre limbi 0.1463, interval -0.2395 pana la +0.1823. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1658 | +0.1658 | +0.0000 |
| de | +0.7551 | +0.7551 | +0.0000 |
| en | +0.6565 | +0.6565 | +0.0000 |
| es | +0.6330 | +0.6330 | +0.0000 |
| fil | +0.5799 | +0.5799 | +0.0000 |
| fr | +0.2686 | +0.2686 | +0.0000 |
| it | +0.5921 | +0.5921 | +0.0000 |
| ja | +0.5927 | +0.5927 | +0.0000 |
| pt | +0.7276 | +0.7276 | +0.0000 |
| si | +0.0891 | +0.0891 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3830 | +0.1057 | +0.0223 | +0.0601 |
| de | +0.6226 | +0.7862 | -0.0298 | -0.0311 |
| en | +0.7676 | +0.6051 | -0.0010 | +0.0514 |
| es | +0.6017 | +0.6286 | +0.0157 | +0.0044 |
| fil | +0.4061 | +0.5193 | -0.0085 | +0.0606 |
| fr | +0.4802 | +0.2791 | +0.0124 | -0.0105 |
| it | +0.5905 | +0.6216 | +0.0066 | -0.0295 |
| ja | +0.5838 | +0.4562 | +0.0277 | +0.1365 |
| pt | +0.7235 | +0.7434 | -0.0022 | -0.0158 |
| si | +0.2613 | +0.1736 | -0.0024 | -0.0845 |
