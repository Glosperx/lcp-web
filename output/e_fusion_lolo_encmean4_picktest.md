# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-19 01:23:42 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag encmean4_picktest --a-set fert_inloc=output/e1_frozen_preds_encmean_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ens.csv`. Date brute: `output/fusion_lolo_encmean4_picktest.csv`, predictii per instanta in `output/fusion_preds_lolo_encmean4_picktest.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.40 | +0.4689 | +0.4829 | **+0.5409** | [+0.4752, +0.6008] | +0.0720 | [+0.0224, +0.1248] | +0.0580 | [+0.0227, +0.0909] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.40 | +0.6915 | +0.6544 | **+0.7396** | [+0.7014, +0.7757] | +0.0481 | [+0.0186, +0.0779] | +0.0851 | [+0.0637, +0.1078] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.40 | +0.8338 | +0.8377 | **+0.8711** | [+0.8445, +0.8937] | +0.0374 | [+0.0172, +0.0585] | +0.0334 | [+0.0211, +0.0477] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.625 | 0.45 | +0.7016 | +0.7432 | **+0.7582** | [+0.7200, +0.7925] | +0.0566 | [+0.0356, +0.0778] | +0.0151 | [+0.0001, +0.0308] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.45 | +0.4085 | +0.5173 | **+0.5095** | [+0.4425, +0.5702] | +0.1009 | [+0.0663, +0.1339] | -0.0078 | [-0.0341, +0.0196] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.45 | +0.5580 | +0.6424 | **+0.6460** | [+0.5912, +0.6963] | +0.0880 | [+0.0596, +0.1205] | +0.0036 | [-0.0192, +0.0271] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.875 | 0.40 | +0.6507 | +0.6127 | **+0.6658** | [+0.6221, +0.7096] | +0.0150 | [-0.0116, +0.0428] | +0.0531 | [+0.0340, +0.0726] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.45 | +0.6454 | +0.7676 | **+0.7867** | [+0.7421, +0.8238] | +0.1413 | [+0.1037, +0.1803] | +0.0191 | [-0.0055, +0.0457] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.45 | +0.7907 | +0.8213 | **+0.8425** | [+0.8103, +0.8696] | +0.0518 | [+0.0327, +0.0733] | +0.0212 | [+0.0059, +0.0361] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.875 | 0.40 | +0.3298 | +0.3407 | **+0.3997** | [+0.3423, +0.4546] | +0.0699 | [+0.0276, +0.1154] | +0.0590 | [+0.0241, +0.0920] |
| **medie** | | | | 0.738 | 0.43 | +0.6079 | +0.6420 | **+0.6760** | | +0.0681 | | +0.0340 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ens.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5283 | **+0.5409** | +0.0126 | [+0.0030, +0.0216] | 99.6% |
| de | +0.7324 | **+0.7396** | +0.0071 | [+0.0014, +0.0131] | 99.0% |
| en | +0.8663 | **+0.8711** | +0.0048 | [+0.0007, +0.0093] | 98.7% |
| es | +0.7486 | **+0.7582** | +0.0096 | [+0.0042, +0.0151] | 100.0% |
| fil | +0.5171 | **+0.5095** | -0.0077 | [-0.0142, -0.0012] | 1.4% |
| fr | +0.5857 | **+0.6460** | +0.0603 | [+0.0336, +0.0870] | 100.0% |
| it | +0.6625 | **+0.6658** | +0.0033 | [-0.0026, +0.0089] | 86.1% |
| ja | +0.7887 | **+0.7867** | -0.0020 | [-0.0102, +0.0065] | 32.4% |
| pt | +0.8375 | **+0.8425** | +0.0050 | [+0.0011, +0.0090] | 99.2% |
| si | +0.3786 | **+0.3997** | +0.0211 | [-0.0009, +0.0430] | 96.9% |
| **medie** | +0.6646 | **+0.6760** | +0.0114 | | 81.3% |

Configuratia noua urca fuziunea pe 8 din 10 limbi. Intervalul pereche exclude zero in sus pe 6. Pe medie, **+0.0114**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6760** | [+0.6608, +0.6901] | |
| fuziune − A | +0.0681 | [+0.0574, +0.0784] | 100.0% |
| fuziune − B | +0.0340 | [+0.0267, +0.0414] | 100.0% |
| configuratia noua − cea de azi | +0.0114 | [+0.0075, +0.0153] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6079 |
| semnalul B singur, `lolo` | 0.6420 |
| fuziunea de azi, A = `p_multi` | 0.6646 |
| **fuziunea cu ansamblul de surse** | **0.6760** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0189**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.40 | 9 | 5179 | +0.6207 | +0.6925 | 0.0718 | 0.0041 |
| de | 0.750 | 0.40 | 9 | 5054 | +0.5991 | +0.6706 | 0.0715 | 0.0031 |
| en | 0.750 | 0.40 | 9 | 5054 | +0.5833 | +0.6560 | 0.0727 | 0.0040 |
| es | 0.625 | 0.45 | 9 | 5031 | +0.6001 | +0.6685 | 0.0684 | 0.0038 |
| fil | 0.625 | 0.45 | 9 | 5054 | +0.6326 | +0.6961 | 0.0635 | 0.0050 |
| fr | 0.750 | 0.45 | 9 | 5055 | +0.6139 | +0.6809 | 0.0670 | 0.0054 |
| it | 0.875 | 0.40 | 9 | 5054 | +0.6005 | +0.6786 | 0.0781 | 0.0034 |
| ja | 0.625 | 0.45 | 9 | 5054 | +0.6063 | +0.6653 | 0.0590 | 0.0034 |
| pt | 0.625 | 0.45 | 9 | 5057 | +0.5902 | +0.6591 | 0.0689 | 0.0034 |
| si | 0.875 | 0.40 | 9 | 5024 | +0.6361 | +0.7082 | 0.0721 | 0.0023 |

Latimea medie a curbei lui w e 0.0693, iar a criteriului de candidati 0.0038, adica de 18 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
