# Ce se stie despre scoaterea de reprezentari la nivel de token dintr-un encoder inghetat

Sinteza de literatura pentru sesiunea de research pe semnalul A. Intrebarea generala: cand ai un
encoder INGHETAT si vrei un vector pentru UN cuvant tinta dintr-o propozitie, pe care apoi il dai unui
regresor, ce s-a publicat despre cum se scoate acel vector.

Fiecare tema are trei parti: ce s-a masurat, cu cifre; pe ce sarcina; si **verdictul de transfer**,
adica daca se aplica la cazul nostru si de ce. Ultima parte e cea care conteaza, fiindca aproape
nimic din literatura asta nu e facut pe regresie de complexitate lexicala multilingva zero-label.

Situatia noastra, ca reper permanent in text: XLM-R base inghetat, `hidden_states[-4:]` mediate,
pool `mean` peste subword-urile tintei, vector centrat pe media limbii, dat lui Ridge(alpha=300)
plus HistGradientBoosting, r = 0.6011 pe zece limbi.

---

## 1. Pooling peste subword-uri: conventia noastra e `mean`, si e a doua cea mai buna

**Referinta centrala: Acs, Kadar si Kornai, "Subword Pooling Makes a Difference", EACL 2021.**

E cel mai apropiat lucru de intrebarea noastra care exista in literatura. Compara NOUA strategii de
pooling: `first`, `last`, `last2` (concatenarea ultimelor doua), `f+l` (combinatie invatata a primului
cu ultimul), `sum`, `max`, `avg`, `attn` (atentie printr-un MLP peste subword-uri) si `LSTM`
(bidirectional peste vectorii de subword). Doua modele, mBERT si XLM-R. Noua limbi tipologic diverse:
araba, chineza, ceha, engleza, finlandeza, franceza, germana, japoneza, coreeana. Trei sarcini:
probing morfologic, POS si NER.

Rezultatul care ne priveste, si e mare, nu marginal. Pe probing morfologic, la stratul 6:

```
sarcina                model     first   last    attn    LSTM
Finlandeza, Case-Noun  mBERT     33.0    90.7    93.9    92.0
Finlandeza, Case-Noun  XLM-R     49.6    94.4    96.0    95.4
Ceha, Gender-Adj       mBERT     41.5    77.1    75.6     --
Ceha, Gender-Adj       XLM-R     41.6    73.5    73.0     --
Engleza, Verbform-Verb mBERT     83.7    91.2    90.7     --
Engleza, Verbform-Verb XLM-R     82.7    91.0    91.3     --
```

Concluzia lor, textual: pentru sarcini morfologice **"alege primul subword", conventia cea mai
raspandita, e cea mai PROASTA strategie**, iar cea mai buna e atentia peste subword-uri. Pe finlandeza
diferenta intre `first` si `last` e de 45 de puncte procentuale la XLM-R. Motivul e transparent:
morfologia flexionara sta in SUFIX, iar `first` arunca exact sufixul.

Ei mai raporteaza si ca decalajul `first` fata de `last` e **mai mare in straturile de jos decat in
cele de sus**, si ca aleg stratul 6 pentru morfologie si POS.

**Verdict de transfer: se transfera, si e prima predictie pre-inregistrata a sesiunii.** Sarcina lor e
un clasificator antrenat peste trasaturi INGHETATE, exact arhitectura noastra. Complexitatea lexicala
e in buna masura o proprietate morfologica: sufixele latinate sunt deja o trasatura in
`solution_bert.LATINATE_SUFFIXES`, iar contributia #3 a lucrarii masoara chiar ca fixul de lema
scaleaza cu bogatia morfologica. Deci prezicem: **`last` bate `first`, si `mean` sta intre ele.**

**Ce nu se transfera:** castigatorii lor, `attn` si `LSTM`, au parametri INVATATI. Ca sa-i antrenam
ne-ar trebui etichete, si atunci am pierde proprietatea zero-label care e jumatate din contributia
lucrarii. Deci plafonul lor nu e plafonul nostru: noi ne oprim la strategiile fara parametri.

