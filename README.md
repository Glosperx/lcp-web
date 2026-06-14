# Predictia complexitatii lexicale in limba romana

Proiect pentru competitia **unibuc/ia-cti-2026** (Nitro AI Judge): dat un cuvant tinta intr-o
propozitie romaneasca, prezice un scor de complexitate lexicala in intervalul **[0, 1]**
(0 = foarte familiar, 1 = foarte dificil).

> **Nota pentru o sesiune Claude noua (alt laptop):** acest README + folderul de memorie
> (`~/.claude/projects/.../memory/`: `pred-eye-project.md`, `pred-eye-findings.md`, `env-setup.md`)
> contin tot contextul. Citeste-le intai. Codul final e un singur fisier: `solution_bert.py`.

---

## 1. Problema & competitia

- **Task:** regresie, scor complexitate in [0,1] per cuvant-in-context.
- **Metrica:** `score = 50*(|Pearson| + max(0, R2))`. Practic `score ~ 50*(r + r2)`, deci
  recuperezi `r` dintr-un scor: `r = (-1 + sqrt(1 + 4*score/50)) / 2`.
- **Date oferite:** doar **14 exemple etichetate** (din enunt) + metrici de **eye-tracking** (ET)
  pe ~3400 cuvinte. Test = **1587** cuvinte.
- **Output CSV:** coloane `subtaskID` (=1), `datapointID`, `answer`.
- **Submisii:** max 50; alegi **3 finale** (N<4). Nota finala = **leaderboard PRIVAT** (alt split,
  "cu mult diferit" de public) -> conteaza **generalizarea**, nu overfit pe public.
- **Etichetele** sunt facute cu metodologia **Complex 2.0** (= SemEval-2021 LCP) -> exista seturi EN
  cu aceeasi metodologie, utile pentru transfer.

---

## 2. Solutia finala (pipeline)

**Idee centrala: supervizare distanta din 2 surse independente. Zero antrenare pe etichetele RO.**
(Cu doar 14 etichete, orice antrenare directa = overfit.)

```
Semnal A - CROSS-LINGUAL ENSEMBLE (transfer zero-shot prin XLM-R)
  CompLex EN   (~8400 cuvinte engleze, complexitate Likert)   --\ XLM-R embed + lexical
  MLSP Romance (~2800 cuvinte fr/it/pt/es/ca, Likert)          --/ -> Ridge+HGB -> predictie RO
       (doi regresori separati, predictiile lor pe RO mediate 50/50 dupa z-score)

Semnal B - LLM-DIRECT
  RoLlama3-8b-Instruct (open-weights 8B, rulat local) noteaza fiecare cuvant 1-5
  in context; scor = valoarea asteptata din probabilitatile token-ilor "1".."5" -> [0,1]

FUZIUNE:   scor = 0.6 * z(A) + 0.4 * z(B)
CALIBRARE: answer = clip(0.27 + 0.125 * z(scor), 0, 1)
```

Detalii:
- **XLM-RoBERTa-base** pune EN/RO/limbi romanice in acelasi spatiu vectorial -> un regresor antrenat
  pe alte limbi se aplica zero-shot pe romana. Embedding = media subword pe ultimele 4 layere,
  centrat pe media limbii (scoate offsetul de limba).
- **Trasaturi lexicale** (pe langa embedding): `zipf` (wordfreq), lungime, nr. silabe, majuscula.
- **Regresor** = blend (medie) **Ridge** (liniar, regularizat L2 alpha=300) + **HistGradientBoosting**
  (arbori, neliniar). Mediati pentru robustete.
- **LLM** citeste direct distributia de probabilitate peste cifrele 1-5 (un singur forward pass,
  denoised), mediind 2 formulari de prompt.
- **Calibrare** (0.27 / 0.125) = media si deviatia reala a scorurilor de test, derivate prin probing
  pe leaderboard-ul public (vezi `pred-eye-findings.md`).

ATENTIE (pentru oral/raport): solutia finala **NU foloseste eye-tracking**. ET era folosit
doar in pasul de distilare, care a fost eliminat (vezi mai jos). Concluzie: supervizarea distanta
(transfer + LLM) bate semnalul comportamental ET pe acest task.

---

## 3. Scoruri (traiectorie public)

