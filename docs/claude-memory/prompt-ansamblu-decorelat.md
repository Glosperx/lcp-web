---
name: prompt-ansamblu-decorelat
description: "E.10 măsurat: rescrierea unui singur prompt nu aduce nimic, iar pârghia e medierea prompturilor DECORELATE; CoT colapsează rezoluția dar e valoros în ansamblu exact fiindcă greșește altfel"
metadata: 
  node_type: memory
  type: project
  originSessionId: 571bf970-7172-4924-97f7-cb319b21ff41
  modified: 2026-08-17T11:50:02.866Z
---

Rulat **17 august 2026** pe `qwen3-8b-4bit`, cele 300 de instanțe de trial, 2100 de măsurători.
Cod: `prompt_lab.py`. Date: `output/promptlab_qwen3-8b-4bit.csv`. Raport: `output/e10_prompt.md`.

## Ce nu funcționează

Toate cele patru prompturi individuale cad între **0.452 și 0.507** în r mediu pe 10 limbi. Rolul de
cursant, „intermediate learner of {lang}", bate rolul de expert cu **+0.026**, deci ablația publicată
G-Eval se confirmă doar ca direcție, nu ca mărime. **Rubrica explicită strică** (0.452). Few-shot
cross-lingual cu 6 exemple din celelalte 9 limbi dă 0.484, exact cât prezice teoria: Pearson e
invariant la scală, iar calibrarea e tot ce aduc exemplele etichetate.

## Ce funcționează, și de ce

Promptul din bake-off, 0.565, e o medie a două prompturi de 0.481 și 0.480. **Tot avantajul lui vine
din mediere, nu din conținut.** Structura de corelații spune când medierea ajută:

| pereche | corelație între scoruri | câștigul medierii |
|---|---|---|
| expert și learner | 0.909 | +0.006, adică nimic |
| expert și short | 0.605 | **+0.085** |

Două prompturi care spun același lucru cu alte cuvinte nu sunt un ansamblu.

**Consecința contraintuitivă: cele mai slabe variante individual sunt cele mai valoroase în ansamblu.**
Ansambluri cu ponderi egale: expert+short 0.5650, plus learner 0.5644, plus rubrică 0.5571, plus
few-shot 0.5897, **plus CoT 0.6077**. Sub selecție leave-one-language-out peste variante, ansamblul
complet e ales pentru toate cele 10 limbi: **r = 0.6077 față de 0.5650, câștig +0.0427, 8 din 10 limbi
în creștere, sd 0.0785, adică 1.7 erori standard.** Sugestiv, nu stabilit la 9 grade de libertate.

## CoT: mecanismul exact al eșecului

Pe cele 300 de instanțe, **78 dau exact 0.500** și rămân doar **105 valori distincte din 300**, față de
300 din 300 la baseline. Rationale-ul generat e coerent și corect, dar la pasul de notare modelul pune
toată masa pe o singură cifră, chiar când propria analiză spune contrariul (`agaw`, filipineză,
etichetă 0.075, analiză „accessible to average readers", distribuție `[0, 0.0001, 0.9999, 0, 0]`).

**Nu dispare varianța**, sd-ul lui CoT e chiar mai mare decât al baseline-ului, 0.0549 față de 0.0400.
Dispare **rezoluția**: un sfert din itemi devin egali între ei, iar egalitățile distrug ordinea, care e
tot ce măsoară Pearson.

**Why:** semnalul B nu e răspunsul modelului, e distribuția lui de incertitudine peste cifrele 1..5 la
o poziție. Orice face modelul mai decis strică citirea. Deliberarea produce angajament.

**How to apply:** nu căuta promptul cel mai bun, caută prompturi decorelate de cele existente. Criteriul
de adăugare a unei variante noi e corelația ei cu setul, nu r-ul ei individual. Selecția variantei e
tuning, deci se face LOLO, exact ca alegerea modelului din §5.1.

## Costul, măsurat

0.62 s per item promptul actual, 2.07 s ansamblul fără CoT, **5.24 s ansamblul complet**, fiindcă CoT
singur costă 3.17 s. Pe cele 5624 de ținte de test: 58 de minute, 3.2 ore, respectiv **8.2 ore** per
model.

## Rezerva s-a închis, și răspunsul e NEGATIV

Măsurat pe Gemma în aceeași zi, 7 variante × 300 de instanțe. **Câștigul din ansamblu nu se transferă,
deci nu recuperează costul de acoperire. Fraza aia nu se poate scrie.**

| | Qwen3-8B-4bit | Gemma-4-12B-4bit |
|---|---|---|
| baseline, cele două prompturi | 0.5650 | 0.6860 |
| cel mai bun ansamblu disponibil | 0.623 (e8) | 0.700 (e5) |
| **sub selecție LOLO peste variante** | **0.6182, adică +0.053** | **0.6808, adică -0.005** |
| corelația medie între cele 7 prompturi | **0.541** | **0.772** |

**Mecanismul:** ansamblul câștigă proporțional cu cât de decorelate sunt erorile. Prompturile Gemmei
sunt individual bune și corelate 0.772 între ele, deci nu mai există eroare independentă de mediat. Pe
setul identic de candidați, e5 pe amândouă, decalajul scade doar de la 0.121 la 0.110.

Corolarul, care e o teză utilă în sine: **medierea prompturilor repară un model slab, nu îmbunătățește
un model bun.** Pe Gemma, selecția LOLO peste variante pierde chiar 0.019 față de a folosi e5 peste tot,
fiindcă alege `v3_fewshot` pe ca, it și pt, unde apoi iese mai prost. E același preț al protocolului,
mutat de pe dimensiunea modelului pe dimensiunea promptului.

**Rezerva rămasă, mai mică:** Gemma n-are `v4_cot`, rularea a fost oprită deliberat înainte de el, deci
setul ei de candidați e mai mic cu unul. Costul închiderii: circa 30 de minute.

**Verificare de consistență, gratuită:** `e2_ansamblu` pe Gemma dă 0.686, identic cu cifra din
bake-off produsă de alt script. Vezi [[bakeoff-etapa1-rezultate]].

**Celulă de urmărit:** pe sinhaleză, Gemma cu rolul de cursant dă **0.691**, în timp ce celelalte
prompturi ale ei dau între 0.049 și 0.346. Un singur n = 30, deci ipoteză, nu rezultat: rolul ar putea
conta cel mai mult exact unde modelul e cel mai slab.

## ÎNCHIS, 18 august: `v4_cot` pe Gemma nu răstoarnă nimic

Ultima variantă lipsă a rulat, 300 de instanțe în 30.1 minute. `v4_cot` singur dă **0.556** pe Gemma,
față de 0.347 pe Qwen, deci CoT nu e slab pe un model bun. În ansamblu însă scara merge în oglindă:
`e5` 0.700, `e6` 0.696, `e7` 0.686, `e8` 0.688 pe Gemma, în timp ce pe Qwen urcă monoton de la 0.590 la
0.623. Selecția LOLO peste variante rămâne **identică** cu cea dinainte de a exista `v4_cot`, 0.6808,
și niciunul din cele trei ansambluri nou deblocate nu câștigă vreo limbă. Verdictul în
`output/e10_verdict.md`. Consecință operațională: **ansamblul de prompturi pe test, 8.2 ore per model,
nu se justifică pe Gemma.**
