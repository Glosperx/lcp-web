# Fuziunea A plus B, brat `gemma4-12b-4bit`, pondere potrivita pe test

Generat 2026-08-18 10:24:53 de `fuse_ab.py --arm gemma4-12b-4bit --fit test`. Date brute: `output/fusion_gemma4-12b-4bit_fittest_lemma.csv`, predictii per instanta in `output/fusion_preds_gemma4-12b-4bit_fittest_lemma.csv`.

Ponderea w e aleasa leave-one-language-out pe TESTUL celorlalte 9 limbi, apoi aplicata pe testul limbii L. Nu vede limba L, pe niciun split. Acelasi protocol pe care il foloseste deja bratul A, antrenat pe etichetele de test ale celorlalte 9 limbi la `finetune_xlmr.py:446`. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.30 | +0.4470 | +0.4829 | **+0.5270** | [+0.4624, +0.5857] | +0.0800 | [+0.0203, +0.1423] | +0.0441 | [+0.0189, +0.0686] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.30 | +0.6551 | +0.6544 | **+0.7160** | [+0.6767, +0.7539] | +0.0608 | [+0.0241, +0.1015] | +0.0615 | [+0.0457, +0.0780] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.30 | +0.8147 | +0.8377 | **+0.8655** | [+0.8366, +0.8902] | +0.0508 | [+0.0280, +0.0767] | +0.0278 | [+0.0177, +0.0391] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.35 | +0.6686 | +0.7432 | **+0.7531** | [+0.7149, +0.7882] | +0.0845 | [+0.0584, +0.1112] | +0.0100 | [-0.0027, +0.0232] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.35 | +0.4091 | +0.5190 | **+0.5186** | [+0.4531, +0.5802] | +0.1094 | [+0.0701, +0.1494] | -0.0004 | [-0.0200, +0.0209] |
| fr | `gemma4-12b-4bit` | 566 | 191 | 0.35 | +0.5305 | +0.6457 | **+0.6488** | [+0.5949, +0.6976] | +0.1183 | [+0.0817, +0.1594] | +0.0031 | [-0.0156, +0.0219] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.30 | +0.6336 | +0.6106 | **+0.6521** | [+0.6066, +0.6978] | +0.0185 | [-0.0139, +0.0519] | +0.0415 | [+0.0268, +0.0567] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.35 | +0.4890 | +0.7676 | **+0.7709** | [+0.7268, +0.8069] | +0.2819 | [+0.2345, +0.3347] | +0.0032 | [-0.0165, +0.0219] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.35 | +0.7705 | +0.8222 | **+0.8388** | [+0.8053, +0.8659] | +0.0683 | [+0.0452, +0.0921] | +0.0166 | [+0.0050, +0.0286] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.35 | +0.2119 | +0.3407 | **+0.3430** | [+0.2933, +0.3951] | +0.1311 | [+0.0827, +0.1807] | +0.0023 | [-0.0237, +0.0285] |
| **medie** | | | | 0.33 | +0.5630 | +0.6424 | **+0.6634** | | +0.1004 | | +0.0210 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 5 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5630 |
| semnalul B singur, `gemma4-12b-4bit` | 0.6424 |
| **fuziunea A plus B, w ales LOLO pe test** | **0.6634** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0063**. Trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.30 | +0.5759 | +0.6802 | 0.1043 |
| de | 0.30 | +0.5528 | +0.6592 | 0.1064 |
| en | 0.30 | +0.5350 | +0.6426 | 0.1076 |
| es | 0.35 | +0.5513 | +0.6551 | 0.1038 |
| fil | 0.35 | +0.5801 | +0.6812 | 0.1011 |
| fr | 0.35 | +0.5666 | +0.6667 | 0.1001 |
| it | 0.30 | +0.5551 | +0.6663 | 0.1112 |
| ja | 0.35 | +0.5712 | +0.6532 | 0.0820 |
| pt | 0.35 | +0.5399 | +0.6456 | 0.1057 |
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
