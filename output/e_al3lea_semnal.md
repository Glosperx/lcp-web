# Al treilea semnal peste A si B: exista loc?

Raportul sesiunii din **23 august 2026**. Artefactele de detaliu, fiecare cu cifrele lui:
`e_literatura_al3lea.md` (sinteza de literatura), `e_c_sanatate.md` (poarta de sanatate a lui C),
`e_c_frontiera_toti.md` (poarta de frontiera peste toti candidatii), `e_c3_*.md` (fuziunea cu trei
termeni, per candidat), `e_shap_multi.md` (atribuire multilingva si reziduul semnat).

**Nimic nu s-a adoptat.** Sistemul ramane 0.683849.

**Raspunsul scurt la intrebarea sesiunii: NU, nu mai e loc pentru un al treilea semnal dintre cele
disponibile.** Toti cei **treisprezece** candidati masurati au corelatia partiala cu eticheta,
controland pe fuziune, sub **0.043** in valoare absoluta, cand poarta cere **0.1077**. Sapte au fost
dusi cap la capat prin fuziune, si niciunul n-a depasit zero. Dar drumul pana la raspuns a
scos doua lucruri care valoreaza mai mult decat cifra, si amandoua sunt in sectiunile 1 si 5.

---

## 0. Doua corecturi la premisele sesiunii

1. **Pe test existau C de la TREI modele, nu sapte.** Celelalte patru erau numai pe trial, cu 300 de
   randuri. S-au masurat in sesiunea asta, vezi sectiunea 6.
2. **Artefactele SHAP de pe disc sunt stale in doua feluri diferite**, si niciunul nu e "romanesc" asa
   cum spunea fisa de memorie. `analysis_shap.py` ruleaza pe **CompLex EN cu split aleator 80/20**,
   deci `Pearson test (toate) = 0.7898` e cifra aia; `shap_beeswarm.py` e cel romanesc, antetul lui
   spune "prezice OUTPUT-ul modelului final (68.90)". Niciunul nu e per limba, niciunul nu e LOLO, si
   niciunul nu atinge 0.683849. Nu se citeaza nimic de acolo.

---

## 1. Descoperirea sesiunii: coloana C a lui Gemma nu masoara surprisal

Asta n-a fost cautat. A iesit dintr-un control de cinci linii, rulat inainte de a cheltui doua ore.

### 1.1 Cifra care nu se poate

`gemma4-12b-4bit`, modelul care furnizeaza semnalul B al sistemului adoptat, are surprisal mediu
**23,95 nati per subword** pe itemi reali de test. Vocabularul lui are 262.144 de intrari, deci o
distributie **uniforma** ar da ln(262144) = **12,48 nati**. O valoare peste uniform e imposibila
pentru un model antrenat pe text real: inseamna ca modelul e mai prost decat aruncarea cu zarul.

Comparatia, pe aceleasi propozitii:

```
                     surprisal("Paris" | "The capital of France is ___")
qwen3-8b-4bit                     0.79
qwen35-9b-8bit                    0.56
llama31-8b-4bit                   0.81
aya-expanse-8b-4bit               1.17
gemma4-12b-4bit                  23.06
```

### 1.2 Ce e stricat, si ce NU e

Diagnosticul separa curat cele doua cai prin care trece acelasi model:

```
prin SABLONUL DE CHAT (calea semnalului B)      pe TEXT BRUT (calea semnalului C)
"What is the capital of France?" -> "Paris"     "The capital of France is" -> "1111111111"
rate("thrombocytopenia") = 0.9049
rate("water")            = 0.0000
r_B pe test = +0.642, cel mai bun din bazin
```

**Semnalul B e sanatos si nu se atinge.** Semnalul C de la Gemma e o coloana degenerata.

`<bos>` e o parte din cauza dar nu toata: adaugat manual, surprisal-ul lui "Paris" scade de la 23,06
la 14,84, dar argmaxul ramane o cifra si continuarea ramane `1111111111`. Cauza de fond se vede in
varianta de 8 biti a aceluiasi model, care **nu se incarca deloc**:

