---
name: tabfm-pe-gpu-memorie-si-dtype
description: "TabFM are 1.65 miliarde de parametri: float16 da NaN mereu, float32 NU incape pe T4, si n_estimators costa timp nu memorie; plus formula de buget masurata"
metadata:
  type: project
---

Masurat pe 24 aug 2026, cand s-a incercat mutarea lui TabFM pe Colab. Completeaza
[[cod-nou-axa-regresorului]] (unde e puntea) si [[axa-regresorului-inchisa]] (unde e concluzia).

## Modelul nu e mic

Configuratia REALA din checkpoint nu seamana cu implicitele din semnatura `TabFM.__init__`:
`embed_dim=256` (nu 8), `icl_num_blocks=24` (nu 2), `icl_dim=2048`, FFN 8192.
`model.safetensors` = **6.59 GB**, adica 1.65 miliarde de parametri.

Greutati pe placa: **6.14 GiB in float32, 3.07 in bfloat16** (confirmat empiric, nu doar calculat).

## float16 e o rulare moarta, pe orice placa

Nu e o precizie mai proasta, e NaN garantat: 0 din 150 de predictii finite, la fel pe MPS si pe
CUDA, cand float32 si bfloat16 dau 150/150 si difera intre ele cu 0.016. Mecanismul, localizat cu
hook-uri pe module: reziduul stivei ICL ajunge la ~4300 la
`icl_predictor.tf_icl.blocks.9.attn.out_proj`, iar `linear2` din FFN trece de 65504. Eroarea arata
ca o problema de date (`finite 0`), de asta e inselatoare. `tabfm_bridge.py` il refuza explicit.

## Pe T4 nu incape in float32

Fiecare etapa tine `[1, T, HC, 256]`. Cu `T=14107` si `A` marimea lui, `ColEmbedding.forward` are
**4A** vii deodata (intrarea, copia din `permute().reshape()`, lista lui `torch.cat`, iesirea).
Pe 14.6 GiB utilizabili: float32 la HC=320 cere 23.4 GiB, la HC=128 inca 13.0. **bfloat16 e
obligatoriu**. Era si lucrul incert pe Turing (cuBLAS cere capability 8.0 pentru GEMM bf16), dar
nu mai e: vezi sectiunea urmatoare.

Patch-urile din `tabfm_colab.ipynb` duc 4A la 2A pe `ColEmbedding` si 3A la 2A pe
`RowInteraction`, verificate bit-identic prin modelul real.

## Masurat pe T4 (24 aug): bf16 MERGE, si memoria nu e o lege de putere

**bf16 pe Turing e inchis, merge.** Pe T4 (capability 7.5) checkpointul se incarca la 3.07 GiB si
proba da 200/200 finite la doua adancimi. Deci nu mai e nevoie de L4 sau A100 pentru bratul A.

**Varful e dominat de ATENTIA ICL, care e PATRATICA in randuri.** `ICLearning.forward` ruleaza tot
contextul ca o singura secventa si `tf_icl` e atentie peste RANDURI, cu 16 capete: matricea de
scoruri e `[1, 16, T, T]`, adica **5.93 GiB in bf16 la T=14107**, iar drumul `math` al lui SDPA
(ales fiindca `attn_mask` e tensor dens) tine doua copii deodata. De aici OOM-ul real:
`Tried to allocate 5.93 GiB ... 11.38 GiB in use`.

**`TABFM_MAXFEAT` nu e latimea pe care o vede modelul.** Cu `TABFM_CROSSES=sqrt`, membrii impari
primesc `int(sqrt(MAXFEAT))` coloane in plus, iar lotul se umple la latimea celui mai lat, deci
TOTI membrii merg la `MAXFEAT + int(sqrt(MAXFEAT))`: 160 -> 172, 256 -> 272. Orice buget de memorie
calculat pe MAXFEAT iese cu 6-8% optimist. Detaliile si fixul din celula de calibrare:
[[cod-nou-checkpoint-membru-tabfm]].

**Termenul de atentie ICL nu se atinge de latime deloc.** Latimea e deja colapsata inainte de stiva ICL, si
`row_interactor_2` iese pe `[B, T, num_cls*e]`. Coborarea latimii nu ajuta la OOM-ul de acolo.

