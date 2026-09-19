# Sesiune de research pe algoritmii semnalului A

Aceasta nu este o cerere de tipul "ruleaza LightGBM si CatBoost". Este o cerere de research: vreau sa
stabilesti ce algoritmi merita testati, sa argumentezi alegerea cu cifrele care sunt deja masurate in
proiect, si abia apoi sa rulezi. LightGBM si CatBoost sunt doua dintre candidati, nu toata lista.

Citeste intai memoria proiectului, in special `cerere-sesiune-gbdt`, `axa-liniara-inchisa`,
`cod-nou-axa-liniara`, `axa-regresorului-inchisa`, `tabfm-maxfeat256-rezultatul`,
`transmisia-a-fuziune-masurata` si `criteriu-plat-mediaza-nu-alege`.

## Reformularea care ar trebui sa conduca toata sesiunea

Poarta care decide pe axa aceasta nu este `r`, este `rho`. Corelatia `rho(ridge, hgb) = 0.811` este
perechea cea mai decorelata din tot tabelul de estimatori, si ea este ceea ce duce intreaga valoare a
blend-ului. Pe 26 august s-au masurat 21 de candidati pe cate trei encodere, si rezultatul a fost un
compromis strict intre `rho` si `r`. Tot ce coboara `rho` sub 0.811 pierde `r_A`:

    lasso-a3e-2   rho 0.739          r_A 0.4746
    krr-rbf       rho 0.726-0.771    r_A 0.5322
    ard           rho 0.787          r_A 0.5220

Iar tot ce urca `r_A` urca si `rho` impreuna cu el:

    lasso-a1e-3   r_A 0.5689 (cel mai bun de pe axa, cu +0.017 peste ridge)   rho 0.858

Ipoteza mea de lucru pentru aceasta sesiune, si vreau sa fie testata explicit, este urmatoarea. Toti
candidatii de pana acum minimizeaza eroarea patratica pe aceeasi tinta. Familia de functii s-a
schimbat foarte mult intre ei, de la liniar dens la liniar rar, la kernel, la arbori cu bagging, la
arbori cu boosting, pana la invatare in context. Obiectivul, in schimb, nu s-a schimbat niciodata.
Iar `rho` nu masoara cat de mari sunt erorile, ci unde sunt ele plasate. Doua modele care minimizeaza
acelasi lucru pe aceleasi date tind sa greseasca in aceleasi locuri, oricat de diferita ar fi forma
functiei pe care o potrivesc.

Daca ipoteza este corecta, atunci parghia care lipseste nu este a saptea familie de arbori, ci un alt
loss sau o alta tinta. Te rog sa verifici ipoteza, nu sa o crezi: este scrisa din rationament, nu
masurata, si poate fi gresita.

## Ce s-a incercat deja, ca sa nu se refaca

Pe partea liniara s-au rulat `ridge` cu o grila de alpha de la 30 la 30000, `lasso` cu o grila de la
1e-4 la 3e-2, `elasticnet`, PLS cu k de la 4 la 64, `huber`, `bayesianridge`, ARD, kernel ridge RBF
exact si LinearSVR. Pe partea de arbori s-au rulat HistGradientBoosting la adancime 3, care este
incumbentul, acelasi la adancime 6, si ExtraTrees. Din familia modelelor fundationale tabulare s-a
rulat TabFM, iar acea axa este inchisa definitiv si nu se redeschide. S-au evaluat de asemenea toate
submultimile de pana la trei membri din cei 21 de candidati.

Rezultatul acelei sesiuni a fost ca nimic nu trece bara de +0.0045 pe fuziune, iar transmisia de la A
catre fuziune iese aproximativ zero: semnalul A a urcat cu +0.0030 in mod consistent pe toate cele
trei encodere, si fuziunea nu s-a miscat deloc.

## Meniul de candidati, ca punct de pornire si nu ca lista inchisa

### Axa 1, familia de functii