```
ValueError: Received 11 parameters not in model:
vision_embedder.patch_dense.bias, vision_embedder.patch_dense.biases, ...
```

Checkpointul e multimodal (`gemma4_unified`), iar `mlx_lm` 0.31.3 il incarca numai prin remaparea
fortata din `mlsp_common.LLM_POOL`, la o clasa text-only. Varianta de 4 biti trece prin remapare si
ruleaza, dar capacitatea de continuare pe text brut nu supravietuieste.

### 1.3 Ce inseamna asta pentru ce e deja scris

- **Sistemul de 0.683849 nu e afectat.** B nu trece pe calea stricata, si cele trei cifre de control
  de mai sus o arata direct.
- **Paperul multilingv nu e afectat**: nu pomeneste surprisal nicaieri.
- **Paperul romanesc foloseste surprisal**, dar de la `RoLlama3-8b-Instruct` prin backendul
  `transformers`, alt model si alta cale. Nu e atins de defectul asta. **Dar riscul e din aceeasi
  clasa** (model instruction-tuned, continuare pe text brut), si `analysis_c_sanatate.py` a fost facut
  agnostic de backend tocmai ca sa poata fi rulat si acolo. **Nerulat, declarat.**
- **Propozitia din `e_bakeoff_test.md`**, "Semnalul C pe test: r mediu per model intre -0.065 si
  +0.094", trebuie corectata: capatul de -0.065 e al unei coloane degenerate, nu al unui surprisal
  slab.
- **Pentru sectiunea de reproductibilitate a paperului**, si e o propozitie care trebuie scrisa:
  modelul care furnizeaza semnalul B se incarca numai printr-o remapare fortata de tip de model, iar
  fidelitatea remaparii e confirmata empiric pe calea de chat si **infirmata pe calea de text brut**.

### 1.4 Poarta care lipsea, si acum exista

`analysis_c_sanatate.py`, trei probe pe text brut. Rezultatul pe tot bazinul:

```
                     SANATOS  surprisal_mediu  ln|V|   continuare pe text brut
qwen3-8b-4bit           True             5.02  11.93   ' Paris. The capital of Italy is Rome. The'
qwen3-8b-8bit           True             4.78  11.93   ' Paris. The capital of Italy is Rome. The'
qwen35-9b-4bit          True             5.73  12.42   ' Paris.\nThe capital of France is Paris.'
qwen35-9b-8bit          True             5.39  12.42   ' Paris.\nThe capital of France is Paris.'
llama31-8b-4bit         True             4.22  11.76   ' Paris. The capital of France is Paris. The'
aya-expanse-8b-4bit     True             5.66  12.45   ' Paris. It is located in the north-central'
gemma4-12b-4bit        False            23.95  12.48   '1111111111'
gemma4-12b-8bit        False              NaN    NaN   nu se incarca
```

**Sase sanatoase din opt.** Cele trei probe sunt necesare impreuna: Gemma **trece** proba de ordonare
(23,06 < 28,79 la Paris fata de Bucharest) desi e degenerat, deci ordonarea singura n-ar fi prins-o.

Doua observatii care merita retinute:

- `llama31-8b-4bit` a fost **respins ca brat B**, dar `surprisal()` ruleaza deliberat fara sablon de
  chat, deci motivul respingerii nu-l atinge ca sursa de C. Aici trece poarta.
- Nu e o poveste despre marime. Gemma e cel mai mare din bazin, dar cade din cauza incarcarii, nu a
  numarului de parametri. **Ipoteza de inverse scaling ramane netestata la noi**, fiindca marimile
  distincte disponibile sunt doar 8B, 9B si 12B, iar cea de 12B a fost eliminata din alt motiv.

---

## 2. Poarta de frontiera, scrisa inainte de a masura orice

Pentru fuziunea adoptata F si un candidat C, ambele standardizate, plafonul peste orice pondere u a
amestecului `(1-u)*zF + u*zC` e corelatia multipla, care se rescrie exact ca
`R_max^2 = r_F^2 + partial^2 * (1 - r_F^2)`. Deci conditia `R_max >= r_F + bara` devine **o singura
cifra**:

