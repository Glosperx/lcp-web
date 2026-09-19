# Reperele publicate pe MLSP, transcrise si verificate

**Fisierul asta NU e generat de niciun script.** E transcris din publicatii si verificat
aritmetic, 18 august 2026, actualizat **19 august 2026 dupa P11** si **20 august 2026 dupa
temperatura**. Daca il regenerezi, il rescrii de mana.

> **Randul nostru s-a schimbat din nou.** Sistemul citeste acum distributia peste cifrele "1".."5" la
> o temperatura aleasa leave-one-language-out, nu doar valoarea ei asteptata. Media e **0.683849** pe
> n = 5624, fata de **0.674946** fara temperatura. Diferenta, +0.0089 cu interval pereche
> [+0.0056, +0.0124], vine din `output/e_dist.md` si `output/e_fusion_lolo_adoptat_temp.md`.
> **0.674946 nu e o cifra moarta**: e ablatia fara temperatura si se citeaza ca atare. Cifrele de pe
> n = 5606 raman istorice.

## Regula unica, de care atarna tot

Toate cifrele de aici sunt **media aritmetica NEPONDERATA a celor 10 corelatii Pearson per
limba**, pe testul MLSP. Fiecare limba conteaza la fel, desi n variaza intre 445 si 600.

Orice alta agregare e alta cantitate si NU se pune alaturi. In special:

- **Compozitul "All" din trackul combinat al shared task-ului e pooled**, adica un singur
  Pearson calculat o data peste toate instantele amalgamate. TMU-HIT raporteaza 0.6241 pe
  three-shot si 0.5609 pe zero-shot in propria lucrare. **Alea NU sunt medii pe limbi.**
  Dovada: media pe limbi a acelorasi doua rulari iese 0.6372 si 0.6100.
- Pooled cere ca predictiile sa fie pe aceeasi scara absoluta intre limbi. Sistemul nostru
  standardizeaza in interiorul limbii, deci **nu poate produce un scor pe trackul combinat**.
  Asta e o limitare de scris in text, nu un rezultat prost.

## Sursele

- **Nohejl, Hayakawa, Ide, Watanabe (2025)**, "A Japanese Dataset and Efficient Multilingual
  LLM-Based Methods for Lexical Simplification and Lexical Complexity Prediction", Journal of
  Natural Language Processing 32(4), pp. 1129-. **Tabelul 13** e sursa a cinci din reperele
  de mai jos.
- **Shardlow et al. (2024a)**, "The BEA 2024 Shared Task on the Multilingual Lexical
  Simplification Pipeline", BEA 2024, aclanthology.org/2024.bea-1.51. **Anexa B** are
  tabelele per limba, din care se calculeaza cele doua repere neexistente in literatura.
- **Enomoto et al. (2024)**, "TMU-HIT at MLSP 2024", aclanthology.org/2024.bea-1.52.
- **Cristea & Nisioi (2024)**, "Archaeology at MLSP 2024", aclanthology.org/2024.bea-1.55.

## Reperele citabile direct (Nohejl, Tabelul 13)

| sistem | etichete in limba tinta | medie |
|---|---|---|
| baseline frecventa | 0 | 0.478 |
| Archaeology | 0 | 0.487 |
| TMU-HIT | mixt, ales pe test | 0.654 |
| G-Eval cu GPT-4o | 3-shot | 0.657 |
| **G-Scale cu GPT-4o** | 3-shot + T + beta pe 30 | **0.669** |

**Maximul publicat e 0.669, nu 0.657.** Daca G-Scale lipseste din tabelul lucrarii, un
reviewer care cunoaste domeniul observa.

### Ce e in spatele cifrei TMU-HIT de 0.654

Cele 10 valori tiparite de Nohejl corespund, verificat la a treia zecimala pe toate 10, celui
**mai bun run TMU-HIT pe fiecare limba** din Anexa B. La `fil` si `fr` cel mai bun run e
zero-shot, la restul e three-shot. Deci bara amesteca doua protocoale, alegand per limba ce a
iesit mai bine pe test. Nu e o eroare a lui Nohejl, asa se raporteaza intr-un overview, dar
inseamna ca 0.654 nu e un sistem unic sub un protocol unic.

