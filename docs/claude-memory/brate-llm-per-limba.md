---
name: brate-llm-per-limba
description: "Qwen3-8B listeaza toate 11 limbile dar tokenizerul lui cade pe sinhaleza; alegerea s-a mutat spre Gemma 4, de confirmat prin bake-off; 9 limbi au model adaptat, si+fil niciunul"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f92e8d7e-2eca-4649-a573-d0cd5dc259e5
  modified: 2026-08-17T09:34:21.017Z
---

Verificat pe **16 august 2026**, pe model cards și rapoarte tehnice, nu pe reputație.

## Criteriul, care e mai important decât alegerea

Nu contează care model e „cel mai bun", ci **care publică o listă enumerată de limbi pe care s-o pot
cita în paper**. Sinhaleza și filipineza sunt limbile pe care se sprijină lucrarea și exact cele pe
care aproape nimeni nu le listează.

| Model | Licență | Acoperire declarată | Listă enumerată |
|---|---|---|---|
| **`Qwen/Qwen3-8B`** | Apache-2.0 | 119 limbi | **da**, sinhaleza și tagalog numite explicit |
| `utter-project/EuroLLM-9B-Instruct` | Apache-2.0 | 35 limbi | da, dar **fără si și fil** |
| `CohereLabs/aya-expanse-8b` | CC-BY-NC | 23 limbi | da, dar **fără ca, si, fil** |
| `Qwen/Qwen3.5-9B` | Apache-2.0 | „201 languages and dialects" | **nu** |
| `google/gemma-4-12B` | Apache-2.0 | „35+ / 140+ pre-trained" | **nu** |
| `google/gemma-3-*` | Gemma ToU | „over 140" | **nu** |

**Brațul universal = `Qwen/Qwen3-8B`.** Qwen3.5-9B și Gemma 4 12B intră doar ca braț de robustețe,
fiindcă acoperirea lor pe si și fil e nedocumentată. Alexandru a întrebat explicit de
`gemma4:12b-it-qat` și `qwen3.5:9b` pe 16 august; răspunsul e ăsta.

## Capcana care ar fi stricat semnalul B în tăcere

**Qwen3 și Qwen3.5 au mod de gândire activ implicit.** `apply_chat_template` injectează un bloc
`<think>`, deci `logits[0, -1]` citit ca acum ar da distribuția peste deschiderea blocului, nu peste
„1".."5". **Obligatoriu `enable_thinking=False`.** Nu crapă, dă cifre plauzibile și greșite.

Partea bună: capcana SentencePiece `"1"` față de `"▁1"` e **deja tratată** în cod, la
`solution_bert.py:257-258`.

## Brațul monolingv: 9 limbi din 11, și niciunul nu e monolingv de fapt

| Limbă | Model | Ce e de fapt |
|---|---|---|
| ro | `OpenLLM-Ro/RoLlama3.1-8b-Instruct` | fine-tune peste **Llama-3.1-8B** |
| ja | `tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.3` | continual pretraining peste **Llama-3.1-8B** |
| pt | `PORTULAN/gervasio-8b-portuguese-ptpt-decoder` | fine-tune peste **Llama-3.1-8B** |
| it | `sapienzanlp/Minerva-7B-instruct-v1.0` | de la zero, 2,5T token-i |
| fr | `OpenLLM-France/Lucie-7B-Instruct-v1.1` | de la zero |
| de | `DiscoResearch/DiscoLM_German_7b_v1` | peste LeoLM/Mistral |
| es, ca | `BSC-LT/salamandra-7b-instruct` | **multilingv pe 35 de limbi**, instruct focalizat ca/en/es |
| **si** | **niciunul** | doar `polyglots/SinLlama_v01`, **bază, fără instruct** |
| **fil** | **niciunul** | doar proxy regional SEA-LION / SeaLLMs |

**Constatarea care reformulează contribuția:** Δ naiv nu compară „monolingv față de universal", ci
„adaptat la limbă față de generic". Dar **ro, ja și pt au toate aceeași bază Llama-3.1-8B**, deci
există un contrast **controlat**, fără confound de scară sau arhitectură.

Decis de Alexandru pe 16 august: **se raportează ambele forme**, Δ_controlat pe ro/ja/pt și Δ_larg pe
9 limbi cu Qwen3-8B ca referință. Dezacordul dintre ele e el însuși un rezultat.

**Why:** alegerea intuitivă, Aya Expanse, ar fi fost greșită (îi lipsesc ca, si, fil), iar alegerea
„cea mai nouă", Gemma 4 sau Qwen3.5, nu poate susține argumentul de acoperire.

