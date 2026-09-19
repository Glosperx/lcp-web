---
name: axa-regresorului-inchisa
description: "25 aug 2026 - axa 'alt algoritm de regresie pentru A' RAMANE inchisa dupa un al doilea test, de data asta pe fuziunea REALA (fuse_ab.py): ridge+tabfm bate ridge+hgb doar in fuziune, nu invers, cu -0.0006"
metadata: 
  node_type: memory
  type: project
  originSessionId: f3a4641f-367e-4f24-b328-31e01a9ad334
  modified: 2026-08-25T13:48:18.808Z
---

Intrebarea a fost: ar da alt algoritm de boosting mai mult decat HGB pe semnalul A, concret TabFM de
la Google. Raspuns masurat, **nu se redeschide fara un motiv nou**.

## Corectia factuala

TabFM (Google Research, iulie 2026, `google-research/tabfm`, PyPI `tabfm`) **NU e boosting**. E
atentie pe randuri si coloane in stil TabPFN plus invatare in context in stil TabICL: la `fit` nu
potriveste parametri, retine blocul de antrenare ca CONTEXT si il reciteste la fiecare predictie.

## Cifrele, encoder xlmr, `--lemma-freq --afeat fert_inloc`, LOLO pe 10 limbi

Pe embeddingul PLIN (774 de coloane), din `output/e_regresor_a.md`:

    blend (Ridge300+HGB)  0.5778   incumbentul
    blend-et              0.5782   +0.0004
    extratrees            0.5691   -0.0087
    ridge singur          0.5520   -0.0258
    hgb singur            0.5472   -0.0306
    hgb-adanc (depth 6)   0.5321   -0.0457

Pe `proj-200` (TabFM nu incape pe 774, vezi mai jos), din `output/e_regresor_a_proj-200.md`:

    blend  0.5697 | ridge 0.5613 | hgb 0.5323 | **tabfm 0.5122**

## Cele trei lucruri care inchid axa

1. **Capacitatea mai mare STRICA.** `hgb-adanc` pierde 0.046. Bratul nu e limitat de capacitate.
2. **Familia de arbori nu conteaza in blend.** ExtraTrees singur bate HGB singur cu +0.022 (bagging
   peste boosting pe spatiu dens), dar `blend-et` e la +0.0004 de blend. Valoarea blend-ului e
   decorelarea liniar/arbore, si orice arbore o produce la fel.
3. **Podeaua de rho e 0.80.** Peste cinci algoritmi cu biasuri inductive complet diferite, corelatia
   nu coboara sub 0.80. TabFM, cel mai diferit dintre toti, sta la 0.829 — adica exact cat sta
   `ridge` fata de `hgb`. Pragul cerut de frontiera la r=0.51 e ~0.67.

Cel mai bun ansamblu posibil din tot ce s-a rulat, `ridge+hgb+extratrees`, da **0.581763**, adica
+0.0065 peste blend. Bara e +0.0174. **TabFM ca al treilea membru SCADE blend-ul cu -0.0033.**

## De ce e un rezultat, nu un esec

Modelele fundationale tabulare isi raporteaza castigurile pe TabArena, unde coloanele sunt eterogene
si au sens semantic. Aici X e 768 de dimensiuni dense de embedding plus 6 lexicale — regimul in care
priorul lor (tabele sintetice din modele cauzale structurale) nu are de unde sa muste. Avem
contra-exemplul cu poarta cantitativa. **Pe sinhaleza TabFM da 0.0049**, fata de 0.2075 la ridge.

## Codul

Ce s-a adaugat, cele doua porti si cele sase capcane platite: [[cod-nou-axa-regresorului]].
Controlul de reproducere trece bit-exact, deci nimic adoptat nu s-a miscat.

Vezi [[transmisia-a-fuziune-masurata]], [[criteriu-plat-mediaza-nu-alege]],
[[frontiera-e-identitate-nu-aproximare]], [[sistemul-e-0690001-m3k]].

## Follow-up 25 august: retestat pe `proj-394`, cu fuziune REALA, nu doar cu A singur

Motivul redeschiderii partiale: [[cod-nou-tabfm-colab-fixat]] a facut posibila o rulare TabFM tunata
(n_estimators=8, `TABFM_MAXFEAT=160`, 4 familii de normalizare) pe `proj-394` (nu `proj-200` ca mai
sus), pe un T4 real. Merita cifre noi fiindca tuning-ul de decorelare (norm-uri multiple, subesantion
de coloane) nu existase la prima masuratoare.

**Pe A singur, cifrele urca fata de proj-200, dar rho nu scade:**

    blend 0.5749 | ridge 0.5627 | hgb 0.5326 | tabfm 0.5541 (fata de 0.5122 pe proj-200)
    rho(tabfm, ridge)=0.877  rho(tabfm, hgb)=0.851  (fata de 0.829 mediu pe proj-200 — MAI SUS, nu mai jos)

