---
name: decalaj-trial-test-masurat
description: "Decalajul trial-test e măsurat și depinde și de semnal, și de model, cu semne opuse, deci nicio cifră de trial nu e o predicție; dar ORDINEA modelelor supraviețuiește, ceea ce salvează protocolul LOLO"
metadata: 
  node_type: memory
  type: project
  originSessionId: 881f8b35-360d-445f-8f36-3dfe03afca8e
  modified: 2026-08-17T21:37:11.602Z
---

Măsurat 17 spre 18 august 2026, pe același braț și aceleași instanțe. Detaliile în
`output/e_split_gap.md` și `output/e1_trial_gap.md`.

| semnal | trial | test | decalaj |
|---|---|---|---|
| A, brațul înghețat XLM-R | 0.5216 | 0.5523 | **+0.031** |
| B, `qwen3-8b-4bit`, brațul principal | 0.5650 | 0.3742 | **−0.191** |
| B, `gemma4-12b-4bit` | 0.6860 | 0.6420 | **−0.044** |
| B, `qwen35-9b-8bit`, doar franceza | 0.2996 | 0.5420 | **+0.242** |

**Nu există o corecție unică.** Decalajul își schimbă semnul între semnale și între modele. Un model
bun rămâne bun, unul slab se prăbușește. La n = 30, intervalul de 95% pentru r = 0.60 e [0.31, 0.79],
deci nimic din asta nu contrazice trial-ul, doar arată cât de puțin spune el.

**Ordinea supraviețuiește, și ăsta e lucrul care salvează protocolul.** Pe trial Gemma bate brațul
principal pe 8 limbi din 10; pe test îl bate pe 10 din 10. Deci selecția leave-one-language-out făcută
pe trial rămâne validă **ca procedură**, chiar dacă cifrele ei nu sunt predicții. Costul ei real pe
test: −0.010, față de −0.031 cât părea pe trial.

## Două explicații verificate, ca să nu se refacă munca

- **Restrângerea de interval contribuie, dar nu ajunge.** Deviația complexității e în medie de 1.087
  ori mai mare pe trial, iar direcția se potrivește limbă cu limbă: singurele două limbi fără scădere,
  fil și fr, sunt exact cele unde trial-ul e mai îngust. Atenuarea așteptată e însă de ordinul 0.04, nu
  0.19.
- **Colapsul de rezoluție: respins.** B are practic toate valorile distincte pe ambele splituri, cu
  deviație comparabilă, 0.0384 pe test față de 0.0401 pe trial.
- **Zgomotul de centrare: respins pentru A.** Centrarea celor 30 de itemi pe media lor față de media de
  test diferă cu −0.0038 în medie.

Consecința pentru orice sesiune viitoare: **nicio cifră de trial nu se citează ca predicție pentru
test, și nici măcar corectată.** Vezi [[bakeoff-etapa1-rezultate]] și [[etapa2-test-rezultate]].

## A patra rasturnare, 22 august 2026, si e cea mai informativa

`frecventa` a trecut o poarta de cernere **calibrata pe membri cu rezultat cunoscut pe test**, cu al
doilea cel mai mare castig de trial masurat vreodata (+0.0130, dupa +0.0153 al lui few-shot), si a
cazut pe test cu -0.0024.

**Amandoua ipotezele portii au tinut pe medie**: `r3` a coborat cu 0.058 fata de podeaua presupusa de
0.097, `rho3` a urcat cu 0.028 fata de plafonul de 0.036. Deci nu ipotezele au fost gresite, ci
marimea pe care erau puse: transferul se masoara PE LIMBA, nu pe medie, fiindca selectia e LOLO. Vezi
[[transferul-se-masoara-pe-limba]] si [[prompturi-decorelate-cernute]].
