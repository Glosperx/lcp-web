---
name: paper-extensie-multilingva-arr-octombrie
description: "După MRL, lucrarea se extinde la 11 limbi și merge la ARR pe 12 oct 2026; spina e tabelul de resurse per limbă cerut de Sergiu, nu numărul de limbi"
metadata: 
  node_type: memory
  type: project
  originSessionId: fd12ce6d-c09f-491d-ae40-a457aff2155d
  modified: 2026-08-17T11:53:29.620Z
---

Decis pe **8 august 2026**, cu Alexandru, după discuția cu Sergiu din aceeași zi. Planul complet:
`~/.claude/plans/crezi-ca-am-putea-bubbly-boot.md`.

Întrebarea „ce urmează după MRL", amânată deliberat în [[paper-target-mrl-emnlp-2026]], are acum
răspuns.

## Calendarul, verificat pe aclrollingreview.org/dates

| Etapă | Data |
|---|---|
| Submisie ARR, ciclul octombrie | **12 oct 2026** |
| Commitment NAACL 2027 / COLING 2027 | 20 dec 2026 |
| Commitment ACL 2027 | ianuarie 2027 |

**ARR nu e conferință, n-are rank** — e platforma de recenzare, venue-ul se alege după recenzii.
CORE 2023: ACL, EMNLP, NAACL = **A\***; COLING = **B** (era A în CORE 2018, downgrade contestat de
comunitate ca bazat pe date insuficiente). MRL e workshop, fără rank.

**COLING 2027** (ediția 32, Macau, 9–14 mai 2027). Submisie tot prin ARR (nu acceptă direct),
commitment 23 dec 2026, notificare 10 feb 2027, long 8p / short 4p.

