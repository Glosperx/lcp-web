---
name: cod-nou-checkpoint-membru-tabfm
description: "25 aug 2026 - al cincilea patch din tabfm_bridge: checkpoint pe MEMBRU de ansamblu, cu poarta proba_checkpoint; plus descoperirea ca TABFM_CROSSES largeste latimea reala peste MAXFEAT (256 -> 272)"
metadata:
  type: project
---

Ce s-a scris ca sa poata rula [[cerere-verificare-parametri-tabfm-256]] la 256 de coloane, unde o
cerere trece de 40 de minute si protectia veche (un `.npy` per cerere) nu mai ajunge.

## Al cincilea patch, in `instaleaza_patch_uri`

Tinta e `TabFMRegressor._batch_forward`, nu un `forward` din `model.py`. Merge fiindca `batch_size`
e **1** (verificat pe instanta, nu presupus), deci bucla interna chiar trece membrii unul cate unul,
iar pe drumul PyTorch capetele buclei sunt pur numpy: `_predict_step_pytorch` intoarce
`out_t.float().cpu().numpy()`, si dupa taiere un membru e `[1, T_test, 1]` float32, adica 2-22 KB.

`_batch_forward` e decorat cu `@jt.typed`, dar `functools.wraps` pastreaza `__module__` pe
`tabfm.src.classifier_and_regressor`, deci garda existenta de captare a originalului il acopera si
pe el. `tinte` a devenit tuple de trei (nume, clasa, ATRIBUT), fiindca atributul nu mai e mereu
`forward`.

Cheia unui fisier de membru: `a{apel}_m{i}_{amprenta}.npy` sub `DEST/_ckpt/<req_key>/`. `apel`
numara chemarile lui `_batch_forward` intr-o cerere (una singura acum, mai multe cu `TABFM_NNLS`).
Amprenta e blake2b(8) peste formele, dtype-urile si octetii lui `(X_batch, y_batch, cat_mask, ds)`,
si sta in NUME deliberat: o nepotrivire devine "fisierul nu exista" si membrul se recalculeaza, in
loc sa se citeasca in tacere numerele altui membru. Costa ~15 ms per bloc de 15 MB.

Se scrie membrul INTREG, nu media partiala. Media ar cere un contor de ponderi ca sa poata fi
reluata, ar rupe `enable_nnls` (care are nevoie de membrii separati) si ar arunca ablatia pe
`n_estimators`, care asa iese gratis: media primilor k membri, fara nicio rulare noua.

Scris atomic, `.tmp.npy` + `os.replace`. `.npy` la coada fiindca `np.save` il adauga singur daca
lipseste, si atunci `os.replace` ar cauta alt fisier. Drive-ul montat chiar cade la mijlocul unei
scrieri, si un `.npy` trunchiat ar fi mai rau decat unul lipsa: ar trece de verificarea de existenta.

Contextul e `_CKPT = {"dir", "apel", "calc"}` plus context managerul `checkpoint_membri(dir)`, pus
in `ruleaza` in jurul lui `fit` SI `predict`. Cu `dir=None` patch-ul cheama originalul, deci proba
de dtype, calibrarea si orice alta predictie din proces raman neatinse. `TABFM_CKPT=0` il stinge.

## Poarta: `proba_checkpoint(model)`

Cele patru patch-uri de memorie se verifica fata de original pe tensori mici. Asta nu se poate:
intrebarea nu e daca aritmetica unui membru e aceeasi, ci daca membrul `i` regenerat maine din
`EnsembleGenerator` e ACELASI. Nu se citeste din cod, se masoara. Aceeasi predictie de patru ori:

    p0  checkpoint stins             reperul
    p1  director gol                 scrie cate un fisier per membru
    p2  dupa stergerea ULTIMULUI     recalculeaza EXACT 1
    p3  cu toate pe disc             ZERO treceri prin model

`_CKPT["calc"]` (membri chiar calculati) e ce distinge o reluare adevarata de una care a
recalculat totul in tacere si a iesit la fel. Cerinta pe numere e `array_equal`, exact.

## Ce s-a masurat local, pe modelul adevarat (cache 6.1 GB, CPU/float32)

    poarta               3 scrise | partiala 1 | completa 0 | toate 4 bit-identice
    cap la cap prin ruleaza, cu doua feluri de cadere (cerere pierduta, si cerere pierduta
                         cu un membru sters): 4/4 .npy finale BYTE-IDENTICE dupa reluare
    control de nepatare  TABFM_CKPT=0 da aceleasi md5 ca rularea cu checkpoint

## Descoperirea care schimba calibrarea: latimea reala nu e MAXFEAT

`TABFM_CROSSES=sqrt` da `int(sqrt(min(n_col, MAXFEAT)))` coloane in plus DOAR membrilor impari
(alocarea "split" din `_get_member_n_features_list`), iar `_transform_features` umple apoi **toti**
membrii la `max_features`, adica la latimea celui mai lat. Masurat direct:

    n_estimators=1  ->  Xs_all (1, T, 256)   k_crosses [0]
    n_estimators=2  ->  Xs_all (2, T, 272)   k_crosses [0, 16]
    n_estimators=8  ->  Xs_all (8, T, 272)   k_crosses [0,16,0,16,0,16,0,16]

Celula 7 de calibrare rula cu `n_estimators=1`, deci masura la 256 memoria unei rulari care merge
la 272: **subestimare de 6.25% fix pe termenul care decide daca incape**. La MAXFEAT=160 acelasi
tipar a dat 172 in loc de 160 (7.5%) si a incaput oricum; la 256 marja e mai stramta. Fix: `N_CAL=2`
in celula 7, minimul care aduce un membru impar in lot, plus `HC_REAL` citit din
`reg.ensemble_generator_.ensemble_configs_`, nu din variabila de mediu.

Bonus platit in aceeasi celula: `fit` (preprocesare CPU) si `predict` (GPU) se cronometreaza acum
separat. Amestecate, partea de CPU intra de `n_estimators` ori in estimare in loc de o data.

## Restul modificarilor din notebook

Garda de prospetime din sectiunea 4 cauta si `proba_checkpoint` si `_bf_ckpt` (acelasi motiv ca
`_attn_econom`: o copie veche in Drive nu crapa, doar pierde tacut protectia). `shutil.make_archive`
isi ia numele din `DEST`, era fixat pe `preds_proj394`.

Vezi [[tabfm-pe-gpu-memorie-si-dtype]], [[cod-nou-axa-regresorului]], [[axa-regresorului-inchisa]].
