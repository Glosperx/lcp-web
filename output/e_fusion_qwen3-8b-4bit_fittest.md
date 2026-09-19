# Fuziunea A plus B, brat `qwen3-8b-4bit`, pondere potrivita pe test

Generat 2026-08-18 00:59:39 de `fuse_ab.py --arm qwen3-8b-4bit --fit test`. Date brute: `output/fusion_qwen3-8b-4bit_fittest.csv`, predictii per instanta in `output/fusion_preds_qwen3-8b-4bit_fittest.csv`.

Ponderea w e aleasa leave-one-language-out pe TESTUL celorlalte 9 limbi, apoi aplicata pe testul limbii L. Nu vede limba L, pe niciun split. Acelasi protocol pe care il foloseste deja bratul A, antrenat pe etichetele de test ale celorlalte 9 limbi la `finetune_xlmr.py:446`. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `qwen3-8b-4bit` | 445 | 150 | 0.75 | +0.4281 | +0.2543 | **+0.4339** | [+0.3510, +0.5103] | +0.0058 | [-0.0159, +0.0269] | +0.1796 | [+0.1082, +0.2478] |
| de | `qwen3-8b-4bit` | 570 | 193 | 0.70 | +0.6314 | +0.3420 | **+0.6207** | [+0.5639, +0.6723] | -0.0107 | [-0.0290, +0.0089] | +0.2787 | [+0.2239, +0.3349] |
| en | `qwen3-8b-4bit` | 570 | 190 | 0.70 | +0.8197 | +0.3882 | **+0.8066** | [+0.7723, +0.8357] | -0.0131 | [-0.0298, +0.0039] | +0.4184 | [+0.3508, +0.4840] |
| es | `qwen3-8b-4bit` | 593 | 208 | 0.75 | +0.6341 | +0.3799 | **+0.6396** | [+0.5924, +0.6823] | +0.0055 | [-0.0096, +0.0202] | +0.2597 | [+0.2039, +0.3162] |
| fil | `qwen3-8b-4bit` | 568 | 553 | 0.80 | +0.4047 | +0.4910 | **+0.4664** | [+0.3955, +0.5333] | +0.0616 | [+0.0380, +0.0881] | -0.0246 | [-0.0901, +0.0491] |
| fr | `qwen3-8b-4bit` | 566 | 191 | 0.75 | +0.5153 | +0.4011 | **+0.5345** | [+0.4732, +0.5896] | +0.0192 | [+0.0027, +0.0367] | +0.1334 | [+0.0751, +0.1948] |
| it | `qwen3-8b-4bit` | 562 | 192 | 0.75 | +0.6136 | +0.3997 | **+0.6349** | [+0.5803, +0.6884] | +0.0213 | [+0.0002, +0.0414] | +0.2352 | [+0.1637, +0.3176] |
| ja | `qwen3-8b-4bit` | 570 | 190 | 0.80 | +0.4880 | +0.4553 | **+0.5516** | [+0.4866, +0.6104] | +0.0636 | [+0.0462, +0.0822] | +0.0963 | [+0.0073, +0.1809] |
| pt | `qwen3-8b-4bit` | 562 | 557 | 0.70 | +0.7663 | +0.4878 | **+0.7550** | [+0.7167, +0.7891] | -0.0112 | [-0.0271, +0.0050] | +0.2672 | [+0.2215, +0.3140] |
| si | `qwen3-8b-4bit` | 600 | 578 | 0.75 | +0.2216 | +0.1405 | **+0.2328** | [+0.1672, +0.3005] | +0.0112 | [-0.0091, +0.0311] | +0.0923 | [+0.0289, +0.1612] |
| **medie** | | | | 0.74 | +0.5523 | +0.3740 | **+0.5676** | | +0.0153 | | +0.1936 | |

Fuziunea bate A pe 7 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 4 limbi fata de A si pe 9 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5523 |
| semnalul B singur, `qwen3-8b-4bit` | 0.3740 |
| **fuziunea A plus B, w ales LOLO pe test** | **0.5676** |

Fata de cel mai bun reper publicat, 0.6571: **-0.0895**. Nu trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.75 | +0.3873 | +0.5880 | 0.2007 |
| de | 0.70 | +0.3775 | +0.5666 | 0.1891 |
| en | 0.70 | +0.3724 | +0.5460 | 0.1736 |
| es | 0.75 | +0.3733 | +0.5651 | 0.1918 |
| fil | 0.80 | +0.3610 | +0.5829 | 0.2219 |
| fr | 0.75 | +0.3710 | +0.5768 | 0.2058 |
| it | 0.75 | +0.3711 | +0.5657 | 0.1946 |
| ja | 0.80 | +0.3649 | +0.5735 | 0.2086 |
| pt | 0.70 | +0.3613 | +0.5517 | 0.1904 |
| si | 0.75 | +0.3999 | +0.6103 | 0.2104 |

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