**CORECȚIE 16 august 2026: COLING 2027 NU are temă specială pe diversitate lingvistică.** Formularea
citată mai jos, „uses of NLP/LLMs in service of linguistic research, with a particular focus on
linguistic diversity", **nu se regăsește** în textul publicat. CFP-ul de pe
[2027.coling-iccl.org](https://2027.coling-iccl.org/) și de pe portalul ACL e generic: „long and
short papers featuring substantial, original, and unpublished research in all aspects of
computational linguistics and natural language processing". Pagina se autodescrie ca preliminară,
deci o temă poate apărea. Până apare, **COLING e o țintă obișnuită de rang B, nu una croită pe
lucrare**. Singura conferință din 2027 cu temă specială declarată e EACL 2027, „The Human in
Language", inaccesibilă (deadline ARR 3 august, trecut).

**A doua corecție: „commitment ACL în ianuarie 2027" e greșit.** Ianuarie 2027 e data de **submisie**
ARR finală pentru ACL 2027; celula de commitment e goală pe ARR și TBA pe site-ul ACL. Prin tiparul
celorlalte ar cădea prin martie 2027, dar e inferență.

**A treia, minoră:** ARR spune commitment NAACL/COLING pe **20 dec**, ambele CFP-uri de venue spun
**23 dec**. Surse în conflict; se planifică pe 20.

Capcana: commitment-ul NAACL/COLING (20 dec) vine **înaintea** celui pentru ACL (ianuarie), deci e
ori/ori. Meta-recenziile ciclului ies până pe 20 dec, deci decizia se ia cu scorurile pe masă.
Recenzii bune, aștepți ACL; recenzii de mijloc, iei NAACL.

EACL 2027 e închis definitiv: cerea submisie ARR pe 3 aug 2026.

## Ce face lucrarea

Nu „aceeași metodă pe mai multe limbi". Trei schimbări structurale:

1. **MLSP își schimbă rolul**, din sursă de antrenare în **și țintă de evaluare**, prin
   leave-one-language-out. Din 1 rezultat devin 11 (MLSP 10 + RoLCP). Fără flip-ul ăsta,
   adăugarea limbilor lipsă doar îngroașă setul de antrenare.
2. `solution_bert.py:56` filtrează acum doar romanicele (fr/it/pt/es/ca). **Se folosesc 5 din 10
   limbi MLSP.** Se scoate filtrul.
3. **Cererea lui Sergiu — tabel cu ce e disponibil pentru fiecare limbă — e spina lucrării, nu
   anexa.** „Unele au modele monolingve, pentru altele putem folosi doar XLM-R." Din tabel ies trei
   paliere: complet (ro, en, de, es, fr, it, pt, ca), altă scriere (ja), doar XLM-R (si, fil).
   Designul care rezultă: config (i) universal XLM-R + LM multilingv pe toate 11, config (ii)
   monolingv unde există, iar **Δ(ii − i) = cât valorează un model monolingv** în setare fără
   etichete în limba țintă. Cifră nemăsurată curat nicăieri.

Teza a doua: **câștigul fix-ului de lemă scalează cu bogăția morfologică** (la RO e +4.09, cel mai
mare câștig unic). Se măsoară pe UD, trebuie să iasă un număr, nu un tabel.

## Eye-tracking: demotat, decis de Sergiu

„Oricum nu eye tracking pare că contează cel mai mult." Corect și pe cifre: contribuția marginală
a lui D e **+0.84 din 69.74**, ~1%. **D nu intră în grila multilingvă**, rămâne studiu de caz RO.

Motivul tehnic, nu doar cel de prioritate: shared task-ul RO a distribuit gaze peste **aceleași
texte** din care vin cuvintele-țintă. MECO/GECO/ZuCo/EMTeC/MultiplEYE au gaze peste textele lor,
deci n-ai lookup pentru cuvintele MLSP. MultiplEYE acoperă 8 din cele 11 limbi și ar merge printr-un
lexicon de gaze la nivel de tip, cu gate pe acoperire — dar nu în ciclul ăsta. **Un predictor de
gaze nu e punte validă**: partea predictibilă din trăsături lexicale e exact partea redundantă cu
semnalele A și C, dovedită de **§4.3** al lucrării curente (măsurile timpurii rețin r̄ = 0.010 după
partializare, cele târzii 0.243). **Corectat pe 15 august 2026:** numărul scris inițial aici, §4.4,
era greșit. Verificat direct în `Paper/documentation_overleaf.tex`: Results e §4 (linia 968), iar
„Eye-tracking contributes through its late measures" e a treia subsecțiune (linia 1023).

**Why:** decizia de venue fixează deadline-ul, iar deadline-ul (9 săptămâni, din care primele două
se duc pe MRL) e ce face diferența între extensie reală și reformatare. Iar reîncadrarea cerută de
Sergiu schimbă ce se măsoară, nu doar cum se prezintă.

**How to apply:** săptămâna 1 e verificarea tabelului de resurse — `wordfreq` nu e instalat pe
niciuna din mașini, deci coloana de frecvențe e nescrisă, iar si/fil sunt sub semnul întrebării.
Vezi [[paper-target-mrl-emnlp-2026]], [[rals-rolcp-datele-sunt-ale-lui-nisioi]],
[[preferinte-de-scriitura-paper]].

## ACTUALIZARE 15 august 2026: nu s-a trimis nimic la MRL

Deadline-ul din 10 august a trecut **fără submisie**, nici lucrarea completă, nici abstractul
non-arhival din varianta (1). Nu există `abstract_mrl.tex`. Confirmat de Alexandru.

Ce se schimbă: nu există publicație anterioară, deci **regula ARR de suprapunere nu se aplică** și
dispare vectorul de desk rejection care motiva toată discuția arhival/non-arhival de mai sus.
Dispare și prezentarea de la Budapesta. Rămân ~8 săptămâni curate până pe 12 octombrie. Toată
secțiunea „Decizia MRL" din planul `crezi-ca-am-putea-bubbly-boot.md` e istorie, nu constrângere.

**Româna rămâne strict zero-label** în grila multilingvă, decis de Alexandru în aceeași zi: e limba
ținută deoparte în leave-one-language-out, exact ca acum, iar RoLCP intră cel mult ca ablație
separată.

Restul stării verificate pe 15 august e în [[lolo-exista-deja-in-cod]] și [[hardware-doua-masini]],
plus documentul de handoff `~/.claude/plans/e-ti-pe-proiectul-din-breezy-cocoa.md`, care conține și
promptul rescris pentru sesiunea de fezabilitate. **Research-ul extern (MLSP, resurse per limbă, UD,
eye-tracking, venue-uri) rămâne integral nefăcut.**

---

## ACTUALIZARE 16 august 2026: research-ul e terminat, iar planul lucrării e scris

Planul complet: `~/.claude/plans/cite-te-claude-plans-cite-te-claude-plan-eager-pine.md`, aprobat de
Alexandru. Raportul de fezabilitate care îl precedă:
`~/.claude/plans/cite-te-claude-plans-e-ti-pe-proiectul-d-delegated-glade.md`.

### Cele trei decizii luate de Alexandru

1. **Revendicarea centrală e protocolul leave-one-language-out, iar Δ e contribuția secundară.**
   Motivul e în [[noutate-si-precedente-lcp-multilingv]]: nimeni n-a rulat LOLO pe MLSP, în timp ce
   mecanismul semnalului B are precedent și Δ are unul apropiat. Dacă Δ iese zero, lucrarea nu moare.
2. **Δ se raportează în două forme:** controlat pe ro/ja/pt, care au aceeași bază Llama-3.1-8B, și
   larg pe 9 limbi cu Qwen3-8B ca referință. Vezi [[brate-llm-per-limba]].
3. **Se scrie o lucrare nouă, care o absoarbe pe cea românească.** Româna devine una din limbile de
   evaluare plus studiu de caz. Lucrarea românească nu se mai trimite separat.

### Ce s-a schimbat față de designul din 8 august, descris mai sus

- **Palierele de resurse din punctul 3 de mai sus sunt parțial infirmate.** Catalana **nu** e o limbă
  cu resurse puține: are cele mai bune cifre de lematizare din tot setul. Filipineza a ieșit din
  categoria imposibil, are lematizator și acum și un treebank UD mare cu leme. **Sinhaleza e singura
  efectiv ruptă.**
- **Configurația (ii) nu e definibilă pentru semnalul A**, fiindcă un encoder monolingv trăiește în
  alt spațiu. Δ rămâne definibil doar pe semnalele B și C.
- **Teza morfologică are nume consacrat:** e **MSP, mean size of paradigm** (Xanthos și Gillis 2010),
  nu un indice propus de noi. Se calculează pe 9 limbi din 11, sinhaleza rămâne exclusă. Precedent
  defavorabil de citat noi primii: Cotterell et al. 2018 au găsit corelația, **Mielke et al. 2019 nu
  au reprodus-o** pe 69 de limbi. De asta teza morfologică e ultima care intră și prima la tăiere.
- **Se raportează r, nu compozitul** `50(|r| + max(0,R²))`, fiindcă mediile complexității variază de
  2,5 ori între limbi și R² devine neinterpretabil.
- **Trial-ul MLSP, 30 de instanțe per limbă, e un set de dezvoltare curat**, practic disjunct de test.
  Ponderile de fuziune se aleg pe trial-ul limbilor **rămase în antrenare**, deci slăbiciunea „cinci
  cantități alese pe scorul de evaluare" din Limitations **dispare**, și cu ea aproape o pagină.

### Eye-tracking: verdict definitiv, cu literatură

Secțiunea „Eye-tracking: demotat" de mai sus rămâne valabilă ca decizie, dar **argumentul din ea e
parțial greșit** și nu trebuie folosit ca atare. Barrett et al. 2016 arată că măsurile târzii
**supraviețuiesc** agregării pe tip, iar Juhasz și Rayner 2003 că vârsta de achiziție, proprietate de
tip, acționează în măsurile **timpurii**. Deci teza din §4.3 nu se poate reciti ca argument general
împotriva unui lexicon de tip.

Argumentul care ține e de ordin de mărime: puntea publicată dă +0.3 F1 in-domain și +2.7 cross-corpus
(Hollenstein și Zhang 2019) la 76% acoperire, în engleză. Plus: catalana și sinhaleza **nu au nicio
resursă ET**, iar pentru nicio limbă MLSP nu există gaze peste textele MultiLS. **D nu intră ca
semnal**, intră ca studiu de caz românesc plus un paragraf de Limitations.

**How to apply:** primul experiment e Δ_frozen pe 10 limbi cu bootstrap pe contexte, și e cel mai
devreme punct de moarte al lucrării, în săptămâna 2. Nimic scump nu se pornește înainte de a-l citi.
Ordinea de tăiere e decisă în plan și nu se improvizează în octombrie.

### Punct de reluare, la sfârșitul zilei de 16 august 2026

**Starea:** planul e aprobat, nu s-a scris nicio linie de cod și nu s-a pornit nicio rulare. Repo-ul e
neatins. Sesiunea următoare e de **execuție**, nu de research.

**Promptul pentru sesiunea următoare e scris**, în §4.2 al planului
`~/.claude/plans/cite-te-claude-plans-cite-te-claude-plan-eager-pine.md`. Se copiază de acolo.

**Șase verificări rămase**, în §4.1 al aceluiași plan. Patru cer un mediu care rulează, deci nu se pot
face prin research: compatibilitatea `transformers` 5.13.1 cu cod scris pe 4.46.3, comportamentul
`wordfreq` pe sinhaleză, debitul M5, și fertilitatea XLM-R măsurată. Două rămân research: închiderea
verificării de noutate, unde graful Semantic Scholar a eșuat, și lucrarea GMU
[2024.bea-1.57](https://aclanthology.org/2024.bea-1.57/), singurul precedent posibil rămas pentru
contribuția 2.

**Așteptarea de calibrat înainte de primul experiment:** bara nu mai e 0.487, e **0.657**. Vezi
[[noutate-si-precedente-lcp-multilingv]].

---

## ACTUALIZARE 16 august 2026, seara: venue-ul e fixat, iar prima rulare s-a făcut

### Venue: NAACL 2027, decis de Alexandru

Nu mai e ori/ori. Dilema descrisă mai sus, commitment NAACL pe 20 dec față de ACL în ianuarie, **e
închisă: se merge pe NAACL 2027**, CORE 2023 **A\***, la egalitate cu ACL și EMNLP.

| Etapă | Data |
|---|---|
| Submisie ARR, ciclul octombrie | **12 oct 2026** |
| Meta-recenzii | până pe 20 dec 2026 |
| **Commitment NAACL** | **20 dec 2026** pe ARR, 23 dec în CFP. Se planifică pe 20 |

Consecința: nu se mai așteaptă scorurile ca să se aleagă venue-ul. Datele și locația NAACL 2027 nu
sunt verificate.

### Planul de bake-off, aprobat

`~/.claude/plans/pai-si-cum-se-zazzy-shamir.md`. Alegerea modelului pentru semnalele B și C trece
dintr-o decizie luată pe hârtie într-una măsurată, în trei etape: **0** fertilitatea tokenizerelor,
gratuită și poartă; **1** bake-off pe cele **300 de instanțe de trial**, niciodată pe test; **2** doar
câștigătorii pe testul complet.

**Nu întârzie nimic:** E1 e brațul înghețat și nu depinde de niciun LLM, deci cel mai devreme punct de
moarte rămâne în săptămâna 2. Revendicarea centrală, C1-C4 și ordinea de tăiere sunt neschimbate.

**Două capcane metodologice de respectat.** Alegerea modelului se face **leave-one-language-out**, la
fel ca ponderile de fuziune, altfel se sparge proprietatea câștigată la V8 care face să dispară
`sec:tuning`. Și **performanța nu poate înlocui acoperirea**: brațul principal e o afirmație despre ce
poate revendica lucrarea, bake-off-ul măsoară doar cât costă alegerea aia.

### Etapa 0 e făcută, și a răsturnat alegerea modelului

Rulată pe 16 august. `measure_fertility.py`, rezultate în `output/fertility_by_lang.csv`. Verificarea
de sănătate trece: XLM-R pe română dă 1.948 față de 1.95 măsurat anterior.

**Qwen3-8B cade pe byte fallback pe sinhaleză deși o listează oficial.** Gemma 4 o tokenizează aproape
ca XLM-R deși nu publică nicio listă. Cifrele, diagnosticul și validarea metodei sunt în
[[fertilitate-tokenizere-masurata]]. Alegerea se mută spre **Gemma 4**, dar **nu e fixată**.

### Punct de reluare, sfârșitul zilei de 16 august

**Starea repo-ului:** un singur fișier nou, `measure_fertility.py`, plus `output/fertility_by_lang.csv`.
Nimic altceva modificat. **Reparațiile din §2.5 al planului precedent sunt încă nefăcute**, cu o
excepție parțială: funcția de mapare a limbii din coloana `language`, cu eroare la nemapare, e scrisă
în `measure_fertility.py` și trebuie factorizată de acolo în cele trei locuri divergente.

**Ce blochează:**

| Ce | Stare |
|---|---|
| `meta-llama/Llama-3.1-8B-Instruct` | acces **RESPINS** pe 16 aug, dar **nu mai blochează**: oglinzi negate cu greutăți identice, vezi [[brate-llm-per-limba]] |
| `CohereLabs/tiny-aya-global` | acces necerut, opțional |
| `aya-expanse-8b`, `EuroLLM-9B-Instruct` | **deblocate**, deja măsurate |

`wordfreq` și `stanza` lipsesc în continuare din `envs/ml_def`. `data/complex_en/` lipsește, iar
`finetune_xlmr.py:46` doar citește, nu descarcă.

**Următorul pas:** reparațiile din §2.5, pașii 0-4, apoi E1. Bake-off-ul pe trial vine în săptămâna 3.

**Lista de task-uri și promptul pentru sesiunea de execuție sunt scrise**, în
`~/.claude/plans/taskuri-executie-saptamana-1.md`. Partea I e lista pe blocuri, 0 descărcări, A
reparații, B verificări de mediu, C E1, D codul de bake-off, E bake-off, F secundar. Partea II e
promptul, de copiat ca atare. Conține și cele patru lucruri din 16 august care contrazic documentele
mai vechi, în frunte cu **brațul universal care nu mai e fixat pe Qwen3-8B**.

**How to apply:** nu fixa Gemma 4 ca braț principal înainte de etapa 1. Fertilitatea e screening, nu
test. Vezi [[fertilitate-tokenizere-masurata]], [[rute-rulare-logits]], [[brate-llm-per-limba]].

---

## ACTUALIZARE 17 august 2026: E1 a rulat, iar criteriul §5.2 a omorât contribuția C2

Sesiune de execuție. Bloc 0, Bloc A și E1 sunt **închise**. Detaliile în
`~/.claude/plans/taskuri-executie-saptamana-2.md`, care e acum documentul de reluare și înlocuiește
`taskuri-executie-saptamana-1-v2.md`. Rezultatul brut: `output/e1_lolo_frozen.csv`, verdictul complet
în `output/e1_verdict.md`.

### Ce s-a decis prin măsurătoare, nu prin discuție

**σ_Δ între cele 10 limbi = 0.0369**, față de 0.0107 estimat pe 3 limbi. Pragul §5.2 e 0.030, deci
**designul centrat pe Δ e mort**. Aplicat fără renegociere. Consecințe:

- **E3 și E4 nu se fac.** Cade **contribuția C2** din §3.1 al planului lucrării.
- **Cvartetul adaptat pe limbă nu se descarcă**, circa 80 GB: RoLlama3.1, Swallow v0.3, Gervásio. Deci
  și D.3, reparația numelui RoLlama3 în RoLlama3.1, își pierde probabil obiectul.
- **Bake-off-ul rămâne**, fiindcă cele 7 modele descărcate servesc brațul universal, adică semnalele B
  și C ale sistemului principal, nu Δ.

**Problema deschisă, de decis de Alexandru:** ordinea de tăiere din §3.5 a fost decisă presupunând că
C2 trăiește. Cu C2 moartă, greutatea cade pe C3, adică regresia lui r per limbă, care are n = 10 deci
putere mică prin construcție, și eventual pe E11, teza morfologică, care era prima la tăiere și are un
precedent publicat de nereplicare.

### Partea bună, și e mare

Cu **semnalul A singur**, fără B, fără C, fără fix de lemă, r mediu **0.5523** peste cele 10 limbi.
Batem **8 din 9** run 1 al lui Cristea și Nisioi, singurul rezultat publicat pe MLSP fără etichete în
limba țintă; pierdem doar franceza, cu 0.018. Sinhaleza urcă de la −0.0290 la 0.2216, japoneza de la
0.2803 la 0.4880. Bara rămâne 0.657 al lui G-Eval cu GPT-4o, unde pierdem 9 din 10.

Structura lui Δ e ea însăși interpretabilă: ajută doar pe ca, es, it, toate romanice, și strică tare
doar pe japoneză, singura cu alt sistem de scriere.

### Fapte operaționale de reținut

- **Niciun LLM n-a rulat vreodată în proiect.** Ollama există local cu 3 modele, dar **nu e ruta
  noastră**, vezi [[rute-rulare-logits]]. Primul număr dat de un LLM cere Blocul D, șapte reparații în
  `LLMRater`.
- **E1 costă 157 de secunde**, nu ore. Embedding-ul XLM-R e 74.3 itemi/s pe MPS. Cache-ul `.npy`
  există acum, deci rulările pe brațul înghețat sunt de ordinul secundelor.
- **Reproducerea bit-exactă e păstrată**, verificată la nivel de funcție: tot ce e nou intră prin
  `na_policy="mlsp"`, opt-in. O rulare completă `--variant best` rămâne nefăcută.
- **Nimic nu e comis în git.**

**How to apply:** nu replanifica Δ. E măsurat și e mort ca design central. Următorul lucru care
deblochează ceva e Blocul D, fiindcă fără el semnalele B și C nu pot produce nicio cifră. Vezi
[[lolo-exista-deja-in-cod]] pentru cifrele complete.

---

## ACTUALIZARE 17 august 2026, sesiunea Bloc E: etapa 1 și E.10 sunt închise

**Documentul de reluare e acum `~/.claude/plans/taskuri-executie-saptamana-4.md`**, care îl înlocuiește
pe `saptamana-3`. Acolo stau starea completă, cele cinci verificări trecute și Partea II, promptul de
sesiune.

**Bake-off-ul a rulat pe tot bazinul**, 7 modele × 300 de instanțe de trial, plus E.10, zece variante de
prompt pe două modele. Aproape 12000 de măsurători, toate pe disc în `output/`. Cifrele sunt în
[[bakeoff-etapa1-rezultate]] și [[prompt-ansamblu-decorelat]]. Prompturile multilingve sunt acum în
engleză cu limba țintei numită explicit, iar calea românească a rămas pe ale ei, verificat prin
reproducerea bit-exactă a lui `output/FINAL_best.csv`, max|diff| = 0.

**Ce a rămas oprit la jumătate, deliberat:** `v4_cot` pe Gemma, o comandă de circa 30 de minute,
`python prompt_lab.py --model gemma4-12b-4bit --variants v4_cot`. E singura rezervă a concluziei că
ansamblul de prompturi nu se transferă între modele.

**Următorul lucru ieftin care deblochează interpretarea:** brațul înghețat E1 evaluat pe aceleași 300 de
instanțe de trial. Minute, embedding-urile sunt în cache. Fără decalajul trial-față-de-test măsurat pe
același model, nicio cifră de trial nu se poate pune lângă bara publicată de 0.657.

Apoi etapa 2, semnalul B pe cele 5624 de ținte de test, 84 până la 112 minute per model, plus fuziunea A
cu B cu ponderi alese tot LOLO. Niciuna din cifrele de etapa 1 nu e sistemul final, sunt semnale
dezbrăcate.

---

## ACTUALIZARE, sesiunea Bloc D: primul LLM a rulat, iar Bloc E e deblocat

Documentul de reluare e acum **`~/.claude/plans/taskuri-executie-saptamana-3.md`**, care îl înlocuiește
pe `saptamana-2` (marcat ISTORIC în antet). Evidența cifrelor e în repo, `output/d4_sanity.md`.

Toate cele șapte reparații sunt făcute. `LLMRater` cere acum numele modelului **explicit**, cunoaște
`mps` și MLX, iar bazinul de 7 modele stă în `mlsp_common.LLM_POOL` cu `revision=` fixat. Semnalele B
și C merg amândouă, verificate pe Qwen3-8B. **Primul număr real dat de un LLM: 0.6823.**

**D.3 s-a rezolvat prin ștergere, nu prin corectare.** Δ_controlat fiind mort, corecția RoLlama3 în
RoLlama3.1 n-avea obiect. Constanta `LLM_NAME` a dispărut; numele vechi a rămas doar ca
`RO_LEGACY_LLM`, trecut explicit la unicul apelant.

**Referința de reproductibilitate pentru `--variant best` e `output/FINAL_best.csv`, nu
`submission.csv` din rădăcină.** Acesta din urmă e un artefact din 23 iulie, dintr-o altă configurație,
și diferă de ce produce codul comis cu max 0.226. Codul reproduce `FINAL_best.csv` bit-cu-bit, deci
rularea completă rămasă neverificată din sesiunea E1 e acum **închisă**.

**Capcanele tehnice măsurate** (garda `<think>` inversată față de cum e formulată de obicei, pragul
`1e-9` insuficient, Gemma 4 care nu se încarcă sub `mlx-lm` 0.31.3, `TokenizerWrapper` neapelabil) sunt
toate în [[rute-rulare-logits]], care e locul lor.

**Ce blochează Bloc E, și e decizie de luat:** prompturile din `solution_bert.py` sunt în română și
spun „expert în lingvistica română". Pe 10 limbi asta confundă limba promptului cu limba țintei.
Neutru în engleză peste tot, sau tradus per limbă. Se declară în paper oricum.

**How to apply:** înainte de orice cifră din Bloc E, rulează `python d4_sanity.py --model <cheie>` pe
modelul respectiv. §10.2 al planului de bake-off o cere, costă secunde, și a prins deja două defecte
reale la prima folosire.

## ACTUALIZARE, 18 august: etapa 2 e închisă, avem cifre pe test

Documentul de reluare devine **`~/.claude/plans/e-ti-pe-proiectul-din-dynamic-map.md`**, planul
sesiunii săptămânii 4, executat integral. Toți cei cinci pași sunt gata: `v4_cot` pe Gemma, brațul
înghețat pe trial, semnalul B pe testul complet cu trei brațe, fuziunea A+B și bootstrapul pe contexte.
**Sistemul dă 0.6522 pe test, la 0.0049 sub G-Eval.** Vezi [[etapa2-test-rezultate]] pentru cifre și
[[decalaj-trial-test-masurat]] pentru de ce cifrele de trial nu erau predicții.

## ACTUALIZARE, 18 august seara: fixul de lemă e portat, sistemul e la 0.6568

`stanza` 1.14 instalat, 1.4 GB de modele jos pentru 8 limbi, `lemmatize_mlsp.py` și
`analysis_lemma.py` scrise. **Contribuția #3 nu mai e o predicție, e o măsurătoare.** Cifre complete
în [[fixul-de-lema-multilingv-masurat]]; ansamblul de modele testat și respins în
[[ansamblul-de-modele-nu-se-transfera]].

Starea raportabilă: **A 0.5630, B 0.6322, fuziunea 0.6568**, la −0.0003 sub G-Eval și **peste
TMU-HIT** cu +0.0030.

Ce rămâne deschis, în ordinea în care Alexandru le-a cerut pe 18 august: **eye-tracking întâi**
(verdictul de respingere e în planul eager-pine §V4, cu condiția de răsturnare scrisă explicit), apoi
**inventarul a ce s-a implementat în proiectul românesc și n-a fost portat**. Promptul de reluare:
`~/.claude/plans/PROMPT-idei-imbunatatire-sesiune-noua.md`.

## ACTUALIZARE, 18 august, sesiunea de gândire: eye-tracking închis cu cifră proprie, plus o pârghie nouă

Documentul de reluare devine **`~/.claude/plans/reluare-19-august-lucrarea-multilingva.md`**, care
conține și fragmentele de cod ce reproduc cifrele. Planul aprobat:
`~/.claude/plans/e-ti-pe-proiectul-din-enchanted-spring.md`.

**Eye-tracking, cele două lucruri de corectat în ce scrie mai sus.** Formularea „+0.84 din 69.74,
~1%" e în compozit, nu în r. Conversia e exactă și dă **+0.0067 în r**, cu fixul de lemă la +0.0328,
de cinci ori mai mult. Vezi [[eye-tracking-cat-a-adus-in-r]]. Și afirmația „un predictor de gaze nu e
punte validă" era **asertată, nu măsurată**: e chiar unghiul pe care V4 nu l-a considerat, iar poarta
care îl decide, 15 minute fără descărcare, e aprobată și descrisă în plan §1.5. Verdictul de
respingere rezistă oricum, acum pe un număr al nostru.

**Pârghia nouă, și e cea mai mare per oră din tot ce a rămas.** Calea românească mediază două brațe
de transfer, calea multilingvă le topește într-un singur fit. Portarea urcă fuziunea de la 0.6568 la
**0.6628**, cu zero inferență, fiindcă `p_en` și `p_multi` sunt amândouă deja în
`output/e1_frozen_preds_lemma.csv`. Trece peste G-Eval. Vezi [[ansamblul-de-surse-pentru-semnalul-a]].

**Două lucruri găsite pe drum, ambele nescrise nicăieri până acum:** fertilitatea per țintă are
reziduu +0.2657 pe sinhaleză după control pe lungime și zipf, unde `wordfreq` nu întoarce nimic, deci
e singura informație de tip frecvență pe care limba aia o are; și **rândul englezesc nu e zero-label**,
fiindcă CompLex EN intră în `Xtr` pentru fiecare limbă inclusiv pentru L = en, iar tabelul de garanții
din `e_fusion_lolo_fittest_lemma.md` nu menționează asta. Atinge direct C1, care e revendicarea
centrală.

**How to apply:** primul pas e §3.1, o oră, zero inferență, cu poarta de reproducere bit-exactă a lui
0.6568 înainte de orice cifră nouă. Nimic din sesiunea de gândire nu a atins repo-ul.

## Adaugat 19 august 2026: constrangerea de calendar, care nu era scrisa nicaieri

**Lucrarea multilingva nu exista ca text.** `Paper/Articol_Complexity/paper_full.tex`, 70 KB, ultima
modificare 30 iulie, e lucrarea ROMANEASCA, „Cross-Lingual Transfer for Romanian Lexical Complexity
Prediction", cu sectiuni despre patru semnale, eye-tracking si RoLCP. Se reutilizeaza `acl.sty`,
bibliografia si o parte din Related Work; Approach, Results, ablatiile, analiza de erori si
Limitations se scriu de la zero pe 10 limbi si pe un protocol care nu apare in textul actual.

Asta, si nu numarul de experimente ramase, dicteaza calendarul. Mergand inapoi de la 12 octombrie: o
saptamana de buffer si lectura de coautor, doua saptamani de scris integral, deci **inghetul cifrelor
e 20 septembrie 2026** si scrisul pe sectiunile care nu depind de cifre incepe in saptamana 3.

**How to apply:** orice propunere noua de experiment dupa 20 septembrie se refuza, indiferent cat de
promitatoare pare. Si toate schimbarile care rescriu cifrele publicate (adoptia mediei de encodere,
fixul de caz din `find_char_span`, `--pick-split test` din
[[selectia-modelului-b-e-pe-splitul-gresit]]) se fac intr-un **singur eveniment de renumerotare**, nu
in trei.

## ACTUALIZARE 19 august 2026: lucrarea multilingva EXISTA ca text

`Paper/Articol_Multilingv/paper_full.tex`, 63 KB, plus derivatul `paper_full_copy-paste.tex` generat
cu `make_copypaste.py` copiat acolo. Compileaza curat: **8 pagini**, continutul se termina pe pagina
6, 0 erori, 0 `Undefined`, 0 `Overfull`, 19 `\bibitem`, `.aux`-urile masterului si derivatului
identice. Sesiune de scris pur, zero masuratori, P10 nepornit.

Structura: 1 Introduction, 2 Related Work, 3 Approach, 4 Results, 5 Conclusions, Limitations. Patru
tabele, nicio figura. Ordinea de scriere a fost Results, Limitations, Approach, Related Work si
Conclusions, Introduction ultima.

**`Paper/TEXT_DE_LIPIT_multilingv.tex` NU se mai lipeste ca atare.** Verificat cifra cu cifra contra
`output/e_rezumat_modele.csv` si a rapoartelor: cinci pasaje aveau erori, toate corectate in lucrare.
Cea grava e pasajul 2, care **inversa cele doua ablatii**: scoaterea mediei de encodere costa 0.0052
si scoaterea selectiei pe test costa 0.0057, nu invers. Restul: pasajul 3 numea 0.610 „the only
published number" desi baseline-ul si Archaeology folosesc si ele zero etichete si desi cifra e
media noastra din Anexa B, nu una publicata; pasajul 4 spunea „the four encoders" cand sistemul
mediaza trei si cand M1 a fost rulat fara `--pick-split`; pasajul 10 spunea „recovers most of the
gap" pentru franceza, unde e o treime; captionul din pasajul 9 se contrazicea si dadea `.487` la
Archaeology cand randul lui tiparit mediaza la `.486`.

Doua capcane in fisierele-sursa, nereparate acolo: `e_adoptie.md` §1 si §3 numesc 0.669223 „media a
patru encodere" si preteaza sistemul adoptat la 4.7 minute de encodere, cand sunt trei si 2.5
minute; `e_m1.md` se inchide cu „70 de configuratii" in loc de 51.

**De completat inainte de trimitere**, marcat si in comentariile din `.tex`: lista de autori a
intrarii `enomoto-etal-2024-tmu`, citarile rapoartelor tehnice ale celor trei modele de limbaj (acum
numite in text fara citare), graful de citari MLSP 2024, si titlul, care e provizoriu.

**How to apply:** cifrele lucrarii nu se mai re-deriva, se citesc din `.tex`. Orice cifra noua trece
intai prin `make_rezumat_modele.py` si `analysis_audit_jurnal.py`. Vezi [[p11-adoptia-facuta]],
[[bifurcatii-de-declarat]] si [[constante-hardcodate-mint-dupa-renumerotare]].

### P10: RULAT si INCHIS, 19 august 2026

`qwen35-9b-8bit` are acum toate cele 10 limbi pe splitul de test. 5624 de instante in **4888s = 81.5
min** la 0.87 s/item, 0 NaN la B si 38 la C. Costul real a fost cu 8 minute peste estimarea de ~73,
fiindca modelul a mers la 0.87 s/item pe tot testul, nu la cei 0.776 masurati pe franceza.

**Ambele porti au trecut.** `md5 output/FINAL_best.csv` = `743bce923af4c4b82e578de47ea32826`. Si, mai
important, **cele 569 de randuri franceze re-masurate ies identice bit cu bit** la B si la C, cu
aceleasi 3 pozitii NaN, `|delta| max = 0`. Deci ruta MLX cu citire de logits e deterministă la
reincarcarea modelului, nu doar in cadrul unei rulari.

**Cifra NU s-a miscat: 0.674946, exact.** Harta ramane `gemma4-12b-4bit` pe toate cele zece limbi si
tot patratul lui P9 se reproduce la a sasea zecimala (0.664581 / 0.669223 / 0.669735 / 0.674946,
+0.010365 [+0.0060, +0.0146]). Deci a fost Ramura A, si n-a fost eveniment de renumerotare.

**Ce a cumparat, in cifre care se citeaza:** bazinul e 3/3 pe fiecare limba. Media lui B a lui
`qwen35-9b-8bit` pe cele 10 limbi e **+0.591**, intre Gemma (+0.642) si `qwen3-8b-4bit` (+0.374), deci
locul doi la selectie e acum el, nu qwen3. Marja lui Gemma la criteriul LOLO, adica media peste
celelalte noua, e intre **+0.0448** (ja) si **+0.0597** (ca) la toate cele zece alegeri, deci nicio
alegere nu e la limita.

**Singura constatare noua, si e onesta ca limitare:** oracolul per limba ar diferi pe **catalana**,
unde `qwen35-9b-8bit` da **+0.507** fata de **+0.483** al lui Gemma. Criteriul nu poate vedea asta,
fiindca nu citeste niciodata etichetele limbii pentru care alege. Asta a intrat in Limitations.

In lucrare s-a schimbat **un singur paragraf**, cel din Limitations care declara bazinul ingust; a
fost inlocuit, nu sters, cum cerea comentariul din `.tex`. Derivatul regenerat, amandoua recompilate:
8 pagini, continutul pana pe pagina 6, 0 `Undefined`, 0 `Overfull`, 0 erori, 0 „rerun", 19
`\bibitem`, `.aux`-uri identice si PDF-uri identice bit cu bit. Numarul de configuratii ramane **51**,
recalculat nu copiat.

**Reparate pe drum, amandoua din lista de 19 august:** etichetele „patru encodere" din
`analysis_adoptie.py` (§1 al raportului) plus aritmetica tabelului de cost, care insuma toate cele
patru randuri din `cost_inferenta.csv` (4.7 min) in loc de cele trei adoptate (**2.5 min**, `xlmr`
+ `labse` + `e5`, fara `xlmr-large`); si comentariul din `bakeoff_trial.aggregate` care spunea ca
harta model-per-limba vine de pe trial, depasit de `--pick-split test`.
