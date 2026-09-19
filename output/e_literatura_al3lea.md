# Literatura pentru al treilea semnal: de unde vine un semnal cu adevarat NOU

Sinteza ceruta pentru sesiunea din 23 august 2026. Regula de citire: fiecare intrare spune **ce s-a
masurat**, **pe ce sarcina**, si **ce NU se transfera** la cazul nostru. Cazul nostru e: complexitate
lexicala per item, zece limbi, protocol zero-label in limba evaluata, doua semnale deja fuzionate la
r = 0.683849, bara de adoptie +0.0045, si constrangerea care leaga e decorelarea, nu calitatea.

Unde n-am o cifra verificata, scrie ca n-o am. Nu se completeaza din memorie.

---

## 1. Surprisal si timpul de citire

### 1.1 Forma legaturii: logaritmica, nu liniara

**Shain, Meister, Pimentel, Cotterell si Levy, PNAS 2024**, "Large-scale evidence for logarithmic
effects of word predictability on reading time". Masoara forma functiei care leaga previzibilitatea de
dificultatea de procesare, pe date de citire la scara mare. Rezultat: functia e **logaritmica**, adica
efectul e in surprisal, `-log p`, nu in probabilitate. Lucrarile anterioare erau neconcludente din
cauza numarului mic de participanti si a gamei limitate de estimari de surprisal.

**Wilcox, Pimentel, Meister, Cotterell si Levy, TACL 2023, 11:1451-1470**, "Testing the Predictions of
Surprisal Theory in 11 Languages". Unsprezece limbi din cinci familii. Trei predictii testate:
surprisal prezice timpii de citire; entropia contextuala prezice si ea; functia de legatura e liniara
in surprisal. **Toate trei se confirma crosslingvistic.**

**Ce nu se transfera.** Amandoua masoara timpi de citire, o variabila de PROCES, pe cuvinte in text
curgator. Noi prezicem o judecata de complexitate agregata peste adnotatori, o variabila de PRODUS.
Forma legaturii nu ne ajuta: noi standardizam in interiorul limbii si masuram Pearson, deci o
transformare monotona a lui `p` nu schimba aproape nimic. Ce se transfera e doar existenta unui efect
nenul, si aia am masurat-o singuri: r_C intre -0.14 si +0.27 pe limba.

### 1.2 Inverse scaling: modelele mai mari prezic mai PROST

**Oh si Schuler, TACL 2023, 11:336-350**, "Why Does Surprisal From Larger Transformer-Based Language
Models Provide a Poorer Fit to Human Reading Times?". Masoara: relatie **strict monotona, pozitiva si
log-liniara intre perplexitate si potrivirea cu timpii de citire**, pe variantele GPT-Neo si OPT, pe
doua seturi de date independente. Adica un model cu perplexitate mai mica potriveste mai PROST.
Mecanismul propus, si e masurat, nu presupus: pierderea vine in principal din **surprisal-ul prea mic
pe cuvintele de clasa deschisa**, substantive si adjective. Modelele mari ajung sa prezica prea bine
exact cuvintele rare, pe care oamenii nu le prezic.

**Oh si Schuler, Findings of EMNLP 2023**, "Transformer-Based Language Model Surprisal Predicts Human
Reading Times Best with About Two Billion Training Tokens". Optimul nu e la capatul scarii, e la
**~2 miliarde de tokeni de antrenare**.

**Ce se transfera, si e singurul loc unde literatura prezice ceva ce am putut verifica.** Ipoteza spune
ca modelul mai mic ar trebui sa dea un C mai bun. Pe cele trei modele valide de pe test, ordinea merge
in directia prezisa: 8B da r_C **+0.094**, 9B da **+0.003**. Dar cu doua puncte nu se testeaza o
monotonie, iar al treilea, Gemma de 12B, a fost eliminat de poarta de sanatate, nu de marime. **Deci
ipoteza ramane deschisa la noi**, si testul ei cere un model sub 4B, care nu s-a rulat.

**Ce nu se transfera.** Cifrele lui Oh si Schuler sunt pe modele BASE, antrenate numai pe modelare de
limba. Bazinul nostru e format din modele instruction-tuned, unele si cuantizate cu antrenare. Poarta
de sanatate a aratat ca asta nu e un detaliu: vezi sectiunea 6.

