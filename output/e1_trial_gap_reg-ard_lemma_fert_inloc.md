# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:27:46 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3323 | [+0.2416, +0.4141] | 30 | 11 | +0.3496 | [-0.0402, +0.5996] | +0.0173 | [-0.3673, +0.2878] |
| de | 570 | 193 | +0.6082 | [+0.5558, +0.6581] | 23 | 11 | +0.8391 | [+0.5920, +0.9391] | +0.2309 | [-0.0241, +0.3467] |
| en | 570 | 190 | +0.7472 | [+0.7068, +0.7830] | 30 | 10 | +0.6268 | [+0.4096, +0.7756] | -0.1205 | [-0.3469, +0.0349] |
| es | 593 | 208 | +0.6260 | [+0.5757, +0.6728] | 30 | 10 | +0.5976 | [+0.2745, +0.8398] | -0.0284 | [-0.3682, +0.2207] |
| fil | 570 | 555 | +0.3879 | [+0.3171, +0.4582] | 30 | 30 | +0.6175 | [+0.4488, +0.7928] | +0.2296 | [+0.0540, +0.4232] |
| fr | 569 | 191 | +0.5503 | [+0.4900, +0.6059] | 30 | 11 | +0.3585 | [-0.0236, +0.6478] | -0.1917 | [-0.5863, +0.1008] |
| it | 570 | 192 | +0.6131 | [+0.5574, +0.6636] | 30 | 10 | +0.6157 | [+0.4065, +0.7988] | +0.0026 | [-0.2147, +0.1945] |
| ja | 570 | 190 | +0.5735 | [+0.5032, +0.6386] | 30 | 10 | +0.5843 | [+0.3216, +0.7667] | +0.0108 | [-0.2602, +0.2075] |
| pt | 567 | 562 | +0.7343 | [+0.6980, +0.7675] | 30 | 30 | +0.7632 | [+0.5616, +0.9078] | +0.0289 | [-0.1669, +0.1767] |
| si | 600 | 578 | +0.0472 | [-0.0378, +0.1341] | 30 | 30 | -0.1559 | [-0.3749, +0.0916] | -0.2031 | [-0.4422, +0.0526] |
| **medie** | | | **+0.5220** | | | | **+0.5196** | | **-0.0024** | |

**Δ split mediu -0.0024**, sd intre limbi 0.1493, interval -0.2031 pana la +0.2309. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3496 | +0.3496 | +0.0000 |
| de | +0.8391 | +0.8391 | +0.0000 |
| en | +0.6268 | +0.6268 | +0.0000 |
| es | +0.5976 | +0.5976 | +0.0000 |
| fil | +0.6175 | +0.6175 | +0.0000 |
| fr | +0.3585 | +0.3585 | +0.0000 |
| it | +0.6157 | +0.6157 | +0.0000 |
| ja | +0.5843 | +0.5843 | +0.0000 |
| pt | +0.7632 | +0.7632 | +0.0000 |
| si | -0.1559 | -0.1559 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3194 | +0.2704 | +0.0129 | +0.0792 |
| de | +0.6208 | +0.8201 | -0.0126 | +0.0190 |
| en | +0.7372 | +0.6087 | +0.0100 | +0.0181 |
| es | +0.6066 | +0.5723 | +0.0194 | +0.0253 |
| fil | +0.3880 | +0.6175 | -0.0001 | +0.0000 |
| fr | +0.5491 | +0.3369 | +0.0012 | +0.0216 |
| it | +0.6029 | +0.6149 | +0.0102 | +0.0008 |
| ja | +0.5382 | +0.5734 | +0.0353 | +0.0109 |
| pt | +0.7353 | +0.7357 | -0.0010 | +0.0275 |
| si | +nan | +nan | +nan | +nan |