**Capcana de extrapolare, platita.** Doua probe la T=1700 si T=3200 dau 3.45 si 3.70 GiB de activari,
adica +7% pentru +88% de randuri. De aici doua concluzii, amandoua gresite: podeaua `max(em, 1.0)`
din notebook a facut din 0.111 un 1.00 si a cerut `MAXFEAT` 96, iar potrivirea afina pe care am
facut-o eu a dat 8.59 GiB si "incape". Motivul comun: la T sub ~4000 termenul `T^2` inca e mic
(0.17 GiB la 1700, 0.61 la 3200), deci NU se vede in doua puncte mici. **Sub 4000 de randuri
memoria lui TabFM minte despre ce se intampla la 14000.** Regula: se masoara la T real, nu se
extrapoleaza; celula de buget o face acum.

**Al patrulea patch, cel care rezolva.** In `MultiheadAttention.forward`: (1) masca lui TabFM e mereu
un PREFIX de chei, deci se taie `k` si `v` la `train_size` si masca dispare, ceea ce lasa SDPA sa
aleaga nucleul mem-efficient care nu materializeaza nimic; (2) plasa de siguranta care taie pe
intervale de query, exacta fiindca softmax e pe randul de query. Verificat pe 64 de cazuri (cu
si fara masca, prefix uniform, prefix variabil, masca rarefiata, cu si fara taiere): **7.2e-07 in
float32**, deci nu bit-identic ca celelalte trei, fiindca SDPA alege alt nucleu pentru alta forma.
Pragul lui e 1e-5, separat de pragul de exact zero al celorlalte. Toate patru stau acum in
`tabfm_bridge.instaleaza_patch_uri()`, chemata din `ruleaza`, care refuza sa porneasca fara cel
de atentie; capcana care a impus mutarea e in [[cod-nou-axa-regresorului]].

## Exponentul 2.70 pe coloane NU se transfera de pe M5 pe T4 (masurat 25 aug)

Formula de buget de mai jos e masurata pe M5/MPS la **2000 de randuri**, unde coloanele domina.
Pe T4 la **14107 randuri** regimul e altul si exponentul se prabuseste:

    la MAXFEAT=160 (latime reala 172)   ~92s per membru la T=14107
    la MAXFEAT=256 (latime reala 272)   ~133s per membru la T=14107
    exponent real = ln(133/92) / ln(272/172) = 0.79      (pe M5: 2.70)

Costul e **sub-liniar in coloane** acolo, nu supra-patratic. Motivul e acelasi care explica varful
de memorie: la T mare domina atentia ICL, patratica in randuri si **oarba la latime**. Consecinta
practica: la numarul asta de randuri **latimea e aproape gratis pe T4**, deci un buget de timp
calculat cu 2.70 iese de ~2.5 ori prea pesimist (8.9 ore prezise, 3.5 masurate).

Regula care ramane: exponentul se remasoara pe placa pe care rulezi, la T-ul real. Celula 7 din
notebook o face acum si pentru randuri (`et`), si tipareste cifra per MEMBRU tocmai ca sa se poata
compara cu reperul precedent.

## n_estimators costa TIMP, nu memorie

`TabFMRegressor` are `batch_size=1`, deci membrii trec prin model unul cate unul. Varful e al unui
singur membru oricat de mare il pui. Butoanele de memorie sunt `TABFM_MAXFEAT`, `TABFM_CHUNK` si
numarul de randuri. Sfatul invers, scris initial in notebook, era gresit.

## Formula de buget, din rularea locala incheiata

12 cereri in 79 de minute la 206 coloane si `n_estimators=2`, adica **3.3 min pe membru pe cerere**:

    min/cerere = 3.3 x (MAXFEAT/206)^2.70 x n_estimators

La buget fix, **ingust-si-multi bate lat-si-putini**: 160 de coloane costa 0.51 din cat costa 206,
deci incap de doua ori mai multi membri, si subesantionarea de coloane decoreleaza in plus. Atentie
la capcana in care am cazut o data: `n_estimators` local a fost **2**, nu implicitul de 8, si
presupunerea gresita a facut estimarea de 4 ori prea optimista.

## Butoane cu efect gratis

`norm_methods` imparte cei `n_estimators` membri peste familiile de preprocesare (`none`, `power`,
`quantile`, `quantile_rtdl`, `robust`), nu adauga treceri prin model. `n_feature_crosses`/
`n_svd_features` merg doar la membrii impari (alocarea "split"), deci ~jumatate din cat par.
`enable_nnls` costa ~2x (inca un pasaj), dar splitul lui de validare se ia din `Xtr`, deci e curat
sub LOLO.
