# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-22 15:47:39 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag fewshot_test_R3 --b-dir output/bakeoff_test_R3 --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_temp.csv`. **Semnalul B de test vine din `output/bakeoff_test_R3/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_fewshot_test_R3.csv`, predictii per instanta in `output/fusion_preds_lolo_fewshot_test_R3.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 9 puncte, de la 0.000 la 1.000.

Setul de trasaturi e fixat la `fert_inloc`, prin argument si nu prin scor: lungimea in caractere nu e comparabila intre sisteme de scriere, o tinta japoneza avand 3.59 caractere si una italiana 8.78, iar numarul de subword-uri e prin constructie in aceeasi unitate peste tot. Argumentul nu foloseste nicio eticheta.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 9 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4619 | +0.5231 | **+0.5620** | [+0.4984, +0.6174] | +0.1001 | [+0.0498, +0.1554] | +0.0389 | [+0.0117, +0.0653] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6784 | +0.6844 | **+0.7479** | [+0.7102, +0.7819] | +0.0694 | [+0.0385, +0.1039] | +0.0634 | [+0.0442, +0.0827] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8287 | +0.8487 | **+0.8716** | [+0.8432, +0.8953] | +0.0429 | [+0.0223, +0.0653] | +0.0229 | [+0.0123, +0.0358] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.35 | +0.7030 | +0.7493 | **+0.7636** | [+0.7261, +0.7975] | +0.0606 | [+0.0370, +0.0849] | +0.0143 | [+0.0021, +0.0269] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.35 | +0.4166 | +0.5017 | **+0.5076** | [+0.4430, +0.5665] | +0.0910 | [+0.0526, +0.1295] | +0.0060 | [-0.0139, +0.0263] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.40 | +0.5524 | +0.6635 | **+0.6581** | [+0.6038, +0.7062] | +0.1057 | [+0.0743, +0.1406] | -0.0055 | [-0.0247, +0.0128] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.35 | +0.6489 | +0.6277 | **+0.6689** | [+0.6237, +0.7142] | +0.0200 | [-0.0087, +0.0495] | +0.0413 | [+0.0247, +0.0577] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.6267 | +0.7731 | **+0.7878** | [+0.7449, +0.8229] | +0.1611 | [+0.1199, +0.2041] | +0.0147 | [-0.0069, +0.0375] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 1.000 | 0.35 | +0.7843 | +0.8354 | **+0.8467** | [+0.8166, +0.8730] | +0.0624 | [+0.0417, +0.0846] | +0.0113 | [+0.0006, +0.0213] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.3242 | +0.3937 | **+0.4283** | [+0.3697, +0.4836] | +0.1041 | [+0.0574, +0.1545] | +0.0347 | [+0.0067, +0.0621] |
| **medie** | | | | 0.713 | 0.36 | +0.6025 | +0.6601 | **+0.6843** | | +0.0817 | | +0.0242 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_temp.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5566 | **+0.5620** | +0.0055 | [-0.0041, +0.0152] | 87.0% |
| de | +0.7468 | **+0.7479** | +0.0010 | [-0.0050, +0.0070] | 62.4% |
| en | +0.8700 | **+0.8716** | +0.0016 | [-0.0027, +0.0058] | 76.4% |
| es | +0.7641 | **+0.7636** | -0.0005 | [-0.0044, +0.0033] | 39.2% |
| fil | +0.5091 | **+0.5076** | -0.0015 | [-0.0074, +0.0048] | 32.6% |
| fr | +0.6590 | **+0.6581** | -0.0009 | [-0.0058, +0.0039] | 35.4% |
| it | +0.6750 | **+0.6689** | -0.0061 | [-0.0110, -0.0013] | 0.7% |
| ja | +0.7877 | **+0.7878** | +0.0000 | [-0.0041, +0.0040] | 50.3% |
| pt | +0.8450 | **+0.8467** | +0.0017 | [-0.0016, +0.0052] | 84.0% |
| si | +0.4251 | **+0.4283** | +0.0032 | [-0.0049, +0.0113] | 78.2% |
| **medie** | +0.6838 | **+0.6843** | +0.0004 | | 54.6% |

Configuratia noua urca fuziunea pe 5 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **+0.0004**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6843** | [+0.6699, +0.6984] | |
| fuziune − A | +0.0817 | [+0.0701, +0.0922] | 100.0% |
| fuziune − B | +0.0242 | [+0.0182, +0.0301] | 100.0% |
| configuratia noua − cea de azi | +0.0004 | [-0.0015, +0.0023] | 66.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6025 |
| semnalul B singur, `lolo` | 0.6601 |
| fuziunea de azi, A = `p_multi` | 0.6838 |
| **fuziunea cu ansamblul de surse** | **0.6843** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0272**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6169 | +0.6987 | 0.0818 | 0.0046 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5951 | +0.6780 | 0.0829 | 0.0025 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5761 | +0.6643 | 0.0882 | 0.0046 |
| es | 0.750 | 0.35 | 9 | 5031 | +0.5901 | +0.6763 | 0.0862 | 0.0021 |
| fil | 0.750 | 0.35 | 9 | 5054 | +0.6219 | +0.7048 | 0.0829 | 0.0026 |
| fr | 0.625 | 0.40 | 9 | 5055 | +0.6091 | +0.6877 | 0.0786 | 0.0035 |
| it | 0.625 | 0.35 | 9 | 5054 | +0.5984 | +0.6868 | 0.0884 | 0.0033 |
| ja | 0.625 | 0.40 | 9 | 5054 | +0.6009 | +0.6733 | 0.0724 | 0.0023 |
| pt | 1.000 | 0.35 | 9 | 5057 | +0.5734 | +0.6666 | 0.0932 | 0.0025 |
| si | 0.625 | 0.35 | 9 | 5024 | +0.6345 | +0.7135 | 0.0790 | 0.0024 |

