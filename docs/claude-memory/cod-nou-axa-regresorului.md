---
name: cod-nou-axa-regresorului
description: "Ce s-a adaugat pe 24 aug 2026 pentru axa regresorului si TabFM: --regressor, --emb-tf proj-N, --export-blocks, puntea TabFM, doua rapoarte; plus sase capcane platite"
metadata:
  type: project
---

Codul din spatele lui [[axa-regresorului-inchisa]]. Concluzia e acolo, aici e ce se poate refolosi
si ce m-a costat timp.

## Ce e nou

`solution_bert.py`
  `_make_regressor` are acum 10 optiuni: `blend` (implicit, bit-exact), `lasso`, `elasticnet`,
  `ridge`, `hgb`, `hgb-adanc`, `extratrees`, `blend-et`, `tabfm-cache`. Plus `_pipe_pred` (imputer
  + scaler, pentru tot ce nu e HGB), `_hgb_pred`, `blend_ridge_et`, `_tabfm_cache_pred`.
  `blend_ridge_hgb` e NEATINS: e importat pe nume din patru fisiere.

`finetune_xlmr.py`
  `--regressor` pe `--frozentrial` si `--frozenmulti`; sufixul `_reg-<nume>` in `_p()`, gol la
  `blend` deci caile publicate raman literal aceleasi; `--regressor` intra si in garda `canonic`.
  `--emb-tf proj-N`: **REDUCE latimea** la N componente, spre deosebire de `pca1`/`pca5` care doar
  scad componente si pastreaza latimea.
  `--export-blocks CALE.npz`: scrie blocurile si se opreste, fara sa potriveasca nimic.

`tabfm_bridge.py` (partea comuna, la nivel de modul cere numai numpy, deci importabil din ambele
venv-uri), `tabfm_runner.py` (linia de comanda), `tabfm_colab.ipynb` (GPU).
  **25 aug**: `tabfm_bridge.instaleaza_patch_uri()` tine acum CELE PATRU patch-uri de memorie
  (erau in celula 5 a notebook-ului) si e chemata din `ruleaza`, care REFUZA sa porneasca daca
  verificarea atentiei cade. Praguri diferite pe scop: exact 0 pentru cele trei de tensori,
  1e-5 pentru atentie (masurat 7.2e-07). Garda pe `forward.__module__` opreste captarea unui
  patch drept "original". Butonul nou e `TABFM_ATTN_GIB`, implicit 0.5.
`analysis_regresor.py --spatiu _tf-proj-N`, `analysis_tabfm_poarta.py`.

Venv izolat: `~/.local/share/tabfm-venv`, `pip install "tabfm[pytorch]" safetensors`.

## Cele doua porti, si de ce exista amandoua

**Cheia de cerere** (`req_key`, blake2b peste formele si octetii lui `Xtr, ytr, Xpredict`). Capatul
care ruleaza TabFM RECONSTRUIESTE cererile din blocuri. Daca ar reconstrui un singur rand altfel,
cheia nu corespunde si `tabfm-cache` refuza sa scrie. Nu e o speranta, e o poarta.

**`setari.json`** in folderul de predictii. Cheia acopera INTRAREA, nu si `n_estimators`. Fara
poarta asta, o reluare cu alta setare ar sari peste fisierele existente si ar amesteca tacit doua
configuratii intr-un singur set. `dtype` se anunta dar nu refuza; restul refuza.

## Capcanele platite

1. **`np.savez` cu `lang.astype(str)`** pe un array de obiecte pandas ramane `object`, iar `np.load`
   il refuza fara `allow_pickle`. Se scrie `np.asarray(list(v), dtype="U16")`.
2. **Scrierea inapoi dupa `emb_transform`** presupune aceeasi latime (`Een[oken] = Een2`). `proj-N`
   intoarce blocuri mai inguste si crapa acolo: se realoca si se umple numai pe `ok`.
3. **Un subproces per potrivire plateste incarcarea modelului de 12 ori.** De aceea puntea e
   export -> o rulare -> import, nu apel direct. Smoke-ul initial a expirat exact pe asta.
4. **`torch.where(mask, x, zeros)` NU e `x.mul_(mask)`** cand `x` are `inf`: `inf * 0 = NaN`.
   Se scrie `x.masked_fill_(~mask, 0)`. Am dat patch-ul gresit lui Alexandru si l-a costat o
   sesiune de Colab. Verificarea corecta e `torch.equal` pe un caz cu `inf`, nu doar pe date curate.
5. **`y` catre TabFM trebuie float32.** `tabfm/src/classifier_and_regressor.py:1801` face
   `.to(device)` INAINTE de verificarea de dtype de pe linia urmatoare, iar MPS refuza float64.
6. **`safetensors` nu vine cu `tabfm`**, dar `huggingface_hub` il foloseste la incarcare si crapa
   cu `NameError` fara el.

7. **O celula de notebook se desincronizeaza tacit de fisierul din proiect.** Patch-urile stateau
   in celula 5; notebook-ul se ruleaza din VSCode pe kernel Colab, tamponul din editor era vechi,
   si rularea a mers cu atentia NEPATCH-UITA. Semnul care o dovedeste, si care merita cautat
   mereu: cadrul din traceback era `model.py:129`, adica fisierul BIBLIOTECII cu codul original.
   Daca patch-ul era instalat, cadrul ar fi aratat fisierul celulei si numele `_attn_econom`.
   Doua cicluri pierdute. Fixul e structural: codul in `tabfm_bridge.py`, apel din `ruleaza`,
   plus verificarea din celula 3 care cauta `_attn_econom` in `inspect.getsource`.

## Conventia de control care a mers si merita repetata

Inainte de a atinge codul semnalului A: copie de rezerva la cele trei fisiere adoptate plus md5, apoi
o rulare cu `--regressor blend` care trebuie sa dea acelasi md5. Poarta interna `ref_r` e stinsa pe
configuratia lui A (`--lemma-freq --afeat fert_inloc`), deci verificarea TREBUIE facuta pe fisier.
Rezerva e in `output/_rezerva_reg/`.

## Costul TabFM, masurat pe M5/MPS float32, `n_estimators=2`

Liniar in randuri, **supra-patratic in coloane**. La 2000 de randuri: 100 col 25s, 200 col 68s,
400 col 441s; la 400 col, 2000 -> 4000 randuri e 441s -> 850s. Deci parghia de cost e LATIMEA.
Rularea completa pe `proj-200`, 12 potriviri pe ~13.5k randuri de context: **79 de minute**.
Blocul de prezis se chunk-uieste, deci `en_only_test` (5624 de randuri) a costat 311s, nu de 5.6 ori
cat o limba cum estimasem.