> **Corelatia partiala a candidatului cu eticheta, controland pe fuziune, trebuie sa fie in valoare
> absoluta cel putin 0.1077.**

Echivalent, in forma directa: `|r_C - 0.683849*rho| >= 0.078581 * sqrt(1 - rho^2)`. Tabelul de praguri,
cu ramura de SUPRESOR pe dreapta (un semnal corelat cu fuziunea dar nu cu eticheta, care corecteaza
scazandu-se):

```
rho cu fuziunea   r_C minim (normala)   r_C maxim (supresor)
0.00              +0.0786               -0.0786
0.10              +0.1466               -0.0098
0.20              +0.2138               +0.0598
0.30              +0.2801               +0.1302
0.50              +0.4100               +0.2792
```

Praguri pentru alte ambitii: +0.0022 cere partial 0.0752; **+0.0045 cere 0.1077**; +0.0089 cere 0.1517.

### Predictiile scrise inainte de a masura rho, si ce s-a intamplat

```
candidat          predictia mea                                   rho masurat   verdict
qwen3-8b-4bit     trece doar daca rho<=0.024 sau rho>=0.25;       +0.125        CORECTA, cade
                  cade in fereastra 0.025..0.25                                  in fereastra
gemma4-12b-4bit   trece pentru orice rho >= 0.026                 -0.100        GRESITA: am
                                                                                 presupus rho>0
```

Predictia pe Gemma a fost gresita, si motivul merita scris: am argumentat ca surprisal si complexitate
impart frecventa, deci rho ar fi pozitiv. La Gemma a iesit **negativ**, fiindca acolo si r_C era
negativ; cele doua semne se rasucesc impreuna si corelatia partiala ramane la **-0.0015**, adica zero.
Retrospectiv, aia era chiar semnatura coloanei degenerate.

---

## 3. Tabelul portii, peste toti candidatii

Toti pe splitul de test, agregat ca medie pe cele zece limbi. `dR` e **plafonul** cu u optim in-sample
per limba, nu castigul.

```
                     r_C     rho_F   partial      prag     R_max        dR  limbi_trec  semn
resid_lolo     -0.642824 -0.925046 -0.012112  0.117318  0.695578  0.011730           1     7
qwen3-8b-4bit   0.094217  0.125115  0.038398  0.117318  0.688258  0.004410           3     8
medie (2 C)     0.053833  0.075209  0.034726  0.117318  0.688227  0.004378           3     8
vecinatate      0.134741  0.217603 -0.033991  0.117318  0.687822  0.003973           2     6
entropie        0.325741  0.491833 -0.037490  0.117318  0.687350  0.003502           3     8
qwen35-9b-8bit  0.003491  0.010913  0.025986  0.117318  0.686987  0.003138           2     6
dezacord_B     -0.104188 -0.136630 -0.003106  0.117318  0.685140  0.001291           1     6
dezacord (C)   -0.044078 -0.076781  0.026872  0.117318  0.684993  0.001144           1     9
```

**Cel mai instructiv rand e `entropie`.** Are **cel mai mare r_C din tot tabelul, +0.326**, de trei ori
mai mult decat surprisal-ul. Si e al cincilea din opt dupa plafon, cu corelatie partiala **-0.037**,
fiindca rho-ul lui cu fuziunea e 0.492. Adica tot ce stie e ce stie deja fuziunea. E ilustrarea cea mai
curata a regulii pe care s-a construit sesiunea: **calitatea unui semnal nu spune nimic despre ce
aduce; conteaza numai partea lui ortogonala.**

Niciun candidat nu are `partial` peste 0.04 in valoare absoluta. Poarta cere 0.1077.

---

## 4. Ce s-a masurat cap la cap, prin fuziune

Poarta e ieftina dar nu inlocuieste masuratoarea. Cinci candidati au fost dusi pana la capat, cu
`u` ales LOLO pe grila [-0.30, +0.30] care contine zero, interval PERECHE prin bootstrap pe contexte, si
conditia de limba citita inaintea mediei.

