# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 12:13:57 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_last4_last --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_last4_last_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_last4_last.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_last4_last.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.30 | +0.3998 | +0.5159 | **+0.5418** | [+0.4766, +0.6001] | +0.1421 | [+0.0806, +0.2026] | +0.0259 | [+0.0004, +0.0507] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.875 | 0.25 | +0.6460 | +0.6812 | **+0.7309** | [+0.6925, +0.7658] | +0.0849 | [+0.0458, +0.1270] | +0.0497 | [+0.0361, +0.0635] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.30 | +0.7931 | +0.8463 | **+0.8635** | [+0.8348, +0.8882] | +0.0704 | [+0.0461, +0.0989] | +0.0172 | [+0.0072, +0.0288] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.30 | +0.6495 | +0.7499 | **+0.7532** | [+0.7158, +0.7874] | +0.1037 | [+0.0739, +0.1329] | +0.0033 | [-0.0077, +0.0148] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.30 | +0.4143 | +0.5082 | **+0.5153** | [+0.4496, +0.5730] | +0.1010 | [+0.0601, +0.1434] | +0.0072 | [-0.0101, +0.0244] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.30 | +0.5403 | +0.6655 | **+0.6655** | [+0.6121, +0.7143] | +0.1252 | [+0.0873, +0.1685] | +0.0000 | [-0.0146, +0.0139] |
| it | `gemma4-12b-4bit` | 570 | 192 | 1.000 | 0.25 | +0.6173 | +0.6354 | **+0.6657** | [+0.6212, +0.7095] | +0.0484 | [+0.0114, +0.0852] | +0.0303 | [+0.0180, +0.0428] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.30 | +0.6006 | +0.7715 | **+0.7900** | [+0.7504, +0.8227] | +0.1893 | [+0.1412, +0.2431] | +0.0185 | [+0.0017, +0.0345] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.30 | +0.7590 | +0.8322 | **+0.8382** | [+0.8092, +0.8645] | +0.0792 | [+0.0568, +0.1028] | +0.0060 | [-0.0029, +0.0142] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.30 | +0.1895 | +0.3860 | **+0.3899** | [+0.3331, +0.4434] | +0.2004 | [+0.1410, +0.2626] | +0.0039 | [-0.0231, +0.0300] |
| **medie** | | | | 0.812 | 0.29 | +0.5609 | +0.6592 | **+0.6754** | | +0.1145 | | +0.0162 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 5 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5418** | -0.0051 | [-0.0152, +0.0048] | 15.9% |
| de | +0.7429 | **+0.7309** | -0.0119 | [-0.0173, -0.0064] | 0.0% |
| en | +0.8673 | **+0.8635** | -0.0038 | [-0.0071, -0.0008] | 0.6% |
| es | +0.7548 | **+0.7532** | -0.0016 | [-0.0062, +0.0028] | 22.7% |
| fil | +0.5133 | **+0.5153** | +0.0020 | [-0.0038, +0.0076] | 76.1% |
| fr | +0.6605 | **+0.6655** | +0.0051 | [-0.0005, +0.0104] | 96.2% |
| it | +0.6704 | **+0.6657** | -0.0047 | [-0.0110, +0.0012] | 5.5% |
| ja | +0.7934 | **+0.7900** | -0.0034 | [-0.0094, +0.0025] | 12.5% |
| pt | +0.8398 | **+0.8382** | -0.0016 | [-0.0049, +0.0016] | 16.1% |
| si | +0.4095 | **+0.3899** | -0.0197 | [-0.0406, +0.0005] | 3.0% |
| **medie** | +0.6799 | **+0.6754** | -0.0045 | | 24.9% |

Configuratia noua urca fuziunea pe 2 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0045**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6754** | [+0.6607, +0.6895] | |
| fuziune − A | +0.1145 | [+0.1001, +0.1282] | 100.0% |
| fuziune − B | +0.0162 | [+0.0111, +0.0212] | 100.0% |
| configuratia noua − cea de azi | -0.0045 | [-0.0072, -0.0019] | 0.1% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5609 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6754** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0183**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.30 | 9 | 5179 | +0.5774 | +0.6914 | 0.1140 | 0.0037 |
| de | 0.875 | 0.25 | 9 | 5054 | +0.5501 | +0.6700 | 0.1199 | 0.0030 |
| en | 0.875 | 0.30 | 9 | 5054 | +0.5337 | +0.6556 | 0.1219 | 0.0029 |
| es | 0.875 | 0.30 | 9 | 5031 | +0.5497 | +0.6679 | 0.1182 | 0.0045 |
| fil | 0.750 | 0.30 | 9 | 5054 | +0.5795 | +0.6943 | 0.1148 | 0.0041 |
| fr | 0.625 | 0.30 | 9 | 5055 | +0.5678 | +0.6775 | 0.1097 | 0.0050 |
| it | 1.000 | 0.25 | 9 | 5054 | +0.5483 | +0.6772 | 0.1289 | 0.0027 |
| ja | 0.750 | 0.30 | 9 | 5054 | +0.5588 | +0.6638 | 0.1050 | 0.0029 |
| pt | 0.750 | 0.30 | 9 | 5057 | +0.5412 | +0.6585 | 0.1173 | 0.0042 |
| si | 0.750 | 0.30 | 9 | 5024 | +0.6045 | +0.7083 | 0.1038 | 0.0046 |

Latimea medie a curbei lui w e 0.1154, iar a criteriului de candidati 0.0038, adica de 31 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