| Etapa | Public | Note |
|-------|--------|------|
| ET proxy + zipf (baseline non-BERT) | ~40 | overfit pe 14, semnal slab |
| ensemble cross-lingual EN + ET + zipf | 56.33 | primul salt (transfer CompLex) |
| wA = EN cross-lingual + LLM + distilare | 63.16 | r~0.730 |
| B1 = RO (MLSP) cross-lingual + LLM + distilare | 63.67 | romanic > englez |
| b2 = ensemble EN+RO + LLM + distilare | 64.41 | ensemble bate ambele |
| **best = ensemble EN+RO + LLM, FARA distilare** | **64.52** | **r~0.741, solutia finala** |

---

## 4. Ce am incercat (jurnal experimente)

**Au functionat:**
- **Transfer cross-lingual din CompLex EN** via XLM-R: 40 -> 56. Cel mai mare salt initial.
- **Frecventa (zipf) + lexical bagate IN regresor** (nu doar blend post-hoc).
- **LLM-direct (RoLlama3-8b)** ca sursa RO-nativa independenta (corr ~0.57 cu cross-lingual).
- **MLSP/MultiLS Romance ca semnal SEPARAT, in ensemble cu CompLex EN**: 63.16 -> 64.52.
  Limbile romanice (fr/it/pt/es/ca) transfera spre RO putin mai bine decat engleza; mediate
  reduc varianta.
- **Calibrare analitica** (mean 0.27, std 0.125) - rezolvata o data, nu mai necesita probing.

**Au esuat / eliminate:**
- **Distilare LLM** (RoLlama3 eticheteaza 3386 cuvinte ET -> regresor XLM-R + stanza/RoWordNet):
  **eliminata** - 0.82 redundanta cu LLM-direct (antrenata pe etichetele lui), iar scoaterea ei a
  **imbunatatit** scorul (64.41 -> 64.52). Era si partea cea mai complexa/lenta.
- **CWI 2018 EN** (~26k cuvinte, scoruri binare/proportie): amestecat cu CompLex -> corr pe 14 s-a
  prabusit 0.891 -> 0.544. Metodologie binara != Likert, si 26k coplesesc 8400 CompLex.
- **MLSP amestecat IN antrenarea CompLex** (nu ca semnal separat): coplesit 8400:2800 -> semnal
  98% identic cu CompLex, zero castig. (Solutia = ensemble de semnale separate, nu mix de date.)
- **Pool Wikipedia** pentru extinderea distilarii (6005 cuvinte): fara castig + nereproductibil.
- **xlm-roberta-large**: EN-test r mai mare, dar transfer pe RO mai PROST (overfit pe EN). base castiga.
- **Antrenare pe cele 14 etichete**: overfit garantat.
- **ET ca semnal direct** (PC1 eye-tracking): slabeste blend-ul multi-sursa.

---

## 5. Lectii cheie (vezi `pred-eye-findings.md`)

1. **Cele 14 etichete si EN-test r NU prezic scorul public.** Imbunatatiri pe ele au inrautatit
   uneori public-ul. n=14 e zgomot - NU selecta modele pe ele.
2. **Calibrarea e rezolvata analitic.** Pearson e invariant la transformari afine; R2 maxim la
   mean=mean_real, std=r*std_real. Scala reala test: mean 0.27, std ~0.125.
3. **Mai multe date != mai bine** daca metodologia/distributia difera (CWI). Sursele bune se adauga
   ca **semnale separate in ensemble**, nu prin amestec de date.
4. **Transfer cross-lingual din engleza e aproape saturat** prin XLM-R; limbile romanice ajuta doar
   ca a doua sursa in ensemble, nu prin volum.

---

## 6. Cum rulezi

```bash
# Python 3.11 (vezi env-setup.md). transformers PINUIT la 4.46.3 (5.x crapa pe bitsandbytes 4-bit).
pip install torch transformers==4.46.3 bitsandbytes accelerate scikit-learn scipy pandas numpy wordfreq

# Calea RAPIDA (implicita): citeste semnalele cache din data/, reproduce bit-exact. Ruleaza pe CPU.
python solution_bert.py                      # variant=best (64.52) -> submission.csv
python solution_bert.py --variant enonly     # doar EN + LLM (fara MLSP gated)
python solution_bert.py --variant roonly     # doar RO (MLSP) + LLM
python solution_bert.py --variant clpure     # doar cross-lingual ensemble, fara LLM

# Calea COMPLETA: recalculeaza totul de la zero (necesita GPU ~8GB; descarca CompLex automat).
python solution_bert.py --recompute          # MLSP e gated -> trebuie pus manual in data/mlsp/
```

- **Cale rapida** = reproducere bit-exact din `data/*.csv` (semnalele cache). Ruleaza oriunde (CPU).
- **Cale completa** = incarca XLM-R + RoLlama3-8b (4-bit), reantreneaza. Output LLM/embeddings poate
  varia minim intre hardware-uri -> finalele bit-exact se bazeaza pe cache-ul din `data/`.

