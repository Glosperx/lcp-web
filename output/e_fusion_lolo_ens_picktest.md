# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-18 15:55:53 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag ens_picktest --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ens.csv`. Date brute: `output/fusion_lolo_ens_picktest.csv`, predictii per instanta in `output/fusion_preds_lolo_ens_picktest.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.35 | +0.4175 | +0.4829 | **+0.5249** | [+0.4571, +0.5848] | +0.1074 | [+0.0493, +0.1675] | +0.0420 | [+0.0098, +0.0736] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.35 | +0.6666 | +0.6544 | **+0.7311** | [+0.6924, +0.7689] | +0.0644 | [+0.0301, +0.1018] | +0.0766 | [+0.0569, +0.0970] |
| en | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.35 | +0.8059 | +0.8377 | **+0.8629** | [+0.8343, +0.8874] | +0.0570 | [+0.0341, +0.0830] | +0.0252 | [+0.0140, +0.0378] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.40 | +0.6617 | +0.7432 | **+0.7492** | [+0.7107, +0.7847] | +0.0875 | [+0.0615, +0.1143] | +0.0060 | [-0.0084, +0.0211] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.750 | 0.40 | +0.4174 | +0.5190 | **+0.5197** | [+0.4556, +0.5825] | +0.1023 | [+0.0642, +0.1396] | +0.0008 | [-0.0219, +0.0246] |
| fr | `gemma4-12b-4bit` | 566 | 191 | 0.875 | 0.40 | +0.5370 | +0.6457 | **+0.6465** | [+0.5922, +0.6962] | +0.1094 | [+0.0761, +0.1459] | +0.0007 | [-0.0196, +0.0216] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.750 | 0.35 | +0.6311 | +0.6106 | **+0.6581** | [+0.6128, +0.7031] | +0.0270 | [-0.0040, +0.0576] | +0.0475 | [+0.0307, +0.0645] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.40 | +0.6205 | +0.7676 | **+0.7898** | [+0.7470, +0.8272] | +0.1694 | [+0.1280, +0.2144] | +0.0222 | [-0.0015, +0.0454] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.750 | 0.35 | +0.7802 | +0.8222 | **+0.8409** | [+0.8076, +0.8680] | +0.0606 | [+0.0382, +0.0827] | +0.0187 | [+0.0073, +0.0307] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.2693 | +0.3407 | **+0.3729** | [+0.3220, +0.4246] | +0.1036 | [+0.0559, +0.1513] | +0.0322 | [+0.0055, +0.0576] |
| **medie** | | | | 0.800 | 0.37 | +0.5807 | +0.6424 | **+0.6696** | | +0.0889 | | +0.0272 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ens.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5288 | **+0.5249** | -0.0039 | [-0.0092, +0.0014] | 7.6% |
| de | +0.7311 | **+0.7311** | +0.0000 | [-0.0000, +0.0000] | 10.4% |
| en | +0.8657 | **+0.8629** | -0.0028 | [-0.0049, -0.0009] | 0.1% |
| es | +0.7484 | **+0.7492** | +0.0008 | [-0.0001, +0.0018] | 95.5% |
| fil | +0.5197 | **+0.5197** | +0.0000 | [-0.0000, +0.0000] | 11.5% |
| fr | +0.5883 | **+0.6465** | +0.0582 | [+0.0305, +0.0869] | 100.0% |
| it | +0.6616 | **+0.6581** | -0.0035 | [-0.0061, -0.0011] | 0.3% |
| ja | +0.7887 | **+0.7898** | +0.0011 | [-0.0028, +0.0051] | 70.5% |
| pt | +0.8403 | **+0.8409** | +0.0005 | [-0.0011, +0.0022] | 73.0% |
| si | +0.3729 | **+0.3729** | +0.0000 | [-0.0000, +0.0000] | 15.3% |
| **medie** | +0.6646 | **+0.6696** | +0.0050 | | 38.4% |

Configuratia noua urca fuziunea pe 4 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **+0.0050**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6696** | [+0.6547, +0.6838] | |
| fuziune − A | +0.0889 | [+0.0768, +0.1009] | 100.0% |
| fuziune − B | +0.0272 | [+0.0204, +0.0340] | 100.0% |
| configuratia noua − cea de azi | +0.0050 | [+0.0021, +0.0081] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5807 |
| semnalul B singur, `lolo` | 0.6424 |
| fuziunea de azi, A = `p_multi` | 0.6646 |
| **fuziunea cu ansamblul de surse** | **0.6696** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0125**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.35 | 9 | 5161 | +0.5931 | +0.6877 | 0.0946 | 0.0070 |
| de | 0.750 | 0.35 | 9 | 5036 | +0.5739 | +0.6650 | 0.0911 | 0.0054 |
| en | 1.000 | 0.35 | 9 | 5036 | +0.5500 | +0.6502 | 0.1002 | 0.0070 |
| es | 0.750 | 0.40 | 9 | 5013 | +0.5744 | +0.6629 | 0.0885 | 0.0054 |
| fil | 0.750 | 0.40 | 9 | 5038 | +0.6016 | +0.6884 | 0.0868 | 0.0052 |
| fr | 0.875 | 0.40 | 9 | 5040 | +0.5847 | +0.6743 | 0.0896 | 0.0058 |
| it | 0.750 | 0.35 | 9 | 5044 | +0.5778 | +0.6731 | 0.0953 | 0.0064 |
| ja | 0.750 | 0.40 | 9 | 5036 | +0.5790 | +0.6584 | 0.0794 | 0.0045 |
| pt | 0.750 | 0.35 | 9 | 5044 | +0.5612 | +0.6528 | 0.0916 | 0.0045 |
| si | 0.625 | 0.35 | 9 | 5006 | +0.6202 | +0.7045 | 0.0843 | 0.0023 |

Latimea medie a curbei lui w e 0.0901, iar a criteriului de candidati 0.0054, adica de 17 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

## Scara configuratiilor

Toate pe aceleasi randuri de test, cu acelasi brat B si acelasi protocol. Se schimba numai din ce e facut semnalul A si ce se alege leave-one-language-out.

| configuratie | limbi | set de trasaturi | w_src mediu | r mediu | fata de 0.6571 |
|---|---|---|---|---|---|
| fuziunea de azi, A = `p_multi` | 10 | `baza` | 0.000 | **0.6568** | -0.0003 |
| doar ansamblul de surse, set `baza` | 10 | `baza` | 0.900 | **0.6636** | +0.0065 |
| doar `fert_inloc`, fara ansamblu | 10 | `fert_inloc` | 0.000 | **0.6591** | +0.0020 |
| **ansamblu plus `fert_inloc`** | 10 | `fert_inloc` | 0.775 | **0.6646** | +0.0075 |
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
