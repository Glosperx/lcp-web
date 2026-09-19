---
name: rute-rulare-logits
description: "Ollama si serverul mlx_lm trunchiaza logprobs, deci nu pot servi semnalele B si C; rutele valide sunt transformers si API-ul Python mlx_lm; Qwen3.5 cere MLX pe Mac"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 70704065-2767-4d0f-af75-97c5215eba41
  modified: 2026-08-16T18:44:57.265Z
---

Verificat pe **16 august 2026**. Decide prin ce rulăm semnalele B și C, independent de ce model alegem.

## Ce cer semnalele, exact

| Semnal | Cerința |
|---|---|
| **B**, nota LLM | vectorul **complet** de logits la o poziție, apoi softmax, apoi suma peste **toate** id-urile care se decodează ca „1".."5" |
| **C**, surprisal | forward cu **teacher forcing**, adică scorarea unei secvențe **date**, nu generarea uneia noi |

Capcana SentencePiece înseamnă mai multe id-uri per cifră, `"1"` și `"▁1"`, tratată deja în cod la
`solution_bert.py:257-258`.

## Rutele care NU merg

| Rută | De ce |
|---|---|
| **Ollama** | `top_logprobs` limitat la **0-20**, întoarce doar primii N, nu distribuția completă. Masa peste cifre e trunchiată prin construcție. Iar semnalul C e **blocat complet**: API-ul de generare nu poate face teacher forcing |
| **Serverul `mlx_lm`** | același defect, `logprobs` limitat la **1-10** |

**Regula: orice rută prin server sau API de chat trunchiază.** Faptul că un model rulează în Ollama nu
spune nimic despre dacă e utilizabil aici. Sunt două întrebări diferite.

Notă: Nohejl et al. 2025 au lucrat exact cu limitarea asta pe GPT-4o, `top_logprobs=20`, și le-a mers,
fiindcă la un prompt bine pus cifrele sunt de obicei în top-20. Dar e fragil și nu e ce face codul
nostru.

## Rutele care merg

| Rută | Cum se citesc logits |
|---|---|
| **`transformers`**, Python | `model(ids).logits[0, -1]` |
| **`mlx_lm`**, API Python, nu server | `model(y[None], cache=prompt_cache)` indexat `[:, -1, :]`, sau `generate_step`, care produce `logprobs = logits - mx.logsumexp(logits, keepdims=True)` |

## Ce model prin ce rută, pe Mac

| Model | `transformers` plus MPS | MLX |
|---|---|---|
| Qwen3-8B | **da**, transformer dens clasic | `mlx-community/Qwen3-8B-4bit` 4.61 GB, `-8bit` 8.7 GB |
| **Qwen3.5-9B** | **practic nu.** Gated DeltaNet cere `causal_conv1d` și `fla`, care cer CUDA și Triton. Fără ele cade **tăcut** pe referința PyTorch, cu regresie de latență de ~14x | **da**, `Qwen3.5-9B-MLX-{bf16,8bit,4bit}`, 4bit ~6.6 GB, 25-35 tok/s |
| Gemma 4 12B | cere cuantizare, iar `bitsandbytes` e CUDA-only | **da**, `gemma-4-12B-it-qat-OptiQ-4bit`. Conversia MLX **aruncă turnurile vision și audio**, rămâne decoderul de text |

Corectează afirmația din [[hardware-doua-masini]] că „codul existent pornește pe Mac cu trei linii
schimbate": adevărat pentru Qwen3-8B și orice transformer dens, **fals pentru Qwen3.5**.

**Neverificat:** dacă `causal_conv1d` și `fla` au build pentru Turing SM75, adică RTX 2070 SUPER și T4.

## Ruta fixată de Alexandru, 16 august seara: mixtă, GRUPATĂ PE PRECIZIE

Nu „transformers peste tot" și nu „MLX peste tot". Fiecare din cele două comparații care contează se
face la **o singură precizie**, deci clasamentul nu amestecă modelul cu cuantizarea:

| Grup | Modele | Format |
|---|---|---|
| Candidați braț universal | Qwen3-8B, Qwen3.5-9B, Gemma 4 12B QAT, Aya Expanse 8B, Llama-3.1 ref | **MLX 4-bit** |
| Cvartetul Δ_controlat | Llama-3.1 ref, RoLlama3.1, Swallow v0.3, Gervásio | **transformers bf16** |

