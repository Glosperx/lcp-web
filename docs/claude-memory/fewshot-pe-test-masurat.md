---
name: fewshot-pe-test-masurat
description: "21 aug 2026 - few-shot cross-lingual rulat pe test: SINGUR pierde (-0.0123), dar ansamblul de trei prompturi plus unirea cifrelor da 0.688506, cel mai mare castig masurat pana acum"
metadata: 
  node_type: memory
  type: project
  originSessionId: c41c7657-b13d-4c6e-b16c-1f1864b8ecb1
  modified: 2026-08-21T18:21:31.006Z
---

Rulat **21 august 2026**. Referinta e sistemul cu temperatura, **0.683849**, din
[[distributia-b-temperatura]]. Raport: `output/e_fewshot.md`. **Nimic nu s-a adoptat.**

Cost real: `prompt_lab.py --model gemma4-12b-4bit --variants v3_fewshot --split test`, 5624 de
instante in **5783 s = 1.6 ore**, la **1.03 s per item**. Estimarea de 3.8 ore venea din cele 2.44 s
masurate pe trial, cand rulau si alte variante in paralel. NaN = 0.

## Rezultatul principal, si e o RASTURNARE trial-test

Patru configuratii, toate cu B recitit din distributii si temperatura realeasa LOLO pe grila extinsa:

| config | ce e | B singur | fuziune | fata de 0.683849 | limbi stricate |
|---|---|---|---|---|---|
| `FS` | few-shot SINGUR | 0.634641 | 0.671531 | **-0.012282** [-0.0184, -0.0065] | de, en, fil, pt, si |
| `FSK` | few-shot singur + unirea cifrelor | 0.631345 | 0.670010 | -0.013800 | aceleasi cinci |
| `FS3` | media celor TREI prompturi | 0.664449 | 0.686736 | +0.002880 [+0.0011, +0.0048] | **de**, -0.0110 |
| `FS3K` | cele trei + unirea cifrelor | 0.666461 | **0.688506** | **+0.004642** [+0.0026, +0.0068] | **niciuna** |

**Few-shot singur PIERDE pe test.** Pe trial era cea mai buna varianta individuala, +0.697 fata de
+0.686 al perechii zero-shot; pe test da B = 0.634641 fata de 0.659202, adica **-0.0246**, si strica
cinci limbi din zece cu interval care exclude zero. E cea mai clara rasturnare trial-test masurata in
proiect, si intareste [[decalaj-trial-test-masurat]]: cifra de trial nu prezice, iar aici nici ordinea
nu s-a pastrat pentru varianta singura. S-a pastrat doar ordinea ANSAMBLU > pereche.

**Ce trece bara: `FS3K` = 0.688506**, +0.004642, CI pereche [+0.002619, +0.006756], P(>0) = 100%,
**zero limbi stricate**. Rezista si la Bonferroni pentru cele patru configuratii: CI 98.75%
[+0.001913, +0.007292]. E de aproape trei ori castigul lui `prio_K`.

**Capcana de citit: germana.** `FS3` cade DOAR pe ea, -0.0110 [-0.0174, -0.0044]; `FS3K` o duce la
-0.0055 [-0.0122, +0.0014], adica trece pe muchie. Deci conditia „nicio limba stricata" separa FS3 de
FS3K pe o singura limba aflata la limita. Nu e o cifra pe care sa te sprijini fara sa o spui.

## Cele doua parghii sunt ADITIVE, nu redundante

- unirea cifrelor singura (`prio_K`): +0.001682
- ansamblul few-shot singur (`FS3`): +0.002880
- suma: +0.004562, stivuite: **+0.004642**, interactiune **+0.000080**

`FS3K` fata de `prio_K` da +0.002960 [+0.001115, +0.004774], deci few-shot-ul adauga peste unirea
cifrelor; `FS3K` fata de `FS3` da +0.001762 [+0.000688, +0.002876], deci unirea adauga peste few-shot.
Spre deosebire de `prio_KW`, care era redundant cu `prio_K` (+0.00018).

