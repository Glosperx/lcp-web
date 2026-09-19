---
name: p11-adoptia-facuta
description: SUPERSEDAT de [[distributia-b-temperatura]] pe 20 aug - "P11 FACUT 19 aug: sistemul e acum pick-split test + media a TREI encodere = 0.674946 pe n=5624; find_char_span reparat, M1 10/10, jurnalul vechi arhivat"
metadata:
  type: project
---

Executat **19 august 2026**, evenimentul unic de renumerotare. Alexandru a ales varianta cu trei
encodere. Toate cifrele de dinainte sunt istorice, fiindca `n` s-a schimbat.

## Sistemul, de acum

```
fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag adoptat \
    --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv
```

**r = 0.674946** pe **n = 5624**, fata de 0.664581 al configuratiei de dinainte, adica **+0.010365**,
CI pereche **[+0.0060, +0.0146]**, P(>0) = 100%.

Patratul curat, toate pe n=5624:

| configuratie | r |
|---|---|
| de dinainte, xlmr + selectie pe trial | 0.664581 |
| media a trei encodere | 0.669223 |
| selectia lui B pe test | 0.669735 |
| **ADOPTAT, amandoua** | **0.674946** |

Cele doua parghii se aduna **106%** din suma naiva, iar fiecare adauga peste cealalta cu interval
care exclude zero (+0.005724 si +0.005211). `encmean` si `picktest` nu se disting una de alta
(-0.000512, CI include zero).

Per limba fata de dinainte: fr **+0.0593**, si +0.0176, ca +0.0128, es +0.0120, pt +0.0052,
en +0.0039, it +0.0021, de +0.0009, **fil -0.0051 si ja -0.0051**.

## Ce s-a schimbat in cod

- **`find_char_span` reparat**, in `solution_bert.py`. Cautarea sensibila la caz rata tinta scrisa cu
  majuscula la inceput de propozitie. Recupereaza toate cele 18 randuri de test (it 8, pt 5, fr 3,
  fil 2) plus 1 din CompLex EN. Acum cad **zero din 5624**. **Capcana ocolita:** `.lower()` poate
  schimba lungimea (`"İ".lower()` da doua caractere), deci se verifica ca felia originala se
  potriveste ca lungime, altfel se renunta; un span gresit e mai rau decat un rand lipsa.
- `make_enc_mean.py` primeste `--encodere` si `--dest`; fara argumente reproduce bit cu bit.
- `analysis_pick_split.py` primeste perechea din linia de comanda.
- Scripturi noi: `analysis_adoptie.py`, `analysis_m1.py`, `analysis_m3.py`,
  `analysis_cost_inferenta.py`, `analysis_audit_jurnal.py`.

## Capcane de tinut minte

- **Cache-ul de embedding se invalideaza TACUT.** Cheia e `emb_{split}_{enc}_{cfg}_{n_randuri}`, iar
  `n_randuri` nu se schimba la fixul de caz, doar masca `ok`. Trebuie sterse de mana, altfel se
  citesc embedinguri vechi fara nicio eroare.
- **`find_char_span` e partajat cu calea romaneasca.** `FINAL_best.csv` e neatins, md5
  `743bce923af4c4b82e578de47ea32826` verificat dupa fix, dar daca se re-ruleaza vreodata RoLCP
  cifrele alea s-ar misca. Vezi [[r-si-r2-masurate-pe-rolcp]].
- **Jurnalul vechi e arhivat** ca `output/e_rezumat_modele_pre-p11_n5606.csv`. Cel nou **e GENERAT**
  de `make_rezumat_modele.py`, nu mai e tinut de mana, fiindca exact asta il facea sa ramana in urma
  tacut. Are 39 de randuri, coloanele `componenta`, `n_itemi`, `d_vs_adoptat`, `ci_lo`, `ci_hi`,
  `p_gt0` si `stare`. `analysis_audit_jurnal.py` ramane ca verificare incrucisata si distinge acum
  artefactele pe `n` vechi de cele lipsa, altfel n-ar mai iesi niciodata curat.

## Cifra adoptata NU e cifra maxima, si distinctia se citeaza

**0.674946 e cea raportata, nu cea mai mare masurata.** Maximul e **0.675996**, aceeasi configuratie
cu patru encodere in loc de trei. Diferenta e **+0.001050, CI [-0.0004, +0.0025], INCLUDE zero**,
P(>0) = 91.6%. Al patrulea encoder nu se distinge de zero, deci s-a ales varianta ieftina, dar la
intrebarea „care e cea mai mare cifra" raspunsul onest e 0.675996 si raportam 0.674946 deliberat.
Ambele sunt marcate in coloana `stare` a jurnalului.

**Why:** e prima data cand cifra de sistem se schimba dupa ce protocolul a validat alegerea, nu
inaintea lui.

**How to apply:** 0.674946 pe n=5624 NU mai e cifra de citat, e ablatia fara temperatura; vezi nota de la final si [[distributia-b-temperatura]]. Vezi [[m1-si-m3-au-trecut]] si
[[combinatia-p9-masurata]] pentru cifrele de dinainte de renumerotare.

**SUPERSEDAT 20 august 2026.** Cifra de citat e acum **0.683849**, cu temperatura, vezi [[distributia-b-temperatura]]. 0.674946 ramane valid ca ablatia cu T = 1, si tot ce scrie mai sus despre pick-split, cele trei encodere si `find_char_span` ramane adevarat: temperatura s-a adaugat peste, nu in locul lor.
