---
name: cerere-verificare-parametri-tabfm-256
description: "25 aug 2026 seara - Alexandru vrea o sesiune viitoare care sa verifice daca TABFM_MAXFEAT=256/n_estimators=8 sunt cei mai buni parametri inainte sa investeasca ~8.8 ore de Colab, nu doar sa-i accepte ca alesi acum"
metadata: 
  node_type: memory
  type: project
  originSessionId: f3a4641f-367e-4f24-b328-31e01a9ad334
  modified: 2026-08-25T14:03:36.920Z
---

Deschis explicit la cererea lui Alexandru, dupa ce a ales `TABFM_MAXFEAT=256` intr-o sesiune
anterioara. Nu s-a rulat inca pe Colab cand s-a scris asta.

## Ce e deja setat in `tabfm_colab.ipynb`

    TABFM_MAXFEAT   160 -> 256   (celula 5)
    n_estimators    8            (neschimbat)
    DEST            preds_proj394_maxfeat256   (celula 4, ca sa nu suprascrie rularea de 142 min
                                                la MAXFEAT=160, deja terminata si consumata local)

Estimarea de cost e o EXTRAPOLARE, nu o masuratoare: 743s/cerere (reperul real, masurat la
MAXFEAT=160 pe acest T4) x (256/160)^2.70, unde exponentul 2.70 vine de pe M5 pe axa coloanelor,
NEVERIFICAT inca pe acest T4. Da ~44 min/cerere, ~8.8 ore total — peste pragul de 30 min/cerere.
Memoria (activari ~8.7 GiB, varf ~11.8 GiB din 14.6) e la fel extrapolata liniar din cele 5.45 GiB
masurate la 160, nu masurata direct. Celula 7 (calibrare) trebuie rulata din nou dupa schimbare,
inainte de celula 8, ca sa inlocuiasca extrapolarea cu o cifra reala.

## Ce ar trebui verificat inainte de a arde cele ~8.8 ore

1. **Daca merita deloc, dat fiind [[axa-regresorului-inchisa]].** Motivul principal pentru care
   axa a ramas inchisa e ca rho(tabfm, ridge/hgb) NU a scazut de la `proj-200` la `proj-394` — de
   fapt a urcat (0.829 mediu -> 0.864). Nu exista o tendinta masurata care sa spuna ca latimea mai
   mare (256 din 394, fata de 160 din 394) va decorela mai bine. Inainte de a investi timpul, merita
   intrebarea: exista vreun motiv sa credem ca DE DATA ASTA decorelarea se imbunatateste, sau
   experimentul repeta acelasi tipar si doar confirma inca o data ce se stie deja?
2. **Daca 256 e chiar cel mai bun punct pe curba cost/beneficiu**, sau daca un `MAXFEAT` mai mic
   (200, care era optiunea "moderata" cu ~4.5 ore si sub pragul de 30 min/cerere) sau un
   `n_estimators` mai mic la MAXFEAT=256 (ca sa reintri sub 30 min/cerere) ar da un raport mai bun.
3. **Cota saptamanala Colab** (~15-30 ore, dinamica, gratuit): 2.4 ore consumate deja azi + 8.8 ore
   noi ar putea sa nu incapa intr-o saptamana, sau sa forteze 2-3 sesiuni separate. Merita clarificat
   daca Alexandru are Colab Pro sau ramane pe gratuit, fiindca schimba tot calculul de buget.
4. **Daca celula 7, rulata dupa schimbare, confirma sau infirma extrapolarea** de mai sus (memorie
   SI timp) — raspunsul e necunoscut pana la o rulare reala.

## STARE 25 aug seara: checkpointul e SCRIS SI TESTAT, rularea nu a inceput

Cerinta de mai jos e **indeplinita**: codul, portile si testele sunt in
[[cod-nou-checkpoint-membru-tabfm]]. Pierderea maxima la o deconectare a coborat de la o cerere
intreaga (~46 min) la un membru (~5.3 min).

Doua lucruri s-au clarificat pe drum:

1. **Colab GRATUIT**, confirmat de Alexandru. Deci ~3-4 sesiuni de cate ~2.8h utile, nu una.
2. **Latimea reala e 272, nu 256** (crosses, vezi nota de cod). Calibrarea veche subestima memoria
   cu 6.25%. Celula 7 ruleaza acum cu `n_estimators=2` si citeste latimea din generator.

