# Plan documentație — predicția complexității lexicale RO (echipa Sahistii)

> Schiță cu toate punctele de atins în raportul de research (ACL-style, scris DE MÂNĂ — LLM = 0.0).
> Fiecare liniuță se dezvoltă mai târziu. Best public = **69.74** (4 semnale), bază 3 semnale = **68.90**.

---

## 1. Introducere & motivație
- Task: predicția complexității lexicale (scor 0-1) a cuvintelor RO în context. Competiția UniBuc
  „Predicting lexical complexity from eye-tracking data" (Nitro AI Judge).
- Provocarea centrală: doar **14 exemple RO etichetate** → imposibil de antrenat supervizat fără supraadaptare.
- Soluția: **supervizare distanță (distant supervision)** — ZERO antrenare pe etichetele RO; transfer din
  resurse externe (EN + limbi romanice + LLM RO) + eye-tracking.
- Predicția finală = fuziunea a **4 semnale independente**, fiecare estimând complexitatea pe altă cale.

## 2. Task & date
- Set de test: 1587 cuvinte-țintă în context; coloane `text`, `token`, `lemma`, `datapointID`.
- Eye-tracking disponibil pentru 1509/1587 (95%), dar doar 2/14 cuvinte etichetate au ET.
- Metrica de evaluare: corelație Pearson (regresie) → **AUC/PRC NU se aplică** (de menționat explicit).
- Sursele externe de etichete: CompLex EN (~8400, SemEval-2021), MLSP romanic (~2800: fr/it/pt/es/ca).

## 3. Metoda — cele 4 semnale

### Semnal A — transfer cross-lingual
- XLM-RoBERTa-base **frozen**, media ultimelor 4 straturi → medie pe subcuvinte → vector 768D, centrat pe limbă.
- + 4 trăsături lexicale: frecvență zipf (cu fix de lemă pe RO), lungime, silabe, majusculă → vector 773D.
- Regresor = **blend Ridge(α=300) + HistGradientBoosting** (liniar + neliniar, regularizare mare = transfer fragil).
- Antrenat separat pe CompLex EN și MLSP romanic; predicțiile pe RO mediate 50/50 (ansamblu z-score).
- De dezvoltat: tokenizare SentencePiece (NU BPE), `<s>`/`</s>` per secvență, separarea embedding vs trăsături.
- De ce frozen > fine-tuning, base > large, blend > OLS/Lasso (OLS 0.43, Ridge 0.49, blend 0.55 pe free-gate).

### Semnal B — nota LLM
- RoLlama3-8b-Instruct (4-bit) notează cuvântul-în-context pe scara **1-5**.
- NU ia cifra generată: 1 forward pass, citește probabilitățile tokenilor „1".."5" la ultima poziție,
  calculează valoarea așteptată E = Σ P(d)·d, mapează (E-1)/4 în [0,1], mediază pe 2 prompturi.
- De dezvoltat: arhitectura decoder Llama (32 straturi, self-attention cauzal, RoPE, GQA, SwiGLU, RMSNorm),
  cum se calculează logits (stare ascunsă 4096D × LM head → ~128k scoruri → softmax), de ce doar ultima poziție.
- **Decizie de design: de ce scară 1-5 și nu 1-100** (4 motive — vezi secțiunea dedicată mai jos).

### Semnal C — surprisal
- `surprisal(w) = -log P(cuvânt | context)`, mediat pe subcuvinte. Din aceleași logits ca B, dar citind
  probabilitatea cuvântului **REAL** (toate pozițiile, nu doar ultima).
- Cheia tehnică: deplasarea `i-1` (decoder cauzal prezice tokenul i din contextul 0..i-1):
  `surprisal = mean_i( -lp[i-1, ids[i]] )`.
- Mediere pe subcuvinte (`/ len(tgt)`) = normalizare pe lungime, nu pe conținut.
- **Independent de B** (corr 0.068): B = opinie cerută prin prompt; C = statistică brută internă.
- Intuiție ortogonalitate: cuvinte frecvente dar surprinzătoare în context (Luna/COST/Cartea, capitalizate /
  început de propoziție) → B mic, C mare.
