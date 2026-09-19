# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 12:40:54 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4167 | [+0.3300, +0.4975] | 30 | 11 | +0.1641 | [-0.2717, +0.5898] | -0.2526 | [-0.6944, +0.1834] |
| de | 570 | 193 | +0.6151 | [+0.5573, +0.6685] | 23 | 11 | +0.7362 | [+0.4956, +0.8477] | +0.1211 | [-0.1322, +0.2452] |
| en | 570 | 190 | +0.7719 | [+0.7286, +0.8083] | 30 | 10 | +0.6634 | [+0.4223, +0.7983] | -0.1085 | [-0.3504, +0.0397] |
| es | 593 | 208 | +0.6227 | [+0.5704, +0.6680] | 30 | 10 | +0.6070 | [+0.2556, +0.7951] | -0.0157 | [-0.3671, +0.1839] |
| fil | 570 | 555 | +0.3962 | [+0.3258, +0.4630] | 30 | 30 | +0.5777 | [+0.3334, +0.7414] | +0.1815 | [-0.0791, +0.3621] |
| fr | 569 | 191 | +0.4960 | [+0.4318, +0.5564] | 30 | 11 | +0.2323 | [-0.1612, +0.5867] | -0.2638 | [-0.6783, +0.0944] |
| it | 570 | 192 | +0.6079 | [+0.5531, +0.6620] | 30 | 10 | +0.5954 | [+0.3592, +0.7891] | -0.0125 | [-0.2545, +0.1917] |
| ja | 570 | 190 | +0.6068 | [+0.5468, +0.6621] | 30 | 10 | +0.5876 | [+0.4263, +0.6927] | -0.0192 | [-0.1895, +0.0998] |
| pt | 567 | 562 | +0.7253 | [+0.6793, +0.7650] | 30 | 30 | +0.7798 | [+0.6138, +0.9035] | +0.0544 | [-0.1165, +0.1824] |
| si | 600 | 578 | +0.2609 | [+0.1989, +0.3249] | 30 | 30 | +0.0367 | [-0.3296, +0.4701] | -0.2242 | [-0.5998, +0.2146] |
| **medie** | | | **+0.5520** | | | | **+0.4980** | | **-0.0540** | |

**Δ split mediu -0.0540**, sd intre limbi 0.1555, interval -0.2638 pana la +0.1815. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1641 | +0.1641 | +0.0000 |
| de | +0.7362 | +0.7362 | +0.0000 |
| en | +0.6634 | +0.6634 | +0.0000 |
| es | +0.6070 | +0.6070 | +0.0000 |
| fil | +0.5777 | +0.5777 | +0.0000 |
| fr | +0.2323 | +0.2323 | +0.0000 |
| it | +0.5954 | +0.5954 | +0.0000 |
| ja | +0.5876 | +0.5876 | +0.0000 |
| pt | +0.7798 | +0.7798 | +0.0000 |
| si | +0.0367 | +0.0367 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3832 | +0.1547 | +0.0335 | +0.0094 |
| de | +0.6286 | +0.7935 | -0.0135 | -0.0573 |
| en | +0.7687 | +0.6158 | +0.0032 | +0.0476 |
| es | +0.6068 | +0.6699 | +0.0159 | -0.0629 |
| fil | +0.4088 | +0.5142 | -0.0126 | +0.0635 |
| fr | +0.4856 | +0.2468 | +0.0104 | -0.0145 |
| it | +0.5913 | +0.5866 | +0.0166 | +0.0088 |
| ja | +0.5525 | +0.4113 | +0.0543 | +0.1763 |
| pt | +0.7331 | +0.7816 | -0.0078 | -0.0018 |
| si | +0.2731 | +0.0655 | -0.0122 | -0.0288 |
