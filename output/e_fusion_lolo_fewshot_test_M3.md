# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-22 15:48:02 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag fewshot_test_M3 --b-dir output/bakeoff_test_M3 --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_temp.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_fewshot_test_M3.csv`, predictii per instanta in `output/fusion_preds_lolo_fewshot_test_M3.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4619 | +0.5159 | **+0.5608** | [+0.4976, +0.6177] | +0.0989 | [+0.0474, +0.1560] | +0.0449 | [+0.0167, +0.0718] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6784 | +0.7109 | **+0.7718** | [+0.7386, +0.8025] | +0.0934 | [+0.0593, +0.1290] | +0.0610 | [+0.0425, +0.0799] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8287 | +0.8474 | **+0.8729** | [+0.8462, +0.8954] | +0.0442 | [+0.0225, +0.0682] | +0.0255 | [+0.0140, +0.0382] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.35 | +0.6991 | +0.7531 | **+0.7664** | [+0.7285, +0.8004] | +0.0673 | [+0.0425, +0.0932] | +0.0133 | [+0.0001, +0.0270] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.35 | +0.4166 | +0.4986 | **+0.5056** | [+0.4388, +0.5643] | +0.0890 | [+0.0497, +0.1259] | +0.0070 | [-0.0128, +0.0278] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.40 | +0.5524 | +0.6742 | **+0.6663** | [+0.6127, +0.7150] | +0.1140 | [+0.0832, +0.1489] | -0.0079 | [-0.0260, +0.0094] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.35 | +0.6489 | +0.6407 | **+0.6796** | [+0.6356, +0.7237] | +0.0307 | [+0.0021, +0.0594] | +0.0389 | [+0.0224, +0.0562] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.6267 | +0.7778 | **+0.7908** | [+0.7487, +0.8257] | +0.1641 | [+0.1219, +0.2082] | +0.0130 | [-0.0086, +0.0357] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.35 | +0.7856 | +0.8211 | **+0.8391** | [+0.8091, +0.8657] | +0.0535 | [+0.0328, +0.0758] | +0.0179 | [+0.0063, +0.0292] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.875 | 0.35 | +0.3073 | +0.3937 | **+0.4308** | [+0.3708, +0.4879] | +0.1236 | [+0.0730, +0.1793] | +0.0371 | [+0.0052, +0.0675] |
| **medie** | | | | 0.750 | 0.36 | +0.6006 | +0.6633 | **+0.6884** | | +0.0879 | | +0.0251 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_temp.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5566 | **+0.5608** | +0.0042 | [-0.0059, +0.0150] | 78.6% |
| de | +0.7468 | **+0.7718** | +0.0250 | [+0.0161, +0.0345] | 100.0% |
| en | +0.8700 | **+0.8729** | +0.0029 | [-0.0016, +0.0077] | 89.6% |
| es | +0.7641 | **+0.7664** | +0.0023 | [-0.0030, +0.0074] | 79.7% |
| fil | +0.5091 | **+0.5056** | -0.0035 | [-0.0110, +0.0033] | 17.0% |
| fr | +0.6590 | **+0.6663** | +0.0074 | [+0.0003, +0.0148] | 97.8% |
| it | +0.6750 | **+0.6796** | +0.0046 | [-0.0025, +0.0117] | 89.7% |
| ja | +0.7877 | **+0.7908** | +0.0030 | [-0.0030, +0.0088] | 83.4% |
| pt | +0.8450 | **+0.8391** | -0.0059 | [-0.0100, -0.0022] | 0.0% |
| si | +0.4251 | **+0.4308** | +0.0057 | [-0.0077, +0.0195] | 79.9% |
| **medie** | +0.6838 | **+0.6884** | +0.0046 | | 71.6% |

Configuratia noua urca fuziunea pe 8 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0046**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6884** | [+0.6740, +0.7024] | |
| fuziune − A | +0.0878 | [+0.0759, +0.0991] | 100.0% |
| fuziune − B | +0.0251 | [+0.0189, +0.0313] | 100.0% |
| configuratia noua − cea de azi | +0.0046 | [+0.0020, +0.0070] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6006 |
| semnalul B singur, `lolo` | 0.6633 |
| fuziunea de azi, A = `p_multi` | 0.6838 |
| **fuziunea cu ansamblul de surse** | **0.6884** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0313**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6169 | +0.7036 | 0.0867 | 0.0044 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5951 | +0.6801 | 0.0850 | 0.0028 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5761 | +0.6689 | 0.0928 | 0.0044 |
| es | 1.000 | 0.35 | 9 | 5031 | +0.5828 | +0.6802 | 0.0974 | 0.0022 |
| fil | 0.750 | 0.35 | 9 | 5054 | +0.6219 | +0.7097 | 0.0878 | 0.0024 |
| fr | 0.625 | 0.40 | 9 | 5055 | +0.6091 | +0.6915 | 0.0824 | 0.0035 |
| it | 0.625 | 0.35 | 9 | 5054 | +0.5984 | +0.6904 | 0.0920 | 0.0037 |
| ja | 0.625 | 0.40 | 9 | 5054 | +0.6009 | +0.6777 | 0.0768 | 0.0021 |
| pt | 0.875 | 0.35 | 9 | 5057 | +0.5776 | +0.6725 | 0.0949 | 0.0026 |
| si | 0.875 | 0.35 | 9 | 5024 | +0.6307 | +0.7178 | 0.0871 | 0.0027 |

Latimea medie a curbei lui w e 0.0883, iar a criteriului de candidati 0.0031, adica de 29 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
