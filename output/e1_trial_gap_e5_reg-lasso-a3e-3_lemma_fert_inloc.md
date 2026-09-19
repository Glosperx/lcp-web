# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:39:23 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4243 | [+0.3283, +0.5065] | 30 | 11 | +0.4964 | [+0.1150, +0.7544] | +0.0722 | [-0.3220, +0.3446] |
| de | 570 | 193 | +0.6115 | [+0.5546, +0.6649] | 23 | 11 | +0.8376 | [+0.6224, +0.9418] | +0.2261 | [+0.0036, +0.3487] |
| en | 570 | 190 | +0.7895 | [+0.7542, +0.8214] | 30 | 10 | +0.6702 | [+0.4718, +0.8098] | -0.1192 | [-0.3209, +0.0227] |
| es | 593 | 208 | +0.6954 | [+0.6513, +0.7335] | 30 | 10 | +0.6649 | [+0.3813, +0.8488] | -0.0304 | [-0.3142, +0.1563] |
| fil | 570 | 555 | +0.3931 | [+0.3214, +0.4607] | 30 | 30 | +0.5429 | [+0.2987, +0.7340] | +0.1498 | [-0.0939, +0.3568] |
| fr | 569 | 191 | +0.5569 | [+0.4973, +0.6130] | 30 | 11 | +0.3332 | [+0.0379, +0.5872] | -0.2237 | [-0.5300, +0.0355] |
| it | 570 | 192 | +0.6312 | [+0.5777, +0.6816] | 30 | 10 | +0.6899 | [+0.5129, +0.8316] | +0.0587 | [-0.1265, +0.2149] |
| ja | 570 | 190 | +0.5815 | [+0.5067, +0.6509] | 30 | 10 | +0.6012 | [+0.2751, +0.8401] | +0.0197 | [-0.3169, +0.2683] |
| pt | 567 | 562 | +0.7569 | [+0.7139, +0.7941] | 30 | 30 | +0.7233 | [+0.5381, +0.8701] | -0.0336 | [-0.2335, +0.1191] |
| si | 600 | 578 | +0.2480 | [+0.1830, +0.3098] | 30 | 30 | +0.3126 | [-0.0228, +0.5996] | +0.0645 | [-0.2682, +0.3610] |
| **medie** | | | **+0.5688** | | | | **+0.5872** | | **+0.0184** | |

**Δ split mediu +0.0184**, sd intre limbi 0.1290, interval -0.2237 pana la +0.2261. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4964 | +0.4964 | +0.0000 |
| de | +0.8376 | +0.8376 | +0.0000 |
| en | +0.6702 | +0.6702 | +0.0000 |
| es | +0.6649 | +0.6649 | +0.0000 |
| fil | +0.5429 | +0.5429 | +0.0000 |
| fr | +0.3332 | +0.3332 | +0.0000 |
| it | +0.6899 | +0.6899 | +0.0000 |
| ja | +0.6012 | +0.6012 | +0.0000 |
| pt | +0.7233 | +0.7233 | +0.0000 |
| si | +0.3126 | +0.3126 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3884 | +0.4156 | +0.0359 | +0.0808 |
| de | +0.6408 | +0.8258 | -0.0293 | +0.0118 |
| en | +0.7675 | +0.6613 | +0.0220 | +0.0089 |
| es | +0.6760 | +0.6328 | +0.0194 | +0.0321 |
| fil | +0.3845 | +0.5523 | +0.0086 | -0.0094 |
| fr | +0.5337 | +0.2752 | +0.0232 | +0.0580 |
| it | +0.6332 | +0.6895 | -0.0020 | +0.0004 |
| ja | +0.5302 | +0.5228 | +0.0513 | +0.0784 |
| pt | +0.7583 | +0.7150 | -0.0014 | +0.0083 |
| si | +0.1874 | +0.3453 | +0.0606 | -0.0327 |