### 1.3 Frecventa si previzibilitate sunt COMPENSATORII

**Oh si Schuler, Journal of Memory and Language 2025, 143:104645**, "Dissociable frequency effects
attenuate as large language model surprisal predictors improve". Masoara efectele separabile ale
frecventei si ale previzibilitatii pe timpii de citire, in functie de marimea modelului si de cantitatea
de date. Rezultat: **efecte pozitive robuste ale marimii modelului si ale volumului de antrenare asupra
cat de multa varianta explica FRECVENTA**, in timp ce contributia surprisal-ului scade. Adica cele doua
se substituie una alteia.

**Asta se transfera direct, si explica rezultatul nostru mai bine decat orice altceva.** Semnalul A al
sistemului contine `zipf` ca trasatura, iar surogatul lexical din `e_shap_multi.md` arata ca `zipf` e
trasatura dominanta pe noua limbi din zece. Daca frecventa si surprisal-ul sunt compensatorii, atunci
un C adaugat peste un sistem care are deja frecventa nu are de unde sa aduca. Cifra care confirma:
corelatia partiala a lui C cu eticheta, controland pe fuziune, e **+0.038** fata de un prag de 0.1077.

---

## 2. Frecventa fata de previzibilitate: diversitatea contextuala

**Adelman, Brown si Quesada, Psychological Science 2006, 17:814-823**, "Contextual Diversity, Not Word
Frequency, Determines Word-Naming and Lexical Decision Times". Masoara: pe trei seturi de citire cu
voce tare si trei de decizie lexicala, **efectele de frecventa dispar cand se controleaza diversitatea
contextuala, dar nu si invers**. Diversitatea contextuala e numarul de contexte distincte in care apare
cuvantul, nu numarul total de aparitii. Efectul se extinde si la duratele de fixatie in citirea de
propozitii.

**Ce se transfera.** E cel mai puternic candidat din literatura pentru o trasatura lexicala noua, si
are exact profilul cerut: nu e o versiune mai buna a frecventei, e o cantitate diferita care o
subsumeaza. Si avem deja infrastructura partiala, `build_freq_tail.py` plus corpusurile Wikipedia
pentru sinhaleza (8,03 milioane de tokeni) si tagalog (12,27 milioane).

**Ce nu se transfera, si e decisiv pentru cost.** Ne trebuie corpusuri segmentate in documente pentru
toate cele zece limbi, nu doua, iar `wordfreq` da frecvente, nu numar de contexte. Estimat ~3 ore si
~200 de linii. Si exista un avertisment din literatura mai noua, **Johns si colegii, JML 2021**,
"Content matters: Measures of contextual diversity must consider semantic content": numararea bruta a
documentelor nu e suficienta, conteaza continutul semantic al contextelor.

---

## 3. Predictori psiholingvistici in afara frecventei

| norma | acoperire verificata | multilingv? |
|---|---|---|
| varsta de achizitie (AoA) | **299 de cuvinte, 25 de limbi**, Luniewska si colegii, Behavior Research Methods 2016 | da, dar minuscul |
| concretete | **37.058 de cuvinte plus 2.896 de expresii**, peste 4.000 de participanti, Brysbaert, Warriner si Kuperman, BRM 2014 | **numai engleza** |
| prevalenta | derivata din acelasi tip de norming, pragul publicat e "cunoscut de cel putin 85% dintre evaluatori" | engleza si cateva limbi europene |
| densitatea vecinatatii semantice | se calculeaza din embedding, deci nu e o norma externa | da, gratis din cache |

**Ce nu se transfera, si taie randul din start.** Cele 299 de cuvinte ale lui Luniewska sunt toate
judecate ca **achizitionate inainte de 6 ani**, adica sunt capatul usor al scarii. Setul nostru de
test are 5624 de tinte, alese tocmai fiindca sunt candidate la a fi dificile. Suprapunerea e prin
constructie aproape goala, si ce ramane e concentrat exact acolo unde eticheta nu variaza. Concretetea
lui Brysbaert e engleza, iar engleza e limba unde suntem deja la 0.8700.

