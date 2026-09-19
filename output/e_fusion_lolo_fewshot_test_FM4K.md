# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-22 16:01:08 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag fewshot_test_FM4K --b-dir output/bakeoff_test_FM4K --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_temp.csv`. **Semnalul B de test vine din `output/bakeoff_test_FM4K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_fewshot_test_FM4K.csv`, predictii per instanta in `output/fusion_preds_lolo_fewshot_test_FM4K.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.35 | +0.4564 | +0.5218 | **+0.5650** | [+0.5029, +0.6194] | +0.1086 | [+0.0581, +0.1670] | +0.0432 | [+0.0142, +0.0700] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.30 | +0.6808 | +0.6996 | **+0.7589** | [+0.7252, +0.7902] | +0.0781 | [+0.0411, +0.1170] | +0.0593 | [+0.0422, +0.0760] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8287 | +0.8531 | **+0.8744** | [+0.8496, +0.8951] | +0.0456 | [+0.0254, +0.0688] | +0.0213 | [+0.0111, +0.0324] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.35 | +0.7030 | +0.7531 | **+0.7649** | [+0.7279, +0.7975] | +0.0619 | [+0.0387, +0.0856] | +0.0118 | [-0.0002, +0.0241] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.875 | 0.35 | +0.4171 | +0.5013 | **+0.5067** | [+0.4398, +0.5646] | +0.0896 | [+0.0517, +0.1253] | +0.0054 | [-0.0131, +0.0263] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 1.000 | 0.35 | +0.5421 | +0.6986 | **+0.6801** | [+0.6287, +0.7269] | +0.1380 | [+0.1046, +0.1748] | -0.0185 | [-0.0338, -0.0039] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.35 | +0.6487 | +0.6414 | **+0.6786** | [+0.6330, +0.7220] | +0.0299 | [+0.0019, +0.0581] | +0.0372 | [+0.0209, +0.0540] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.6140 | +0.7909 | **+0.8014** | [+0.7631, +0.8338] | +0.1874 | [+0.1409, +0.2364] | +0.0105 | [-0.0088, +0.0301] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.35 | +0.7863 | +0.8227 | **+0.8401** | [+0.8097, +0.8669] | +0.0538 | [+0.0333, +0.0760] | +0.0174 | [+0.0062, +0.0281] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.3166 | +0.3966 | **+0.4332** | [+0.3722, +0.4916] | +0.1165 | [+0.0681, +0.1687] | +0.0366 | [+0.0063, +0.0658] |
| **medie** | | | | 0.812 | 0.35 | +0.5994 | +0.6679 | **+0.6903** | | +0.0909 | | +0.0224 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_temp.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5566 | **+0.5650** | +0.0084 | [-0.0017, +0.0194] | 94.0% |
| de | +0.7468 | **+0.7589** | +0.0121 | [+0.0019, +0.0225] | 99.4% |
| en | +0.8700 | **+0.8744** | +0.0043 | [-0.0009, +0.0106] | 94.7% |
| es | +0.7641 | **+0.7649** | +0.0008 | [-0.0056, +0.0073] | 60.2% |
| fil | +0.5091 | **+0.5067** | -0.0024 | [-0.0101, +0.0056] | 26.2% |
| fr | +0.6590 | **+0.6801** | +0.0211 | [+0.0116, +0.0311] | 100.0% |
| it | +0.6750 | **+0.6786** | +0.0036 | [-0.0045, +0.0115] | 79.5% |
| ja | +0.7877 | **+0.8014** | +0.0137 | [+0.0062, +0.0214] | 100.0% |
| pt | +0.8450 | **+0.8401** | -0.0049 | [-0.0096, -0.0003] | 1.9% |
| si | +0.4251 | **+0.4332** | +0.0080 | [-0.0055, +0.0219] | 85.9% |
| **medie** | +0.6838 | **+0.6903** | +0.0065 | | 74.2% |

Configuratia noua urca fuziunea pe 8 din 10 limbi. Intervalul pereche exclude zero in sus pe 3. Pe medie, **+0.0065**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6903** | [+0.6756, +0.7043] | |
| fuziune − A | +0.0909 | [+0.0787, +0.1020] | 100.0% |
| fuziune − B | +0.0224 | [+0.0165, +0.0282] | 100.0% |
| configuratia noua − cea de azi | +0.0065 | [+0.0037, +0.0092] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5994 |
| semnalul B singur, `lolo` | 0.6679 |
| fuziunea de azi, A = `p_multi` | 0.6838 |
| **fuziunea cu ansamblul de surse** | **0.6903** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0332**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.35 | 9 | 5179 | +0.6142 | +0.7051 | 0.0909 | 0.0037 |
| de | 0.750 | 0.30 | 9 | 5054 | +0.5926 | +0.6831 | 0.0905 | 0.0020 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5761 | +0.6708 | 0.0947 | 0.0045 |
| es | 0.750 | 0.35 | 9 | 5031 | +0.5901 | +0.6829 | 0.0928 | 0.0040 |
| fil | 0.875 | 0.35 | 9 | 5054 | +0.6185 | +0.7116 | 0.0931 | 0.0033 |
| fr | 1.000 | 0.35 | 9 | 5055 | +0.6003 | +0.6920 | 0.0917 | 0.0043 |
| it | 0.750 | 0.35 | 9 | 5054 | +0.5961 | +0.6925 | 0.0964 | 0.0033 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5966 | +0.6788 | 0.0822 | 0.0028 |
| pt | 0.750 | 0.35 | 9 | 5057 | +0.5809 | +0.6746 | 0.0937 | 0.0041 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6330 | +0.7198 | 0.0868 | 0.0033 |

Latimea medie a curbei lui w e 0.0913, iar a criteriului de candidati 0.0035, adica de 26 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
