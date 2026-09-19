# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 11:58:31 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4310 | [+0.3483, +0.5052] | 30 | 11 | +0.3698 | [-0.1027, +0.6976] | -0.0612 | [-0.5341, +0.2876] |
| de | 570 | 193 | +0.6561 | [+0.6031, +0.7036] | 23 | 11 | +0.7449 | [+0.5372, +0.8347] | +0.0888 | [-0.1335, +0.1922] |
| en | 570 | 190 | +0.8117 | [+0.7745, +0.8432] | 30 | 10 | +0.7103 | [+0.4772, +0.8442] | -0.1013 | [-0.3505, +0.0394] |
| es | 593 | 208 | +0.6749 | [+0.6280, +0.7164] | 30 | 10 | +0.6876 | [+0.3552, +0.8791] | +0.0127 | [-0.3161, +0.2084] |
| fil | 570 | 555 | +0.4075 | [+0.3361, +0.4750] | 30 | 30 | +0.5930 | [+0.3665, +0.7820] | +0.1855 | [-0.0506, +0.3902] |
| fr | 569 | 191 | +0.5431 | [+0.4768, +0.6045] | 30 | 11 | +0.3278 | [-0.0766, +0.6320] | -0.2153 | [-0.6278, +0.1038] |
| it | 570 | 192 | +0.6283 | [+0.5742, +0.6809] | 30 | 10 | +0.6841 | [+0.4632, +0.8377] | +0.0558 | [-0.1714, +0.2265] |
| ja | 570 | 190 | +0.5907 | [+0.5277, +0.6466] | 30 | 10 | +0.4958 | [+0.2485, +0.6666] | -0.0949 | [-0.3469, +0.0860] |
| pt | 567 | 562 | +0.7616 | [+0.7199, +0.7993] | 30 | 30 | +0.7997 | [+0.6345, +0.9098] | +0.0381 | [-0.1336, +0.1576] |
| si | 600 | 578 | +0.2915 | [+0.2283, +0.3549] | 30 | 30 | +0.0391 | [-0.3547, +0.4645] | -0.2524 | [-0.6553, +0.1801] |
| **medie** | | | **+0.5796** | | | | **+0.5452** | | **-0.0344** | |

**Δ split mediu -0.0344**, sd intre limbi 0.1367, interval -0.2524 pana la +0.1855. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3698 | +0.3173 | -0.0525 |
| de | +0.7449 | +0.7614 | +0.0165 |
| en | +0.7103 | +0.7226 | +0.0123 |
| es | +0.6876 | +0.6910 | +0.0034 |
| fil | +0.5930 | +0.5954 | +0.0024 |
| fr | +0.3278 | +0.3098 | -0.0180 |
| it | +0.6841 | +0.6891 | +0.0050 |
| ja | +0.4958 | +0.4890 | -0.0068 |
| pt | +0.7997 | +0.8018 | +0.0021 |
| si | +0.0391 | +0.0753 | +0.0362 |

**Diferenta medie +0.0001**, interval -0.0525 pana la +0.0362.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4018 | +0.3113 | +0.0292 | +0.0585 |
| de | +0.6610 | +0.8220 | -0.0049 | -0.0771 |
| en | +0.8061 | +0.6433 | +0.0056 | +0.0670 |
| es | +0.6428 | +0.6572 | +0.0321 | +0.0304 |
| fil | +0.4093 | +0.5068 | -0.0018 | +0.0862 |
| fr | +0.5328 | +0.3948 | +0.0103 | -0.0670 |
| it | +0.6207 | +0.6640 | +0.0076 | +0.0201 |
| ja | +0.5849 | +0.4056 | +0.0058 | +0.0902 |
| pt | +0.7604 | +0.8267 | +0.0012 | -0.0270 |
| si | +0.2319 | -0.0131 | +0.0596 | +0.0522 |
