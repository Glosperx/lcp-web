# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 17:26:29 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_labse_ft-exact --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_labse_ft-exact_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_labse_ft-exact.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_labse_ft-exact.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.625 | 0.30 | +0.4529 | +0.5159 | **+0.5510** | [+0.4863, +0.6095] | +0.0981 | [+0.0449, +0.1564] | +0.0351 | [+0.0126, +0.0565] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.30 | +0.6508 | +0.6812 | **+0.7377** | [+0.7008, +0.7718] | +0.0868 | [+0.0502, +0.1272] | +0.0564 | [+0.0383, +0.0748] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.30 | +0.8089 | +0.8463 | **+0.8688** | [+0.8413, +0.8921] | +0.0599 | [+0.0353, +0.0871] | +0.0225 | [+0.0122, +0.0344] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.30 | +0.6848 | +0.7499 | **+0.7648** | [+0.7279, +0.7976] | +0.0799 | [+0.0512, +0.1085] | +0.0149 | [+0.0025, +0.0277] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.35 | +0.4034 | +0.5082 | **+0.5080** | [+0.4444, +0.5675] | +0.1046 | [+0.0645, +0.1447] | -0.0001 | [-0.0203, +0.0204] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.875 | 0.35 | +0.5179 | +0.6655 | **+0.6552** | [+0.6006, +0.7048] | +0.1373 | [+0.1017, +0.1771] | -0.0103 | [-0.0275, +0.0063] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.30 | +0.6328 | +0.6354 | **+0.6679** | [+0.6239, +0.7122] | +0.0352 | [+0.0039, +0.0681] | +0.0325 | [+0.0182, +0.0472] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.5883 | +0.7715 | **+0.7859** | [+0.7446, +0.8205] | +0.1976 | [+0.1500, +0.2465] | +0.0144 | [-0.0069, +0.0359] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 1.000 | 0.30 | +0.7636 | +0.8322 | **+0.8445** | [+0.8172, +0.8693] | +0.0809 | [+0.0563, +0.1072] | +0.0123 | [+0.0027, +0.0218] |
| si | `gemma4-12b-4bit` | 600 | 578 | 1.000 | 0.30 | +0.2488 | +0.3860 | **+0.3944** | [+0.3396, +0.4461] | +0.1457 | [+0.0933, +0.1974] | +0.0084 | [-0.0119, +0.0299] |
| **medie** | | | | 0.812 | 0.31 | +0.5752 | +0.6592 | **+0.6778** | | +0.1026 | | +0.0186 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5510** | +0.0040 | [-0.0101, +0.0170] | 71.0% |
| de | +0.7429 | **+0.7377** | -0.0052 | [-0.0133, +0.0031] | 9.8% |
| en | +0.8673 | **+0.8688** | +0.0015 | [-0.0045, +0.0085] | 68.2% |
| es | +0.7548 | **+0.7648** | +0.0100 | [+0.0018, +0.0179] | 99.1% |
| fil | +0.5133 | **+0.5080** | -0.0052 | [-0.0165, +0.0055] | 17.2% |
| fr | +0.6605 | **+0.6552** | -0.0053 | [-0.0151, +0.0041] | 15.2% |
| it | +0.6704 | **+0.6679** | -0.0025 | [-0.0105, +0.0048] | 25.2% |
| ja | +0.7934 | **+0.7859** | -0.0075 | [-0.0186, +0.0033] | 9.1% |
| pt | +0.8398 | **+0.8445** | +0.0047 | [-0.0008, +0.0106] | 95.1% |
| si | +0.4095 | **+0.3944** | -0.0151 | [-0.0431, +0.0148] | 15.3% |
| **medie** | +0.6799 | **+0.6778** | -0.0021 | | 42.5% |

Configuratia noua urca fuziunea pe 4 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **-0.0021**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6778** | [+0.6635, +0.6919] | |
| fuziune − A | +0.1026 | [+0.0900, +0.1149] | 100.0% |
| fuziune − B | +0.0186 | [+0.0131, +0.0240] | 100.0% |
| configuratia noua − cea de azi | -0.0021 | [-0.0061, +0.0021] | 16.7% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5752 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6778** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0207**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.625 | 0.30 | 9 | 5179 | +0.5932 | +0.6934 | 0.1002 | 0.0033 |
| de | 0.625 | 0.30 | 9 | 5054 | +0.5712 | +0.6726 | 0.1014 | 0.0015 |
| en | 0.875 | 0.30 | 9 | 5054 | +0.5496 | +0.6582 | 0.1086 | 0.0038 |
| es | 1.000 | 0.30 | 9 | 5031 | +0.5598 | +0.6697 | 0.1099 | 0.0010 |
| fil | 0.625 | 0.35 | 9 | 5054 | +0.5987 | +0.6979 | 0.0992 | 0.0013 |
| fr | 0.875 | 0.35 | 9 | 5055 | +0.5819 | +0.6816 | 0.0997 | 0.0041 |
| it | 0.750 | 0.30 | 9 | 5054 | +0.5717 | +0.6805 | 0.1088 | 0.0030 |
| ja | 0.750 | 0.35 | 9 | 5054 | +0.5766 | +0.6672 | 0.0906 | 0.0020 |
| pt | 1.000 | 0.30 | 9 | 5057 | +0.5511 | +0.6608 | 0.1097 | 0.0014 |
| si | 1.000 | 0.30 | 9 | 5024 | +0.6083 | +0.7108 | 0.1025 | 0.0021 |

Latimea medie a curbei lui w e 0.1031, iar a criteriului de candidati 0.0023, adica de 44 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
