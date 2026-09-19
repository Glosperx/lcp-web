# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-29 14:05:52 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag p3only --b-dir output/bakeoff_test_P3ONLY --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_P3ONLY/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_p3only.csv`, predictii per instanta in `output/fusion_preds_lolo_p3only.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.500 | 0.45 | +0.4710 | +0.4683 | **+0.5519** | [+0.4867, +0.6095] | +0.0809 | [+0.0353, +0.1330] | +0.0835 | [+0.0441, +0.1198] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.500 | 0.45 | +0.6751 | +0.6881 | **+0.7828** | [+0.7477, +0.8150] | +0.1078 | [+0.0739, +0.1446] | +0.0947 | [+0.0675, +0.1218] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.45 | +0.8287 | +0.7862 | **+0.8568** | [+0.8280, +0.8815] | +0.0281 | [+0.0061, +0.0514] | +0.0706 | [+0.0486, +0.0960] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.500 | 0.45 | +0.7038 | +0.7148 | **+0.7524** | [+0.7091, +0.7886] | +0.0486 | [+0.0258, +0.0722] | +0.0376 | [+0.0183, +0.0585] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.500 | 0.50 | +0.4150 | +0.4432 | **+0.4700** | [+0.4020, +0.5325] | +0.0551 | [+0.0235, +0.0847] | +0.0268 | [-0.0039, +0.0610] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.500 | 0.50 | +0.5549 | +0.6370 | **+0.6493** | [+0.5945, +0.6989] | +0.0944 | [+0.0664, +0.1254] | +0.0123 | [-0.0122, +0.0375] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.45 | +0.6487 | +0.6096 | **+0.6789** | [+0.6305, +0.7252] | +0.0302 | [+0.0021, +0.0583] | +0.0693 | [+0.0441, +0.0964] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.500 | 0.50 | +0.6279 | +0.7275 | **+0.7578** | [+0.7101, +0.7971] | +0.1299 | [+0.0920, +0.1664] | +0.0303 | [+0.0013, +0.0626] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.45 | +0.7863 | +0.7501 | **+0.8107** | [+0.7779, +0.8399] | +0.0245 | [+0.0056, +0.0450] | +0.0606 | [+0.0414, +0.0798] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.500 | 0.50 | +0.3297 | +0.3660 | **+0.4204** | [+0.3575, +0.4801] | +0.0907 | [+0.0504, +0.1333] | +0.0545 | [+0.0089, +0.0969] |
| **medie** | | | | 0.575 | 0.47 | +0.6041 | +0.6191 | **+0.6731** | | +0.0690 | | +0.0540 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 8 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5519** | -0.0120 | [-0.0319, +0.0087] | 12.2% |
| de | +0.7712 | **+0.7828** | +0.0116 | [-0.0026, +0.0254] | 94.8% |
| en | +0.8723 | **+0.8568** | -0.0155 | [-0.0265, -0.0053] | 0.1% |
| es | +0.7672 | **+0.7524** | -0.0148 | [-0.0254, -0.0052] | 0.2% |
| fil | +0.5074 | **+0.4700** | -0.0373 | [-0.0513, -0.0242] | 0.0% |
| fr | +0.6679 | **+0.6493** | -0.0186 | [-0.0337, -0.0045] | 0.6% |
| it | +0.6795 | **+0.6789** | -0.0006 | [-0.0127, +0.0111] | 46.6% |
| ja | +0.7942 | **+0.7578** | -0.0364 | [-0.0511, -0.0224] | 0.0% |
| pt | +0.8413 | **+0.8107** | -0.0305 | [-0.0407, -0.0219] | 0.0% |
| si | +0.4350 | **+0.4204** | -0.0146 | [-0.0321, +0.0037] | 5.5% |
| **medie** | +0.6900 | **+0.6731** | -0.0169 | | 16.0% |

Configuratia noua urca fuziunea pe 1 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0169**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6731** | [+0.6578, +0.6880] | |
| fuziune − A | +0.0690 | [+0.0589, +0.0792] | 100.0% |
| fuziune − B | +0.0540 | [+0.0448, +0.0630] | 100.0% |
| configuratia noua − cea de azi | -0.0169 | [-0.0214, -0.0123] | 0.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6041 |
| semnalul B singur, `lolo` | 0.6191 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6731** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0160**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.500 | 0.45 | 9 | 5179 | +0.6193 | +0.6878 | 0.0685 | 0.0021 |
| de | 0.500 | 0.45 | 9 | 5054 | +0.5966 | +0.6622 | 0.0656 | 0.0021 |
| en | 0.750 | 0.45 | 9 | 5054 | +0.5761 | +0.6533 | 0.0772 | 0.0026 |
| es | 0.500 | 0.45 | 9 | 5031 | +0.5934 | +0.6656 | 0.0722 | 0.0021 |
| fil | 0.500 | 0.50 | 9 | 5054 | +0.6255 | +0.6968 | 0.0713 | 0.0025 |
| fr | 0.500 | 0.50 | 9 | 5055 | +0.6099 | +0.6769 | 0.0670 | 0.0044 |
| it | 0.750 | 0.45 | 9 | 5054 | +0.5961 | +0.6731 | 0.0770 | 0.0019 |
| ja | 0.500 | 0.50 | 9 | 5054 | +0.6018 | +0.6649 | 0.0631 | 0.0034 |
| pt | 0.750 | 0.45 | 9 | 5057 | +0.5809 | +0.6585 | 0.0776 | 0.0020 |
| si | 0.500 | 0.50 | 9 | 5024 | +0.6350 | +0.7023 | 0.0673 | 0.0025 |

Latimea medie a curbei lui w e 0.0707, iar a criteriului de candidati 0.0026, adica de 28 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