```
candidat      delta pe fuziune   CI 95% pereche          P(>0)   limbi stricate   podea de zgomot
qwen3-8b-4bit -0.000363          [-0.001264, +0.000517]  21.0%   fil              -0.000140
entropie      -0.000433          [-0.001417, +0.000512]  21.0%   de, fr           -
dezacord (B)  +0.000000          [+0.000000, +0.000000]   0.0%   niciuna          -
vecinatate    -0.000892          [-0.001587, -0.000202]   0.7%   si               -
resid_lolo    -0.002347          [-0.003243, -0.001498]   0.0%   fil, ja          +0.000000
```

Controlul de reproducere trece: cu grila lui `u` redusa la {0}, `p3` reproduce `p_fuz` cu eroare
maxima **1.11e-16** pe limbi.

`dezacord` alege **u = 0 pe 10 limbi din 10**, exact cum varianta lui de PONDERE alesese `a = 0` pe
10 din 10 pe 22 august. Doua parametrizari diferite ale aceleiasi marimi, acelasi zero.

Si poarta si-a facut treaba: a prezis pentru `qwen3-8b-4bit` un plafon de +0.00441 cu u oracol per
limba, iar masurat cu u global LOLO iese -0.00036. Diferenta e explicata, si nu de marimea optimului ci de SEMNUL lui. `u` optim per limba merge de la
**-0.36 pe filipineza** la **+0.18 pe germana**, iar criteriul LOLO alege +0.05 pentru noua limbi din
zece. Cele doua limbi care trec poarta individual o trec **in directii opuse**: germana are corelatie
partiala **+0.2364** peste un prag de 0.1235, filipineza **-0.1611** peste un prag de 0.0788. O pondere
globala nu poate servi si una si alta, si le mediaza la aproape zero.

### 4.1 Tiparul e o proprietate a LIMBII, nu a modelului. Predictie inregistrata inainte de date

Corelatia partiala per limba, pentru trei modele din **trei familii diferite** (Qwen3, Qwen3.5,
Llama-3.1):

```
lang   qwen3-8b-4bit   qwen35-9b-8bit   llama31-8b-4bit
de           +0.2364          +0.1912           +0.2343
si           +0.0815          +0.0603           +0.0482
it           +0.0516          +0.0453           +0.0279
pt           +0.0484          +0.0425           +0.0523
es           +0.0415          +0.0666           +0.0240
ja           +0.0361          -0.0185           +0.0254
en           +0.0294          +0.0435           +0.0190
ca           +0.0268          -0.0068           +0.0334
fr           -0.0067          -0.0236           -0.0373
fil          -0.1611          -0.1406           -0.1723
```

Cele trei coloane coreleaza intre ele, peste limbi, la **0.963, 0.991 si 0.949**. Semnul e acelasi pe
**8 limbi din 10**, iar cele doua exceptii sunt limbi unde toate trei valorile sunt sub 0.04, adica
zgomot.

**Deci ce surprisal-ul are de spus peste fuziune e o proprietate a limbii, nu a modelului care il
calculeaza.** Germana are mereu ~+0.20, filipineza mereu ~-0.16, si asta nu se schimba trecand de la
Qwen la Llama.

**Predictia, scrisa la 18:58, inainte ca celelalte trei modele sa termine de rulat:** un ansamblu de
sase surprisal-uri va urca plafonul putin, fiindca medierea unor membri corelati la 0.95-0.99 reduce
zgomot dar pastreaza tiparul, si **castigul masurat cap la cap va ramane in +/-0.001 fata de zero**,
fiindca `u` global tot nu poate servi simultan germana la +0.18 si filipineza la -0.36. Numarul de
membri nu atinge cauza.

### 4.2 Cele patru modele lipsa, si verificarea predictiei

Masurate pe test cu `--only-c`, 5624 de randuri fiecare, **75 de minute in total** la 0.18-0.21 s per
item, adica de patru ori mai ieftin decat o rulare completa cu B. Toate patru au trecut intai poarta
de sanatate.

