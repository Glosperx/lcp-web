---
name: ansamblul-de-modele-nu-se-transfera
description: "Medierea a două LLM-uri câștigă pe trial și pierde pe test, de două ori independent; modelele decorelate de Gemma sunt exact cele slabe"
metadata: 
  node_type: memory
  type: project
  originSessionId: 763bcd63-ce50-4dbe-9cbf-a9053339dfec
  modified: 2026-08-18T07:31:03.667Z
---

Măsurat **18 august 2026**, la întrebarea „dacă corelația între modele e mică, nu le combinăm?".
Premisa e rezonabilă, dar datele o resping.

## Corelațiile între cele 7 modele, pe trial, standardizate în interiorul limbii

Media perechilor distincte e **0.653**, între 0.489 și 0.933. Structura contează mai mult decât media:

- **Perechile de cuantizare sunt același model:** qwen3-8b 4bit/8bit = 0.915, qwen35-9b 4bit/8bit = 0.933.
- **Cele două modele bune sunt corelate între ele:** Gemma cu Qwen3.5-9B = 0.790.
- **Cele decorelate de Gemma sunt exact cele slabe:** Qwen3-8B 0.537 (r = 0.565 pe trial, 0.374 pe
  test), Aya 0.542 (r = 0.514).

Deci nu există o pereche care să fie și decorelată, și bună. Asta e rezultatul, nu un accident de set.

## Ansamblul câștigă pe trial și pierde pe test, de două ori independent

| pereche | trial, Gemma | trial, ansamblu | test, Gemma | test, ansamblu |
|---|---|---|---|---|
| Gemma + Qwen3-8B, 10 limbi | 0.6860 | 0.7091 | **0.6420** | **0.5840** (−0.058) |
| Gemma + Qwen3.5-9B, doar fr | 0.6091 | 0.4997 | **0.6424** | **0.6259** (−0.017) |

Cea mai bună combinație de pe trial, Gemma + Qwen3-8B + Qwen3.5-9B, dă **0.7264**, adică +0.040 peste
cel mai bun model singur și +0.071 peste selecția LOLO argmax. **Toate acele cifre sunt de trial și
niciuna nu se transferă.** Pe test ansamblul pierde pe 9 limbi din 10, câștigă doar pe `fil`.

Cauza e cunoscută din [[decalaj-trial-test-masurat]]: Qwen3-8B pare cu 0.191 mai bun pe trial decât e
pe test. Medierea unui model bun cu unul care se prăbușește trage în jos.

## Legătura cu E.10

E același mecanism ca la prompturi, în [[prompt-ansamblu-decorelat]]: **medierea decorelată repară un
model slab, nu îmbunătățește unul bun.** Acolo ansamblul urca Qwen și cobora Gemma. Aici, la nivel de
modele, se repetă. Două niveluri diferite, aceeași concluzie, ceea ce o face raportabilă ca teză, nu
ca observație izolată.

**Why:** ideea 2 din `~/.claude/plans/idei-imbunatatire-dupa-etapa2.md` cerea 92 de minute de rulare
pentru `qwen35-9b-8bit` pe celelalte 9 limbi de test, ca să se poată face media de modele. Dovada de
pe franceză spune că ar ieși negativ.

**How to apply:** nu se rulează, decât dacă Alexandru vrea cifra completă pentru paper. Dacă totuși se
rulează, ipoteza prealabilă e că ansamblul pierde, deci e o confirmare de rezultat negativ, nu o
căutare de câștig. Vezi [[bakeoff-etapa1-rezultate]] și [[fixul-de-lema-multilingv-masurat]].
