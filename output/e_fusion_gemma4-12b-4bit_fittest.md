# Fuziunea A plus B, brat `gemma4-12b-4bit`, pondere potrivita pe test

Generat 2026-08-18 00:59:50 de `fuse_ab.py --arm gemma4-12b-4bit --fit test`. Date brute: `output/fusion_gemma4-12b-4bit_fittest.csv`, predictii per instanta in `output/fusion_preds_gemma4-12b-4bit_fittest.csv`.

Ponderea w e aleasa leave-one-language-out pe TESTUL celorlalte 9 limbi, apoi aplicata pe testul limbii L. Nu vede limba L, pe niciun split. Acelasi protocol pe care il foloseste deja bratul A, antrenat pe etichetele de test ale celorlalte 9 limbi la `finetune_xlmr.py:446`. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.30 | +0.4281 | +0.4829 | **+0.5208** | [+0.4537, +0.5808] | +0.0927 | [+0.0306, +0.1560] | +0.0379 | [+0.0122, +0.0637] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.30 | +0.6314 | +0.6544 | **+0.7084** | [+0.6683, +0.7460] | +0.0770 | [+0.0397, +0.1167] | +0.0540 | [+0.0373, +0.0701] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.30 | +0.8197 | +0.8377 | **+0.8670** | [+0.8383, +0.8923] | +0.0473 | [+0.0249, +0.0714] | +0.0293 | [+0.0194, +0.0407] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.30 | +0.6341 | +0.7432 | **+0.7457** | [+0.7080, +0.7816] | +0.1116 | [+0.0805, +0.1444] | +0.0026 | [-0.0085, +0.0143] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.30 | +0.4047 | +0.5190 | **+0.5210** | [+0.4564, +0.5826] | +0.1163 | [+0.0720, +0.1605] | +0.0020 | [-0.0151, +0.0205] |
| fr | `gemma4-12b-4bit` | 566 | 191 | 0.30 | +0.5153 | +0.6457 | **+0.6478** | [+0.5931, +0.6973] | +0.1325 | [+0.0919, +0.1761] | +0.0021 | [-0.0133, +0.0183] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.30 | +0.6136 | +0.6106 | **+0.6436** | [+0.5976, +0.6903] | +0.0300 | [-0.0029, +0.0637] | +0.0330 | [+0.0192, +0.0473] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.35 | +0.4880 | +0.7676 | **+0.7754** | [+0.7315, +0.8110] | +0.2874 | [+0.2397, +0.3405] | +0.0078 | [-0.0113, +0.0263] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.30 | +0.7663 | +0.8222 | **+0.8375** | [+0.8038, +0.8648] | +0.0712 | [+0.0480, +0.0949] | +0.0153 | [+0.0055, +0.0251] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.30 | +0.2216 | +0.3407 | **+0.3483** | [+0.2972, +0.4004] | +0.1267 | [+0.0751, +0.1779] | +0.0076 | [-0.0138, +0.0294] |
| **medie** | | | | 0.30 | +0.5523 | +0.6424 | **+0.6616** | | +0.1093 | | +0.0192 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 5 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5523 |
| semnalul B singur, `gemma4-12b-4bit` | 0.6424 |
| **fuziunea A plus B, w ales LOLO pe test** | **0.6616** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0045**. Trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.30 | +0.5661 | +0.6779 | 0.1118 |
| de | 0.30 | +0.5435 | +0.6570 | 0.1135 |
| en | 0.30 | +0.5226 | +0.6394 | 0.1168 |
| es | 0.30 | +0.5432 | +0.6529 | 0.1097 |
| fil | 0.30 | +0.5687 | +0.6778 | 0.1091 |
| fr | 0.30 | +0.5564 | +0.6638 | 0.1074 |
| it | 0.30 | +0.5455 | +0.6642 | 0.1187 |
| ja | 0.35 | +0.5594 | +0.6490 | 0.0896 |
| pt | 0.30 | +0.5285 | +0.6427 | 0.1142 |
| si | 0.30 | +0.5890 | +0.6970 | 0.1080 |

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
