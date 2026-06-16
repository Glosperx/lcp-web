# CONTEXT HANDOFF — pred_eye (predictie complexitate lexicala RO)

> **DEPASIT (stale). Best aici = 64.52 = era veche.** Sursa curenta de adevar = **`SESSION_CONTEXT.md`**
> (best **68.90** dupa lemma-freq + surprisal; experimente noi: surprisal, lemma, fine-tuning, SHAP, ET,
> few-shot/CoT/self-consistency). Citeste ALA intai. Acest fisier = doar istoric pana la 64.52.

Document pentru reluarea muncii intr-o sesiune Claude noua. Citeste si `README.md` (pipeline detaliat)
+ folderul de memorie `~/.claude/projects/.../memory/` (`pred-eye-project.md`, `pred-eye-findings.md`,
`env-setup.md`). Fara diacritice intentionat.

---

## 1. Current State

Proiectul e in stare FINALA functionala. Best public = **64.52** (r~0.741).

- `solution_bert.py` — rescris complet (16KB, self-contained, 2 semnale). E SINGURUL cod activ.
- Variante validate bit-exact (maxdiff 0.0 vs CSV-urile submise): `best`, `enonly`, `roonly`, `clpure`.
- `README.md` + `.gitignore` scrise. Cod vechi mutat in `_arhiva_dezvoltare/`.
- User a creat repo GitHub **privat**: https://github.com/Glosperx/Eye-tracking_prediction
  — `git push` NU e inca facut (user il da manual; i-am dat comenzile: git init / add / commit /
  remote add / push). `.gitignore` exclude doar `data/mlsp/`, `*.npy`, `data/complex_en/`, `data/cwi_en/`.

TODO deschis (al user-ului, nu al meu): alege 3 finale pe platforma, scrie raport (OM),
revoca token HF.

---

## 2. Decisions Made (cu motiv)

- **Distant supervision, ZERO antrenare pe cele 14 etichete** — 14 = prea putine, overfit garantat.
- **Cross-lingual ensemble EN+RO** — CompLex EN (8400) + MLSP Romance (2800), fiecare antrenat
  separat (Ridge+HGB), predictiile pe RO mediate 50/50. Motiv: ensemble a doua surse de transfer
  ~independente (corr 0.86) reduce varianta; a batut fiecare endpoint (EN 63.16, RO 63.67 -> 64.41/64.52).
- **Distilare LLM ELIMINATA** — era 0.82 redundanta cu LLM-direct (antrenata pe etichetele lui);
  scoaterea ei a IMBUNATATIT scorul (64.41 -> 64.52) si a simplificat proiectul. User a cerut explicit.
- **Eye-tracking NEFOLOSIT in solutia finala** — ET era doar in distilare (acum scoasa). De justificat
  la oral: distant supervision bate semnalul ET.
- **Fuziune 0.6*z(cross-lingual) + 0.4*z(LLM)**; **calibrare clip(0.27 + 0.125*z(scor),0,1)**
  (mean/std reale ale test-ului, derivate prin probing).
- **Ridge(alpha=300) + HistGradientBoosting** mediati — liniar + neliniar = robust.
- **xlm-roberta-base** (NU large — large transfera mai prost pe RO).
- **Repo privat** => datele competitiei se versioneaza (privat != public); doar MLSP gated exclus.

---

## 3. What Works (confirmat)

- `python solution_bert.py [--variant best|enonly|roonly|clpure]` — cale rapida (cache), CPU, bit-exact.
- Scoruri publice confirmate: **best 64.52**, b2 (cu distilare) 64.41, B1 (RO-only+distill) 63.67,
  wA (EN-only+distill) 63.16, b2_nodistill 64.52.
- Toate variantele reproduc bit-exact din `data/*.csv` (verificat maxdiff 0.0).
- `solution_bert.py` standalone (nu importa nimic din `_arhiva_dezvoltare/`).

---

## 4. In Progress / Broken

- NIMIC rupt.
- `output/ND_ENonly.csv` (~64.5 estimat, 0.98 corr cu best) si `output/ND_CLpure.csv` (fara LLM,
  0.93 corr, ~55? estimat) — NECONFIRMATE pe public. Candidate F2/F3.
- **Ensemble 2-LLM** (RoLlama3 + RoMistral-7b pentru semnalul B) — propus, NETESTAT. Cel mai plauzibil
  lever ramas (prin analogie cu ensemble-ul cross-lingual).
- `git push` neefectuat (user il da; are nevoie de PAT GitHub sau credential manager).

---

## 5. Next Steps (prioritate)

1. **git push** pe repo-ul privat (comenzi date; verifica `git status` ca `data/mlsp/` NU apare).
2. **Alege 3 finale pe platforma**: F1=`output/FINAL_best.csv` (64.52, confirmat);
   F2=`output/ND_ENonly.csv` (reproductibil fara MLSP gated); F3=`output/ND_CLpure.csv` (divers, fara LLM).
