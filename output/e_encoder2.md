# Semnalul A, redeschis: extractie, frontiera, coada

Raportul sesiunii din **23 august 2026**. Artefactele de detaliu, fiecare cu cifrele lui:
`e_literatura_encoder.md` (sinteza de literatura), `e_frontiera_enc.md` (poarta de cernere),
`e_extractie.md` (sweep-ul de 16 configuratii), `e_wsrc.md`, `e_pondere_flabel.md`,
`e_freq_tail.md`, `e_coada.md`, `e_bilant.md` (tabelul cu toti candidatii).

**Nimic nu s-a adoptat.** Sistemul ramane 0.683849.

---

## 0. Prima verificare: se reproduc cifrele vechi?

Da, si o corectie de citit inainte de a cita ceva. Cele patru tabele per encoder din
`output/e_encoder.md` reproduc **exact** pe splitul de acum, la a patra zecimala, pe toate cele zece
limbi. Dar celula de total a acelui raport spune `medie | 5606`, in timp ce coloana lui `n` insumeaza
**5624**. E o constanta ramasa in urma, exact tiparul cunoscut. Cifrele de brat A de acolo se pot
cita; **coloana de fuziune nu**, fiindca e pe 0.664581, adica pe sistemul de dinainte de pick-split
si de temperatura.

Doua lucruri s-au inchis fara sa coste nimic, prin masuratoare directa:

- **Decuparea de 500 de caractere nu pierde nimic**, si nici trunchierea la 512 de tokeni: 0 randuri
  din 5624 depasesc limita, 0 span-uri negasite, 0 tinte fara subword. Contextul decupat are mediana
  intre 39 de caractere (ja) si 241 (ca). Ipoteza ca sinhaleza si-ar pierde contextul din dreapta prin
  fertilitate mare e **falsa**: maximul ei e 187 de tokeni, la o treime din limita.

---

## 1. Aritmetica scrisa INAINTE de a rula, si care a prezis aproape tot

### 1.1 Transmisia A spre fuziune

Citita din trei rapoarte cu acelasi brat B si acelasi protocol, deci singura diferenta e sursa lui A:

```
sursa lui A              r_A        r_fuziune   factor
un singur xlmr           0.580723   0.669591    referinta
media a 3 (fara large)   0.601244   0.675391    0.283
media a 4                0.607890   0.675996    0.236
marginal, de la 3 la 4                          0.091
```

Factorul **scade** pe masura ce A se imbunatateste. Consecinta: ca fuziunea sa urce cu bara de
+0.0045, bratul A trebuie sa urce cu **+0.017 pana la +0.049**. Pentru scara, trecerea de la un
encoder la patru a adus +0.027. **Deci nicio parghie singura de encoder nu putea ajunge, si asta se
stia inainte de prima rulare.**

### 1.2 Frontiera ca poarta

Formula `r_ens = (suma r_i)/sqrt(n + 2*suma rho_ij)` s-a verificat ca **identitate pe fiecare limba**,
nu doar pe medie: eroarea maxima 1.11e-16. Pragurile scrise inainte, pentru un al patrulea membru:

```
r al membrului nou   rho maxim (optimist)   (pesimist)
0.50                 0.643                  0.432
0.55                 0.742                  0.521
0.578 (ca ceilalti)  0.799                  0.573
0.62                 0.885                  0.650
```

Membrii de acum sunt la rho 0.846-0.887. **Un membru din aceeasi familie era mort inainte de a fi
rulat**, si asta a ordonat toata sesiunea: nu s-a cautat un encoder mai bun, s-a cautat unul
structural diferit.

### 1.3 Poarta se valideaza cap la cap

Cu vectorul cuvantului izolat ca al patrulea membru, frontiera a prezis ΔA = **-0.0107** si s-a
masurat **-0.0107**; prin transmisie a prezis pe fuziune intre -0.0010 si -0.0028, si s-a masurat
**-0.0021**, la mijlocul intervalului. Poarta functioneaza, deci de acum un candidat se poate cerne
fara sa i se ruleze fuziunea.

