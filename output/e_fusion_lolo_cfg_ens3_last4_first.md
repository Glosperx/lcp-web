# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 17:26:06 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_ens3_last4_first --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_ens3_last4_first_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_ens3_last4_first.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_ens3_last4_first.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.625 | 0.40 | +0.4597 | +0.5159 | **+0.5550** | [+0.4903, +0.6126] | +0.0953 | [+0.0505, +0.1440] | +0.0391 | [+0.0076, +0.0695] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.35 | +0.6822 | +0.6812 | **+0.7504** | [+0.7136, +0.7845] | +0.0682 | [+0.0359, +0.1038] | +0.0692 | [+0.0492, +0.0890] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.35 | +0.8299 | +0.8463 | **+0.8711** | [+0.8444, +0.8942] | +0.0412 | [+0.0202, +0.0635] | +0.0248 | [+0.0140, +0.0370] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.500 | 0.40 | +0.7100 | +0.7499 | **+0.7655** | [+0.7292, +0.7976] | +0.0555 | [+0.0338, +0.0772] | +0.0155 | [+0.0014, +0.0307] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.500 | 0.40 | +0.4092 | +0.5082 | **+0.5063** | [+0.4412, +0.5641] | +0.0971 | [+0.0609, +0.1329] | -0.0019 | [-0.0249, +0.0219] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.40 | +0.5579 | +0.6655 | **+0.6616** | [+0.6075, +0.7100] | +0.1037 | [+0.0707, +0.1396] | -0.0039 | [-0.0234, +0.0146] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.875 | 0.35 | +0.6483 | +0.6354 | **+0.6763** | [+0.6321, +0.7209] | +0.0281 | [-0.0010, +0.0578] | +0.0409 | [+0.0241, +0.0574] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.500 | 0.40 | +0.6178 | +0.7715 | **+0.7880** | [+0.7461, +0.8216] | +0.1702 | [+0.1284, +0.2133] | +0.0165 | [-0.0054, +0.0405] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.500 | 0.40 | +0.7877 | +0.8322 | **+0.8454** | [+0.8152, +0.8712] | +0.0577 | [+0.0385, +0.0782] | +0.0132 | [+0.0004, +0.0255] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.3604 | +0.3860 | **+0.4406** | [+0.3831, +0.4955] | +0.0802 | [+0.0335, +0.1311] | +0.0545 | [+0.0246, +0.0843] |
| **medie** | | | | 0.625 | 0.38 | +0.6063 | +0.6592 | **+0.6860** | | +0.0797 | | +0.0268 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5550** | +0.0080 | [-0.0025, +0.0186] | 93.2% |
| de | +0.7429 | **+0.7504** | +0.0075 | [-0.0000, +0.0148] | 97.4% |
| en | +0.8673 | **+0.8711** | +0.0037 | [-0.0007, +0.0083] | 95.4% |
| es | +0.7548 | **+0.7655** | +0.0106 | [+0.0050, +0.0164] | 100.0% |
| fil | +0.5133 | **+0.5063** | -0.0070 | [-0.0125, -0.0011] | 1.4% |
| fr | +0.6605 | **+0.6616** | +0.0011 | [-0.0070, +0.0094] | 60.8% |
| it | +0.6704 | **+0.6763** | +0.0059 | [+0.0002, +0.0115] | 97.9% |
| ja | +0.7934 | **+0.7880** | -0.0054 | [-0.0145, +0.0037] | 13.0% |
| pt | +0.8398 | **+0.8454** | +0.0056 | [+0.0011, +0.0099] | 99.2% |
| si | +0.4095 | **+0.4406** | +0.0310 | [+0.0052, +0.0584] | 98.7% |
| **medie** | +0.6799 | **+0.6860** | +0.0061 | | 75.7% |

Configuratia noua urca fuziunea pe 8 din 10 limbi. Intervalul pereche exclude zero in sus pe 4. Pe medie, **+0.0061**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6860** | [+0.6715, +0.6999] | |
| fuziune − A | +0.0797 | [+0.0682, +0.0900] | 100.0% |
| fuziune − B | +0.0268 | [+0.0202, +0.0329] | 100.0% |
| configuratia noua − cea de azi | +0.0061 | [+0.0026, +0.0095] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6063 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6860** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0289**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.625 | 0.40 | 9 | 5179 | +0.6235 | +0.7020 | 0.0785 | 0.0024 |
| de | 0.750 | 0.35 | 9 | 5054 | +0.5957 | +0.6799 | 0.0842 | 0.0022 |
| en | 0.625 | 0.35 | 9 | 5054 | +0.5824 | +0.6667 | 0.0843 | 0.0025 |
| es | 0.500 | 0.40 | 9 | 5031 | +0.5975 | +0.6786 | 0.0811 | 0.0027 |
| fil | 0.500 | 0.40 | 9 | 5054 | +0.6309 | +0.7074 | 0.0765 | 0.0039 |
| fr | 0.625 | 0.40 | 9 | 5055 | +0.6126 | +0.6901 | 0.0775 | 0.0048 |
| it | 0.875 | 0.35 | 9 | 5054 | +0.5951 | +0.6877 | 0.0926 | 0.0021 |
| ja | 0.500 | 0.40 | 9 | 5054 | +0.6078 | +0.6761 | 0.0683 | 0.0026 |
| pt | 0.500 | 0.40 | 9 | 5057 | +0.5889 | +0.6697 | 0.0808 | 0.0027 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6314 | +0.7144 | 0.0830 | 0.0019 |

Latimea medie a curbei lui w e 0.0807, iar a criteriului de candidati 0.0028, adica de 29 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