**How to apply:** si și fil rămân condiții pur cross-linguale pe brațul universal, declarat explicit,
nu ascuns. Licențial, `RoLlama3.1` și `Aya Expanse` sunt CC-BY-NC, ceea ce blochează un serviciu, nu
experimentele. Vezi [[noutate-si-precedente-lcp-multilingv]], [[hardware-doua-masini]].

---

## ACTUALIZARE 16 august 2026, seara: criteriul de mai sus era greșit, nu doar alegerea

Alexandru a cerut comparația pas cu pas și a contestat două dintre eliminări. Avea dreptate la
amândouă, iar măsurătoarea care a urmat a răsturnat alegerea. Detaliile complete în planul
`~/.claude/plans/pai-si-cum-se-zazzy-shamir.md`.

**1. Argumentele de capacitate erau false.** Qwen3.5-9B și Gemma 4 12B rulează amândouă bine pe Mac,
prin MLX. Eliminarea lor pe kernel-uri și memorie nu se susține. Vezi [[rute-rulare-logits]].

**2. Criteriile brațului principal nu se aplică celui de robustețe.** Lista enumerată de limbi e
obligatorie doar pentru brațul care susține în paper afirmația de acoperire. Pentru „se ține concluzia
cu alt model universal" nu contează deloc. Tratasem greșit cele două ca având aceleași cerințe.

**3. Decisiv: lista lui Qwen3 nu se traduce în capacitate.** Măsurat pe cele 5624 de ținte, Qwen3-8B
cade pe **byte fallback pe sinhaleză**, 11.56 subword-uri per țintă, deși o listează explicit. Gemma 4
o tokenizează aproape ca XLM-R, deși nu publică nicio listă. Cifrele și validarea metodei sunt în
[[fertilitate-tokenizere-masurata]].

**Consecința: argumentul de acoperire se mută de pe citarea unei liste pe măsurătoarea noastră**, care
e dovadă directă și are grup de control. Cu criteriul ăsta, **Gemma 4 12B trece în față**.
**Nefixat încă**, fiindcă fertilitatea e poartă de screening, nu test. Decide bake-off-ul pe trial.

### Corecția de citare pentru Qwen3, dacă totuși rămâne