---

## 2. Extractia tokenilor: singurul efect mare din toata sesiunea

`--emb-cfg` a fost expus (`frozen_trial_gap` accepta parametrul de cand exista, dar `main()` nu-l
pasa niciodata), si s-au rulat cele 16 combinatii straturi x pooling pe xlmr.

**Poolingul `first` bate `last` cu +0.0253 pe medie, cu acelasi semn pe 10 limbi din 10 si pe toate
cele 4 familii de straturi.** Asta **inverseaza** rezultatul din Acs, Kadar si Kornai (EACL 2021),
care pe probing morfologic gasesc `first` cea mai proasta strategie, cu pana la 45 de puncte sub
`last` pe finlandeza.

Inversarea nu e un accident, si se verifica in trei feluri:

- efectul creste cu fertilitatea limbii, **r = +0.726, p = 0.017**;
- e mai mare pe tintele multi-subword (+0.0299) decat pe toate (+0.0253), iar 950 din 5624 de tinte
  au un singur subword, unde toate strategiile coincid;
- e maxim pe sinhaleza, **+0.097**, limba cu cea mai mare fragmentare.

**Explicatia.** Ei probeaza trasaturi morfologice, caz, gen, forma verbala, care traiesc in sufix;
acolo ultimul subword e chiar raspunsul. Noi prezicem o proprietate lexicala, care tine de identitatea
cuvantului. Ultimele bucati sunt fragmente scurte, impartite de mii de cuvinte (`ts`, `es`, `a` in
catalana), deci nu identifica lexemul; prima bucata poarta materialul initial, care il identifica.
Aceeasi segmentare, semnal opus, fiindca sarcina e alta. **Nu contrazice lucrarea lor, ii delimiteaza
domeniul**, si asta e o propozitie care merita scrisa in paper.

Onestitate necesara: segmentarea lui XLM-R nu e morfologica (`controvertits` da `contro`+`verti`+`ts`),
deci formularea corecta nu e "prima bucata e lema", ci "ultima bucata e un fragment impartit, prima nu".

### 2.1 Straturile nu conteaza, si de ce era usor sa cred contrariul

Selectia LOLO peste grila de 16 valoreaza **+0.00016** peste podeaua de zgomot, adica nimic. Dar asta
e o afirmatie despre grila, nu despre pooling, si distinctia se vede masurand fiecare axa separat:

```
axa                              latime pe limba   latime pe medie   acelasi semn
pooling (straturi fixate)        0.0296            0.0253            10/10
straturi (pooling fixat la mean) 0.0287            0.0087             7/10
straturi (pooling fixat la first)0.0236            0.0116             8/10
```

Latimea PE LIMBA e aproape egala pe cele doua axe, deci dupa ea ar parea la fel de importante. Dupa
mediere se despart, iar ce le separa cu adevarat e **constanta semnului**. O axa larga dar cu semn
care se schimba de la limba la limba e zgomot cu amplitudine mare. Numai poolingul e efect.

Consecinta pentru protocol: `first` **nu** e argmaxul unei grile plate, e capatul unei axe
sistematice. Axa de straturi se lasa la valoarea mostenita, fiindca nimic din ea nu supravietuieste
medierii.

**Pe fuziune insa**, chiar si cel mai bun candidat de extractie da **+0.0015 cu interval care include
zero**. Nu trece bara. Exact ce prezicea transmisia.

---

## 3. Ce s-a inchis, cu cifre

### 3.1 Reprezentari structural diferite: amandoua moarte, pe pragul scris dinainte

```
candidat                        r      rho la ceilalti   castig pe A   prag scris inainte
contextual ++ izolat (ctxiso)   0.5610 0.8974            -0.0032       -
numai vectorul izolat (isoonly) 0.5020 0.8216            -0.0107       r>=0.55 si rho<=0.75
```

