Continuam documentatia de curs din `Paper/Articol_Multilingv/documentatie_overleaf.tex`. Experimentele
sunt gata si rezultatele exista. In sesiunea asta doar scriem documentatia, nu rulam experimente noi.

Regulile si pasii 0-9 sunt in `docs/PROMPT_sesiune_documentatie.md`. Pasii 0-3 sunt facuti. Acknowledgments
e scris. Modelul de stil e RALS (Anghel et al., EMNLP 2025, `~/Downloads/2025.emnlp-main.1603.pdf`).

## Unde am ramas (12 oct, citarile rezolvate, URMEAZA auditul)

.tex sha **4ff7c0a6**, compilat curat, 14 pagini, corpul tot pe p8. Backup inainte de citari in scratchpad-ul sesiunii 32f8ff93
(`doc_before_cit.tex`, sha 34116f53). Nimic comis. De urcat in Overleaf (doar .tex-ul).
- Fraza `\texttt{1}`..`\texttt{5}` din Step 5 -> font uniform (era singurul `\texttt` din corp).
- 11 intrari bib noi, verificate pe sursa: scikit-learn (HGB), LightGBM, XGBoost, CatBoost, ExtraTrees, RandomForest, TabFM (Kong et al.,
  arXiv:2609.37959; noi am rulat 1.0.0, paperul descrie 1.1.0, textul spune "TabFM 1.0.0"), Qwen3.5, Llama 3.1, Aya Expanse, LoRA.
  TreeSHAP adaugat la fraza SHAP. Scoase din bib (necitate): Pires, Peters, Wu si Dredze, Liu 2021, Gorman si Bedrick.
- Raman: Claude Opus/Sonnet fara citare (nu exista paper); `\nocite{*}` inca activ.
- **URMATOAREA SESIUNE: `docs/PROMPT_sesiune_audit_references.md`** (audit References + greseli de scriere/forma, decis de el).

## Unde am ramas (11 oct, scurtarea la 8 pagini FACUTA, sesiunea 36e1e6b0), ULTIMUL bloc

Sesiunea `docs/PROMPT_sesiune_scurtare_8_pagini_continuare.md`. .tex sha **97101002** (urcat de el in Overleaf), compilat curat (0 erori/Undefined/
Overfull/??), **14 pagini**. **Corpul (pana la Conclusions) se termina pe pagina 8**, coloana dreapta jos; Implementation tot pe p8;
Limitations de la p9. Varianta (A) aleasa de el: Limitations, Acknowledgments, bibliografia si anexele nu se numara.
Backup-uri in scratchpad-ul sesiunii 36e1e6b0 `bak/` (409c89f3 = inceputul sesiunii, apoi 505e11a6, b3a5b329, cfd26403, 90b4702c,
6b333173, f816e680, 63a8bb49, e0ee7f03, f2043431, eed5bd16). Copia de referinta dinainte de orice scurtare (bc856e97), ceruta de el:
`Paper/Articol_Multilingv/documentatie_overleaf_inainte_de_scurtare.tex` (3 randuri de comentariu sus, restul identic). Nimic comis.
In Overleaf trebuie urcate .tex-ul SI `figures/fig_pipeline_doc.pdf` (Fig. 1 orizontala).
- Scos (la cererea lui): ultimul paragraf din Related Work (Pires, Peters, Libovicky); autorii (`\author{}`; pentru ARR, la final,
  optiunea `[review]`, care ii ascunde singura si pune numere de rand).
- Fig. 1 orizontala (`fig_pipeline_doc.pdf`, `\textwidth`); verticala ramane alternativa in comentariu.
- Anexe noi, text mutat cuvant cu cuvant, doar trimiterile schimbate: A Method Details (lista celor 4 trasaturi din Step 2 +
  paragraful cu scrierea latina si indicatorii; descrierea bootstrap-ului din 3.5), B Additional Results for Signal A (Encoder Layers,
  figura t-SNE + paragraful ei, Regression models + Tabelul 5 + TabFM, Tabelul 6 A-B/Ridge-HGB), C Additional Results for Signal B
  (Language models + Tabelul 7 + "Replacing Gemma 4"), D SHAP of All Inputs, E Comparison with Published Results (Tabelul 8). Ordinea:
  anexele de text intai, floaturile pe doua coloane la sfarsit (altfel textul lor incepea inaintea tabelului din E); tabelele din
  anexe `[hb]` (cu `[t]` Tabelul 5 urca intre referinte). Formula centrarii (ec. 3) ramane in 4.1, la cererea lui.
- Doua propozitii-punte noi (Claude): Step 2 "We then add four word features (Appendix A): Subword count, Word frequency, Syllable
  count and Capitalised."; 3.5 "... over the languages, with a 95% bootstrap confidence interval (Appendix A)."
- Scurtari de text aratate in chat si aprobate: 3.5 efectul indirect (scos "for signal A and for the choice of T and of the grouping");
  4.3 setarile in trei propozitii, scos 7.4%, paragraful A-B scurtat, ultimul paragraf lipit de primul; 4.4: doua propozitii (surse,
  5,627/5,624, "We compare only the means") si fraza TMU-HIT per-language best mutate in caption-ul Tabelului 8. Lista din Data inline.
- Respinse/neaplicate: keywords si abstract pe toata latimea (cu caseta sablonului strica, -98 pt; fara caseta incalca sablonul:
  titlebox minim 5 cm, abstractul in prima coloana); unirea propozitiilor din paragraful 3 al introducerii; Introduction nescurtata
  (castig 1 rand); paragraful din RW cu G-Scale 0.669 (inca acolo, ~4 randuri daca e nevoie de rezerva).
- Semnalat: din 4.1 nu mai trimite nimic la comparatia celor 10 regresori (doar TabFM e numit in intro-ul sectiunii 4); oferit o
  propozitie, fara raspuns. Rezerva pe p8: ~49 pt (~4 randuri) cu trimiterile reale.
- Ramane: verificarea finala (scos `\nocite{*}`, `[review]` pentru ARR, emailuri daca e cazul), el verifica la curs ca blocurile
  mutate pot sta in anexa. Uneltele de masurat: `docs/scurtare_tools/` (compile.sh, measure.py, variants.py).
- Dupa scurtare: `\newpage` inainte de `\bibliography` (cerut de el: titlul References era jos in coloana stanga de pe p9;
  acum sus in coloana dreapta). De scos daca o schimbare viitoare aduce titlul oricum sus intr-o coloana.
- Verificat cu script fata de copia de referinta (bc856e97): nimic pierdut din greseala. Fapte scoase cu acordul lui, care nu
  mai apar nicaieri: Step 2 (scala Zipf, rolul indicatorilor); TabFM "averages 8 predictions"; Baseline ("close to signal B alone
  (0.663, 0.665)", Opus + Sonnet +0.001, trimiterea la tabel); Language models (corelatiile intre LLM-uri 0.769/0.504/0.558,
  Llama 0.681/0.731, Aya 0.565/0.659, "all less than between prompts", "own machine"); 4.4 (corelatia unica pe toate limbile, lista
  celor 7 limbi, "lists only published methods"); Sectiunea 5 (95% din tinte au privire, "embedding exists in every language",
  ponderile surprisal de/fil); RW Pires/Peters/Libovicky; 3.5 "for signal A and for the choice of T and of the grouping"; 4.3 7.4%.
  Oferit: oricare poate reveni in anexe (nu se numara); fara raspuns.
- Eye-tracking (MultiplEYE): decis de el, NU intra in 3.1 Data (nu e parte din metoda); ajunge ca e in Sectiunea 5 si in Data
  Sharing. RoLCP e deja in Data (2) si in Data Sharing. Semnalat, neaplicat: Data spune "We do not use its trial split", dar
  trial-ul a fost folosit in dezvoltare (lista scurta de LLM-uri, Anexa C; exemplele few-shot, Sectiunea 5); Limitations o spune.
- Deschis: t-SNE pe fiecare encoder in Anexa B (exista `output/tsne_centrare_3encodere.png`, 2x3 panouri, cu titlu si randul de
  vecini: XLM-R 0.64->0.39, mE5 0.51->0.30, LaBSE 0.38->0.27); de refacut in stilul Fig. 3 daca o vrea; recomandat: langa figura
  cu vectorul lipit. Fara raspuns inca.