Poarta de frontiera peste toate cele **sase** surprisal-uri valide:

```
                          r_C     rho_F   partial      prag     R_max        dR   semn
qwen3-8b-8bit        0.102795  0.134273  0.042157  0.117318  0.689232  0.005383      8
medie a celor 6      0.054779  0.075704  0.035309  0.117318  0.688552  0.004703      8
qwen3-8b-4bit        0.094217  0.125115  0.038398  0.117318  0.688258  0.004410      8
llama31-8b-4bit      0.051102  0.069106  0.025489  0.117318  0.688039  0.004190      8
aya-expanse-8b-4bit  0.032224  0.043613  0.031048  0.117318  0.687001  0.003152      8
qwen35-9b-8bit       0.003491  0.010913  0.025986  0.117318  0.686987  0.003138      6
qwen35-9b-4bit       0.002345  0.006860  0.027743  0.117318  0.686560  0.002712      6
```

`qwen3-8b-8bit` e **primul candidat din toata sesiunea al carui PLAFON trece bara**: +0.005383 fata de
+0.0045. Corelatia lui partiala ramane insa 0.042, adica o treime din poarta.

**Verificarea predictiei scrise la 18:58, inainte ca datele astea sa existe:**

```
                        prezis                    masurat cap la cap
ansamblul de 6          in +/-0.001 fata de zero  -0.000868  [-0.001657, -0.000084]
qwen3-8b-8bit singur    -                         -0.000756  [-0.001585, +0.000042]
```

**Predictia se confirma.** Amandoua strica filipineza cu interval care exclude zero, si amandoua aleg
`u = +0.05` pe opt limbi din zece, exact ca varianta cu doi membri. Peste podeaua de zgomot, ansamblul
iese la **-0.000721**.

Motivul e cel scris in 4.1 si se vede acum direct: **cei sase membri coreleaza intre ei la 0.7506**,
mediat pe limbi. Medierea unor membri atat de corelati reduce zgomot dar nu poate schimba tiparul per
limba, iar tiparul e cauza.

Si o cifra care nu e despre semnal: **`qwen3-8b-8bit` e cel mai bun surprisal din tot bazinul**,
r_C = +0.1028, peste varianta lui de 4 biti la +0.0942. E cel mai mare `dR` masurat, si tot nu trece.

### 4.3 E.4, controlul de cuantizare, se inchide pentru C

Ramas deschis in `e_bakeoff_test.md`, fiindca lipseau doua din cele patru rulari. Acum sunt toate:

```
pereche          4 biti    8 biti    diferenta
qwen3-8b         +0.0942   +0.1028   +0.0086
qwen35-9b        +0.0023   +0.0035   +0.0012
```

**Cuantizarea aproape nu conteaza pentru surprisal.** Ambele perechi merg in aceeasi directie, 8 biti
peste 4 biti, dar cu 0.0086 si 0.0012, adica sub latimea oricarui interval relevant. Diferenta dintre
familii, de la +0.1028 la +0.0023, e de zece ori mai mare decat diferenta dintre cuantizari ale
aceluiasi model.

---

## 5. A doua descoperire: de ce strica frecventa pe filipineza

Intrebarea era deschisa din sesiunea trecuta, formulata acolo ca "nu stim mecanismul": scoaterea
coloanei de frecventa urca fuziunea pe filipineza cu +0.0225, CI exclude zero, dar un indicator de OOV
per token nu repara nimic. Acum are raspuns, din doua masuratori independente.

**Prima.** Surogatul lexical din `e_shap_multi.md` arata cat de mult se sprijina sistemul pe `zipf`, pe
fiecare limba. Pe filipineza importanta lui e **0.8608** prin permutare, printre cele mai mari din
tabel, iar surogatul reconstruieste `p_fuz` din lexical singur la r = 0.867.

**A doua.** Pe filipineza **152 din 570 de tinte, adica 26,7%, au zipf exact 0.** Nicio alta limba cu
frecventa disponibila nu trece de 3,6%. Si pe exact acele randuri fuziunea se prabuseste:

