---
name: poarta-al-treilea-semnal-0107
description: "23 aug 2026 - poarta pentru ORICE al treilea semnal peste fuziune e o singura cifra: corelatia partiala cu eticheta, controland pe fuziune, >= 0.1077; toti cei 13 candidati masurati au sub 0.043"
metadata: 
  node_type: memory
  type: project
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-23T15:59:03.341Z
---

Derivata si validata **23 august 2026**, in `analysis_c_frontiera.py` -> `output/e_c_frontiera_toti.md`.

## Poarta

Pentru fuziunea adoptata F si un candidat C, plafonul peste orice pondere `u` a amestecului
`(1-u)*zF + u*zC` e corelatia multipla, care se rescrie exact ca

    R_max^2 = r_F^2 + partial^2 * (1 - r_F^2)

Deci `R_max >= r_F + bara` devine **o singura cifra**:

> **|corelatia partiala a candidatului cu eticheta, controland pe fuziune| >= 0.1077**

la r_F = 0.683849 si bara 0.0045. Alte ambitii: +0.0022 cere 0.0752, +0.0089 cere 0.1517. Forma
directa: `|r_C - 0.683849*rho| >= 0.078581 * sqrt(1 - rho^2)`. **Ramura de jos e de SUPRESOR**: un
semnal corelat cu fuziunea dar nu cu eticheta corecteaza scazandu-se, deci `u < 0` e legitim si grila
lui `u` trebuie sa se intinda in negativ.

## Ce a trecut: nimic. Opt candidati, toti sub 0.04

    candidat          r_C      rho_F    partial   plafon dR
    resid_lolo       -0.6428  -0.9250   -0.0121   +0.0117 (dar o singura limba)
    qwen3-8b-4bit    +0.0942  +0.1251   +0.0384   +0.0044
    vecinatate       +0.1347  +0.2176   -0.0340   +0.0040
    entropie         +0.3257  +0.4918   -0.0375   +0.0035
    qwen35-9b-8bit   +0.0035  +0.0109   +0.0260   +0.0031
    llama31-8b-4bit  +0.0511  +0.0691   +0.0255   +0.0042
    dezacord_B       -0.1042  -0.1366   -0.0031   +0.0013

**Randul cel mai instructiv e `entropie`:** are cel mai mare r_C din tabel, **+0.326**, de trei ori mai
mult decat surprisal-ul, si e al cincilea dupa plafon, cu partiala **-0.037**, fiindca rho cu fuziunea
e 0.49. Calitatea unui semnal nu spune nimic despre ce aduce.

## A doua conditie, si ea a fost cea ucigasa

Plafonul e cu `u` optim IN-SAMPLE per limba. Sub LOLO se alege un singur `u` global, deci **semnul
corelatiei partiale trebuie sa fie constant peste limbi**. Nu e: germana are **+0.2364** (prag 0.1235)
si filipineza **-0.1611** (prag 0.0788), amandoua peste pragul lor, in **directii opuse**. `u` optim
merge de la -0.36 pe fil la +0.18 pe de.

Si tiparul e o proprietate a **LIMBII, nu a modelului**: corelatiile partiale per limba ale celor trei
familii (Qwen3, Qwen3.5, Llama-3.1) coreleaza intre ele la **0.963, 0.991, 0.949**. Deci un ansamblu
de surprisal-uri nu poate repara nimic, oricat de multi membri ar avea.

**How to apply:** orice candidat de al treilea semnal se trece prin poarta INAINTE de a fi masurat,
si costa sub un minut. Se cer amandoua: `|partial| >= 0.1077` **si** semn constant pe cel putin 8
limbi din 10. Vezi [[frontiera-e-identitate-nu-aproximare]], [[criteriu-plat-mediaza-nu-alege]],
[[transmisia-a-fuziune-masurata]].

## Verificat pe sase surprisal-uri, 23 aug seara

Cele patru modele lipsa s-au rulat pe test cu `--only-c`, 75 de minute. Poarta pe toate sase:
`qwen3-8b-8bit` are cel mai mare plafon din sesiune, **+0.005383, PESTE bara**, si corelatie partiala
tot 0.042. Cap la cap da **-0.000756**. Ansamblul celor sase da **-0.000868**, [-0.001657, -0.000084],
cu filipineza stricata.

**Predictia inregistrata inainte de date se confirma:** ansamblul ramane in +/-0.001 de zero, fiindca
cei sase membri coreleaza intre ei la **0.7506** si medierea nu schimba tiparul per limba.

**Deci plafonul e conditie necesara, nu suficienta.** Ce decide de fapt e constanta semnului peste
limbi. Un candidat al carui plafon trece bara poate iesi negativ cap la cap.

E.4, controlul de cuantizare, se inchide pentru C: qwen3-8b 4bit +0.0942 fata de 8bit +0.1028,
qwen35-9b 4bit +0.0023 fata de 8bit +0.0035. Diferenta intre familii e de zece ori mai mare decat
intre cuantizari.
