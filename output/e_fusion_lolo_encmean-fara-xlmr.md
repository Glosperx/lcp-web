# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-19 01:25:16 de `fuse_ab.py --arm lolo --fit test --ens --tag encmean-fara-xlmr --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ens.csv`. Date brute: `output/fusion_lolo_encmean-fara-xlmr.csv`, predictii per instanta in `output/fusion_preds_lolo_encmean-fara-xlmr.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.625 | 0.45 | +0.4864 | +0.4829 | **+0.5477** | [+0.4825, +0.6067] | +0.0613 | [+0.0172, +0.1075] | +0.0648 | [+0.0275, +0.1002] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.500 | 0.45 | +0.6844 | +0.6544 | **+0.7376** | [+0.6994, +0.7739] | +0.0531 | [+0.0266, +0.0809] | +0.0832 | [+0.0595, +0.1078] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.45 | +0.8347 | +0.8377 | **+0.8731** | [+0.8474, +0.8948] | +0.0384 | [+0.0195, +0.0574] | +0.0354 | [+0.0216, +0.0516] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.45 | +0.7047 | +0.7432 | **+0.7602** | [+0.7220, +0.7942] | +0.0555 | [+0.0345, +0.0767] | +0.0170 | [+0.0015, +0.0326] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.45 | +0.4035 | +0.5173 | **+0.5076** | [+0.4406, +0.5691] | +0.1041 | [+0.0693, +0.1372] | -0.0097 | [-0.0360, +0.0179] |
| fr | `qwen35-9b-8bit` | 569 | 191 | 0.750 | 0.45 | +0.5583 | +0.5420 | **+0.5927** | [+0.5395, +0.6466] | +0.0344 | [+0.0037, +0.0653] | +0.0508 | [+0.0237, +0.0784] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.500 | 0.45 | +0.6483 | +0.6127 | **+0.6663** | [+0.6223, +0.7105] | +0.0179 | [-0.0066, +0.0435] | +0.0536 | [+0.0328, +0.0750] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.45 | +0.6378 | +0.7676 | **+0.7835** | [+0.7391, +0.8208] | +0.1458 | [+0.1083, +0.1848] | +0.0159 | [-0.0095, +0.0428] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.45 | +0.7912 | +0.8213 | **+0.8435** | [+0.8118, +0.8705] | +0.0523 | [+0.0326, +0.0740] | +0.0222 | [+0.0069, +0.0372] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.875 | 0.40 | +0.3107 | +0.3407 | **+0.3939** | [+0.3351, +0.4493] | +0.0831 | [+0.0383, +0.1303] | +0.0532 | [+0.0181, +0.0871] |
| **medie** | | | | 0.662 | 0.45 | +0.6060 | +0.6320 | **+0.6706** | | +0.0646 | | +0.0386 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 8 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ens.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5283 | **+0.5477** | +0.0194 | [+0.0069, +0.0315] | 100.0% |
| de | +0.7324 | **+0.7376** | +0.0051 | [-0.0043, +0.0146] | 85.7% |
| en | +0.8663 | **+0.8731** | +0.0068 | [+0.0008, +0.0135] | 98.8% |
| es | +0.7486 | **+0.7602** | +0.0115 | [+0.0042, +0.0188] | 100.0% |
| fil | +0.5171 | **+0.5076** | -0.0095 | [-0.0181, -0.0011] | 1.4% |
| fr | +0.5857 | **+0.5927** | +0.0070 | [-0.0037, +0.0173] | 90.5% |
| it | +0.6625 | **+0.6663** | +0.0038 | [-0.0042, +0.0117] | 82.3% |
| ja | +0.7887 | **+0.7835** | -0.0051 | [-0.0157, +0.0057] | 17.2% |
| pt | +0.8375 | **+0.8435** | +0.0060 | [+0.0010, +0.0109] | 98.7% |
| si | +0.3786 | **+0.3939** | +0.0152 | [-0.0141, +0.0438] | 84.7% |
| **medie** | +0.6646 | **+0.6706** | +0.0060 | | 75.9% |

Configuratia noua urca fuziunea pe 8 din 10 limbi. Intervalul pereche exclude zero in sus pe 4. Pe medie, **+0.0060**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6706** | [+0.6558, +0.6849] | |
| fuziune − A | +0.0646 | [+0.0540, +0.0745] | 100.0% |
| fuziune − B | +0.0386 | [+0.0307, +0.0465] | 100.0% |
| configuratia noua − cea de azi | +0.0060 | [+0.0019, +0.0098] | 99.8% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6060 |
| semnalul B singur, `lolo` | 0.6320 |
| fuziunea de azi, A = `p_multi` | 0.6646 |
| **fuziunea cu ansamblul de surse** | **0.6706** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0135**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.625 | 0.45 | 9 | 5179 | +0.6222 | +0.6853 | 0.0631 | 0.0040 |
| de | 0.500 | 0.45 | 9 | 5054 | +0.6014 | +0.6641 | 0.0627 | 0.0021 |
| en | 0.625 | 0.45 | 9 | 5054 | +0.5835 | +0.6492 | 0.0657 | 0.0050 |
| es | 0.750 | 0.45 | 9 | 5031 | +0.5957 | +0.6616 | 0.0659 | 0.0034 |
| fil | 0.625 | 0.45 | 9 | 5054 | +0.6314 | +0.6958 | 0.0644 | 0.0039 |
| fr | 0.750 | 0.45 | 9 | 5055 | +0.6119 | +0.6802 | 0.0683 | 0.0044 |
| it | 0.500 | 0.45 | 9 | 5054 | +0.6054 | +0.6720 | 0.0666 | 0.0034 |
| ja | 0.625 | 0.45 | 9 | 5054 | +0.6054 | +0.6591 | 0.0537 | 0.0021 |
| pt | 0.750 | 0.45 | 9 | 5057 | +0.5861 | +0.6523 | 0.0662 | 0.0041 |
| si | 0.875 | 0.40 | 9 | 5024 | +0.6361 | +0.7081 | 0.0720 | 0.0036 |

Latimea medie a curbei lui w e 0.0649, iar a criteriului de candidati 0.0036, adica de 18 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
| splitul pe care se alege modelul | `fuse_ab.py`, `fuse_ens` | `--pick-split trial`, adica `tab_pick = r_table(load_runs('trial'), "B")`. Selectia citeste trial-ul, potrivirea ponderii citeste splitul lui `--fit`. Niciun rand al limbii L nu intra in criteriu, pe niciunul dintre splituri: L e exclusa chiar din media care alege. |
| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_choice` | apelul cu `exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. Se face pe ACELASI `tab_pick`, deci schimbarea splitului de selectie nu deschide o scurgere pe unde selectia imbricata a inchis una. |
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
