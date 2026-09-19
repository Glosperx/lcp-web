---
name: sistemul-e-0690001-m3k
description: "23 aug 2026 seara - Alexandru a ADOPTAT M3K: sistemul e acum 0.690001, nu 0.683849; artefactele canonice au tagul adoptat_m3k; pt e la un fir de a pica si al treilea prompt a iesit ULTIMUL pe trial"
metadata:
  type: project
---

**Adoptat 23 august 2026 seara, la cererea explicita a lui Alexandru.** Sistemul nu mai e 0.683849.

## Cifra si artefactele

    r = 0.690001, CI [0.6757, 0.7037]
    fata de 0.683849:  +0.006153, CI pereche [+0.003436, +0.008713], P = 100%

Artefacte canonice, produse cu **tag propriu**, nimic suprascris:

    output/e_fusion_lolo_adoptat_m3k.md
    output/fusion_preds_lolo_adoptat_m3k.csv
    output/fusion_lolo_adoptat_m3k.csv

Comanda: `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag adoptat_m3k
--b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv
--vs output/fusion_preds_lolo_adoptat_temp.csv`. Reproduce rularea din 22 august la **0.0 exact**.

Fisierele vechi (`_adoptat_temp`) raman intacte, mtime 20 august, si sunt referinta pentru diferentele
perechi de pana acum.

## Per limba, si ce s-a schimbat

    limba   0.683849   M3K       diferenta
    de      0.7468     0.7712    +0.0244
    si      0.4251     0.4350    +0.0099
    fr      0.6590     0.6679    +0.0089
    ca      0.5566     0.5639    +0.0073
    ja      0.7877     0.7942    +0.0065
    it      0.6750     0.6795    +0.0045
    es      0.7641     0.7672    +0.0031
    en      0.8700     0.8723    +0.0023
    fil     0.5091     0.5074    -0.0017
    pt      0.8450     0.8413    -0.0037

Urca pe 8 din 10. Bratul B trece de la 0.6592 la 0.6649, `w_src` mediu de la 0.738 la 0.800.

## Doua caveate care calatoresc cu cifra

1. **Portugheza e la un fir de a pica.** -0.0037, CI [-0.0078, **+0.0001**], P(>0) = 2.8%. Include
   zero, deci trece conditia, dar marginea superioara e +0.0001.
2. **Al treilea prompt al lui M3K a iesit ULTIMUL pe trial**, -0.008127 sub protocolul complet. Deci
   alegerea lui M3K in locul lui FS3K (0.688506) e **in intregime o decizie pe setul de test**. Cele
   doua nu se disting: +0.001510, CI [-0.001142, +0.004239]. Pentru cifra e irelevant, pentru
   Limitations nu. Vezi [[cifra-de-raportat-in-paper]] si [[bifurcatii-de-declarat]].

## Ce se schimba pentru masuratorile viitoare

Referinta pentru orice `--vs` devine `output/fusion_preds_lolo_adoptat_m3k.csv`. Bara ramane +0.0045.
**Poarta de 0.1077 se recalculeaza** la noul r_F: la 0.690001 pragul devine putin mai mare, fiindca
`1 - r_F^2` scade. Vezi [[poarta-al-treilea-semnal-0107]].

Alexandru a respins explicit directia "un model de evaluare mai mare", cu motivul ca **nu e o solutie
inginereasca**. Nu se repropune. Vezi [[al3lea-semnal-ce-ramane-deschis]].