- **ASTEAPTA REVIEW-UL PROFESORULUI** (11 oct seara): el a trimis/urcat varianta 97101002. Nu se schimba nimic pana la review.
- Copia de referinta: autorii scosi si din ea, la cererea lui (sha ae03eaca; singura schimbare fata de bc856e97, notata in antet).
- Verificat (cerut de el) daca Anexa A Method Details e permisa: ARR CFP (aclrollingreview.org/cfp) da ca exemple de continut
  pentru anexe "pre-processing decisions, model parameters, feature templates" (detalii pentru reproducere), dar tot ce e central
  sau necesar ca sa judeci corectitudinea si afirmatiile trebuie sa ramana in corp, altfel risc de desk reject; recenzentii nu
  sunt obligati sa citeasca anexele; ACLPUB formatting: anexele dupa bibliografie, nu se numara, "not critical to the reading".
  Concluzia data lui: lista trasaturilor si procedura bootstrap sunt de tipul permis; corpul pastreaza Step 2 cu numele
  trasaturilor, formula, Word features, SHAP. Sablonul cursului (`docs/instructions_documentation.md`) cere in Approach "explain
  every step in the process" si "at least two pages", fara limita de 8 pagini (limita e a ARR).
- Propuse, NEAPLICATE (cost masurat ~0, corpul ramane pe p8): (1) in propozitia-punte din Step 2, "\emph{Word frequency} from
  the wordfreq library \citep{speer-2022-wordfreq}" (4.3 numeste wordfreq, care acum e prezentat si citat doar in anexa);
  (2) in 3.5 "a 95\% bootstrap confidence interval that resamples whole contexts (Appendix~A)". De aplicat dupa review, daca vrea.

## Unde am ramas (11 oct noaptea tarziu, scurtarea inceputa)

Sesiunea `docs/PROMPT_sesiune_scurtare_8_pagini.md`. .tex sha **409c89f3**, compilat curat (0 erori/Undefined/Overfull/??),
**14 pagini** (anexa B noua), corpul se termina pe **pagina 11**, coloana dreapta, ~80% jos (inainte: pagina 12, jos). Backup-uri in
scratchpad-ul sesiunii a0f202c1 `bak/` (bc856e97 = originalul, 69753d47 = doar poza, 5761d922, d51b9eca, 31330342). **El urca
.tex-ul in Overleaf** (nicio figura noua, doar latimile). Nimic comis. Feedback: [[documentatie-scurtare-feedback-11-oct]] din memorie.
- Facut: pipeline la 0.65, t-SNE la 0.75, SHAP la 0.55 din latimea textului (tabelele NU s-au micsorat). Respins de el si revenit:
  taierea definitiilor repetate din sectiunea 4 (Method si sectiunea 4 sunt cele mai importante, nu se taie masiv).
- Step 2: scoase propozitia cu scala Zipf si cea cu indicatorii. Tabelul 8 (Comparison with Published Results) in anexa B,
  cuvant cu cuvant, cu trimitere "Table 8 (Appendix B)" in 4.4.
- Texte rescrise de Gemma 4 (prompturi in `docs/PROMPT_gemma_*`): Language models 4.2 (400 -> 239 de cuvinte, `_language_models`..`_v5`,
  cu clauza despre etichetele de trial ale limbii de test pusa la loc), Regression models (116 -> 89, `_results_regression_models_v3`),
  TabFM (124 -> 115, `_results_tabfm`), Baseline (218 -> 171, `_results_baseline_v4`), 4.4 (303 -> 273, `_results_published_v4`, cu valorile
  in text), Sectiunea 5 (335 -> 302, `_what_did_not_work_v5`). Gemma NU respecta limitele de cuvinte: scurteaza 10-25%.
- Nepuse/respinse: intro-ul sectiunii 4 (propunere in chat: scos doar "Signal B does not fine-tune ..." si "in the dataset", neraspunsa);
  spatiul din 3.1 Data (itemsep/parsep/topsep 0 nu muta textul de dupa lista, justificarea verticala il absoarbe; singura varianta ar fi
  lista inline, nedecisa); a1 (Regression models + TabFM), a3 (tab:llms), a4 (tab:corr-ab) in anexa B ("da, cred ca e ok" cerut de el
  inainte, neexecutat; masurat ~1.3 pagini pe baza precedenta); celelalte blocuri din lista (a2 layers, a6 bootstrap, a7 lista trasaturilor).
- Semnalat in Baseline (neatins): fuziunea metoda + Claude e pe zece limbi (0.706, 0.724, +0.013) iar restul paragrafului pe unsprezece
  (0.713, 0.732, +0.011 in `output/doc_claude.txt`); "below our method by 0.008" pe unsprezece e in zgomot (-0.0076 [-0.0176, +0.0020]);
  TabFM fara citare in bibliografie.
- Corpul trebuie sa ajunga la 8 pagini; mai raman ~3 pagini. Optiunile masurate (pe baza veche, din prompt): G1 sau P3 din chat
  (anexa B cu a1, a3, a4, a6, a7 + figura 1 orizontala; t-SNE in anexa sau patru blocuri de text taiate). `\section*{Implementation}`:
  intrebat daca se numara, fara raspuns. Anexa: de confirmat de el la curs.
- Apoi verificarea finala: scos `\nocite{*}`, autori si emailuri.

## Unde am ramas (11 oct noaptea, Limitations SCRIS)

Sesiunea `docs/PROMPT_sesiune_limitations.md`, pasii 1-3 facuti. .tex sha **bc856e97**, compilat curat (0 erori/Undefined/
Overfull/??), **15 pagini** (bibliografia si anexa au impins o pagina), corpul se termina tot pe pagina 12; Limitations pe
pagina 12, Acknowledgments si bibliografia de la 13. Backup 04022d88 in scratchpad-ul sesiunii 9f4ea581 `bak/`; draftul
meu aprobat (sha 043c7a62) e textul dintre `<<< >>>` din `docs/PROMPT_gemma_limitations.txt`. **El urca .tex-ul in Overleaf** (figurile neschimbate). Nimic comis.
- Limitations: doua paragrafe, text de Gemma 4 (`docs/PROMPT_gemma_limitations.txt`, apoi `_v2` cu trei schimbari:
  "When" in loc de "If", trial-ul limbii de test doar cand e limba MLSP, al 3-lea prompt ales dupa comparatia pe test),
  pus neschimbat (identitate verificata cu script), 256 de cuvinte. Paragraful 1 (cerut de el, primul): doar LLM-uri
  open-weight de 8-12 miliarde de parametri, 4/8 biti; Claude Opus in locul lui B duce media de la 0.693 la 0.725
  (doc_claude.txt, A + opus); TabFM doar redus (394 din 768 de dimensiuni, XLM-R base, zece limbi). Paragraful 2:
  exceptiile de la zero-label (lista scurta pe trial, al 3-lea prompt pe test, setarile fixe comparate pe test pe
  versiuni vechi, versiunea raportata aleasa pe test). Fara cifra de configuratii: jurnalul `output/e_rezumat_modele.csv`
  se opreste pe 22 aug. Scoase/nepuse: "slightly optimistic", scara 0-1 (standardizarea pe limba), bugetul (nu exista suma).
- El considera ca Limitations nu intra in cele 8 pagini (regula ACL/ARR); de confirmat la curs daca se numara.
- Semnalat, nerezolvat: "All experiments use publicly released datasets" (MultiplEYE romanesc neverificat ca public).
- Intrebat de el: What Did Not Work mutat in Limitations (ca sa iasa din cele 8 pagini)? Recomandat NU: cursul cere
  sectiunea de experimente, sunt rezultate (nu limite), iar ACL nu vrea continut nou in Limitations. Daca lipseste loc
  la scurtare: What Did Not Work in anexa, de intrebat la curs. Nedecis.
- URMEAZA: sesiunea de scurtare la 8 pagini (corp pana la Conclusions; Limitations si anexele nu se numara), cu
  `docs/PROMPT_sesiune_scurtare_8_pagini.md` (scris 11 oct). Apoi verificarea finala cu scoaterea lui `\nocite{*}`,
  autori si emailuri.

## Unde am ramas (11 oct seara, Abstract si Keywords SCRISE)

Sesiunea `docs/PROMPT_sesiune_abstract.md`, pasii 1-3 facuti. .tex sha **04022d88**, compilat curat (0 erori/Undefined/
Overfull/??), 14 pagini, corpul se termina tot pe pagina 12. Backup 05155e79 in scratchpad-ul sesiunii 3273e1c4 `bak/`.
**El urca .tex-ul in Overleaf** (figurile neschimbate). Nimic comis.
- Abstract: draftul meu (157 de cuvinte) aprobat in chat, apoi rescris de Gemma 4 (`docs/PROMPT_gemma_abstract.txt`) si
  revizuit de el de patru ori, fiecare `_vN` pornind de la ultimul raspuns: `_v2` "test language" si "30 labels of each
  evaluated language"; `_v3` fara prima fraza ("Labelled data ... few languages"), modelul nenumit ("an open-weight LLM"),
  "on all the languages of the evaluation data" in loc de lista; `_v4` formularile lui "combines two regressor models,
  ridge regression and gradient-boosted trees, trained" si "using zero-shot prompt"; `_v5` fara "or setting selection".
  Textul `_v5` (138 de cuvinte) pus neschimbat, identitate verificata cu script; sursele cifrelor in comentarii.
  Semnalate, lasate de el: "using zero-shot prompt" (fara articol, singular desi sunt trei prompturi); "regressor
  models"; fraza zero-label spune doar "for training" (setarile nu mai sunt numite; Introduction le are); romana nu
  mai e numita in abstract.