---

## 7. Structura fisierelor

```
pred_eye/
  solution_bert.py          <- SINGURUL cod (self-contained, ~16KB). Asta se preda.
  README.md                 <- acest fisier
  data/
    test_set.csv                      input competitie
    crosslingual_test.csv             semnal A: CompLex EN (cache)
    crosslingual_mlsponly_test.csv    semnal A: MLSP Romance (cache)
    llm_complexity_test.csv           semnal B: LLM (cache)
    complex_en/                       CompLex brut (pt --recompute)
    mlsp/                             MLSP/MultiLS brut, gated (pt --recompute; nu se urca)
  output/
    FINAL_best.csv     (64.52, F1)
    ND_ENonly.csv      (F2 candidat - fara MLSP gated, reproductibil din date publice)
    ND_CLpure.csv      (F3 candidat - fara LLM, cel mai divers)
  _arhiva_dezvoltare/       <- cod vechi (distilare, ET, surprisal, probe). Nu e folosit.
```

Variante `solution_bert.py` (toate reproduc bit-exact din cache, maxdiff 0.0):
`best` (0.6 ensemble + 0.4 LLM), `enonly`, `roonly`, `clpure`.

---

## 8. Resurse externe (necesita aprobare Sergiu - toate rulate local, fara API/closed-source)

| Resursa | Rol |
|---------|-----|
| **wordfreq** | frecventa (scor Zipf) RO + EN, in trasaturile lexicale |
| **XLM-RoBERTa-base** | embeddings contextuale multilingve |
| **RoLlama3-8b-Instruct** (OpenLLM-Ro) | LLM 8B open-weights, rating complexitate 1-5 |
| **CompLex** (SemEval-2021 LCP) | date complexitate EN, transfer cross-lingual |
| **MLSP / MultiLS 2024** | date complexitate limbi romanice (gated HuggingFace), transfer |

(Stanza / RoWordNet / nltk WordNet erau folosite DOAR in distilare - eliminate odata cu ea.)

---

## 9. Date & GitHub (repo PRIVAT)

Repo-ul e **privat**, deci datele oferite de competitie pot fi versionate fara probleme
(privat != public; regula "datele nu trebuie puse public" e respectata).

`.gitignore` exclude doar:
- `data/mlsp/` - **gated** pe HuggingFace, nu se redistribuie (nici macar privat, e termenul HF)
- `*.npy` - cache mare de embeddings (derivat, se regenereaza)
- `data/complex_en/`, `data/cwi_en/` - descarcabile public din cod

Restul (`data/test_set.csv`, semnalele tale, `output/`) se versioneaza -> reproducere bit-exact.
**Nu face repo-ul public** fara sa muti datele competitiei + MLSP afara.

---

## 10. Stare & de facut

- [x] Solutie finala: best = 64.52 (r~0.741).
- [x] Cod consolidat self-contained, reproducere bit-exact.
- [ ] **Alege 3 finale pe platforma:** F1=`FINAL_best.csv` (64.52, confirmat); F2=`ND_ENonly.csv`
      (~64.5, reproductibil fara gated); F3=`ND_CLpure.csv` (divers, fara LLM - neconfirmat public).
- [ ] **Mail Sergiu** pentru aprobarea resurselor din sectiunea 8.
- [ ] **Raport** - scris de OM (rapoartele generate cu LLM primesc 0.0). Cifrele/tabelele din acest
      README + memorie ajuta.
- [ ] (optional, netestat) **Ensemble 2 LLM-uri** (RoLlama3 + RoMistral-7b) pentru semnalul B -
      prin analogie cu ensemble-ul cross-lingual care a functionat.
- [ ] Revoca token-ul HuggingFace folosit pentru descarcarea MLSP.

---

## 11. Note de mediu (vezi `env-setup.md`)

- Python 3.11: `& "C:\Users\glosper\AppData\Local\Programs\Python\Python311\python.exe"`
  (`python` simplu poate rezolva la un Python gol).
- **`transformers==4.46.3`** - versiunile 5.x dau segfault la incarcarea RoLlama3-8b in 4-bit
  (bitsandbytes). XLM-R/BERT merg pe ambele.
- GPU: RTX 2070 SUPER 8GB e suficient (XLM-R + RoLlama3-8b in 4-bit).
- Ruleaza un singur job GPU odata; `TQDM_DISABLE=1` + `python -u` pentru log-uri curate.
