# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:01:59 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4316 | [+0.3533, +0.5040] | 30 | 11 | +0.2143 | [-0.3183, +0.6352] | -0.2174 | [-0.7560, +0.2121] |
| de | 570 | 193 | +0.6409 | [+0.5872, +0.6904] | 23 | 11 | +0.7974 | [+0.5339, +0.9156] | +0.1565 | [-0.1174, +0.2912] |
| en | 570 | 190 | +0.8062 | [+0.7679, +0.8393] | 30 | 10 | +0.7006 | [+0.4317, +0.8356] | -0.1056 | [-0.3749, +0.0411] |
| es | 593 | 208 | +0.6526 | [+0.6053, +0.6951] | 30 | 10 | +0.6733 | [+0.3886, +0.8464] | +0.0207 | [-0.2598, +0.1975] |
| fil | 570 | 555 | +0.4158 | [+0.3450, +0.4823] | 30 | 30 | +0.5893 | [+0.3578, +0.7645] | +0.1735 | [-0.0572, +0.3651] |
| fr | 569 | 191 | +0.5413 | [+0.4760, +0.6000] | 30 | 11 | +0.3693 | [-0.0311, +0.6566] | -0.1720 | [-0.5706, +0.1293] |
| it | 570 | 192 | +0.6253 | [+0.5720, +0.6784] | 30 | 10 | +0.6487 | [+0.4452, +0.8070] | +0.0234 | [-0.1962, +0.1938] |
| ja | 570 | 190 | +0.5890 | [+0.5301, +0.6433] | 30 | 10 | +0.5689 | [+0.3415, +0.7011] | -0.0201 | [-0.2522, +0.1205] |
| pt | 567 | 562 | +0.7604 | [+0.7214, +0.7967] | 30 | 30 | +0.7871 | [+0.6182, +0.9120] | +0.0267 | [-0.1439, +0.1550] |
| si | 600 | 578 | +0.2647 | [+0.2025, +0.3307] | 30 | 30 | -0.0229 | [-0.4482, +0.5159] | -0.2876 | [-0.7168, +0.2497] |
| **medie** | | | **+0.5728** | | | | **+0.5326** | | **-0.0402** | |

**Δ split mediu -0.0402**, sd intre limbi 0.1532, interval -0.2876 pana la +0.1735. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2143 | +0.1905 | -0.0238 |
| de | +0.7974 | +0.7951 | -0.0023 |
| en | +0.7006 | +0.6972 | -0.0034 |
| es | +0.6733 | +0.6879 | +0.0146 |
| fil | +0.5893 | +0.6113 | +0.0220 |
| fr | +0.3693 | +0.3564 | -0.0129 |
| it | +0.6487 | +0.6584 | +0.0097 |
| ja | +0.5689 | +0.5600 | -0.0089 |
| pt | +0.7871 | +0.7766 | -0.0105 |
| si | -0.0229 | +0.0208 | +0.0437 |

**Diferenta medie +0.0028**, interval -0.0238 pana la +0.0437.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3976 | +0.1969 | +0.0340 | +0.0174 |
| de | +0.6553 | +0.8667 | -0.0144 | -0.0693 |
| en | +0.8046 | +0.6954 | +0.0016 | +0.0052 |
| es | +0.6270 | +0.6694 | +0.0256 | +0.0039 |
| fil | +0.4160 | +0.5628 | -0.0002 | +0.0265 |
| fr | +0.5277 | +0.3170 | +0.0136 | +0.0523 |
| it | +0.6171 | +0.6595 | +0.0082 | -0.0108 |
| ja | +0.5777 | +0.4340 | +0.0113 | +0.1349 |
| pt | +0.7599 | +0.7759 | +0.0005 | +0.0112 |
| si | +0.2640 | +0.1186 | +0.0007 | -0.1415 |
