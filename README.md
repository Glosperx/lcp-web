# Predicția complexității lexicale în limba română

Proiect pentru competiția **unibuc/ia-cti-2026** (Nitro AI Judge). Pentru un cuvânt-țintă dintr-o
propoziție românească estimăm un scor de complexitate lexicală în intervalul `[0, 1]`, unde 0 înseamnă
foarte familiar și 1 foarte dificil.

Autori: Alexandru Cojoacă, Mihai-Alexandru Preoteasa.

Raportul complet (în engleză, format ACL) este în
`Cross-Lingual Transfer for Romanian Lexical Complexity Prediction.pdf`, cu sursa LaTeX în `report/`.

## Problema

Setul de antrenare conține doar 14 exemple românești etichetate, prea puține pentru a antrena un model
supervizat fără supraadaptare. De aceea nu antrenăm nimic pe etichetele românești; le folosim doar la
validare. În rest recurgem la supervizare distanță: transferăm cunoștințe despre complexitate din
resurse externe (limbi cu mii de cuvinte adnotate și un model de limbaj românesc) și din măsurătorile de
eye-tracking puse la dispoziție de competiție.

Metrica de evaluare combină corelația cu calitatea potrivirii: `score = 50 · (|r| + max(0, R²))`.

## Abordarea

Predicția finală este fuziunea a patru semnale independente, fiecare estimând complexitatea pe altă cale.

**A — Transfer cross-lingual.** Învățăm complexitatea din adnotări în engleză (CompLex) și în limbi
romanice (MLSP: fr/it/pt/es/ca) și o transferăm pe română prin XLM-RoBERTa-base, un model multilingv
care aduce cuvinte cu sens apropiat în același spațiu vectorial. Encoder-ul rămâne înghețat: peste
embedding (media ultimelor 4 straturi, centrată pe limbă) adăugăm câteva trăsături lexicale simple
(frecvență, lungime, silabe, majusculă), iar un regresor blend Ridge + HistGradientBoosting face
predicția. Cel mai important detaliu pentru română: pentru că limba e puternic flexionată, multe forme
lipsesc din lista de frecvențe și par fals rare, așa că folosim frecvența lemei când e mai mare decât a
formei. Acest fix singur aduce cel mai mare câștig.

**B — Notă de la un model de limbaj.** RoLlama3-8B (rulat local, cuantizat pe 4 biți) evaluează cuvântul
în context pe o scară 1–5. Nu citim cifra generată, ci valoarea așteptată din probabilitățile pe care
modelul le atribuie cifrelor 1…5 la următoarea poziție, ceea ce dă un scor continuu și mai stabil.

**C — Surprisal.** Cât de neașteptat e cuvântul în context, `−log P(cuvânt | context)`, calculat din
aceleași logits ca semnalul B. Fiind o statistică internă brută, e aproape independent de nota cerută
prin prompt (corelație 0.07), deci aduce informație nouă.

**D — Eye-tracking.** Cuvintele dificile rețin privirea mai mult și provoacă recitiri. Comprimăm cele 8
metrici de efort din eye-tracking într-un singur scor de „efort de citire” cu PCA; prima componentă
explică ~62% din varianță și toate metricile contribuie în aceeași direcție.

**Fuziune și calibrare.** Cele patru semnale trăiesc pe scări diferite, deci fiecare e normalizat
(z-score) și combinat printr-o medie ponderată, apoi adus la scara reală a scorurilor din test
(`clip(0.27 + 0.125 · z, 0, 1)`). Neavând etichete românești pe care să reglăm ponderile, le-am ales pe
scorul de pe leaderboard-ul public; curbele cresc și scad lin la variația fiecărei ponderi, semn că
semnalele sunt reale, nu zgomot. Ponderile efective rezultate: A 44%, B 29%, D 20%, C 6%.

## Rezultate

Tabelul construiește sistemul un semnal pe rând (scoruri pe leaderboard-ul public).

| Configurație | Scor | Δ |
|---|---|---|
| Predicție constantă (media) | 0.00 | — |
| Doar trăsături de suprafață (zero-shot RO) | 10.27 | +10.27 |
| + eye-tracking (fără resurse externe) | 41.76 | +31.49 |
| + cross-lingual A + LLM B | 64.52 | +22.76 |
| + surprisal C | 64.81 | +0.29 |
| + fix frecvență pe lemă (în A) | 68.90 | +4.09 |
| + eye-tracking PCA D | **69.74** | +0.84 |

