# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:58:29 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4204 | [+0.3322, +0.4988] | 30 | 11 | +0.1557 | [-0.2983, +0.6162] | -0.2647 | [-0.7228, +0.2024] |
| de | 570 | 193 | +0.6103 | [+0.5514, +0.6642] | 23 | 11 | +0.6927 | [+0.4108, +0.8204] | +0.0824 | [-0.2036, +0.2270] |
| en | 570 | 190 | +0.7582 | [+0.7142, +0.7970] | 30 | 10 | +0.6555 | [+0.4122, +0.7871] | -0.1027 | [-0.3537, +0.0409] |
| es | 593 | 208 | +0.6188 | [+0.5656, +0.6654] | 30 | 10 | +0.5868 | [+0.2137, +0.7881] | -0.0320 | [-0.4055, +0.1713] |
| fil | 570 | 555 | +0.3921 | [+0.3227, +0.4583] | 30 | 30 | +0.5787 | [+0.3341, +0.7443] | +0.1866 | [-0.0669, +0.3668] |
| fr | 569 | 191 | +0.4935 | [+0.4296, +0.5549] | 30 | 11 | +0.2284 | [-0.1691, +0.5868] | -0.2651 | [-0.6711, +0.0912] |
| it | 570 | 192 | +0.6072 | [+0.5530, +0.6632] | 30 | 10 | +0.5948 | [+0.3571, +0.7932] | -0.0124 | [-0.2568, +0.1953] |
| ja | 570 | 190 | +0.6063 | [+0.5467, +0.6601] | 30 | 10 | +0.6024 | [+0.4339, +0.7126] | -0.0040 | [-0.1858, +0.1184] |
| pt | 567 | 562 | +0.7154 | [+0.6709, +0.7547] | 30 | 30 | +0.7978 | [+0.6325, +0.9175] | +0.0825 | [-0.0869, +0.2062] |
| si | 600 | 578 | +0.2390 | [+0.1739, +0.3063] | 30 | 30 | -0.0236 | [-0.3657, +0.3837] | -0.2626 | [-0.6093, +0.1578] |
| **medie** | | | **+0.5461** | | | | **+0.4869** | | **-0.0592** | |

**Δ split mediu -0.0592**, sd intre limbi 0.1614, interval -0.2651 pana la +0.1866. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1557 | +0.1557 | +0.0000 |
| de | +0.6927 | +0.6927 | +0.0000 |
| en | +0.6555 | +0.6555 | +0.0000 |
| es | +0.5868 | +0.5868 | +0.0000 |
| fil | +0.5787 | +0.5787 | +0.0000 |
| fr | +0.2284 | +0.2284 | +0.0000 |
| it | +0.5948 | +0.5948 | +0.0000 |
| ja | +0.6024 | +0.6024 | +0.0000 |
| pt | +0.7978 | +0.7978 | +0.0000 |
| si | -0.0236 | -0.0236 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3835 | +0.1832 | +0.0369 | -0.0275 |
| de | +0.6161 | +0.7890 | -0.0058 | -0.0963 |
| en | +0.7622 | +0.6230 | -0.0040 | +0.0325 |
| es | +0.6062 | +0.6509 | +0.0126 | -0.0641 |
| fil | +0.4086 | +0.5098 | -0.0165 | +0.0689 |
| fr | +0.4790 | +0.2505 | +0.0145 | -0.0221 |
| it | +0.5833 | +0.5664 | +0.0239 | +0.0284 |
| ja | +0.5489 | +0.4054 | +0.0574 | +0.1970 |
| pt | +0.7276 | +0.7899 | -0.0122 | +0.0079 |
| si | +0.2681 | +0.0243 | -0.0291 | -0.0479 |