Deci normele psiholingvistice **nu sunt o parghie pentru coada**, care e unde ne trebuie: sinhaleza,
filipineza, catalana. Sunt un instrument pentru limbile pe care mergem deja bine.

---

## 4. Atribuire de trasaturi: cat pot sa cred ce vad

**Hooker, Mentch si Zhou, Statistics and Computing 2021, 31:82**, "Unrestricted permutation forces
extrapolation: variable importance requires at least one more model, or there is no free variable
importance". Masoara si argumenteaza: ruperea dependentelor dintre trasaturi in datele tinute deoparte
**forteaza modelul sa extrapoleze in regiuni cu putine sau zero date**, ceea ce **supraestimeaza masiv
trasaturile corelate**, si in importante, si in graficele de dependenta partiala. Recomandarea lor e in
titlu: importanta corecta cere **inca un model**, adica reantrenare fara trasatura.

**Aas, Jullum si Loland, Artificial Intelligence 2021, 298:103502**, "Explaining individual predictions
when features are dependent". Masoara: Kernel SHAP presupune independenta trasaturilor si **poate da
explicatii foarte gresite, chiar si pe modele simple**, fiindca evalueaza predictii pe instante
nereprezentative. Propun estimari conditionale, prin gaussiana, copula gaussiana sau distributie
empirica.

**Se transfera integral, si l-am verificat pe datele noastre.** In `output/e_shap_multi.md`, aceleasi
trasaturi, acelasi model, doua importante:

```
                     zipf     nsub   length
permutare marginala  +0.7472  +0.0570  +0.0300
reantrenare fara ea  +0.2942  +0.0367  +0.0167
```

Permutarea da lui `zipf` de **2,5 ori** mai mult decat reantrenarea. Artefactul vechi de pe disc arata
acelasi tipar in cealalta directie, intre permutare si SHAP: `output/shap/feature_importance.txt` pune
`zipf` 0.4536 peste `embedding(768)` 0.1433 prin permutare, iar SHAP le **inverseaza**, 0.068 fata de
0.182.

**Consecinta practica pentru raport:** nicio afirmatie de forma "trasatura X conteaza de N ori mai mult
decat Y" nu se scrie pe baza unei singure importante. Se raporteaza amandoua, iar cand difera, aia e
observatia.

**Nota de implementare:** `shap` nu e instalat in `envs/ml_def` si nu s-a instalat pentru o figura.
Alternativa folosita, reantrenarea fara coloana, e chiar cea recomandata de Hooker si colegii, deci nu
e un substitut mai slab, ci raspunsul lor la aceeasi intrebare.

---

## 5. Reducere de dimensiune pentru inspectie

**Chari si Pachter, PLOS Computational Biology 2023**, "The specious art of single-cell genomics".
Argumenteaza ca embeddingurile 2D t-SNE si UMAP nu reprezinta fidel spatiul de mare dimensiune si au
forme arbitrare. Demonstratia: construiesc **Picasso**, un autoencoder care transforma aceleasi date
intr-o forma 2D **prestabilita arbitrar**, de pilda un elefant, pastrand aparenta de structura.

**Lause, Berens si Kobak, PLOS Computational Biology 2024**, "The art of seeing the elephant in the
room", e replica: embeddingurile chiar nu pastreaza distantele de mare dimensiune, dar pot totusi
transmite informatie relevanta.

**Ce se transfera.** Concluzia comuna a celor doua lucrari, si e singura pe care o folosim: **din t-SNE
sau UMAP nu se poate citi o cantitate**, nici distanta, nici densitate, nici marimea unui grup. Se
poate cel mult ilustra o concluzie obtinuta numeric in alta parte.

**Ce am facut cu asta.** Criteriul a fost scris inainte: graficele se fac numai daca pasul numeric iese
pozitiv. A iesit negativ, corelatia partiala a predictorului de reziduu e **-0.0121** fata de pragul
0.1077, deci **graficele nu s-au facut**, si asta e decizia, nu o omisiune.

---

## 6. Diversitatea in ansambluri

