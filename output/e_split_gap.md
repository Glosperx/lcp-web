# Decalajul trial fata de test, masurat pe ambele semnale

Scris 17 august 2026, completat 18 august dupa etapa 2. Toate cele trei brate de test sunt rulate.

Intrebarea la care raspunde: aproape 12000 de masuratori din Bloc E sunt pe trial, n = 30 per limba,
iar bara publicata e pe test, n intre 445 si 600. Cat se pierde la traducere.

Raspunsul, si e cel care conteaza: **decalajul depinde si de semnal, si de model, deci nu exista o
corectie unica. Dar ORDINEA se pastreaza.**

| semnal | trial | test | decalaj |
|---|---|---|---|
| A, bratul inghetat XLM-R | +0.5216 | +0.5523 | **+0.031** |
| B, nota LLM, `qwen3-8b-4bit`, bratul principal | +0.5650 | +0.3742 | **−0.191** |
| B, nota LLM, `gemma4-12b-4bit` | +0.6860 | +0.6420 | **−0.044** |
| B, nota LLM, `qwen35-9b-8bit`, doar fr | +0.2996 | +0.5420 | **+0.242** |

**Un model bun ramane bun; unul slab se prabuseste.** Decalajul lui Gemma e de patru ori mai mic decat
al bratului principal, iar `qwen35-9b-8bit` pe franceza merge in cealalta directie, cu +0.242: cei 30
de itemi de trial il subestimasera grav. La n = 30, intervalul de 95% pentru r = 0.60 e [0.31, 0.79],
deci nimic din toate astea nu contrazice trial-ul, doar arata cat de putin spune el.

**Ordinea modelelor supravietuieste, si asta salveaza protocolul.** Pe trial Gemma bate bratul
principal pe 8 din 10 limbi; pe test il bate pe 10 din 10. Pe franceza, unde selectia LOLO alege
`qwen35-9b-8bit`, ordinea fata de Gemma se pastreaza si ea, +0.542 fata de +0.642. Deci selectia
leave-one-language-out facuta pe trial ramane valida ca PROCEDURA, chiar daca cifrele ei nu sunt
predictii pentru test. Costul ei masurat pe test: 0.6320 sub selectie LOLO fata de 0.6420 al Gemmei
peste tot, adica **−0.010**, platit integral pe franceza. Pe trial acelasi cost parea −0.031.

Ambele masurate pe aceleasi limbi, aceleasi doua splituri, aceleasi instante. A e din
`e1_trial_gap.md`, acelasi brat antrenat prezicand ambele splituri. B e din `bakeoff_qwen3-8b-4bit.csv`
fata de `bakeoff_test/qwen3-8b-4bit.csv`.

## Semnalul B, limba cu limba

| limba | trial | test | diferenta | sd complexitate, trial/test |
|---|---|---|---|---|
| ca | +0.367 | +0.254 | −0.113 | 0.81x |
| de | +0.795 | +0.342 | −0.453 | 1.16x |
| en | +0.748 | +0.388 | −0.360 | 1.05x |
| es | +0.528 | +0.380 | −0.148 | 1.24x |
| fil | +0.481 | +0.489 | +0.008 | 0.85x |
| fr | +0.406 | +0.401 | −0.005 | 0.92x |
| it | +0.573 | +0.405 | −0.168 | 1.00x |
| ja | +0.576 | +0.455 | −0.121 | 1.04x |
| pt | +0.615 | +0.487 | −0.128 | 1.11x |
| si | +0.561 | +0.141 | −0.420 | 1.68x |
| **medie** | **+0.565** | **+0.374** | **−0.191** | 1.087x |

## Doua explicatii verificate, una confirmata partial si una respinsa

**Restrangerea de interval: contribuie, dar nu ajunge.** Deviatia standard a complexitatii e in medie
de 1.087 ori mai mare pe trial decat pe test, iar directia se potriveste limba cu limba: **singurele
doua limbi fara scadere, fil si fr, sunt exact cele unde trial-ul e mai INGUST decat testul**, 0.85x si
0.92x. Sinhaleza, cu cel mai larg trial relativ (1.68x), are a doua cea mai mare scadere. Dar 8.7% mai
multa imprastiere nu produce singura o scadere de 0.19; atenuarea asteptata e de ordinul 0.04.

**Colapsul de rezolutie: respins.** Semnalul B are practic toate valorile distincte pe ambele
splituri, 445/445 pe catalana si 570/570 pe germana, iar deviatia lui e comparabila: 0.0384 pe test
fata de 0.0401 pe trial. Nu se aplatizeaza la scara, deci nu de aici vine.

**Centrarea: respinsa, dar doar pentru A.** Din `e1_trial_gap.md`, diferenta dintre centrarea pe
propriul bloc de 30 si centrarea pe media de test e in medie −0.0038, cu maximul 0.0117. Semnalul B nu
se centreaza, deci intrebarea nici nu se pune acolo.

## Ce inseamna operational

1. **Nicio cifra de bake-off nu se poate cita ca predictie pentru test.** Gemma cu +0.686 pe trial nu
   inseamna +0.686 pe test, ci +0.642. Se masoara direct, nu se corecteaza cu o constanta.
2. **Costul §5.2 al alegerii pe acoperire creste de trei ori pe test.** Pe trial, bratul principal
   costa −0.0901 r fata de alternativa aleasa LOLO. Pe test costa **−0.2580**, adica 0.3742 fata de
   0.6322. Asta e cifra care trebuie scrisa in lucrare, nu cea de pe trial.
3. **Pretul se vede si in fuziune.** Ponderea w se alege pe trial, cum cere protocolul, iar pe trial B
   pare mai bun decat e pe test. Cu bratul principal, fuziunea da 0.5320, adica **sub A singur**, care
   da 0.5523: w ≈ 0.45 acorda prea mult unui semnal care pe test valoreaza 0.374. Cu bratul selectat
   LOLO, unde B chiar e bun, w iese 0.22 si fuziunea da 0.6522, peste ambele semnale pe toate cele 10
   limbi. Detaliile in `e_fusion_lolo.md` si `e_fusion_qwen3-8b-4bit.md`.
