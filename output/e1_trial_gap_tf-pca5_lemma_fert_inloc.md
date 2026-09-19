# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:01:17 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4252 | [+0.3402, +0.4998] | 30 | 11 | +0.2763 | [-0.1686, +0.6319] | -0.1490 | [-0.5933, +0.2177] |
| de | 570 | 193 | +0.6033 | [+0.5484, +0.6556] | 23 | 11 | +0.7488 | [+0.4981, +0.9197] | +0.1455 | [-0.1191, +0.3275] |
| en | 570 | 190 | +0.7939 | [+0.7519, +0.8291] | 30 | 10 | +0.6790 | [+0.4088, +0.8053] | -0.1149 | [-0.3885, +0.0233] |
| es | 593 | 208 | +0.6569 | [+0.6104, +0.6970] | 30 | 10 | +0.6393 | [+0.3068, +0.8382] | -0.0175 | [-0.3437, +0.1810] |
| fil | 570 | 555 | +0.3986 | [+0.3276, +0.4670] | 30 | 30 | +0.6419 | [+0.4631, +0.8064] | +0.2433 | [+0.0522, +0.4243] |
| fr | 569 | 191 | +0.5252 | [+0.4557, +0.5864] | 30 | 11 | +0.2910 | [-0.1097, +0.5868] | -0.2342 | [-0.6293, +0.0792] |
| it | 570 | 192 | +0.6084 | [+0.5558, +0.6617] | 30 | 10 | +0.6187 | [+0.4394, +0.7827] | +0.0102 | [-0.1810, +0.1877] |
| ja | 570 | 190 | +0.5496 | [+0.4892, +0.6077] | 30 | 10 | +0.6469 | [+0.3990, +0.7924] | +0.0972 | [-0.1527, +0.2505] |
| pt | 567 | 562 | +0.7491 | [+0.7084, +0.7880] | 30 | 30 | +0.7879 | [+0.6207, +0.9069] | +0.0389 | [-0.1316, +0.1646] |
| si | 600 | 578 | +0.1373 | [+0.0664, +0.2090] | 30 | 30 | -0.1425 | [-0.5186, +0.3162] | -0.2797 | [-0.6613, +0.1860] |
| **medie** | | | **+0.5447** | | | | **+0.5187** | | **-0.0260** | |

**Δ split mediu -0.0260**, sd intre limbi 0.1678, interval -0.2797 pana la +0.2433. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2763 | +0.2412 | -0.0351 |
| de | +0.7488 | +0.7537 | +0.0049 |
| en | +0.6790 | +0.6784 | -0.0006 |
| es | +0.6393 | +0.6318 | -0.0075 |
| fil | +0.6419 | +0.6464 | +0.0045 |
| fr | +0.2910 | +0.2581 | -0.0329 |
| it | +0.6187 | +0.6251 | +0.0064 |
| ja | +0.6469 | +0.6442 | -0.0027 |
| pt | +0.7879 | +0.7860 | -0.0019 |
| si | -0.1425 | -0.0796 | +0.0629 |

**Diferenta medie -0.0002**, interval -0.0351 pana la +0.0629.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3724 | +0.2075 | +0.0528 | +0.0688 |
| de | +0.6146 | +0.8055 | -0.0113 | -0.0567 |
| en | +0.7671 | +0.6622 | +0.0268 | +0.0168 |
| es | +0.5575 | +0.6019 | +0.0994 | +0.0374 |
| fil | +0.3943 | +0.5520 | +0.0043 | +0.0899 |
| fr | +0.5249 | +0.3154 | +0.0003 | -0.0244 |
| it | +0.5597 | +0.5988 | +0.0487 | +0.0199 |
| ja | +0.5328 | +0.5449 | +0.0168 | +0.1020 |
| pt | +0.7508 | +0.7737 | -0.0017 | +0.0142 |
| si | +0.0085 | -0.0408 | +0.1288 | -0.1017 |
