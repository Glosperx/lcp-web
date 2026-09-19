---
name: cod-nou-al-treilea-semnal
description: "Cele cinci scripturi noi din 23 aug 2026 pentru al treilea semnal, plus --only-c din bakeoff_trial, cu controalele care le valideaza si cele doua capcane platite"
metadata: 
  node_type: memory
  type: project
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-23T17:16:16.261Z
---

Scris pe **23 august 2026**, sesiunea pe al treilea semnal. Toate ruleaza pe
`/opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python`.

## Scripturile

- **`analysis_c_sanatate.py`** (145 linii). Poarta de sanatate pentru C: **trei probe pe TEXT BRUT**,
  necesare impreuna. `uniform` (surprisal mediu pe itemi reali < ln|V|), `degenerare` (>= 3 tokeni
  distincti in 10 la decodare greedy), `ordonare` (continuare corecta mai putin surprinzatoare decat
  una implauzibila). Agnostic de backend, prin `LLMRater._logits_last`. Vezi
  [[gemma-nu-poate-da-surprisal]].
- **`analysis_c_frontiera.py`** (323 linii). Poarta de frontiera pentru un al treilea semnal PONDERAT,
  in forma cu doua marimi. Scoate `r_C`, `rho` cu zA / zB / p_fuz, corelatia partiala, pragul, `R_max`
  si `u_opt`, **pe limba**. `--exclude` scoate modelele care pica poarta de sanatate, `--c-csv
  NUME=CALE` primeste candidati care nu sunt iesirea unui LLM. Vezi [[poarta-al-treilea-semnal-0107]].
- **`analysis_c_fuse.py`** (207 linii). Al treilea termen peste fuziunea **inghetata**:
  `p3 = (1-u)*z(p_fuz) + u*z(C)`, cu `u` ales LOLO pe grila [-0.30, +0.30] care contine zero.
  **Nu atinge `fuse_ab.py`**, deliberat: grila lui `w` nu se largeste, deci patologia de criteriu
  imbricat din [[ponderea-per-item-inchisa]] nu poate aparea. `--u-grid 0` e controlul de reproducere,
  `--zgomot N` e podeaua.
- **`analysis_shap_multi.py`** (291 linii). Atribuire pe sistemul multilingv, per limba. Blocul 1a
  surogat lexical cu **doua** importante (permutare si reantrenare fara coloana), 1b control de
  fidelitate cu A si B in set, 1c itemii pe care A si B gresesc amandoua in acelasi sens. Blocul 2
  prezice reziduul SEMNAT leave-one-language-out si il trece prin poarta. Scrie
  `output/c_resid_lolo.csv`.
- **`analysis_alti_candidati.py`** (91 linii). Trei candidati aproape gratis in formatul `lang, idx, C`:
  entropia si dezacordul lui B prin `fuse_ab.h_from_dist`, si densitatea vecinatatii semantice din
  `data/emb_mlsp10_xlmr_last4_5624.npy`, cu vecinii cautati **in interiorul limbii** (intre limbi
  cosinusul e dominat de componenta de limba).
- **`bakeoff_trial.py --only-c`** (~20 linii adaugate). Masoara numai surprisal-ul, sarind peste
  `rate_parts`. **0.18-0.21 s per item fata de 0.84-1.09**, deci de patru ori mai ieftin. CERE `--out`.

## Controalele care le valideaza, toate trecute

- `--only-c` reproduce coloana C **bit cu bit**: 0 diferente din 30 de randuri fata de
  `output/bakeoff_test/qwen3-8b-4bit.csv`, comparate ca TEXT, nu ca float.
- `analysis_c_fuse.py --u-grid 0` reproduce `p_fuz` cu eroare maxima **1.11e-16** pe limbi.
- Podeaua de zgomot, cinci seminte: -0.000140 la surprisal, +0.000000 la reziduu.

## Cele doua capcane platite

1. **Directorul de scriere.** `bakeoff_trial.load_runs` ia FIECARE `*.csv` dintr-un director ca pe un
   model, iar `fuse_ab.pick_model` alege din bazinul asa format. Un fisier cu `B` gol cazut in
   `output/bakeoff_test/` ar fi intrat tacit in bazinul sistemului adoptat si ar fi mutat cifra
   publicata **fara sa crape nimic**. De aia rularile de C scriu in **`output/surprisal_test/`**, un
   director pe care nimic din conducta nu-l citeste, iar `analysis_c_frontiera` il ia prin cale.
2. **Fisierul PARTIAL.** `measure` scrie rand cu rand cu flush, deci un CSV citit in timpul rularii are
   un prefix de randuri. `reindex` pune NaN pe rest, `zscore` duce NaN in zero, si candidatul iese
   aproape constant fara sa crape. Asa a intrat `aya-expanse-8b-4bit` cu **255 din 5624** de randuri si
   a raportat `R_max` 0.0558 si `dR` -0.628, cifre care arata a rezultat. `load_c` are acum
   `n_astept` si refuza fisierele incomplete, cu mesaj.

## Doua lucruri de stiut inainte de a atinge blocul 1 din `analysis_shap_multi`

- HGB crapa cu `window shape cannot be larger than input array shape` pe coloane constante sau integral
  NaN **in interiorul unei limbi**: `surface_na` la ja si si, `freq_na` la si, `zipf` la si, `capital`
  la en/fr/it. Se scot per limba prin `utile()` si se declara in raport.
- Un surogat care primeste `A` si `B` recupereaza `p_fuz` la r = 0.997 si trimite tot restul la zero,
  fiindca amestecul e literal liniar in ele. Intrebarea "ce trasaturi duc predictia" are sens numai pe
  setul LEXICAL. Varianta cu A si B ramane, dar ca **control de fidelitate**.

`shap` NU e instalat in `ml_def` si nu s-a instalat. Alternativa folosita, reantrenarea fara coloana,
e chiar ce recomanda literatura in locul permutarii. Vezi [[atribuirea-cere-doua-masuri]].