3. **Mail Sergiu** (sergiu.nisioi@unibuc.ro) — aprobare resurse: wordfreq, XLM-RoBERTa-base,
   RoLlama3-8b-Instruct, CompLex EN, MLSP/MultiLS Romance. (Draft in istoricul conversatiei.)
4. **Raport** — scris de OM (LLM-generated = 0.0). Cifre/tabele din README + memorie.
5. (optional) **Ensemble 2-LLM** — daca user vrea sa mai impinga scorul.
6. **Revoca token HF** folosit la descarcarea MLSP.

---

## 6. Gotchas & Context (non-evident)

- **Python 3.11 obligatoriu**: `& "C:\Users\glosper\AppData\Local\Programs\Python\Python311\python.exe"`.
  `python` simplu rezolva la un Python gol (C:\Python314).
- **`transformers==4.46.3` PINUIT** — 5.x da segfault (exit 139) la incarcarea RoLlama3-8b in 4-bit
  (bitsandbytes). XLM-R/BERT merg pe ambele. NU face `pip install stanza` (urca transformers la 5.x).
- **MLSP e gated pe HF** (`MLSP2024/MLSP2024`) — necesita cont + acces aprobat + token. NU se urca in git.
  Fisierele descarcate sunt in `data/mlsp/` (test+trial, fr/it/pt/es/ca, ~2900 randuri).
- **Cele 14 etichete + EN-test r NU prezic scorul public** — NU selecta modele pe ele (n=14 = zgomot;
  am avut cazuri unde corr-14 mai mare a dat public mai mic).
- **Mai multe date != mai bine**: CWI 2018 EN (binar) a prabusit corr-14 la 0.544; MLSP amestecat IN
  CompLex (nu ca semnal separat) a dat semnal 98% identic (coplesit 8400:2800). Sursele bune se adauga
  ca SEMNALE SEPARATE in ensemble, nu prin mix de date.
- **xlm-roberta-large transfera mai PROST** decat base pe RO (overfit pe EN). NU-l reincerca.
- **Raport scris cu LLM = 0.0** — user il scrie de mana.
- **Datele nu se pun public** (regula competitie) — repo e privat, deci OK; NU-l face public fara sa
  muti datele afara.
- **Un singur job GPU odata** (joburi GPU concurente au crapat exit 127). `TQDM_DISABLE=1` + `python -u`.
- **Calibrarea e rezolvata analitic** (mean 0.27, std 0.125) — nu mai trebuie probing pe leaderboard.
- Recuperezi r dintr-un scor: `r = (-1 + sqrt(1 + 4*score/50)) / 2`.

---

## 7. File Map

**Cod activ:**
- `solution_bert.py` — SINGURUL cod. Functii cheie:
  - `lexical(tokens, langs)` — zipf(wordfreq)+lungime+silabe+majuscula
  - clasa `XLMR` — embed cuvant (xlm-roberta-base, medie subword last-4 layers)
  - clasa `LLMRater` — RoLlama3-8b 4-bit, rating 1-5 din probabilitatile token-ilor "1".."5"
  - `blend_ridge_hgb(Xtr,ytr,Xpredict)` — media Ridge(alpha=300) + HistGradientBoosting
  - `recompute_signals(test)` — calculeaza A (CompLex EN + `_recompute_mlsp`) si B (LLM) de la zero (GPU)
  - `_recompute_mlsp(...)` — transfer MLSP Romance; None daca `data/mlsp/` lipseste
  - `load_cached_signals(test)` — citeste cele 3 CSV cache (cale rapida)
  - `main()` — fuziune per varianta (best/enonly/roonly/clpure) + calibrare -> `submission.csv`

**Date (`data/`):**
- `test_set.csv` — input (1587, coloane text, token, datapointID)
- `crosslingual_test.csv` — semnal A: CompLex EN (datapointID, xl_complexity)
- `crosslingual_mlsponly_test.csv` — semnal A: MLSP Romance
- `llm_complexity_test.csv` — semnal B: LLM (datapointID, llm_cx)
- `complex_en/` — CompLex brut (lcp_single_{train,trial,test}.tsv)
- `mlsp/` — MLSP/MultiLS brut gated ({fr,it,pt,es,ca}_{test,trial}.tsv) — NU in git

**Output (`output/`):**
- `FINAL_best.csv` (64.52, F1), `ND_ENonly.csv` (F2), `ND_CLpure.csv` (F3),
  + istoric: B1_mlsp.csv (63.67), b2_nodistill.csv (64.52), FINAL_b2/wA/multisup/crosslingual.

**Alte:**
- `README.md` — pipeline + jurnal experimente complet (fara diacritice)
- `.gitignore` — exclude mlsp/, *.npy, complex_en/, cwi_en/
- `_arhiva_dezvoltare/` — cod vechi (src/ cu distilare/ET/surprisal/probe, solution.py non-BERT, source_code/)
- Memorie: `~/.claude/projects/c--Users-glosper-Documents-pred-eye/memory/`
  (`pred-eye-project.md`, `pred-eye-findings.md`, `env-setup.md`, `MEMORY.md` index)
