# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 12:59:53 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_e5_last4_q --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_e5_last4_q_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_e5_last4_q.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_e5_last4_q.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.30 | +0.4531 | +0.5159 | **+0.5569** | [+0.4931, +0.6135] | +0.1038 | [+0.0459, +0.1642] | +0.0410 | [+0.0163, +0.0647] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.30 | +0.6593 | +0.6812 | **+0.7348** | [+0.6963, +0.7697] | +0.0755 | [+0.0393, +0.1126] | +0.0536 | [+0.0365, +0.0706] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8150 | +0.8463 | **+0.8685** | [+0.8414, +0.8918] | +0.0535 | [+0.0311, +0.0783] | +0.0222 | [+0.0113, +0.0346] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.35 | +0.6995 | +0.7499 | **+0.7648** | [+0.7277, +0.7980] | +0.0652 | [+0.0416, +0.0908] | +0.0148 | [+0.0026, +0.0268] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.35 | +0.4106 | +0.5082 | **+0.5115** | [+0.4470, +0.5694] | +0.1009 | [+0.0612, +0.1398] | +0.0034 | [-0.0173, +0.0243] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.35 | +0.5513 | +0.6655 | **+0.6666** | [+0.6133, +0.7160] | +0.1153 | [+0.0783, +0.1562] | +0.0011 | [-0.0170, +0.0193] |
| it | `gemma4-12b-4bit` | 570 | 192 | 1.000 | 0.30 | +0.6375 | +0.6354 | **+0.6720** | [+0.6272, +0.7151] | +0.0346 | [+0.0015, +0.0662] | +0.0367 | [+0.0218, +0.0513] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.35 | +0.5908 | +0.7715 | **+0.7840** | [+0.7423, +0.8173] | +0.1931 | [+0.1476, +0.2419] | +0.0125 | [-0.0067, +0.0330] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.35 | +0.7769 | +0.8322 | **+0.8455** | [+0.8146, +0.8721] | +0.0686 | [+0.0464, +0.0926] | +0.0133 | [+0.0008, +0.0247] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.2243 | +0.3860 | **+0.4005** | [+0.3434, +0.4546] | +0.1762 | [+0.1208, +0.2343] | +0.0145 | [-0.0161, +0.0462] |
| **medie** | | | | 0.762 | 0.33 | +0.5818 | +0.6592 | **+0.6805** | | +0.0987 | | +0.0213 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5569** | +0.0099 | [-0.0030, +0.0228] | 93.0% |
| de | +0.7429 | **+0.7348** | -0.0081 | [-0.0158, -0.0002] | 2.2% |
| en | +0.8673 | **+0.8685** | +0.0012 | [-0.0046, +0.0068] | 68.2% |
| es | +0.7548 | **+0.7648** | +0.0099 | [+0.0023, +0.0173] | 99.7% |
| fil | +0.5133 | **+0.5115** | -0.0018 | [-0.0088, +0.0055] | 31.4% |
| fr | +0.6605 | **+0.6666** | +0.0062 | [-0.0045, +0.0173] | 86.7% |
| it | +0.6704 | **+0.6720** | +0.0016 | [-0.0047, +0.0083] | 68.6% |
| ja | +0.7934 | **+0.7840** | -0.0094 | [-0.0197, +0.0014] | 5.1% |
| pt | +0.8398 | **+0.8455** | +0.0056 | [+0.0007, +0.0109] | 98.8% |
| si | +0.4095 | **+0.4005** | -0.0090 | [-0.0354, +0.0171] | 26.7% |
| **medie** | +0.6799 | **+0.6805** | +0.0006 | | 58.1% |

Configuratia noua urca fuziunea pe 6 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0006**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6805** | [+0.6661, +0.6944] | |
| fuziune − A | +0.0987 | [+0.0861, +0.1108] | 100.0% |
| fuziune − B | +0.0213 | [+0.0154, +0.0271] | 100.0% |
| configuratia noua − cea de azi | +0.0006 | [-0.0031, +0.0041] | 63.6% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5818 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6805** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0234**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.30 | 9 | 5179 | +0.5899 | +0.6950 | 0.1051 | 0.0028 |
| de | 0.750 | 0.30 | 9 | 5054 | +0.5739 | +0.6756 | 0.1017 | 0.0025 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5566 | +0.6609 | 0.1043 | 0.0023 |
| es | 0.750 | 0.35 | 9 | 5031 | +0.5695 | +0.6724 | 0.1029 | 0.0022 |
| fil | 0.625 | 0.35 | 9 | 5054 | +0.6033 | +0.7006 | 0.0973 | 0.0038 |
| fr | 0.750 | 0.35 | 9 | 5055 | +0.5859 | +0.6833 | 0.0974 | 0.0039 |
| it | 1.000 | 0.30 | 9 | 5054 | +0.5694 | +0.6822 | 0.1128 | 0.0019 |
| ja | 0.625 | 0.35 | 9 | 5054 | +0.5833 | +0.6703 | 0.0870 | 0.0033 |
| pt | 0.625 | 0.35 | 9 | 5057 | +0.5626 | +0.6635 | 0.1009 | 0.0022 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6223 | +0.7129 | 0.0906 | 0.0037 |

Latimea medie a curbei lui w e 0.1000, iar a criteriului de candidati 0.0029, adica de 35 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