```
limba   tinte cu zipf=0   r al fuziunii pe ele   r pe restul
fil     152 din 570        +0.2320                +0.4642
```

Rata de esec comun a celor doua semnale, adica itemii unde si A si B sunt deplasate in acelasi sens cu
peste o deviatie standard, e **25,7% pe itemii cu zipf = 0** fata de **15,6% pe restul** aceleiasi limbi.

**Mecanismul, formulat.** Sistemul se sprijina cel mai tare pe frecventa exact pe limba unde frecventa
lipseste pentru un sfert din tinte. Scoaterea coloanei ajuta fiindca il forteaza sa nu se mai sprijine
pe o trasatura pe care un sfert din itemi n-o pot furniza. **Si de asta indicatorul de OOV n-a
reparat:** un indicator spune "aici valoarea lipseste", dar nu pune nimic in locul ei. Marcarea unei
gauri nu e umplerea ei.

Asta se leaga direct de observatia deja masurata pe sinhaleza, unde scoaterea frecventei din
CELELALTE noua limbi urca bratul A cu +0.0243. Aceeasi propozitie, doua limbi: **un model antrenat pe
limbi care au frecventa invata sa depinda de ea, iar limbile care n-o au platesc.**

---

## 6. Reziduul semnat, si de ce t-SNE nu s-a rulat

Criteriul a fost scris inainte, si e mai restrictiv decat pare:

> Un indicator al unei regiuni cu eroare mare **in modul** e inutil prin constructie, fiindca singurul
> mecanism prin care ar putea intra e ponderea per item, iar aceea e inchisa cu `a = 0` pe 10/10 limbi
> si pe cinci seminte de zgomot. Ce se cauta e o regiune cu reziduu **SEMNAT** nenul.

Masurat: un model antrenat LOLO pe trasaturi fara eticheta prezice reziduul semnat la r out-of-fold
**+0.3519** pe medie, ceea ce pare mult. Dar corelatia lui cu fuziunea e **-0.925**: modelul invata in
principal sa reproduca minus predictia, adica o contractie. Corelatia partiala cu eticheta iese
**-0.0121**, si trece poarta pe **o singura limba din zece**.

Singura exceptie e **filipineza, cu partial -0.4096 si plafon +0.1101**, adica un castig urias pe o
limba. Dar `u` se alege pe celelalte noua, care vor toate ~0, deci filipineza primeste +0.05 si
pierde. Cap la cap: **-0.002347**, cu doua limbi stricate. E acelasi tipar ca la criteriul plat: ce e
adevarat pe o limba nu e invatabil de la celelalte noua.

**Deci pasul numeric a iesit negativ, si conform criteriului scris inainte graficele t-SNE si UMAP nu
s-au facut.** Nu e o omisiune, e decizia.

---

## 7. Atribuire: cele doua importante nu sunt de acord, si dezacordul e rezultatul

Surogat pe trasaturi lexicale, fara A si fara B, per limba. Doua importante:

```
                     zipf     nsub     length
permutare marginala  +0.7472  +0.0570  +0.0300
reantrenare fara ea  +0.2942  +0.0367  +0.0167
```

Permutarea da lui `zipf` de **2,5 ori** mai mult. E exact efectul prezis de Hooker, Mentch si Zhou
(Statistics and Computing 2021): permutarea nerestrictionata forteaza extrapolarea si supraestimeaza
trasaturile corelate. `shap` nu e instalat in `envs/ml_def` si nu s-a instalat pentru o figura; oricum
Kernel SHAP presupune independenta (Aas, Jullum si Loland 2021), deci ar fi fost al doilea membru al
aceleiasi familii, nu un al doilea punct de vedere. Reantrenarea fara coloana e chiar ce recomanda
Hooker si colegii in loc de permutare.

**Consecinta pentru paper:** nicio propozitie de forma "trasatura X conteaza de N ori mai mult decat Y"
nu se scrie pe o singura importanta.

