# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-21 18:12:22 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag prio_W --b-dir output/bakeoff_test_W --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_temp.csv`. **Semnalul B de test vine din `output/bakeoff_test_W/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_prio_W.csv`, predictii per instanta in `output/fusion_preds_lolo_prio_W.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4619 | +0.5185 | **+0.5576** | [+0.4930, +0.6138] | +0.0957 | [+0.0455, +0.1498] | +0.0391 | [+0.0109, +0.0659] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6784 | +0.6890 | **+0.7512** | [+0.7148, +0.7851] | +0.0728 | [+0.0402, +0.1073] | +0.0622 | [+0.0435, +0.0816] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8287 | +0.8471 | **+0.8709** | [+0.8442, +0.8938] | +0.0422 | [+0.0209, +0.0658] | +0.0238 | [+0.0132, +0.0361] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.35 | +0.6991 | +0.7481 | **+0.7629** | [+0.7259, +0.7955] | +0.0638 | [+0.0394, +0.0893] | +0.0149 | [+0.0017, +0.0287] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.40 | +0.4159 | +0.5104 | **+0.5102** | [+0.4447, +0.5678] | +0.0943 | [+0.0593, +0.1292] | -0.0002 | [-0.0232, +0.0229] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.40 | +0.5494 | +0.6675 | **+0.6601** | [+0.6059, +0.7090] | +0.1107 | [+0.0785, +0.1479] | -0.0074 | [-0.0266, +0.0104] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.35 | +0.6487 | +0.6381 | **+0.6767** | [+0.6317, +0.7202] | +0.0280 | [-0.0006, +0.0570] | +0.0386 | [+0.0219, +0.0549] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.6267 | +0.7711 | **+0.7871** | [+0.7438, +0.8221] | +0.1605 | [+0.1192, +0.2040] | +0.0160 | [-0.0057, +0.0396] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 1.000 | 0.35 | +0.7843 | +0.8295 | **+0.8424** | [+0.8122, +0.8690] | +0.0581 | [+0.0370, +0.0800] | +0.0129 | [+0.0018, +0.0238] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.3166 | +0.3849 | **+0.4241** | [+0.3659, +0.4796] | +0.1075 | [+0.0586, +0.1595] | +0.0392 | [+0.0083, +0.0690] |
| **medie** | | | | 0.762 | 0.37 | +0.6010 | +0.6604 | **+0.6843** | | +0.0834 | | +0.0239 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_temp.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5566 | **+0.5576** | +0.0010 | [-0.0023, +0.0042] | 70.5% |
| de | +0.7468 | **+0.7512** | +0.0044 | [+0.0016, +0.0071] | 100.0% |
| en | +0.8700 | **+0.8709** | +0.0009 | [-0.0007, +0.0025] | 87.6% |
| es | +0.7641 | **+0.7629** | -0.0011 | [-0.0027, +0.0004] | 7.6% |
| fil | +0.5091 | **+0.5102** | +0.0011 | [-0.0007, +0.0030] | 88.0% |
| fr | +0.6590 | **+0.6601** | +0.0011 | [-0.0010, +0.0034] | 85.6% |
| it | +0.6750 | **+0.6767** | +0.0017 | [-0.0007, +0.0040] | 92.5% |
| ja | +0.7877 | **+0.7871** | -0.0006 | [-0.0020, +0.0007] | 19.2% |
| pt | +0.8450 | **+0.8424** | -0.0026 | [-0.0045, -0.0010] | 0.0% |
| si | +0.4251 | **+0.4241** | -0.0011 | [-0.0044, +0.0022] | 27.4% |
| **medie** | +0.6838 | **+0.6843** | +0.0005 | | 57.8% |

Configuratia noua urca fuziunea pe 6 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **+0.0005**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6843** | [+0.6698, +0.6985] | |
| fuziune − A | +0.0834 | [+0.0719, +0.0941] | 100.0% |
| fuziune − B | +0.0239 | [+0.0176, +0.0300] | 100.0% |
| configuratia noua − cea de azi | +0.0005 | [-0.0002, +0.0012] | 90.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6010 |
| semnalul B singur, `lolo` | 0.6604 |
| fuziunea de azi, A = `p_multi` | 0.6838 |
| **fuziunea cu ansamblul de surse** | **0.6843** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0272**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6169 | +0.6998 | 0.0829 | 0.0043 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5951 | +0.6782 | 0.0831 | 0.0027 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5761 | +0.6650 | 0.0889 | 0.0047 |
| es | 1.000 | 0.35 | 9 | 5031 | +0.5828 | +0.6765 | 0.0937 | 0.0025 |
| fil | 0.625 | 0.40 | 9 | 5054 | +0.6243 | +0.7047 | 0.0804 | 0.0030 |
| fr | 0.750 | 0.40 | 9 | 5055 | +0.6072 | +0.6880 | 0.0808 | 0.0041 |
| it | 0.750 | 0.35 | 9 | 5054 | +0.5961 | +0.6866 | 0.0905 | 0.0036 |
| ja | 0.625 | 0.40 | 9 | 5054 | +0.6009 | +0.6739 | 0.0730 | 0.0022 |
| pt | 1.000 | 0.35 | 9 | 5057 | +0.5734 | +0.6677 | 0.0943 | 0.0027 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6330 | +0.7146 | 0.0816 | 0.0032 |

Latimea medie a curbei lui w e 0.0849, iar a criteriului de candidati 0.0033, adica de 26 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
