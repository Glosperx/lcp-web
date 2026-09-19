# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:37:00 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4045 | [+0.3099, +0.4867] | 30 | 11 | +0.5180 | [+0.1283, +0.7848] | +0.1135 | [-0.2978, +0.3866] |
| de | 570 | 193 | +0.6039 | [+0.5470, +0.6586] | 23 | 11 | +0.8239 | [+0.5751, +0.9392] | +0.2200 | [-0.0357, +0.3539] |
| en | 570 | 190 | +0.7776 | [+0.7417, +0.8107] | 30 | 10 | +0.6491 | [+0.5108, +0.8019] | -0.1286 | [-0.2731, +0.0290] |
| es | 593 | 208 | +0.6727 | [+0.6293, +0.7131] | 30 | 10 | +0.6505 | [+0.3550, +0.8378] | -0.0221 | [-0.3176, +0.1684] |
| fil | 570 | 555 | +0.3916 | [+0.3188, +0.4602] | 30 | 30 | +0.5517 | [+0.3281, +0.7365] | +0.1601 | [-0.0650, +0.3596] |
| fr | 569 | 191 | +0.5677 | [+0.5094, +0.6227] | 30 | 11 | +0.3453 | [+0.0273, +0.5919] | -0.2223 | [-0.5510, +0.0374] |
| it | 570 | 192 | +0.6206 | [+0.5668, +0.6696] | 30 | 10 | +0.6827 | [+0.5059, +0.8228] | +0.0621 | [-0.1236, +0.2157] |
| ja | 570 | 190 | +0.5714 | [+0.4985, +0.6398] | 30 | 10 | +0.6014 | [+0.2642, +0.8361] | +0.0299 | [-0.3176, +0.2788] |
| pt | 567 | 562 | +0.7487 | [+0.7069, +0.7850] | 30 | 30 | +0.7188 | [+0.5298, +0.8683] | -0.0299 | [-0.2320, +0.1246] |
| si | 600 | 578 | +0.2098 | [+0.1428, +0.2759] | 30 | 30 | +0.2480 | [-0.1015, +0.5627] | +0.0381 | [-0.3286, +0.3575] |
| **medie** | | | **+0.5569** | | | | **+0.5789** | | **+0.0221** | |

**Δ split mediu +0.0221**, sd intre limbi 0.1315, interval -0.2223 pana la +0.2200. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.5180 | +0.5180 | +0.0000 |
| de | +0.8239 | +0.8239 | +0.0000 |
| en | +0.6491 | +0.6491 | +0.0000 |
| es | +0.6505 | +0.6505 | +0.0000 |
| fil | +0.5517 | +0.5517 | +0.0000 |
| fr | +0.3453 | +0.3453 | +0.0000 |
| it | +0.6827 | +0.6827 | +0.0000 |
| ja | +0.6014 | +0.6014 | +0.0000 |
| pt | +0.7188 | +0.7188 | +0.0000 |
| si | +0.2480 | +0.2480 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3747 | +0.4001 | +0.0298 | +0.1179 |
| de | +0.6403 | +0.8227 | -0.0364 | +0.0012 |
| en | +0.7574 | +0.6535 | +0.0202 | -0.0044 |
| es | +0.6538 | +0.6260 | +0.0189 | +0.0245 |
| fil | +0.3832 | +0.5531 | +0.0084 | -0.0014 |
| fr | +0.5421 | +0.2679 | +0.0256 | +0.0774 |
| it | +0.6258 | +0.6749 | -0.0052 | +0.0078 |
| ja | +0.5367 | +0.5281 | +0.0347 | +0.0733 |
| pt | +0.7526 | +0.7113 | -0.0039 | +0.0075 |
| si | +0.1730 | +0.3506 | +0.0368 | -0.1026 |