- Teoria surprisal-ului (Hale 2001, Levy 2008): efortul de procesare ∝ surprisal.
- Pondere mică (0.08) dar reală: sweep public w0=64.52, **w0.08=64.81 (vârf)**, w0.20=63.84.

### Semnal D — eye-tracking (PCA)
- `reading_effort` = **PC1 (SVD)** al 8 metrici ET de efort standardizate (TFT/FFD/FPRT/RRT/TFC/FPFC/TRC_in/RPD_inc).
- PC1 explică ~62% varianță, acoperire 1509/1587; ponderea per metrică = loadings PC1 (nu aleasă manual).
- Cuvintele fără ET (~78) primesc efortul median.

#### D.1 — De unde vin metricile ET (sursa datelor)
- ET-ul e **input dat de competiție**, NU output. Numele competiției: „predicting complexity FROM eye-tracking".
  Folosirea lui ca semnal e legitimă, nu leakage.
- Sursa brută: `data/train_et.csv` (585.573 rânduri, 95 participanți, 10 texte). Fiecare rând = UN cititor ×
  UN cuvânt la o poziție (`participant_id`, `text_name`, `word_idx`, + metrici brute TFT/FFD/...).
- Agregare: pentru fiecare (text, poziție-cuvânt) → **media peste cei ~95 participanți** → `TFT_mean` etc.,
  apoi normalizare z → `TFT_mean_norm`. NU e join pe șirul cuvântului (nu „media lui «laptele» oriunde"),
  ci pe **poziție** — același cuvânt în propoziții diferite are ET diferit (complexitate per cuvânt-în-context).
- 10/12 texte de test sunt în experimentul ET → ET-ul cuvintelor de test = măsurători reale ale acelor
  cuvinte, mediate peste cititori. Cele 2 texte fără ET → ~78 cuvinte cu `has_et_features=0` → median fill.
- Aliniere finală: `X_test.csv` (1587 rânduri, unite pe `datapointID` cu `test_set.csv`).

#### D.2 — Selecția celor 8 metrici (manuală, ÎNAINTE de PCA)
- Din ~22 metrici ET brute am păstrat 8. Criteriul: **corelația fiecărei metrici cu ținta-proxy**
  (predicția-best 68.90, fiindcă n-avem etichete RO). Tabel în `et_metric_eval.csv`.
- Notă onestă: proxy-ul e parțial circular → folosit DOAR pentru selecție grosieră (păstrez/arunc),
  NU pentru ponderi. Pragul e brutal (TFT 0.63 vs SL 0.003), circularitatea nu poate inventa asta.
- Tăieri: (1) zgomot ~0 → afară (LP 0.022, SL_in 0.003, SL_out −0.049, RPD_exc 0.076 = saccade/landing,
  mecanică, nu dificultate); (2) redundante → afară (FRT/RBRT/FPRT duplică TFT); (3) efort real → înăuntru.

#### D.3 — Cum funcționează PCA și de unde ies ponderile
- PCA **nu alege** feature-uri; le folosește pe toate 8 și le **cântărește**. De-aia selecția manuală contează
  (zgomot în PCA distorsionează PC1).
- Pași: (1) standardizare (medie 0, σ=1, ca metricile în unități diferite să fie comparabile); (2) matricea
  de covarianță 8×8 (cât se mișcă împreună perechile); (3) direcția de varianță maximă = vectorul propriu cu
  valoarea proprie cea mai mare (în cod: `Vt[0]` din SVD); (4) loadings = componentele acelei axe = ponderile.
- Geometric: norul de puncte e o elipsă; PC1 = axa lungă; ponderea unui feature = **cosinusul unghiului**
  dintre PC1 și axa feature-ului. Pentru date standardizate, loading = corr(feature, PC1).
- Exemplu numeric real (2 metrici): corr(TFT,TFC)=0.955 → PC1 la 45° → w_TFT=w_TFC=0.707, PC1 explică 98%.
  Vector unitar (`w_TFT² + w_TFC² = 1`).
- Scorul per cuvânt = proiecție (produs scalar): `reading_effort = Σ wᵢ·z(metricᵢ)` (în cod `pc1 = Z @ w`).
  Ex: z(TFT)=0.91, z(TFC)=0.73 → 0.707·0.91 + 0.707·0.73 = 1.158.
- Loadings PC1 reale (8 metrici): TFT +0.438, TFC +0.426, FPRT +0.417, FPFC +0.388, RRT +0.355, FFD +0.290,
  RPD_inc +0.276, TRC_in +0.127. **Toate pozitive** → axă curată „mai mult efort = mai complex".
- Important: PCA e **nesupervizat** — nu vede niciodată complexitatea. Scoate **efortul** (axa de variație
  dominantă); legătura efort↔complexitate e asumpția noastră teoretică, validată de lift-ul public.
- Fixarea semnului: SVD poate întoarce −PC1; forțăm ca TFT mare → scor mare (`if w[TFT]<0: w=-w`).

#### D.4 — ET timpuriu vs târziu (legătura cu surprisal)
- **ET timpuriu** (FFD/FPRT/skip) = acces lexical, corr controlat ≈ 0.01 (= pură frecvență, dublează A).
- **ET târziu** (RRT/RPD/recitiri) = integrare în context, corr controlat = 0.243, corr cu surprisal = 0.177.
- → ET aduce ceva PESTE A+B+C: late ET = dificultate de integrare, parțial ortogonal. Închide cercul cu
  paperul GAZE4NLP (surprisal → TFT, fix metrica dominantă la noi).

#### D.5 — PCA vs sumă manuală
- Varianta manuală (`et_complexity_proxy`, ponderi din literatură) dă practic același rezultat: corr 0.97.
- Am păstrat PCA fiindcă ponderile vin din date, nu din alegeri subiective. Defensabil.

## 4. Fuziune & calibrare
- Fuziune **imbricată** (nested), nu plată. Pași cu formulele din cod:
  - Pas 1 (bază A+B):   `s = 0.60·z(A) + 0.40·z(B)`
  - Pas 2 (+surprisal): `s = 0.92·z(s) + 0.08·z(C)`   ← aici = 68.90
  - Pas 3 (+eye-track): `s = 0.80·z(s) + 0.20·z(D)`   ← aici = 69.74
  - Constante: `W_CL=0.6, W_LLM=0.4, W_SURP=0.08, W_ET=0.20`.
- De ce z-score peste tot: semnalele sunt în unități incompatibile (A = predicție regresie, C = -log P în nați,
  D = proiecție PCA) → standardizarea le aduce pe aceeași scară ca să fie amestecabile cu ponderi.
- Calibrare analitică: `clip(0.27 + 0.125·z(s), 0, 1)` (media/abaterea reale ale testului).
- De dezvoltat: de ce calibrarea e analitică — Pearson invariant la transformări afine, R² maxim la mean/std reale.
- Sweep ET public: w0=68.90, w0.10=69.66, **w0.20=69.74 (vârf)**, w0.30=69.00 (unimodal).

## 4b. Ponderile finale & cum le-am ales (secțiune dedicată)

### Ponderile efective per semnal (imbricarea desfăcută)
```
A (cross-lingual): 0.80 · 0.92 · 0.60 = 0.44   (44%)
B (nota LLM):      0.80 · 0.92 · 0.40 = 0.29   (29%)
D (eye-tracking):                       0.20   (20%)
C (surprisal):     0.80 · 0.08        = 0.06   (6%)
                                        = 1.00
```
- Aproximativ (z() dintre pași re-standardizează), dar astea sunt ponderile nominale: **A 44 / B 29 / D 20 / C 6**.

### Cum am validat că sunt bune — sweep pe leaderboard public
- Singura supervizare reală pe RO: NU pe etichete (cele 14 nu prezic), ci pe scorul public.
- Pentru fiecare pondere am încercat mai multe valori → vârf clar, curbe **unimodale și netede**
  (zgomotul ar da curbe zimțate; netezimea = semnal real):
  - W_ET:   0→68.90, 0.10→69.66, **0.20→69.74**, 0.30→69.00
  - W_SURP: 0→64.52, **0.08→64.81**, 0.12→64.71, 0.20→63.84
- Ordinea corectă: **leaderboard-ul ALEGE ponderile → SHAP DESCRIE ce a ieșit.** Nu invers.

### De ce SHAP NU a ales ponderile (corecție importantă)
- Am rulat SHAP pe semnale (`shap_et.py`): mean|SHAP| A 0.061 > B 0.034 > D 0.017 > C 0.006. DESCRIPTIV.
- SHAP nu poate alege ponderea: (1) n-avem țintă RO (cele 14 nu prezic, ET are 2/14); (2) e circular —
  SHAP pe propria predicție, iar importanța lui D scalează cu W_ET pe care NOI l-am ales; (3) descrie modelul
  final, nu îl proiectează.

### Overfit pe public? — hedge onest
- Nu știm complet (public ≠ privat). Argumente că ponderile sunt reale: curbe unimodale netede; ET trecut prin
  test direct pe public (nu gate fals-pozitiv ca e5/mid/lasso).
- Strategie finale (3 submisii): F1 `et_pca_w20` (69.74, ET agresiv), F2 `et_pca_w10` (69.66, moderat),
  F3 `exp_lemmafreq` (68.90, fără ET, sigur). Dacă ET e overfit public, F3 protejează pe privat.

## 5. Experimente & rezultate (tabel ablație)
- cross-lingual + LLM: **64.52**
- + surprisal: **64.81** (+0.29)
- + lemma-freq (fără surprisal): **68.645** (+4.13, cel mai mare câștig)
- + lemma + surprisal (3 semnale): **68.90**
- + ET PCA blend w0.20 (4 semnale, NEW BEST): **69.74** (+0.84)
- Concluzie: lemma = gigantul; surprisal mic dar real; ET-blend mic dar real.

## 6. Câștigul-cheie: frecvența cu lemă (SHAP-driven)
- RO puternic flexionat → 186/1587 forme OOV în wordfreq (zipf=0) → tratate fals ca super-rare.
- Fix: `max(zipf(formă), zipf(lemă))`. 60 forme reparate, 360 cu frecvență mai mare a lemei.
- corr(token-zipf, lemma-zipf) = 0.75; A schimbat pentru 1380 cuvinte. Public 64.52 → 68.90.

## 7. Analiză & interpretabilitate
- **SHAP** (`analysis_shap.py`, `shap_beeswarm.py`): frecvența DOMINĂ (perm 0.4536), apoi embedding, lungime ~0.
  La nivel de semnal (4 semnale, w0.20): A 0.061 > B 0.034 > D 0.017 > C 0.006.
- **Studiul ET** (`analysis_et.py`): ET timpuriu controlat ≈ frecvență (0.0103); ET târziu controlat = 0.2430
  → aliniat cu surprisal (teoria surprisal). Rayner 1998 pentru conceptul ET.
- **Baseline-uri fără resurse externe** (ablație raport):
  - constant 0.27 (floor analitic) ≈ 0
  - surface-only (7 trăsături de suprafață, Ridge zero-shot RO): **10.27** (r~0.175)
  - ET + surface self-sup: **41.76** (r~0.542)
  - full (4 semnale): **69.74**
  - → **lift resurse externe = ~87% din scor**; suprafața singură ~13%.

## 8. Rezultate negative (de raportat onest)
- Fine-tuning XLM-R (full + LoRA): TOATE < frozen (frozen 0.5148 vs best FT 0.4618). Cauză: fără etichete RO,
  FT supraadaptează limba-sursă, degradează alinierea multilinguală pe care frozen o exploatează.
- Encoder swap (e5/LaBSE): câștig pe free-gate dar PICĂ public (e5 0.5855 gate → 63.00 public).
- Mid-layer embeddings: gate win → 64.49 public.
- Lasso/ElasticNet regressor: gate 0.5688 → 64.28 public.
- → **3 gate fals-pozitivi** (e5, mid, lasso): free-gate-ul EN↔Romanic supra-recompensează transferul între
  limbile lui dar pică pe →RO. Lecție metodologică pentru raport.
- LLM prompt: few-shot / CoT / self-consistency CoT — toate < zeroshot (8B sub pragul de emergență CoT).
- Raritatea (-zipf) ca semnal separat: redundantă cu A (corr 0.936).
- POS/dep/morfologie spaCy + RoWordNet: toate redundante cu frecvența (controlat < 0.08).

## 9. Decizie de design: de ce scară 1-5 și nu 1-100 (Semnal B)
1. Granularitatea nu se pierde — soft-read-ul face semnalul deja continuu; oricum standardizăm.
2. Calibrare — un LLM 8B distinge ușor/mediu/greu (1-5), dar nu 63 vs 64; pe scară fină bias spre numere rotunde.
3. Tokenizare (motivul decisiv) — „1".."5" sunt tokeni unici → 5 probabilități curate; „63"/„100" se sparg.
4. Se potrivește cu datele sursă — adnotările Complex 2.0 / Likert sunt pe scări mici (~1-5).

## 10. Concluzii & selecția finalelor
- HEDGE pentru leaderboard privat (public ≠ privat): F1 `et_pca_w20.csv` (69.74), F2 `et_pca_w10.csv` (69.66),
  F3 `exp_lemmafreq.csv` (68.90, fără ET, sigur).
- Credit idei: Sergiu Nisioi (embedding + features), Stefan (frecvență; complexitate ≠ dificultate).

---

## Referințe & link-uri (paper-e)

### Surprisal din LM → eye-tracking (lucrare-soră, limbă romanică)
- **Benchmarking Language Model Surprisal for Eye-Tracking Predictions in Brazilian Portuguese**
  (GAZE4NLP 2025). Task aproape identic: surprisal LM → metrici ET; efect cel mai puternic pe TFT (= top
  la noi); efect liniar; limbă romanică → transferabil ca argument spre RO.
  https://aclanthology.org/2025.gaze4nlp-1.2.pdf

### Teoria surprisal-ului (de ce surprisal = dificultate de procesare)
- **Lexical surprisal as a general predictor of reading time** (Mitchell et al., EACL 2009).
  https://dl.acm.org/doi/10.5555/2380816.2380866
- Hale 2001 (parser surprisal); Levy 2008 (expectation-based comprehension). [de adăugat citările exacte]

### Eye-tracking (conceptul, NU pentru ponderi — heuristic)
- Rayner 1998, „Eye movements in reading and information processing" (DOI 10.1037/0033-2909.124.3.372).

### De căutat / de completat
- [ ] Paper XLM-RoBERTa (Conneau et al. 2020) — pentru Semnal A.
- [ ] Paper CompLex / SemEval-2021 Task 1 (Shardlow et al.) — sursa EN.
- [ ] Paper MLSP shared task — sursa romanică.
- [ ] RoLlama3 (OpenLLM-Ro) — citarea modelului.
- [ ] SHAP (Lundberg & Lee 2017).
- [ ] BibTeX / DOI pentru GAZE4NLP 2025 (de extras pentru `custom.bib`).

---

## Figuri de pus în raport (`make_figures.py`, `output/raport/`)
- Tabel ablație (cele 5 trepte 64.52 → 69.74).
- Curba surprisal (sweep w) + curba ET (sweep w).
- Corelații ET (timpuriu vs târziu, controlat).
- 2 figuri SHAP (`output/shap/`): bar + beeswarm la nivel de semnal.