- Keywords: scos Zero-Label Evaluation, adaugat Eye-Tracking (cerut de el). Lista: Lexical Complexity Prediction,
  Cross-Lingual Transfer, Leave-One-Language-Out, Multilingual Encoders, Large Language Models, Eye-Tracking.
- **URMATOAREA SESIUNE: `docs/PROMPT_sesiune_limitations.md`** (decis de el). Limitations (nescris; lista propusa: al 3-lea prompt ales pe test, setarile fixate in dezvoltare, lista
  scurta de LLM-uri pe trial, plus trimiteri pentru ce e deja in text), verificarea finala cu scoaterea lui
  `\nocite{*}`, autori si emailuri, apoi sesiunea SEPARATA de scurtare la 8 pagini fara anexe.

## Unde am ramas (11 oct, final de sesiune: What Did Not Work si Conclusions ACCEPTATE si URCATE)

.tex sha **05155e79**, compilat curat (0 erori/Undefined/Overfull/??), 14 pagini, corpul se termina pe pagina 12.
**Urcat in Overleaf de el ("mi se pare ok", "am pus pe overleaf").** Backup-uri in scratchpad-ul sesiunii 41d5a7c2 `bak/`.
Nimic comis.
- What Did Not Work: patru buline (Eye-tracking dataset, LLM surprisal, Fine-tuning XLM-R, Few-shot prompt), text de
  Gemma 4 (`docs/PROMPT_gemma_what_did_not_work.txt`, `_v2` pentru bulina de eye-tracking cu intervalul). Eye-tracking pe
  romana masurat direct: +0.0066 [-0.0009, +0.0144] pe cele 1.587 etichete RoLCP (`analysis_doc_et_romanian.py` ->
  `output/doc_et_romanian.txt`). Bib nou `jakobi-etal-2025-multipleye` (Crossref) si fraza MultiplEYE in Data Sharing.