Si o observatie despre coada, din acelasi tabel: **sinhaleza e singura limba unde fertilitatea bate
frecventa**, `nsub` +0.3309 fata de `zipf` indisponibil, iar surogatul lexical reconstruieste acolo
doar r = 0.4115 fata de 0.69-0.92 in rest. Adica pe sinhaleza sistemul nu se comporta ca un model
lexical, fiindca nu are din ce.

---

## 8. Tabelul de prioritizare, ordonat dupa RAPORT castig/cost

Castigul e **masurat pe fuziune**, nu asteptat, unde exista o cifra. Costul de calcul e citit din
marcajele de timp. Bara e +0.0045.

```
#  ce s-a masurat                dovada    castig pe fuziune      calcul   cod    ce s-a inchis                        bate bara?
1  poarta de sanatate a lui C    masurat   0 direct, dar a scos   12 min   145    "orice model din bazin poate da C";  n/a, e poarta
                                           un defect care ar fi                    2 din 8 nu pot, si unul e chiar
                                           contaminat 4 rulari                     modelul semnalului B
2  poarta de frontiera, 8 cand.  masurat   0 direct, dar respinge <1 min   323    surprisal, entropie, dezacord,       n/a, e poarta
                                           7 candidati pe hartie                   vecinatate, reziduu: toti sub 0.04
3  mecanismul filipinezei        masurat   0 pe cifra, dar inchide 3 min   291    "nu stim de ce strica frecventa pe    nu, e contributie
   (zipf = 0 pe 26.7% din tinte)           o intrebare deschisa                    fil"; acum are mecanism si un test
4  C ca al treilea termen,       masurat   -0.000363              <1 min   207    surprisal ca semnal, DEFINITIV        nu
   qwen3-8b-4bit, u LOLO                   [-0.00126, +0.00052]
5  entropia lui B, aditiv        masurat   -0.000433              <1 min   ~10    incertitudinea lui B ca semnal        nu
                                           [-0.00142, +0.00051]                    aditiv (varianta-pondere era moarta)
6  dezacordul lui B, aditiv      masurat   +0.000000 exact        <1 min   ~10    dezacordul ca semnal aditiv; u = 0    nu
                                           u = 0 pe 10/10 limbi                    pe 10/10, ca si a = 0 pe 22 aug
7  vecinatatea semantica         masurat   -0.000892              <1 min    91    densitatea vecinatatii ca trasatura   nu
                                           [-0.00159, -0.00020]                    lexicala, fara resurse externe
8  reziduul semnat prezis LOLO   masurat   -0.002347              3 min    291    "exista o regiune identificabila      nu
                                           [-0.00324, -0.00150]                    fara etichete unde ambele cad"
9  atribuire: permutare fata de  masurat   0 pe cifra             3 min    (in 3) "importanta trasaturilor se poate     nu, e metodologie
   reantrenare                                                                     raporta cu o singura masura"
10 C de la 4 modele lipsa        masurat   ansamblu de 6:         75 min    ~20   ansamblul de surprisal-uri, si E.4    nu
                                           -0.000868                             pentru C; predictia din 4.1 confirmata
                                           [-0.00166, -0.00008]
11 t-SNE / UMAP                  NERULAT   -                      0 min     0     nimic; criteriul scris inainte a      nu
                                                                                   cerut ca pasul 8 sa fie pozitiv
```

Ordonat dupa raport, **primele trei locuri nu sunt cifre, sunt lucruri gasite**. Randurile 4-8, adica
toti candidatii de semnal, costa impreuna sub cinci minute si ies toate negative sau zero. Asta e
forma pe care o are o sesiune in care raspunsul e nu.

Randul cu cel mai prost raport e 10: **75 de minute pentru un rezultat prezis corect in avans**, la a
patra zecimala a semnului si in interval. A meritat totusi rulat, fiindca predictia era inregistrata si
trebuia verificata, si fiindca inchide E.4, controlul de cuantizare, ramas deschis din
`e_bakeoff_test.md`.

---

## 9. Raspunsul la intrebarea sesiunii

**Nu mai e loc pentru un al treilea semnal dintre cele disponibile, si acum se stie de ce.**

