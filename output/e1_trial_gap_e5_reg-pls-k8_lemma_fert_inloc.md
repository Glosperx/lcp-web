# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:22:21 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3946 | [+0.2982, +0.4837] | 30 | 11 | +0.3340 | [+0.0398, +0.6024] | -0.0606 | [-0.3753, +0.2216] |
| de | 570 | 193 | +0.5570 | [+0.4959, +0.6137] | 23 | 11 | +0.8003 | [+0.5589, +0.9258] | +0.2433 | [-0.0017, +0.3851] |
| en | 570 | 190 | +0.7649 | [+0.7241, +0.8024] | 30 | 10 | +0.6516 | [+0.3684, +0.8779] | -0.1133 | [-0.4018, +0.1170] |
| es | 593 | 208 | +0.6513 | [+0.6013, +0.6946] | 30 | 10 | +0.6381 | [+0.2818, +0.8580] | -0.0132 | [-0.3687, +0.2187] |
| fil | 570 | 555 | +0.4320 | [+0.3627, +0.4964] | 30 | 30 | +0.5606 | [+0.3037, +0.7581] | +0.1286 | [-0.1303, +0.3372] |
| fr | 569 | 191 | +0.5364 | [+0.4752, +0.5986] | 30 | 11 | +0.3142 | [+0.0957, +0.5081] | -0.2222 | [-0.4447, -0.0199] |
| it | 570 | 192 | +0.5661 | [+0.5129, +0.6214] | 30 | 10 | +0.5992 | [+0.3349, +0.8100] | +0.0331 | [-0.2392, +0.2562] |
| ja | 570 | 190 | +0.5807 | [+0.5118, +0.6447] | 30 | 10 | +0.7086 | [+0.4872, +0.8448] | +0.1280 | [-0.1017, +0.2845] |
| pt | 567 | 562 | +0.7098 | [+0.6602, +0.7531] | 30 | 30 | +0.6499 | [+0.4179, +0.8262] | -0.0598 | [-0.2958, +0.1197] |
| si | 600 | 578 | +0.2053 | [+0.1393, +0.2751] | 30 | 30 | +0.3946 | [+0.1102, +0.6129] | +0.1893 | [-0.1084, +0.4108] |
| **medie** | | | **+0.5398** | | | | **+0.5651** | | **+0.0253** | |

**Δ split mediu +0.0253**, sd intre limbi 0.1462, interval -0.2222 pana la +0.2433. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3340 | +0.3340 | +0.0000 |
| de | +0.8003 | +0.8003 | +0.0000 |
| en | +0.6516 | +0.6516 | +0.0000 |
| es | +0.6381 | +0.6381 | +0.0000 |
| fil | +0.5606 | +0.5606 | +0.0000 |
| fr | +0.3142 | +0.3142 | +0.0000 |
| it | +0.5992 | +0.5992 | +0.0000 |
| ja | +0.7086 | +0.7086 | +0.0000 |
| pt | +0.6499 | +0.6499 | +0.0000 |
| si | +0.3946 | +0.3946 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4103 | +0.5090 | -0.0157 | -0.1750 |
| de | +0.5909 | +0.8201 | -0.0339 | -0.0198 |
| en | +0.7686 | +0.6142 | -0.0037 | +0.0374 |
| es | +0.6593 | +0.6361 | -0.0080 | +0.0020 |
| fil | +0.4147 | +0.5660 | +0.0173 | -0.0054 |
| fr | +0.4881 | +0.2639 | +0.0483 | +0.0503 |
| it | +0.5843 | +0.6668 | -0.0182 | -0.0676 |
| ja | +0.4981 | +0.5518 | +0.0826 | +0.1568 |
| pt | +0.7324 | +0.6527 | -0.0226 | -0.0028 |
| si | +0.1897 | +0.3170 | +0.0156 | +0.0776 |
