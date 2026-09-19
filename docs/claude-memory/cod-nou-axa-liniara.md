---
name: cod-nou-axa-liniara
description: "Ce s-a adaugat pe 26 aug 2026 pentru axa liniara: familii parametrice de regresori, doua analize noi, un driver; plus blocajul care explica de ce lasso n-a rulat niciodata si cinci capcane platite"
metadata:
  type: project
---

Codul din spatele lui [[axa-liniara-inchisa]]. Concluzia e acolo, aici e ce se refoloseste si ce m-a
costat timp.

## Blocajul care explica un gol de pe disc

`lasso` si `elasticnet` existau in `_make_regressor` de la sesiunea TabFM, dar mergeau prin
`_linreg_pred`, care **nu are imputer**. Sub `na_policy="mlsp"` coloanele de suprafata sunt NaN pe
`ja` si `si` (`surface_applicable` da False pe amandoua), iar Lasso da
`ValueError: Input X contains NaN`.

**Deci lipsa oricarui `e1_frozen_preds_reg-lasso*` nu insemna "n-a fost incercat", insemna "nu putea
rula".** Merita cautat tiparul: o optiune care exista in cod, nu are niciun artefact pe disc, si
nimeni nu-si aminteste sa fi picat. Fixul: amandoua trec pe `_pipe_pred`. `_linreg_pred` ramane
neatins pentru calea romaneasca.

## Ce e nou

`solution_bert.py`
  Fabrici: `_mk_ridge_a`, `_mk_lasso`, `_mk_enet`, `_mk_pls`, `_mk_huber`, `_mk_bayes`, `_mk_ard`,
  `_mk_svr_lin`, `_mk_krr_a`. Toate prin `_pipe_pred`, deci toate primesc imputerul.
  `_FAM` plus `regressor_kind(v)`: familii parametrice `ridge-a<A>`, `lasso-a<A>`, `krr-a<A>`,
  `pls-k<K>`, `enet-a<A>-l<zecimi>`. **Numele de pe linia de comanda E numele din fisier**, deci
  `<A>` se scrie fara punct (`30`, `1e-3`, `3e-2`) si nu exista nicio traducere care sa poata minti.
  Acelasi tipar ca `proj-N` la `--emb-tf`, si din acelasi motiv: alpha e continuu.
  `blend_lasso_hgb` langa `blend_ridge_et`. `blend_ridge_hgb` NEATINS (importat pe nume din 4 fisiere).
  Garda de forma in `_pipe_pred`: aplatizeaza (n,1) si REFUZA orice alta forma.

`finetune_xlmr.py`: `--regressor` trece pe `type=regressor_kind`, deci o greseala de scriere cade la
  parsare, inainte de embedding si de cele 12 potriviri.

`analysis_regresor.py`: `--extra NUME=CALE` (membru din alt spatiu, pentru ruta hibrida), `--membri`,
  `--top`, `--max-k`, verificarea de randuri intarita la cvintetul `META`, `zl` pre-calculat,
  `degenerate()`, plus doua sectiuni noi (inlocuirea jumatatii liniare; grila aleasa LOLO).

`analysis_regresor_multi.py` (NOU): acelasi lucru pe toate 3 encoderele deodata, plus sectiunea celor
  doua brate si tabelul de fuziune CITIT din rapoartele lui `fuse_ab`.

`make_reg_runs.py` (NOU): driver encoder x regresor, sare peste ce exista, cronometreaza, jurnal in
  `output/_reg_runs_log.csv`.

## Capcanele platite

1. **Enumerarea de submultimi e 2^k si a atarnat.** Cu grila de alpha pe disc `k=21`, adica 2 milioane
   de submultimi si ~10 milioane de `pearsonr`. A mancat un timeout de 600s. Fixul nu e sa-ti aminteşti
   sa dai un flag, e garda: `--max-k 3` implicit plus refuz explicit peste 200k combinatii.
2. **Un optim la MARGINEA grilei nu e un optim.** `lasso-a1e-3` si `pls-k16` erau capetele grilei
   initiale. Prelungita (lasso pana la 1e-4, pls la k4, ridge la 30000) `lasso-a1e-3` s-a dovedit
   interior, dar asta se afla numai daca prelungesti. Raportul avertizeaza acum singur.
3. **Predictie CONSTANTA, nu doar NaN.** Pe e5, `lasso` la alpha=0.03 zeroeste TOTI coeficientii pe
   sinhaleza si ramane interceptul: `std` exact 0, `zl` da `inf`, si `nan` s-a plimbat tacut in tot
   tabelul. Doua situri de reparat, nu unul: `zl` (podea pe deviatie) SI `rho_matrice` (`nanmean`,
   fiindca `pearsonr` pe o constanta da corect `nan`).
4. **Concluzia scrisa de mana s-a contrazis cu propriul tabel** dupa ce s-au adaugat doua rulari:
   spunea "amandoua ies SUB control" cand una ieșea peste. Exact
   [[constante-hardcodate-mint-dupa-renumerotare]]. Acum se calculeaza din `fz`. Si eticheta
   "cea mai mare diferenta" alegea pe `r`, nu pe `delta`, deci arata alt rand decat spunea.
5. **Corelatia pe TOATI candidatii e o capcana de interpretare.** Intre cele doua brate iese +0.606,
   ceea ce pare ca brațele vor acelasi lucru. E artefactul candidatilor catastrofali, prosti pe ambele.
   In banda utila e -0.041. Se raporteaza banda, nu totalul.

## Capcana care NU s-a materializat, si merita spus

`PLSRegression.predict` intoarce (n, 1) in sklearn vechi, si asta ar fi corupt tacit cele trei blocuri
taiate cu `p[:n_te]`. **Pe sklearn 1.9 aplatizeaza singur cand `y` e 1-D** (masurat: da `(200,)`).
Garda ramane, fiindca e gratis, dar nu prinde pe nimeni astazi. Prezis din cap, dezminti prin
masurare.

## Controalele, toate trecute

    md5 pe cele 4 fisiere adoptate            neschimbate cap-coada
    --regressor blend                          70c74c22218b7525d8e1d3d11b663f67
    make_a_blend --control (proj-394)          1.11e-16
    make_a_blend pe embeddingul PLIN (NOU)     1.94e-16
    blend_lasso_hgb vs make_a_blend            1.94e-16   (doua drumuri, acelasi numar)
    bratul adoptat de 0.6900 reconstruit (NOU) 8.88e-16   (media z pe limba a celor TREI blend-uri)
    identitatea de frontiera                   2.22e-16
