# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:38:11 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4363 | [+0.3416, +0.5197] | 30 | 11 | +0.3928 | [+0.0534, +0.6504] | -0.0435 | [-0.3981, +0.2304] |
| de | 570 | 193 | +0.5781 | [+0.5165, +0.6344] | 23 | 11 | +0.8227 | [+0.6056, +0.9255] | +0.2446 | [+0.0225, +0.3649] |
| en | 570 | 190 | +0.7859 | [+0.7484, +0.8199] | 30 | 10 | +0.6725 | [+0.4087, +0.8630] | -0.1134 | [-0.3781, +0.0789] |
| es | 593 | 208 | +0.6951 | [+0.6514, +0.7339] | 30 | 10 | +0.6693 | [+0.3146, +0.8842] | -0.0258 | [-0.3792, +0.1984] |
| fil | 570 | 555 | +0.4228 | [+0.3504, +0.4875] | 30 | 30 | +0.5409 | [+0.2802, +0.7380] | +0.1181 | [-0.1522, +0.3291] |
| fr | 569 | 191 | +0.5341 | [+0.4728, +0.5960] | 30 | 11 | +0.3133 | [+0.0922, +0.5105] | -0.2208 | [-0.4505, -0.0127] |
| it | 570 | 192 | +0.6057 | [+0.5540, +0.6598] | 30 | 10 | +0.6158 | [+0.3605, +0.8092] | +0.0100 | [-0.2552, +0.2138] |
| ja | 570 | 190 | +0.5922 | [+0.5253, +0.6566] | 30 | 10 | +0.7319 | [+0.5469, +0.8601] | +0.1396 | [-0.0591, +0.2839] |
| pt | 567 | 562 | +0.7223 | [+0.6708, +0.7643] | 30 | 30 | +0.6836 | [+0.4725, +0.8383] | -0.0387 | [-0.2572, +0.1232] |
| si | 600 | 578 | +0.2112 | [+0.1461, +0.2791] | 30 | 30 | +0.3751 | [+0.1516, +0.5900] | +0.1639 | [-0.0702, +0.3908] |
| **medie** | | | **+0.5584** | | | | **+0.5818** | | **+0.0234** | |

**Δ split mediu +0.0234**, sd intre limbi 0.1416, interval -0.2208 pana la +0.2446. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3928 | +0.3928 | +0.0000 |
| de | +0.8227 | +0.8227 | +0.0000 |
| en | +0.6725 | +0.6725 | +0.0000 |
| es | +0.6693 | +0.6693 | +0.0000 |
| fil | +0.5409 | +0.5409 | +0.0000 |
| fr | +0.3133 | +0.3133 | +0.0000 |
| it | +0.6158 | +0.6158 | +0.0000 |
| ja | +0.7319 | +0.7319 | +0.0000 |
| pt | +0.6836 | +0.6836 | +0.0000 |
| si | +0.3751 | +0.3751 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4230 | +0.4772 | +0.0133 | -0.0844 |
| de | +0.6246 | +0.8353 | -0.0465 | -0.0126 |
| en | +0.7757 | +0.6101 | +0.0102 | +0.0624 |
| es | +0.6772 | +0.6567 | +0.0179 | +0.0126 |
| fil | +0.4147 | +0.5413 | +0.0081 | -0.0004 |
| fr | +0.5204 | +0.2433 | +0.0137 | +0.0700 |
| it | +0.6051 | +0.6717 | +0.0006 | -0.0559 |
| ja | +0.5082 | +0.5979 | +0.0840 | +0.1340 |
| pt | +0.7423 | +0.7141 | -0.0200 | -0.0305 |
| si | +0.2165 | +0.2901 | -0.0053 | +0.0850 |