Aceasta axa este aproape epuizata, dar urmatoarele lipsesc din ea.

    lightgbm            Creste arborii leaf-wise, nu depth-wise cum face incumbentul. Cerut explicit.
    catboost            Creste arbori oblivious, adica aceeasi taietura pe tot nivelul, plus ordered
                        boosting. Este cel mai diferit bias inductiv de tip arbore care nu a fost
                        incercat, fiindca hgb, hgb-adanc si extratrees sunt toti axis-aligned si
                        crescuti liber. Cerut explicit.
    randomforest        Bootstrap plus taieturi complete. Nu este acelasi lucru cu ExtraTrees, care
                        foloseste taieturi aleatoare si nu foloseste bootstrap.
    lgbm linear_tree    Foi liniare in loc de foi constante, adica un hibrid intre liniar si arbore.
                        Spatiul de trasaturi este dens, deci este plauzibil ca acest hibrid sa se
                        potriveasca aici mai bine decat oricare dintre cele doua separat.
    MLPRegressor        Este singura familie complet absenta din proiect. Neliniar dens, si nu
                        axis-aligned. Pe 774 de dimensiuni de embedding acesta este exact regimul in
                        care se comporta bine. Exista deja in sklearn.
    KNeighbors          Local si non-parametric. Este de asteptat ca `r_A` sa fie mic, dar `rho`
                        poate fi mic si el, iar poarta este `rho`. Merita masurat tocmai din acest
                        motiv, nu fiindca ar fi promitator ca predictie.

### Axa 2, loss-ul

Aceasta axa este complet neatinsa. Am verificat: `absolute_error`, `quantile`,
`TransformedTargetRegressor` si transformarea pe rang nu apar nicaieri in cod.

    hgb cu loss absolute_error   Minimizeaza L1, deci plaseaza erorile in alte locuri decat L2.
    hgb cu loss quantile la 0.5  Mediana conditionala in loc de media conditionala.
    tinta transformata logit     Coloana complexity se afla in intervalul [0, 0.975] si are 28 de
                                 zerouri exacte, deci transformarea logit are nevoie de un epsilon
                                 de strangere. Tinta este marginita, iar toti regresorii de pana
                                 acum o trateaza ca daca ar fi nemarginita.
    tinta transformata pe rang   Metrica finala este corelatia Pearson, iar pe date monotone ea este
                                 apropiata de o corelatie de rang. A antrena direct pe rang aliniaza
                                 obiectivul cu metrica pe care este evaluat sistemul.

### Axa 3, incadrarea problemei

Aceasta axa este de asemenea neatinsa, si dupa mine are cel mai mare potential de a cobori `rho`.

Propunerea concreta este clasificare ordinala pe cinci clase, urmata de valoarea asteptata calculata
din probabilitati. Este exact ce face semnalul B cu modelul de limbaj, dar aplicat pe embedding.
Etichetele originale provin din agregarea unor judecati Likert de la 1 la 5, deci aceasta incadrare
este mai fidela datelor decat regresia pe o valoare continua. Structura erorii ar fi complet
diferita, si de aceea este candidatul cu cea mai mare sansa de a cobori `rho` la un `r` decent.

## Ordinea de lucru, si de ce conteaza ordinea si nu doar rezultatul

Proiectul are deja o conventie pe care o folosesc patru scripturi (`analysis_regresor.py`,
`analysis_frontiera_enc.py`, `analysis_c_frontiera.py`, `analysis_alti_candidati.py`): **poarta si
predictia se scriu INAINTE de a citi vreo cifra a candidatilor.** In `analysis_regresor.py` sectiunea
se numeste literal "Ce i-ar trebui unui al treilea estimator. Scris inainte de a-l cauta".

Vreau aceeasi disciplina aici, si e mai utila decat orice rationament facut dupa ce vezi rezultatul:

