---
name: bakeoff-etapa1-rezultate
description: "Bloc E etapa 1 e închis: 7 modele × 300 instanțe de trial, Gemma 0.686 și Qwen3-8B 0.565 pe B, selecția LOLO dă 2 câștigători, semnalul C e mort, dar toate cifrele sunt pe trial deci NU se compară cu bara publicată de 0.657"
metadata: 
  node_type: memory
  type: project
  originSessionId: 571bf970-7172-4924-97f7-cb319b21ff41
  modified: 2026-08-17T09:33:55.538Z
---

Rulat **17 august 2026**. Datele brute: `output/bakeoff_<model>.csv`, raportul complet
`output/e_bakeoff.md`, codul `bakeoff_trial.py`. Toate cele 7 modele au trecut D.4 înainte de prima
cifră. 38 de minute în total, zero NaN pe semnalul B în 2100 de instanțe.

## Semnalul B, r mediu pe 10 limbi, pe TRIAL (n = 30 per limbă)

| model | r mediu |
|---|---|
| `gemma4-12b-4bit` | **0.686** |
| `qwen35-9b-8bit` | 0.662 |
| `qwen35-9b-4bit` | 0.622 |
| `qwen3-8b-8bit` | 0.584 |
| `qwen3-8b-4bit`, brațul principal | **0.565** |
| `llama31-8b-4bit` | 0.547 |
| `aya-expanse-8b-4bit` | 0.514 |

Aya iese **ultimul**, deci precedentul din §12.1 se confirmă a doua oară: afirmația de pe model card,
că bate Llama-3.1, nu supraviețuiește măsurătorii pe criteriile noastre. Vezi
[[brate-llm-per-limba]].

## Ce nu se renegociază după rularea asta

1. **Selecția LOLO nu e unanimă, deci e ea însăși un rezultat.** Gemma câștigă pe 9 limbi. Pe
   franceză, selecția pe celelalte 9 alege `qwen35-9b-8bit`, fiindcă Gemma se prăbușește pe sinhaleză
   și îi scade media. Modelul ales dă apoi **0.2996** pe franceză, față de 0.609 cât ar fi dat Gemma.
   **r mediu sub selecție LOLO: 0.6551**, iar prețul protocolului, -0.031, se plătește integral pe o
   singură limbă.
2. **Semnalul C e mort ca semnal.** r mediu per model între -0.080 și +0.072, cu semnul schimbându-se
   între limbi în interiorul aceluiași model. Nu intră în fuziune.
3. **§5.2, costul alegerii pe acoperire: -0.0901 r**, față de alternativa aleasă tot LOLO, cu sd 0.2162
   între limbi. Comparația cu „cel mai bun model pe limba L" dă -0.1834, dar aia e o margine
   superioară, nu o alternativă: acel model e ales folosind chiar trial-ul lui L.
4. **Pe sinhaleză, familia Qwen3-8B e cea mai bună din tot bazinul**, 0.561 pe 4 biți și 0.595 pe 8,
   în timp ce Gemma dă 0.170 și Aya 0.001. Compromisul nu e „acoperire în loc de performanță" peste
   tot, ci „acoperire plus cea mai bună performanță exact unde acoperirea contează".
5. **E.4:** 8 biți aduc +0.0189 r la Qwen3-8B și +0.0395 la Qwen3.5-9B, la 1.15x și 1.11x timp.
6. **E.3, debitul real:** 0.90 s per item la Qwen3-8B-4bit, 1.19 s la Gemma. Pe test, 5624 de ținte,
   asta înseamnă **84 până la 112 minute per model**.

## Capcana care trebuie ținută minte la orice comparație

**Toate cifrele de mai sus sunt pe trial, n = 30 per limbă. Bara publicată e pe test, n între 445 și
600.** Nu se compară direct. Dovada că diferența de split nu e mică e în casă: pe sinhaleză, brațul
înghețat dă 0.222 pe test și publicațiile dau 0.31 la TMU-HIT și 0.33 la G-Eval, dar semnalul B pe
trial dă 0.56. Fie cele 30 de instanțe sinhaleze de trial sunt altfel, fie e zgomot la n = 30. Pragul
de zgomot, calculat: la n = 30, intervalul de 95% pentru un r de 0.60 e [0.31, 0.79].

Măsurătoarea ieftină care ar lămuri, nefăcută: brațul înghețat E1 evaluat pe aceleași 300 de instanțe
de trial. Dă decalajul trial-test pe același model, deci traduce 0.686 într-o predicție pentru test.

## Bara de publicabilitate, pentru referință rapidă

Din Tabelul 13 al lui Nohejl et al., pe test: baseline frecvență 0.478, Archaeology 0.487, TMU-HIT
0.654, **G-Eval cu GPT-4o 0.657**, G-Scale calibrat pe trial 0.669. Brațul înghețat E1 al nostru dă
**0.552 pe test**. Vezi [[noutate-si-precedente-lcp-multilingv]].

**Why:** pragul real nu e 0.487 al lui Archaeology, ci 0.657, dar el e atins cu 30 de etichete în
limba țintă, iar revendicarea noastră e zero-label plus selecție LOLO inclusiv a modelului.

**How to apply:** la 0.64-0.65 pe test, fără etichete, lucrarea e publicabilă. Sub 0.487 nu e lucrare.
Nu cita niciodată o cifră de trial lângă una publicată.

## DEPĂȘIT PARȚIAL, 18 august: cifrele de aici sunt de trial și nu sunt predicții

Etapa 2 a măsurat aceleași modele pe testul complet. `qwen3-8b-4bit` cade de la 0.565 la **0.374**,
Gemma de la 0.686 la **0.642**, iar `qwen35-9b-8bit` pe franceză URCĂ de la 0.2996 la **0.542**. Deci
prețul protocolului nu e -0.031 ci **-0.010**, iar costul §5.2 al brațului principal nu e -0.0901 ci
**-0.2580**. Ordinea modelelor se păstrează, nivelurile nu. Detaliile în [[decalaj-trial-test-masurat]]
și [[etapa2-test-rezultate]].