**A doua limita:** tintele noastre au putine subword-uri. Media fertilitatii pe test e 2.45, deci
diferenta intre `first`, `last`, `mean` si `max` se joaca de obicei intre doua-trei vectori, nu intre
zece. Efectul de 45 de puncte de pe finlandeza nu are cum sa se reproduca la scara asta.

---

## 2. Alegerea stratului: `last4` e mostenit, iar literatura arata spre mijloc

**Referinte: Jalili Sabet et al., "SimAlign", Findings EMNLP 2020; Dou si Neubig, "awesome-align",
EACL 2021; Acs et al. 2021 pentru partea morfologica.**

Calitatea alinierii cuvintelor intre limbi, folosind stari ascunse dintr-un singur strat, are o
**forma de parabola peste straturi**: creste, atinge maximul pe la stratul 8 din 12, apoi scade.
Explicatia data acolo, si e mecanica: in straturile de jos contextualizarea e prea slaba, in cele de
sus reprezentarile sunt prea specializate pe sarcina de preantrenare, adica pe MLM. SimAlign fixeaza
stratul 8 din exact acest motiv. Acs et al. ajung independent la stratul 6 pentru morfologie si POS.

Deci doua linii de cercetare diferite, pe sarcini diferite, converg pe **straturile de mijloc**, iar
noi folosim media ultimelor patru, adica 9-12.

**Verdict de transfer: partial, si trebuie spus de ce nu complet.** Aia e aliniere INTRE limbi, adica
o proprietate a spatiului comun. Noi nu aliniem nimic: pentru fiecare limba se potriveste un regresor
propriu, iar embeddingul e centrat pe media limbii inainte de a intra in el, ceea ce scoate deja o
parte din componenta specifica limbii. Cu alte cuvinte, o parte din problema pe care straturile de
mijloc o rezolva acolo, noi o rezolvam deja altfel.

**Contra-argument in favoarea straturilor de sus, si e specific sarcinii noastre:** complexitatea
lexicala coreleaza puternic cu frecventa, iar frecventa e exact ce codeaza capul de MLM. Straturile de
sus sunt "prea specializate pe MLM" pentru aliniere, dar pentru noi specializarea pe MLM ar putea fi
un avantaj, nu un defect. Predictia e deci ambigua, si de aia se masoara.

**Ce nu s-a facut nicaieri si nici noi n-am facut:** `last4` a fost ales pe un model de 12 straturi si
folosit apoi si pe `xlmr-large`, care are 24. Comentariul din `solution_bert.py` recunoaste explicit
ca `mid`, care numeste straturile 6-9 absolut, nu inseamna acelasi lucru pe 24 de straturi.

---

## 3. Anizotropie, dimensiuni scapate, whitening: cea mai mare parte NU se transfera

**Referinte: Ethayarajh, EMNLP 2019; Timkey si van Schijndel, EMNLP 2021; Libovicky, Rosa si Fraser,
Findings EMNLP 2020; Haemmerl et al., Findings ACL 2023.**

Ce s-a masurat:

- **Ethayarajh 2019**: reprezentarile contextuale **nu sunt izotrope in niciun strat** al lui ELMo,
  BERT sau GPT-2. Straturile de sus au auto-similaritate mult mai mica pentru acelasi cuvant in
  contexte diferite. Si cifra care ne intereseaza cel mai mult: **sub 5% din varianta reprezentarilor
  contextuale ale unui cuvant se explica printr-un embedding static**, si asta in toate straturile.
- **Timkey si van Schijndel 2021**: cateva dimensiuni "scapate" (rogue) domina similaritatea cosinus
  si ascund calitatea reprezentarii; directiile dominante corespund unor lucruri neinteresante,
  frecventa tokenului de exemplu, nu continutului semantic. Reparatia lor: standardizarea
  dimensiunilor.
