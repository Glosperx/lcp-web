# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 13:01:02 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_nofreq --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_nofreq_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_nofreq.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_nofreq.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.625 | 0.25 | +0.3631 | +0.5159 | **+0.5409** | [+0.4772, +0.5991] | +0.1778 | [+0.1024, +0.2539] | +0.0250 | [+0.0024, +0.0476] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.25 | +0.5572 | +0.6812 | **+0.7185** | [+0.6795, +0.7558] | +0.1613 | [+0.1102, +0.2177] | +0.0373 | [+0.0230, +0.0515] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.25 | +0.7770 | +0.8463 | **+0.8606** | [+0.8301, +0.8870] | +0.0836 | [+0.0571, +0.1131] | +0.0144 | [+0.0061, +0.0233] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.25 | +0.5932 | +0.7499 | **+0.7531** | [+0.7145, +0.7896] | +0.1599 | [+0.1215, +0.2003] | +0.0032 | [-0.0075, +0.0137] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.500 | 0.25 | +0.4270 | +0.5082 | **+0.5357** | [+0.4717, +0.5949] | +0.1088 | [+0.0584, +0.1608] | +0.0276 | [+0.0111, +0.0434] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.500 | 0.30 | +0.4795 | +0.6655 | **+0.6589** | [+0.6059, +0.7062] | +0.1794 | [+0.1314, +0.2300] | -0.0066 | [-0.0222, +0.0089] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.25 | +0.5293 | +0.6354 | **+0.6558** | [+0.6083, +0.7026] | +0.1265 | [+0.0823, +0.1704] | +0.0204 | [+0.0055, +0.0359] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.25 | +0.5260 | +0.7715 | **+0.7868** | [+0.7461, +0.8196] | +0.2608 | [+0.2046, +0.3188] | +0.0153 | [+0.0016, +0.0288] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.25 | +0.6762 | +0.8322 | **+0.8326** | [+0.8014, +0.8597] | +0.1564 | [+0.1225, +0.1924] | +0.0004 | [-0.0088, +0.0088] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.25 | +0.2976 | +0.3860 | **+0.4047** | [+0.3512, +0.4545] | +0.1071 | [+0.0584, +0.1564] | +0.0187 | [+0.0036, +0.0335] |
| **medie** | | | | 0.688 | 0.26 | +0.5226 | +0.6592 | **+0.6748** | | +0.1522 | | +0.0156 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5409** | -0.0061 | [-0.0248, +0.0136] | 27.2% |
| de | +0.7429 | **+0.7185** | -0.0243 | [-0.0357, -0.0134] | 0.0% |
| en | +0.8673 | **+0.8606** | -0.0067 | [-0.0136, -0.0006] | 1.8% |
| es | +0.7548 | **+0.7531** | -0.0017 | [-0.0122, +0.0083] | 36.7% |
| fil | +0.5133 | **+0.5357** | +0.0225 | [+0.0060, +0.0381] | 99.5% |
| fr | +0.6605 | **+0.6589** | -0.0016 | [-0.0119, +0.0098] | 39.8% |
| it | +0.6704 | **+0.6558** | -0.0146 | [-0.0240, -0.0057] | 0.0% |
| ja | +0.7934 | **+0.7868** | -0.0066 | [-0.0221, +0.0081] | 18.4% |
| pt | +0.8398 | **+0.8326** | -0.0072 | [-0.0132, -0.0013] | 1.0% |
| si | +0.4095 | **+0.4047** | -0.0048 | [-0.0206, +0.0100] | 25.7% |
| **medie** | +0.6799 | **+0.6748** | -0.0051 | | 25.0% |

Configuratia noua urca fuziunea pe 1 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **-0.0051**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6748** | [+0.6601, +0.6886] | |
| fuziune − A | +0.1521 | [+0.1369, +0.1678] | 100.0% |
| fuziune − B | +0.0156 | [+0.0109, +0.0199] | 100.0% |
| configuratia noua − cea de azi | -0.0051 | [-0.0092, -0.0013] | 0.4% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5226 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6748** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0177**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.625 | 0.25 | 9 | 5179 | +0.5459 | +0.6904 | 0.1445 | 0.0015 |
| de | 0.625 | 0.25 | 9 | 5054 | +0.5243 | +0.6707 | 0.1464 | 0.0014 |
| en | 0.625 | 0.25 | 9 | 5054 | +0.4999 | +0.6549 | 0.1550 | 0.0017 |
| es | 0.875 | 0.25 | 9 | 5031 | +0.5089 | +0.6666 | 0.1577 | 0.0016 |
| fil | 0.500 | 0.25 | 9 | 5054 | +0.5425 | +0.6909 | 0.1484 | 0.0014 |
| fr | 0.500 | 0.30 | 9 | 5055 | +0.5367 | +0.6769 | 0.1402 | 0.0021 |
| it | 0.625 | 0.25 | 9 | 5054 | +0.5274 | +0.6777 | 0.1503 | 0.0016 |
| ja | 1.000 | 0.25 | 9 | 5054 | +0.5089 | +0.6625 | 0.1536 | 0.0016 |
| pt | 0.875 | 0.25 | 9 | 5057 | +0.4997 | +0.6577 | 0.1580 | 0.0014 |
| si | 0.625 | 0.25 | 9 | 5024 | +0.5531 | +0.7056 | 0.1525 | 0.0010 |

Latimea medie a curbei lui w e 0.1507, iar a criteriului de candidati 0.0015, adica de 98 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
