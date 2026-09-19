# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-19 01:22:03 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4802 | [+0.4084, +0.5441] | 30 | 11 | +0.4920 | [+0.1506, +0.7593] | +0.0118 | [-0.3338, +0.2893] |
| de | 570 | 193 | +0.6568 | [+0.6091, +0.7007] | 23 | 11 | +0.8146 | [+0.5587, +0.9308] | +0.1579 | [-0.1175, +0.2846] |
| en | 570 | 190 | +0.8208 | [+0.7872, +0.8504] | 30 | 10 | +0.7297 | [+0.5557, +0.8577] | -0.0910 | [-0.2663, +0.0428] |
| es | 593 | 208 | +0.6654 | [+0.6196, +0.7070] | 30 | 10 | +0.6504 | [+0.3184, +0.8422] | -0.0150 | [-0.3484, +0.1791] |
| fil | 570 | 555 | +0.3570 | [+0.2877, +0.4263] | 30 | 30 | +0.6293 | [+0.3760, +0.7959] | +0.2724 | [+0.0114, +0.4534] |
| fr | 569 | 191 | +0.5784 | [+0.5190, +0.6335] | 30 | 11 | +0.3308 | [+0.0128, +0.5837] | -0.2476 | [-0.5694, +0.0183] |
| it | 570 | 192 | +0.6191 | [+0.5597, +0.6745] | 30 | 10 | +0.7304 | [+0.5696, +0.8480] | +0.1114 | [-0.0525, +0.2435] |
| ja | 570 | 190 | +0.6133 | [+0.5534, +0.6651] | 30 | 10 | +0.5665 | [+0.2927, +0.7473] | -0.0468 | [-0.3252, +0.1448] |
| pt | 567 | 562 | +0.7709 | [+0.7279, +0.8091] | 30 | 30 | +0.7398 | [+0.5656, +0.8546] | -0.0311 | [-0.2103, +0.0891] |
| si | 600 | 578 | +0.2719 | [+0.2021, +0.3408] | 30 | 30 | -0.0152 | [-0.2832, +0.3368] | -0.2872 | [-0.5618, +0.0756] |
| **medie** | | | **+0.5834** | | | | **+0.5668** | | **-0.0165** | |

**Δ split mediu -0.0165**, sd intre limbi 0.1714, interval -0.2872 pana la +0.2724. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4920 | +0.5084 | +0.0164 |
| de | +0.8146 | +0.8196 | +0.0050 |
| en | +0.7297 | +0.7416 | +0.0119 |
| es | +0.6504 | +0.6571 | +0.0067 |
| fil | +0.6293 | +0.6362 | +0.0069 |
| fr | +0.3308 | +0.2830 | -0.0478 |
| it | +0.7304 | +0.7348 | +0.0044 |
| ja | +0.5665 | +0.5772 | +0.0107 |
| pt | +0.7398 | +0.7556 | +0.0158 |
| si | -0.0152 | +0.0290 | +0.0442 |

**Diferenta medie +0.0074**, interval -0.0478 pana la +0.0442.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4666 | +0.4404 | +0.0136 | +0.0516 |
| de | +0.6808 | +0.8420 | -0.0240 | -0.0274 |
| en | +0.8207 | +0.7416 | +0.0001 | -0.0119 |
| es | +0.6456 | +0.7267 | +0.0198 | -0.0763 |
| fil | +0.3712 | +0.5848 | -0.0142 | +0.0445 |
| fr | +0.5456 | +0.2018 | +0.0328 | +0.1290 |
| it | +0.6274 | +0.7211 | -0.0083 | +0.0093 |
| ja | +0.6275 | +0.5517 | -0.0142 | +0.0148 |
| pt | +0.7692 | +0.7943 | +0.0017 | -0.0545 |
| si | +0.2572 | +0.0009 | +0.0147 | -0.0161 |
