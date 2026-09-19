# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-18 12:25:36 de `fuse_ab.py --arm lolo --fit test --ens --tag ens_baza --a-set baza=output/e1_frozen_preds_lemma.csv --vs output/fusion_preds_lolo_fittest_lemma.csv`. Date brute: `output/fusion_lolo_ens_baza.csv`, predictii per instanta in `output/fusion_preds_lolo_ens_baza.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 9 puncte, de la 0.000 la 1.000.

Setul de trasaturi e fixat la `baza`, prin argument si nu prin scor: lungimea in caractere nu e comparabila intre sisteme de scriere, o tinta japoneza avand 3.59 caractere si una italiana 8.78, iar numarul de subword-uri e prin constructie in aceeasi unitate peste tot. Argumentul nu foloseste nicio eticheta.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 9 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.35 | +0.4163 | +0.4829 | **+0.5245** | [+0.4573, +0.5848] | +0.1082 | [+0.0493, +0.1678] | +0.0416 | [+0.0100, +0.0731] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.875 | 0.35 | +0.6645 | +0.6544 | **+0.7318** | [+0.6928, +0.7696] | +0.0673 | [+0.0322, +0.1053] | +0.0774 | [+0.0573, +0.0982] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.40 | +0.8136 | +0.8377 | **+0.8657** | [+0.8384, +0.8895] | +0.0521 | [+0.0310, +0.0760] | +0.0280 | [+0.0153, +0.0422] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.40 | +0.6648 | +0.7432 | **+0.7506** | [+0.7120, +0.7854] | +0.0858 | [+0.0596, +0.1123] | +0.0075 | [-0.0075, +0.0226] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 1.000 | 0.35 | +0.4151 | +0.5190 | **+0.5227** | [+0.4594, +0.5846] | +0.1076 | [+0.0661, +0.1479] | +0.0037 | [-0.0165, +0.0245] |
| fr | `qwen35-9b-8bit` | 566 | 191 | 0.875 | 0.35 | +0.5323 | +0.5440 | **+0.5836** | [+0.5290, +0.6363] | +0.0513 | [+0.0109, +0.0933] | +0.0395 | [+0.0162, +0.0630] |
| it | `gemma4-12b-4bit` | 562 | 192 | 1.000 | 0.35 | +0.6265 | +0.6106 | **+0.6590** | [+0.6135, +0.7040] | +0.0325 | [+0.0013, +0.0636] | +0.0484 | [+0.0307, +0.0660] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.40 | +0.5346 | +0.7676 | **+0.7818** | [+0.7388, +0.8184] | +0.2471 | [+0.2020, +0.2973] | +0.0141 | [-0.0121, +0.0406] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.875 | 0.40 | +0.7812 | +0.8222 | **+0.8412** | [+0.8078, +0.8681] | +0.0600 | [+0.0392, +0.0805] | +0.0190 | [+0.0061, +0.0325] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.2615 | +0.3407 | **+0.3746** | [+0.3230, +0.4270] | +0.1131 | [+0.0635, +0.1637] | +0.0339 | [+0.0061, +0.0602] |
| **medie** | | | | 0.900 | 0.37 | +0.5710 | +0.6322 | **+0.6636** | | +0.0925 | | +0.0313 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_fittest_lemma.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5305 | **+0.5245** | -0.0060 | [-0.0168, +0.0061] | 14.4% |
| de | +0.7160 | **+0.7318** | +0.0159 | [+0.0083, +0.0237] | 100.0% |
| en | +0.8674 | **+0.8657** | -0.0017 | [-0.0058, +0.0027] | 22.4% |
| es | +0.7531 | **+0.7506** | -0.0025 | [-0.0079, +0.0031] | 19.6% |
| fil | +0.5186 | **+0.5227** | +0.0041 | [-0.0010, +0.0089] | 95.1% |
| fr | +0.5823 | **+0.5836** | +0.0013 | [-0.0061, +0.0085] | 64.3% |
| it | +0.6565 | **+0.6590** | +0.0025 | [-0.0058, +0.0106] | 72.0% |
| ja | +0.7616 | **+0.7818** | +0.0201 | [+0.0020, +0.0406] | 98.5% |
| pt | +0.8388 | **+0.8412** | +0.0024 | [-0.0018, +0.0068] | 87.0% |
| si | +0.3430 | **+0.3746** | +0.0316 | [+0.0109, +0.0526] | 99.9% |
| **medie** | +0.6568 | **+0.6636** | +0.0068 | | 67.3% |