`isoonly` a ratat **ambele** jumatati ale pragului. Argumentul lui Ethayarajh, ca un vector static
explica sub 5% din varianta unuia contextual, chiar prezice decorelare, si se vede: pe sinhaleza rho
scade la 0.335. Dar calitatea cade odata cu ea, la r 0.1015 acolo. **Decorelarea nu se poate cumpara
cu orice pret**, si frontiera spune exact cat de mult e "prea mult".

### 3.2 Glot500: candidatul cel mai promitator, si tot nu trece

Vocabular de 401.145 fata de 250.002 al lui XLM-R, tokenizeaza sinhaleza si tagalog la nivel de cuvant
intreg. Si totusi: r **0.5625**, rho **0.8899**, castig pe A **-0.0018**. Nici macar pe sinhaleza nu
ajuta (0.2468 fata de 0.3306 al ansamblului). Ipoteza "vocabular extins deci reprezentare diferita" e
respinsa cu cifre.

### 3.3 e5 cu prefixul lui: caveatul se inchide, si era mic

`output/e_encoder.md` declara ca e5 a fost evaluat fara `query: `, deci cifra lui e o margine
inferioara. Masurat acum: A **0.5751 -> 0.5747**, adica **-0.0004**, in urcare pe 4 limbi din 10;
fuziunea 0.680172 -> 0.680511. **Caveatul era corect ca principiu si neglijabil ca marime.**

Capcana platita, verificata pe octeti inainte de rulare: prefixul muta offset-urile cu 7 caractere.
Fara deplasarea span-ului s-ar fi citit `valent`, `a`, `▁afectiuni` in loc de `▁afectiuni`, `lor` —
si nimic n-ar fi crapat.

### 3.4 Izotropia: literatura nu se transfera, si acum se stie de ce

```
transformare              varianta scoasa   r_A       fuziune    fata de referinta
niciuna (referinta)       -                 0.5778    0.679888   -
minus 1 componenta        6.8%              0.5710    0.679067   -0.0008
minus 5 componente        19.4%             0.5444    0.670478   -0.0094
albire ZCA completa       -                 0.5742    0.678426   -0.0015
```

**Explicatia e chiar in literatura care motiveaza metoda.** Timkey si van Schijndel noteaza ca
directiile dominante ale spatiului corespund unor lucruri "neinteresante", frecventa tokenului de
exemplu. Pentru ei frecventa e zgomot care strica similaritatea cosinus. **Pentru noi frecventa e
semnalul.** Scoaterea primei componente scoate 6.8% din varianta si costa -0.0068 pe A; cinci
componente scot 19.4% si costa -0.0334. Asta e cea mai curata ilustrare din sesiune a regulii ca o
metoda nu se importa fara sa se verifice ce inseamna cantitatea ei in sarcina noua.

### 3.5 `w_src = 0.738`: premisa intrebarii era falsa

Bratul EN-only nu e mai bun. `p_en` da **0.5945**, `p_multi` da **0.5980**. Criteriul de selectie are
latimea 0.0033 si nimereste argmaxul adevarat pe **1 limba din 10**. Toata parghia valoreaza **0.0027**
cap la cap, de la 0.682053 la `w_src = 0` pana la 0.684764 la `w_src = 1`.

**Mecanismul, masurat direct:** corelatia cu semnalul B e 0.7084 pentru `p_multi` si **0.6813** pentru
`p_en`, care e mai decorelat pe 9 limbi din 10, iar pe sinhaleza cu +0.1521. Frontiera A+B la 50/50
prezice +0.0025 in favoarea lui `p_en`; masurat cap la cap iese +0.0027.

**Deci `w_src` mare nu inseamna ca transferul din engleza e mai bun.** Inseamna ca bratul englez,
nevazand niciun rand de MLSP, face ALTE greseli decat un LLM care vede propozitia. E reducere de
varianta, acelasi mecanism ca la ansamblul de encodere, la alt nivel. In paper nu se prezinta ca
rezultat despre transfer cross-lingual.