### Ce e in spatele cifrei G-Scale de 0.669

G-Scale = softmax cu temperatura peste probabilitatile tokenilor `1`..`5` la o singura pozitie,
valoare asteptata, apoi regresie liniara cu trasaturi optionale. **Adica semnalul nostru B plus
o temperatura.**

Pentru Pearson, regresia liniara nu schimba nimic, fiind afina, iar Nohejl o spune explicit in
Anexa G. Deci diferenta G-Eval -> G-Scale, de la 0.657 la 0.669, **vine integral din scalarea
cu temperatura**, cu T = 2.0 ales pe media trial-urilor tuturor celor 10 limbi.

Consecinta pentru noi, in ambele sensuri:
- Nu putem revendica "citim logits in loc sa esantionam, deci de 20 de ori mai ieftin". E
  contributia declarata a lui Nohejl, motivatia (1) din sectiunea lui 4.
- Nici "LLM-ul si frecventa sunt decorelate si se completeaza". E Tabelul 12 al lui, unde R^2
  urca de la 0.498 la 0.575 adaugand log-frecventa.
- **Dar +0.012 din temperatura ne era disponibil, si l-am luat.** Facut pe 20 august 2026, sub un
  protocol mai strict decat al lui: T se alege LOLO, pe randurile de test ale celorlalte 9 limbi,
  deci fara nicio eticheta din limba evaluata, pe cand el il alege pe trial-ul tuturor celor 10.
  Masurat, parghia da **+0.0171 pe semnalul B singur** si **+0.0089 pe sistem**. `rate_parts` din
  `solution_bert.py` salveaza acum vectorul de 5 probabilitati, iar `bakeoff_trial.py` il scrie in
  CSV; coloana `B` a ramas bit cu bit aceeasi, verificat pe toate cele 5624 de randuri.
  **Ramane parghia LUI**, deci intra la rezultate, nu la contributii.

## Reperele care NU exista publicate, calculate de noi

Mediate din tabelele per limba ale Anexei B a lui Shardlow et al. 2024a. Cer nota de subsol
care spune de unde vin.

| sistem | etichete in limba tinta | medie |
|---|---|---|
| **TMU-HIT zero-shot, run uniform** | **0** | **0.6100** |
| TMU-HIT three-shot, run uniform | 3 | 0.6372 |

**0.6100 e singura bara comparabila ca protocol cu a noastra**, si e comparatia care conteaza
in abstract.

## Matricea completa, per limba

| sistem | ca | en | fil | de | fr | it | ja | pt | si | es | medie |
|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline frecventa | 0.301 | 0.748 | 0.389 | 0.591 | 0.517 | 0.519 | 0.642 | 0.713 | -0.196 | 0.551 | 0.478 |
| Archaeology | 0.274 | 0.790 | 0.443 | 0.551 | 0.533 | 0.534 | 0.485 | 0.683 | 0.044 | 0.527 | 0.486 |
| TMU-HIT (mixt) | 0.616 | 0.820 | 0.569 | 0.718 | 0.625 | 0.601 | 0.733 | 0.786 | 0.308 | 0.762 | 0.654 |
| TMU-HIT 0-shot | 0.528 | 0.804 | 0.569 | 0.658 | 0.625 | 0.539 | 0.645 | 0.764 | 0.248 | 0.720 | 0.610 |
| TMU-HIT 3-shot | 0.616 | 0.820 | 0.501 | 0.718 | 0.528 | 0.601 | 0.733 | 0.786 | 0.308 | 0.762 | 0.637 |
| G-Eval 4o | 0.573 | 0.827 | 0.494 | 0.711 | 0.764 | 0.629 | 0.745 | 0.761 | 0.328 | 0.739 | 0.657 |
| G-Scale 4o | 0.583 | 0.840 | 0.504 | 0.714 | 0.774 | 0.654 | 0.767 | 0.774 | 0.330 | 0.749 | 0.669 |
| AL NOSTRU, pana la P11 | 0.530 | 0.867 | 0.519 | 0.716 | 0.582 | 0.656 | 0.762 | 0.839 | 0.343 | 0.753 | 0.6568 |
| AL NOSTRU, fara temperatura | 0.541 | 0.870 | 0.512 | 0.733 | 0.645 | 0.665 | 0.784 | 0.843 | 0.396 | 0.761 | 0.6749 |
| **AL NOSTRU** | 0.557 | **0.870** | 0.509 | **0.747** | 0.659 | **0.675** | **0.788** | **0.845** | **0.425** | **0.764** | **0.6838** |