Estimarile cu care se compara ce iese din celula 7, recalculate pe latimile REALE (172 -> 272):

    per membru   ~5.3 min      per cerere   ~46 min      toate 12   ~8.9 ore
    varf         11-12 GiB din 14.6, plafon 13.4

## Calibrarea RULATA pe T4, 25 aug seara: totul verde, si o surpriza de cost

    latime vazuta de model   272   (fixul cu n_estimators=2 a functionat)
    incarcare model          280s din Drive (~23 MB/s; descarcarea directa ar fi probabil mai rapida)
    T= 3200   predict  49.9s   fit  3.4s   activari 4.98 GiB   finite 200/200
    T=14107   predict 265.7s   fit 10.0s   activari 7.91 GiB   finite 505/505
    varf                     3.08 greutati + 7.91 activari = 10.99 GiB din 14.6, marja 2.41
    memorie                  4.12 GiB ficsi (chunk) + 0.29 MB/rand = 2.07 tensori de etapa
                             <- patch-urile promit 2, deci se auto-verifica: SUNT instalate
    exponent pe randuri      1.13
    per membru 2.2 min | per cerere 18 min | toate 12: 3.5 ore

**Rularea a pornit cu configuratia decisa, nemodificata.** Nu s-a atins niciun buton.

**Punct de reluare:** `tabfm_bridge.py` e pus in Drive de Alexandru. Urmatorul pas e sa ruleze
celulele 1-6, apoi celula 7 (calibrarea), si sa dea output-ul inainte de celula 8. Scara de coborare
daca nu incape, in ordine, si primele doua NU ating cifrele: `TABFM_ATTN_GIB` la jumatate,
`TABFM_CHUNK` la jumatate, abia apoi `TABFM_MAXFEAT` un pas mic, si `n_estimators` doar daca
problema e timpul. Niciunul din primele doua nu ajunge in `setari.json`, deci se scriu de mana.

## Cerinta neaparata: checkpoint pe MEMBRU, nu doar pe cerere (INDEPLINITA, vezi mai sus)

Alexandru a cerut explicit checkpoint-uri, dat fiind ca la MAXFEAT=256 o cerere trece de 30 min
(pragul de siguranta). Ce exista deja: `ruleaza()` scrie fiecare `.npy` dupa ce cererea se termina
si sare peste cele gata la reluare — asta protejeaza intre cereri, NU in interiorul uneia.

Ce nu exista: checkpoint in interiorul unei cereri, pe membru de ansamblu. Verificat pe sursa reala
(`tabfm-venv/lib/python3.11/site-packages/tabfm/src/classifier_and_regressor.py:3009`,
`TabFMRegressor._batch_forward`): membrii ansamblului trec unul cate unul printr-o bucla interna
(`batch_size=1`), rezultatele se aduna intr-o lista si se concateneaza abia la final, in interiorul
unui singur apel `reg.predict(P)` din `ruleaza()`. Nu exista hook expus pentru asta.

Calea de implementat, dupa modelul patch-urilor deja existente din `instaleaza_patch_uri`: monkey-patch
pe `_batch_forward` (sau pe bucla din `predict`/`_predict_internal`), care sa scrie pe disc media
partiala a membrilor terminati dupa fiecare membru, si la pornire sa citeasca un checkpoint partial
existent si sa continue doar cu membrii ramasi inainte sa combine. Necesita si o cheie de identitate
pentru checkpoint-ul partial (similar cu `req_key`), ca sa nu se amestece un checkpoint partial cu
alta configuratie. Nu s-a scris inca acest cod — e exact ce ar trebui sa faca sesiunea viitoare
INAINTE de a rula cele ~8.8 ore, nu dupa.

## Context necesar pentru sesiunea viitoare

[[axa-regresorului-inchisa]] (motivul indoielii), [[cod-nou-tabfm-colab-fixat]] (starea notebook-ului,
cele trei bug-uri deja reparate si validate). Rularea la MAXFEAT=160 e completa si consumata local;
predictiile ei nu se sterg si nu se ating de rularea noua (DEST separat).