### 3.6 Ponderarea per limba fara etichete: inchisa, si plafonul insusi nu trece

Intrebarea era daca efectul de +0.0994 al lui LaBSE pe sinhaleza se poate exploata fara selectie.
Trei ponderi fara etichete, validate PE LIMBA:

```
pondere                      pe medii   pooled 30   IN LIMBA (Spearman)   castig pe A
fertilitatea tokenizerului   -0.564     -0.636       +0.260               -0.0029
corelatia cu minus-frecventa +0.756     +0.668       -0.250               -0.0008
acordul cu ceilalti membri   -0.969     +0.652       +0.050               -0.0007
```

Coloana `pooled 30` a lui `zipf` arata **+0.668**, care pare excelent, dar in interiorul limbii e
**-0.250**, adica in directia gresita. E exact capcana din sesiunea trecuta: o marime care prezice pe
agregat nu autorizeaza o procedura care alege per limba. Toate trei ponderile pierd, iar **plafonul
cu beta ales de oracol e 0.603 fata de 0.598**, adica +0.005 pe A, care dupa transmisie e sub bara
chiar si cu etichete. Inchisa definitiv.

---

## 4. Coada, si e partea cu cel mai mult de spus

### 4.1 Plafonul: cat valoreaza frecventa acolo unde exista

Ablatia `--no-freq`, care anuleaza coloana peste tot, costa **+0.0597 pe bratul A** al celor opt limbi
care au frecventa reala. Deci trasatura e importanta, si absenta ei pe sinhaleza nu e un detaliu.

**Dar apare ceva ce nimeni nu cauta.** Pe fuziune, ablatia costa -0.0051 pe medie si strica patru
limbi cu interval care exclude zero. Pe filipineza insa **imbunatateste cu +0.0225, CI [+0.0060,
+0.0381], P = 99.5%**. Adica **pe filipineza coloana de frecventa strica activ**, si e singura limba
unde scoaterea ei ajuta semnificativ. Filipineza are 152 din 570 de tinte cu zipf 0, de patru ori mai
mult decat urmatoarea limba.

Si a doua observatie din acelasi tabel: pe sinhaleza, unde coloana era deja goala, **scoaterea
frecventei din CELELALTE noua limbi urca bratul A cu +0.0243**. Explicatia: un model antrenat pe limbi
care AU frecventa se sprijina pe o trasatura pe care sinhaleza n-o poate furniza. Problema cozii nu e
doar ca ii lipseste o coloana, e ca modelul invata sa depinda de ea in alta parte.

### 4.2 Tabelele de frecventa din Wikipedia

Construite pentru sinhaleza (8.03 milioane de tokeni, 491.077 tipuri) si tagalog (12.27 milioane,
377.474 tipuri). Acoperirea tintelor de test:

```
limba   inainte (wordfreq)   exact   plus prefix   plus subword
si      0 din 600            89.8%   99.7%         100%
fil     418 din 570 (73.3%)  90.0%   97.7%         100%
```

**Capcana platita, si nu crapa nimic.** Prima versiune tokeniza cu `re.findall(r"[^\W\d_]+")`. In
Python `\w` **nu** cuprinde semnele vocalice sinhaleze, care sunt in categoria Unicode Mn, deci
fiecare cuvant sinhalez se sparge in consoane separate: `ලංකාව` devine `ල`, `ක`, `ව`. Tabelul ar fi
iesit plin de litere izolate cu frecvente uriase. Se foloseste `regex` cu `[\p{L}\p{M}]`, care
pastreaza si ZWJ-ul din conjunctele sinhaleze.

**Controlul cerut de protocol trece:** 0 randuri schimbate din 14082 in celelalte opt limbi, pe toate
cele trei trepte. Verificarea a trebuit facuta constienta de NaN, fiindca `ja` si `si` au coloanele de
suprafata NaN si `!=` le raporta ca schimbate la fiecare rulare.

