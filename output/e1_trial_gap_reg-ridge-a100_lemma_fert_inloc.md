# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:21:43 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4150 | [+0.3274, +0.4957] | 30 | 11 | +0.1631 | [-0.2783, +0.5871] | -0.2519 | [-0.6990, +0.1842] |
| de | 570 | 193 | +0.6101 | [+0.5512, +0.6637] | 23 | 11 | +0.7435 | [+0.4927, +0.8545] | +0.1335 | [-0.1245, +0.2613] |
| en | 570 | 190 | +0.7685 | [+0.7242, +0.8049] | 30 | 10 | +0.6557 | [+0.4098, +0.7883] | -0.1128 | [-0.3621, +0.0334] |
| es | 593 | 208 | +0.6192 | [+0.5663, +0.6651] | 30 | 10 | +0.5893 | [+0.2283, +0.7869] | -0.0298 | [-0.3910, +0.1779] |
| fil | 570 | 555 | +0.3904 | [+0.3200, +0.4574] | 30 | 30 | +0.5863 | [+0.3487, +0.7462] | +0.1959 | [-0.0562, +0.3708] |
| fr | 569 | 191 | +0.4963 | [+0.4324, +0.5560] | 30 | 11 | +0.2306 | [-0.1697, +0.5899] | -0.2657 | [-0.6804, +0.0954] |
| it | 570 | 192 | +0.6069 | [+0.5520, +0.6606] | 30 | 10 | +0.5941 | [+0.3664, +0.7908] | -0.0128 | [-0.2513, +0.1901] |
| ja | 570 | 190 | +0.6014 | [+0.5424, +0.6567] | 30 | 10 | +0.5929 | [+0.4355, +0.6958] | -0.0085 | [-0.1795, +0.1054] |
| pt | 567 | 562 | +0.7258 | [+0.6810, +0.7655] | 30 | 30 | +0.7802 | [+0.6114, +0.9035] | +0.0544 | [-0.1159, +0.1824] |
| si | 600 | 578 | +0.2566 | [+0.1939, +0.3210] | 30 | 30 | +0.0310 | [-0.3252, +0.4648] | -0.2257 | [-0.5946, +0.2130] |
| **medie** | | | **+0.5490** | | | | **+0.4967** | | **-0.0523** | |

**Δ split mediu -0.0523**, sd intre limbi 0.1601, interval -0.2657 pana la +0.1959. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1631 | +0.1631 | +0.0000 |
| de | +0.7435 | +0.7435 | +0.0000 |
| en | +0.6557 | +0.6557 | +0.0000 |
| es | +0.5893 | +0.5893 | +0.0000 |
| fil | +0.5863 | +0.5863 | +0.0000 |
| fr | +0.2306 | +0.2306 | +0.0000 |
| it | +0.5941 | +0.5941 | +0.0000 |
| ja | +0.5929 | +0.5929 | +0.0000 |
| pt | +0.7802 | +0.7802 | +0.0000 |
| si | +0.0310 | +0.0310 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3790 | +0.1503 | +0.0360 | +0.0128 |
| de | +0.6213 | +0.7935 | -0.0112 | -0.0500 |
| en | +0.7609 | +0.6094 | +0.0076 | +0.0463 |
| es | +0.5990 | +0.6511 | +0.0202 | -0.0618 |
| fil | +0.4046 | +0.5154 | -0.0142 | +0.0709 |
| fr | +0.4790 | +0.2229 | +0.0173 | +0.0077 |
| it | +0.5840 | +0.5778 | +0.0229 | +0.0163 |
| ja | +0.5383 | +0.3821 | +0.0631 | +0.2108 |
| pt | +0.7314 | +0.7840 | -0.0056 | -0.0038 |
| si | +0.2587 | +0.0187 | -0.0021 | +0.0123 |
