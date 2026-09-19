---
name: gemma-nu-poate-da-surprisal
description: "23 aug 2026 - coloana C a lui gemma4-12b-4bit e degenerata, surprisal mediu 23.95 peste ln|V|=12.48; modelul e sanatos prin sablonul de chat (B intact) si colapseaza pe text brut; poarta e analysis_c_sanatate.py"
metadata: 
  node_type: memory
  type: project
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-23T15:58:33.890Z
---

Gasit **23 august 2026**, dintr-un control de cinci linii rulat inainte de a cheltui doua ore de
inferenta. Nu era cautat.

## Cifra care nu se poate

`gemma4-12b-4bit` are surprisal mediu **23.95 nati per subword** pe itemi reali de test. Vocabularul
lui are 262.144 de intrari, deci o distributie **uniforma** ar da ln(262144) = **12.48**. O valoare
peste uniform e imposibila pentru un model antrenat pe text real. Pentru scara, surprisal-ul lui
"Paris" in "The capital of France is ___": qwen3 0.79, qwen35 0.56, llama31 0.81, aya 1.17,
**gemma 23.06**.

## Ce e stricat si ce NU e

    prin SABLONUL DE CHAT (calea lui B)        pe TEXT BRUT (calea lui C)
    "capital of France?" -> "Paris"            "The capital of France is" -> "1111111111"
    rate("thrombocytopenia") = 0.9049
    rate("water")            = 0.0000
    r_B pe test = +0.642, cel mai bun din bazin

**Semnalul B e sanatos, sistemul de 0.683849 nu e afectat.** `<bos>` e o parte din cauza dar nu toata:
adaugat manual, "Paris" scade 23.06 -> 14.84, dar argmaxul ramane o cifra. Cauza de fond se vede la
varianta de 8 biti, care **nu se incarca deloc**: `Received 11 parameters not in model:
vision_embedder.patch_dense.bias, ...`. Checkpointul e multimodal (`gemma4_unified`) si `mlx_lm`
0.31.3 il incarca doar prin remaparea fortata din `LLM_POOL`, la o clasa text-only.

## Poarta, care acum exista: `analysis_c_sanatate.py`

Trei probe pe text brut, si sunt necesare **impreuna**: `uniform` (surprisal mediu < ln|V|),
`degenerare` (>= 3 tokeni distincti in 10 la decodare greedy), `ordonare` (continuare corecta mai
putin surprinzatoare decat una implauzibila). **Gemma TRECE proba de ordonare** (23.06 < 28.79) desi e
degenerat, deci ordonarea singura n-ar fi prins-o.

Rezultat pe tot bazinul: **6 sanatoase din 8**. Cad numai cele doua Gemma. `llama31-8b-4bit`, respins
ca brat B, trece aici, fiindca `surprisal()` ruleaza deliberat fara sablon de chat.

**How to apply:** orice model nou care trebuie sa dea C trece intai prin poarta. Poarta e agnostica de
backend, deci se poate rula si pe `RoLlama3-8b-Instruct` de pe calea romaneasca, unde riscul e din
aceeasi clasa (instruction-tuned, continuare pe text brut) - **nerulat, declarat**. Paperul multilingv
nu e atins, nu pomeneste surprisal. Propozitia din `e_bakeoff_test.md`, "r mediu per model intre
-0.065 si +0.094", trebuie corectata: capatul de -0.065 e al unei coloane degenerate.

Pentru reproductibilitate in paper: modelul care da semnalul B se incarca **numai printr-o remapare
fortata de tip de model**, iar fidelitatea ei e confirmata empiric pe calea de chat si **infirmata pe
calea de text brut**. Vezi [[semnalul-c-surprisal-stare]] si [[brate-llm-per-limba]].