**Consecinta de decizie:** `FS3K` CONTINE unirea cifrelor, pe care Alexandru a refuzat s-o adopte pe
21 august. Deci adoptarea lui `FS3K` reia acea decizie, si moșteneste bifurcatia din
[[bifurcatii-de-declarat]]. `FS3` singur nu o moșteneste, dar strica germana.

## De ce merge ansamblul desi membrul nou e mai slab

**REZOLVAT pe 22 august prin control, vezi [[ansamblul-de-prompturi-formula]].** Mecanismul e EXACT
formula de reducere a variantei, `r_ens = (suma r_i)/sqrt(n + 2*suma rho_ij)`, care prezice ansamblul
observat la 0.0003. Zero reziduu, deci exemplele few-shot nu aduc informatie noua.

Nu e nici pur si simplu „decorelare": niciun rezumat scalar nu prezice castigul. Conteaza combinatia
lui r solo cu TOATE corelatiile perechi. Corectie fata de ce scria aici initial si fata de
[[prompt-ansamblu-decorelat]].

**Si consecinta e negativa pentru paper:** `marcat`, care nu foloseste nicio eticheta, da un castig
INDISTINGUIBIL de few-shot, +0.001510 [-0.001142, +0.004239]. Deci revendicarea fata de G-Eval nu se
poate scrie.

Forma distributiilor la T=1 e aproape identica (masa pe argmax 0.858 few-shot, 0.877 si 0.859
zero-shot; atomi efectivi 1.46, 1.43, 1.44), dar T-ul ales difera mult: **few-shot singur vrea T=4,
perechea zero-shot vrea T=12, ansamblul de trei alege T=6**. Ansamblul foloseste o SINGURA temperatura
pentru toate trei, deci T=6 e un compromis. `make_bt_runs` are deja grila `per-prompt` pentru cate un T
per prompt. **RULAT pe 22 august si INCHIS:** `FS3P` 0.687241 si `FS3KP` 0.687604, amandoua SUB
`FS3K` si amandoua strica portugheza, ca `distTpp` care strica spaniola. Vezi
[[ansamblul-de-prompturi-formula]].

## FS3 nu era in brief, si de ce intra oricum

Cernuta pe trial din `output/promptlab_gemma4-12b-4bit.csv`, **inainte de orice cifra de test**: media
celor trei da +0.7109, fata de +0.6970 few-shot singur si +0.6860 perechea. Costa zero inferenta,
fiindca distributiile celor doua zero-shot sunt deja pe test. Cele patru configuratii sunt o
multiplicitate de patru si sunt declarate ca atare in raport.

Unirea cifrelor alege `1|23|45` unanim pe toate zece limbile si la `FS3K`, ca la `prio_K`. La `FS`
insa criteriul alege partitia NEUTRA pe 9 din 10 limbi, deci parghia unirii nu e universala: cere
distributia larga a ansamblului tempeat, nu orice B.

## Revendicarea zero-label se pastreaza tehnic, dar nu mai valoreaza nimic

`prompt_lab.lolo_shots` ia cele 6 exemple numai din **trial-ul celorlalte limbi**, si `measure`
cheama `load_mlsp("trial")` LITERAL, nu `load_mlsp(split)`. Efect secundar dorit: exemplele unei limbi
sunt aceleasi pe trial si pe test, deci configuratia e fixa, nu reesantionata.

**Dar revendicarea fata de G-Eval nu se mai poate scrie**, fiindca `marcat`, fara nicio eticheta, da un
castig indistinguibil. Vezi [[ansamblul-de-prompturi-formula]]. Corecteaza si ce spera
[[noutate-si-precedente-lcp-multilingv]] de la punctul asta.

Vezi [[cod-nou-fewshot-si-prefix]] pentru fisierele si controalele.