**Kuncheva si Whitaker, Machine Learning 2003, 51:181-207**, "Measures of diversity in classifier
ensembles and their relationship with the ensemble accuracy". Masoara **zece masuri de diversitate** si
legatura lor cu acuratetea ansamblului. Rezultat: **nu apare nicio legatura proeminenta**, iar
diversitatea singura e un predictor slab al acuratetii ansamblului. Autorii isi exprima indoiala fata
de utilitatea masurilor de diversitate in construirea ansamblurilor reale.

**Wood, Mu, Webb, Reeve, Lujan si Brown, JMLR 2023, 24(359)**, "A Unified Theory of Diversity in
Ensemble Learning". Demonstreaza o familie de **descompuneri EXACTE bias-varianta-diversitate** pentru
o gama larga de functii de pierdere, patratica, entropie incrucisata, Poisson. Diversitatea e o
dimensiune ascunsa a descompunerii bias-varianta, o masura de potrivire in acelasi sens ca bias-ul si
varianta, dar care tine cont de dependentele statistice dintre membri.

**Ce se transfera, si confirma ce facem deja.** Pentru pierdere patratica si membri standardizati,
descompunerea exacta e chiar frontiera pe care o folosim ca poarta,
`r_ens = (suma r_i) / sqrt(n + 2*suma rho_ij)`, verificata la 1.11e-16 pe fiecare limba in
`e_frontiera_enc.md`. Deci nu inventam o unealta, folosim forma particulara a unui rezultat publicat.

**Ce nu se transfera.** Avertismentul lui Kuncheva si Whitaker priveste masurile de diversitate
NEPERECHE si sarcini de clasificare, unde legatura chiar e slaba. La regresie cu pierdere patratica
legatura nu e slaba, e o identitate. Deci "diversitatea nu prezice castigul" e adevarat la ei si fals
la noi, si distinctia e in functia de pierdere.

---

## 7. Incertitudine si OOD ca semnal

**Lakshminarayanan, Pritzel si Blundell, NeurIPS 2017**, "Simple and Scalable Predictive Uncertainty
Estimation Using Deep Ensembles". **Ovadia si colegii, NeurIPS 2019**, "Can you trust your model's
uncertainty? Evaluating predictive uncertainty under dataset shift": benchmark la scara mare al
metodelor de estimare a incertitudinii sub deplasare de distributie; **calibrarea post-hoc traditionala
nu tine** sub deplasare, si nici cateva alte metode anterioare.

**Ce nu se transfera, si e o distinctie masurata la noi, nu importata.** Toata literatura asta trateaza
incertitudinea ca pe o cantitate care spune **cat sa te increzi** intr-o predictie, deci ca pe o
PONDERE. La noi ponderea per item e inchisa cu cifre: `fuse_ab --h entropie/dezacord/zgomot` alege
`a = 0` pe **10 limbi din 10**, si la semnal real, si pe cinci seminte de zgomot. Ca semnal ADITIV,
adica al treilea termen in amestec, e alt obiect si trece prin frontiera ca oricare altul.

---

## 8. Ce spune literatura, pusa cap la cap, despre intrebarea sesiunii

Trei lucruri, in ordinea utilitatii:

1. **Frecventa si surprisal-ul sunt substituibile** (Oh si Schuler 2025). Sistemul nostru are deja
   frecventa si se sprijina pe ea puternic. Deci surprisal-ul nu avea de unde sa aduca, si asta era
   prezis de literatura inainte de a masura noi ceva.
2. **Diversitatea contextuala** e singurul candidat lexical din literatura cu dovada ca subsumeaza
   frecventa (Adelman si colegii 2006), si e si singurul care ar putea servi coada. Costa ~3 ore.
3. **Normele psiholingvistice nu servesc coada.** Sunt engleze sau minuscule, si acopera capatul usor
   al scarii. Nu sunt o parghie pentru sinhaleza si filipineza.

Si un al patrulea, care nu e despre semnal ci despre metoda: **atribuirea prin permutare pe trasaturi
corelate supraestimeaza**, verificat pe datele noastre cu un factor de 2,5 pe `zipf`. Orice propozitie
din paper despre importanta trasaturilor trebuie sa poarte amandoua cifrele.
