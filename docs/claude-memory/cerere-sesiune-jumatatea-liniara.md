---
name: cerere-sesiune-jumatatea-liniara
description: "INCHISA 26 aug 2026 - sesiunea s-a facut, rezultatul e in [[axa-liniara-inchisa]]. Premisa era corecta (podeaua de rho se rupe) dar castigul nu transmite; sistemul ramane 0.690001."
metadata:
  type: project
---

**INCHISA. Rezultatul: [[axa-liniara-inchisa]], codul: [[cod-nou-axa-liniara]]. Fiecare punct al
cererii are raspuns masurat. Ce urmeaza mai jos e cererea ca atare, pastrata pentru context.**

Cerut dupa ce axa TabFM s-a inchis definitiv ([[tabfm-maxfeat256-rezultatul]]). Formularea lui:
"in loc de ridge sa folosim altceva".

## De ce NU e o redeschidere a lui [[axa-regresorului-inchisa]]

Tot ce s-a masurat vreodata pe axa aia a schimbat **jumatatea de arbori** sau a adaugat un al
treilea membru: `hgb`, `hgb-adanc`, `extratrees`, `blend-et`, `tabfm`. **Jumatatea liniara a ramas
`Ridge(alpha=300)` in toate.** Nu exista niciun CSV `e1_frozen_preds_reg-lasso*` sau
`reg-elasticnet*`, deci n-au fost rulate niciodata sub LOLO.

## De ce e o ipoteza cu motiv, nu doar o casuta nebifata

1. **`lasso` si `elasticnet` BAT blend-ul pe free-gate.** Din docstring-ul lui `_make_regressor`
   (`analysis_lasso.py`): lasso 0.5688 / elasticnet 0.5650 fata de blend 0.5512. Protocol diferit,
   deci cifrele nu se citeaza, dar ordinea e un semnal.
2. **rho(ridge, hgb) = 0.811-0.815 e perechea care duce toata valoarea blend-ului.** Podeaua de rho
   de 0.80 n-a fost coborata de niciun candidat, dar toti candidatii incercati erau neliniari.
   Un liniar RAR (L1) are alt bias inductiv decat unul dens (L2), deci e singura directie in care
   rho(liniar, hgb) ar putea cobori sub 0.81.
3. **L1 transfera mai bine cross-lingual**, ceea ce e exact regimul LOLO.
4. **`alpha=300` n-a fost re-potrivit niciodata sub LOLO.** E mostenit.

## Primele teste, in ordine de cost (toate FARA GPU, sklearn pur, minute)

    1. --regressor lasso si elasticnet, singuri, sub LOLO      -> r si rho fata de hgb
    2. daca rho(L1, hgb) < 0.81: blend nou, L1 + HGB           -> cere o functie noua in
                                                                  solution_bert.py, dupa modelul
                                                                  lui `blend_ridge_et`
    3. grila de alpha pentru ridge si lasso, aleasa LOLO
    4. alte liniare neincercate: PLS, huber, kernel ridge

## Cum se pastreaza TabFM fara sa coste: ruta HIBRIDA (verificata 26 aug)

Alexandru a cerut explicit sa pastram TabFM. Naiv, asta ar insemna mutarea intregului A pe
`proj-394`, care costa **-0.0025** in fuziune. Nu e nevoie: `make_a_blend.py` mediaza CSV-uri cu
aceleasi randuri, iar randurile coincid EXACT intre embeddingul plin si `proj-394` (verificat pe
`split, idx, lang, token, context_id`, toate identice, 5917 randuri).

Deci liniarul si arborii raman pe embeddingul PLIN si numai TabFM vine din cache-ul `proj-394`.
Masurat: `mean(ridge_plin, hgb_plin, tabfm_proj394@256)` da A 0.5829 si fuziune **0.6827**, adica
-0.0001 fata de blend singur (0.6828). **TabFM intra gratis pe ruta asta, in loc de -0.0025.**

Predictiile lui sunt deja pe disc si nu mai cer GPU:
`output/e1_frozen_preds_tf-proj-394_reg-tabfm-cache_mf256_lemma_fert_inloc.csv` (si `_mf160`).

## Eficienta: ansamblurile ies gratis

`analysis_regresor.py` calculeaza r pentru media standardizata a TUTUROR submultimilor. Deci se
ruleaza fiecare candidat O SINGURA DATA ca regresor singur, apoi matricea rho si toate ansamblurile
ies dintr-un singur apel, si numai top 2-3 trec prin `fuse_ab.py`.

Promptul scris pentru sesiunea aia: `PROMPT_sesiune_semnal_A.md` in radacina proiectului.

## Poarta, si capcanele de respectat

Aceeasi ca peste tot: `analysis_regresor.py`, identitatea de frontiera, si **rho, nu r**, e cifra
care decide. Un candidat cu r mai bun dar rho mai mare pierde — s-a intamplat de trei ori.

Capcane care se aplica direct aici:
- [[criteriu-plat-mediaza-nu-alege]]: daca mai multi candidati sunt la egalitate, se mediaza, nu se
  alege. Masurat de trei ori.
- [[bifurcatii-de-declarat]]: alegerea intre configuratii se face LOLO, nu pe scorul de test.
- Conventia de control din [[cod-nou-axa-regresorului]]: rezerva + md5 pe fisierele adoptate, apoi
  o rulare `--regressor blend` care trebuie sa dea acelasi md5.
- `blend_ridge_hgb` e importat pe nume din patru fisiere: **nu se atinge**, se adauga alaturi.

## Unelte deja existente

`--regressor` in `finetune_xlmr.py` (`--frozentrial` si `--frozenmulti`), sufixul `_reg-<nume>`;
`analysis_regresor.py --spatiu` pentru r, rho si curba de prag; `make_a_blend.py` pentru orice A
compus din CSV-uri (control provat la 1.11e-16); `fuse_ab.py --a-set ... --vs` pentru comparatia
perechea in fuziune.

Reperele fata de care se compara, pe embeddingul PLIN, acelasi B (M3K), `--arm lolo --fit test
--pick-split test`: blend da fuziune **0.6828**, iar sistemul adoptat (3 encodere) e **0.690001**.