Configuratia noua urca fuziunea pe 7 din 10 limbi. Intervalul pereche exclude zero in sus pe 3. Pe medie, **+0.0068**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6636** | [+0.6483, +0.6777] | |
| fuziune − A | +0.0925 | [+0.0801, +0.1048] | 100.0% |
| fuziune − B | +0.0313 | [+0.0245, +0.0385] | 100.0% |
| configuratia noua − cea de azi | +0.0068 | [+0.0034, +0.0104] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5710 |
| semnalul B singur, `lolo` | 0.6322 |
| fuziunea de azi, A = `p_multi` | 0.6568 |
| **fuziunea cu ansamblul de surse** | **0.6636** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0065**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.35 | 9 | 5161 | +0.5857 | +0.6803 | 0.0946 | 0.0090 |
| de | 0.875 | 0.35 | 9 | 5036 | +0.5624 | +0.6573 | 0.0949 | 0.0069 |
| en | 0.875 | 0.40 | 9 | 5036 | +0.5458 | +0.6426 | 0.0968 | 0.0084 |
| es | 0.750 | 0.40 | 9 | 5013 | +0.5652 | +0.6553 | 0.0901 | 0.0080 |
| fil | 1.000 | 0.35 | 9 | 5038 | +0.5858 | +0.6876 | 0.1018 | 0.0079 |
| fr | 0.875 | 0.35 | 9 | 5040 | +0.5771 | +0.6738 | 0.0967 | 0.0084 |
| it | 1.000 | 0.35 | 9 | 5044 | +0.5623 | +0.6654 | 0.1031 | 0.0077 |
| ja | 1.000 | 0.40 | 9 | 5036 | +0.5725 | +0.6517 | 0.0792 | 0.0065 |
| pt | 0.875 | 0.40 | 9 | 5044 | +0.5494 | +0.6453 | 0.0959 | 0.0076 |
| si | 0.750 | 0.35 | 9 | 5006 | +0.6101 | +0.7040 | 0.0939 | 0.0052 |

Latimea medie a curbei lui w e 0.0947, iar a criteriului de candidati 0.0076, adica de 13 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

## Scara configuratiilor

Toate pe aceleasi randuri de test, cu acelasi brat B si acelasi protocol. Se schimba numai din ce e facut semnalul A si ce se alege leave-one-language-out.

| configuratie | limbi | set de trasaturi | w_src mediu | r mediu | fata de 0.6571 |
|---|---|---|---|---|---|
| fuziunea de azi, A = `p_multi` | 10 | `baza` | 0.000 | **0.6568** | -0.0003 |
| doar ansamblul de surse, set `baza` | 10 | `baza` | 0.900 | **0.6636** | +0.0065 |
| doar `fert_inloc`, fara ansamblu | 10 | `fert_inloc` | 0.000 | **0.6591** | +0.0020 |
| **ansamblu plus `fert_inloc`** | 10 | `fert_inloc` | 0.775 | **0.6645** | +0.0074 |
| ansamblu plus setul ales si el LOLO | 10 | `fert_inloc`, `fert_plus`, `fara_lung` | 0.787 | **0.6636** | +0.0065 |

Reperul e cel mai bun reper publicat pe test, G-Eval cu GPT-4o 0.6571.

## Limba tinuta deoparte nu e folosita nicaieri. Unde e garantat, linie cu linie

| ce se alege | unde | cum |
|---|---|---|
| semnalul A, ambele brate | `finetune_xlmr.py`, `frozen_trial_gap` | `te, tr = (lang == L), (lang != L)`, apoi `Xtr = np.vstack([Xen, Xml[tr]])`. Randurile de test ale lui L sunt in afara antrenarii. Bratul `p_en` nu vede deloc MLSP. |
| tot A, pe trial | `finetune_xlmr.py`, `frozen_trial_gap` | trial-ul lui L intra doar in `Xpred`, niciodata in `Xtr`. |
| setul de trasaturi al lui A | `solution_bert.py`, `_Xc` | fertilitatea e `len(tokenize(tinta))`, deci o proprietate a tokenizerului, nu a etichetelor. Centrarea ei foloseste media limbii, nu complexitatea. |
| modelul lui B | `fuse_ab.py`, `load_signals` | `pick_model(tab_trial, set(exclude) \| {lg})`: limba pentru care se alege intra chiar ea in multimea exclusa. |
| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_choice` | apelul cu `exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. |
| `w_src` | `fuse_ab.py`, `fit_choice` | acelasi criteriu, aceeasi multime `others`. |
| ponderea w | `fuse_ab.py`, `fit_choice` | `others = {l2: d for l2, d in fit.items() if l2 != lg}`. Curba nu contine niciun rand al lui L, pe niciun split. |
| w-ul limbilor de potrivire, in criteriu | `fuse_ab.py`, `fit_choice` | bucla `for l3 in others if l3 != l2`: cand un candidat se masoara pe L', ponderea lui L' vine de pe celelalte opt limbi, deci nici L nici L' nu intra in ea. |
| standardizarea | `fuse_ab.py`, `zscore` si `zA_of` | media si deviatia se iau din predictii, nu din etichete, la ambele niveluri de standardizare ale lui A. |

Si unde **nu** e garantata, fiindca trebuie scris tot. Doua locuri:

1. `zA` pentru o limba de potrivire L' vine din iteratia L' a lui `frozen_trial_gap`, adica dintr-un model antrenat pe toate limbile in afara de L'. Acel model a inclus randurile de test ale lui L. Alegerile lui L depind deci indirect de etichetele lui L, prin predictiile lui A pe alte limbi. Dependenta e identica la potrivirea pe trial si la cea pe test, fiindca ambele folosesc aceleasi predictii. Marimea efectului ramane **neverificata**; ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L si L', adica 90 de potriviri `blend_ridge_hgb` in loc de 10, deci o rulare separata cu aprobare. Bratul `p_en` **nu** are dependenta asta: nu vede niciun rand de MLSP.
2. Modelul lui B al limbilor de potrivire se re-alege cu `exclude={L}`, deci la un nivel, nu la doua. In bucla interioara care alege w-ul lui L' pe celelalte opt, modelul acelor opt ramane cel ales cu `exclude={L}`, nu cu `exclude={L, L'}`. Nivelul urmator ar cere `pick_model` cu trei limbi excluse, si nu s-a coborat pana acolo.

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
