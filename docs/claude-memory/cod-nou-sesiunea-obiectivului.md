---
name: cod-nou-sesiunea-obiectivului
description: "Ce s-a adaugat pe 26 aug 2026 pentru sesiunea obiectivului: 4 clase de invelisuri de regresor, cele trei roluri, slack, optimismul de selectie; plus coliziunea libomp care omoara LightGBM fara traceback si controlul care nu e bit-exact"
metadata:
  type: project
---

Codul din spatele lui [[sesiunea-obiectivului-rezultatul]]. Concluzia e acolo, aici e ce se refoloseste
si ce m-a costat timp. Nimic adoptat nu s-a atins: `blend_ridge_hgb` neatins, `finetune_xlmr.py` zero
linii schimbate (fiindca `--regressor` trecea deja prin `regressor_kind`).

## Ce e nou

`solution_bert.py`
  `_lgbm_pred`, `_cat_pred` legate ca `_hgb_pred`, adica FARA imputer (trateaza NaN nativ).
  `_mk_rf`, `_mk_mlp`, `_mk_knn` prin `_pipe_pred`, adica CU imputer.
  `_tt_pred` plus `_TRANSF` (`id`, `rank`, `logit2`, `logit005`): transformarea tintei ca INVELIS peste
  orice regresor existent. Primeste si intoarce numai `ytr`, deci pragurile nu pot vedea limba tinuta
  deoparte **prin semnatura, nu prin disciplina**.
  `_ord_pred` (Frank-Hall, K-1 clasificatori binari, citire = suma probabilitatilor de supravietuire),
  `_orde_pred` (aceeasi, in unitati de complexitate prin mediile claselor), `_clf_pred` (multinomial).
  `_rs_pred` (subspatii aleatoare de coloane), `_w_pred` (ponderi `1 + c*|z(ytr)|`).
  `_COMP`: al doilea tuplu de familii parametrice, verificat INAINTE de `_FAM`, pentru numele compuse.
  `regressor_kind` capata **RECURSIE** pe numele de baza, altfel garantia "o greseala de scriere cade la
  parsare" se pierde tacit pentru `tt-rank-ridgee`.

`analysis_regresor.py`
  Cele TREI ROLURI (`X+hgb`, `ridge+X`, `ridge+hgb+X`), coloana `slack`, sectiunea pe CLASA DE MECANISM,
  si sectiunea de OPTIMISM DE SELECTIE (selectie LOLO peste toate submultimile enumerate).
  `MECANISM` / `ORDINE_M`: harta candidat -> clasa, scrisa in `_predictii_obiectiv.md` inainte de rulari.

`analysis_regresor_multi.py`: aceleasi trei roluri pe 3 encodere, rho fata de AMBII membri.
`make_reg_runs.py`: `--grup` pe clase de mecanism, plus `clasa` in jurnal.
`make_obi_sinteza.py` (NOU): sinteza regenerabila. Proza in script, **nicio cifra tastata de mana**.

## Capcanele platite

1. **LightGBM moare FARA traceback pe macOS dupa ce torch atinge MPS.** Procesul dispare, in jurnal
   rămâne doar `resource_tracker: leaked semaphore`. E coliziunea a doua incarcari de `libomp`.
   Masurat, ca sa nu se caute alt fix: `OMP_NUM_THREADS=1` NU ajuta, `KMP_DUPLICATE_LIB_OK=TRUE` NU
   ajuta, `n_jobs=2` cade la fel, **numai `n_jobs=1` merge**. Specific LightGBM: CatBoost cu
   `thread_count=-1` si RandomForest cu `n_jobs=-1` trec amandoua. **Tiparul de retinut: un log care se
   opreste dupa ultima linie de pregatire si nu are nicio excepție nu e un bug de Python, e o cadere de
   proces, si atunci se caută in biblioteci native.**
2. **Un CSV de predictii pe disc NU dovedeste o rulare terminata**: `frozen_trial_gap` scrie dupa
   FIECARE limba. Garda de randuri din `analysis_regresor.incarca` a prins fisierul partial al lui
   `rf-n300` (2748 din 5624) si a oprit analiza. Dar `make_reg_runs.py` sare peste ce exista pe disc,
   deci un fisier partial ar fi sarit la reluare.
3. **Controlul `rs-<baza>-f10-n1` NU e bit-exact, si prima formulare a docstringului mințea.**
   Sintetic float64 8.9e-16, sintetic float32 3.9e-07, **pe embeddingul real 4.3e-05**. Cauza:
   `X[:, c]` produce o copie ne-contigua, deci BLAS insumeaza in alta ordine, iar 774 de coloane
   colineare cu Ridge la alpha=300 amplifica. `tt-id-<baza>` iese la EXACT 0, fiindca atinge numai `y`.
   Cele doua controale separa curat un invelis care nu poate schimba nimic de unul care schimba ordinea.
4. **Poarta din cerere (`rho < 0.811` si `r > 0.53`) e prea permisiva**: pragul de `r` e SUB `r` al lui
   `hgb` insusi (0.5379 mediat), deci admite candidati mai slabi decat membrul de inlocuit. Din 7 care
   o trec, doar 2 trec criteriul exact de frontiera.
5. **O functie de shell in zsh a stricat argumentele** (`xlmr=` s-a pierdut din `--cai`), fara eroare
   vizibila pana la mesajul "lipseste". Constructiile cu multe cai se scriu in Python, cu liste de
   argumente explicite, nu in shell.
6. **`hgb-q50` e bit-identic cu `hgb-abs`** (max|diff| exact 0). Valorile din foi se calculeaza prin
   mediana ponderata la ambele, iar factorul 2 din gradient nu schimba argmaxul castigului de taietura.
   O rulare cheltuita ca sa se dovedeasca, nu ca sa se afle ceva nou.
7. **A doua propozitie scrisa de mana care s-a contrazis cu propriul tabel**: "si aici nu tine niciunul"
   despre cele doua brate. Era corecta pe axa liniara si a devenit falsa cand s-au adaugat inlocuitorii
   jumatatii de arbori. Acum se calculeaza. Vezi [[constante-hardcodate-mint-dupa-renumerotare]].
8. **Controalele apar ca "castigatori"** daca filtrul e `delta > 0` pe float: `rs-ridge-f10-n1` are
   delta zero pana la ~1e-16 si trecea in lista. Pragul e acum 1e-6 si clasa CONTROL se scoate explicit.

## Ce se refoloseste

`--grup obiectiv` reruleaza toata sesiunea. `make_obi_sinteza.py` se re-executa oricand si recalculeaza
fiecare cifra din artefacte. Numele compuse (`tt-`, `ord-`, `orde-`, `clf-`, `rs-`, `w-`) merg peste
ORICE regresor de baza, deci o combinatie noua nu cere cod nou.
