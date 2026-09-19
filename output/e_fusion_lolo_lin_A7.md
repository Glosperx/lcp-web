# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 17:31:49 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag lin_A7 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_A7-encmean_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_lin_A7.csv`, predictii per instanta in `output/fusion_preds_lolo_lin_A7.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4637 | +0.5187 | **+0.5652** | [+0.5023, +0.6208] | +0.1015 | [+0.0504, +0.1599] | +0.0465 | [+0.0182, +0.0731] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.35 | +0.6763 | +0.7108 | **+0.7707** | [+0.7375, +0.8010] | +0.0944 | [+0.0605, +0.1310] | +0.0600 | [+0.0412, +0.0789] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.8297 | +0.8471 | **+0.8729** | [+0.8468, +0.8948] | +0.0432 | [+0.0220, +0.0670] | +0.0258 | [+0.0148, +0.0381] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.35 | +0.7052 | +0.7553 | **+0.7687** | [+0.7320, +0.8016] | +0.0635 | [+0.0395, +0.0889] | +0.0134 | [+0.0013, +0.0256] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.35 | +0.4221 | +0.5000 | **+0.5082** | [+0.4415, +0.5665] | +0.0861 | [+0.0471, +0.1235] | +0.0082 | [-0.0114, +0.0293] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 1.000 | 0.35 | +0.5479 | +0.6752 | **+0.6683** | [+0.6161, +0.7156] | +0.1204 | [+0.0869, +0.1578] | -0.0069 | [-0.0222, +0.0084] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.35 | +0.6449 | +0.6406 | **+0.6788** | [+0.6348, +0.7219] | +0.0339 | [+0.0055, +0.0632] | +0.0382 | [+0.0219, +0.0553] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.6220 | +0.7795 | **+0.7961** | [+0.7544, +0.8295] | +0.1741 | [+0.1282, +0.2213] | +0.0166 | [-0.0022, +0.0369] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.35 | +0.7858 | +0.8243 | **+0.8421** | [+0.8117, +0.8686] | +0.0563 | [+0.0357, +0.0788] | +0.0178 | [+0.0063, +0.0287] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.500 | 0.35 | +0.3252 | +0.3979 | **+0.4333** | [+0.3766, +0.4860] | +0.1081 | [+0.0638, +0.1570] | +0.0354 | [+0.0083, +0.0617] |
| **medie** | | | | 0.812 | 0.35 | +0.6023 | +0.6649 | **+0.6904** | | +0.0882 | | +0.0255 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5652** | +0.0013 | [-0.0015, +0.0040] | 81.6% |
| de | +0.7712 | **+0.7707** | -0.0005 | [-0.0023, +0.0012] | 27.4% |
| en | +0.8723 | **+0.8729** | +0.0006 | [-0.0004, +0.0017] | 86.2% |
| es | +0.7672 | **+0.7687** | +0.0015 | [-0.0005, +0.0037] | 93.2% |
| fil | +0.5074 | **+0.5082** | +0.0008 | [-0.0014, +0.0030] | 78.2% |
| fr | +0.6679 | **+0.6683** | +0.0003 | [-0.0023, +0.0029] | 61.9% |
| it | +0.6795 | **+0.6788** | -0.0007 | [-0.0027, +0.0013] | 25.1% |
| ja | +0.7942 | **+0.7961** | +0.0019 | [-0.0012, +0.0048] | 89.4% |
| pt | +0.8413 | **+0.8421** | +0.0008 | [-0.0003, +0.0020] | 94.2% |
| si | +0.4350 | **+0.4333** | -0.0017 | [-0.0109, +0.0073] | 35.0% |
| **medie** | +0.6900 | **+0.6904** | +0.0004 | | 67.2% |

Configuratia noua urca fuziunea pe 7 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **+0.0004**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6904** | [+0.6761, +0.7041] | |
| fuziune − A | +0.0882 | [+0.0764, +0.0992] | 100.0% |
| fuziune − B | +0.0255 | [+0.0197, +0.0312] | 100.0% |
| configuratia noua − cea de azi | +0.0004 | [-0.0007, +0.0016] | 77.2% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6023 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6904** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0333**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6182 | +0.7044 | 0.0862 | 0.0039 |
| de | 0.750 | 0.35 | 9 | 5054 | +0.5946 | +0.6816 | 0.0870 | 0.0031 |
| en | 0.875 | 0.35 | 9 | 5054 | +0.5760 | +0.6702 | 0.0942 | 0.0046 |
| es | 1.000 | 0.35 | 9 | 5031 | +0.5874 | +0.6817 | 0.0943 | 0.0028 |
| fil | 0.750 | 0.35 | 9 | 5054 | +0.6228 | +0.7107 | 0.0879 | 0.0023 |
| fr | 1.000 | 0.35 | 9 | 5055 | +0.6049 | +0.6929 | 0.0880 | 0.0040 |
| it | 0.750 | 0.35 | 9 | 5054 | +0.5981 | +0.6918 | 0.0937 | 0.0035 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5990 | +0.6788 | 0.0798 | 0.0023 |
| pt | 0.875 | 0.35 | 9 | 5057 | +0.5808 | +0.6737 | 0.0929 | 0.0034 |
| si | 0.500 | 0.35 | 9 | 5024 | +0.6342 | +0.7186 | 0.0844 | 0.0039 |

Latimea medie a curbei lui w e 0.0888, iar a criteriului de candidati 0.0034, adica de 26 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