1. Inainte de a instala sau rula orice, scrie pentru fiecare candidat din meniu ce te astepti sa se
   intample cu `rho` fata de `ridge` si cu `r_A`, si de ce, in cateva cuvinte. Scrie si care crezi ca
   sunt cei doi sau trei cei mai promitatori. Pune-le intr-un fisier, ca sa nu se poata rescrie
   ulterior.
2. Abia apoi ruleaza cernerea de mai jos.
3. La final compara predictia cu masuratoarea si spune EXPLICIT unde ai gresit. Un candidat pe care
   l-ai crezut promitator si a picat este informatie despre mecanism, nu o rusine, si e exact ce a
   dus la rezultatele bune din sesiunile trecute.

Motivul pentru care insist: pe axa aceasta diferentele sunt de ordinul 0.001, iar o explicatie
construita dupa ce ai vazut cifra se potriveste pe orice cifra. Daca predictia e scrisa inainte, ea
poate fi gresita, si atunci chiar spune ceva.

Nu opri sesiunea ca sa ma intrebi intre pasi. Mergi pana la capat si raporteaza o singura data, cu
tot, in afara de cazul in care ceva chiar te blocheaza.

## Protocolul de cernere

Scopul protocolului este sa nu se cheltuiasca trei encodere pe candidati care sunt deja morti pe unul.

1. O rulare pe xlmr per candidat, cu `--frozentrial --lemma-freq --afeat fert_inloc --regressor X`.
2. `analysis_regresor.py`, din care se citesc `r_A`, `rho` fata de `ridge`, `rho` fata de `hgb` si
   `r(X+hgb)`.
3. Trece la trei encodere numai ceea ce are `rho(X, ridge)` sub 0.811 si in acelasi timp `r_A` peste
   0.53. Cele doua conditii impreuna sunt tot ce conteaza, fiindca fiecare luata separat nu spune
   nimic despre ce se intampla in blend.
4. Ce trece pasul 3 se ruleaza pe trei encodere, apoi prin `analysis_regresor_multi.py`, iar cele mai
   bune doua sau trei ansambluri trec prin `fuse_ab.py`.
5. In final, incearca parametri diferiti pe cele doua brate: `num_leaves`, `depth` sau loss diferit
   pentru `p_en` fata de `p_multi`. Cele doua brate sunt masurat independente in banda utila,
   corelatia deltelor fiind -0.041, iar pentru arbori aceasta parghie nu a fost incercata niciodata.

Daca propui candidati care nu sunt in meniul de mai sus, si te rog sa propui, judeca-i cu acelasi
criteriu de la pasul 3, si explica de ce ar cobori `rho`, nu de ce ar urca `r`.

## Ce este deja gata si nu trebuie rescris

In `solution_bert.py` exista `_FAM` si `regressor_kind`, care implementeaza familiile parametrice de
regresori; se adauga `lgbm-l<N>`, `cat-d<D>` si celelalte dupa exact acel model. `make_reg_runs.py`
este driverul care itereaza encoder pe regresor, sare peste ce exista deja pe disc si scrie un
jurnal. `analysis_regresor.py` accepta `--spatiu`, `--extra`, `--membri`, `--max-k` si `--col`.
`analysis_regresor_multi.py` face tabelul pe trei encodere, sectiunea celor doua brate, si tabelul de
fuziune citit direct din rapoartele lui `fuse_ab`. `make_a_blend.py` construieste orice A compus si
este controlat la 1.9e-16. `make_enc_mean.py --cai` face media pe encodere.

Doua lucruri practice, ambele verificate pe 26 august. LightGBM, CatBoost si XGBoost nu sunt
instalate in `envs/ml_def`. Si, mai important, LightGBM si CatBoost trateaza NaN nativ, deci se leaga
ca `_hgb_pred`, adica fara imputer, si nu ca `_pipe_pred`. Acest detaliu conteaza fiindca limbile
`ja` si `si` au coloane de suprafata NaN, si exact acest lucru a facut ca `lasso` sa nu poata rula
niciodata inainte de sesiunea precedenta. In schimb `MLPRegressor` si `KNeighbors` nu trateaza NaN,
deci ele trebuie legate prin `_pipe_pred`.

