# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:43:21 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4008 | [+0.3225, +0.4708] | 30 | 11 | +0.4354 | [-0.0301, +0.7440] | +0.0346 | [-0.4361, +0.3567] |
| de | 570 | 193 | +0.6131 | [+0.5583, +0.6657] | 23 | 11 | +0.7387 | [+0.4435, +0.8865] | +0.1256 | [-0.1785, +0.2851] |
| en | 570 | 190 | +0.8168 | [+0.7788, +0.8501] | 30 | 10 | +0.7269 | [+0.4889, +0.9088] | -0.0899 | [-0.3390, +0.0919] |
| es | 593 | 208 | +0.6670 | [+0.6221, +0.7073] | 30 | 10 | +0.7203 | [+0.4627, +0.8726] | +0.0533 | [-0.2070, +0.2074] |
| fil | 570 | 555 | +0.4000 | [+0.3285, +0.4661] | 30 | 30 | +0.6010 | [+0.3529, +0.8242] | +0.2010 | [-0.0562, +0.4357] |
| fr | 569 | 191 | +0.5397 | [+0.4721, +0.6001] | 30 | 11 | +0.4008 | [+0.0296, +0.6565] | -0.1388 | [-0.5051, +0.1300] |
| it | 570 | 192 | +0.5925 | [+0.5329, +0.6525] | 30 | 10 | +0.6368 | [+0.3710, +0.8187] | +0.0443 | [-0.2311, +0.2382] |
| ja | 570 | 190 | +0.3295 | [+0.2574, +0.3991] | 30 | 10 | +0.3608 | [-0.0003, +0.6196] | +0.0314 | [-0.3367, +0.2908] |
| pt | 567 | 562 | +0.7464 | [+0.7049, +0.7866] | 30 | 30 | +0.7743 | [+0.5981, +0.9005] | +0.0279 | [-0.1548, +0.1561] |
| si | 600 | 578 | +0.2430 | [+0.1798, +0.3103] | 30 | 30 | +0.0392 | [-0.3452, +0.5186] | -0.2038 | [-0.5995, +0.2750] |
| **medie** | | | **+0.5349** | | | | **+0.5434** | | **+0.0086** | |

**Δ split mediu +0.0086**, sd intre limbi 0.1211, interval -0.2038 pana la +0.2010. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4354 | +0.2407 | -0.1947 |
| de | +0.7387 | +0.7427 | +0.0040 |
| en | +0.7269 | +0.7245 | -0.0024 |
| es | +0.7203 | +0.7268 | +0.0065 |
| fil | +0.6010 | +0.6164 | +0.0154 |
| fr | +0.4008 | +0.3614 | -0.0394 |
| it | +0.6368 | +0.6310 | -0.0058 |
| ja | +0.3608 | +0.2755 | -0.0853 |
| pt | +0.7743 | +0.7760 | +0.0017 |
| si | +0.0392 | +0.1838 | +0.1446 |

**Diferenta medie -0.0155**, interval -0.1947 pana la +0.1446.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4086 | +0.2192 | -0.0078 | +0.2162 |
| de | +0.6318 | +0.7874 | -0.0187 | -0.0487 |
| en | +0.7954 | +0.7052 | +0.0214 | +0.0217 |
| es | +0.6695 | +0.7015 | -0.0025 | +0.0188 |
| fil | +0.4093 | +0.5751 | -0.0093 | +0.0259 |
| fr | +0.5205 | +0.3279 | +0.0192 | +0.0729 |
| it | +0.6137 | +0.6880 | -0.0212 | -0.0512 |
| ja | +0.5960 | +0.4995 | -0.2665 | -0.1387 |
| pt | +0.7418 | +0.7876 | +0.0046 | -0.0133 |
| si | +0.2456 | -0.0728 | -0.0026 | +0.1120 |
