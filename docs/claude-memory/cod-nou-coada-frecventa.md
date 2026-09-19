---
name: cod-nou-coada-frecventa
description: "Codul scris 23-24 aug 2026 pentru coada: --freq-drop, --ctx-div, build_ctx_div.py si registrul CTX_DIV; plus capcana de patch care s-a platit de doua ori"
metadata: 
  node_type: memory
  type: project
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-24T09:10:25.154Z
---

Scris **23-24 august 2026**, pentru cele doua incercari pe coada. Amandoua au iesit negative, dar codul
ramane si e controlat.

## Ce s-a adaugat

- **`finetune_xlmr._freq_drop(X, dim_emb, p, seed)`** plus `--freq-drop P`. Anuleaza coloana de
  frecventa pe o fractiune `p` din randurile de ANTRENARE; blocurile prezise raman neatinse. Indexul
  lui zipf in X e **`dim_emb + 1`**: `_Xc` intoarce [embedding centrat] ++ [slot de fertilitate] ++
  [lexical], iar lexical are zipf pe coloana 0; `drop_len` scoate `lex[:, 1]`, deci nu muta zipf.
  La `p = 0` intoarce chiar obiectul primit, fara copie, deci calea veche e bit-exact neatinsa.
- **`build_ctx_div.py`**. Diversitate contextuala: in cate DOCUMENTE distincte apare cuvantul.
  Diferenta de cod fata de `build_freq_tail.numara` e **un `set()`**. Corpus in `data/wiki_ctx/`
  (4.5 GB, un shard `wikimedia/wikipedia` per limba), tabele in `data/ctx_div/`.
- **`mlsp_common.CTX_DIV`, `load_ctx_div()`, `ctx_div_safe()`**. Acelasi tipar ca `TAIL_FREQ` si
  `zipf_safe`, deci interschimbabile in `lexical`. Registru gol implicit: nicio cifra publicata nu
  trece prin ramura asta pana cand cineva cheama `load_ctx_div()`.
- **`solution_bert.lexical(..., ctxdiv=None|"plus"|"inloc")`**. `plus` adauga o coloana la coada dupa
  indicatori, `inloc` inlocuieste coloana 0 pastrand latimea. Cere `na_policy="mlsp"` si crapa altfel.
- **`finetune_xlmr --ctx-div {plus,inloc}`**, cu sufix propriu `_cd-plus` / `_cd-inloc`.

## Controalele, toate trecute

Fara niciunul din flaguri, `e1_frozen_preds_lemma_fert_inloc.csv` iese **bit cu bit**:
`shasum 30272f99eb1a024d5dc424cd4bb748ed6dc881f7`. Verificat de doua ori, o data dupa fiecare set de
modificari. Semnalul A al sistemului,
`e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv`, e `319d3f0ca25702c00e622c2cfd2e2e9da8b46a9d`.

O rulare `--frozentrial` completa costa **46 de secunde** cu embeddingurile in cache, mult sub ce se
presupunea. Deci o baleiere de 3 encodere x 3 valori e sub 8 minute.

## Doua capcane de proces, platite azi

1. **Un script de patch cu mai multe `assert` care crapa la ultimul NU scrie fisierul.** Patch-urile
   dinainte se pierd in tacere, si urmatoarea rulare cade cu o eroare fara nicio legatura
   (`TypeError: frozen_trial_gap() got an unexpected keyword argument 'ctx_div'`). **Se verifica
   intotdeauna cu `grep` ca patch-ul e in fisier**, nu ca scriptul a tiparit "ok". S-a platit de doua
   ori in aceeasi zi.
2. **Un CSV citit in timp ce o rulare de fundal inca scrie e un PREFIX de randuri**, si nu crapa nimic:
   `reindex` pune NaN pe rest si `zscore` le duce in zero. `make_enc_mean` a prins-o
   (`e5 n-are aceleasi randuri ca xlmr: 3490 fata de 5917`), `analysis_c_frontiera` nu o prinsese si
   raportase `R_max` 0.0558 pentru un fisier cu 255 din 5624 randuri. Are acum garda `n_astept`.
   O verificare `ls | wc -l` NU e suficienta: fisierul exista de la prima linie.

Vezi [[dropout-frecventa-inchis]], [[diversitatea-contextuala-inchisa]],
[[constante-hardcodate-mint-dupa-renumerotare]].