**Local, `ridge+hgb+tabfm`=0.576436 bate blend cu +0.0015** (peste 0.581763 al lui `ridge+hgb+extratrees`
de mai sus, dar tot sub bara de +0.0174). Verdictul scriptului: `tabfm r 0.5541 rho 0.864 prag 0.781 -> CADE`.

**Testul care conteaza, prin `fuse_ab.py` real, acelasi B (M3K), acelasi protocol (`--arm lolo --fit
test --pick-split test`), doar A variaza:**

    A = ridge+hgb          (control)   fuziune 0.6803
    A = ridge+tabfm        (fara hgb)  fuziune 0.6797   (-0.0006 fata de control)
    A = ridge+hgb+tabfm    (toate 3)   fuziune 0.6805   (+0.0002 fata de control)

**Raspuns direct la intrebarea care a motivat redeschiderea** ("ar bate tabfm cifra lui hgb ca partener
al lui ridge?"): NU. `ridge+tabfm` iese SUB `ridge+hgb`, desi pe A singur cele doua sunt aproape identice
(0.5747 vs 0.5749) — diferenta vine din rho mai mare al lui tabfm fata de ridge (0.877) decat al lui hgb
(0.815), nu din calitatea predictiei. Câstigul de +0.0002 al variantei cu toate trei confirma aproape
exact estimarea teoretica facuta din factorul de transmisie (0.09-0.26 x castigul pe A).

**De ce mai multa antrenare pe Colab (mai multe coloane, mai multi `n_estimators`) probabil nu schimba
verdictul**: trecerea 200->394 coloane a URCAT rho (0.829->0.864 mediu), nu l-a scazut. Nu exista o
tendinta masurata in directia care ar ajuta. Daca se incearca totusi o rulare mai mare (spre latimea
maxima documentata ~500, sau mai multi `n_estimators`), pragul de watch e rho fata de ridge/hgb din
`analysis_regresor.py --spatiu _tf-proj-NNN` dupa `--regressor tabfm-cache` — daca rho nu scade sub
~0.78-0.80, castigul in fuziune ramane in zgomot (<0.001), indiferent cat de mult urca r_A singur.

## Corectie 25 aug seara: cele trei cifre de fuziune de mai sus NU sunt reproductibile

CSV-ul `e1_frozen_preds_tf-proj-394_ridgetabfm_lemma_fert_inloc.csv`, cel dat lui `--a-set` pentru
0.6797, **nu e** media lui `reg-ridge` si `reg-tabfm-cache`: coloana `p_multi` e in unitati z
(-6.3 .. 8.4), nu in scala complexitatii [0,1]. Nu se potriveste nici cu media, nici cu media
z-scorurilor pe limba, nici pe (split, limba). Nu exista in cod niciun script care sa il scrie.

Constructia CORECTA e media pe coloane a CSV-urilor, si asta e **masurat**, nu presupus: `blend`
(adica ridge+hgb potrivit inauntru) e egal cu `mean(reg-ridge, reg-hgb)` la **1.11e-16** pe toate
cele trei coloane de predictii. Deci un blend facut inauntru si media CSV-urilor sunt acelasi lucru.

**Dar cifra a supravietuit, si asta e a doua jumatate a raspunsului.** Refacut prin media provata,
`ridge+tabfm` la MAXFEAT=160 da **0.6798**, fata de 0.6797 al constructiei vechi. La 0.0001. Motivul
e in docstring-ul lui `fuse_ab`: A se standardizeaza per limba inainte de fuziune, iar r e invariant
la transformari afine, deci un `p_multi` z-scoruit in interiorul limbii da acelasi r. Constructia
veche nu era reproductibila; cifra pe care a produs-o era buna.

Regula care ramane: pentru orice A compus, se foloseste `make_a_blend.py` (media pe coloane, cu
control pe `p_en` si `p_multi` la 1.11e-16), nu o combinatie ad-hoc. `p_multi_testmu` e scrisa cu
8 zecimale in CSV si nu e citita de `fuse_ab`, deci nu intra in control.

Artefacte de azi (netaguite ca adoptate, doar de test): `output/e_fusion_lolo_ctrl_proj394.md`,
`output/e_fusion_lolo_ridgetabfm_proj394.md`, `output/e_fusion_lolo_tabfm_proj394.md`,
`output/e_regresor_a_proj-394.md` (regenerat, acum include coloana `tabfm`).

## Follow-up 26 august: si jumatatea LINIARA e acum masurata, si tot inchisa

Tot ce e mai sus schimba jumatatea de ARBORI. Jumatatea liniara (`Ridge(alpha=300)`) a fost masurata
separat pe 26 august: 21 de candidati x 3 encodere, grile de alpha alese LOLO, plus o parghie nou
gasita (alpha per BRAT de transfer). **Podeaua de rho de 0.80 SE RUPE** cu L1, pana la 0.739, deci
afirmatia de la punctul 3 de mai sus e valabila numai pentru candidatii neliniari. Nu ajuta insa: ce
coboara rho pierde r_A, si transmisia A -> fuziune iese ~0 pe axa asta. Detaliile si cifrele:
[[axa-liniara-inchisa]].
