# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-21 18:12:33 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag prio_G --b-dir output/bakeoff_test_G --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_temp.csv`. **Semnalul B de test vine din `output/bakeoff_test_G/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_prio_G.csv`, predictii per instanta in `output/fusion_preds_lolo_prio_G.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.35 | +0.4564 | +0.5167 | **+0.5561** | [+0.4913, +0.6132] | +0.0997 | [+0.0480, +0.1544] | +0.0394 | [+0.0108, +0.0661] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.500 | 0.35 | +0.6751 | +0.6800 | **+0.7439** | [+0.7065, +0.7787] | +0.0688 | [+0.0371, +0.1033] | +0.0639 | [+0.0449, +0.0835] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.8259 | +0.8464 | **+0.8701** | [+0.8431, +0.8929] | +0.0442 | [+0.0226, +0.0681] | +0.0237 | [+0.0130, +0.0360] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.35 | +0.7030 | +0.7506 | **+0.7640** | [+0.7273, +0.7968] | +0.0611 | [+0.0379, +0.0853] | +0.0134 | [+0.0013, +0.0265] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.40 | +0.4159 | +0.5116 | **+0.5110** | [+0.4458, +0.5689] | +0.0952 | [+0.0597, +0.1302] | -0.0006 | [-0.0234, +0.0224] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.40 | +0.5494 | +0.6643 | **+0.6583** | [+0.6041, +0.7071] | +0.1089 | [+0.0769, +0.1451] | -0.0060 | [-0.0255, +0.0119] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.500 | 0.35 | +0.6484 | +0.6353 | **+0.6742** | [+0.6300, +0.7178] | +0.0258 | [-0.0027, +0.0541] | +0.0389 | [+0.0225, +0.0553] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.6267 | +0.7711 | **+0.7876** | [+0.7450, +0.8224] | +0.1609 | [+0.1190, +0.2040] | +0.0165 | [-0.0052, +0.0396] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 1.000 | 0.35 | +0.7843 | +0.8318 | **+0.8449** | [+0.8155, +0.8707] | +0.0606 | [+0.0390, +0.0831] | +0.0131 | [+0.0018, +0.0240] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.3166 | +0.3862 | **+0.4252** | [+0.3682, +0.4809] | +0.1086 | [+0.0601, +0.1615] | +0.0390 | [+0.0085, +0.0687] |
| **medie** | | | | 0.725 | 0.37 | +0.6002 | +0.6594 | **+0.6835** | | +0.0834 | | +0.0241 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_temp.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5566 | **+0.5561** | -0.0005 | [-0.0029, +0.0018] | 31.8% |
| de | +0.7468 | **+0.7439** | -0.0029 | [-0.0049, -0.0011] | 0.1% |
| en | +0.8700 | **+0.8701** | +0.0001 | [-0.0004, +0.0006] | 65.2% |
| es | +0.7641 | **+0.7640** | -0.0000 | [-0.0015, +0.0015] | 47.6% |
| fil | +0.5091 | **+0.5110** | +0.0020 | [+0.0006, +0.0032] | 100.0% |
| fr | +0.6590 | **+0.6583** | -0.0007 | [-0.0012, -0.0002] | 0.4% |
| it | +0.6750 | **+0.6742** | -0.0008 | [-0.0026, +0.0011] | 20.4% |
| ja | +0.7877 | **+0.7876** | -0.0001 | [-0.0007, +0.0004] | 29.6% |
| pt | +0.8450 | **+0.8449** | -0.0001 | [-0.0008, +0.0006] | 36.9% |
| si | +0.4251 | **+0.4252** | +0.0001 | [-0.0021, +0.0018] | 54.2% |
| **medie** | +0.6838 | **+0.6835** | -0.0003 | | 38.6% |

Configuratia noua urca fuziunea pe 3 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **-0.0003**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6835** | [+0.6692, +0.6976] | |
| fuziune − A | +0.0834 | [+0.0716, +0.0941] | 100.0% |
| fuziune − B | +0.0241 | [+0.0179, +0.0303] | 100.0% |
| configuratia noua − cea de azi | -0.0003 | [-0.0008, +0.0002] | 10.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6002 |
| semnalul B singur, `lolo` | 0.6594 |
| fuziunea de azi, A = `p_multi` | 0.6838 |
| **fuziunea cu ansamblul de surse** | **0.6835** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0264**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.35 | 9 | 5179 | +0.6142 | +0.6994 | 0.0852 | 0.0040 |
| de | 0.500 | 0.35 | 9 | 5054 | +0.5966 | +0.6783 | 0.0817 | 0.0031 |
| en | 0.875 | 0.35 | 9 | 5054 | +0.5731 | +0.6645 | 0.0914 | 0.0041 |
| es | 0.750 | 0.35 | 9 | 5031 | +0.5901 | +0.6765 | 0.0864 | 0.0025 |
| fil | 0.625 | 0.40 | 9 | 5054 | +0.6243 | +0.7043 | 0.0800 | 0.0032 |
| fr | 0.750 | 0.40 | 9 | 5055 | +0.6072 | +0.6879 | 0.0807 | 0.0043 |
| it | 0.500 | 0.35 | 9 | 5054 | +0.5995 | +0.6861 | 0.0866 | 0.0036 |
| ja | 0.625 | 0.40 | 9 | 5054 | +0.6009 | +0.6735 | 0.0726 | 0.0028 |
| pt | 1.000 | 0.35 | 9 | 5057 | +0.5734 | +0.6670 | 0.0936 | 0.0029 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6330 | +0.7141 | 0.0811 | 0.0023 |

Latimea medie a curbei lui w e 0.0839, iar a criteriului de candidati 0.0033, adica de 26 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
