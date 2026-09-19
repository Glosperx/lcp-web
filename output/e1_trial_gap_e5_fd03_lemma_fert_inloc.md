# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:50:23 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4547 | [+0.3734, +0.5305] | 30 | 11 | +0.4118 | [+0.0891, +0.6804] | -0.0428 | [-0.3850, +0.2407] |
| de | 570 | 193 | +0.5649 | [+0.5063, +0.6200] | 23 | 11 | +0.7725 | [+0.5416, +0.8915] | +0.2076 | [-0.0266, +0.3494] |
| en | 570 | 190 | +0.7995 | [+0.7642, +0.8324] | 30 | 10 | +0.7042 | [+0.4000, +0.8771] | -0.0953 | [-0.4125, +0.0816] |
| es | 593 | 208 | +0.6896 | [+0.6460, +0.7277] | 30 | 10 | +0.7088 | [+0.4049, +0.8962] | +0.0192 | [-0.2804, +0.2133] |
| fil | 570 | 555 | +0.4177 | [+0.3510, +0.4828] | 30 | 30 | +0.5435 | [+0.2801, +0.7433] | +0.1259 | [-0.1393, +0.3428] |
| fr | 569 | 191 | +0.5432 | [+0.4820, +0.6034] | 30 | 11 | +0.4020 | [+0.1549, +0.6151] | -0.1412 | [-0.3967, +0.0776] |
| it | 570 | 192 | +0.5777 | [+0.5254, +0.6328] | 30 | 10 | +0.6698 | [+0.4405, +0.8252] | +0.0921 | [-0.1401, +0.2636] |
| ja | 570 | 190 | +0.5797 | [+0.5106, +0.6451] | 30 | 10 | +0.6652 | [+0.4364, +0.8193] | +0.0855 | [-0.1583, +0.2537] |
| pt | 567 | 562 | +0.7415 | [+0.6940, +0.7816] | 30 | 30 | +0.7257 | [+0.5415, +0.8661] | -0.0158 | [-0.2055, +0.1280] |
| si | 600 | 578 | +0.2517 | [+0.1913, +0.3080] | 30 | 30 | +0.2558 | [-0.0284, +0.5381] | +0.0042 | [-0.2844, +0.2979] |
| **medie** | | | **+0.5620** | | | | **+0.5859** | | **+0.0239** | |

**Δ split mediu +0.0239**, sd intre limbi 0.1057, interval -0.1412 pana la +0.2076. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4118 | +0.3995 | -0.0123 |
| de | +0.7725 | +0.7574 | -0.0151 |
| en | +0.7042 | +0.7253 | +0.0211 |
| es | +0.7088 | +0.6948 | -0.0140 |
| fil | +0.5435 | +0.5566 | +0.0131 |
| fr | +0.4020 | +0.3968 | -0.0052 |
| it | +0.6698 | +0.6663 | -0.0035 |
| ja | +0.6652 | +0.6608 | -0.0044 |
| pt | +0.7257 | +0.7189 | -0.0068 |
| si | +0.2558 | +0.2781 | +0.0223 |

**Diferenta medie -0.0005**, interval -0.0151 pana la +0.0223.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4143 | +0.5080 | +0.0404 | -0.0962 |
| de | +0.5592 | +0.7625 | +0.0057 | +0.0100 |
| en | +0.7913 | +0.6394 | +0.0082 | +0.0648 |
| es | +0.6877 | +0.7416 | +0.0019 | -0.0328 |
| fil | +0.3821 | +0.5336 | +0.0356 | +0.0099 |
| fr | +0.5243 | +0.3050 | +0.0189 | +0.0970 |
| it | +0.5697 | +0.6891 | +0.0080 | -0.0193 |
| ja | +0.5450 | +0.5798 | +0.0347 | +0.0854 |
| pt | +0.7415 | +0.7329 | +0.0000 | -0.0072 |
| si | +0.2181 | +0.2601 | +0.0336 | -0.0043 |
