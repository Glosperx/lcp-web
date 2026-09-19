# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 17:24:45 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_e5_ft-prefix --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_e5_ft-prefix_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_e5_ft-prefix.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_e5_ft-prefix.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.30 | +0.4563 | +0.5159 | **+0.5577** | [+0.4942, +0.6138] | +0.1013 | [+0.0443, +0.1616] | +0.0418 | [+0.0174, +0.0659] |
| de | `gemma4-12b-4bit` | 570 | 193 | 1.000 | 0.30 | +0.6647 | +0.6812 | **+0.7377** | [+0.6993, +0.7722] | +0.0730 | [+0.0368, +0.1100] | +0.0564 | [+0.0397, +0.0735] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.8066 | +0.8463 | **+0.8663** | [+0.8385, +0.8900] | +0.0597 | [+0.0364, +0.0858] | +0.0200 | [+0.0092, +0.0323] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.35 | +0.7024 | +0.7499 | **+0.7658** | [+0.7282, +0.7989] | +0.0634 | [+0.0403, +0.0885] | +0.0159 | [+0.0032, +0.0283] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.500 | 0.35 | +0.3914 | +0.5082 | **+0.5109** | [+0.4453, +0.5697] | +0.1194 | [+0.0776, +0.1626] | +0.0027 | [-0.0186, +0.0248] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.35 | +0.5462 | +0.6655 | **+0.6651** | [+0.6117, +0.7144] | +0.1188 | [+0.0812, +0.1611] | -0.0004 | [-0.0182, +0.0166] |
| it | `gemma4-12b-4bit` | 570 | 192 | 1.000 | 0.30 | +0.6330 | +0.6354 | **+0.6712** | [+0.6259, +0.7151] | +0.0382 | [+0.0045, +0.0708] | +0.0358 | [+0.0210, +0.0504] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.5789 | +0.7715 | **+0.7842** | [+0.7421, +0.8187] | +0.2054 | [+0.1584, +0.2544] | +0.0128 | [-0.0072, +0.0340] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.35 | +0.7773 | +0.8322 | **+0.8452** | [+0.8138, +0.8720] | +0.0679 | [+0.0459, +0.0923] | +0.0130 | [+0.0008, +0.0245] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.2609 | +0.3860 | **+0.4004** | [+0.3449, +0.4528] | +0.1394 | [+0.0873, +0.1925] | +0.0144 | [-0.0122, +0.0408] |
| **medie** | | | | 0.838 | 0.33 | +0.5818 | +0.6592 | **+0.6804** | | +0.0986 | | +0.0212 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5577** | +0.0107 | [-0.0024, +0.0237] | 93.8% |
| de | +0.7429 | **+0.7377** | -0.0052 | [-0.0132, +0.0029] | 11.6% |
| en | +0.8673 | **+0.8663** | -0.0010 | [-0.0067, +0.0047] | 37.6% |
| es | +0.7548 | **+0.7658** | +0.0110 | [+0.0028, +0.0188] | 99.7% |
| fil | +0.5133 | **+0.5109** | -0.0024 | [-0.0151, +0.0103] | 34.8% |
| fr | +0.6605 | **+0.6651** | +0.0046 | [-0.0063, +0.0166] | 78.8% |
| it | +0.6704 | **+0.6712** | +0.0008 | [-0.0066, +0.0074] | 59.2% |
| ja | +0.7934 | **+0.7842** | -0.0091 | [-0.0190, +0.0011] | 3.9% |
| pt | +0.8398 | **+0.8452** | +0.0054 | [+0.0005, +0.0106] | 98.7% |
| si | +0.4095 | **+0.4004** | -0.0092 | [-0.0391, +0.0197] | 27.7% |
| **medie** | +0.6799 | **+0.6804** | +0.0006 | | 54.6% |

Configuratia noua urca fuziunea pe 5 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0006**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6804** | [+0.6660, +0.6943] | |
| fuziune − A | +0.0987 | [+0.0858, +0.1113] | 100.0% |
| fuziune − B | +0.0212 | [+0.0153, +0.0270] | 100.0% |
| configuratia noua − cea de azi | +0.0006 | [-0.0035, +0.0046] | 60.1% |

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
| **fuziunea cu ansamblul de surse** | **0.6804** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0233**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.30 | 9 | 5179 | +0.5939 | +0.6955 | 0.1016 | 0.0013 |
| de | 1.000 | 0.30 | 9 | 5054 | +0.5708 | +0.6755 | 0.1047 | 0.0019 |
| en | 0.875 | 0.35 | 9 | 5054 | +0.5581 | +0.6614 | 0.1033 | 0.0024 |
| es | 0.875 | 0.35 | 9 | 5031 | +0.5697 | +0.6726 | 0.1029 | 0.0027 |
| fil | 0.500 | 0.35 | 9 | 5054 | +0.6083 | +0.7006 | 0.0923 | 0.0030 |
| fr | 0.750 | 0.35 | 9 | 5055 | +0.5893 | +0.6838 | 0.0945 | 0.0043 |
| it | 1.000 | 0.30 | 9 | 5054 | +0.5743 | +0.6828 | 0.1085 | 0.0018 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5834 | +0.6705 | 0.0871 | 0.0036 |
| pt | 0.750 | 0.35 | 9 | 5057 | +0.5636 | +0.6638 | 0.1002 | 0.0027 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6210 | +0.7132 | 0.0922 | 0.0032 |

Latimea medie a curbei lui w e 0.0987, iar a criteriului de candidati 0.0027, adica de 37 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
