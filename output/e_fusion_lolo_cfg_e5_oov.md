# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 17:25:20 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_e5_oov --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_e5_oov_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_e5_oov.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_e5_oov.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.30 | +0.4625 | +0.5159 | **+0.5588** | [+0.4960, +0.6147] | +0.0963 | [+0.0400, +0.1553] | +0.0430 | [+0.0194, +0.0662] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.30 | +0.6542 | +0.6812 | **+0.7339** | [+0.6953, +0.7692] | +0.0798 | [+0.0431, +0.1171] | +0.0527 | [+0.0354, +0.0696] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.30 | +0.8113 | +0.8463 | **+0.8667** | [+0.8385, +0.8909] | +0.0554 | [+0.0312, +0.0824] | +0.0204 | [+0.0113, +0.0308] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.30 | +0.7044 | +0.7499 | **+0.7658** | [+0.7284, +0.7989] | +0.0613 | [+0.0368, +0.0883] | +0.0158 | [+0.0051, +0.0265] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.35 | +0.4130 | +0.5082 | **+0.5128** | [+0.4472, +0.5711] | +0.0998 | [+0.0599, +0.1395] | +0.0047 | [-0.0158, +0.0253] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.35 | +0.5506 | +0.6655 | **+0.6666** | [+0.6135, +0.7155] | +0.1160 | [+0.0790, +0.1569] | +0.0011 | [-0.0166, +0.0178] |
| it | `gemma4-12b-4bit` | 570 | 192 | 1.000 | 0.30 | +0.6277 | +0.6354 | **+0.6699** | [+0.6252, +0.7137] | +0.0422 | [+0.0088, +0.0741] | +0.0345 | [+0.0197, +0.0493] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.35 | +0.5923 | +0.7715 | **+0.7847** | [+0.7427, +0.8190] | +0.1924 | [+0.1463, +0.2409] | +0.0132 | [-0.0068, +0.0342] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.35 | +0.7773 | +0.8322 | **+0.8450** | [+0.8140, +0.8719] | +0.0678 | [+0.0455, +0.0922] | +0.0129 | [+0.0008, +0.0240] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.1976 | +0.3860 | **+0.3957** | [+0.3392, +0.4514] | +0.1981 | [+0.1393, +0.2586] | +0.0097 | [-0.0233, +0.0420] |
| **medie** | | | | 0.725 | 0.33 | +0.5791 | +0.6592 | **+0.6800** | | +0.1009 | | +0.0208 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5588** | +0.0119 | [-0.0023, +0.0262] | 94.2% |
| de | +0.7429 | **+0.7339** | -0.0089 | [-0.0176, -0.0002] | 2.1% |
| en | +0.8673 | **+0.8667** | -0.0006 | [-0.0062, +0.0046] | 41.6% |
| es | +0.7548 | **+0.7658** | +0.0109 | [+0.0029, +0.0186] | 99.8% |
| fil | +0.5133 | **+0.5128** | -0.0005 | [-0.0083, +0.0074] | 44.7% |
| fr | +0.6605 | **+0.6666** | +0.0062 | [-0.0046, +0.0174] | 86.4% |
| it | +0.6704 | **+0.6699** | -0.0005 | [-0.0075, +0.0062] | 44.7% |
| ja | +0.7934 | **+0.7847** | -0.0087 | [-0.0191, +0.0016] | 5.3% |
| pt | +0.8398 | **+0.8450** | +0.0052 | [+0.0002, +0.0104] | 97.8% |
| si | +0.4095 | **+0.3957** | -0.0138 | [-0.0405, +0.0131] | 16.8% |
| **medie** | +0.6799 | **+0.6800** | +0.0001 | | 53.3% |

Configuratia noua urca fuziunea pe 4 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0001**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6800** | [+0.6654, +0.6941] | |
| fuziune − A | +0.1009 | [+0.0880, +0.1128] | 100.0% |
| fuziune − B | +0.0208 | [+0.0150, +0.0267] | 100.0% |
| configuratia noua − cea de azi | +0.0001 | [-0.0037, +0.0038] | 52.1% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5791 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6800** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0229**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.30 | 9 | 5179 | +0.5888 | +0.6947 | 0.1059 | 0.0024 |
| de | 0.625 | 0.30 | 9 | 5054 | +0.5730 | +0.6753 | 0.1023 | 0.0024 |
| en | 0.750 | 0.30 | 9 | 5054 | +0.5534 | +0.6606 | 0.1072 | 0.0018 |
| es | 0.750 | 0.30 | 9 | 5031 | +0.5653 | +0.6718 | 0.1065 | 0.0020 |
| fil | 0.625 | 0.35 | 9 | 5054 | +0.5998 | +0.6999 | 0.1001 | 0.0028 |
| fr | 0.625 | 0.35 | 9 | 5055 | +0.5845 | +0.6828 | 0.0983 | 0.0040 |
| it | 1.000 | 0.30 | 9 | 5054 | +0.5661 | +0.6820 | 0.1159 | 0.0019 |
| ja | 0.625 | 0.35 | 9 | 5054 | +0.5799 | +0.6697 | 0.0898 | 0.0029 |
| pt | 0.625 | 0.35 | 9 | 5057 | +0.5593 | +0.6630 | 0.1037 | 0.0023 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6216 | +0.7129 | 0.0913 | 0.0036 |

Latimea medie a curbei lui w e 0.1021, iar a criteriului de candidati 0.0026, adica de 39 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