### 4.3 Rezultatul, si e negativ pe fuziune

```
varianta      r_A      fuziune    fata de referinta   fuz_si    fuz_fil   limbi stricate
referinta     0.5778   0.679888   -                   0.409545  0.513283  -
exact         0.5812   0.677790   -0.0021             0.388145  0.516198  2
prefix        0.5814   0.678952   -0.0009             0.402482  0.516293  1
subword       0.5813   0.678949   -0.0009             0.402137  0.514727  1
```

Pe bratul A sinhaleza chiar urca cu **+0.0147** la treapta `prefix`, exact cum ar trebui. Pe fuziune
insa sinhaleza **scade**, de la 0.4095 la 0.4025. E decuplarea A-fuziune inca o data, si e motivul
pentru care protocolul cere ca orice cifra sa fie dusa pana la capat.

**Predictia tipologica scrisa inainte s-a confirmat.** In docstring-ul lui `build_freq_tail.py`, scris
inainte de masuratoare, backoff-ul pe prefix e motivat pentru sinhaleza, care e aglutinanta si
sufixeaza, iar pentru tagalog, care foloseste infixe si reduplicare, motivatia e declarata mai slaba.
Masurat: pe `si` prefixul aduce +0.0147, pe `fil` **pierde -0.0097**, si cu cat backoff-ul e mai
agresiv cu atat pierde mai mult (`subword` -0.0191). Exemplele arata de ce: `kalikutin` cade pe `kali`
si `mamaos` pe `mama`, care sunt cuvinte fara legatura.

### 4.4 Encoderele monolingve nu incap in protocol

Nu din cauza unui scor prost, ci structural: sub LOLO, regresorul care prezice limba L se antreneaza
pe CompLex EN plus celelalte noua limbi, embedate cu ACELASI encoder. Un model monolingv sinhalez nu
poate reprezenta franceza. Masurat, fertilitatea in subword-uri per tinta:

```
limba   xlmr   SinBERT   RoBERTa-Tagalog
si      3.32   5.19      21.24
fil     2.37   8.61       1.66
fr      2.02   9.76       3.33
en      1.88   8.93       2.22
```

SinBERT sparge celelalte limbi in 4.15 ori mai multe bucati (mediana). Si o cifra care surprinde:
**SinBERT fragmenteaza sinhaleza mai rau decat XLM-R**, 5.19 fata de 3.32, fiindca are un vocabular de
52.000 fata de 250.000. Nici macar avantajul de tokenizare pe limba proprie nu e garantat.

Ce ramane utilizabil dintr-un model monolingv fara sa strice protocolul: un scalar per item care nu
cere regresor cross-lingual, de pilda surprisal-ul din capul de MLM. Declarat, nerulat.

### 4.5 Indicatorul de OOV per token: ideea a venit din masuratoare si tot nu tine

Ablatia de la 4.1 sugereaza direct ca zerourile de OOV induc in eroare, iar `freq_na` de la
`na_policy` e per LIMBA, nu per token. `solution_bert.lexical` avea de mult `feats=("oov",)`, coloana
indicator `zipf == 0`, nefolosita niciodata pe calea multilingva. S-a expus si s-a rulat.

Rezultat: singur **0.678914** (fata de 0.679888), in ansamblu de trei **0.683647** (fata de 0.683849).
Ambele sub referinta lor. Deci problema filipinezei **nu** e ca modelul confunda "rar real" cu
"negasit"; un indicator care face exact distinctia aia nu repara nimic. Ce e, ramane deschis.

---

## 5. Ansamblurile, adica singurul loc unde ceva urca

Aceeasi mediere neponderata a trei encodere ca sistemul, fara niciun parametru liber; se schimba doar
ce se mediaza.

