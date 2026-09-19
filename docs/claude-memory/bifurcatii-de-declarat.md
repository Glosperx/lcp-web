---
name: bifurcatii-de-declarat
description: "51 de configuratii de sistem masurate, fiecare curata pe dinauntru dar alegerea INTRE ele se face uitandu-ne la scorul de test; formularea pentru Limitations e in output/e_adoptie.md §4"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1db2cc03-b25b-478b-93a1-cce9b8a92faf
  modified: 2026-08-18T21:52:14.007Z
---

Constatat **19 august 2026**, scris ca sectiunea 4 din `output/e_adoptie.md`.

S-au masurat **51 de configuratii de sistem** pe splitul de test, numarate ca fuziuni: 13 pe `n`
curent in `output/e_rezumat_modele.csv` si 38 in arhiva `output/e_rezumat_modele_pre-p11_n5606.csv`.
**Cifra de citat e numarul de CONFIGURATII, nu de randuri de jurnal**, fiindca fiecare configuratie
scrie si un rand de brat A, iar arhiva se numara si ea: fara ea declaratia ar ascunde exact partea
cea mai lunga a cautarii. Fiecare e curata pe
dinauntru: limba evaluata e exclusa la fiecare nivel de alegere, la antrenarea bratului A, la
alegerea setului de trasaturi, la alegerea modelului lui B, la `w_src` si la `w`. Niciuna nu
foloseste vreo eticheta din limba pe care o evalueaza.

**Dar alegerea INTRE ele o facem noi, uitandu-ne la scorul de test.** Asta nu se repara cu inca un
nivel de leave-one-language-out, fiindca nu e un nivel de protocol, e o decizie de cercetator: care
experiment se raporteaza ca sistem. Se repara **declarand-o**.

Regula propusa, scrisa ca sa fie verificabila:
1. Configuratia raportata e cea cu r mediu maxim pe test dintre cele masurate.
2. O configuratie noua se adopta doar daca intervalul ei PERECHE fata de cea curenta exclude zero.
   Punctul estimat mai mare nu ajunge.
3. Fiecare configuratie masurata ramane in jurnal, inclusiv cele care au pierdut, si jurnalul se
   publica.

Formularea propusa pentru Limitations e in `output/e_adoptie.md` §4, gata de copiat. Ce ar face-o
**falsificabila**, si nu doar onesta, e M1: alegerea intre brate facuta ea insasi LOLO.

**Jurnalul E ACUM GENERAT**, de `make_rezumat_modele.py`, tocmai fiindca a fost tinut de mana si a
ramas in urma tacut de fiecare data. Auditul incrucisat e `analysis_audit_jurnal.py`: pentru fiecare `output/fusion_*.csv` compara media
lui `r_fuz_raw` si `r_A_raw`, pentru fiecare `e1_frozen_preds*.csv` compara r al lui `p_multi` pe test,
si cauta cifra in coloana `r_mediu`. **Capcana pe care a avut-o chiar auditul:** tabelele vechi n-au
sufixul `_raw` si globul cerea `e1_frozen_preds_*`, deci sarea tacut peste 16 fisiere si iesea „curat"
fiindca nu citise. Reparat. A doua oara, dupa P11, a trebuit sa invete sa distinga artefactele pe `n`
vechi de cele LIPSA, altfel n-ar mai fi iesit niciodata curat. Vezi
[[constante-hardcodate-mint-dupa-renumerotare]].

**Why:** e aceeasi slabiciune de reviewer ca la tuning-ul pe scorul public din etapa 1, si aceeasi
reparatie: se declara, nu se ascunde.

**How to apply:** dupa orice configuratie noua se ruleaza `make_rezumat_modele.py` si apoi
`analysis_audit_jurnal.py`; nimic nu se mai adauga de mana. Cand se citeaza numarul in paper, se
recalculeaza, nu se copiaza dintr-o sesiune veche. Vezi
[[combinatia-p9-masurata]] si [[paper-slabiciuni-de-reviewer]].

## Inca una, 21 august 2026

`prio_K` (unirea cifrelor vecine, 0.685530) a fost **gasita** uitandu-ma la o curba r(K) calculata pe
test, si abia apoi i-am ales partitia LOLO. Deci intra pe aceeasi lista: hiperparametrul e curat, dar
decizia de a incerca parghia nu e. Perechea ei, `prio_KW`, are media mai mare si a fost respinsa
fiindca strica portugheza cu CI care exclude zero, ceea ce e argumentul care arata ca lista se
foloseste, nu se recita. Vezi [[prioritizarea-parghiilor-masurata]].

## Adaugat 22 august 2026: paisprezece configuratii de semnal B

Pe aceleasi 5624 de randuri de test s-au masurat FS, FSK, FS3, FS3K, FS3P, FS3KP, R3, R3K, M3, M3K,
L3, L3K, plus `prio_*` de pe 21 august. Doua trec ambele conditii, `FS3K` = 0.688506 si `M3K` =
0.690001, si nu sunt distinctibile intre ele (+0.001510 [-0.001142, +0.004239]).

**Maximul a paisprezece nu e un rezultat.** Singura formulare care supravietuieste: al treilea prompt
se alege pe TRIAL, unde few-shot era clar primul (+0.7109 fata de +0.6904), si atunci `FS3K` e o cifra
selectata pe trial si evaluata o data pe test; celelalte sunt controale. Dar chiar si asa, `K` vine de
la o curba calculata pe test. Vezi [[ansamblul-de-prompturi-formula]].
## Sesiunea de research, 22 august 2026

Sapte configuratii candidate noi si treisprezece controale, pe aceleasi 5624 de randuri. **Niciuna nu
trece bara**, deci maximul peste bazin nu s-a mutat si optimismul de +0.001937 ramane valabil; dar
bazinul e mai mare, deci daca in viitor ceva trece bara, optimismul lui se recalculeaza pe bazinul nou.

Candidate: `FR3`, `FR3K` pe fuziune; `witem entropie`, `witem dezacord` pe fuziune; grilele monotone la
pas 1/4, 1/8, 1/12 pe semnalul B. Controale: reproducerea de octet a lui `bakeoff_test_Text`,
`--mod calibrare --pas 0` fata de `--mod colaps`, `witem` cu grila lui `a` la zero, cinci seminte de
zgomot pentru pondere, si cate zece bazine aleatoare pentru fiecare familie de calibrare.

`make_rezumat_modele.py` si `analysis_audit_jurnal.py` rulate dupa; auditul iese curat, 115 cifre pe n
curent, 102 randuri in jurnal, zero lipsa.