Llama-3.1 se descarcă în ambele forme, fiindcă joacă în ambele comparații. Confound-ul de precizie
rămâne **doar între grupuri**, la Δ_larg, unde se declară explicit în paper.

Motivul pentru care „tot pe MLX" a fost respins: **RoLlama3.1 și Gervásio nu au build-uri MLX**,
verificat pe HF; doar Swallow v0.3 are. Uniformitatea ar fi cerut conversie locală cu `mlx_lm.convert`,
după ce oricum se descarcă formatul HF.

Toate cele **5 repo-uri MLX sunt libere**, inclusiv `mlx-community/aya-expanse-8b-4bit`, spre deosebire
de `CohereLabs/aya-expanse-8b` care e `gated: auto`. Deci nu e nevoie de token HF.

## Capcana `transformers` 5.13.1, care atinge direct semnalul B

Codul e scris pe 4.46.3. **`apply_chat_template` are acum `return_dict=True` implicit**, față de
`False` înainte. Deci `solution_bert.py:288` primește un `BatchEncoding`, nu un tensor, iar
`self.model(ids)` îl trimite ca `input_ids`. Se repară cu `return_dict=False`.

`torch_dtype` merge în continuare, `from_pretrained` îl scoate din `kwargs` cu `# kept for BC`.

## Capcana modului de gândire

Qwen3 și Qwen3.5 au `<think>` activ implicit. `apply_chat_template` îl injectează, deci `logits[0,-1]`
ar da distribuția peste deschiderea blocului, nu peste cifre. **`enable_thinking=False` obligatoriu.**
Nu crapă, dă cifre plauzibile și greșite.

Testul care prinde asta înainte de a produce cifre: se verifică pe o singură propoziție că suma
probabilităților peste cele cinci cifre nu e degenerată. Cu modul de gândire activ, iese aproape de zero.

## Actualizare 16 august, seara: ruta e VERIFICATĂ, nu doar fixată. Bloc D închis

Primul LLM a rulat. Evidența completă e în repo, `output/d4_sanity.md`; aici rămân doar lucrurile care
nu se citesc din cod.

**Verificarea „promptul nu conține `<think>`" e INVERSATĂ și nu trebuie folosită.** Măsurat pe
tokenizerele reale: cu `enable_thinking=False` promptul **conține** `<think>`, sub forma blocului
închis `<think>\n\n</think>\n\n`; fără kwarg, Qwen3-8B nu-l conține deloc. Garda corectă e o
conjuncție: bloc închis (prinde doar Qwen3.5), plus masă nedegenerată (singurul criteriu care prinde
Qwen3-8B).

**Pragul `< 1e-9` din codul original e insuficient.** La Qwen3.5 fără gardă masa rămâne 5.17e-06, deci
trece de el, iar `_once()` întoarce **0.0378 în loc de 0.5942**, tăcut. Pragul care prinde e `1e-3`.

**Gemma 4 nu se încarcă sub `mlx-lm` 0.31.3.** `config.json` declară `model_type: gemma4_unified`, iar
`mlx_lm` livrează doar `gemma4`/`gemma4_text` și n-are intrare în `MODEL_REMAPPING`, deci `load()`
ridică `ValueError`. Blochează Gemma în Bloc E, nu în Bloc D. Ocolire neîncercată:
`model_config={"model_type": "gemma4"}`. Alternativa e upgrade de `mlx-lm`, care cere aprobare.

**`TokenizerWrapper` din mlx_lm nu e apelabil.** Deleagă prin `__getattr__`, dar `__call__` e dunder și
se caută pe tip, deci `tok(text, return_offsets_mapping=True)` crapă. Surprisal-ul are nevoie de
tokenizerul HF brut de dedesubt, `tok._tokenizer`.

`mlx_lm.load` acceptă **`revision=`** direct, deci regula SHA-ului nu cere cod în plus.

**Why:** două dintre rutele care par cele mai comode, Ollama și serverul mlx_lm, dau cifre plauzibile
și trunchiate, iar semnalul C nici măcar nu e exprimabil în ele. E același tipar de bug tăcut ca
`enable_thinking`.

**How to apply:** înainte de a propune orice model, întreabă prin ce rută se citesc logits. Vezi
[[fertilitate-tokenizere-masurata]], [[brate-llm-per-limba]].