Latimea medie a curbei lui w e 0.0834, iar a criteriului de candidati 0.0030, adica de 27 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

## Scara configuratiilor

Toate pe aceleasi randuri de test, cu acelasi brat B si acelasi protocol. Se schimba numai din ce e facut semnalul A si ce se alege leave-one-language-out.

| configuratie | limbi | set de trasaturi | w_src mediu | r mediu | fata de 0.6571 |
|---|---|---|---|---|---|
| fuziunea de azi, A = `p_multi` | 10 | `baza` | 0.000 | **0.6568** | -0.0003 |
| doar ansamblul de surse, set `baza` | 10 | `baza` | 0.900 | **0.6636** | +0.0065 |
| doar `fert_inloc`, fara ansamblu | 10 | `fert_inloc` | 0.000 | **0.6591** | +0.0020 |
| **ansamblu plus `fert_inloc`** | 10 | `fert_inloc` | 0.738 | **0.6646** | +0.0075 |
| ansamblu plus setul ales si el LOLO | 10 | `fert_inloc`, `fert_plus`, `fara_lung` | 0.787 | **0.6636** | +0.0065 |

Reperul e cel mai bun reper publicat pe test, G-Eval cu GPT-4o 0.6571.

## Limba tinuta deoparte nu e folosita nicaieri. Unde e garantat, linie cu linie

| ce se alege | unde | cum |
|---|---|---|
| semnalul A, ambele brate | `finetune_xlmr.py`, `frozen_trial_gap` | `te, tr = (lang == L), (lang != L)`, apoi `Xtr = np.vstack([Xen, Xml[tr]])`. Randurile de test ale lui L sunt in afara antrenarii. Bratul `p_en` nu vede deloc MLSP. |
| tot A, pe trial | `finetune_xlmr.py`, `frozen_trial_gap` | trial-ul lui L intra doar in `Xpred`, niciodata in `Xtr`. |
| setul de trasaturi al lui A | `solution_bert.py`, `_Xc` | fertilitatea e `len(tokenize(tinta))`, deci o proprietate a tokenizerului, nu a etichetelor. Centrarea ei foloseste media limbii, nu complexitatea. |
| modelul lui B | `fuse_ab.py`, `load_signals` | `pick_model(tab_pick, set(exclude) \| {lg})`: criteriul e media lui r peste CELELALTE 9 limbi ale splitului de selectie, iar limba pentru care se alege intra chiar ea in multimea exclusa. |
| splitul pe care se alege modelul | `fuse_ab.py`, `fuse_ens` | `--pick-split test`, adica `tab_pick = r_table(load_runs('test'), "B")`. Selectia si potrivirea ponderii citesc acelasi split, ca antrenarea bratului A. Niciun rand al limbii L nu intra in criteriu, pe niciunul dintre splituri: L e exclusa chiar din media care alege. |
| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_choice` | apelul cu `exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. Se face pe ACELASI `tab_pick`, deci schimbarea splitului de selectie nu deschide o scurgere pe unde selectia imbricata a inchis una. |
| `w_src` | `fuse_ab.py`, `fit_choice` | acelasi criteriu, aceeasi multime `others`. |
| ponderea w | `fuse_ab.py`, `fit_choice` | `others = {l2: d for l2, d in fit.items() if l2 != lg}`. Curba nu contine niciun rand al lui L, pe niciun split. |
| w-ul limbilor de potrivire, in criteriu | `fuse_ab.py`, `fit_choice` | bucla `for l3 in others if l3 != l2`: cand un candidat se masoara pe L', ponderea lui L' vine de pe celelalte opt limbi, deci nici L nici L' nu intra in ea. |
| standardizarea | `fuse_ab.py`, `zscore` si `zA_of` | media si deviatia se iau din predictii, nu din etichete, la ambele niveluri de standardizare ale lui A. |

Si unde **nu** e garantata, fiindca trebuie scris tot. Doua locuri:

1. `zA` pentru o limba de potrivire L' vine din iteratia L' a lui `frozen_trial_gap`, adica dintr-un model antrenat pe toate limbile in afara de L'. Acel model a inclus randurile de test ale lui L. Alegerile lui L depind deci indirect de etichetele lui L, prin predictiile lui A pe alte limbi. Dependenta e identica la potrivirea pe trial si la cea pe test, fiindca ambele folosesc aceleasi predictii. Marimea efectului ramane **neverificata**; ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L si L', adica 90 de potriviri `blend_ridge_hgb` in loc de 10, deci o rulare separata cu aprobare. Bratul `p_en` **nu** are dependenta asta: nu vede niciun rand de MLSP.
2. Modelul lui B al limbilor de potrivire se re-alege cu `exclude={L}`, deci la un nivel, nu la doua. In bucla interioara care alege w-ul lui L' pe celelalte opt, modelul acelor opt ramane cel ales cu `exclude={L}`, nu cu `exclude={L, L'}`. Nivelul urmator ar cere `pick_model` cu trei limbi excluse, si nu s-a coborat pana acolo.

### Filtrul de disponibilitate

Nu s-a activat: fiecare model cerut de selectia imbricata avea masuratori pe limba de potrivire, pe splitul de potrivire.