- Conclusions: Future Work SCOS; un text de Gemma 4 (`docs/PROMPT_gemma_conclusions*.txt`, ultimul `_eyetracking_v3`),
  impartit in patru paragrafe la cererea lui; eye-tracking fara cifra ("Even on Romanian, they did not bring a significant
  improvement."), intervalul doar in What Did Not Work. Opus 0.721 spus ca fiind peste noi.
- Implementation: paranteza cu componentele scoasa (cerut de el).
- Semnalate, nerezolvate: "All experiments use publicly released datasets" (nu s-a verificat ca MultiplEYE romanesc e
  public); "This was against 0.551" stangaci in bulina de fine-tuning; cele doua referinte inghetate difera (0.551/0.515);
  LoRA fara citare.
- **URMATOAREA SESIUNE: `docs/PROMPT_sesiune_abstract.md`** (Abstract scris de Claude, aprobat, apoi rescris de Gemma 4;
  keywords). Apoi: Limitations (nescris; lista propusa: al 3-lea prompt ales pe test, setarile fixate in dezvoltare,
  lista scurta de LLM-uri pe trial, plus trimiteri pentru ce e deja in text), pasul 8 (scoti `\nocite{*}`), pasul 9
  (autori), si sesiunea separata de scurtare la 8 pagini.

## Unde am ramas (11 oct noaptea tarziu, What Did Not Work SCRIS, asteapta review-ul lui)

Sesiunea `docs/PROMPT_sesiune_what_did_not_work.md`, pasul 1. Lista taiata de el la patru buline, in ordinea lui:
eye-tracking (cel mai dezvoltat), surprisal, fine-tuning XLM-R, few-shot; plus MultiplEYE in Data Sharing. Restul
listei (prompt de frecventa, prefix, scara 0-9, inlocuitori de frecventa, ansamblu LLM etc.) NU intra.
.tex sha **5c3fc5be** (TEXTUL GEMMA 4 PUS NESCHIMBAT la cererea lui, rulat cu docs/PROMPT_gemma_what_did_not_work.txt, seed 0; doar titlurile "Eye-tracking dataset" si "LLM surprisal" schimbate de el; semnalate nereparate: "do not include any other languages" ambiguu fata de MultiplEYE, "This was against" stangaci), compilat curat, 14 pagini; corpul se termina tot pe pagina 11
(Conclusions inca gol, coloana dreapta a paginii 11). Sectiunea ~290 de cuvinte. Backup 1083d9ee in scratchpad-ul
sesiunii 41d5a7c2 `bak/`. Bib nou: `jakobi-etal-2025-multipleye` (ETRA 2025, DOI 10.1145/3715669.3726843, verificat pe
Crossref, primii 5 autori + others). Data Sharing: fraza noua despre MultiplEYE; "All experiments use publicly
released datasets" lasat neschimbat (de decis de el: nu s-a verificat ca partea romaneasca MultiplEYE e publica).
Semnalate in chat: +0.007 e derivat din compozitul de leaderboard (68.90 -> 69.74), aproximativ (69.74 vs 68.99 pe
tot RoLCP); cele doua referinte inghetate la fine-tuning difera (0.551 vs 0.515), cauza neclara; LoRA fara citare.
Pasul 2: Future Work SCOS (decis de el); sectiunea redenumita "Conclusions", un paragraf ca RALS, ~150 de cuvinte, scris
de mine, sha **05155e79** (Conclusions impartit in 4 paragrafe, cerut de el, cuvinte neschimbate; TOT TEXTUL DE LA GEMMA, cerut de el: Conclusions v3 si itemul eye-tracking din What Did Not Work v2, prompturile docs/PROMPT_gemma_conclusions_eyetracking_v3.txt si docs/PROMPT_gemma_what_did_not_work_v2.txt; continut: in Conclusions doar "Even on Romanian, they did not bring a significant improvement.", intervalul +0.007 [-0.001, 0.014] mutat in What Did Not Work; inainte: paranteza scoasa din Implementation; Conclusions = TEXTUL GEMMA 4 neschimbat, cerut de el, cu frazele despre eye-tracking rescrise la cererea lui: "nici pe romana nu aduce un castig semnificativ", +0.007 [-0.001, +0.014], masurat direct pe cele 1.587 etichete RoLCP cu analysis_doc_et_romanian.py -> output/doc_et_romanian.txt; promptul docs/PROMPT_gemma_conclusions_eyetracking_v2.txt), compilat curat, 14 pagini, corpul se termina pe pagina 12. Asteapta review-ul lui. Intrebat:
scriem acum Limitations? Apoi pasul 3 (Abstract).

## Unde am ramas (11 oct noaptea, Introduction ACCEPTATA de el)

.tex sha **1083d9ee**, compilat curat (0 erori, 0 Undefined, 0 `??`, 0 Overfull), 13 pagini. Backup-uri (1bc24478,
2fe5f38e, e993bc79, d7b7e9c1, 0a44d686, 10730803, b4736e96) in scratchpad-ul sesiunii aee36048 `bak/`. Nimic comis.
**Urcat in Overleaf de el pe 11 oct noaptea (1083d9ee).**
Introduction, forma acceptata ("asta mi se pare ok acum"): ~296 cuvinte, patru paragrafe pe modelul RALS (fara
contributii numerotate, fara roadmap), SCRISA DE GEMMA 4 12B la cererea lui (`docs/gemma_introducere.py`, MLX 4 biti,
gandirea oprita prin canalul gol pus manual; prompturile `docs/PROMPT_gemma_introducere*.txt`), text pus neschimbat,
doar rupt la ~100 de caractere: (1) cititorii, cei care invata o limba primii (fraza de deschidere data de el) + CWI 2018
"words that challenge non-native speakers" + simplificarea lexicala, Saggion 2024; (2) primul pas, Qiu 2024, LCP;
(3) review-ul Shardlow 2024 (noua seturi, opt limbi in afara de engleza), romana abia in 2025 (RoLCP), fara etichete
nu ai pe ce antrena si nici cu ce alege setarile; (4) "In this paper, we address", cele doua semnale, nicio eticheta a
limbii de test in antrenare sau alegerea setarilor, 11 limbi, 0.693, trimitere la What Did Not Work.
Sursele faptelor sunt in comentariul de deasupra. Semnalate, necorectate: "lexical complexity prediction" scris complet
de doua ori in (3) desi LCP e definit in (2); "its settings" ambiguu in (3); "a generally low level of reading
proficiency" in loc de "limited" din fraza lui. Pe drum: o varianta cu contributii First/Second/Third (504 cuvinte)
respinsa ca prea lunga; una scrisa de mine dupa RALS respinsa ("nu-mi place deloc").
**Limita noua, de la el: 8 pagini fara anexe.** Corpul se termina acum pe pagina 11 (~10.5 pagini), cu What Did Not
Work si Conclusions inca goale; grosul e in Results (paginile 6-11, 8 tabele, 3 figuri). Scurtarea = sesiune SEPARATA.

## Unde am ramas inainte (11 oct seara, Related Work ACCEPTAT de el)

.tex sha **1bc24478**, compilat curat (0 erori, 0 Undefined, 0 `??`, 0 Overfull), 13 pagini. Contine si randurile
Claude din blocul de mai jos (759f7816). **Urcat in Overleaf de el pe 11 oct seara (1bc24478).** Backup-uri
(6311649e, 9c4d2930, 7479dc53) in scratchpad-ul sesiunii bf834357 `bak/`. Nimic comis.
Related Work, forma acceptata ("mi se pare ok acum"): ~400 cuvinte, cinci paragrafe scurte, o idee pe paragraf
(el vrea "enter-uri" intre idei si doar ce e complet relevant pentru metoda):
(1) CWI 2018 (franceza prezisa din celelalte limbi) + LCP 2021 / CompLex 2.0 (trasaturi de frecventa si lungime);
(2) MLSP 2024 (zece limbi, doar trial, baseline log-frecventa) + Archaeology intr-o fraza (XGBoost pe trasaturi),
inchis cu "In our work" = LOLO ca franceza in CWI 2018; (3) G-Eval, TMU-HIT (cel mai bun din patru prompturi pe
trial), G-Scale (temperatura pe trial-ul tuturor, regresie pe trial-ul fiecarei limbi, LLM si frecventa relativ
necorelate), inchis cu semnalul B; (4) paragraf separat cerut de el: cea mai mare medie publicata, G-Scale 0.669 cu 30
de etichete pe limba, plus trimitere la Section~\ref{sec:published}; (5) Pires, Peters, Libovicky, inchis cu
encodere inghetate, embeddinguri centrate pe limba, doar regresorii antrenati.
Scoase la cererea lui: Archaeology run 1 si bug-ul (raman doar in 4.4), RoLCP (e in Data), descrierea encoderelor
(Method), Rust (Method), Saggion, Qiu, review-ul 2024, Wu si Dredze, Liu 2021, fraza Claude, detaliile TMU-HIT si
Nohejl pe ca/fil/si. Cifre per paper in RW: NU (dublura cu Tabelul tab:published), doar fraza cu 0.669.
Comentariile de sursa sunt pe fiecare fraza; frazele comprimate NU au trecut prin verificarea pe PDF-uri.

## Next steps, in ordine (sesiunea urmatoare)

0. URMATOAREA SESIUNE (ordinea ceruta de el pe 11 oct noaptea): `docs/PROMPT_sesiune_what_did_not_work.md`, adica
   What Did Not Work incepand cu eye-tracking-ul, apoi Conclusions and Future Work, apoi Abstract si keywords. ABIA
   DUPA asta, in alta sesiune: scurtarea paperului la 8 pagini fara anexe (lista de candidati in chat intai, cu cat
   castiga fiecare; nimic taiat fara OK-ul lui).
1. ~~El urca .tex-ul local in Overleaf.~~ FACUT, inclusiv 1083d9ee (Introduction), pe 11 oct noaptea.
2. Verificare scurta a Related Work pe PDF-uri: doar frazele reformulate la scurtare (LCP 2021 "ranked close to the
   deep-learning ones"; G-Scale "adds a temperature ... and a linear regression"; "Its authors find ... relatively
   uncorrelated", tras de ei din en/ja/es; Pires "transfers even across scripts"; Libovicky "find the representations
   more language-neutral"; 0.669 si "30 labelled instances"). Cu `docs/papers/related_work/q.py`, fara subagenti.
   `docs/PROMPT_verificare_related_work.md` NU exista; il scrii doar daca el vrea sesiune separata.
3. ~~Pasul 5, Introduction~~ FACUT 11 oct noaptea (vezi blocul de sus). Vechiul text al punctului: (sectiunea 1 era GOALA): modelul Columbia pe 5 paragrafe (memoria intro-style-hgs), stil
   RALS, fara formule, fara cadru de competitie, fara em-dash. Propunere in chat intai.
4. Cele patru puncte deschise din blocul Claude de mai jos (Sonnet vs B pe 11 limbi, "below our method by 0.008",
   metoda + Claude pe 11 limbi, A + Sonnet vs metoda): le decide el, textul lui nu se atinge fara cerere.
5. Semnalate, neaplicate: Method pasul 6 nu-l citeaza pe Nohejl la temperatura (acum RW il pomeneste, deci Method
   ar trebui sa-l citeze); 4.4 "Archaeology run~1 is the only published method that reads no label ..., as we do"
   ("only" neverificat pentru GMU/RETUYT-INCO/SCaLAR; "as we do" fata de lista scurta pe trial si al 3-lea prompt
   pe test).
6. Pasul 4, What Did Not Work (sectiune goala): lista intai in chat, ca s-o taie.
7. Pasul 6: Conclusions and Future Work, Limitations (lista din "Ordinea ramasa", plus lista scurta de modele pe
   trial si al 3-lea prompt pe test), Implementation (timpii din release/README.md).
8. Pasul 7 Abstract si keywords; pasul 8 verificarea finala (scoti `\nocite{*}`); pasul 9 autori si emailuri.

## Unde am ramas (11 oct, predictiile Claude primite)

Predictiile Claude (din `~/Downloads/opus_baseline`) copiate in `output/doc_claude/{opus,sonnet}_preds_11lang.csv`.
Script nou `analysis_doc_claude.py` -> `output/doc_claude.txt` (fuziunea din release/fuse.py, Claude in locul lui B;
nota Claude = medie z(1-5), z(0-100) pe limba). Reproduce exact Opus .7212/.7111 si Sonnet .6849/.6747, deci
Sonnet .685 pe 11 limbi e confirmat. Necomise.
In .tex (sha **759f7816**, compilat curat, 13 pagini, backup 7479dc53 in scratchpad-ul sesiunii 566a8acb `bak/`):
randurile "Signal A + Claude Sonnet 5.5" .695 si "Opus" .725 din Tabelul 3; patru fraze noi dupa paragraful lui
(A + Opus +0.004 peste Opus, A + Sonnet +0.010 peste Sonnet, ambele cu interval peste zero; Gemma +0.029;
corelatia notei Claude cu A .77 fata de .685 la Gemma); comentariile de sursa refacute pe doc_claude.txt.
Textul lui din paragraful Baseline e neschimbat (cifrele pe 10 limbi raman aceleasi la 3 zecimale).
De decis de el: (1) "close to signal B alone (0.663 and 0.665)": pe 11 limbi Sonnet e peste B cu +0.0215
[+0.010, +0.032], doar pe 10 nu se distinge; (2) "below our method by 0.008": pe 11 intervalul include zero
[-0.018, +0.002]; (3) metoda + Claude exista acum si pe 11 limbi (Sonnet .713, Opus .732), textul da doar 10.
(4) A + Sonnet (.695) nu se distinge de metoda (.693): +0.0025 [-0.006, +0.010], nescris in text.
**Urcat in Overleaf de el pe 11 oct (sha 759f7816, neschimbat local dupa).** Cele patru puncte de mai sus
raman deschise; textul lui nu se atinge fara cererea lui.
Cu asta, toate "--" din sectiunea 4 sunt completate. Urmatorul pas: vezi "Next steps" din blocul de sus (RW acceptat dupa).

## Unde am ramas (11 oct, LLM-urile locale rulate si trecute in .tex)

Llama 3.1 8B si Aya Expanse 8B rulate pe test (11 limbi, 7.211 instante, 3 prompturi, `signal_b.py --with-ro`,
copie in `~/lcp-llm-extra/release`, release/ din repo neatins; 0.28 s si 0.25 s pe citire). Sursa:
`output/doc_llm_extra.txt` (scriptul `analysis_doc_llm_extra.py`, ratingurile in
`output/doc_llm_extra_signal_b.csv`, `output/doc_llm_extra_fuse_<cheie>.txt`). Necomise.
Cifre, citirea din Tabelul 3 (B / fuziune): Llama .506 / .636, Aya .450 / .626; citirea completa Llama .517 / .638,
Aya .500 / .634. Fata de sistem: -0.0568 [-0.0652, -0.0486] si -0.0664 [-0.0762, -0.0573]. Corelatia lui B cu Gemma
si cu Qwen3.5: Llama .681 / .731, Aya .565 / .659. Niciunul nu bate Gemma in B pe vreo limba; in fuziune bat Gemma
doar pe romana (Llama .744, Aya .761 fata de .742, aceeasi citire). Control cu 5 modele in bazin: Gemma ales pe
11/11 limbi si 0/121 la fitting, media ramane 0.692521. Marginea grilei de T: Llama T = 0.5 pe toate limbile,
Aya T = 64 pe 8 din 11. Aya pe sinhaleza B .021 (tokenizer pe octeti), nu degenerat numeric.
Controlul `--limit 3` pe Gemma: diferenta maxima 2.2e-16 fata de valorile stocate (zgomot de ultim bit).
Cuantizarile optionale (qwen35-9b-4bit, qwen3-8b-8bit): NU se ruleaza, decis de mine.

In .tex (sha **6311649e**, compilat curat, 13 pagini, backup 92f25735 in scratchpad-ul sesiunii 84200af1 `bak/`),
4.2 Signal B, paragraful "Language models": (1) fraza dupa "Among these three..." (modelele rulate ulterior pe test +
controlul cu cinci modele, media 0.693); (2) randurile Llama/Aya din tabelul LLM-urilor; (3) "Replacing Gemma 4..."
cu cifrele lor si "These four rows"; (4) corelatiile lor, cu "All of these correlations are less than those between
the ratings of the three prompts of Gemma 4" (am schimbat "This is less than" fiindca "This" nu mai avea referent).
NEPUSE in text, de decis de mine: nota ca pe romana bat Gemma in fuziune; citirea completa; marginea grilei de T.
In Overleaf se urca doar .tex-ul. Raman "--" doar la cele doua randuri "Signal A + Claude" (predictiile Claude).

## Unde am ramas (11 oct, sesiunea Related Work, asteapta review-ul lui)

.tex sha **92f25735**, compilat curat (0 erori, 0 Undefined, 0 `??`, 0 Overfull), 13 pagini. Tot ce trebuie pentru
verificare e in `docs/papers/related_work/` (necomis): cele 21 de PDF-uri citate (ACL Anthology, arXiv, J-STAGE pentru
Nohejl, Springer pentru CompLex 2.0), textul lor pe pagini in `paged/` (marcaje "=== PDF page N ==="), `q.py`
(`python3 q.py paged/X.txt "citat"` da pagina PDF unde apare) si backup-ul .tex-ului de la start,
`documentatie_overleaf_73a581a3.tex`. Pagina tiparita = pagina PDF + offset (ex. Nohejl +1128, MLSP +570).
Compilare: dir gol, .tex + acl.sty + acl_natbib.bst + figures/, pdflatex, bibtex, pdflatex x2.
Related Work SCRIS: "Related Work" (nu "Challenges"), proza ca in RALS, trei paragrafe (date LCP; sisteme pe MLSP
2024 si ce etichete citesc; encodere inghetate plus Rust), fiecare inchis cu "In our work". Fiecare afirmatie are
comentariu cu sursa (sectiune, pagina PDF / tiparita). Bib nou: liu-etal-2021-preserving (Madotto, nu Xu).
Verificat in trei runde independente pe PDF-uri; toate problemele aplicate. El nu mai vrea agenti multipli (tokeni).
Lungime: TAIAT 11 oct, a doua runda ceruta de el ("prea lung, doar ce e complet relevant, cu enter-uri"):
sha **1bc24478** (dupa scoaterea lui Archaeology run 1/bug si fraza ceruta cu G-Scale 0.669 + trimitere la 4.4), compilat curat, 13 pagini, ~370 cuvinte,
patru paragrafe scurte; Archaeology a ramas o fraza (XGBoost pe trasaturi) in paragraful MLSP. Run 1 ramane doar in 4.4, o idee pe paragraf, RW incape in
coloana stanga a paginii 1. Scoase si RoLCP + baseline RALS (sunt in Data/Results), cele 3 encodere (Method), Rust
(Method), Liu 2021, esantionarea/shot-urile TMU-HIT, Nohejl pe ca/fil/si, gruparea notelor. Backup-uri: 6311649e
(lung) si 9c4d2930 (~630 cuvinte) in scratchpad-ul sesiunii bf834357 `bak/`.
Semnalate in afara RW, neatinse: 4.4 "Archaeology run 1 is the only published method that reads no label ..., as
we do" (only neverificat pentru GMU/RETUYT-INCO/SCaLAR; "as we do" + Labels 0 la noi vs lista scurta de modele
aleasa pe trial-ul tuturor limbilor si al 3-lea prompt ales pe test); Method pasul 6 nu-l citeaza pe Nohejl la
temperatura; Limitations TREBUIE sa spuna lista scurta de modele pe trial si al 3-lea prompt pe test.
Urmatorul pas: review-ul lui pe Related Work (reformularile lui raman cuvant cu cuvant), apoi lista afirmatiilor in chat
si `docs/PROMPT_verificare_related_work.md` (sesiune separata, agentul reciteste PDF-urile din
`docs/papers/related_work/` fara rationamentul nostru). Fara subagenti multipli (memoria `fara-agenti-multipli-tokeni`).

## Unde am ramas (11 oct noaptea, FINAL de sesiune: sectiunea 4 acceptata provizoriu)

.tex sha **73a581a3** (fraza Implementation: forma lui din glioma, cu \href "Github repository", paranteza adaptata la proiect), compilat curat (0 erori, 0 Undefined, 0 `??`, 0 Overfull), 12 pagini. Backup-urile
(40123c97, 1bff82e7, eefb499b, 6deebe5e, 784a5af4) sunt in scratchpad-ul sesiunii ec87bc71 (`bak/`). In Overleaf se urca doar .tex-ul.

Sectiunea 4 e "ok momentan" (spus de mine), dar o mai schimbam dupa LLM-urile locale si predictiile Claude:
- randurile Llama 3.1 8B si Aya Expanse 8B din tabelul LLM-urilor: FACUT mai tarziu in aceeasi zi, vezi primul bloc
  (`output/doc_llm_extra.txt`, `docs/PROMPT_rulare_llm_test.md`);
- cele doua randuri "Signal A + Claude Sonnet/Opus" din tabelul Claude (acum "--"), dupa ce refac predictiile Claude.

Nou in sesiunea asta: `\section*{\uppercase{Implementation}}` cu fraza de reproductibilitate (ca in glioma,
paranteza adaptata la pipeline-ul nostru) si linkul anonim https://anonymous.4open.science/r/zero-label-lcp.
Restul Implementation (unelte, timpii din release/README.md, masinile) ramane pentru pasul 6. Fraza de
reproductibilitate e aprobata asa si nu se mai atinge.

## Ce urmeaza (in ordine)

1. ~~Cand sunt gata LLM-urile locale si Claude: completezi randurile "--".~~ FACUT 11 oct (sha 759f7816). Ramane
   revizuirea sectiunii 4 de catre el si cele patru puncte deschise din primul bloc.
2. Pasul 4, What Did Not Work: lista intai in chat, ca s-o tai.
3. Pasul 5, Introduction si Related Work, in stilul RALS. Related Work descrie ce face fiecare paper
   (notele mutate din 4.4 sunt in comentariul blocului "Systems on the MLSP 2024 data"); 4.4 ramane
   doar cu rezultatele. Apoi `docs/PROMPT_verificare_related_work.md` intr-o sesiune separata.
4. Pasul 6: Conclusions and Future Work, Limitations, restul Implementation.
5. Pasul 7: Abstract si keywords.
6. Pasul 8: verificarea finala, scoti `\nocite{*}`, adaugi intrarile bib lipsa (TabFM, LightGBM,
   XGBoost, CatBoost, scikit-learn pentru ExtraTrees/RandomForest/HGB, Llama 3.1, Aya Expanse).
7. Pasul 9: autori si emailuri.

Sesiunea urmatoare: Related Work, cu `docs/PROMPT_sesiune_related_work.md` (verificare in PDF-uri pentru
fiecare afirmatie). Introduction se scrie separat.

What Did Not Work: RALS nu are o asemenea sectiune (o cere cursul: "a bullet point list of experiments
tried"). Vreau totusi sa scriem acolo despre eye-tracking (memoria `eye-tracking-cat-a-adus-in-r`). Se
decide la pasul 4; deocamdata doar context.

Decizii inca deschise (de la mine): fraza din Data "We do not use its trial split" fata de coloana Trial
din tabelul LLM-urilor; varianta promptului Claude (.721 = "5 + 100"); motivul trasaturilor lexicale (scris
prin RALS); anexa cu prompturile exacte ale lui B (oferita, nedecisa).

## Unde am ramas inainte (11 oct noaptea, dupa runda 4 de review pe sectiunea 4)

.tex sha **eefb499b**, compilat curat, 12 pagini. Backup 1bff82e7 in scratchpad-ul sesiunii ec87bc71.
Runda 4: LOLO pe semnale scris explicit (A antrenat doar pe celelalte limbi; B fara fine-tuning);
fraza despre ablatie scoasa; Encoders reformulat (corelatia Pearson intre perechi); "Bold marks..." scos
din toate captionurile in afara de Tabelul 8 (acolo bold = maximul coloanei, nu al nostru); captionuri
Claude si LLM-uri reduse la o fraza (explicatia randurilor "Signal A + Claude" mutata in text);
temperatura fara "puterea 1/T"; Tabelul 7 explicat (corelatie intre doua predictii, nu cu adevarul);
4.4 doar rezultate, descrierile metodelor mutate ca note pentru pasul 5 in comentariul din Related Work
("Systems on the MLSP 2024 data").

## Unde am ramas inainte (11 oct noaptea, dupa runda 3 de review pe sectiunea 4)

.tex sha **1bff82e7**, compilat curat (0 erori, 0 Undefined, 0 `??`, 0 Overfull), 12 pagini. Backup
40123c97 in scratchpad-ul sesiunii ec87bc71 (`bak/`). Aplicat din review-ul lui:
- Intro sectiunea 4: LOLO explicat pentru ambele semnale (B nu antreneaza nimic, dar T, gruparea, LLM-ul
  si w se aleg pe celelalte limbi); "We say so where they appear" scos, inlocuit cu cele trei comparatii
  din dezvoltare (straturi, TabFM, LLM-uri pe trial); ablatia si intervalul pereche rescrise simplu.
- 4.1: Encoders rescris narativ (fiecare singur, corelatiile, apoi media); coloanele de corelatie (1)(2)
  SCOASE din Tabelele 1, 4 (LLM-uri) si 5 (prompturi), valorile sunt in text; "Encoder Layers" cu
  "step 1 in Figure 1"; "Embedding Centring" cu formula (eq:centring); cifrele vecinilor scoase,
  implicatia scrisa ("could find it easier... we did not measure this"); ridge+HGB "with equal weights";
  "Results are in Table 2"; Tabelul 2 fara randul "Development run", caption scurt; TabFM: doar PCA
  768->394, fara T4/16 GB in text; de ce doi regresori (date diferite, erori partial diferite);
  SHAP fara explicatia metodei (pastrata in comentariu).
- 4.2: "Baseline" (textul lui neschimbat) + tabelul Claude mutat imediat dupa (acum Tabelul 3);
  captionuri scurte la Fig. 3, Tabelele 3, 4, 5; prompturile descrise concret (doar primul e "expert");
  gruparea explicata (2 si 3 devin o nota cu valoarea 2.5 si suma probabilitatilor).
- 4.3: paragraful de inceput rescris (A = predictia regresorilor, B = nota LLM-ului, medie ponderata).
Intrebari ramase la el: prima fraza din Baseline ("current foundation models") e a lui, neschimbata;
4.4 ramane in Results (recomandat), Related Work doar trimite la tabel.

## Unde am ramas inainte (11 oct seara, dupa runda 2 de review pe sectiunea 4)

.tex sha **40123c97**, compilat curat (0 erori, 0 Undefined, 0 `??`, 0 Overfull), 12 pagini. Backup-urile
(3c956929, 2da92e95, c95af23a, feeb18e1, d25d59c0) sunt in scratchpad-ul sesiunii ae42791d (`bak/`).
In Overleaf se urca doar .tex-ul. Urmeaza review-ul meu pe sectiunea 4, apoi pasul 4 (What Did Not Work).

Sectiunea 4 acum, in ordinea ceruta de mine (A, B, fuziune, publicate):
- Inceput: LOLO explicat (fara data leakage) si intervalele pereche; doua comparatii din dezvoltare.
- 4.1 Signal A. Tabel 1: encodere, cu corelatiile dintre ele (.870-.890) si cei doi regresori.
  Straturi: sweep de dezvoltare (`output/e_extractie.md`). Centrare = domain adaptation + Fig. 2 (t-SNE).
  Tabel 2: modelele de regresie, o coloana, fara matricea de corelatii; kNN scos (cifrele in comentariu);
  bloc separat "Development run" cu TabFM si controlul lui (XLM-R singur, PCA la 394 dimensiuni fiindca nu
  incapea pe T4 de 16 GB, 10 limbi, bratul multilingv): ridge+HGB .575/.680, TabFM .567/.678 (fuziunea
  rulata pe 11 oct din predictiile salvate, `output/e_fusion_lolo_doc_tabfm_alone_mf256.md`), ridge+TabFM
  .579/.681. Ridge/HGB cu ponderi egale. Regresorul englez vs multilingv. Trasaturi (motiv prin RALS) +
  Fig. 3 (SHAP, mutata pe pagina textului). Tabelul SHAP e scos, cifrele raman in text.
- 4.2 Signal B. Paragraful meu despre Claude (neschimbat). Tabel 3: LLM-uri (trial pentru 5 modele, test
  pentru Gemma/Qwen3.5/Qwen3 cu aceeasi citire, corelatii; Gemma ingrosat; Llama si Aya cu "--" pe test).
  Paragraful meu despre Qwen (neschimbat). Tabel 4: prompturi (cu corelatiile dintre ele), T fix, fara grupare.
- 4.3 Fusion. Cum se face, setarile alese, Tabel 5 (pe limba), Tabel 6 (A--B si Ridge--HGB pe limba),
  Tabel 7 (semnale, Claude, randurile "Signal A + Claude Sonnet/Opus" cu "--").
- 4.4 Comparatia cu rezultatele publicate (Tabel 8), neschimbata.

In asteptare:
- Llama 3.1 8B si Aya Expanse 8B pe test: le rulez intr-o sesiune separata cu `docs/PROMPT_rulare_llm_test.md`
  (iesire `output/doc_llm_extra.txt`); apoi se completeaza randurile lor din Tabelul 3.
- Claude: refac eu predictiile; apoi se completeaza cele doua "--" din Tabelul 7.

De decis de mine:
- Data (Method) spune "We do not use its trial split", dar Tabelul 3 foloseste trial-ul. Se schimba fraza
  din Method (aprobat) sau se scoate coloana Trial.
- Promptul Claude: .721 e varianta "5 + 100"; varianta doar 1-5 dadea .697.
- Motivul trasaturilor lexicale: scris prin baseline-ul RALS; de confirmat daca asta a fost motivul real.
- In Tabelul 1, "Plus XLM-R large" are cele mai mari cifre dar nu e ales; bold e doar pe metoda completa.
- Intrari bib lipsa: TabFM, LightGBM, XGBoost, CatBoost, ExtraTrees, RandomForest, Llama 3.1, Aya Expanse.
- Optional: TabFM pe metoda actuala (3 encodere, 11 limbi) pe Colab T4, ca sa fie comparabil direct.

Surse noi in sesiunea ae42791d: `analysis_doc_correlations.py` are partile 4 (ridge-HGB pe limba) si 5
(encodere), `output/doc_correlations.txt` refacut (partile 1-3 identice);
`output/e_fusion_lolo_doc_tabfm_alone_mf256.md` (fuse_ab.py pe predictiile TabFM salvate).

## Unde am ramas inainte (11 oct, dupa a doua RESTRUCTURARE a Results, ceruta de mine)

.tex sha **feeb18e1**, compilat curat, 12 pagini. Backup-urile (3c956929, 2da92e95, c95af23a) sunt in
scratchpad-ul sesiunii ae42791d (`bak/`). Sectiunea 4 are acum ordinea ceruta: 4.1 Signal A, 4.2 Signal B,
4.3 Fusion, 4.4 Published. Frazele mele (paragraful Claude, paragraful Qwen) sunt mutate, neschimbate.

- 4.1: la inceputul sectiunii, LOLO si intervalele pereche. Encodere (Tabel 1 cu corelatiile dintre
  encodere: .870-.890), straturi (sweep de dezvoltare `output/e_extractie.md`, XLM-R singur, 10 limbi,
  versiune veche: last4 .578, celelalte .569-.572, fuziunea < 0.002, intervale peste zero), centrare
  ca domain adaptation + t-SNE, cele 10 modele (Tabel 2), ridge/HGB cu ponderi egale, cei doi
  regresori, trasaturile (motivul scris prin baseline-ul RALS) + SHAP.
- 4.2: Claude, tabel LLM nou (Tabel 4: trial din `output/e_bakeoff.md` pentru Gemma, Qwen3.5, Qwen3,
  Llama 3.1, Aya Expanse; test pentru primele trei, aceeasi citire; corelatii), prompturi (Tabel 5,
  cu corelatiile dintre prompturi), T si grupare. Tabelul vechi de corelatii LLM/prompturi e scos.
- 4.3: cum se face fuziunea, setarile alese, Tabel 6 (per limba), Tabel 7 (A--B si Ridge--HGB pe
  limba), Tabel 8 (semnale + Claude + randurile "Signal A + Claude Sonnet/Opus" cu "--").
- `analysis_doc_correlations.py` are partile 4 (ridge-HGB pe limba) si 5 (encodere);
  `output/doc_correlations.txt` refacut, partile 1-3 identice.

De decis de mine:
- Predictiile Claude nu sunt pe Mac si nici in git; le refac eu, apoi se completeaza cele doua "--".
- Data (Method) spune "We do not use its trial split", dar tabelul LLM foloseste trial-ul. Trebuie
  schimbata fraza din Method (aprobat) sau scos trial-ul din tabel.
- Promptul Claude: .721 e varianta "5 + 100"; varianta doar 1-5 dadea .697.
- Motivul trasaturilor lexicale: e scris prin baseline-ul RALS; de confirmat daca asta a fost motivul real.

## Unde am ramas inainte (10 oct, 19:40, dupa RESTRUCTURAREA Results ceruta de mine)

Sectiunea 4 are acum 7 subsectiuni: 4.1 Per-Language (Tabel 1, cu coloana noua A--B = corelatia dintre
semnale pe limba, media .685), 4.2 Signals and Baselines (Tabel 2 doar cu Signal A, Signal B, Full method,
Claude Sonnet, Claude Opus), 4.3 Signal A (Tabel 3: encodere si regresori; Tabel 4: 10 modele de regresie
rulate pe 11 limbi + matricea de corelatie intre ele), 4.4 Signal B (Tabel 5: T, grupare, prompturi, Qwen;
Tabel 6: corelatii intre LLM-uri si intre prompturi), 4.5 Published (Tabel 7, 10 limbi), 4.6 SHAP, 4.7 t-SNE.
.tex sha **3c956929**, compilat curat, 11 pagini. Frazele mele (Qwen, paragraful Claude) neschimbate.

Surse noi:
- `analysis_doc_signal_a_models.py` (features / fit --model / report) -> `output/doc_signal_a_models/`
  (predictii pe model; feature-urile .npz sunt in .gitignore) si `output/doc_signal_a_models.txt`.
  Ridge+HGB reproduce exact release/predictions/signal_a.csv. XGBoost NU e in ml_def: a fost instalat
  doar in scratchpad (`--pylib`); pentru rerulare trebuie `pip install xgboost`.
- `analysis_doc_correlations.py` -> `output/doc_correlations.txt` (A--B pe limba, LLM-uri, prompturi).

Ramase:
- Fara citari pentru LightGBM, XGBoost, CatBoost, ExtraTrees, RandomForest (cer intrari noi in bib,
  in afara sectiunii 4).
- Comparatia cu paperurile publicate trebuie spusa si in Related Work (pasul 5), cerut de mine.
- Sonnet .685 pe 11 limbi, de confirmat (vezi mai jos).

## Unde am ramas inainte (10 oct seara, dupa REverificarea Results)

**A doua verificare a sectiunii 4 e FACUTA** (`docs/PROMPT_reverificare_results.md`, sesiunea 9baa9412).
Auditul n-a gasit nimic fals. Toate cifrele au fost recalculate, iar Tabelul 2 a fost refacut independent
(copii ale release/ cu setarile editate in fisier, 32 de rulari, bootstrap propriu): totul se potriveste.
Am aplicat doar schimbari de forma, cu "go" de la mine fara plan separat. Nou sha1 **9197668b**, compilat
curat (0 erori, 0 Undefined, 0 Overfull, 0 `??`), 10 pagini. Backup (sha 2283b75a) in scratchpad-ul
sesiunii 9baa9412 (`bak/`). Method neatins; frazele mele (Qwen, paragraful Claude) identice.
**Urmeaza review-ul meu manual pe sectiunea 4**, apoi pasul 4 (What Did Not Work).

Ce s-a schimbat la reverificare:
- 4.1: finalul fara lista de propozitii scurte (w si w_src in doua fraze); "Catalan has no such gap:
  3.6%"; "In the other nine languages with frequency data".
- 4.2: conventia "eleven languages, ten in parentheses"; ablatia definita; toate intervalele intr-o
  singura fraza (exceptii: XLM-R large pe 10, English regressor only, No grouping); paragrafele incep cu
  "For signal A / For signal B"; XLM-R large citat; "On average" scos; Gemma ales cu cifre (0.664 fata
  de 0.591, media r_B pe cele 10 limbi MLSP); B alone 0.094 / 0.025 pe 10 limbi adaugate.
- 4.3: fraza cu predictiile shared task-ului mutata in primul paragraf; "Ours is lower only on Catalan
  (by 0.021) and French (by 0.107)".
- 4.4: caption Fig. 2 (referinta si unitatea, spuse separat); indicatorii intr-o fraza; "partly cancel"
  devine "one encoder pushes signal A up while another pushes it down"; `\emph` consecvent pe cele
  patru nume; Sinhala fara a treia repetare a frecventei 0.
- 4.5: "same context" (nu "same sentence"); de ce lipim encoderele; share explicat concret, "If the
  neighbours were picked at random, it would be 0.11".

Dupa asta, tot pe 10 oct: Fig. 3 (t-SNE) refacuta cu fonturile dublate si legenda pe doua randuri, aceeasi
proiectie (`output/tsne_concat_fara_knn.py` editat). .tex sha **06bb0b0f** (doar comentariul figurii).
In Overleaf se urca .tex-ul SI `figures/fig_tsne_encoders.png`.

Tot 10 oct, Tabelul 2 micsorat la cererea mea: o singura coloana (11 limbi), fara randurile Signal A only /
Signal B only (sunt randul Mean din Tabelul 1), cu "Full method" ingrosat, caption mai scurt. In 4.2 a
ramas o singura cifra pe 10 limbi: castigul XLM-R large dispare pe cele 10 limbi MLSP. .tex sha **fecc91a3**.

Ramase, de confirmat de mine:
- Sonnet .685 pe 11 limbi. Sesiunea Claude confirma ca a notat toti cei 7211 itemi. Dar .685 [.671, .699]
  pe 11 limbi e identic, si ca valoare si ca interval, cu varianta "doar 0-100" pe 10 limbi (.6854
  [0.671, 0.699]), in timp ce Opus si Gemma au intervale diferite intre 10 si 11 limbi. Probabil e o eticheta
  gresita. De cerut randul pentru romana al variantei "5 + 100" (din tab_llm_frontier.tex).
- Pentru o fuziune cu Claude pe 11 limbi, fisierul nostru este `output/doc_fuse_ro11.csv` (0.692521), nu
  `fusion_preds_lolo_adoptat_m3k_ro11.csv` (cifra istorica 0.693718).
- Optional, in afara .tex: un `assert` pe 2000 de esantioane in `analysis_doc_ablations_extra.py`
  (azi nu exista niciun esantion degenerat, dar o trunchiere ar fi tacuta).

## Unde am ramas inainte (10 oct, dupa sesiunea de verificare Results)

**Method e APROBAT de mine.** Nu il mai schimbi decat daca iti cer eu.

**Sectiunea 4, Experimental Results, e VERIFICATA SI RESCRISA** (sesiunea din
`docs/PROMPT_verificare_results.md`: audit in chat, plan, "go"). Ultima versiune a .tex-ului: sha1
2283b75a, compilata curat (0 erori, 0 Undefined, 0 Overfull, 0 `??`), 10 pagini. Paginile 9-10 sunt
bibliografie si anexa, umflate de `\nocite{*}`. Backup-ul de dinainte (sha 110df127) e in scratchpad-ul
sesiunii bd5805f4 (`bak/`). Trebuie urcate in Overleaf .tex-ul SI `figures/fig_tsne_encoders.png`
(refacut fara titlul de sus, aceeasi proiectie, seed 0).

Ce s-a schimbat in sectiunea 4:
- 4.1: trei zecimale (0.693 [0.679, 0.706]); pe filipineza 26.7% din tinte au frecventa 0 (in loc de
  "fara leme"); gruparea nu se mai descrie a doua oara; deductiile "X, so Y" sparte.
- 4.2: Tabelul 2 are 8 randuri noi: English regressor only, Multilingual regressor only, Temperature
  fixed at 1, No grouping, Expert/Short/Marked prompt only, "Gemma 4, Qwen reading". Intervale
  bootstrap PERECHE pentru ablatii. Doua paragrafe noi (regresorii; partile lui B). La Qwen: "On
  average", Gemma citit ca Qwen (.681/.676), romana (Qwen3.5 mai bun, Gemma ales pe celelalte limbi).
  Paragraful Claude neschimbat.
- 4.3: 0.690 [0.675, 0.703]; "Every other method in Table 3"; fraza falsa despre predictii scoasa
  (shared task-ul publica predictiile participantilor si baseline-ului, Shardlow Sec. 8); garda Opus
  (Opus 0.711 e peste orice medie din Tabelul 3).
- 4.4: SHAP explicat pentru incepator; 0.31 fata de 0.12-0.13 lamurit (contributiile se anuleaza partial).
- 4.5: "target vectors" -> "target embeddings"; t-SNE explicat; vecinii explicati concret. Cifrele
  0.57/0.33/0.11 raman (reproduse exact pe 10 oct).

Sursa noua: `analysis_doc_ablations_extra.py` (radacina repo) -> `output/doc_ablations_extra.txt`.
Ruleaza logica din release/fuse.py pe predictiile stocate (fara modele noi), cu setarile schimbate pe
modul la rulare. Reproduce si randurile Qwen pe 11 limbi (cu `output/doc_qwen_ro_signal_b.csv`).
release/ e NEATINS, deci `fuse.py` din release nu are flag-uri pentru ablatiile noi.

Rezultate noi, de stiut pentru pasii urmatori:
- gruparea {1},{2,3},{4,5} NU misca fuziunea (+0.0001 [-0.0010, +0.0012] pe 11, -0.0009 pe 10), urca
  doar B cu 0.002; la T = 1 selectia pastreaza toate cele 5 note separate;
- regresorul multilingv NU misca fuziunea: doar regresorul englez da 0.6926 fata de 0.6925 (11);
  amestecul urca A cu 0.004-0.005;
- temperatura: -0.005 (11) / -0.008 (10) fara ea; un singur prompt: -0.006..-0.017 (11);
- XLM-R large: +0.0017 [+0.0005, +0.0030] pe 11 limbi, dar +0.0001 pe 10, si nu e adoptat.

Deschise, nerespunse de mine:
- release/ nu reproduce .622 / .661 si nici ablatiile noi. Le adaugam in release/ la pasul 8?
- What Did Not Work (pasul 4): gruparea si regresorul multilingv sunt deja in Tabelul 2; pasul 4 doar
  trimite la ele.

## Baseline-ul Claude, de stiut

- Sursa: `output/doc_claude_baseline.txt`, rezultatele lipite de mine dintr-o alta sesiune. Predictiile
  Claude nu sunt in repo, iar promptul exact nu e scris nicaieri.
- **Opus zero-shot e PESTE metoda noastra** (+0.028 pe 11 limbi, +0.021 pe 10). Fuziunea noastra cu Opus da
  0.724 pe 10 limbi (+0.013 peste Opus singur). Introducerea, abstractul si concluziile trebuie formulate
  tinand cont de asta: nu scriem ca suntem cei mai buni fara etichete.
- Combinatiile au fost calculate cu versiunea veche a predictiilor noastre (0.6900, fata de 0.6897 in
  release); am decis ca rezultatele conteaza, sunt in text cu un comentariu LaTeX despre asta.

## Ce citesti intai

- Memoria: `cerere-sesiune-documentatie` (punctul de reluare), `baseline-claude-opus-bate-sistemul`,
  `preferinte-de-scriitura-paper` (are regulile noi din 10 oct), `scrie-uman-nu-overexplain`,
  `raspunsuri-fara-diacritice-fara-tabele-md`, `noutate-si-precedente-lcp-multilingv`.
- .tex-ul intreg. Daca sha-ul difera de 2283b75a, imi spui intai ce s-a schimbat. Daca am editat eu,
  textul meu ramane cuvant cu cuvant.
- `docs/instructions_documentation.md`, pentru ce cere cursul.

## Stilul pe care il vreau (din review-urile de pe 10 oct)

- Propozitii simple si concrete. Spui direct ce am facut ("We use the grouping {1}, {2, 3}, {4, 5}"),
  apoi pe scurt de ce. Fara fraze in plus care nu aduc nimic.
- Fara trimiteri vagi ("as described below"): metoda concreta se spune pe loc.
- Fara deductii inlantuite de tipul "X, and Y, so Z"; faptele se spun separat.
- Expresii respinse: "To this end", "held out (in turn)", "unweighted", "Two adjustments follow",
  "neighbouring", "on their own", "complementary", "gold". Titlurile de pas: "Step 1: Embedding."
- Termenii din text sunt aceiasi ca in figuri si in tabele (de exemplu trasaturile cu numele din SHAP).
- Cand ceva e nou pentru un incepator (o biblioteca, un termen), il explici scurt la prima mentiune.

## Sursele cifrelor

- `output/doc_fuse_ro11.{txt,csv}`: 0.692521 [0.6789, 0.7057], n 7211. Cifra principala.
- `output/doc_fuse_mlsp10.{txt,csv}`: 0.689745 [0.6751, 0.7035], n 5624. Rularea fara romana.
- `output/doc_ablations.txt`: toate ablatiile din `release/fuse.py`.
- `output/doc_ablations_qwen_ro.txt`: cele doua Qwen pe 11 limbi (rulate pe 10 oct seara, in afara release/).
- `output/doc_claude_baseline.txt`: baseline-ul Claude.
- `output/doc_counts.txt`, `output/shap_signal_a_per_encoder_*.csv` si `figures/`.
- Nu se citeaza: 0.674946, 0.683849, 0.690001, 0.692527, 0.693718 si 0.687831.

## Reguli

- Langa fiecare cifra si fiecare detaliu de metoda, un comentariu LaTeX scurt cu sursa, in engleza.
- Nu atingi paper_full.tex, Paper/documentation_overleaf.tex sau release/. Nu faci git add si nici commit.
- Compilezi intr-un director gol din scratchpad (pdflatex, bibtex, pdflatex de doua ori) cu acl.sty si
  acl_natbib.bst din Paper/Articol_Multilingv plus figures/: 0 erori, 0 Undefined, 0 `??`, 0 Overfull.
- Inainte de orice modificare, backup al .tex-ului in scratchpad.
- In chat: romana, fara diacritice, fara tabele markdown.

## Ordinea ramasa

1. ~~Review-ul pe Experimental Results (sectiunea 4).~~ FACUT 10 oct, sha 2283b75a.
2. Pasul 4, What Did Not Work: lista intai in chat, ca s-o tai.
3. Pasul 5: Related Work FACUT si acceptat 11 oct (sha 1bc24478; fraza Claude scoasa la scurtare, cu acordul lui).
   Ramane Introduction. Verificarea RW: vezi "Next steps" sus. Related Work spune corect ce etichete
   foloseste fiecare sistem (corectia din 9 oct) si pomeneste baseline-ul Claude.
4. Pasul 6, Conclusions and Future Work, Limitations, Implementation. La Limitations sunt deja notate:
   efectul centrarii pe corelatie nu e masurat; testul nostru e release-ul curatat (5.624), cel publicat
   are 5.627; etichetele limbii testate ajung la ordinul doi (indirect effect); al treilea prompt ales pe
   test; setarile fixe (alpha, HGB, fereastra, straturi, encodere, prompturi) au fost fixate in
   dezvoltare, unele uitandu-ne la test; promptul/varianta Claude, daca au fost alese pe test;
   XLM-R large castiga pe 11 limbi (+0.0017, interval peste zero) dar nu e adoptat, fiindca alegerea
   s-a facut pe 10. La Implementation: timpii din release/README.md (0.36 s pe citire Gemma 4, ~2 h 10
   min pentru 21.633 de citiri; A ~7 min la prima rulare), ceruti de curs ("how long did ... take").
5. Pasul 7, Abstract si keywords.
6. Pasul 8, verificarea finala. Scoti `\nocite{*}`.
7. Pasul 9, autori si emailuri.

## Deschise, le intrebi la pasul unde apar

- Anexa: acum anexa A e "SHAP of All Inputs". Blocul din 10 oct din `PROMPT_sesiune_documentatie.md`
  propunea anexe pentru hiperparametri si pentru prompturile lui B (si ar putea intra promptul Claude).
- Data a ramas subsectiune in Method (Method e aprobat asa); propunerea din 10 oct cu Data ca sectiune
  separata si tabel de statistici per limba nu s-a aplicat. Intreaba doar daca e cazul.
- Predictiile si promptul Claude, pentru reproductibilitate.
- README-ul din release/ nu are "Known limitations", iar pasul 6 le cere.

La final, sau cand ramane putin context, actualizezi memoria `cerere-sesiune-documentatie` cu punctul
de reluare si rescrii fisierul asta.