Lista celor 119 limbi **nu e în raportul tehnic și nu e pe model card**. E doar în blogul
[qwenlm.github.io/blog/qwen3](https://qwenlm.github.io/blog/qwen3/), tabelul „Language Family". Se
citează raportul tehnic pentru număr și blogul pentru listă, ca surse distincte.

### Modele verificate în plus

| Model | Constatare |
|---|---|
| `aya-expanse-32b` | **exact aceleași 23 de limbi ca 8B.** Acoperirea nu se cumpără cu parametri |
| `CohereLabs/tiny-aya-global`, feb 2026 | 3.35B, 70+ limbi, **10 din 11 ale noastre**, mai mult decât Expanse. Dar **fără sinhaleză**, nici în varianta `tiny-aya-fire` pentru Asia de Sud |
| `CohereForAI/aya-101` | acoperă **toate 11**, Apache-2.0, dar e **mT5-xxl encoder-decoder**, deci surprisal-ul nu e aceeași cantitate. Eliminat pe arhitectură |
| `Qwen3.6` | serie existentă, 27B și 35B-A3B, aceeași problemă de enumerare, dimensiuni peste ce încape |

**Constatarea de scris în paper:** toată linia **cauzală** Cohere ratează sinhaleza, inclusiv varianta
regională declarată „best for South Asian languages". Dovadă independentă pentru C4, mai puternică
decât argumentul CC-100, fiindcă deficitul persistă la un laborator care își face un scop declarat din
limbile slab servite.

### `meta-llama/Llama-3.1-8B-Instruct`, ce e și de ce ne trebuie

Lansat 23 iulie 2024, 8B, context 128K, licență Llama 3.1 Community. Suportă oficial **8 limbi**: en,
de, fr, it, pt, hi, es, th, adică 6 din cele 11 ale noastre. **Nu e candidat pentru brațul universal.**

Rolul lui e unul singur: **referința lui Δ_controlat**, fiindcă e baza comună a celor trei modele
adaptate, RoLlama3.1, Swallow și Gervásio. Fără el nu ai de ce scădea.

**Predicție testabilă gratuită:** din cele trei limbi ale lui Δ_controlat, **pt e pe lista oficială a
lui Llama-3.1, iar ro și ja nu sunt.** Deci Δ ar trebui să iasă **mai mic pe pt** decât pe ro și ja.
Dacă nu iese așa, ceva e greșit în montaj, nu în teorie. Verificare internă pentru C2, cost zero.

#### Accesul a fost RESPINS pe 16 august, și nu contează

Cererea la `meta-llama/Llama-3.1-8B-Instruct` a fost respinsă, poarta e `gated: "manual"`, iar
`resolve/main` dă 401. **Oglinzile negate rezolvă complet problema**, verificat pe API în aceeași zi:

| Repo | `gated` |
|---|---|
| `NousResearch/Meta-Llama-3.1-8B-Instruct` | false |
| `unsloth/Meta-Llama-3.1-8B-Instruct` | false |
| `mlx-community/Meta-Llama-3.1-8B-Instruct-{4bit,8bit,bf16}` | false, 4.53 / 8.54 / 16.08 GB |
| `NousResearch/Meta-Llama-3.1-8B`, **baza** | false |

Identitatea e **dovedită, nu presupusă**: NousResearch și unsloth au aceiași sha256 LFS pe toate cele
patru shard-uri (`2b1879f3`, `09d433f6`, `fc1cdddd`, `92ecfe1a`), iar dimensiunile coincid octet cu
octet cu meta-llama.

**Capcana, care atinge semnalul B:** `tokenizer_config.json`, adică șablonul de chat, **diferă**.
meta-llama azi are 55351 octeți, build-urile MLX au 55351/55350, dar **NousResearch are 50870**,
instantaneu din iulie 2024. B citește `logits[0, -1]` după `apply_chat_template`, deci alt șablon e
alt prompt.

**Alegerea: `mlx-community/Meta-Llama-3.1-8B-Instruct-bf16`.** Șablon curent, bf16 deci fără confound
de cuantizare, 16.08 GB intră pe M5, și ruta e oricum MLX pentru Qwen3.5 și Gemma 4. Pe
`transformers`, NousResearch cu `revision=` fixat și șablonul declarat.

**De verificat înainte de descărcare, nu presupus:** dacă RoLlama3.1, Swallow și Gervásio pornesc din
Llama-3.1-8B **base**, atunci Δ_controlat față de Instruct-ul Meta măsoară adaptarea la limbă **plus**
patru rețete diferite de instruct tuning. Semnalul C nu cere șablon de chat deci poate folosi baza,
B îl cere. Baza e la fel de negată la NousResearch.

---

## ACTUALIZARE 17 august 2026: brațul monolingv nu se mai descarcă

E1 a rulat, iar criteriul §5.2 a dat **σ_Δ = 0.0369**, peste pragul de 0.030. Designul centrat pe Δ e
mort, deci **cvartetul adaptat pe limbă nu se mai descarcă**: RoLlama3.1, Swallow v0.3, Gervásio,
circa 80 GB. Cu ele cad E3, E4 și contribuția C2. Vezi [[lolo-exista-deja-in-cod]] și
[[paper-extensie-multilingva-arr-octombrie]].

**Ce rămâne valabil din tabelele de mai sus:** brațul universal. Cele 5 modele MLX 4-bit sunt
descărcate, cu SHA fixat, plus **Qwen3-8B și Qwen3.5-9B și pe 8 biți**, ca **control de cuantizare**
decis de Alexandru pe 17 august. Motivul controlului: Gemma 4 pe 8 biți încape în 24 GB, deci memoria
nu era argumentul, dar checkpoint-ul Gemma ales e **QAT** iar variantă QAT pe 8 biți **nu există**,
verificat, 404. Deci în loc să mutăm Gemma pe 8 biți, măsurăm direct cât costă cuantizarea.

Total pe disc: 47 GB, evidența în `output/bloc0_downloads.md`.

**Niciunul n-a rulat încă.** Blochează Bloc D, șapte reparații în `LLMRater`.

## ACTUALIZARE 17 august 2026, seara: toate au rulat, iar Gemma 4 s-a deblocat

**Gemma 4 se încarcă**, prin `model_config={"model_type": "gemma4"}` trecut la `mlx_load`, opt-in doar
pe intrarea ei din `LLM_POOL`. Trece D.4 cu masă 0.99998. Nu mai e nevoie de upgrade de `mlx-lm`.
Neverificat, și de ținut minte: „nu crapă" nu e „arhitectura e exact cea declarată".

**Alegerea brațului principal are acum cifre**, în [[bakeoff-etapa1-rezultate]]. Qwen3-8B nu e cel mai
bun, e al cincilea din șapte, dar e cel mai bun pe sinhaleză, adică exact limba pentru care s-a ales pe
acoperire. Aya, alegerea „intuitivă" pe care model card-ul o dădea peste Llama-3.1, iese ultima.
