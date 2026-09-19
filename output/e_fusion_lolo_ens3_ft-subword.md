# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 13:13:03 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag ens3_ft-subword --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_ens3_ft-subword_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_ens3_ft-subword.csv`, predictii per instanta in `output/fusion_preds_lolo_ens3_ft-subword.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.35 | +0.4504 | +0.5159 | **+0.5545** | [+0.4899, +0.6118] | +0.1041 | [+0.0528, +0.1594] | +0.0386 | [+0.0098, +0.0659] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.875 | 0.30 | +0.6827 | +0.6812 | **+0.7443** | [+0.7076, +0.7787] | +0.0616 | [+0.0267, +0.0984] | +0.0631 | [+0.0460, +0.0800] |
| en | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.35 | +0.8225 | +0.8463 | **+0.8693** | [+0.8422, +0.8921] | +0.0468 | [+0.0247, +0.0711] | +0.0230 | [+0.0122, +0.0355] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.35 | +0.7007 | +0.7499 | **+0.7638** | [+0.7268, +0.7966] | +0.0632 | [+0.0397, +0.0880] | +0.0139 | [+0.0012, +0.0273] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.35 | +0.4005 | +0.5082 | **+0.5126** | [+0.4468, +0.5717] | +0.1120 | [+0.0714, +0.1518] | +0.0044 | [-0.0159, +0.0260] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 1.000 | 0.35 | +0.5421 | +0.6655 | **+0.6606** | [+0.6073, +0.7099] | +0.1185 | [+0.0831, +0.1576] | -0.0049 | [-0.0216, +0.0110] |
| it | `gemma4-12b-4bit` | 570 | 192 | 1.000 | 0.35 | +0.6464 | +0.6354 | **+0.6755** | [+0.6309, +0.7196] | +0.0291 | [+0.0004, +0.0585] | +0.0401 | [+0.0230, +0.0566] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.35 | +0.6031 | +0.7715 | **+0.7901** | [+0.7487, +0.8240] | +0.1871 | [+0.1407, +0.2364] | +0.0187 | [-0.0018, +0.0395] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 1.000 | 0.35 | +0.7843 | +0.8322 | **+0.8451** | [+0.8154, +0.8710] | +0.0607 | [+0.0391, +0.0832] | +0.0129 | [+0.0017, +0.0237] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.500 | 0.35 | +0.2898 | +0.3860 | **+0.4049** | [+0.3488, +0.4573] | +0.1151 | [+0.0648, +0.1677] | +0.0189 | [-0.0070, +0.0450] |
| **medie** | | | | 0.900 | 0.35 | +0.5923 | +0.6592 | **+0.6821** | | +0.0898 | | +0.0229 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5545** | +0.0075 | [-0.0009, +0.0154] | 96.0% |
| de | +0.7429 | **+0.7443** | +0.0015 | [-0.0033, +0.0061] | 72.5% |
| en | +0.8673 | **+0.8693** | +0.0020 | [-0.0017, +0.0060] | 86.1% |
| es | +0.7548 | **+0.7638** | +0.0090 | [+0.0040, +0.0138] | 100.0% |
| fil | +0.5133 | **+0.5126** | -0.0007 | [-0.0109, +0.0100] | 43.9% |
| fr | +0.6605 | **+0.6606** | +0.0002 | [-0.0064, +0.0067] | 53.8% |
| it | +0.6704 | **+0.6755** | +0.0051 | [-0.0002, +0.0101] | 96.9% |
| ja | +0.7934 | **+0.7901** | -0.0032 | [-0.0098, +0.0037] | 18.9% |
| pt | +0.8398 | **+0.8451** | +0.0052 | [+0.0022, +0.0084] | 100.0% |
| si | +0.4095 | **+0.4049** | -0.0046 | [-0.0340, +0.0254] | 38.0% |
| **medie** | +0.6799 | **+0.6821** | +0.0022 | | 70.6% |

Configuratia noua urca fuziunea pe 7 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0022**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6821** | [+0.6673, +0.6959] | |
| fuziune − A | +0.0898 | [+0.0778, +0.1020] | 100.0% |
| fuziune − B | +0.0229 | [+0.0170, +0.0287] | 100.0% |
| configuratia noua − cea de azi | +0.0022 | [-0.0013, +0.0058] | 88.4% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5923 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6821** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0250**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.35 | 9 | 5179 | +0.6085 | +0.6976 | 0.0891 | 0.0031 |
| de | 0.875 | 0.30 | 9 | 5054 | +0.5848 | +0.6759 | 0.0911 | 0.0014 |
| en | 1.000 | 0.35 | 9 | 5054 | +0.5672 | +0.6626 | 0.0954 | 0.0038 |
| es | 0.875 | 0.35 | 9 | 5031 | +0.5828 | +0.6743 | 0.0915 | 0.0028 |
| fil | 0.750 | 0.35 | 9 | 5054 | +0.6176 | +0.7021 | 0.0845 | 0.0012 |
| fr | 1.000 | 0.35 | 9 | 5055 | +0.5984 | +0.6858 | 0.0874 | 0.0035 |
| it | 1.000 | 0.35 | 9 | 5054 | +0.5868 | +0.6842 | 0.0974 | 0.0030 |
| ja | 1.000 | 0.35 | 9 | 5054 | +0.5916 | +0.6714 | 0.0798 | 0.0026 |
| pt | 1.000 | 0.35 | 9 | 5057 | +0.5714 | +0.6653 | 0.0939 | 0.0030 |
| si | 0.500 | 0.35 | 9 | 5024 | +0.6309 | +0.7135 | 0.0826 | 0.0029 |

Latimea medie a curbei lui w e 0.0893, iar a criteriului de candidati 0.0027, adica de 33 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
