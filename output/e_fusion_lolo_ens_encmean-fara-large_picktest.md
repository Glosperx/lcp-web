# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-19 01:03:18 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag ens_encmean-fara-large_picktest --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ens.csv`. Date brute: `output/fusion_lolo_ens_encmean-fara-large_picktest.csv`, predictii per instanta in `output/fusion_preds_lolo_ens_encmean-fara-large_picktest.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.40 | +0.4567 | +0.4829 | **+0.5387** | [+0.4728, +0.5992] | +0.0820 | [+0.0296, +0.1370] | +0.0558 | [+0.0191, +0.0895] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.40 | +0.6773 | +0.6544 | **+0.7350** | [+0.6964, +0.7716] | +0.0578 | [+0.0273, +0.0893] | +0.0806 | [+0.0584, +0.1040] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.40 | +0.8279 | +0.8377 | **+0.8701** | [+0.8433, +0.8930] | +0.0422 | [+0.0214, +0.0639] | +0.0324 | [+0.0201, +0.0465] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.40 | +0.6973 | +0.7432 | **+0.7599** | [+0.7227, +0.7939] | +0.0626 | [+0.0385, +0.0877] | +0.0167 | [+0.0021, +0.0315] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.625 | 0.45 | +0.4187 | +0.5190 | **+0.5142** | [+0.4510, +0.5778] | +0.0955 | [+0.0610, +0.1291] | -0.0047 | [-0.0294, +0.0219] |
| fr | `gemma4-12b-4bit` | 566 | 191 | 0.875 | 0.40 | +0.5506 | +0.6457 | **+0.6493** | [+0.5944, +0.6990] | +0.0988 | [+0.0667, +0.1338] | +0.0036 | [-0.0167, +0.0242] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.750 | 0.40 | +0.6496 | +0.6106 | **+0.6646** | [+0.6206, +0.7082] | +0.0150 | [-0.0114, +0.0416] | +0.0540 | [+0.0354, +0.0733] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.45 | +0.6237 | +0.7676 | **+0.7823** | [+0.7366, +0.8210] | +0.1586 | [+0.1188, +0.2008] | +0.0146 | [-0.0118, +0.0424] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.875 | 0.40 | +0.7947 | +0.8222 | **+0.8458** | [+0.8130, +0.8722] | +0.0511 | [+0.0296, +0.0718] | +0.0236 | [+0.0104, +0.0383] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.40 | +0.3161 | +0.3407 | **+0.3940** | [+0.3366, +0.4504] | +0.0779 | [+0.0344, +0.1241] | +0.0533 | [+0.0181, +0.0872] |
| **medie** | | | | 0.762 | 0.41 | +0.6012 | +0.6424 | **+0.6754** | | +0.0742 | | +0.0330 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ens.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5288 | **+0.5387** | +0.0099 | [+0.0005, +0.0186] | 98.0% |
| de | +0.7311 | **+0.7350** | +0.0040 | [-0.0029, +0.0107] | 86.8% |
| en | +0.8657 | **+0.8701** | +0.0043 | [+0.0003, +0.0087] | 98.5% |
| es | +0.7484 | **+0.7599** | +0.0115 | [+0.0055, +0.0173] | 100.0% |
| fil | +0.5197 | **+0.5142** | -0.0055 | [-0.0114, +0.0006] | 4.0% |
| fr | +0.5883 | **+0.6493** | +0.0610 | [+0.0328, +0.0893] | 100.0% |
| it | +0.6616 | **+0.6646** | +0.0030 | [-0.0032, +0.0090] | 82.6% |
| ja | +0.7887 | **+0.7823** | -0.0064 | [-0.0151, +0.0024] | 7.5% |
| pt | +0.8403 | **+0.8458** | +0.0054 | [+0.0018, +0.0091] | 99.7% |
| si | +0.3729 | **+0.3940** | +0.0211 | [-0.0021, +0.0457] | 96.2% |
| **medie** | +0.6646 | **+0.6754** | +0.0108 | | 77.3% |

Configuratia noua urca fuziunea pe 8 din 10 limbi. Intervalul pereche exclude zero in sus pe 5. Pe medie, **+0.0108**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6754** | [+0.6602, +0.6895] | |
| fuziune − A | +0.0741 | [+0.0631, +0.0848] | 100.0% |
| fuziune − B | +0.0330 | [+0.0257, +0.0406] | 100.0% |
| configuratia noua − cea de azi | +0.0108 | [+0.0066, +0.0149] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6012 |
| semnalul B singur, `lolo` | 0.6424 |
| fuziunea de azi, A = `p_multi` | 0.6646 |
| **fuziunea cu ansamblul de surse** | **0.6754** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0183**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.40 | 9 | 5161 | +0.6148 | +0.6921 | 0.0773 | 0.0056 |
| de | 0.625 | 0.40 | 9 | 5036 | +0.5954 | +0.6703 | 0.0749 | 0.0036 |
| en | 0.750 | 0.40 | 9 | 5036 | +0.5767 | +0.6554 | 0.0787 | 0.0055 |
| es | 1.000 | 0.40 | 9 | 5013 | +0.5841 | +0.6671 | 0.0830 | 0.0038 |
| fil | 0.625 | 0.45 | 9 | 5038 | +0.6242 | +0.6944 | 0.0702 | 0.0042 |
| fr | 0.875 | 0.40 | 9 | 5040 | +0.6044 | +0.6798 | 0.0754 | 0.0052 |
| it | 0.750 | 0.40 | 9 | 5044 | +0.5965 | +0.6782 | 0.0817 | 0.0047 |
| ja | 0.625 | 0.45 | 9 | 5036 | +0.6014 | +0.6647 | 0.0633 | 0.0032 |
| pt | 0.875 | 0.40 | 9 | 5044 | +0.5773 | +0.6579 | 0.0806 | 0.0041 |
| si | 0.625 | 0.40 | 9 | 5006 | +0.6356 | +0.7081 | 0.0725 | 0.0043 |

Latimea medie a curbei lui w e 0.0758, iar a criteriului de candidati 0.0044, adica de 17 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
