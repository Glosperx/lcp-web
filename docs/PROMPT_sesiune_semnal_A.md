Vreau o sesiune de research pe semnalul A: sa testam mai multe modele de regresie, sa masuram
pentru fiecare (1) scorul r, (2) corelatiile intre modele, si (3) ce r iese din fuziunea finala cu
tot cu semnalul B. Vreau sa pastram TabFM in ansamblu.

Citeste intai memoria proiectului, in special `cerere-sesiune-jumatatea-liniara`,
`axa-regresorului-inchisa`, `tabfm-maxfeat256-rezultatul` si `criteriu-plat-mediaza-nu-alege`.

## Ce e DEJA masurat, si nu se reface

Axa "alt algoritm" a fost inchisa o data, dar toate variantele au schimbat jumatatea de ARBORI sau
au adaugat un al treilea membru. Cifrele, embedding plin, LOLO pe 10 limbi, `--lemma-freq --afeat
fert_inloc`:

    blend (Ridge300+HGB) 0.5778 | blend-et 0.5782 | extratrees 0.5691
    ridge 0.5520 | hgb 0.5472 | hgb-adanc 0.5321

    rho: ridge-hgb 0.811 | ridge-extratrees 0.858 | hgb-extratrees 0.914

Iar TabFM, pe `proj-394` (nu incape pe cele 774 de coloane):

    tabfm @MAXFEAT=256, n_estimators=8:  r 0.5673, rho(t,ridge) 0.900, rho(t,hgb) 0.873

Concluziile care NU se redeschid: capacitatea mai mare strica (`hgb-adanc` -0.046); familia de
arbori nu conteaza in blend (`blend-et` la +0.0004 de blend); si pe TabFM plafonul intregii axe e
+0.0011..+0.0026 in fuziune, sub bara de +0.0045, deci nu se mai cheltuie GPU pe el.

## Ce e GENUIN deschis, si de ce

**Jumatatea LINIARA a blend-ului n-a fost atinsa niciodata.** A fost `Ridge(alpha=300)` in absolut
toate variantele, iar `alpha` e mostenit si nu s-a re-potrivit sub LOLO. `lasso` si `elasticnet`
exista in `_make_regressor` dar nu exista niciun CSV `e1_frozen_preds_reg-lasso*`, deci n-au rulat
niciodata sub protocolul asta. Pe free-gate bat blend-ul (0.5688 / 0.5650 fata de 0.5512), alt
protocol deci cifrele nu se citeaza, dar ordinea e un semnal.

Motivul mecanic: `rho(ridge, hgb) = 0.811` e perechea cea mai decorelata din tot tabelul si e ce
duce toata valoarea blend-ului. Podeaua de rho de 0.80 n-a fost coborata de niciun candidat, dar
toti candidatii incercati erau NELINIARI. Un liniar rar (L1) are alt bias inductiv decat unul dens
(L2), deci e singura directie in care `rho(liniar, hgb)` ar putea cobori sub 0.81.

## Candidatii de testat

Liniari (jumatatea neatinsa): `lasso`, `elasticnet`, `ridge` cu grila de alpha aleasa LOLO, si
neincercatii: PLS, Huber, BayesianRidge/ARD, kernel ridge RBF, SVR liniar.
Neliniari, ca parteneri: `hgb` (incumbentul), `extratrees`, `tabfm-cache`.

## Cum se ruleaza eficient

`analysis_regresor.py` calculeaza r pentru media standardizata a TUTUROR submultimilor, deci
**ansamblurile ies gratis odata ce ai fiecare regresor rulat o singura data**. Deci:

    1. o rulare `finetune_xlmr.py --frozentrial --lemma-freq --afeat fert_inloc --regressor X`
       per candidat singur (minute, sklearn pur, zero GPU)
    2. `analysis_regresor.py` o data -> tabelul de r, matricea rho, toate ansamblurile, si curba
       de prag
    3. numai cele 2-3 ansambluri de top trec prin `fuse_ab.py`, care e partea scumpa in atentie

## Cum se pastreaza TabFM fara sa coste

TabFM exista doar pe `proj-394`, iar mutarea intregului A acolo costa **-0.0025 in fuziune**
(masurat: blend pe xlmr plin da 0.6828, pe proj-394 da 0.6803). NU muta tot. `make_a_blend.py`
mediaza CSV-uri cu aceleasi randuri, iar randurile coincid exact intre spatii (verificat pe
`split, idx, lang, token, context_id`). Deci ruta corecta e HIBRIDA: liniarul si arborii pe
embeddingul PLIN, TabFM din cache-ul `proj-394`.

Verificat deja: `mean(ridge_plin, hgb_plin, tabfm_proj394@256)` da fuziune **0.6827**, adica
-0.0001 fata de blend singur. TabFM intra gratis pe ruta asta, in loc de -0.0025.
Predictiile lui sunt in `output/e1_frozen_preds_tf-proj-394_reg-tabfm-cache_mf256_lemma_fert_inloc.csv`
(si varianta `_mf160`). Nu mai trebuie rulat nimic pe GPU.

## Poarta, si ea decide

`rho`, nu `r`. Un candidat cu r mai bun dar rho mai mare pierde; s-a intamplat de trei ori.
`analysis_regresor.py` aplica identitatea de frontiera

    r_ens = (suma r_i) / sqrt(k + 2 * suma_{i<j} rho_ij)

care nu e o aproximare ci o identitate algebrica pentru media standardizata (verificata la 1e-16 pe
limba), si tipareste pentru fiecare candidat `prag optimist` si verdictul TRECE/CADE.

## Capcane de respectat

- `blend_ridge_hgb` e importat pe NUME din patru fisiere. Nu se atinge; se adauga alaturi, dupa
  modelul lui `blend_ridge_et`.
- Conventia de control: rezerva plus md5 la fisierele adoptate, apoi o rulare `--regressor blend`
  care trebuie sa dea acelasi md5. Poarta interna `ref_r` e stinsa pe configuratia asta, deci
  verificarea se face PE FISIER.
- Alegerea intre configuratii se face LOLO, niciodata pe scorul de test.
- Daca mai multi candidati sunt la egalitate, se MEDIAZA, nu se alege unul. Regula e masurata de
  trei ori in proiect.
- `TABFM_CACHE` nu intra in numele construit de `_p()`, deci doua rulari tabfm se suprascriu tacit.

## Reperele fata de care se compara

Toate cu acelasi B (M3K), `--arm lolo --fit test --pick-split test`:

    blend pe xlmr PLIN                fuziune 0.6828     <- controlul pentru ruta hibrida
    blend pe proj-394                 fuziune 0.6803     <- controlul daca ceva ramane proiectat
    sistemul adoptat (3 encodere)     fuziune 0.690001
    bara pe fuziune                          +0.0045

## Ce vreau la final

Un tabel cu, pentru fiecare candidat si pentru ansamblurile de top: r pe A, rho fata de ceilalti
membri, verdictul portii, si r-ul fuziunii cu B pentru cele care trec. Plus comparatie PEREACHE cu
`--vs` fata de controlul potrivit, cu P(>0), fiindca diferentele sunt de ordinul 0.001 si media
singura nu spune nimic.