## Cum se ruleaza, concret

Interpretorul este `/opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python`. Nu `python3` de
sistem, care nu are torch, transformers si nici restul dependintelor.

Ai voie sa instalezi ce iti trebuie in acel env, adica `pip install lightgbm catboost`, fara sa mai
intrebi. Nu instala nimic global si nu atinge alte env-uri.

Embeddingurile sunt in cache in `data/`, deci o rulare `--frozentrial` costa 25-40 de secunde pe CPU
si nu are nevoie de GPU. Nu re-embeda nimic. Matricea intreaga, pe trei encodere, sta sub o ora.

Inainte de a atinge codul semnalului A, fa copia de rezerva cu md5 si ruleaza controlul cu
`--regressor blend`. Rezerva de acum este in `output/_rezerva_reg/`.

## Reperele fata de care se compara

    pe A, controlul este ridge+hgb                    0.575296
    blend pe xlmr plin, fara --ens, in fuziune        0.6828    vs fusion_preds_lolo_xlmr_plin.csv
    ruta hibrida cu tabfm@256, in fuziune             0.6827    vs fusion_preds_lolo_hibrid_rht.csv
    sistemul adoptat, 3 encodere cu --ens             0.6900    vs fusion_preds_lolo_adoptat_m3k.csv
    bara pe fuziune                                   +0.0045

Cifra 0.575296 este media celor zece corelatii pe limba si nu trebuie confundata cu 0.577613, care
apare la curba de prag si care aplica identitatea de frontiera pe `r` si `rho` deja mediate peste
limbi. Explicatia diferentei este scrisa in raport.

## Capcane de respectat, toate platite deja

Functia `blend_ridge_hgb` este importata pe nume din patru fisiere, deci nu se atinge; orice varianta
noua se adauga alaturi de ea. Inainte de a modifica codul semnalului A se face o copie de rezerva cu
md5 la fisierele adoptate, iar apoi o rulare cu `--regressor blend` trebuie sa dea inapoi md5-ul
`70c74c22218b7525d8e1d3d11b663f67`; poarta interna `ref_r` este stinsa pe aceasta configuratie, deci
verificarea se face pe fisier. La `analysis_regresor.py` se foloseste `--max-k 3`, fiindca enumerarea
submultimilor creste ca 2^k si cu tot ce este acum pe disc k trece de 25. Un optim aflat la marginea
grilei nu este un optim, ci doar cel mai departe unde s-a privit, deci grila se prelungeste si se
spune ca a fost prelungita. O predictie constanta pe o limba se raporteaza explicit; nu se lasa un
`nan` sa se plimbe prin tabel. Alegerea intre configuratii se face leave-one-language-out, niciodata
pe scorul de test, iar cand mai multi candidati sunt la egalitate se mediaza in loc sa se aleaga.
Concluziile se calculeaza din tabel si nu se scriu de mana: o propozitie scrisa de mana s-a contrazis
deja cu propriul tabel dupa ce s-au adaugat doua rulari. Si, in sfarsit, un castig pe A poate cobori
fuziunea, ceea ce s-a intamplat de cinci ori pana acum.

## Ce vreau la final

Acelasi format ca `output/e_regresor_liniar.md`, plus raspuns direct la doua intrebari.

Prima: a coborat vreun candidat corelatia `rho` fata de `ridge` sub 0.811 pastrand `r_A` peste 0.53?
Daca nu, axa familiei de functii se inchide definitiv, cu al doilea punct pe aceeasi tendinta.

A doua, si este intrebarea de research a sesiunii: este adevarata ipoteza despre loss? Adica au
candidatii care schimba obiectivul, adica axele 2 si 3, un `rho` sistematic mai mic decat cei care
schimba doar familia de functii, la `r` comparabil? Raspunsul la aceasta intrebare conteaza mai mult
decat orice cifra individuala din sesiune, fiindca el spune daca axa merita redeschisa vreodata.