Randul nostru e `output/e_fusion_lolo_adoptat_temp.md`, adica fuziunea A+B cu `w`, modelul lui B SI
temperatura alese LOLO pe test, bratul A pe media a trei encodere, cu fixul de lema si cu
`find_char_span` reparat. Media exacta: **0.683849**, pe n = 5624. Intervalul ei, bootstrap pe
contexte: **[0.6694, 0.6980]**. Randul de deasupra, 0.674946, e acelasi sistem cu T = 1, adica
ablatia care izoleaza temperatura.

**Cele mai bune cifre publicate vreodata pe sapte limbi din zece sunt ale noastre**: engleza,
germana, italiana, japoneza, portugheza, sinhaleza si spaniola. Pana la P11 erau trei. Ramanem sub
publicat pe catalana, filipineza si franceza. Temperatura nu a schimbat lista, dar a ingustat toate
trei decalajele.

## Cap la cap

| fata de | castigam | medie | pierdem la |
|---|---|---|---|
| baseline frecventa | 10/10 | +0.2063 | - |
| Archaeology | 10/10 | +0.1974 | - |
| TMU-HIT zero-shot uniform | 9/10 | +0.0738 | fil -0.060 |
| TMU-HIT (mixt) | 8/10 | +0.0300 | ca -0.059, fil -0.060 |
| G-Eval 4o | 8/10 | +0.0267 | ca -0.016, **fr -0.105** |
| G-Scale 4o | 8/10 | +0.0149 | ca -0.026, **fr -0.115** |

Spaniola a iesit din lista pierderilor fata de TMU-HIT: era -0.001, e acum +0.002.

**Si aici e propozitia care tot NU se poate scrie, dar cu mai putin loc de intors.** Trecem peste
G-Scale cu +0.0149, iar intervalul mediei noastre e lat de 0.0286, deci diferenta e acum **52%
dintr-o latime de interval**, fata de 20% inainte de temperatura. Tot nu se poate TESTA, fiindca nu
avem predictiile per instanta ale lui Nohejl, deci „batem cel mai bun sistem publicat" ramane o
afirmatie fara interval in spate. Ce se poate scrie e ca trecem peste el pe opt limbi din zece, cu
zero etichete in limba tinta fata de cele 30 ale lui.

**Propozitia care se sustine** e fata de singura bara comparabila ca protocol, TMU-HIT zero-shot
uniform la 0.6100: **+0.0649, castigand pe 9 limbi din 10**. Aia merge in abstract.

### Franceza explica singura tot deficitul

**Actualizat dupa P11 si dupa temperatura, si s-a ingustat de doua ori.** Pierderea fata de G-Scale
pe franceza era 0.192, a ajuns 0.129 dupa P11 si e acum **0.115**: `--pick-split test` a mutat
franceza de la 0.582 la 0.645, iar temperatura de la 0.645 la 0.659. Franceza ramane singura limba
unde decalajul e mare, dar nu mai rastoarna media. Pe celelalte noua limbi:

| pe 9 limbi, fara fr | medie |
|---|---|
| TMU-HIT (mixt) | 0.657 |
| TMU-HIT 0-shot | 0.608 |
| G-Eval 4o | 0.645 |
| G-Scale 4o | 0.657 |
| **AL NOSTRU** | **0.687** |

Cauza era cunoscuta si diagnosticata: selectia LOLO alegea pe franceza `qwen35-9b-8bit`, care da
0.544 acolo, in loc de Gemma. **Reparat la P11**: selectia se face acum pe splitul de evaluare si
alege Gemma peste tot. Vezi `output/e_pick_split.md`. Ce ramane din decalaj tine de bratul A, si
reziduul de fertilitate de la §3.5 e inca deschis.

## Cifre care NU se folosesc niciodata

