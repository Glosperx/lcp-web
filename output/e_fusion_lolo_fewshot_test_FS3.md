# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-21 21:14:37 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag fewshot_test_FS3 --b-dir output/bakeoff_test_FS3 --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_temp.csv`. **Semnalul B de test vine din `output/bakeoff_test_FS3/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_fewshot_test_FS3.csv`, predictii per instanta in `output/fusion_preds_lolo_fewshot_test_FS3.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.35 | +0.4564 | +0.5207 | **+0.5601** | [+0.4956, +0.6166] | +0.1037 | [+0.0537, +0.1595] | +0.0395 | [+0.0119, +0.0651] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.30 | +0.6808 | +0.6714 | **+0.7358** | [+0.6983, +0.7702] | +0.0550 | [+0.0197, +0.0916] | +0.0644 | [+0.0477, +0.0814] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.8259 | +0.8527 | **+0.8722** | [+0.8475, +0.8928] | +0.0463 | [+0.0258, +0.0695] | +0.0195 | [+0.0099, +0.0305] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.35 | +0.7014 | +0.7520 | **+0.7645** | [+0.7279, +0.7970] | +0.0631 | [+0.0398, +0.0876] | +0.0125 | [+0.0002, +0.0252] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.35 | +0.4166 | +0.5109 | **+0.5123** | [+0.4481, +0.5703] | +0.0957 | [+0.0589, +0.1321] | +0.0014 | [-0.0172, +0.0206] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.875 | 0.35 | +0.5460 | +0.6954 | **+0.6796** | [+0.6265, +0.7273] | +0.1337 | [+0.1003, +0.1713] | -0.0158 | [-0.0313, -0.0012] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.35 | +0.6489 | +0.6372 | **+0.6740** | [+0.6295, +0.7173] | +0.0251 | [-0.0033, +0.0533] | +0.0367 | [+0.0207, +0.0525] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.6140 | +0.7929 | **+0.8037** | [+0.7661, +0.8350] | +0.1897 | [+0.1438, +0.2383] | +0.0108 | [-0.0080, +0.0297] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.35 | +0.7856 | +0.8299 | **+0.8444** | [+0.8146, +0.8707] | +0.0588 | [+0.0377, +0.0807] | +0.0145 | [+0.0036, +0.0249] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.3242 | +0.3814 | **+0.4207** | [+0.3625, +0.4779] | +0.0965 | [+0.0508, +0.1459] | +0.0393 | [+0.0108, +0.0674] |
| **medie** | | | | 0.800 | 0.35 | +0.6000 | +0.6644 | **+0.6867** | | +0.0868 | | +0.0223 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 8 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_temp.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5566 | **+0.5601** | +0.0036 | [-0.0032, +0.0104] | 84.4% |
| de | +0.7468 | **+0.7358** | -0.0110 | [-0.0174, -0.0044] | 0.1% |
| en | +0.8700 | **+0.8722** | +0.0022 | [-0.0020, +0.0070] | 84.5% |
| es | +0.7641 | **+0.7645** | +0.0004 | [-0.0036, +0.0044] | 58.5% |
| fil | +0.5091 | **+0.5123** | +0.0032 | [-0.0029, +0.0090] | 84.8% |
| fr | +0.6590 | **+0.6796** | +0.0207 | [+0.0136, +0.0275] | 100.0% |
| it | +0.6750 | **+0.6740** | -0.0010 | [-0.0060, +0.0037] | 31.9% |
| ja | +0.7877 | **+0.8037** | +0.0160 | [+0.0099, +0.0228] | 100.0% |
| pt | +0.8450 | **+0.8444** | -0.0006 | [-0.0040, +0.0027] | 36.6% |
| si | +0.4251 | **+0.4207** | -0.0044 | [-0.0125, +0.0035] | 14.7% |
| **medie** | +0.6838 | **+0.6867** | +0.0029 | | 59.5% |

Configuratia noua urca fuziunea pe 6 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0029**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6867** | [+0.6722, +0.7010] | |
| fuziune − A | +0.0868 | [+0.0746, +0.0978] | 100.0% |
| fuziune − B | +0.0223 | [+0.0167, +0.0279] | 100.0% |
| configuratia noua − cea de azi | +0.0029 | [+0.0011, +0.0048] | 99.9% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6000 |
| semnalul B singur, `lolo` | 0.6644 |
| fuziunea de azi, A = `p_multi` | 0.6838 |
| **fuziunea cu ansamblul de surse** | **0.6867** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0296**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.35 | 9 | 5179 | +0.6142 | +0.7019 | 0.0877 | 0.0044 |
| de | 0.750 | 0.30 | 9 | 5054 | +0.5926 | +0.6817 | 0.0891 | 0.0021 |
| en | 0.875 | 0.35 | 9 | 5054 | +0.5731 | +0.6672 | 0.0941 | 0.0050 |
| es | 0.875 | 0.35 | 9 | 5031 | +0.5869 | +0.6792 | 0.0923 | 0.0041 |
| fil | 0.750 | 0.35 | 9 | 5054 | +0.6219 | +0.7072 | 0.0853 | 0.0037 |
| fr | 0.875 | 0.35 | 9 | 5055 | +0.6042 | +0.6886 | 0.0844 | 0.0046 |
| it | 0.625 | 0.35 | 9 | 5054 | +0.5984 | +0.6890 | 0.0906 | 0.0037 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5966 | +0.6748 | 0.0782 | 0.0030 |
| pt | 0.875 | 0.35 | 9 | 5057 | +0.5776 | +0.6703 | 0.0927 | 0.0042 |
| si | 0.625 | 0.35 | 9 | 5024 | +0.6345 | +0.7171 | 0.0826 | 0.0036 |

Latimea medie a curbei lui w e 0.0877, iar a criteriului de candidati 0.0038, adica de 23 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
