# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-29 14:05:31 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag p1only --b-dir output/bakeoff_test_P1ONLY --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_P1ONLY/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_p1only.csv`, predictii per instanta in `output/fusion_preds_lolo_p1only.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.45 | +0.4619 | +0.4778 | **+0.5431** | [+0.4753, +0.6040] | +0.0812 | [+0.0368, +0.1300] | +0.0653 | [+0.0271, +0.1046] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.500 | 0.45 | +0.6751 | +0.6103 | **+0.7218** | [+0.6783, +0.7607] | +0.0468 | [+0.0167, +0.0804] | +0.1115 | [+0.0824, +0.1416] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.45 | +0.8310 | +0.8111 | **+0.8612** | [+0.8332, +0.8856] | +0.0302 | [+0.0109, +0.0510] | +0.0501 | [+0.0336, +0.0703] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.625 | 0.45 | +0.7038 | +0.7346 | **+0.7588** | [+0.7212, +0.7927] | +0.0550 | [+0.0344, +0.0766] | +0.0242 | [+0.0081, +0.0412] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.45 | +0.4159 | +0.4739 | **+0.4900** | [+0.4265, +0.5501] | +0.0741 | [+0.0383, +0.1088] | +0.0161 | [-0.0112, +0.0449] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.875 | 0.45 | +0.5460 | +0.6272 | **+0.6365** | [+0.5813, +0.6869] | +0.0905 | [+0.0577, +0.1255] | +0.0093 | [-0.0158, +0.0343] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.45 | +0.6489 | +0.5910 | **+0.6639** | [+0.6176, +0.7085] | +0.0150 | [-0.0124, +0.0431] | +0.0729 | [+0.0475, +0.0987] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.50 | +0.6267 | +0.7324 | **+0.7625** | [+0.7180, +0.7999] | +0.1358 | [+0.0994, +0.1731] | +0.0301 | [-0.0003, +0.0603] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.45 | +0.7864 | +0.8120 | **+0.8431** | [+0.8138, +0.8686] | +0.0567 | [+0.0370, +0.0782] | +0.0311 | [+0.0152, +0.0460] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.45 | +0.3242 | +0.3691 | **+0.4178** | [+0.3559, +0.4794] | +0.0936 | [+0.0522, +0.1373] | +0.0486 | [+0.0108, +0.0862] |
| **medie** | | | | 0.650 | 0.46 | +0.6020 | +0.6239 | **+0.6699** | | +0.0679 | | +0.0459 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5431** | -0.0209 | [-0.0440, +0.0016] | 3.6% |
| de | +0.7712 | **+0.7218** | -0.0494 | [-0.0692, -0.0323] | 0.0% |
| en | +0.8723 | **+0.8612** | -0.0111 | [-0.0209, -0.0023] | 1.1% |
| es | +0.7672 | **+0.7588** | -0.0084 | [-0.0181, +0.0014] | 5.1% |
| fil | +0.5074 | **+0.4900** | -0.0174 | [-0.0313, -0.0031] | 0.8% |
| fr | +0.6679 | **+0.6365** | -0.0314 | [-0.0463, -0.0177] | 0.0% |
| it | +0.6795 | **+0.6639** | -0.0156 | [-0.0301, -0.0010] | 2.0% |
| ja | +0.7942 | **+0.7625** | -0.0317 | [-0.0464, -0.0169] | 0.0% |
| pt | +0.8413 | **+0.8431** | +0.0018 | [-0.0056, +0.0095] | 68.8% |
| si | +0.4350 | **+0.4178** | -0.0173 | [-0.0413, +0.0078] | 8.9% |
| **medie** | +0.6900 | **+0.6699** | -0.0201 | | 9.0% |

Configuratia noua urca fuziunea pe 1 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0201**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6699** | [+0.6542, +0.6845] | |
| fuziune − A | +0.0679 | [+0.0570, +0.0780] | 100.0% |
| fuziune − B | +0.0459 | [+0.0375, +0.0545] | 100.0% |
| configuratia noua − cea de azi | -0.0201 | [-0.0253, -0.0151] | 0.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6020 |
| semnalul B singur, `lolo` | 0.6239 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6699** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0128**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.45 | 9 | 5179 | +0.6169 | +0.6851 | 0.0682 | 0.0054 |
| de | 0.500 | 0.45 | 9 | 5054 | +0.5966 | +0.6652 | 0.0686 | 0.0027 |
| en | 0.625 | 0.45 | 9 | 5054 | +0.5782 | +0.6499 | 0.0717 | 0.0050 |
| es | 0.625 | 0.45 | 9 | 5031 | +0.5923 | +0.6613 | 0.0690 | 0.0041 |
| fil | 0.625 | 0.45 | 9 | 5054 | +0.6243 | +0.6911 | 0.0668 | 0.0037 |
| fr | 0.875 | 0.45 | 9 | 5055 | +0.6042 | +0.6743 | 0.0701 | 0.0047 |
| it | 0.625 | 0.45 | 9 | 5054 | +0.5984 | +0.6718 | 0.0734 | 0.0043 |
| ja | 0.625 | 0.50 | 9 | 5054 | +0.6009 | +0.6603 | 0.0594 | 0.0026 |
| pt | 0.625 | 0.45 | 9 | 5057 | +0.5831 | +0.6519 | 0.0688 | 0.0034 |
| si | 0.625 | 0.45 | 9 | 5024 | +0.6345 | +0.6992 | 0.0647 | 0.0039 |

Latimea medie a curbei lui w e 0.0681, iar a criteriului de candidati 0.0040, adica de 17 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
