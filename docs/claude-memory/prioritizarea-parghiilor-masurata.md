---
name: prioritizarea-parghiilor-masurata
description: "21 aug 2026 - raportul de prioritizare a inchis 5 parghii cu cifre si a gasit una noua care trece bara, 0.685530 prin unirea cifrelor; ce NU se mai reia"
metadata: 
  node_type: memory
  type: project
  originSessionId: a83bfa8c-49a6-4b98-8ed9-40f8abb301dc
  modified: 2026-08-21T15:57:49.190Z
---

Rulat **21 august 2026**, `analysis_prioritate.py` -> `output/e_prioritate.md`, 75 s plus ~12 min de
inferenta pe trial. Referinta e sistemul cu temperatura, 0.683849, din
[[distributia-b-temperatura]]. **Nimic nu s-a adoptat**, decizia e a lui Alexandru.

## Cifra noua, si nu era pe lista

**Unirea cifrelor vecine**, adica citirea distributiei pe blocuri contigue in loc de cele cinci note
egal spatiate. Partitia `1|23|45` e aleasa **unanim pe toate zece limbile** dintre 15 candidate, iar
fuziunea da **0.685530**, adica **+0.00168**, CI pereche **[+0.00072, +0.00269]**, P(>0) = 100%,
**zero limbi stricate**. Cost zero: aceeasi inferenta, aceleasi distributii de pe disc, alta citire.

Mecanismul: nu adauga informatie, **respatiaza nivelurile**. Eticheta nu e liniara in nota, si
spatierea grosiera e mai aproape de ea decat cea egala. E `--mod colaps` in `make_bt_runs.py`.

**Bifurcatie de declarat**, pe lista din [[bifurcatii-de-declarat]]: parghia a ieșit din curba r(K)
calculata pe TEST. Hiperparametrul e LOLO, dar decizia de a o incerca vine de la o cifra de test.

**Combinatia mai mare s-a respins.** Unirea plus ponderea da +0.00186, mai mult, dar **strica
portugheza cu -0.0056, CI [-0.0094, -0.0022]**. Acelasi motiv ca `distTpp`. Criteriul e acum o
coloana in cod, `limbi stricate`, citita INAINTEA coloanei cu media.

## Cele cinci care se inchid, cu cifra care le inchide

1. **Al treilea termen pentru dezacord.** Plafon +0.00231, dar **podeaua de zgomot pe 2 coloane e
   +0.00121**, deci excedentul e ~+0.00110, sub pragul de +0.002. Calibrarea pe zgomot e obligatorie
   la orice plafon in-sample: `dezacord_E` singur da +0.00055 fata de +0.00063 al unei coloane de
   zgomot, adica **sub** podea.
2. **Reziduul de fertilitate ca termen global.** Plafonul pare mare, +0.00723, dar la **transfer** da
   **-0.00153, CI [-0.00186, -0.00122], exclude zero in jos**, si semnul coeficientului cade la fel
   pe doar **4 din 10** limbi. Inchide punctul rams deschis din [[franceza-diagnosticata]].
   **Capcana de citire:** `de` are reziduu partial NEGATIV in §3.5 si totusi plafon pozitiv mare aici.
   Nu e contradictie: corelatia partiala are semn, castigul predictiv nu, fiindca regresia
   potriveste coeficientul. Deci plafonul nu decide niciodata singur, transferul decide.
3. **Distributia intreaga ca trasaturi.** Citirea liniara optima a celor 5 probabilitati, aleasa
   LOLO, e **sub** `B`: +0.6407 fata de +0.6592. In-sample da +0.6760, deci exact tiparul „nu
   transfera". Explica si de ce unirea cifrelor merge: e aceeasi familie, dar regularizata la 15
   candidate discrete, monotone, partajate intre prompturi.
4. **Media geometrica** a celor doua distributii: -0.00031. Constrangere de reținut daca se reia:
   puterea si produsul **comuta**, `(p^(1/T) q^(1/T))^(1/2) = (pq)^(1/(2T))`, deci produsul la T fix
   ar fi confundat cu temperatura si nu e comparabil cu media aritmetica.
5. **Ponderea intre prompturi**, singura: +0.00048, CI include zero. `w = 0.4` iese pe toate limbile,
   coerent cu promptul 2 mai bun, dar castigul e absorbit de fuziune si e redundant cu unirea
   cifrelor (stivuite adauga doar +0.00018).

