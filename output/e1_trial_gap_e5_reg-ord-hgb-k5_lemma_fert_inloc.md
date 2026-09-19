# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:13:45 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4159 | [+0.3449, +0.4828] | 30 | 11 | +0.4592 | [-0.0109, +0.7974] | +0.0433 | [-0.4416, +0.3908] |
| de | 570 | 193 | +0.5730 | [+0.5236, +0.6227] | 23 | 11 | +0.7305 | [+0.4888, +0.8710] | +0.1575 | [-0.0912, +0.3083] |
| en | 570 | 190 | +0.7848 | [+0.7505, +0.8180] | 30 | 10 | +0.7000 | [+0.4055, +0.8538] | -0.0848 | [-0.3842, +0.0751] |
| es | 593 | 208 | +0.6820 | [+0.6409, +0.7192] | 30 | 10 | +0.6922 | [+0.4310, +0.8608] | +0.0101 | [-0.2507, +0.1859] |
| fil | 570 | 555 | +0.4076 | [+0.3417, +0.4706] | 30 | 30 | +0.5521 | [+0.2697, +0.8025] | +0.1445 | [-0.1460, +0.4013] |
| fr | 569 | 191 | +0.5616 | [+0.4974, +0.6204] | 30 | 11 | +0.3290 | [-0.0030, +0.5900] | -0.2325 | [-0.5662, +0.0404] |
| it | 570 | 192 | +0.5936 | [+0.5430, +0.6444] | 30 | 10 | +0.7070 | [+0.5417, +0.8327] | +0.1134 | [-0.0681, +0.2557] |
| ja | 570 | 190 | +0.4749 | [+0.4019, +0.5433] | 30 | 10 | +0.5077 | [+0.1840, +0.7324] | +0.0328 | [-0.3043, +0.2652] |
| pt | 567 | 562 | +0.7652 | [+0.7266, +0.8012] | 30 | 30 | +0.7736 | [+0.5938, +0.9100] | +0.0084 | [-0.1784, +0.1483] |
| si | 600 | 578 | +0.2370 | [+0.1708, +0.2998] | 30 | 30 | +0.3042 | [-0.0540, +0.5764] | +0.0672 | [-0.2786, +0.3448] |
| **medie** | | | **+0.5496** | | | | **+0.5756** | | **+0.0260** | |

**Δ split mediu +0.0260**, sd intre limbi 0.1158, interval -0.2325 pana la +0.1575. Trial-ul e mai mare pe 8 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4592 | +0.4413 | -0.0179 |
| de | +0.7305 | +0.7462 | +0.0157 |
| en | +0.7000 | +0.7060 | +0.0060 |
| es | +0.6922 | +0.6981 | +0.0059 |
| fil | +0.5521 | +0.5808 | +0.0287 |
| fr | +0.3290 | +0.3098 | -0.0192 |
| it | +0.7070 | +0.7089 | +0.0019 |
| ja | +0.5077 | +0.4892 | -0.0185 |
| pt | +0.7736 | +0.7783 | +0.0047 |
| si | +0.3042 | +0.3416 | +0.0374 |

**Diferenta medie +0.0045**, interval -0.0192 pana la +0.0374.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4179 | +0.4835 | -0.0020 | -0.0243 |
| de | +0.6115 | +0.7876 | -0.0385 | -0.0571 |
| en | +0.7842 | +0.6893 | +0.0006 | +0.0107 |
| es | +0.6938 | +0.6628 | -0.0118 | +0.0294 |
| fil | +0.4186 | +0.5679 | -0.0110 | -0.0158 |
| fr | +0.5285 | +0.2349 | +0.0331 | +0.0941 |
| it | +0.6128 | +0.7155 | -0.0192 | -0.0085 |
| ja | +0.5812 | +0.5052 | -0.1063 | +0.0025 |
| pt | +0.7768 | +0.7865 | -0.0116 | -0.0129 |
| si | +0.2191 | +0.1802 | +0.0179 | +0.1240 |
