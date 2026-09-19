# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-18 12:25:47 de `fuse_ab.py --arm lolo --fit test --tag src --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_fittest_lemma.csv`. Date brute: `output/fusion_lolo_src.csv`, predictii per instanta in `output/fusion_preds_lolo_src.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 1 puncte, de la 0.000 la 0.000.

Setul de trasaturi e fixat la `fert_inloc`, prin argument si nu prin scor: lungimea in caractere nu e comparabila intre sisteme de scriere, o tinta japoneza avand 3.59 caractere si una italiana 8.78, iar numarul de subword-uri e prin constructie in aceeasi unitate peste tot. Argumentul nu foloseste nicio eticheta.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 1 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.000 | 0.35 | +0.4461 | +0.4829 | **+0.5314** | [+0.4684, +0.5897] | +0.0853 | [+0.0288, +0.1437] | +0.0485 | [+0.0177, +0.0781] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.000 | 0.35 | +0.6502 | +0.6544 | **+0.7191** | [+0.6801, +0.7565] | +0.0689 | [+0.0349, +0.1058] | +0.0647 | [+0.0464, +0.0836] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.000 | 0.35 | +0.8156 | +0.8377 | **+0.8675** | [+0.8394, +0.8918] | +0.0519 | [+0.0301, +0.0771] | +0.0298 | [+0.0181, +0.0428] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.000 | 0.40 | +0.6650 | +0.7432 | **+0.7499** | [+0.7121, +0.7849] | +0.0849 | [+0.0608, +0.1092] | +0.0068 | [-0.0070, +0.0213] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.000 | 0.35 | +0.4147 | +0.5190 | **+0.5204** | [+0.4542, +0.5819] | +0.1057 | [+0.0654, +0.1465] | +0.0014 | [-0.0186, +0.0227] |
| fr | `qwen35-9b-8bit` | 566 | 191 | 0.000 | 0.35 | +0.5406 | +0.5440 | **+0.5856** | [+0.5326, +0.6372] | +0.0451 | [+0.0035, +0.0908] | +0.0416 | [+0.0188, +0.0655] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.000 | 0.35 | +0.6288 | +0.6106 | **+0.6544** | [+0.6080, +0.7002] | +0.0256 | [-0.0050, +0.0571] | +0.0438 | [+0.0270, +0.0616] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.000 | 0.40 | +0.5880 | +0.7676 | **+0.7735** | [+0.7298, +0.8099] | +0.1855 | [+0.1462, +0.2272] | +0.0058 | [-0.0137, +0.0257] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.000 | 0.35 | +0.7684 | +0.8222 | **+0.8373** | [+0.8037, +0.8649] | +0.0689 | [+0.0459, +0.0916] | +0.0151 | [+0.0036, +0.0265] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.000 | 0.35 | +0.2352 | +0.3407 | **+0.3519** | [+0.3001, +0.4044] | +0.1168 | [+0.0700, +0.1631] | +0.0113 | [-0.0135, +0.0371] |
| **medie** | | | | 0.000 | 0.36 | +0.5753 | +0.6322 | **+0.6591** | | +0.0839 | | +0.0269 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_fittest_lemma.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5305 | **+0.5314** | +0.0009 | [-0.0024, +0.0044] | 71.1% |
| de | +0.7160 | **+0.7191** | +0.0032 | [-0.0005, +0.0065] | 96.0% |
| en | +0.8674 | **+0.8675** | +0.0001 | [-0.0012, +0.0015] | 58.8% |
| es | +0.7531 | **+0.7499** | -0.0032 | [-0.0057, -0.0007] | 0.7% |
| fil | +0.5186 | **+0.5204** | +0.0018 | [-0.0006, +0.0040] | 93.5% |
| fr | +0.5823 | **+0.5856** | +0.0034 | [+0.0007, +0.0062] | 99.2% |
| it | +0.6565 | **+0.6544** | -0.0020 | [-0.0041, +0.0001] | 2.8% |
| ja | +0.7616 | **+0.7735** | +0.0119 | [+0.0000, +0.0240] | 97.5% |
| pt | +0.8388 | **+0.8373** | -0.0015 | [-0.0029, -0.0001] | 1.9% |
| si | +0.3430 | **+0.3519** | +0.0089 | [-0.0016, +0.0189] | 95.7% |
| **medie** | +0.6568 | **+0.6591** | +0.0023 | | 61.7% |

Configuratia noua urca fuziunea pe 7 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **+0.0023**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6591** | [+0.6442, +0.6736] | |
| fuziune − A | +0.0838 | [+0.0710, +0.0958] | 100.0% |
| fuziune − B | +0.0269 | [+0.0206, +0.0332] | 100.0% |
| configuratia noua − cea de azi | +0.0023 | [+0.0006, +0.0040] | 99.5% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5753 |
| semnalul B singur, `lolo` | 0.6322 |
| fuziunea de azi, A = `p_multi` | 0.6568 |
| **fuziunea cu ansamblul de surse** | **0.6591** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0020**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.000 | 0.35 | 9 | 5161 | +0.5896 | +0.6741 | 0.0845 | 0.0000 |
| de | 0.000 | 0.35 | 9 | 5036 | +0.5669 | +0.6532 | 0.0863 | 0.0000 |
| en | 0.000 | 0.35 | 9 | 5036 | +0.5486 | +0.6368 | 0.0882 | 0.0000 |
| es | 0.000 | 0.40 | 9 | 5013 | +0.5653 | +0.6497 | 0.0844 | 0.0000 |
| fil | 0.000 | 0.35 | 9 | 5038 | +0.5931 | +0.6828 | 0.0897 | 0.0000 |
| fr | 0.000 | 0.35 | 9 | 5040 | +0.5791 | +0.6681 | 0.0890 | 0.0000 |
| it | 0.000 | 0.35 | 9 | 5044 | +0.5693 | +0.6604 | 0.0911 | 0.0000 |
| ja | 0.000 | 0.40 | 9 | 5036 | +0.5738 | +0.6470 | 0.0732 | 0.0000 |
| pt | 0.000 | 0.35 | 9 | 5044 | +0.5538 | +0.6401 | 0.0863 | 0.0000 |
| si | 0.000 | 0.35 | 9 | 5006 | +0.6130 | +0.7015 | 0.0885 | 0.0000 |

Latimea medie a curbei lui w e 0.0861, iar a criteriului de candidati 0.0000, adica de inf ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
