---
name: cifra-de-raportat-in-paper
description: "22 aug 2026 - draftul citeaza inca 0.6749 desi sistemul adoptat e 0.683849, deci castigul liber e +0.0089; recomandarea e 0.683849 in tabel si FS3K/M3K in ablatie, cu motivele"
metadata:
  type: project
---

Constatat **22 august 2026**, la finalul sesiunii de research.

## Draftul e in urma, si asta e cel mai mare castig disponibil

`Paper/Articol_Multilingv/paper_full.tex` are randul `Ours` din `tab:results` la **.675** si in text
`reaches $0.6749$, with a bootstrap interval of $[0.660, 0.689]$`. Sistemul adoptat e insa
**0.683849**, din `output/e_fusion_lolo_adoptat_temp.md`. Diferenta e **+0.0089**, cu interval pereche
[+0.0056, +0.0124] si P(>0) = 100%, si nu costa nicio decizie noua: e configuratia deja adoptata.
Randul devine **.684**, intervalul din text devine [0.669, 0.698].

**Asta se face inainte de orice discutie despre 0.6885 sau 0.6900.** E de doua ori mai mult decat
castigul pe care il ofera al treilea prompt, si nu adauga nicio bifurcatie.

## Candidatii de deasupra, si de ce recomandarea e sa NU se urce

`FS3K` 0.688506 (+0.004642 fata de sistem) si `M3K` 0.690001 (+0.006153). Amandoi trec ambele
conditii, zero limbi stricate, si amandoi rezista la Bonferroni chiar si pe 30 de configuratii:
FS3K [+0.001203, +0.007802], M3K [+0.001974, +0.010702]. Deci multiplicitatea nu ii separa.

Trei motive pentru care recomandarea e sa ramana **0.683849** in tabel:

1. **Mecanismul nu e o contributie.** Frontiera e o identitate algebrica exacta, vezi
   [[frontiera-e-identitate-nu-aproximare]]: castigul celui de-al treilea prompt E reducerea de
   varianta, si nimic altceva. Fraza care ramane de scris e "trei prompturi bat doua".
2. **Amandoi contin `K`**, care a fost gasit uitandu-ne la o curba de test, si al carui castig pe B e
   doar +0.001480 peste podeaua de zgomot a unui bazin de 15, vezi [[calibrarea-monotona-inchisa]].
3. **Scara.** Intervalul propriu al lui r pe sistem e [0.6694, 0.6980], adica +/-0.015. Toata discutia
   0.6838-0.6900 e o treime din el, si costa doua decizii de test in plus plus 2.5x inferenta la
   few-shot (1.03 s per item fata de 0.40).

`M3K` nu e candidat de titlu in niciun caz: al treilea membru al lui a iesit ULTIMUL pe trial sub
protocolul complet (-0.008127), deci alegerea lui e in intregime o decizie pe setul de test, si oricum
nu se distinge de FS3K (+0.001510 [-0.001142, +0.004239]).

**Daca totusi se urca la FS3K**, atunci in text trebuie sa scrie explicit ca al treilea prompt aduce
prin reducere de varianta, nu prin exemplele lui, si ca partitia `K` vine de la o curba de test.

## Contextul comparatiei, ca sa nu se piarda

In `tab:results`, primele trei randuri si `Ours` nu folosesc nicio eticheta in limba evaluata; celelalte
trei conditioneaza pe 3-30 de exemple etichetate in ea. Comparatia like-for-like e deci `Ours` fata de
`TMU-HIT, zero-shot` .610. La .684 marja devine +0.074. Peste sistemele care folosesc etichete,
G-Scale .669 si G-Eval .657, se trece oricum. Vezi [[noutate-si-precedente-lcp-multilingv]] si
[[agregare-medie-pe-limbi-nu-pooled]].