Resursele externe explică aproximativ 87% din scorul final; suprafața singură ajunge la doar 41.76.
O analiză SHAP la nivel de trăsături pune frecvența pe primul loc, urmată de nota LLM și surprisal, iar
trăsăturile de suprafață contează aproape deloc.

## Ce nu a funcționat

Câteva direcții care păreau promițătoare dar nu au ajutat, raportate pe scurt pentru onestitate:

- **Fine-tuning XLM-RoBERTa** (full și LoRA): toate variantele au ieșit sub encoder-ul înghețat. Fără
  etichete românești, fine-tuning-ul supraadaptează limba-sursă și strică alinierea multilinguală pe
  care se bazează transferul.
- **Schimbarea encoder-ului** (e5, LaBSE) și **embedding din straturi intermediare**: câștigau la
  validarea in-source dar picau pe public, fiindcă validarea măsoară transferul engleză↔romanic, nu
  transferul către română.
- **Prompturi few-shot și chain-of-thought** pentru LLM: adăugau zgomot; la 8B parametri CoT încă nu
  ajută.
- **Trăsături suplimentare** (raritate, POS, entități, WordNet): redundante cu frecvența.

## Structura proiectului

```
solutie_finala.py / .ipynb   cod final (rulează pe CPU, citește semnalele din data/)
recompute_gpu.py             recalculează semnalele A/B/C de la zero (necesită GPU)
data/                         input competiție + semnalele cache (predicții, doar id+scor)
output/                       submisii generate, inclusiv cele 3 finale
report/                       sursa LaTeX a raportului (report.tex, custom.bib, figures/)
analysis_*.py, shap_*.py      analize și interpretabilitate (SHAP, studiu eye-tracking)
make_*figures.py             generarea figurilor din raport
```

Cele trei submisii finale (păstrate ca acoperire față de leaderboard-ul privat, care folosește un alt
split):

| Fișier | Scor public | Descriere |
|---|---|---|
| `output/et_pca_w20.csv` | 69.74 | patru semnale, eye-tracking agresiv |
| `output/et_pca_w10.csv` | 69.66 | patru semnale, eye-tracking moderat |
| `output/exp_lemmafreq.csv` | 68.90 | trei semnale, fără eye-tracking (cel mai sigur) |

## Cum se rulează

Calea rapidă reproduce rezultatul bit-exact din semnalele cache, pe CPU:

```bash
pip install torch transformers==4.46.3 scikit-learn scipy pandas numpy wordfreq
python solutie_finala.py        # citește data/, scrie submission.csv (patru semnale, 69.74)
```

Recalcularea semnalelor de la zero încarcă XLM-RoBERTa și RoLlama3-8B și are nevoie de GPU (~8 GB):

```bash
python recompute_gpu.py
```

`transformers` e fixat la 4.46.3 fiindcă versiunile 5.x dau segfault la încărcarea RoLlama3-8B în 4 biți
(bitsandbytes). O placă RTX 2070 SUPER de 8 GB e suficientă.

## Resurse externe

Toate sunt open-weights sau date publice/gated, rulate local, fără API-uri închise.

| Resursă | Rol |
|---|---|
| XLM-RoBERTa-base | embeddings contextuale multilingve (semnalul A) |
| RoLlama3-8B-Instruct (OpenLLM-Ro) | notă de complexitate 1–5 și surprisal (semnalele B, C) |
| CompLex (SemEval-2021 LCP) | adnotări de complexitate în engleză, transfer |
| MLSP / MultiLS 2024 | adnotări în limbi romanice, transfer |
| wordfreq | frecvență (scor Zipf) pentru română și engleză |

## Date

Repo-ul este privat, deci datele competiției pot fi versionate. `.gitignore` exclude datele MLSP (gated
pe HuggingFace, nu se redistribuie), CompLex (descărcabil din cod) și cache-ul mare de embeddings.
Predicțiile noastre din `data/` și `output/` rămân versionate pentru reproducere bit-exact.