- **Libovicky et al. 2020**: propun doua metode pentru a face reprezentarile multilingve neutre la
  limba. Prima e **centrarea nesupravegheata pe media fiecarei limbi**. A doua e o proiectie potrivita
  pe date paralele mici. Sarcinile: identificarea limbii, alinierea cuvintelor in propozitii paralele.
  Verdictul lor de baza: reprezentarile sunt "doar moderat neutre la limba" implicit.

**Verdictul de transfer, si asta e cel mai important "nu" din toata fisa.** Aproape toata literatura de
anizotropie masoara efecte pe **similaritate cosinus**. Noi nu folosim cosinus nicaieri. Vectorul intra
ca 768 de coloane brute intr-un Ridge si intr-un HGB. O dimensiune care domina cosinusul nu domina
automat o regresie penalizata: Ridge o poate ignora, iar HGB, care taie pe axe, o foloseste doar daca
prezice. Deci cifrele lor nu se pot importa, si nici concluzia "whitening ajuta" nu se poate importa.

**Ce se transfera totusi, si e o observatie utila pentru paper:** metoda 1 din Libovicky et al., adica
centrarea pe media limbii, **e exact ce face deja `solution_bert._Xc` si `_center_per_lang`**. Am
implementat o metoda publicata fara s-o citam. Asta merita o propozitie in Related Work, fiindca da
un precedent pentru o alegere care acum arata ca o decizie ad-hoc.

**Ce ramane netestat, si de aia intra in plan:** decorelarea propriu-zisa, adica whitening-ul, plus
scoaterea primelor componente principale. Argumentul a priori de ce ar putea conta la NOI, desi
literatura de cosinus nu se aplica: Ridge cu alpha = 300 penalizeaza coeficientii **in baza data**,
deci o rotatie a bazei schimba estimatorul; iar HGB taie pe axe, deci o rotatie il schimba si mai
mult. Semnul efectului e necunoscut inainte de masuratoare, si asta se scrie ca atare.

---

## 4. Contextual fata de static: de ce un vector de TIP e candidatul cel mai decorelat

**Referinte: Ethayarajh, EMNLP 2019; Bommasani, Davis si Cardie, ACL 2020.**

Bommasani et al. construiesc embeddinguri STATICE pornind de la unele contextuale, prin agregare peste
multe contexte, si arata ca **agregarea peste multe contexte imbunatateste semnificativ calitatea
reprezentarii** la evaluare intrinseca. Ethayarajh da cealalta jumatate: sub 5% din varianta unui
vector contextual e explicata de unul static.

**Verdict de transfer: se transfera, dar altfel decat pare.** Nu ne intereseaza sa construim
embeddinguri statice mai bune. Ne intereseaza cifra lui Ethayarajh ca **argument de DECORELARE**: daca
un vector static explica sub 5% din varianta celui contextual, atunci un brat construit pe vectorul
cuvantului IZOLAT e structural diferit de bratul contextual, deci e candidatul cu cea mai mica
corelatie asteptata dintre toate cele disponibile la cost mic.

Si exista un argument de sarcina in plus: complexitatea lexicala e in mare masura o proprietate de
TIP, nu de instanta. Un cuvant rar e greu in aproape orice propozitie. Deci un vector de tip nu e
neaparat slab pe sarcina asta, spre deosebire de dezambiguizare, unde ar fi inutil.

**Ce nu se transfera:** cifra de sub 5% e masurata pe engleza, pe ELMo, BERT si GPT-2, nu pe XLM-R
multilingv, si nu spune nimic despre corelatia dintre PREDICTIILE a doua modele de regresie construite
pe cele doua reprezentari. Corelatia dintre predictii poate fi mult mai mare decat cea dintre
reprezentari, fiindca amandoua sunt fortate spre aceeasi eticheta. Deci ramane o ipoteza de masurat,
nu o predictie tare.

---

## 5. Prefixele modelelor contrastive: cifra lui e5 din raportul nostru e o margine inferioara

**Referinta: Wang, Yang, Huang, Yang, Majumder si Wei, "Multilingual E5 Text Embeddings", raport
tehnic 2024.**