```
ansamblu de trei             r_A       fuziune    fata de sistem   fuz_si    fuz_fil
sistemul (last4, mean)       0.601072  0.683849   -                0.425137  0.509095
cu poolingul `first`         0.606299  0.686010   +0.0022           0.440567  0.506283
cu frecventa de coada, prefix0.593992  0.682255   -0.0016           0.404370  0.514135
cu indicatorul de OOV        0.597198  0.683647   -0.0002           0.423819  0.513553
```

**`ens3_first` e cea mai mare cifra a sesiunii: 0.686010, adica +0.0022 fata de sistem, cu intervalul
mediei [+0.0004, +0.0039] si P = 99.0%.** Urca pe 8 limbi din 10; sinhaleza urca cu **+0.0154** si
germana cu +0.0036, amandoua cu interval care exclude zero.

**Si totusi nu se califica pentru adoptie, din doua motive, in ordinea din protocol.**

1. **Filipineza e stricata cu interval care exclude zero**: -0.0028, CI [-0.0052, -0.0003], P = 1.2%.
   Protocolul spune ca aceasta conditie se citeste INAINTEA mediei. O singura limba stricata
   semnificativ opreste adoptia, indiferent ce face media.
2. **+0.0022 e sub bara de +0.0045**, adica sub castigul onest asteptat dupa scaderea optimismului de
   selectie.

Merita spus si de ce e coerent cu tot restul: poolingul `first` ajuta cel mai mult unde fragmentarea e
mare (si, ja) si cel mai putin unde e mica. Filipineza are 11.9% tinte de un singur subword si e una
dintre limbile unde `first` aduce cel mai putin (+0.0022 pe brat A). Nu e o surpriza, e aceeasi
mecanica citita in cealalta directie.

---

## 6. Tabelul de prioritizare, ordonat dupa raport castig/cost

Castigul e **masurat**, nu asteptat, si e pe FUZIUNE. Costul de calcul e citit din marcajele de timp
ale rularilor. Bara e +0.0045.

```
#  ce s-a masurat              dovada    castig pe fuziune  cost calcul  cost cod   bate bara?
1  pooling `first`, un encoder masurat   +0.00114           2.9 min      ~25 linii  nu (CI include 0)
2  pooling `first`, ansamblu   masurat   +0.0022 vs sistem  8.7 min      0 linii    nu, si strica fil
3  cel mai bun din grila       masurat   +0.00146           3.9 min      0 linii    nu (CI include 0)
4  e5 cu prefixul lui          masurat   +0.00061           2.8 min      ~10 linii  nu
5  indicator OOV per token     masurat   -0.00097           0.7 min      ~8 linii   nu
6  izotropie, -1 componenta    masurat   -0.00075           0.8 min      ~40 linii  nu
7  frecventa de coada, prefix  masurat   -0.00093           0.7 min      ~180 linii nu
8  Glot500 ca al 4-lea membru  masurat   -0.0018 pe A       3.0 min      1 linie    nu
9  ctxiso                      masurat   -0.0036            4.9 min      0 linii    nu
10 albire ZCA                  masurat   -0.00155           0.7 min      0 linii    nu
11 ponderare fara etichete     plafon    -0.0007 .. -0.0029 0 min        ~90 linii  nu, nici oracolul
12 numai vectorul izolat       masurat   -0.0131            2.5 min      ~12 linii  nu
13 izotropie, -5 componente    masurat   -0.00935           0.7 min      0 linii    nu
14 `w_src`, diagnostic         masurat   0 pe cifra         0 min        ~110 linii nu, e contributie
15 ablatie de plafon           plafon    -0.00511           0.7 min      ~10 linii  nu, e masuratoare
```

Ordonat dupa raport, primele patru locuri sunt lucruri care pe partea B n-ar fi meritat niciodata
rulate: 2.8 pana la 3.9 minute fiecare. Pe partea A o rulare completa costa minute, iar `fuse_ab`
costa **11 secunde**, deci nu exista motiv sa se raporteze vreodata numai cifra pe brat.

