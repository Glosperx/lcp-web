# Fuziunea A plus B, brat `lolo`, pondere potrivita pe test

Generat 2026-08-18 13:17:46 de `fuse_ab.py --arm lolo --fit test`. Date brute: `output/fusion_lolo_fittest_lemma.csv`, predictii per instanta in `output/fusion_preds_lolo_fittest_lemma.csv`.

Ponderea w e aleasa leave-one-language-out pe TESTUL celorlalte 9 limbi, apoi aplicata pe testul limbii L. Nu vede limba L, pe niciun split. Acelasi protocol pe care il foloseste deja bratul A, antrenat pe etichetele de test ale celorlalte 9 limbi la `finetune_xlmr.py:446`. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.35 | +0.4470 | +0.4829 | **+0.5305** | [+0.4670, +0.5889] | +0.0835 | [+0.0271, +0.1419] | +0.0475 | [+0.0178, +0.0764] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.30 | +0.6551 | +0.6544 | **+0.7160** | [+0.6767, +0.7539] | +0.0608 | [+0.0241, +0.1015] | +0.0615 | [+0.0457, +0.0780] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.35 | +0.8147 | +0.8377 | **+0.8674** | [+0.8393, +0.8916] | +0.0527 | [+0.0314, +0.0773] | +0.0296 | [+0.0180, +0.0428] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.35 | +0.6686 | +0.7432 | **+0.7531** | [+0.7149, +0.7882] | +0.0845 | [+0.0584, +0.1112] | +0.0100 | [-0.0027, +0.0232] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.35 | +0.4091 | +0.5190 | **+0.5186** | [+0.4531, +0.5802] | +0.1094 | [+0.0701, +0.1494] | -0.0004 | [-0.0200, +0.0209] |
| fr | `qwen35-9b-8bit` | 566 | 191 | 0.35 | +0.5305 | +0.5440 | **+0.5823** | [+0.5284, +0.6348] | +0.0517 | [+0.0112, +0.0963] | +0.0382 | [+0.0148, +0.0624] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.35 | +0.6336 | +0.6106 | **+0.6565** | [+0.6106, +0.7021] | +0.0229 | [-0.0074, +0.0538] | +0.0459 | [+0.0286, +0.0636] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.40 | +0.4890 | +0.7676 | **+0.7616** | [+0.7163, +0.7993] | +0.2727 | [+0.2277, +0.3221] | -0.0060 | [-0.0288, +0.0157] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.35 | +0.7705 | +0.8222 | **+0.8388** | [+0.8053, +0.8659] | +0.0683 | [+0.0452, +0.0921] | +0.0166 | [+0.0050, +0.0286] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.35 | +0.2119 | +0.3407 | **+0.3430** | [+0.2933, +0.3951] | +0.1311 | [+0.0827, +0.1807] | +0.0023 | [-0.0237, +0.0285] |
| **medie** | | | | 0.35 | +0.5630 | +0.6322 | **+0.6568** | | +0.0938 | | +0.0245 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 6 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5630 |
| semnalul B singur, `lolo` | 0.6322 |
| **fuziunea A plus B, w ales LOLO pe test** | **0.6568** |

Fata de cel mai bun reper publicat, 0.6571: **-0.0003**. Nu trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.35 | +0.5759 | +0.6725 | 0.0966 |
| de | 0.30 | +0.5528 | +0.6512 | 0.0984 |
| en | 0.35 | +0.5350 | +0.6351 | 0.1001 |
| es | 0.35 | +0.5513 | +0.6477 | 0.0964 |
| fil | 0.35 | +0.5801 | +0.6812 | 0.1011 |
| fr | 0.35 | +0.5666 | +0.6667 | 0.1001 |
| it | 0.35 | +0.5551 | +0.6585 | 0.1034 |
| ja | 0.40 | +0.5712 | +0.6461 | 0.0749 |
| pt | 0.35 | +0.5399 | +0.6382 | 0.0983 |
| si | 0.35 | +0.6020 | +0.7007 | 0.0987 |

## Limba tinuta deoparte nu e folosita nicaieri. Unde e garantat, linie cu linie

| ce se alege | unde | cum |
|---|---|---|
| semnalul A | `finetune_xlmr.py:444-446` | `te, tr = (lang == L), (lang != L)`, apoi `Xtr = np.vstack([Xen, Xml[tr]])`. Randurile de test ale lui L sunt in afara antrenarii. |
| tot A, pe trial | `finetune_xlmr.py:449-450` | trial-ul lui L intra doar in `Xpred`, niciodata in `Xtr`. |
| modelul lui B | `fuse_ab.py`, `load_signals` | `pick_model(tab_trial, set(exclude) \| {lg})`: limba pentru care se alege intra chiar ea in multimea exclusa. |
| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_weight` | apelul cu `exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. Fara asta w(L) ar vedea limba L prin modelul ales pentru L'. |
| ponderea w | `fuse_ab.py`, `fit_weight` | `others = [d for l2, d in fit.items() if l2 != lg]`. Curba nu contine niciun rand al lui L, pe niciun split. |
| standardizarea | `fuse_ab.py`, `zscore` | media si deviatia se iau din predictii, nu din etichete. |

Si unde **nu** e garantata, fiindca trebuie scris tot: `zA` pentru o limba de potrivire L' vine din iteratia L' a lui `frozen_trial_gap`, adica dintr-un model antrenat pe toate limbile in afara de L'. Acel model a inclus randurile de test ale lui L. Ponderea lui L depinde deci indirect de etichetele lui L, prin predictiile lui A pe alte limbi.

Dependenta asta e **identica la potrivirea pe trial si la cea pe test**, fiindca ambele folosesc aceleasi predictii A din `output/e1_frozen_preds.csv`. Trecerea la potrivirea pe test nu adauga nimic si nu inrautateste nimic. Marimea efectului ramane **neverificata**; ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L, si L', adica 90 de potriviri `blend_ridge_hgb` in loc de 10, deci o rulare separata cu aprobare.

### Filtrul de disponibilitate

Selectia imbricata poate cere un model care nu a fost rulat pe limba de potrivire, pe splitul de potrivire. Candidatii se restrang atunci la modelele masurate efectiv acolo. Restrangerea se uita la ACOPERIRE, nu la scor, deci nu introduce nicio eticheta. Cazurile, toate:

| split de potrivire | limba tinuta deoparte | limba de potrivire | cerut | folosit |
|---|---|---|---|---|
| test | fr | ca | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | de | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | en | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | es | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | it | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | ja | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | pt | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
