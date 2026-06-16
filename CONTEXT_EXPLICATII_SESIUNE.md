# Context pentru sesiunea de explicații — proiect predicție complexitate lexicală RO

> Scop: continui să explic proiectul în detaliu, tehnic, în română, pentru ca Mihai să-și scrie
> documentația de research (raport scris DE MÂNĂ — rapoartele generate cu LLM primesc 0.0).
> Fișierele-sursă de adevăr în folder: `README.md`, `SESSION_CONTEXT.md` (best 69.74, cel mai actual),
> `solutie_finala.py` (cod CPU, povestea A/B/C/D), `recompute_gpu.py` (XLM-R + RoLlama3).

## Unde am rămas în explicație

Parcurgem soluția semnal cu semnal. Predicția finală = fuziunea a 4 semnale independente, fără
nicio etichetă RO (distant supervision), apoi calibrare.

- **Semnal A (transfer cross-lingual) — EXPLICAT COMPLET.** XLM-RoBERTa-base frozen embeddează
  fiecare cuvânt-țintă în context (media ultimelor 4 straturi → media pe subcuvinte → 768D,
  centrat pe limbă) + 4 trăsături lexicale (zipf cu fix de lemă pe RO, lungime, silabe, majusculă)
  → vector 773D → blend Ridge(α=300) + HistGradientBoosting, antrenat separat pe CompLex EN (~8400)
  și MLSP romanic (~2800), predicțiile pe RO mediate 50/50. Discutat: tokenizare SentencePiece (NU BPE),
  `<s>`/`</s>` per secvență nu per cuvânt, separarea embedding vs cele 4 trăsături, SHAP (zipf domină),
  de ce frozen>fine-tuning, de ce base>large, de ce blend>OLS/Lasso (OLS 0.43, Ridge 0.49, blend 0.55).
- **Semnal B (nota LLM) — EXPLICAT COMPLET.** RoLlama3-8b-Instruct (4-bit) notează cuvântul-în-context
  pe 1-5. NU ia cifra: face 1 forward pass, citește probabilitățile tokenilor "1".."5" la ultima poziție,
  calculează valoarea așteptată E=Σ P(d)·d, mapează (E-1)/4 în [0,1], mediază pe 2 prompturi. Discutat:
  arhitectura decoder Llama (32 straturi, self-attention cauzal, RoPE, GQA, SwiGLU, RMSNorm), cum se
  calculează logits (stare ascunsă 4096D × LM head → ~128k scoruri → softmax), de ce doar ultima poziție.
- **Semnal C (surprisal) — URMĂTORUL DE EXPLICAT.** `-log P(cuvânt|context)`, mediat pe subcuvinte,
  din aceleași logits ca B dar citind probabilitatea cuvântului REAL (toate pozițiile, nu doar ultima).
  Independent de B (corr 0.068). De acoperit: pipeline complet, de ce e ortogonal pe nota B, teoria surprisal.
- **Semnal D (eye-tracking PCA) — DE EXPLICAT.** reading_effort = PC1 (SVD) al 8 metrici ET de efort
  standardizate din X_test.csv. De acoperit: ce metrici, de ce PCA, loadings, late vs early ET.
- **Fuziune + calibrare — schițat, de aprofundat.** s=0.6·A+0.4·B → +0.08·C → +0.20·D; calibrare
  clip(0.27+0.125·z(s),0,1). De aprofundat: de ce calibrarea e analitică (Pearson invariant la afin,
  R² maxim la mean/std reale), matematica exactă.

## PUNCT DE SALVAT PENTRU DOCUMENTAȚIE: de ce scară 1-5 și nu 1-100 (Semnal B)

Decizie de design justificată (de pus în raport, nu lăsată arbitrară). O scară mai grosieră (1-5)
dă un semnal mai bun decât 1-100, din patru motive:

1. **Granularitatea nu se pierde** — soft-read-ul (valoarea așteptată din probabilități) face semnalul
   deja continuu (0.37, 0.52, ...). 1-100 nu ar adăuga nimic la rezoluție; oricum standardizăm (z-score).
2. **Calibrare** — un LLM 8B distinge real ușor/mediu/greu (1-5), dar NU 63 vs 64 pe 1-100. Pe scară fină
   masa de probabilitate se împrăștie zgomotos, cu bias spre numere rotunde (50, 70, 100) = artefacte.
3. **Tokenizare (motivul tehnic decisiv)** — "1".."5" sunt tokeni unici → citești 5 probabilități curate
   la primul pas. "63"/"100" se sparg în mai mulți tokeni → P(secvență), mult mai complicat și zgomotos.
4. **Se potrivește cu datele sursă** — adnotările Complex 2.0 / Likert sunt tot pe scări mici (~1-5).

Rezumat: scară mică + citire probabilistică = stabilitatea unei scări pe care modelul o stăpânește
+ continuitatea necesară regresiei. Combinația optimă; nici 1-100-cifră, nici 1-5-cifră nu o bat.

## Stil de explicație (preferințe)

- Română, tehnic dar clar, concis (Mihai preferă răspunsuri directe, fără verbozitate inutilă).
- Corectează confuziile explicit când apar (am avut: tokeni speciali per cuvânt, embedding vs trăsături,
  lemma „pentru antrenament” — de fapt e doar pe RO, căutare cuvânt în datele EN — de fapt nu există).
- Folosește exemple concrete (cuvinte reale: „urmărire”, „Pământului”), scheme ASCII, cifre reale din cod.
- Confirmă ce a înțeles corect, apoi adaugă/nuanțează.

## Prompt de lipit la începutul sesiunii noi

"Continuăm explicarea proiectului meu de ML (predicție complexitate lexicală RO din folderul ăsta).
Citește README.md, SESSION_CONTEXT.md, solutie_finala.py și recompute_gpu.py ca să ai contextul, plus
CONTEXT_EXPLICATII_SESIUNE.md care zice unde am rămas. Am parcurs deja în detaliu Semnalul A și
Semnalul B. Vreau să continuăm cu Semnalul C (surprisal), apoi D (eye-tracking), apoi fuziunea +
calibrarea. Explică tehnic, în română, concis, cu exemple concrete — îmi scriu documentația de research
din asta."