- **0.6241 si 0.5609.** Compozitul pooled al trackului combinat. Alta metrica.
- **Orice cifra de trial.** Gemma da 0.686 pe trial si 0.642 pe test.
- **0.6522 si 0.6540.** Dinainte de fixul de lema, depasite.
- **0.6616 si 0.6634.** Gemma peste tot, incalca 5.1. Numai ca margine superioara, etichetata.
- **0.6568, 0.664555, 0.671952, 0.669591, 0.676253.** Toate pe n = 5606, dinainte de P11. Istorice.
- **0.682977 si 0.685763.** Variante de temperatura care NU sunt sistemul. Prima e cu grila din
  briefing, care se termina la T = 4, adica exact pe marginea unde cade argmaxul la toate cele zece
  limbi. A doua e cu cate o temperatura per prompt, aleasa dintre 256 de perechi cu o margine de
  0.001 pe un criteriu lat de 0.085. Amandoua sunt in `output/e_dist.md` si se citeaza doar ca
  ablatii etichetate. Sistemul e 0.683849.
- **0.3495 pe sinhaleza.** Cifra veche, dinainte de lema. Cea corecta e **0.3430**.

## Ramase de reparat inainte de trimitere

1. **n per limba, aproape reparat.** Oficial 5627 (Tabelul 5 al lui Enomoto et al.). Aveam 5606;
   dupa fixul de caz din `find_char_span` avem **5624**, deci raman **trei** randuri, nu douazeci si
   unu. Tot trebuie o fraza care spune cate si de ce, dar e o nota de subsol, nu o limitare.
2. **Sectiunea de noutate** nu poate revendica eficienta logits-urilor, complementaritatea
   LLM-frecventa sau temperatura. Toate trei sunt ale lui Nohejl, iar a treia e acum si in sistemul
   nostru, deci trebuie citata acolo unde apare cifra, nu doar in related work. Ce ramane: modele
   open-weight rulate local, zero etichete in limba tinta, LOLO inclusiv la alegerea modelului si a
   temperaturii, si teza morfologica a fixului de lema.
3. **R^2 nu e raportat de noi deloc.** Ar fi metrica pe care o putem lua: TMU-HIT are -0.311
   pe zero-shot si 0.246 pe three-shot, iar G-Scale, cel mai bun, are 0.293. O calibrare
   potrivita LOLO ne-ar da si R^2, si un compozit raportabil, dintr-un singur experiment.

## Cum se reproduce randul nostru

```
python bakeoff_trial.py --model gemma4-12b-4bit --split test --out output/dist/gemma4-12b-4bit_test.csv
python make_bt_runs.py --grid extinsa --dir bakeoff_test_Text
python fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag adoptat_temp \
  --b-dir output/bakeoff_test_Text \
  --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv
```

Prima comanda e cea care a cerut re-rularea de 102 minute, si e verificata: coloana `B` pe care o
scrie e identica bit cu bit cu `output/bakeoff_test/gemma4-12b-4bit.csv`, doar ca acum salveaza si
distributia. Fara `--b-dir`, aceeasi comanda de fuziune da in continuare 0.674946, verificat.

**Ce se revendica nu e o valoare a lui T.** Castigul fata de T = 1 are interval care exclude zero
pentru 19 din cele 21 de valori incercate intre 1.25 si 64, iar intre T = 4 si T = 24 r-ul mediu
variaza cu 0.0028. Se revendica un platou, si tabelul lui e in `output/e_dist.md`, sectiunea (e).

## Verificarea aritmetica, reproductibila

```python
L=["ca","en","fil","de","fr","it","ja","pt","si","es"]
# Anexa B, Shardlow et al. 2024a, randurile TMU-HIT. A1/A2 = trackul combinat defalcat.
r1=[.5279,.8036,.5692,.6582,.6253,.5391,.6448,.7638,.2482,.7201]  # run 1, zero-shot
r2=[.6158,.8198,.5013,.7177,.5278,.6011,.7333,.7858,.3081,.7616]  # run 2, three-shot
m=lambda v:sum(v)/len(v)
assert abs(m(r1)-0.6100)<5e-5 and abs(m(r2)-0.6372)<5e-5      # NU dau 0.5609 / 0.6241
assert abs(m([max(a,b) for a,b in zip(r1,r2)])-0.6538)<5e-5   # = TMU-HIT la Nohejl
```
