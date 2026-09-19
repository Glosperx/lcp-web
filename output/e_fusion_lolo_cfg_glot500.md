# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 13:00:50 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_glot500 --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_glot500_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_glot500.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_glot500.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.30 | +0.4254 | +0.5159 | **+0.5446** | [+0.4804, +0.6027] | +0.1193 | [+0.0700, +0.1685] | +0.0287 | [+0.0071, +0.0502] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.30 | +0.6438 | +0.6812 | **+0.7353** | [+0.6973, +0.7696] | +0.0916 | [+0.0544, +0.1332] | +0.0541 | [+0.0365, +0.0721] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.30 | +0.8188 | +0.8463 | **+0.8698** | [+0.8422, +0.8937] | +0.0510 | [+0.0284, +0.0759] | +0.0235 | [+0.0136, +0.0353] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.30 | +0.6606 | +0.7499 | **+0.7574** | [+0.7192, +0.7923] | +0.0968 | [+0.0661, +0.1272] | +0.0075 | [-0.0041, +0.0199] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 1.000 | 0.30 | +0.4153 | +0.5082 | **+0.5151** | [+0.4507, +0.5725] | +0.0998 | [+0.0588, +0.1415] | +0.0069 | [-0.0101, +0.0240] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 1.000 | 0.30 | +0.5613 | +0.6655 | **+0.6728** | [+0.6202, +0.7202] | +0.1115 | [+0.0767, +0.1489] | +0.0073 | [-0.0063, +0.0215] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.30 | +0.6265 | +0.6354 | **+0.6685** | [+0.6227, +0.7144] | +0.0420 | [+0.0100, +0.0736] | +0.0331 | [+0.0182, +0.0480] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.5872 | +0.7715 | **+0.7824** | [+0.7399, +0.8169] | +0.1952 | [+0.1515, +0.2420] | +0.0110 | [-0.0092, +0.0308] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 1.000 | 0.30 | +0.7537 | +0.8322 | **+0.8384** | [+0.8092, +0.8643] | +0.0847 | [+0.0603, +0.1099] | +0.0062 | [-0.0030, +0.0149] |
| si | `gemma4-12b-4bit` | 600 | 578 | 1.000 | 0.30 | +0.2365 | +0.3860 | **+0.3994** | [+0.3408, +0.4524] | +0.1629 | [+0.1129, +0.2147] | +0.0134 | [-0.0098, +0.0353] |
| **medie** | | | | 0.912 | 0.30 | +0.5729 | +0.6592 | **+0.6784** | | +0.1055 | | +0.0192 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 4 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5446** | -0.0023 | [-0.0149, +0.0103] | 36.5% |
| de | +0.7429 | **+0.7353** | -0.0075 | [-0.0139, -0.0012] | 0.9% |
| en | +0.8673 | **+0.8698** | +0.0025 | [-0.0018, +0.0070] | 87.5% |
| es | +0.7548 | **+0.7574** | +0.0026 | [-0.0037, +0.0092] | 80.5% |
| fil | +0.5133 | **+0.5151** | +0.0018 | [-0.0054, +0.0094] | 68.2% |
| fr | +0.6605 | **+0.6728** | +0.0124 | [+0.0040, +0.0214] | 99.7% |
| it | +0.6704 | **+0.6685** | -0.0019 | [-0.0081, +0.0044] | 27.4% |
| ja | +0.7934 | **+0.7824** | -0.0109 | [-0.0192, -0.0033] | 0.2% |
| pt | +0.8398 | **+0.8384** | -0.0014 | [-0.0061, +0.0032] | 24.4% |
| si | +0.4095 | **+0.3994** | -0.0101 | [-0.0311, +0.0112] | 17.3% |
| **medie** | +0.6799 | **+0.6784** | -0.0015 | | 44.3% |

Configuratia noua urca fuziunea pe 4 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **-0.0015**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6784** | [+0.6643, +0.6920] | |
| fuziune − A | +0.1055 | [+0.0930, +0.1173] | 100.0% |
| fuziune − B | +0.0192 | [+0.0140, +0.0243] | 100.0% |
| configuratia noua − cea de azi | -0.0015 | [-0.0046, +0.0017] | 17.4% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5729 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6784** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0213**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.30 | 9 | 5179 | +0.5908 | +0.6940 | 0.1032 | 0.0047 |
| de | 0.750 | 0.30 | 9 | 5054 | +0.5684 | +0.6727 | 0.1043 | 0.0026 |
| en | 0.875 | 0.30 | 9 | 5054 | +0.5471 | +0.6578 | 0.1107 | 0.0051 |
| es | 1.000 | 0.30 | 9 | 5031 | +0.5616 | +0.6702 | 0.1086 | 0.0033 |
| fil | 1.000 | 0.30 | 9 | 5054 | +0.5888 | +0.6971 | 0.1083 | 0.0023 |
| fr | 1.000 | 0.30 | 9 | 5055 | +0.5726 | +0.6796 | 0.1070 | 0.0043 |
| it | 0.750 | 0.30 | 9 | 5054 | +0.5704 | +0.6801 | 0.1097 | 0.0034 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5728 | +0.6672 | 0.0944 | 0.0019 |
| pt | 1.000 | 0.30 | 9 | 5057 | +0.5512 | +0.6612 | 0.1100 | 0.0038 |
| si | 1.000 | 0.30 | 9 | 5024 | +0.6087 | +0.7100 | 0.1013 | 0.0036 |

Latimea medie a curbei lui w e 0.1058, iar a criteriului de candidati 0.0035, adica de 30 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