Modelele E5 sunt antrenate cu prefixele `query: ` si `passage: ` in fata textului. Documentatia lor
spune direct doua lucruri: prefixele sunt folosite la antrenare si **absenta lor degradeaza
performanta**; iar pentru sarcini SIMETRICE, adica similaritate semantica, bitext mining, cautare de
parafraze, se foloseste `query: ` pe amandoua partile. `multilingual-e5-large` e initializat din
XLM-R large, 24 de straturi, 1024 de dimensiuni; noi folosim varianta base.

**Verdict de transfer: partial, si in directia care ne convine sa stim.** Recomandarea lor e despre
**embeddingul de propozitie**, adica despre vectorul agregat care iese la capat si care e antrenat
contrastiv cu prefixul prezent. Noi luam stari ascunse **per token** dintr-un context brut, deci nu
folosim obiectul pe care l-au optimizat ei. Efectul asteptat e prin urmare atenuat, nu absent:
prefixul schimba tot ce vede modelul, deci schimba si starile per token.

Consecinta practica, si e o corectie de onestitate in raportul nostru: `output/e_encoder.md` declara
deja ca e5 a fost evaluat fara prefix, deci **cifra lui de -0.0027 fata de base e o margine
inferioara**, nu evaluarea lui in conditii proprii. Costul de a repara asta e o rulare de zece minute.

**Capcana tehnica de care literatura nu te avertizeaza:** prefixul se pune in fata textului, deci MUTA
toate offset-urile de caractere. Codul nostru selecteaza subword-urile tintei prin suprapunere de
offset-uri. Daca prefixul se adauga fara sa se deplaseze span-ul cu lungimea lui, se citesc alte
subword-uri si **nimic nu crapa**, iese doar o cifra proasta care s-ar interpreta gresit ca "prefixul
nu ajuta".

---

## 6. Limbi cu resurse putine: modele pe octeti, vocabulare extinse, modele monolingve

**Referinte: Imani et al., "Glot500", ACL 2023; Limisiewicz et al., "MYTE", 2024; Clark et al.,
"CANINE", TACL 2022; Xue et al., "ByT5", TACL 2022; Dhananjaya et al., "BERTifying Sinhala",
LREC 2022; Cruz si Cheng, pentru tagalog.**

Trei familii de solutii, cu costuri foarte diferite:

**(a) Vocabular extins prin preantrenare continuata.** Glot500-m acopera 511 limbi predominant cu
resurse putine, e construit pe XLM-R si are ~0.4 miliarde de parametri, dintre care majoritatea in
matricea de embedding din cauza vocabularului marit. Raporteaza imbunatatiri fata de XLM-R base atat
pe limbile de "cap" cat si pe cele de "coada", si bate XLM-R large pe cele de coada. Concluzia lor
metodologica merita citata: niciun factor singur nu explica calitatea reprezentarilor, ci combinatia
dintre marimea corpusului, scriere, ajutorul limbilor inrudite si capacitatea totala a modelului.

**(b) Modele fara tokenizare, pe caractere sau octeti.** CANINE lucreaza pe caractere cu downsampling;
ByT5 pe octeti UTF-8 direct, si e raportat ca deosebit de potrivit pentru limbi cu resurse putine si
bogate morfologic, unde tokenizarea pe subcuvinte fragmenteaza excesiv. MYTE inlocuieste conventia pe
caractere a UTF-8 cu **coduri de octeti pe morfeme**, invatate cu Morfessor 2.0, si obtine encodari
mai scurte pentru toate cele 99 de limbi testate, cu castiguri de la 1% pe vietnameza si chineza pana
la aproape 70% pe birmana; paritatea de tokenizare in cazul cel mai rau fata de engleza scade de la
3.5 la 1.7.

**(c) Modele monolingve.** SinBERT are doua variante, small cu 6 straturi si large cu 12, e bazat pe
RoBERTa si e raportat mult superior modelelor existente pentru sinhaleza. Pentru tagalog, Cruz si
Cheng preantreneaza modele in stil BERT si RoBERTa pe WikiTextTL-39, cu un castig mediu de 4.47 puncte
de acuratete pe trei sarcini de clasificare.