## Scara de raspuns: inchisa, cu sondaj rulat

Proxy-ul de pe disc a prezis negativ **inainte** de rulare, si a nimerit. Curba r(K) sub alegere LOLO
are varful la **K=3** (+0.6613) si nu la K=5 (+0.6592), iar la T adoptat masa e imprastiata pe **4.49
atomi din 5** cu **zero legaturi** in 5624 de randuri. Cei cinci atomi nu leaga.

Sondajul pe trial, trei brate, ~6 min fiecare: ancora `1 -> 0` da **-0.0081**, atomii `5 -> 10` dau
**-0.0018**, amandoua **-0.0099**, toate cu CI care include zero si toate cu semn negativ. Pe 0-9
modelul foloseste efectiv **2.51 din 10** cifre fata de 1.75 din 5, deci **nu deschide rezolutie, o
imparte**.

**Doua imposibilitati de arhitectura, de nereluat:** `1-10` nu se poate citi, fiindca „10" sunt doi
tokeni si primul se ciocneste cu nota 1, deci **0-9 e singura scara de zece atomi citibila dintr-o
pozitie**; `0-99` ar cere 2 sau 11 treceri inainte per rand, deci nu mai e o configuratie de 6 minute.
Designul are nevoie de **trei** brate, nu doua: `0-9` schimba si atomii si ancora, iar `0-4` izoleaza
ancora.

## Ce a rams pe lista

Doua lucruri, si primul e prost formulat in raport, corectat aici pe 21 aug dupa verificarea codului:

1. **Few-shot din celelalte limbi nu e netestat.** `prompt_lab.lolo_shots` ia exemplele numai din
   celelalte limbi, deci `v3_fewshot` din E.10 e chiar asta, rulata pe trial: **+0.697 pe Gemma fata
   de +0.686 al semnalului B de acum**, cea mai buna varianta individuala. Ce lipseste e rularea pe
   **test**, 2.44 s per item deci **~3.8 ore**, si trecerea prin fuziune. Se ruleaza ca configuratie
   FIXA pe toate limbile; selectia LOLO peste variante a pierdut deja (+0.6808 fata de +0.6860), deci
   ce se testeaza e varianta fixa. Are si valoare de revendicare, vezi
   [[noutate-si-precedente-lcp-multilingv]].
2. **Pozitia de citire**, prefix fortat: chiar netestata, ~6 min pe trial.

**AMANDOUA RULATE PE 21 AUGUST SEARA, si lista e acum goala.** Few-shot singur PIERDE pe test,
-0.0123 cu cinci limbi stricate; dar ansamblul de TREI prompturi plus unirea cifrelor da
**0.688506**, +0.004642, CI [+0.0026, +0.0068], zero limbi stricate, si e ADITIV cu `prio_K`
(interactiune +0.00008). Pozitia de citire e negativa pe toate trei prefixele. Vezi
[[fewshot-pe-test-masurat]] si [[pozitia-de-citire-masurata]].

Coloana „cost" a randului 10 din `output/e_prioritate.md` spune inca „~5.5 min trial" si e greasita
din motivul de sus. Vezi [[parametri-llm-de-explorat]] pentru agenda originala.

## Cod, si trei controale care trebuie sa treaca

`make_bt_runs.py` are acum `--mod {temperatura, pondere, produs, pondere-produs, colaps,
colaps-pondere}`; scara e parametrizata in `solution_bert.py` prin `LLMRater(scale=...)` si
`prompts_multi_for`, cu implicit 1-5. Controalele: directorul cu `w=0.5` iese identic la octet cu cel
adoptat; fuziunea pe el da exact 0.683849 cu diferenta +0.0000 pe toate zece limbile; scara 1-5 prin
codul parametrizat reproduce fisierul canonic de trial cu `max |dif| = 0.0` si pe B si pe toate
coloanele de distributie.

**Doua capcane gasite pe drum:** `d4_sanity.py` avea un al DOILEA `"12345"` hardcodat, in tabelul de
raport, care crapa pe 0-4 dar **nu** pe 0-9, fiindca acolo cifrele 1-5 exista; si `fuse_ab` tipareste
doua statistici diferite, media pe limbi a lui P(>0) in tabelul per limba (75%) si P(>0) al mediei in
tabelul de agregare (100%) - a doua e cea care se citeaza, prima m-a facut sa citesc greasit o data.
Vezi [[constante-hardcodate-mint-dupa-renumerotare]].