Motivul nu e ca semnalele candidate ar fi slabe. `entropie` are r_C = +0.326, ceea ce ar fi un semnal
respectabil. Motivul e ca **partea lor ortogonala pe fuziune e mica**: corelatia partiala maxima peste
cei treisprezece candidati masurati e +0.042, iar poarta cere 0.1077. Si acolo unde exista o parte ortogonala reala,
**semnul ei difera pe limbi**: germana +0.2364, filipineza -0.1611, amandoua peste pragul lor propriu,
in directii opuse. O pondere globala aleasa LOLO nu poate servi si una si alta.

Si literatura prezicea exact asta, dinainte: Oh si Schuler (Journal of Memory and Language 2025) arata
ca **frecventa si surprisal-ul sunt compensatorii**. Sistemul nostru are deja frecventa si se sprijina
puternic pe ea, deci surprisal-ul nu avea de unde sa aduca.

**Ce a iesit in schimb, si valoreaza mai mult decat cifra:**

1. **Un defect care ar fi contaminat orice masuratoare viitoare de C.** Modelul care da semnalul B nu
   poate modela text brut, iar coloana lui de surprisal, prezenta pe disc de la inceput, e degenerata.
   Poarta care il prinde nu exista pana azi.
2. **Mecanismul filipinezei**, o intrebare deschisa de o sesiune: 26,7% din tinte cu zipf = 0, si pe
   ele fuziunea da 0.2320 fata de 0.4642. Cu un test direct de facut, imputarea acelor zerouri din
   corpusul Wikipedia tagalog care exista deja pe disc.
3. **Poarta de 0.1077**, care de acum respinge sau accepta orice candidat viitor in sub un minut.
4. **Atribuirea nu se raporteaza cu o singura masura**: permutarea da lui `zipf` de 2,5 ori mai mult
   decat reantrenarea, pe aceleasi date si acelasi model.

**Ce ramane deschis, declarat, nerulat:**

- diversitatea contextuala (numarul de contexte distincte), singurul candidat lexical din literatura cu
  dovada ca subsumeaza frecventa; ~3 ore, corpusuri pentru toate cele zece limbi;
- imputarea zerourilor de frecventa pe filipineza din `data/freq_tail/`, care e testul direct al
  mecanismului de la punctul 2 si costa sub 30 de minute;
- surprisal din capul de MLM al lui XLM-R, si C de la un model sub 4B pentru ipoteza de inverse scaling;
- poarta de sanatate rulata pe `RoLlama3-8b-Instruct`, calea romaneasca.

## 10. Multiplicitate

Candidati de semnal masurati in sesiunea asta: **treisprezece prin poarta de frontiera, sapte dusi cap
la capat prin fuziune**. Jurnalul avea inainte 151 de randuri neadaugate, 102 adaugate si 84 in arhiva. Niciun
candidat nu s-a apropiat de bara, deci nu se pune problema unei corectii de multiplicitate pentru o
adoptie; se declara pentru completitudine.

## 11. Controale de protocol

- reproducere: cu grila lui `u` redusa la {0}, `p3` reproduce `p_fuz` cu eroare maxima **1.11e-16**;
- `--only-c` reproduce coloana C **bit cu bit**, 0 diferente din 30 de randuri fata de
  `output/bakeoff_test/qwen3-8b-4bit.csv`;
- podeaua de zgomot, cinci seminte, pe aceeasi grila: **-0.000140** la surprisal, **+0.000000** la
  reziduu;
- nimic din `output/bakeoff_test/` sau `output/bakeoff_test_Text/` nu a fost atins: cele sase fisiere
  au mtime din 17-20 august, iar rularile noi scriu in `output/surprisal_test/`, un director pe care
  `load_runs` nu-l citeste pentru niciun split;
- garda de fisier partial: un CSV citit in timpul rularii a produs tacut `R_max` 0.0558 si `dR` -0.628
  pentru `aya-expanse-8b-4bit` la 255 din 5624 de randuri. `load_c` refuza acum fisierele incomplete.