**Verdict de transfer, si aici e cel mai instructiv contra-exemplu din toata fisa.** Acelasi studiu pe
sinhaleza, BERTifying Sinhala, raporteaza ca **dintre modelele multilingve care includ sinhaleza
(XLM-R, LaBSE, LASER), XLM-R e de departe cel mai bun**. Masuratoarea noastra spune exact invers: pe
sinhaleza LaBSE da +0.3580 fata de +0.2586 al lui XLM-R base, adica **+0.0994, cu interval care
exclude zero**, cel mai mare efect de encoder din tot experimentul.

Nu e o contradictie, e o diferenta de sarcina, si trebuie scrisa asa: ei clasifica TEXTE, la nivel de
propozitie sau document, folosind embeddingul agregat, pe care LaBSE il optimizeaza pentru
similaritate de traducere, nu pentru discriminarea continutului intr-o singura limba. Noi facem
regresie pe UN TOKEN, folosind stari ascunse per pozitie. Un model bun la primul lucru nu e neaparat
bun la al doilea, si invers. **Concluzia utila: "cel mai bun model pentru limba X" nu e o proprietate
transferabila intre nivelul de propozitie si cel de token, si orice alegere de encoder facuta pe
literatura, nu pe masuratoare proprie, e o alegere pe sarcina altcuiva.**

**Ce nu se transfera din (b), si e o limita de cost, nu de principiu:** CANINE, ByT5 si MYTE sunt
arhitecturi diferite, nu greutati de pus intr-un `AutoModel` existent. ByT5 e encoder-decoder, deci
"stari ascunse pentru subword-urile tintei" nici nu e definit la fel. Costul de integrare depaseste
bugetul unei sesiuni, deci raman ca directie declarata, nu ca experiment.

---

## 7. Context: ce s-a folosit efectiv la complexitate lexicala

**Referinta: Shardlow et al., "SemEval-2021 Task 1: Lexical Complexity Prediction".**

Sistemele de sus au combinat trasaturi construite de mana cu reprezentari din transformere si un
regresor cu gradient boosting. PolyU CBS-Comp raporteaza 0.754 corelatie pe subtask 1, cuvinte
singure, dintr-o combinatie de trasaturi lexicale, sintactice, embeddinguri de cuvinte si trasaturi
derivate din transformere, cu Gradient Boosting Regressor. IITK foloseste ansambluri de arbori cu
gradient boosting peste un set eterogen: trasaturi lingvistice, embeddinguri statice si contextuale,
lexicoane de norme psiholingvistice, WordNet, frecvente de bigrame de cuvinte si de caractere.

**Verdict de transfer: arhitectura noastra e in familia castigatoare, cifra lor nu e comparabila.**
Combinatia "trasaturi lexicale plus embedding contextual plus gradient boosting" e exact ce face
`blend_ridge_hgb`, deci nu inventam o arhitectura ciudata. Dar 0.754 e pe engleza monolingva, cu
antrenare supravegheata pe date din aceeasi distributie. Noi suntem multilingv si zero-label pe noua
limbi din zece. Cifrele nu se pun una langa alta, si reperele corecte raman cele din
`output/repere_publicate.md`.

---

## Consolidat: ce NU se transfera, si de ce

```
ce                                    de ce nu se transfera
--------------------------------      ---------------------------------------------------------
cifrele de anizotropie / whitening    sunt masurate pe similaritate COSINUS; noi dam dimensiunile
                                      brute lui Ridge + HGB si nu calculam cosinus nicaieri
castigatorii din poolingul de         `attn` si `LSTM` au parametri INVATATI; ne-ar trebui etichete
subword-uri                           si am pierde proprietatea zero-label
marimea efectului de pooling          tintele lor au multe subword-uri; ale noastre au 2.45 in medie,
                                      deci first/last/mean/max difera intre 2-3 vectori, nu 10
stratul 8 din alinierea de cuvinte    aia e aliniere INTRE limbi; noi potrivim un regresor per limba
                                      si centram deja pe media limbii, deci rezolvam altfel o parte
                                      din aceeasi problema
"XLM-R e cel mai bun pe sinhaleza"    e masurat pe clasificare de TEXT cu embedding agregat; noi
                                      facem regresie pe UN TOKEN, si masuram inversul (LaBSE +0.0994)
recomandarea de prefix a lui E5       e despre embeddingul de PROPOZITIE antrenat contrastiv; noi
                                      luam stari per token dintr-un context brut
CANINE / ByT5 / MYTE                  arhitecturi diferite, nu greutati de pus intr-un AutoModel;
                                      la ByT5 "stari pentru subword-urile tintei" nici nu e definit
0.754 de la SemEval-2021              engleza monolingva, supravegheat, aceeasi distributie
```

