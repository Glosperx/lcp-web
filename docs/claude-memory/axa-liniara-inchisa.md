---
name: axa-liniara-inchisa
description: "26 aug 2026 - jumatatea LINIARA a blend-ului, singura parte neatinsa a axei regresorului, e masurata si INCHISA: 21 de candidati x 3 encodere, podeaua de rho SE RUPE dar castigul nu transmite, sistemul ramane 0.690001"
metadata:
  type: project
---

Rezultatul sesiunii cerute in [[cerere-sesiune-jumatatea-liniara]]. **Axa e inchisa cu cifre, si de
data asta pe fuziunea reala, pe 3 encodere.** Completeaza [[axa-regresorului-inchisa]], care acoperea
numai jumatatea de arbori.

75 de rulari, 66 de minute de CPU, 0 cazute. Cod in [[cod-nou-axa-liniara]].

## Premisa cererii era CORECTA, si tot n-a ajutat

Ipoteza era ca un liniar rar (L1) coboara `rho(liniar, hgb)` sub podeaua de 0.80 pe care niciun
candidat NELINIAR n-o rupsese. **Se rupe.** `rho` fata de `hgb`, fata de reperul `ridge` 0.811:

    lasso-a3e-2  0.739    krr-rbf  0.726-0.771    pls-k4  0.731-0.803    svr-lin  0.747-0.793

Dar nu valoreaza nimic, si mecanismul e acelasi masurat deja de doua ori: **partea decorelata e
ZGOMOTUL, nu semnalul.** Tot ce coboara rho pierde r_A: `lasso-a3e-2` cade la 0.4746 (de la 0.5519 al
lui ridge), `ard` la 0.5220. Iar `lasso-a1e-3`, care are cel mai bun r_A de pe toata axa (0.5689,
**+0.017 peste ridge**), URCA rho la 0.858, deci perechea cu hgb da doar +0.0015. Al treilea caz
identic, dupa TabFM k=1 (rho 0.764, si tot strica blend-ul).

## Cifra care inchide axa: transmisia e ~ZERO, nu doar mica

Pe drumul care conteaza pentru sistem (media a 3 encodere, `--ens`, acelasi B M3K):

    adoptat   ridge300 pe ambele brate         A 0.5993   fuziune 0.6900
    A4        lasso-a1e-3 pe ambele            A 0.5961   fuziune 0.6887   -0.0013  P 28.0%
    A6        ridge-a1000 pe ambele            A 0.6013   fuziune 0.6896   -0.0004  P 53.8%
    A8        ridge-a3000 numai pe p_en        A 0.6021   fuziune 0.6900   -0.0000  P 60.7%
    A7        p_en ridge3000 + p_multi lasso   A 0.6023   fuziune 0.6904   +0.0004  P 67.2%

**A urca +0.0030 constant si reproductibil pe toate trei encoderele, si fuziunea nu se mișca.**
Transmisia pe axa asta e ~0, fata de 0.09-0.26 din [[transmisia-a-fuziune-masurata]]. Al cincilea caz
in proiect in care un castig pe A nu ajunge in fuziune. Pe un singur encoder cel mai mult a dat
`mean(hgb, extratrees, pls-k16)` = 0.6839 fata de 0.6828, adica +0.0011 la P 68.5%, o moneda.

## alpha=300 a fost in sfarsit re-potrivit sub LOLO, si e o alegere buna

Era mostenit si nemasurat. Acum: pe `p_multi` cel mai bun e `ridge-a1000` (+0.0009, 3/3 encodere), pe
`p_en` `ridge-a3000` (+0.0045, 3/3). Amandoua optime INTERIOARE, grila prelungita pana la 30 si 30000
ca sa se dovedeasca. Castigul e insa sub zgomot in fuziune, deci **300 nu se schimba**.

Selectia LOLO a grilei e **UNANIMA** pe toate cele 10 taieri, la toate familiile. Deci nu e selectie
per limba, e o singura valoare globala estimata din limbile de potrivire, si regula
[[criteriu-plat-mediaza-nu-alege]] NU se aplica: ea e despre argmax care sare intre limbi.

## Parghia noua, gasita si inchisa in aceeasi sesiune

`p_en` si `p_multi` sunt COLOANE SEPARATE in CSV, deci alpha se poate alege PE BRAT, ceea ce nicio
configuratie din proiect nu face. Motivul mecanic: `p_en` e o singura potrivire care prezice zece
limbi nevazute, `p_multi` e o potrivire per limba cu noua limbi de test in antrenare.

Masurat: in banda utila cele doua brate sunt **INDEPENDENTE**, nu opuse. Corelatia deltelor e
**-0.041** la `|delta| <= 0.005` (n=11) si +0.130 la `<= 0.010` (n=19). Cifra pe toti candidatii,
**+0.606, e un ARTEFACT**: candidatii catastrofali sunt prosti pe ambele brate si fabrica singuri o
corelatie pozitiva care spune numai "prost e prost peste tot". Nu se citeaza.

Concret: cel mai bun pe `p_multi` (`lasso-a1e-3`, +0.0029) e **-0.0030 pe `p_en`**; cel mai bun pe
`p_en` (`ridge-a3000`, +0.0045) e -0.0006 pe `p_multi`. Singurul pozitiv 3/3 pe AMBELE e `ridge-a1000`.
Configuratia per-brat (A7) e prima din sesiune care trece peste sistem, dar cu +0.0004 la P 67.2%.
**Nu se adopta.** `alpha=300` sta intre cele doua cereri si de asta a supravietuit.

## TabFM s-a pastrat gratis, cum s-a cerut

Ruta hibrida din [[cerere-sesiune-jumatatea-liniara]] se confirma: `mean(lasso-a1e-3, hgb,
tabfm394@256)` da 0.6830 fata de 0.6827 al controlului hibrid. TabFM intra fara sa coste, dar nici nu
aduce. TabFM exista numai pe xlmr/`proj-394`, deci sub media celor 3 encodere poate intra numai prin
bratul xlmr.

## Sistemul ramane 0.690001

Nimic nu se adopta. Vezi [[sistemul-e-0690001-m3k]]. Raport: `output/e_regresor_liniar.md`, plus
`e_regresor_a{,_e5,_labse}.md` si `e_fusion_lolo_lin_A{1..8}.md`.
