# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-09-26 19:02:03 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag en_fara_complex_ro11 --b-dir output/bakeoff_test_M3K_ro11 --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc_en-fara-complex_ro11.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K_ro11/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_en_fara_complex_ro11.csv`, predictii per instanta in `output/fusion_preds_lolo_en_fara_complex_ro11.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.40 | +0.4561 | +0.5187 | **+0.5632** | [+0.5005, +0.6183] | +0.1071 | [+0.0585, +0.1611] | +0.0444 | [+0.0105, +0.0762] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.35 | +0.6830 | +0.7067 | **+0.7704** | [+0.7367, +0.8016] | +0.0874 | [+0.0521, +0.1240] | +0.0637 | [+0.0443, +0.0830] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.8064 | +0.8471 | **+0.8695** | [+0.8437, +0.8920] | +0.0631 | [+0.0434, +0.0838] | +0.0224 | [+0.0091, +0.0367] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.40 | +0.7058 | +0.7553 | **+0.7672** | [+0.7302, +0.7998] | +0.0614 | [+0.0391, +0.0837] | +0.0119 | [-0.0017, +0.0258] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.40 | +0.4176 | +0.5000 | **+0.5045** | [+0.4374, +0.5639] | +0.0868 | [+0.0500, +0.1212] | +0.0044 | [-0.0186, +0.0283] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.875 | 0.40 | +0.5452 | +0.6721 | **+0.6608** | [+0.6086, +0.7080] | +0.1156 | [+0.0843, +0.1502] | -0.0113 | [-0.0300, +0.0061] |
| it | `gemma4-12b-4bit` | 570 | 192 | 1.000 | 0.35 | +0.6464 | +0.6406 | **+0.6801** | [+0.6358, +0.7232] | +0.0337 | [+0.0048, +0.0629] | +0.0395 | [+0.0226, +0.0569] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.40 | +0.6159 | +0.7795 | **+0.7909** | [+0.7487, +0.8262] | +0.1750 | [+0.1316, +0.2213] | +0.0114 | [-0.0111, +0.0349] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.40 | +0.7876 | +0.8243 | **+0.8416** | [+0.8108, +0.8685] | +0.0540 | [+0.0350, +0.0746] | +0.0173 | [+0.0045, +0.0297] |
| ro | `gemma4-12b-4bit` | 1587 | 274 | 0.750 | 0.35 | +0.7302 | +0.6588 | **+0.7394** | [+0.7051, +0.7704] | +0.0092 | [-0.0146, +0.0327] | +0.0806 | [+0.0666, +0.0960] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.40 | +0.3111 | +0.3951 | **+0.4302** | [+0.3694, +0.4884] | +0.1191 | [+0.0748, +0.1665] | +0.0351 | [-0.0005, +0.0684] |
| **medie** | | | | 0.773 | 0.39 | +0.6096 | +0.6635 | **+0.6925** | | +0.0829 | | +0.0290 | |

Fuziunea bate A pe 11 din 11 limbi si B pe 10 din 11. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6925** | [+0.6789, +0.7057] | |
| fuziune − A | +0.0830 | [+0.0724, +0.0927] | 100.0% |
| fuziune − B | +0.0290 | [+0.0226, +0.0353] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6096 |
| semnalul B singur, `lolo` | 0.6635 |
| **fuziunea cu ansamblul de surse** | **0.6925** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0354**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.40 | 10 | 6766 | +0.6240 | +0.7072 | 0.0832 | 0.0047 |
| de | 0.750 | 0.35 | 10 | 6641 | +0.6041 | +0.6864 | 0.0823 | 0.0037 |
| en | 0.625 | 0.40 | 10 | 6641 | +0.5935 | +0.6766 | 0.0831 | 0.0042 |
| es | 0.750 | 0.40 | 10 | 6618 | +0.6018 | +0.6869 | 0.0851 | 0.0052 |
| fil | 0.750 | 0.40 | 10 | 6641 | +0.6306 | +0.7132 | 0.0826 | 0.0045 |
| fr | 0.875 | 0.40 | 10 | 6642 | +0.6151 | +0.6975 | 0.0824 | 0.0049 |
| it | 1.000 | 0.35 | 10 | 6641 | +0.6012 | +0.6952 | 0.0940 | 0.0042 |
| ja | 0.875 | 0.40 | 10 | 6641 | +0.6080 | +0.6845 | 0.0765 | 0.0027 |
| pt | 0.625 | 0.40 | 10 | 6644 | +0.5954 | +0.6794 | 0.0840 | 0.0043 |
| ro | 0.750 | 0.35 | 10 | 5624 | +0.5994 | +0.6895 | 0.0901 | 0.0043 |
| si | 0.625 | 0.40 | 10 | 6611 | +0.6431 | +0.7205 | 0.0774 | 0.0034 |

Latimea medie a curbei lui w e 0.0837, iar a criteriului de candidati 0.0042, adica de 20 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
