---
name: criteriu-plat-mediaza-nu-alege
description: Regula transversala a proiectului: cand criteriul de selectie e plat, selectia LOLO e zgomot si medierea o bate; masurat de trei ori
metadata:
  type: feedback
---

Tiparul a aparut de trei ori independent in proiect, cu aceeasi forma, si e cea mai utila regula
practica pe care am scos-o din date.

**Regula: cand latimea criteriului de selectie e mult mai mica decat latimea efectului pe care il
alegi, argmaxul e zgomot. Atunci se mediaza, nu se alege.**

Cele trei masuratori:

1. **Encodere per limba (18 aug).** Latimea criteriului peste 36 de candidati: **0.0077**, fata de
   0.082 cat are curba lui `w`, de zece ori mai mica. Selectia LOLO a nimerit cel mai bun encoder de
   **0 ori din 10** si a dat 0.6599, sub sistemul de 0.6646. **Medierea neponderata a dat 0.6720**,
   +0.0074 cu CI care exclude zero, si a atins exact plafonul oracol (0.6045 pe A) fara etichete.
2. **Combinarea de modele pe semnalul B.** Oracol +0.0070, varianta LOLO-curata **+0.0012**.
3. **Alegerea candidatului (set, `w_src`) in sistemul publicat.** Latimea criteriului 0.0058 fata de
   0.0847 a curbei lui `w`, tot de ~15 ori mai mica. E scris ca atare in raport: separa ceva, dar
   marginea e subtire si o parte e zgomot.

**Why:** selectia cere ca ORDINEA candidatilor sa fie estimabila din limbile de potrivire. Medierea
cere doar ca ei sa fie decorelati. A doua conditie e mult mai slaba si se verifica direct (corelatii
0.847-0.884 intre encodere). In plus, ce face un candidat potrivit pentru limba L e adesea o
proprietate A LUI L (scriere proprie, `wordfreq` care n-o serveste), pe care celelalte 9 limbi n-o
impart, deci nu e invatabila de la ele nici in principiu.

**How to apply:** orice propunere care are forma „alegem X per limba" trebuie sa vina cu **latimea
criteriului masurata** inainte de a fi crezuta. Daca e plata fata de efect, varianta care se ruleaza e
medierea. Si nicio regula tipologica inventata post-hoc nu salveaza selectia: „scriere non-latina ->
LaBSE" ajuta `si` (+0.126) si strica `ja` (-0.062), ambele non-latine.

A doua capcana, inrudita, din aceeasi zi: **corelatia unei trasaturi cu eroarea bruta `y - p` nu
masoara „cat a mai ramas"**. Iese negativa pe toate cele 10 limbi, inclusiv pe cele cu reziduu initial
zero, fiindca masoara cat foloseste modelul trasatura. Varianta corecta e corelatia partiala cu
predictia in controale pe AMBELE laturi.

Vezi si [[encoderul-masurat-lolo]], [[ansamblul-de-modele-nu-se-transfera]],
[[franceza-diagnosticata]], [[pondere-fuziune-potrivita-pe-test]].