Costul cel mai prost raportat la ce a adus e **frecventa de coada**: ~180 de linii, doua corpusuri
descarcate, si un rezultat negativ pe fuziune. Dar el a produs singura observatie noua despre
filipineza, deci nu e cheltuiala pierduta, e cheltuiala mutata de la cifra la contributie.

### Ce s-a inchis, si nu se mai reia

- alegerea stratului: axa nu supravietuieste medierii pe limbi (semn constant doar 7/10)
- selectia LOLO peste grila de configuratii: +0.00016 peste podeaua de zgomot
- `ctxiso` si `isoonly` ca membri: sub pragul de frontiera scris inainte
- Glot500 ca al 4-lea membru: rho 0.8899, deci mort prin aritmetica
- e5 fara prefix: caveatul era real dar valoreaza -0.0004 pe A
- izotropia in toate cele trei variante
- ponderarea per limba fara etichete: nici plafonul cu oracol nu trece
- `w_src` ca rezultat despre transfer: e reducere de varianta, si parghia valoreaza 0.0027
- encoderele monolingve: incompatibile structural cu LOLO zero-label

### Ce ramane deschis

- **De ce strica frecventa pe filipineza.** Scoaterea coloanei urca fuziunea cu +0.0225, CI exclude
  zero, dar indicatorul de OOV per token nu repara. Nu stim mecanismul.
- **Surprisal din capul de MLM** ca inlocuitor de frecventa, inclusiv dintr-un model monolingv, care
  e singura cale prin care un model monolingv incape in protocol. Declarat, nerulat.
- **Pooling cu atentie peste subword-uri**, castigatorul din Acs et al. Cere parametri invatati, deci
  ar rupe proprietatea zero-label daca s-ar antrena pe etichete.
- **Modele pe octeti sau caractere** (CANINE, ByT5, MYTE). Arhitecturi diferite, nu greutati de pus
  intr-un `AutoModel`; la ByT5 notiunea de "stari pentru subword-urile tintei" nici nu e definita la
  fel.

---

## 7. Recomandare

**Nu se adopta nimic.** Niciun candidat nu trece bara de +0.0045 cu zero limbi stricate, si asta era
prezis de aritmetica transmisiei inainte de prima rulare.

Ce merita dus in paper, si nu tine de cifra:

1. **Inversarea fata de Acs, Kadar si Kornai.** E un rezultat cu mecanism verificat in trei feluri, pe
   10 limbi din 10, si delimiteaza domeniul unei lucrari publicate in loc sa o contrazica.
2. **Frontiera ca poarta de cernere**, validata cap la cap: prezice ΔA la a patra zecimala si castigul
   pe fuziune in interval. E o unealta metodologica, nu un rezultat despre date.
3. **`w_src` explicat**, ca sa nu ramana in paper o propozitie despre transfer care nu e adevarata.
4. **Observatia despre coada**, care e mai tare acum decat era la inceputul sesiunii: nu doar ca
   sinhalezei ii lipsesc doua din trei trasaturi lexicale, ci ca **un model antrenat pe limbi care AU
   frecventa se sprijina pe o trasatura pe care sinhaleza n-o poate furniza** (+0.0243 pe brat A cand
   frecventa se scoate de peste tot), si ca **pe filipineza coloana strica activ** (+0.0225 pe
   fuziune cand se scoate, CI exclude zero). Amandoua sunt masurate, si niciuna nu era stiuta.
5. **Sinhaleza a urcat de la 0.4251 la 0.4406** in `ens3_first`, cel mai mare castig per limba din
   sesiune. Nu ajunge pentru adoptie, dar arata ca directia "coada, prin extractie" e reala.

Decizia care ramane a lui Alexandru: daca `ens3_first`, la +0.0022 cu CI care exclude zero pe medie
dar cu filipineza stricata, merita raportat ca varianta, sau lasat complet deoparte.
