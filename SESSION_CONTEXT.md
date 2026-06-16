# SESSION_CONTEXT.md

## Project Overview
- Predicts **lexical complexity (0-1)** of Romanian words in context. UniBuc competition "Predicting lexical
  complexity from eye-tracking data" (Nitro AI Judge, team **Sahistii**). **Distant supervision** — ZERO
  training on the 14 RO labels (they don't predict public). Transfer from labeled EN + Romance + a RO LLM.
- **Stack:** Python 3.11 ONLY (`C:\Users\glosper\AppData\Local\Programs\Python\Python311\python.exe`).
  `transformers==4.46.3` **PINNED** (5.x segfaults RoLlama3 4-bit). torch 2.5.1+cu121, bitsandbytes,
  scikit-learn, scipy, wordfreq, peft==0.13.2 (`--no-deps`), shap 0.51, matplotlib 3.11. GPU ~8GB, ONE job
  at a time. Run with `TQDM_DISABLE=1 TRANSFORMERS_VERBOSITY=error PYTHONIOENCODING=utf-8` (cp1252 console).

## Current Objective
- Push score beyond 64.52 AND build rigorous report/research material. Real tel = report (5p, BY HAND,
  LLM=0.0) + being chosen by prof **Sergiu Nisioi** for EMNLP collaboration. Rank affects grade only by
  hundredths. **Result: 64.52 -> 64.81 (surprisal) -> 68.90 (lemma-freq), +4.38.**

## Public Leaderboard Scores (every probe, chronological)
| candidate | file | public |
|-----------|------|--------|
| original best (cross-lingual EN+RO ensemble + LLM) | output/FINAL_best.csv | 64.52 |
| mid-layer embeddings | output/exp_midlayer.csv | 64.49 |
| surprisal w=0.10 | output/exp_surp_w10.csv | 64.79 |
| surprisal w=0.15 | output/exp_surp_w15.csv | 64.50 |
| surprisal w=0.20 | output/exp_surp_w20.csv | 63.84 |
| surprisal w=0.08 | output/exp_surp_w08.csv | 64.81 |
| surprisal w=0.12 | output/exp_surp_w12.csv | 64.71 |
| encoder e5 (multilingual-e5-base) | output/exp_e5.csv | 63.00 |
| LLM few-shot prompt | output/exp_llm_fewshot.csv | 63.31 |
| **lemma-freq + surprisal w0.08 (BEST)** | **output/exp_lemmafreq.csv** | **68.90** |
| lemma-freq, NO surprisal (w0) | output/exp_lemma_w00.csv | 68.645 |
| surface-only baseline (FARA resurse externe) | output/exp_baseline_surface.csv | 10.27 (r~0.175) |
| constant 0.27 (floor analitic) | output/exp_baseline_const.csv | ~0 |
| Lasso signal-A (regressor swap) | output/exp_lasso.csv | 64.28 (r~0.739) GATE FALS-POZITIV |
| ET + surface self-sup (no-external MAI MARE) | output/exp_baseline_et.csv | 41.76 (r~0.542) |
- Ablation: cross-lingual+LLM 64.52 | +surprisal 64.81 (+0.29) | +lemma no-surp 68.645 (+4.13) |
  **+lemma+surprisal 68.90 (FINAL)**. Lemma = the giant; surprisal = small but real (+0.26 on lemma base).

## Approaches Tried (with full metrics)

### A. Embedding layer sweep — free gate `transfer_eval` (transfer_avg, baseline last4=0.5512)
last4 0.5512 | **mid 0.5558** | concat4 0.5301 | ctxiso 0.5425 | last4+oov 0.5524 | last4+oov+phon 0.5522 |
last4+oov+phon+morph 0.5522. mid won gate but **FAILED public (64.49<64.52)**. Micro-tuning saturated.

### B. Encoder swap — free gate (transfer_avg)
xlmr 0.5512 | labse 0.5554 | **e5 0.5855** (EN->ML 0.5353, ML->EN 0.6356). e5 won gate big but
**FAILED public 63.00**. Gate measures EN<->Romance, NOT ->RO.

### C. Surprisal signal C (RoLlama3 `-log P(word|context)`, per-token) — WORKED
Independent of LLM rating (corr 0.068). Public weight curve: w0=64.52, **w0.08=64.81 (peak)**, w0.10=64.79,
w0.12=64.71, w0.15=64.50, w0.20=63.84.

### D. Eye-tracking orthogonality (`analysis_et.py`)
ET coverage 1509/1587 test (95%) but only **2/14 labeled** words have ET. corr(et_proxy, our pred)=0.622
(0.334 controlled for freq+len). Early ET (FFD/FPRT/skip) controlled corr with pred = **0.0103** (= pure
frequency); Late ET (RRT/RPD/TRC/refix) controlled = **0.2430**, corr with surprisal C controlled 0.177
(early -0.027). => late ET = integration difficulty = aligns with surprisal (surprisal theory).

### E. Fine-tuning XLM-R (`finetune_xlmr.py`) — ALL FAILED vs frozen
Free gate transfer EN->MLSP (frozen baseline 0.5148). Full sweep:
| cfg | transfer_en2ml |
|-----|------|
| base lr1e-5 ep3 fz0 | 0.4155 |
| base lr1e-5 ep3 fz6 | 0.3691 |
| base lr1e-5 ep5 fz0 | 0.4235 |
| base lr1e-5 ep5 fz6 | 0.3757 |
| base lr2e-5 ep3 fz0 | 0.4139 |
| base lr2e-5 ep3 fz6 | 0.3994 |
| base lr2e-5 ep5 fz0 | 0.4495 |
| base lr2e-5 ep5 fz6 | 0.4054 |
| base lr3e-5 ep3 fz0 | 0.4332 |
| base lr3e-5 ep3 fz6 | 0.4179 |
| base lr3e-5 ep5 fz0 | 0.4609 |
| base lr3e-5 ep5 fz6 | 0.4318 |
| large lr1e-5 ep3 fz0 | -0.0288 |
| large lr1e-5 ep3 fz12 | 0.2029 |
(2 large configs killed — slow ~107min/each, conclusion already clear.)
LoRA sweep (Q+V): lora4 lr1e-4 0.4096, lora4 lr2e-4 0.4308, lora8 lr1e-4 0.4391, lora8 lr2e-4 0.4498,
lora16 lr1e-4 0.4402, **lora16 lr2e-4 0.4618**. LoRA ~= full-FT, still < frozen 0.5148.
Multilingual held-out-language (EN-only vs EN+Romance, LoRA r16):
| held-out | EN-only | EN+Romance | frozen-multi |
|----------|---------|------------|--------------|
| it | 0.5268 | 0.5506 | 0.6006 |
| pt | 0.6503 | 0.6710 | 0.7775 |
| es | 0.5375 | 0.5782 | 0.6185 |
Multilingual helps fine-tuning (+0.02-0.04) but **frozen wins everywhere** (0.666 vs 0.600 avg). Cause: no
RO labels => fine-tuning overfits source language, degrades multilingual alignment frozen exploits.

### F. Rarity (-zipf) as separate signal (Stefan's idea) — REDUNDANT
corr(rarity, cross-lingual A)=**0.936** (A is ~a frequency detector), (rarity, LLM B)=0.525,
(rarity, best)=0.851, (rarity, real 14 labels)=0.606. Unique contribution beyond A+B = **0.012**. Not added.

### G. SHAP feature importance (`analysis_shap.py`, `shap_beeswarm.py`) — base Pearson 0.79
| feature | perm importance | SHAP mean\|abs\| |
|---------|------|------|
| zipf (frequency) | **0.4536** | 0.068 |
| embedding (768) | 0.1433 | 0.182 |
| length | 0.0377 | 0.008 |
| capital | 0.0023 | 0.003 |
| syllables | 0.0011 | 0.002 |
=> frequency DOMINATES. Beeswarm (incl. surprisal+LLM as features, surrogate r=0.987): frequency #1, LLM
rating #2, surprisal #3 (small but real), rest ~0.

### H. Lemma-aware frequency (SHAP-driven) — BIGGEST WIN +4.13
RO inflected => **186/1587 surface forms OOV** in wordfreq (zipf=0) => falsely super-rare/complex; 60 fixed
by lemma, 360 higher lemma freq; corr(token-zipf, lemma-zipf)=0.75. Fix: `max(zipf_token, zipf_lemma)`.
Signal A changed for 1380 words (corr old/lemma A = 0.911). Public 64.52 -> 68.645 (no surp) / **68.90**.

### I. LLM prompt few-shot / CoT / self-consistency (`llm_prompt.py`, Wei 2022 + Wang 2022) — ALL FAILED
Free gate (Pearson vs true complexity). cot_sc = self-consistency CoT (k=3 sampled rationales, temp0.7,
averaged soft-read; EN/Rom n=150):
| source | zeroshot | fewshot | cot | cot_sc |
|--------|----------|---------|-----|--------|
| EN | 0.5668 (n300) | 0.4533 | 0.3519 | 0.4989 (n150) |
| Romance | 0.4651 (n300) | 0.2998 | 0.2745 | 0.3717 (n150) |
| RO14 (n=14) | 0.5907 | 0.8415 | 0.3577 | 0.2677 |
RO14 fewshot=0.84 is n=14 mirage. few-shot public **63.31<64.81**. CoT dead (8B below scale threshold).
**Self-consistency RECOVERED part of greedy-CoT loss (cot_sc 0.50/0.37 > cot 0.35/0.27) but still LOST to
zeroshot (0.59/0.47)** => sampling+averaging helps a sub-scale model but can't close the emergence gap.
cot_sc failed gate => NO predict-ro, NO submit (stays 68.90). Report finding, not a new best.
**zeroshot optimal — DON'T change LLM prompt.**

### J. Sugestiile lui Sergiu testate (`analysis_features.py`, `analysis_lasso.py`, `analysis_hardset.py`)
Instalat spaCy 3.8.14 + `ro_core_news_sm` (+ `rowordnet`); **transformers ramane 4.46.3** (pin intact).
Metodologie = contributie unica controlata pe zipf+len, proxy = best 68.90.
- **POS/dep/morfologie/NER (spaCy) + RoWordNet (polisemie/sinonime/antonime/adancime): TOATE redundante
  cu frecventa.** Raw semnificativ (in_wordnet -0.385, polysemy -0.284, n_synonyms -0.240) dar controlat
  pe freq+len < 0.08. Singur candidat `is_entity` ctrl -0.14 (slab, acoperire 15.9%). Confirma SHAP.
  POS medie complexitate: PROPN 0.40 > ADJ 0.34 > VERB/NOUN 0.27.
- **Ridge vs Lasso (feature-space real 768emb+lexical, free-gate):** transfer_avg Lasso(0.01) **0.5688**,
  ElasticNet 0.5650, blend Ridge300+HGB [SOLUTIE] 0.5512, Ridge300 0.4893, OLS 0.4337. **L1/sparsitate
  transfera mai bine cross-lingual.** SUBMIS: public **64.28 < 68.90** => AL 3-LEA GATE FALS-POZITIV
  (e5/mid/lasso). Gate-ul EN↔Romanic nu prezice →RO; L1 taie dim necesare RO + subutilizeaza frecventa.
  Castigul era mai ales ML->EN; pe EN->ML (productie) blend-ul tinea — semn de avertizare ignorat. Blend ramane.
- **Hard-testset** (`output/hard_testset/`): fara etichete => hard = dezacord semnale std(zA,zB,zC)>q75 SAU
  OOV = 461/1587 (29%), mai rare (zipf 3.21 vs 4.62). corr A<->B 0.57, C(surprisal)<->B 0.068 (ortogonal).
  Cele mai grele = cuvinte frecvente dar surprisal mare (Luna/COST/Cartea), capitalizate/inceput-propozitie.
- **Infezabil pe RO** (lipsa lexicon): child-freq, AoA, imaginabilitate (`output/extra_features/infeasible.md`).

## Current State
- **BEST = 68.90** = `output/exp_lemmafreq.csv`. Regenerate:
  `python solution_bert.py --lemma-freq --surp-weight 0.08 --out output/exp_lemmafreq.csv`
  (reuses cached `data/emb_*.npy` + `data/llm_complexity_test.csv` + `data/surprisal_test.csv`; recomputes
  only signal A).
- `best` (64.52) **bit-exact**: `python solution_bert.py --variant best` -> maxdiff 0.0 vs FINAL_best.csv.
  All experiments opt-in flags; default path untouched. **Nothing broken.**
- **Files (cumulative):** MODIFIED `solution_bert.py` (lemma `lexical(...,lemmas=)`, `XLMR(cfg,encoder)`,
  `transfer_eval`, `LLMRater.surprisal`, 4-tuple `recompute_signals(...,lemma_freq=)`, flags
  `--encoder/--emb/--feats/--eval/--sweep/--llm-file/--lemma-freq/--surp-weight/--regressor/--et-weight`),
  `README.md`.
  NEW: `finetune_xlmr.py`, `llm_prompt.py`, `analysis_et.py`, `analysis_shap.py`, `shap_beeswarm.py`,
  `baseline_surface.py`, `baseline_et.py`, `analysis_features.py`, `analysis_lasso.py`, `analysis_hardset.py`,
  `make_figures.py`.
  Outputs: `output/exp_*.csv`, `output/shap/*.png`, `output/et_analysis/*`. Data caches: `data/finetune_*.csv`,
  `data/llm_gate.csv`, `data/surprisal_test.csv`, `data/llm_fewshot_test.csv`,
  `data/crosslingual_test_*_lemma.csv`, `data/emb_*.npy`.
- **Session 2026-06-16 (self-consistency CoT):** ADDED to `llm_prompt.py` `PromptRater.rate_cot_sc`
  (k sampled rationales temp0.7/top_p0.9, seeded `SEED+i`, averaged soft-read) + mode `cot_sc` in
  `rate_mode`/`--mode`/`--modes` + arg `--cot-k` (default 5; rater.cot_k). NO change to `solution_bert.py`.
  Ran `llm_prompt.py --llm-gate --modes zeroshot,cot_sc --n 150 --cot-k 3` => FAILED (section I).
  New artifacts: `data/llm_gate.csv` (overwritten w/ cot_sc rows), `llm_cot_sc_gate_log.txt`. NO predict-ro,
  NO submit (gate fail). Memory added: `pred-eye-cot-failed`. Best unchanged 68.90.
- **Session 2026-06-16 (part 2 — baseline-uri + feature-uri Sergiu + RAPORT):**
  - **Baseline-uri no-external (ablatie raport):** const 0.27 ->~0 | surface-only `exp_baseline_surface.csv`
    10.27 (r0.175) | ET+surface self-sup `exp_baseline_et.csv` **41.76 (r0.542)** | full 68.90 (r0.776).
    ET = `et_complexity_proxy` (ET-only, X_test.csv); 78 fara ET => gap-fill regresie surface->proxy.
    Scripturi `baseline_surface.py`, `baseline_et.py`.
  - **ET metric eval** (`output/extra_features/et_metric_eval.csv`): corr metrica ET vs complexitate (proxy
    68.90): TFT 0.63, FRT/RBRT 0.61, FPRT 0.60, TFC 0.58, FPFC 0.53, RRT 0.52, FFD 0.43, RPD_inc 0.35,
    skip −0.34, TRC_in 0.18; **zgomot ~0: LP 0.02, SL_in 0.003, SL_out −0.05, RPD_exc 0.08**. Excluderea SL/LP
    justificata EMPIRIC; FRT/RBRT/FPRT excluse ca redundante (duplicat TFT). Ponderile proxy NU conteaza:
    egal/literatura/PCA corr **0.985+**. Alternativa curata = PCA `reading_effort` (PC1, in word_features.csv).
    Citare ET concept: Rayner 1998 (DOI 10.1037/0033-2909.124.3.372) — NU pt ponderi (heuristic).
  - **ET-blend in 68.90 (`--et-weight`):** candidati `exp_et_w{05,10,20}.csv` generati (corr 0.999/0.997/0.986
    cu best). DE SUBMIS (incepe w10). Free-gate NU testeaza ET => doar public decide. Default et_w=0 = bit-exact.
  - **RAPORT (in lucru):** template ACL primit. **CONSTRANGERE: raport scris DOAR de LLM = 0.0** => user il
    rescrie de mana; eu dau draft dens + figuri. **AUC/PRC NU se aplica (regresie)** => figuri ablatie/curba
    surprisal/corelatii ET/SHAP. `make_figures.py` scris (3 figuri -> `output/raport/`). RAMAS: ruleaza
    make_figures.py, scrie `output/raport/report.tex` + `custom.bib` (draft pe fapte reale), user rescrie.
  - Instalat spaCy 3.8.14 + ro_core_news_sm (pin transformers 4.46.3 intact). Memorii actualizate:
    `pred-eye-baseline-surface`, `pred-eye-extra-features`.

## Next Steps
- **Pick 3 finals (private leaderboard):** F1 `exp_lemmafreq.csv` (68.90), F2 `exp_lemma_w00.csv` (68.645),
  F3 `exp_lemma_w12.csv` (~68.9, brackets surp weight 0/0.08/0.12).
- **Write LaTeX report BY HAND** (LLM=0.0). Materials ready: ablation table above, 2 SHAP figs
  (`output/shap/`), ET study (`output/et_analysis/`), all negative-result tables, free-gate methodology.
  Credit ideas: Sergiu (embedding+features), Stefan (frequency; complexity!=difficulty).
- **[MAINE] Verifica feature-urile SHAP** (`analysis_shap.py`/`shap_beeswarm.py`): in beeswarm `cratima`
  are SHAP ~0 cu TOATE punctele albastre => suspect feature aproape constant (mai niciun cuvant RO din
  test n-are cratima) sau calculat gresit. La fel ~zero: `OOV`, `consoane`, `silabe`. Verifica: (1) cratima
  produce valori non-zero (nu mereu 0); (2) decide daca scoti feature-urile moarte. Default best e
  bit-exact, deci scoaterea = doar experiment opt-in, NU atinge 68.90.
- **[RAPORT] baseline FARA resurse externe — FACUT (`baseline_surface.py`).** (a) constant 0.27 =
  floor analitic ~0 (var 0 => Pearson nedefinit). (b) regresie liniara Ridge pe 7 trasaturi de suprafata
  (len, silabe, max-consoane, vowel-ratio, majuscula, diacritice RO, sufix latinat), antrenata pe
  CompLex EN + MLSP Romanic, zero-shot RO, ensemble 50/50, calib 0.27/0.125 => `output/exp_baseline_surface.csv`,
  **public 10.27 (r~0.175)**. Free-gate surface-only transfer_avg = -0.0445 (EN->ML 0.048, ML->EN -0.137);
  gate-ul intra-Romanic SUBESTIMEAza (RO public 10.27 > 0 prin componenta universala lungime->complexitate).
  **Lift resurse externe = +58.6 (87% din scor)**; surface singur explica ~13%. Consistent cu SHAP (length
  perm 0.038). Nuanta: Ridge invata coef negativ pt lungime (coliniaritate EN cu silabe) => regresia
  subutilizeaza lungimea (raw length-vs-best 0.331 > ensemble-vs-best 0.242). solution_bert.py NEATINS
  (68.90 bit-exact). Memorie: `pred-eye-baseline-surface`.
- **Revoke HF token** (gated MLSP download).
- **LLM prompt lever EXHAUSTED** (zeroshot vs fewshot/cot/cot_sc all done — section I). Only untested LLM
  lever left = **2-LLM ensemble** (2nd RO LLM e.g. RoMistral-7b as independent signal B, ensemble w/
  RoLlama3) — proposed, plausible small gain by analogy to cross-lingual ensemble. NOT a prompt change.
- **[CANDIDATI DE SUBMIS] ET blend in 68.90** — flag nou `--et-weight` (ET=et_complexity_proxy, ~0.33
  ortogonal pe predictie). Generati `output/exp_et_w{05,10,20}.csv` (`--lemma-freq --surp-weight 0.08
  --et-weight {0.05,0.10,0.20}`). Foarte aproape de best (corr 0.999/0.997/0.986; randuri schimbate >0.05:
  0/3/50). Submite (incepe cu w10) sa vezi daca ortogonalitatea ET ajuta peste 68.90. Default `--et-weight 0`
  = 68.90 bit-exact (bloc gated). Free-gate NU poate testa ET => doar public real decide.
- **[CANDIDAT RESPINS] Lasso signal-A** — L1 a batut Ridge pe free-gate (0.5688 vs 0.5512) DAR pe public
  **64.28 < 68.90** (`output/exp_lasso.csv`, flag `--regressor lasso`). AL 3-LEA GATE FALS-POZITIV (e5/mid/
  lasso): gate-ul EN↔Romanic supra-recompenseaza transferul intre limbile lui, pica pe →RO. L1 taie dim
  embedding necesare RO + subutilizeaza frecventa (motor RO). NU submite elasticnet (acelasi mecanism).
  Blend ramane campion. Default `--regressor blend` = 68.90 BIT-EXACT (verificat maxdiff 0.0).

## Key Configs / Non-obvious Decisions
- **Fusion (best):** `s = 0.6*z(cross_lingual_ensemble) + 0.4*z(LLM)`; ensemble =
  `z(0.5*z(EN_CompLex) + 0.5*z(MLSP_Romance))`. Surprisal: `s=(1-0.08)*z(s)+0.08*z(surp)`. Calibration:
  `clip(0.27 + 0.125*z(s), 0, 1)` (analytic, real test mean 0.27/std 0.125).
- **Lemma fix:** `lexical()` freq = `max(zipf(token,lg), zipf(lemma,lg))` when lemmas given; RO passes
  `test["lemma"]`, EN/MLSP pass None. Opt-in `--lemma-freq` => best bit-exact.
- **Regressor A:** mean of `Ridge(alpha=300)` + `HistGradientBoosting(max_depth=3, lr=0.05, max_iter=400,
  l2_regularization=1.0)`. High reg deliberate (transfer fragile).
- **Encoder:** `xlm-roberta-base` FROZEN, mean last-4 layers, subword-span mean-pool, language-centered.
- **Free gate:** `transfer_eval` train CompLex EN <-> test MLSP Romance (thousands of labels), NOT the 14.
  Frozen baseline transfer_avg 0.5512 (EN->ML 0.5148).
- **surprisal != LLM rating:** rating = prompt-for-1-5 (opinion); surprisal = raw `-log P` internals. corr 0.068.
- **DON'T RETRY:** xlm-roberta-large, e5/LaBSE swap, encoder fine-tuning (any), CWI dataset, mixing MLSP into
  CompLex, few-shot/CoT/self-consistency-CoT prompting, rarity as separate signal, Lasso/ElasticNet regressor
  swap (gate fals-pozitiv, public 64.28<68.90), spaCy/RoWordNet feats (redundante cu frecventa). All documented
  failures with numbers above.
- **GATE FALS-POZITIVI (3):** e5 (gate 0.5855→public 63.00), mid-layer (gate win→64.49), Lasso (gate 0.5688→
  64.28). Free-gate-ul EN↔Romanic supra-recompenseaza ce ajuta transferul intre limbile lui dar pica →RO.
  Lectie raport: gate-ul e ghid pt SELECTIE GROSIERA, dar castiguri mici pe gate NU garanteaza public RO.
