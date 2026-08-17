# D.4: testul de sanatate al lui LLMRater

Un bloc per rulare, adaugat la sfarsit. Propozitia vine din splitul TRIAL,
fara citirea vreunei etichete. Pragurile: masa bruta >= 0.001, concentrare <= 0.999.

## qwen3-8b-4bit: **PASS**

Rulat 2026-08-16 21:41:33. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.725492 |
| **valoare intoarsa de _once()** | **0.6823242189098176** |
| timp incarcare | 3.3 s |
| **timp per item** | **0.557 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0038  3=0.2669  4=0.7255  5=0.0038

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## CONTROL fara enable_thinking, qwen3-8b-4bit: **FAIL**

Rulat 2026-08-16 21:41:53. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| enable_thinking declarat de sablon | fortat off |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **3.440502e-13** |
| concentrare max(p) | nan |
| **valoare intoarsa de _once()** | **None** |
| timp incarcare | 3.5 s |
| **timp per item** | **0.419 s** |

Distributia normalizata peste cifre: n/a

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

Criterii picate:

- 4. masa bruta degenerata: 3.441e-13 < 0.001
- 6. _once() a intors None, nu un float in [0,1]

## qwen35-9b-4bit: **PASS**

Rulat 2026-08-16 21:42:17. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3.5-9B-MLX-4bit` |
| revision | `938d8919941c6e7efd3c7150eff7fe9d12afa631` |
| backend | mlx |
| device | mlx |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.990931e-01** |
| concentrare max(p) | 0.410179 |
| **valoare intoarsa de _once()** | **0.594162343490893** |
| timp incarcare | 4.1 s |
| **timp per item** | **1.294 s** |

Distributia normalizata peste cifre: 1=0.0204  2=0.1037  3=0.4102  4=0.4102  5=0.0555

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## CONTROL fara enable_thinking, qwen35-9b-4bit: **FAIL**

Rulat 2026-08-16 21:42:23. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3.5-9B-MLX-4bit` |
| revision | `938d8919941c6e7efd3c7150eff7fe9d12afa631` |
| backend | mlx |
| device | mlx |
| enable_thinking declarat de sablon | fortat off |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | False |
| **masa bruta peste cele 5 cifre** | **5.171903e-06** |
| concentrare max(p) | 0.923748 |
| **valoare intoarsa de _once()** | **0.03783820159288265** |
| timp incarcare | 4.3 s |
| **timp per item** | **0.486 s** |

Distributia normalizata peste cifre: 1=0.9237  2=0.0316  3=0.0204  4=0.0180  5=0.0062

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

Criterii picate:

- 2. bloc de gandire DESCHIS la finalul promptului
- 4. masa bruta degenerata: 5.172e-06 < 0.001

---

# Sinteza celor patru rulari de mai sus. 16 august 2026

**D.4 e trecut.** Qwen3-8B-4bit produce primul numar dat de un LLM in proiect: **0.6823** pe instanta
de trial `ca` / `successius`, cu masa de probabilitate **1.000000** peste cele cinci cifre si
**0.56 s per item** pe MLX. Se inchide si verificarea B.1, un `LLMRater()._once` real dupa coborarea
primului model.

## Ce dovedesc rularile de control

Perechea cu si fara `enable_thinking=False`, pe acelasi model si aceeasi propozitie:

| model | masa cu garda | masa fara garda | `_once()` cu garda | `_once()` fara garda |
|---|---|---|---|---|
| Qwen3-8B-4bit | 1.000000 | 3.44e-13 | 0.6823 | `None` |
| Qwen3.5-9B-4bit | 0.999093 | 5.17e-06 | **0.5942** | **0.0378** |

Randul lui Qwen3.5 e cel care conteaza. Fara garda, `_once()` **nu esueaza**: intoarce 0.0378 in loc
de 0.5942. Masa ramasa, 5.17e-06, trece de pragul `< 1e-9` din codul original, deci varianta veche ar
fi produs tacut numarul gresit pe toate cele 300 de instante. Exact tiparul „nu crapa, da cifre
plauzibile si gresite". Pragul care il prinde e `MASS_MIN = 1e-3`.

Criteriile au putere separata, si fiecare a fost exercitat:

- **criteriul 2**, bloc de gandire deschis, se aprinde numai la Qwen3.5, al carui sablon injecteaza
  `<think>\n` in prompt. La Qwen3-8B promptul arata curat si criteriul nu prinde nimic.
- **criteriul 4**, masa degenerata, se aprinde la amandoua. E singurul care prinde Qwen3-8B.

De aceea garda e o conjunctie, nu un singur test. Verificarea „promptul nu contine `<think>`" ar fi
fost **inversata**: configuratia corecta contine `<think>`, sub forma blocului inchis
`<think>\n\n</think>\n\n`, iar cea rupta la Qwen3-8B nu-l contine deloc.

## Un defect prins de test, si reparat

Prima rulare a dat **masa bruta 2.000000**, adica o suma de probabilitati peste 1. Cauza: la
tokenizerele BPE `encode("1")` si `encode(" 1")` intorc acelasi id, iar bucla din `LLMRater.__init__`
il adauga de doua ori, deci `self.digit["1"] = [16, 16]` si masa se numara dublu.

La Qwen dublarea e simetrica pe toate cele cinci cifre, deci normalizarea o anuleaza si `_once()`
iesea corect: 0.6823242189098176 inainte si dupa reparatie, identic. Pe un tokenizer unde `▁1` e id
distinct doar pentru unele cifre, raportul dintre cifre s-ar fi distorsionat si scorul ar fi iesit
gresit in tacere. Reparat prin deduplicare, plus un criteriu nou, **4b**, care respinge orice masa
peste 1.

## Neverificat

- **Gemma 4 nu se incarca** sub `mlx-lm` 0.31.3: `config.json` declara `model_type: gemma4_unified`,
  iar `mlx_lm` livreaza doar `gemma4`/`gemma4_text` si nu are intrare in `MODEL_REMAPPING`. Ocolirea
  prin `model_config={"model_type": "gemma4"}` nu a fost incercata.
- Celelalte patru modele din bazin, `qwen3-8b-8bit`, `qwen35-9b-8bit`, `llama31-8b-4bit`,
  `aya-expanse-8b-4bit`. Comanda: `python d4_sanity.py --model <cheie>`.
- Debitul de 0.56 s per item e masurat pe **o singura** instanta scurta, dupa incalzire. Nu e o
  estimare valida pentru cele 300 de instante de trial.
