# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:59:55 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4616 | [+0.3758, +0.5401] | 30 | 11 | +0.3884 | [+0.0723, +0.6383] | -0.0732 | [-0.4016, +0.1995] |
| de | 570 | 193 | +0.5695 | [+0.5100, +0.6247] | 23 | 11 | +0.7957 | [+0.4820, +0.9239] | +0.2262 | [-0.0964, +0.3688] |
| en | 570 | 190 | +0.7839 | [+0.7462, +0.8177] | 30 | 10 | +0.6654 | [+0.5520, +0.8077] | -0.1185 | [-0.2370, +0.0320] |
| es | 593 | 208 | +0.6466 | [+0.5977, +0.6909] | 30 | 10 | +0.6969 | [+0.5087, +0.8365] | +0.0503 | [-0.1411, +0.1963] |
| fil | 570 | 555 | +0.4013 | [+0.3299, +0.4695] | 30 | 30 | +0.4810 | [+0.2134, +0.6872] | +0.0797 | [-0.1891, +0.3097] |
| fr | 569 | 191 | +0.5327 | [+0.4715, +0.5902] | 30 | 11 | +0.5237 | [+0.3019, +0.6980] | -0.0090 | [-0.2300, +0.1728] |
| it | 570 | 192 | +0.5894 | [+0.5350, +0.6443] | 30 | 10 | +0.6849 | [+0.4796, +0.8247] | +0.0955 | [-0.1156, +0.2522] |
| ja | 570 | 190 | +0.5661 | [+0.4926, +0.6329] | 30 | 10 | +0.6647 | [+0.3868, +0.8177] | +0.0987 | [-0.1871, +0.2683] |
| pt | 567 | 562 | +0.7241 | [+0.6809, +0.7618] | 30 | 30 | +0.7008 | [+0.4871, +0.8845] | -0.0234 | [-0.2401, +0.1601] |
| si | 600 | 578 | +0.3563 | [+0.2850, +0.4249] | 30 | 30 | +0.2923 | [-0.2042, +0.5889] | -0.0641 | [-0.5633, +0.2374] |
| **medie** | | | **+0.5632** | | | | **+0.5894** | | **+0.0262** | |

**Δ split mediu +0.0262**, sd intre limbi 0.1034, interval -0.1185 pana la +0.2262. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3884 | +0.3884 | +0.0000 |
| de | +0.7957 | +0.7957 | +0.0000 |
| en | +0.6654 | +0.6654 | +0.0000 |
| es | +0.6969 | +0.6969 | +0.0000 |
| fil | +0.4810 | +0.4810 | +0.0000 |
| fr | +0.5237 | +0.5237 | +0.0000 |
| it | +0.6849 | +0.6849 | +0.0000 |
| ja | +0.6647 | +0.6647 | +0.0000 |
| pt | +0.7008 | +0.7008 | +0.0000 |
| si | +0.2923 | +0.2923 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4315 | +0.4810 | +0.0301 | -0.0926 |
| de | +0.6293 | +0.8503 | -0.0598 | -0.0546 |
| en | +0.7839 | +0.6772 | +0.0000 | -0.0118 |
| es | +0.6686 | +0.6195 | -0.0220 | +0.0774 |
| fil | +0.4192 | +0.5133 | -0.0179 | -0.0323 |
| fr | +0.4883 | +0.4014 | +0.0444 | +0.1223 |
| it | +0.5940 | +0.6904 | -0.0046 | -0.0055 |
| ja | +0.5481 | +0.5620 | +0.0180 | +0.1027 |
| pt | +0.7321 | +0.7396 | -0.0080 | -0.0388 |
| si | +0.3156 | +0.3100 | +0.0407 | -0.0177 |