## Ce prezice literatura pentru sweep-ul nostru, scris INAINTE de rezultate

1. **`last` bate `first`.** Acs et al. masoara pana la 45 de puncte diferenta pe finlandeza. La noi
   efectul va fi mult mai mic, fiindca tintele au 2.45 subword-uri in medie, dar semnul ar trebui sa
   fie acelasi.
2. **`mean` sta intre `first` si `last`,** fiindca le mediaza literalmente.
3. **Efectul de pooling e mai mare pe limbile cu fertilitate mare**, adica pe si si ja, si aproape nul
   pe engleza, unde majoritatea tintelor sunt un singur subword.
4. **Straturile de mijloc fata de `last4`: ambiguu.** Doua linii de cercetare arata spre mijloc pentru
   aliniere si morfologie; frecventa, care e cel mai bun predictor unic al complexitatii, sta mai
   degraba sus, langa capul de MLM.
5. **`isoonly` are cea mai mica corelatie asteptata** cu bratele contextuale dintre toti candidatii
   ieftini, pe argumentul lui Ethayarajh.
6. **Glot500-m e singurul candidat de al patrulea membru cu sansa reala** de corelatie sub prag, si
   anume prin si si fil, unde vocabularul lui extins chiar tokenizeaza altfel.

## Referinte

- Acs, Kadar, Kornai. Subword Pooling Makes a Difference. EACL 2021. https://aclanthology.org/2021.eacl-main.194/
- Jalili Sabet, Dufter, Yvon, Schutze. SimAlign. Findings of EMNLP 2020. https://arxiv.org/abs/2004.08728
- Dou, Neubig. Word Alignment by Fine-tuning Embeddings on Parallel Corpora. EACL 2021.
- Ethayarajh. How Contextual are Contextualized Word Representations? EMNLP 2019. https://aclanthology.org/D19-1006/
- Timkey, van Schijndel. All Bark and No Bite: Rogue Dimensions. EMNLP 2021. https://aclanthology.org/2021.emnlp-main.372/
- Libovicky, Rosa, Fraser. On the Language Neutrality of Pre-trained Multilingual Representations. Findings of EMNLP 2020. https://aclanthology.org/2020.findings-emnlp.150/
- Bommasani, Davis, Cardie. Interpreting Pretrained Contextualized Representations via Reductions to Static Embeddings. ACL 2020. https://aclanthology.org/2020.acl-main.431/
- Wang et al. Multilingual E5 Text Embeddings: A Technical Report. 2024. https://arxiv.org/abs/2402.05672
- Imani et al. Glot500: Scaling Multilingual Corpora and Language Models to 500 Languages. ACL 2023. https://aclanthology.org/2023.acl-long.61/
- Limisiewicz et al. MYTE: Morphology-Driven Byte Encoding. 2024. https://arxiv.org/abs/2403.10691
- Clark et al. CANINE. TACL 2022. Xue et al. ByT5. TACL 2022.
- Dhananjaya et al. BERTifying Sinhala. LREC 2022. https://aclanthology.org/2022.lrec-1.803/
- Cruz, Cheng. Pre-trained Language Models for Tagalog with Multi-source Data.
- Shardlow et al. SemEval-2021 Task 1: Lexical Complexity Prediction. https://aclanthology.org/2021.semeval-1.1/
