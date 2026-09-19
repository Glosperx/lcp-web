---
name: transferul-se-masoara-pe-limba
description: "22 aug 2026 - rho3 transfera trial-test cu +0.98 pe MEDII dar doar +0.64 PE LIMBA, iar r3 invers, +0.52 si +0.79; cum selectia e LOLO, conteaza cea pe limba, si de aia a cazut frecventa"
metadata:
  type: project
---

Masurat **22 august 2026**, pe cinci membri x zece limbi, dupa ce `frecventa` a trecut ambele porti de
cernere pe trial si a picat pe test. Vezi [[prompturi-decorelate-cernute]].

## Corectia, si e la o cifra pe care s-a construit o procedura

Fisa veche spunea: `rho3` transfera trial-test cu **+0.997**, `r3` cu **+0.726**, deci cerne pe `rho3`.
Cifrele acelea sunt corelatii peste PROMPTURI ale mediilor pe limbi, si se confirma: recalculate acum
pe cinci membri dau +0.980 si +0.519. **Dar fiecare hiperparametru din conducta se alege
leave-one-language-out, deci ce guverneaza e transferul PE LIMBA, si acolo ordinea se inverseaza:**

| marime | corelatie peste medii, 5 membri | corelatie pe limba, 5 x 10 = 50 puncte |
|---|---|---|
| `rho3`, decorelarea | **+0.980** | **+0.643** |
| `r3`, calitatea | +0.519 | **+0.791** |

Per membru, corelatia pe limba a lui `rho3` e intre **+0.125 si +0.524**, adica aproape nimic:
few-shot +0.445, rubrica +0.125, marcat +0.368, learner +0.524, frecventa +0.444.

Deplasarile per limba, peste toate cele 50 de puncte: `rho3` medie +0.017 dar abatere 0.051 si interval
[-0.087, +0.143]; `r3` medie -0.042, abatere 0.098, interval [-0.196, +0.261].

## Cum arata esecul in practica

La `frecventa`, **amandoua ipotezele portii au tinut pe medie**: `r3` a coborat cu 0.058 fata de podeaua
presupusa de 0.097, `rho3` a urcat cu 0.028 fata de plafonul de 0.036. Si totusi configuratia a pierdut.
Pe sinhaleza, limba care purta tot castigul de trial, `r3` a cazut +0.478 -> +0.310 si `rho3` a urcat
0.655 -> 0.763, cele mai mari doua deplasari din tot tabelul, amandoua in sens rau, simultan.

**Why:** o marime care transfera pe medie nu autorizeaza o procedura care alege per limba. Media
ascunde exact varianta care decide.

**How to apply:** orice cernere pe trial pentru o decizie LOLO se valideaza pe corelatia PE LIMBA a
statisticii de cernere, nu pe corelatia mediilor. Si se calibreaza pe candidati cu rezultat cunoscut pe
test, nu pe un prag ales. Vezi [[decalaj-trial-test-masurat]] si [[criteriu-plat-mediaza-nu-alege]].
