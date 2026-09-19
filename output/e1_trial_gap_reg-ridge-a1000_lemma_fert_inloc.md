# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:22:08 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4173 | [+0.3293, +0.5004] | 30 | 11 | +0.1653 | [-0.2574, +0.5952] | -0.2520 | [-0.6884, +0.1881] |
| de | 570 | 193 | +0.6213 | [+0.5630, +0.6735] | 23 | 11 | +0.7176 | [+0.4894, +0.8385] | +0.0964 | [-0.1398, +0.2281] |
| en | 570 | 190 | +0.7783 | [+0.7356, +0.8144] | 30 | 10 | +0.6734 | [+0.4461, +0.8146] | -0.1050 | [-0.3330, +0.0459] |
| es | 593 | 208 | +0.6279 | [+0.5765, +0.6727] | 30 | 10 | +0.6436 | [+0.3120, +0.8192] | +0.0158 | [-0.3209, +0.1939] |
| fil | 570 | 555 | +0.4061 | [+0.3363, +0.4717] | 30 | 30 | +0.5494 | [+0.2862, +0.7275] | +0.1433 | [-0.1350, +0.3408] |
| fr | 569 | 191 | +0.4941 | [+0.4294, +0.5548] | 30 | 11 | +0.2359 | [-0.1450, +0.5881] | -0.2582 | [-0.6527, +0.0983] |
| it | 570 | 192 | +0.6066 | [+0.5513, +0.6612] | 30 | 10 | +0.6016 | [+0.3527, +0.7920] | -0.0050 | [-0.2610, +0.1922] |
| ja | 570 | 190 | +0.6141 | [+0.5538, +0.6698] | 30 | 10 | +0.5702 | [+0.4039, +0.6796] | -0.0439 | [-0.2229, +0.0787] |
| pt | 567 | 562 | +0.7227 | [+0.6749, +0.7636] | 30 | 30 | +0.7755 | [+0.6068, +0.8999] | +0.0528 | [-0.1222, +0.1815] |
| si | 600 | 578 | +0.2654 | [+0.2058, +0.3282] | 30 | 30 | +0.0514 | [-0.3243, +0.4711] | -0.2140 | [-0.5949, +0.2123] |
| **medie** | | | **+0.5554** | | | | **+0.4984** | | **-0.0570** | |

**Δ split mediu -0.0570**, sd intre limbi 0.1450, interval -0.2582 pana la +0.1433. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1653 | +0.1653 | +0.0000 |
| de | +0.7176 | +0.7176 | +0.0000 |
| en | +0.6734 | +0.6734 | +0.0000 |
| es | +0.6436 | +0.6436 | +0.0000 |
| fil | +0.5494 | +0.5494 | +0.0000 |
| fr | +0.2359 | +0.2359 | +0.0000 |
| it | +0.6016 | +0.6016 | +0.0000 |
| ja | +0.5702 | +0.5702 | +0.0000 |
| pt | +0.7755 | +0.7755 | +0.0000 |
| si | +0.0514 | +0.0514 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3882 | +0.1614 | +0.0291 | +0.0039 |
| de | +0.6369 | +0.7903 | -0.0156 | -0.0727 |
| en | +0.7802 | +0.6232 | -0.0019 | +0.0502 |
| es | +0.6183 | +0.7018 | +0.0096 | -0.0582 |
| fil | +0.4138 | +0.5038 | -0.0077 | +0.0456 |
| fr | +0.4955 | +0.2861 | -0.0014 | -0.0502 |
| it | +0.6005 | +0.6073 | +0.0061 | -0.0057 |
| ja | +0.5719 | +0.4469 | +0.0422 | +0.1233 |
| pt | +0.7346 | +0.7733 | -0.0119 | +0.0022 |
| si | +0.2795 | +0.1413 | -0.0141 | -0.0899 |
