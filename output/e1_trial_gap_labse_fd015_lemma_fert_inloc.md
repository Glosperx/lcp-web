# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:47:12 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4760 | [+0.3985, +0.5487] | 30 | 11 | +0.4508 | [+0.1170, +0.7065] | -0.0252 | [-0.3568, +0.2474] |
| de | 570 | 193 | +0.5670 | [+0.5100, +0.6195] | 23 | 11 | +0.7587 | [+0.4483, +0.9054] | +0.1917 | [-0.1195, +0.3571] |
| en | 570 | 190 | +0.8075 | [+0.7741, +0.8375] | 30 | 10 | +0.7074 | [+0.5809, +0.8572] | -0.1000 | [-0.2322, +0.0558] |
| es | 593 | 208 | +0.6524 | [+0.6058, +0.6932] | 30 | 10 | +0.6937 | [+0.4784, +0.8337] | +0.0413 | [-0.1830, +0.1871] |
| fil | 570 | 555 | +0.4119 | [+0.3427, +0.4790] | 30 | 30 | +0.4826 | [+0.2315, +0.6946] | +0.0708 | [-0.1889, +0.2983] |
| fr | 569 | 191 | +0.5357 | [+0.4762, +0.5953] | 30 | 11 | +0.5445 | [+0.3045, +0.7195] | +0.0088 | [-0.2466, +0.1957] |
| it | 570 | 192 | +0.5707 | [+0.5151, +0.6265] | 30 | 10 | +0.7275 | [+0.5585, +0.8398] | +0.1567 | [-0.0231, +0.2877] |
| ja | 570 | 190 | +0.5744 | [+0.5036, +0.6387] | 30 | 10 | +0.6300 | [+0.3169, +0.8168] | +0.0556 | [-0.2697, +0.2532] |
| pt | 567 | 562 | +0.7422 | [+0.7028, +0.7772] | 30 | 30 | +0.7102 | [+0.4955, +0.9013] | -0.0320 | [-0.2454, +0.1532] |
| si | 600 | 578 | +0.3637 | [+0.2913, +0.4319] | 30 | 30 | +0.2806 | [-0.1460, +0.5702] | -0.0831 | [-0.5126, +0.2197] |
| **medie** | | | **+0.5701** | | | | **+0.5986** | | **+0.0285** | |

**Δ split mediu +0.0285**, sd intre limbi 0.0953, interval -0.1000 pana la +0.1917. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4508 | +0.4160 | -0.0348 |
| de | +0.7587 | +0.7392 | -0.0195 |
| en | +0.7074 | +0.7203 | +0.0129 |
| es | +0.6937 | +0.6944 | +0.0007 |
| fil | +0.4826 | +0.5176 | +0.0350 |
| fr | +0.5445 | +0.5459 | +0.0014 |
| it | +0.7275 | +0.7372 | +0.0097 |
| ja | +0.6300 | +0.6230 | -0.0070 |
| pt | +0.7102 | +0.7090 | -0.0012 |
| si | +0.2806 | +0.2985 | +0.0179 |

**Diferenta medie +0.0015**, interval -0.0348 pana la +0.0350.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4392 | +0.4736 | +0.0368 | -0.0228 |
| de | +0.5577 | +0.7886 | +0.0093 | -0.0299 |
| en | +0.8056 | +0.7250 | +0.0019 | -0.0176 |
| es | +0.6741 | +0.6733 | -0.0217 | +0.0204 |
| fil | +0.4185 | +0.5156 | -0.0066 | -0.0330 |
| fr | +0.4975 | +0.3698 | +0.0382 | +0.1747 |
| it | +0.5609 | +0.7339 | +0.0098 | -0.0064 |
| ja | +0.5671 | +0.5205 | +0.0073 | +0.1095 |
| pt | +0.7306 | +0.7514 | +0.0116 | -0.0412 |
| si | +0.3448 | +0.3569 | +0.0189 | -0.0763 |
