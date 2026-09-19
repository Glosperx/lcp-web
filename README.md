# Predictia complexitatii lexicale in limba romana

Proiect pentru competitia **unibuc/ia-cti-2026** (Nitro AI Judge). Pentru un cuvant-tinta dintr-o
propozitie romaneasca estimam un scor de complexitate lexicala in `[0, 1]` (0 = familiar, 1 = dificil).

Autori: Alexandru Cojoaca, Mihai-Alexandru Preoteasa.
Raportul complet (engleza, format ACL): `docs/papers/Cross-Lingual Transfer for Romanian Lexical Complexity Prediction.pdf`, sursa LaTeX in `report/`.

## Problema

Setul de antrenare are doar 14 exemple romanesti etichetate, prea putine pentru un model supervizat.
Nu antrenam nimic pe ele; le folosim doar la validare. In rest folosim supervizare distanta: transferam
cunostinte din resurse externe (limbi cu mii de cuvinte adnotate, un model de limbaj romanesc) si din
masuratorile de eye-tracking date de competitie. Metrica: `score = 50 * (|r| + max(0, R2))`.

## Abordarea

Predictia finala fuzioneaza patru semnale independente:

- **A - transfer cross-lingual.** XLM-RoBERTa-base inghetat aduce engleza, romana si limbile romanice in
  acelasi spatiu. Peste embedding (media ultimelor 4 straturi, centrata pe limba) adaugam cateva trasaturi
  lexicale (frecventa, lungime, silabe, majuscula), iar un blend Ridge + HistGradientBoosting, antrenat pe
  CompLex EN si MLSP romanic, prezice pe romana. Detaliul decisiv: romana fiind flexionata, multe forme
  lipsesc din lista de frecvente si par fals rare, deci folosim frecventa lemei cand e mai mare. Acest fix
  aduce cel mai mare castig.
- **B - nota LLM.** RoLlama3-8B (local, 4 biti) evalueaza cuvantul in context pe scara 1-5. Citim valoarea
  asteptata din probabilitatile cifrelor 1...5, nu cifra generata - scor continuu si stabil.
- **C - surprisal.** `-log P(cuvant | context)`, din aceleasi logits ca B. Fiind statistica bruta, e
  aproape independent de nota B (corelatie 0.07), deci aduce informatie noua.
- **D - eye-tracking.** Comprimam cele 8 metrici de efort intr-un scor de citire cu PCA; prima componenta
  explica ~62% din varianta, toate metricile contribuie in aceeasi directie.

Semnalele sunt normalizate (z-score), combinate prin medie ponderata si calibrate la scara reala a
testului (`clip(0.27 + 0.125 * z, 0, 1)`). Neavand etichete romanesti, ponderile au fost alese pe scorul
public; curbele cresc si scad lin, semn ca semnalele sunt reale. Ponderi efective: A 44%, B 29%, D 20%, C 6%.

## Rezultate

Scoruri pe leaderboard-ul public, un semnal pe rand:

| Configuratie | Scor | Delta |
|---|---|---|
| Predictie constanta (media) | 0.00 | - |
| Doar trasaturi de suprafata (zero-shot RO) | 10.27 | +10.27 |
| + eye-tracking (fara resurse externe) | 41.76 | +31.49 |
| + cross-lingual A + LLM B | 64.52 | +22.76 |
| + surprisal C | 64.81 | +0.29 |
| + fix frecventa pe lema (in A) | 68.90 | +4.09 |
| + eye-tracking PCA D | **69.74** | +0.84 |

Resursele externe explica ~87% din scorul final. SHAP pune frecventa pe primul loc, apoi nota LLM si
surprisal; trasaturile de suprafata conteaza aproape deloc.

## Ce nu a functionat

- **Fine-tuning XLM-RoBERTa** (full si LoRA): toate sub encoder-ul inghetat - fara etichete RO, FT
  supraadapteaza limba-sursa si strica alinierea multilinguala.
- **Schimbarea encoder-ului** (e5, LaBSE) si **straturi intermediare**: castigau la validarea in-source dar
  picau pe public (in-source masoara transferul EN-romanic, nu spre RO).
- **Few-shot si chain-of-thought**: zgomot; la 8B, CoT inca nu ajuta.
- **Trasaturi suplimentare** (raritate, POS, entitati, WordNet): redundante cu frecventa.

## Structura

```
solutie_finala.py            cod final (CPU, citeste semnalele din data/); varianta notebook in notebooks/
recompute_gpu.py             recalculeaza semnalele A/B/C de la zero (GPU)
data/                        input competitie + semnalele cache
output/                      submisii generate, inclusiv cele 3 finale
report/                      sursa LaTeX a raportului (report.tex, custom.bib, figures/)
Paper/                       sursa articolului ACL/MRL (paper_full.tex si derivate)
analysis_*.py, shap_*.py     analize si interpretabilitate
make_*figures.py             generarea figurilor din raport
docs/                        documentatie, prompturi de sesiune, PDF-uri de referinta (docs/papers/)
logs/                        loguri de rulare arhivate
notebooks/                   notebook-uri (.ipynb)
legacy/                      artefacte din solutia initiala (source_code.zip)
```

Cele 3 submisii finale (acoperire fata de leaderboard-ul privat, cu alt split):

| Fisier | Scor | Descriere |
|---|---|---|
| `output/et_pca_w20.csv` | 69.74 | patru semnale, eye-tracking agresiv |
| `output/et_pca_w10.csv` | 69.66 | patru semnale, eye-tracking moderat |
| `output/exp_lemmafreq.csv` | 68.90 | trei semnale, fara eye-tracking (cel mai sigur) |

## Cum se ruleaza

Calea rapida reproduce rezultatul bit-exact din cache, pe CPU:

```bash
pip install torch transformers==4.46.3 scikit-learn scipy pandas numpy wordfreq
python solutie_finala.py        # scrie submission.csv (patru semnale, 69.74)
```

Recalcularea de la zero incarca XLM-RoBERTa si RoLlama3-8B si cere GPU (~8 GB): `python recompute_gpu.py`.
`transformers` e fixat la 4.46.3 (5.x da segfault la RoLlama3-8B in 4 biti). O RTX 2070 SUPER 8 GB ajunge.

## Resurse externe

Toate open-weights sau date publice/gated, rulate local, fara API-uri inchise: XLM-RoBERTa-base
(embeddings, semnal A), RoLlama3-8B-Instruct (nota si surprisal, B/C), CompLex SemEval-2021 (transfer EN),
MLSP/MultiLS 2024 (transfer romanic), wordfreq (frecventa zipf).

## Date

Repo privat, deci datele competitiei pot fi versionate. `.gitignore` exclude MLSP (gated pe HuggingFace),
CompLex (descarcabil din cod) si cache-ul mare de embeddings. Predictiile din `data/` si `output/` raman
versionate pentru reproducere bit-exact.
