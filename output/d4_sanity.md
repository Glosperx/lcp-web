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

## qwen3-8b-4bit: **PASS**

Rulat 2026-08-17 11:26:38. Instanta trial: lang `ca`, tinta `successius `.

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
| timp incarcare | 5.2 s |
| **timp per item** | **0.597 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0038  3=0.2669  4=0.7255  5=0.0038

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt legacy]: **PASS**

Rulat 2026-08-17 11:30:18. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | legacy, in romana, fara nume de limba |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.725492 |
| **valoare intoarsa de _once()** | **0.6823242189098176** |
| timp incarcare | 4.3 s |
| **timp per item** | **0.597 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0038  3=0.2669  4=0.7255  5=0.0038

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:30:23. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.558182 |
| **valoare intoarsa de _once()** | **0.606960451846612** |
| timp incarcare | 3.8 s |
| **timp per item** | **0.511 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0070  3=0.5582  4=0.4347  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:30:38. Instanta trial: lang `ja`, tinta `連れ戻す`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Japanese` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.903421 |
| **valoare intoarsa de _once()** | **0.5234657313822401** |
| timp incarcare | 3.8 s |
| **timp per item** | **0.409 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0014  3=0.9034  4=0.0952  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:30:43. Instanta trial: lang `si`, tinta `තථාගතයන්`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Sinhala` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.869331 |
| **valoare intoarsa de _once()** | **0.7233783862608176** |
| timp incarcare | 3.4 s |
| **timp per item** | **0.478 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0006  3=0.1177  4=0.8693  5=0.0124

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:30:48. Instanta trial: lang `fil`, tinta `agaw`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Filipino` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.927478 |
| **valoare intoarsa de _once()** | **0.5115155549927157** |
| timp incarcare | 3.6 s |
| **timp per item** | **0.272 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0132  3=0.9275  4=0.0593  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## llama31-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:31:10. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Meta-Llama-3.1-8B-Instruct-4bit` |
| revision | `241a666dad6cb93c8ff213d39a7f34a36bf26db4` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | False |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999571e-01** |
| concentrare max(p) | 0.449005 |
| **valoare intoarsa de _once()** | **0.4129090216033571** |
| timp incarcare | 3.6 s |
| **timp per item** | **0.838 s** |

Distributia normalizata peste cifre: 1=0.0598  2=0.4490  3=0.2766  4=0.2088  5=0.0057

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## aya-expanse-8b-4bit [prompt multi]: **FAIL**

Rulat 2026-08-17 11:31:15. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/aya-expanse-8b-4bit` |
| revision | `3a7cee37dd4ab4ed76642f61f6253da4748e63ba` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | False |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.864342e-01** |
| concentrare max(p) | 0.999931 |
| **valoare intoarsa de _once()** | **0.5000168108714715** |
| timp incarcare | 4.1 s |
| **timp per item** | **0.508 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0000  3=0.9999  4=0.0001  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[24]` | '1' |
| 2 | `[25]` | '2' |
| 3 | `[26]` | '3' |
| 4 | `[27]` | '4' |
| 5 | `[28]` | '5' |

Criterii picate:

- 5. masa concentrata integral pe o cifra: 0.999931 > 0.999

## qwen3-8b-8bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:31:22. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-8bit` |
| revision | `48a0b75b1ae72503e21e1558d040bc227510ff06` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.499624 |
| **valoare intoarsa de _once()** | **0.6247188607852716** |
| timp incarcare | 4.7 s |
| **timp per item** | **1.112 s** |

Distributia normalizata peste cifre: 1=0.0000  2=0.0008  3=0.4996  4=0.4996  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen35-9b-8bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:31:29. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3.5-9B-MLX-8bit` |
| revision | `84f7c2deea248d8df56240f88102def51c7ed5d6` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.998200e-01** |
| concentrare max(p) | 0.571648 |
| **valoare intoarsa de _once()** | **0.4864082348429244** |
| timp incarcare | 5.3 s |
| **timp per item** | **0.824 s** |

Distributia normalizata peste cifre: 1=0.0026  2=0.2383  3=0.5716  4=0.1856  5=0.0018

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## aya-expanse-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:35:24. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/aya-expanse-8b-4bit` |
| revision | `3a7cee37dd4ab4ed76642f61f6253da4748e63ba` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | False |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.864342e-01** |
| concentrare max(p) | 0.999931 |
| **valoare intoarsa de _once()** | **0.5000168108714715** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1163** pe 10/10 finite |
| timp incarcare | 3.9 s |
| **timp per item** | **0.289 s** |
| timp sonda de dispersie, 10 limbi | 4.4 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3753  0.2906  0.4486  0.4692  0.6340  0.4863  0.5045  0.3738  0.6904  0.3832

Distributia normalizata peste cifre: 1=0.0000  2=0.0000  3=0.9999  4=0.0001  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[24]` | '1' |
| 2 | `[25]` | '2' |
| 3 | `[26]` | '3' |
| 4 | `[27]` | '4' |
| 5 | `[28]` | '5' |

Avertismente, nu criterii picate:

- masa concentrata pe o cifra la instanta asta: 0.999931 > 0.999. Avertisment, nu FAIL: decide criteriul 5, pe 10 limbi.

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:35:34. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.558182 |
| **valoare intoarsa de _once()** | **0.606960451846612** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 3.7 s |
| **timp per item** | **0.350 s** |
| timp sonda de dispersie, 10 limbi | 4.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0070  3=0.5582  4=0.4347  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:36:08. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 6.2 s |
| **timp per item** | **1.429 s** |
| timp sonda de dispersie, 10 limbi | 7.0 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:38:13. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.558182 |
| **valoare intoarsa de _once()** | **0.606960451846612** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 3.8 s |
| **timp per item** | **0.350 s** |
| timp sonda de dispersie, 10 limbi | 4.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0070  3=0.5582  4=0.4347  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:40:22. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.558182 |
| **valoare intoarsa de _once()** | **0.606960451846612** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 3.6 s |
| **timp per item** | **0.354 s** |
| timp sonda de dispersie, 10 limbi | 4.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0070  3=0.5582  4=0.4347  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## llama31-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:45:08. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Meta-Llama-3.1-8B-Instruct-4bit` |
| revision | `241a666dad6cb93c8ff213d39a7f34a36bf26db4` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | False |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999571e-01** |
| concentrare max(p) | 0.449005 |
| **valoare intoarsa de _once()** | **0.4129090216033571** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0742** pe 10/10 finite |
| timp incarcare | 4.6 s |
| **timp per item** | **0.445 s** |
| timp sonda de dispersie, 10 limbi | 7.1 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5342  0.3361  0.4260  0.4279  0.5336  0.5128  0.6097  0.4079  0.4838  0.4763

Distributia normalizata peste cifre: 1=0.0598  2=0.4490  3=0.2766  4=0.2088  5=0.0057

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## aya-expanse-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:50:27. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/aya-expanse-8b-4bit` |
| revision | `3a7cee37dd4ab4ed76642f61f6253da4748e63ba` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | False |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.864342e-01** |
| concentrare max(p) | 0.999931 |
| **valoare intoarsa de _once()** | **0.5000168108714715** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1163** pe 10/10 finite |
| timp incarcare | 6.8 s |
| **timp per item** | **0.388 s** |
| timp sonda de dispersie, 10 limbi | 6.4 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3753  0.2906  0.4486  0.4692  0.6340  0.4863  0.5045  0.3738  0.6904  0.3832

Distributia normalizata peste cifre: 1=0.0000  2=0.0000  3=0.9999  4=0.0001  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[24]` | '1' |
| 2 | `[25]` | '2' |
| 3 | `[26]` | '3' |
| 4 | `[27]` | '4' |
| 5 | `[28]` | '5' |

Avertismente, nu criterii picate:

- masa concentrata pe o cifra la instanta asta: 0.999931 > 0.999. Avertisment, nu FAIL: decide criteriul 5, pe 10 limbi.

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 11:55:36. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.8 s |
| **timp per item** | **0.845 s** |
| timp sonda de dispersie, 10 limbi | 8.2 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## qwen35-9b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 12:01:47. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3.5-9B-MLX-4bit` |
| revision | `938d8919941c6e7efd3c7150eff7fe9d12afa631` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.995802e-01** |
| concentrare max(p) | 0.443098 |
| **valoare intoarsa de _once()** | **0.5126282879559234** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0817** pe 10/10 finite |
| timp incarcare | 5.2 s |
| **timp per item** | **0.347 s** |
| timp sonda de dispersie, 10 limbi | 5.4 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5729  0.4776  0.4448  0.5296  0.6473  0.5656  0.6259  0.4149  0.6749  0.5380

Distributia normalizata peste cifre: 1=0.0118  2=0.2372  3=0.4431  4=0.3045  5=0.0034

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-8bit [prompt multi]: **PASS**

Rulat 2026-08-17 12:07:05. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-8bit` |
| revision | `48a0b75b1ae72503e21e1558d040bc227510ff06` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.499624 |
| **valoare intoarsa de _once()** | **0.6247188607852716** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0436** pe 10/10 finite |
| timp incarcare | 10.9 s |
| **timp per item** | **1.172 s** |
| timp sonda de dispersie, 10 limbi | 6.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5699  0.4988  0.5182  0.5566  0.6092  0.5090  0.5265  0.5024  0.6332  0.5393

Distributia normalizata peste cifre: 1=0.0000  2=0.0008  3=0.4996  4=0.4996  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen35-9b-8bit [prompt multi]: **PASS**

Rulat 2026-08-17 12:12:43. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3.5-9B-MLX-8bit` |
| revision | `84f7c2deea248d8df56240f88102def51c7ed5d6` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.998200e-01** |
| concentrare max(p) | 0.571648 |
| **valoare intoarsa de _once()** | **0.4864082348429244** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1045** pe 10/10 finite |
| timp incarcare | 15.3 s |
| **timp per item** | **1.390 s** |
| timp sonda de dispersie, 10 limbi | 6.3 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5942  0.4653  0.3704  0.5313  0.6390  0.5893  0.5996  0.4102  0.7389  0.5672

Distributia normalizata peste cifre: 1=0.0026  2=0.2383  3=0.5716  4=0.1856  5=0.0018

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 12:37:30. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.558182 |
| **valoare intoarsa de _once()** | **0.606960451846612** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 3.6 s |
| **timp per item** | **0.477 s** |
| timp sonda de dispersie, 10 limbi | 4.7 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0070  3=0.5582  4=0.4347  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 12:51:29. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.558182 |
| **valoare intoarsa de _once()** | **0.606960451846612** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 4.2 s |
| **timp per item** | **0.468 s** |
| timp sonda de dispersie, 10 limbi | 4.9 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0070  3=0.5582  4=0.4347  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 13:19:08. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.558182 |
| **valoare intoarsa de _once()** | **0.606960451846612** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 5.0 s |
| **timp per item** | **0.560 s** |
| timp sonda de dispersie, 10 limbi | 5.0 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0070  3=0.5582  4=0.4347  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 14:06:56. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.558182 |
| **valoare intoarsa de _once()** | **0.606960451846612** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 5.5 s |
| **timp per item** | **0.703 s** |
| timp sonda de dispersie, 10 limbi | 5.2 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0070  3=0.5582  4=0.4347  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 14:11:06. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 22.8 s |
| **timp per item** | **1.104 s** |
| timp sonda de dispersie, 10 limbi | 8.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 20:47:58. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 7.5 s |
| **timp per item** | **1.094 s** |
| timp sonda de dispersie, 10 limbi | 7.6 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 21:20:59. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.725164 |
| **valoare intoarsa de _once()** | **0.5646828396475313** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 3.2 s |
| **timp per item** | **0.293 s** |
| timp sonda de dispersie, 10 limbi | 5.2 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0081  3=0.7252  4=0.2668  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-17 22:40:24. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999208e-01** |
| concentrare max(p) | 0.769603 |
| **valoare intoarsa de _once()** | **0.2987942922563753** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.7 s |
| **timp per item** | **0.700 s** |
| timp sonda de dispersie, 10 limbi | 7.7 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0492  2=0.7696  3=0.1180  4=0.0632  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## qwen35-9b-8bit [prompt multi]: **PASS**

Rulat 2026-08-18 00:23:08. Instanta trial: lang `fr`, tinta `préjugés`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3.5-9B-MLX-8bit` |
| revision | `84f7c2deea248d8df56240f88102def51c7ed5d6` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `French` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.998188e-01** |
| concentrare max(p) | 0.666703 |
| **valoare intoarsa de _once()** | **0.47466060629934204** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1045** pe 10/10 finite |
| timp incarcare | 5.5 s |
| **timp per item** | **0.565 s** |
| timp sonda de dispersie, 10 limbi | 5.5 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5942  0.4653  0.3704  0.5313  0.6390  0.5893  0.5996  0.4102  0.7389  0.5672

Distributia normalizata peste cifre: 1=0.0007  2=0.2164  3=0.6667  4=0.1159  5=0.0003

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen35-9b-8bit [prompt multi]: **PASS**

Rulat 2026-08-19 11:43:27. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3.5-9B-MLX-8bit` |
| revision | `84f7c2deea248d8df56240f88102def51c7ed5d6` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.997812e-01** |
| concentrare max(p) | 0.492737 |
| **valoare intoarsa de _once()** | **0.3809384637708717** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1045** pe 10/10 finite |
| timp incarcare | 7.0 s |
| **timp per item** | **0.996 s** |
| timp sonda de dispersie, 10 limbi | 4.9 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5942  0.4653  0.3704  0.5313  0.6390  0.5893  0.5996  0.4102  0.7389  0.5672

Distributia normalizata peste cifre: 1=0.0191  2=0.4927  3=0.4348  4=0.0519  5=0.0014

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-19 17:31:19. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 7.4 s |
| **timp per item** | **0.937 s** |
| timp sonda de dispersie, 10 limbi | 6.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-19 17:32:33. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.6 s |
| **timp per item** | **0.632 s** |
| timp sonda de dispersie, 10 limbi | 6.9 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-19 17:39:49. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999208e-01** |
| concentrare max(p) | 0.769603 |
| **valoare intoarsa de _once()** | **0.2987942922563753** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.6 s |
| **timp per item** | **0.597 s** |
| timp sonda de dispersie, 10 limbi | 7.2 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0492  2=0.7696  3=0.1180  4=0.0632  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 18:37:14. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 7.5 s |
| **timp per item** | **0.885 s** |
| timp sonda de dispersie, 10 limbi | 7.0 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 18:38:00. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999798e-01** |
| concentrare max(p) | 0.495735 |
| **valoare intoarsa de _once()** | **0.2790292338702731** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1829** pe 10/10 finite |
| timp incarcare | 5.7 s |
| **timp per item** | **0.763 s** |
| timp sonda de dispersie, 10 limbi | 7.1 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3608  0.1987  0.1987  0.2862  0.5962  0.2801  0.3387  0.1527  0.7688  0.2811

Distributia normalizata peste cifre: 1=0.0000  2=0.0005  3=0.4957  4=0.4957  5=0.0080

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 18:39:15. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999855e-01** |
| concentrare max(p) | 0.562110 |
| **valoare intoarsa de _once()** | **0.3594890378966036** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1949** pe 10/10 finite |
| timp incarcare | 5.5 s |
| **timp per item** | **0.835 s** |
| timp sonda de dispersie, 10 limbi | 6.9 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5001  0.2784  0.2392  0.3742  0.6949  0.3768  0.4536  0.1326  0.8131  0.3677

Distributia normalizata peste cifre: 1=0.0000  2=0.5621  3=0.4378  4=0.0001  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 0 | `[236771]` | '0' |
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 18:39:52. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999855e-01** |
| concentrare max(p) | 0.562110 |
| **valoare intoarsa de _once()** | **0.3594890378966036** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1949** pe 10/10 finite |
| timp incarcare | 5.5 s |
| **timp per item** | **0.740 s** |
| timp sonda de dispersie, 10 limbi | 6.9 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5001  0.2784  0.2392  0.3742  0.6949  0.3768  0.4536  0.1326  0.8131  0.3677

Distributia normalizata peste cifre: 1=0.0000  2=0.5621  3=0.4378  4=0.0001  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 0 | `[236771]` | '0' |
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 18:45:55. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 10 cifre** | **9.999798e-01** |
| concentrare max(p) | 0.495735 |
| **valoare intoarsa de _once()** | **0.2790292338702731** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1829** pe 10/10 finite |
| timp incarcare | 5.7 s |
| **timp per item** | **0.662 s** |
| timp sonda de dispersie, 10 limbi | 8.2 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3608  0.1987  0.1987  0.2862  0.5962  0.2801  0.3387  0.1527  0.7688  0.2811

Distributia normalizata peste cifre: 1=0.0000  2=0.0005  3=0.4957  4=0.4957  5=0.0080

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 0 | `[236771]` | '0' |
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |
| 6 | `[236825]` | '6' |
| 7 | `[236832]` | '7' |
| 8 | `[236828]` | '8' |
| 9 | `[236819]` | '9' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 19:37:15. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999208e-01** |
| concentrare max(p) | 0.769603 |
| **valoare intoarsa de _once()** | **0.2987942922563753** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.6 s |
| **timp per item** | **0.677 s** |
| timp sonda de dispersie, 10 limbi | 6.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0492  2=0.7696  3=0.1180  4=0.0632  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 21:15:02. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.6 s |
| **timp per item** | **0.643 s** |
| timp sonda de dispersie, 10 limbi | 7.3 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **FAIL**

Rulat 2026-08-21 21:17:00. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | 'Rating' -> [12127] |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **7.547340e-07** |
| concentrare max(p) | 0.483034 |
| **valoare intoarsa de _once()** | **0.23314628159513362** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1973** pe 10/10 finite |
| timp incarcare | 5.4 s |
| **timp per item** | **0.614 s** |
| timp sonda de dispersie, 10 limbi | 7.0 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.4363  0.1948  0.2384  0.3224  0.6887  0.3920  0.5466  0.1334  0.7730  0.4376

Distributia normalizata peste cifre: 1=0.3534  2=0.4830  3=0.0577  4=0.0894  5=0.0165

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

Criterii picate:

- 4. masa bruta degenerata: 7.547e-07 < 0.001

## gemma4-12b-4bit [prompt multi]: **FAIL**

Rulat 2026-08-21 21:17:14. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | 'Answer' -> [7925] |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **6.166364e-07** |
| concentrare max(p) | 0.676428 |
| **valoare intoarsa de _once()** | **0.2601542236290816** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1754** pe 10/10 finite |
| timp incarcare | 4.8 s |
| **timp per item** | **0.550 s** |
| timp sonda de dispersie, 10 limbi | 6.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.4542  0.3026  0.4737  0.4027  0.6961  0.4383  0.5720  0.1893  0.8379  0.4693

Distributia normalizata peste cifre: 1=0.6764  2=0.0460  3=0.0091  4=0.0974  5=0.1710

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

Criterii picate:

- 4. masa bruta degenerata: 6.166e-07 < 0.001

## gemma4-12b-4bit [prompt multi]: **FAIL**

Rulat 2026-08-21 21:17:27. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | 'Difficulty' -> [98641] |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **5.677573e-07** |
| concentrare max(p) | 0.783420 |
| **valoare intoarsa de _once()** | **0.2325219149056892** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2200** pe 10/10 finite |
| timp incarcare | 4.9 s |
| **timp per item** | **0.523 s** |
| timp sonda de dispersie, 10 limbi | 6.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.4930  0.1910  0.1878  0.2939  0.7302  0.3809  0.5370  0.0795  0.7727  0.4898

Distributia normalizata peste cifre: 1=0.1642  2=0.7834  3=0.0119  4=0.0390  5=0.0015

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

Criterii picate:

- 4. masa bruta degenerata: 5.678e-07 < 0.001

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 21:19:21. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | 'Rating: ' -> [12127, 236787, 236743] |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999881e-01** |
| concentrare max(p) | 0.952466 |
| **valoare intoarsa de _once()** | **0.24400883848461935** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2177** pe 10/10 finite |
| timp incarcare | 4.7 s |
| **timp per item** | **0.572 s** |
| timp sonda de dispersie, 10 limbi | 7.0 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.4131  0.2243  0.1010  0.2491  0.6514  0.2569  0.3605  0.0038  0.7536  0.3766

Distributia normalizata peste cifre: 1=0.0369  2=0.9525  3=0.0082  4=0.0024  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 21:24:24. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | 'Answer: ' -> [7925, 236787, 236743] |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999909e-01** |
| concentrare max(p) | 0.962708 |
| **valoare intoarsa de _once()** | **0.24295594647041008** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2178** pe 10/10 finite |
| timp incarcare | 5.5 s |
| **timp per item** | **0.556 s** |
| timp sonda de dispersie, 10 limbi | 7.3 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.4028  0.2055  0.0814  0.2410  0.6274  0.2478  0.3603  0.0033  0.7533  0.3704

Distributia normalizata peste cifre: 1=0.0329  2=0.9627  3=0.0039  4=0.0004  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-21 21:29:55. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | 'Difficulty: ' -> [98641, 236787, 236743] |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999749e-01** |
| concentrare max(p) | 0.950021 |
| **valoare intoarsa de _once()** | **0.2420838528842787** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2157** pe 10/10 finite |
| timp incarcare | 5.4 s |
| **timp per item** | **0.590 s** |
| timp sonda de dispersie, 10 limbi | 8.9 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.4206  0.2338  0.1359  0.2496  0.6589  0.2597  0.3503  0.0050  0.7594  0.3809

Distributia normalizata peste cifre: 1=0.0417  2=0.9500  3=0.0064  4=0.0018  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-22 13:55:16. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999208e-01** |
| concentrare max(p) | 0.769603 |
| **valoare intoarsa de _once()** | **0.2987942922563753** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 6.0 s |
| **timp per item** | **1.015 s** |
| timp sonda de dispersie, 10 limbi | 6.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0492  2=0.7696  3=0.1180  4=0.0632  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-22 18:30:05. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 6.2 s |
| **timp per item** | **0.972 s** |
| timp sonda de dispersie, 10 limbi | 6.9 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-22 18:30:38. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.3 s |
| **timp per item** | **0.652 s** |
| timp sonda de dispersie, 10 limbi | 6.9 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-22 19:26:22. Instanta trial: lang `ca`, tinta `successius `.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999781e-01** |
| concentrare max(p) | 0.988855 |
| **valoare intoarsa de _once()** | **0.24729895522692757** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.7 s |
| **timp per item** | **0.975 s** |
| timp sonda de dispersie, 10 limbi | 7.0 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0110  2=0.9889  3=0.0001  4=0.0000  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-22 19:45:56. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999208e-01** |
| concentrare max(p) | 0.769603 |
| **valoare intoarsa de _once()** | **0.2987942922563753** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.6 s |
| **timp per item** | **0.666 s** |
| timp sonda de dispersie, 10 limbi | 6.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0492  2=0.7696  3=0.1180  4=0.0632  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-23 18:34:00. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.725164 |
| **valoare intoarsa de _once()** | **0.5646828396475313** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 3.8 s |
| **timp per item** | **0.275 s** |
| timp sonda de dispersie, 10 limbi | 4.7 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0081  3=0.7252  4=0.2668  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen3-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-23 18:34:25. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-4bit` |
| revision | `545dc4251c05440727734bcd94334791f6ab0192` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.725164 |
| **valoare intoarsa de _once()** | **0.5646828396475313** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0474** pe 10/10 finite |
| timp incarcare | 2.5 s |
| **timp per item** | **0.275 s** |
| timp sonda de dispersie, 10 limbi | 4.7 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5608  0.4995  0.5084  0.5390  0.5843  0.5068  0.5154  0.5080  0.6588  0.5165

Distributia normalizata peste cifre: 1=0.0000  2=0.0081  3=0.7252  4=0.2668  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## llama31-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-23 18:35:13. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Meta-Llama-3.1-8B-Instruct-4bit` |
| revision | `241a666dad6cb93c8ff213d39a7f34a36bf26db4` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | False |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999816e-01** |
| concentrare max(p) | 0.575915 |
| **valoare intoarsa de _once()** | **0.37451152801696885** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0742** pe 10/10 finite |
| timp incarcare | 3.7 s |
| **timp per item** | **0.333 s** |
| timp sonda de dispersie, 10 limbi | 5.1 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5342  0.3361  0.4260  0.4279  0.5336  0.5128  0.6097  0.4079  0.4838  0.4763

Distributia normalizata peste cifre: 1=0.0156  2=0.5759  3=0.3035  4=0.1049  5=0.0001

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## aya-expanse-8b-4bit [prompt multi]: **PASS**

Rulat 2026-08-23 18:54:20. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/aya-expanse-8b-4bit` |
| revision | `3a7cee37dd4ab4ed76642f61f6253da4748e63ba` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | False |
| enable_thinking a avut efect | None |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.838661e-01** |
| concentrare max(p) | 0.999799 |
| **valoare intoarsa de _once()** | **0.5000499249679219** |
| **dispersia lui B pe 10 limbi (sd)** | **0.1163** pe 10/10 finite |
| timp incarcare | 4.1 s |
| **timp per item** | **0.270 s** |
| timp sonda de dispersie, 10 limbi | 5.0 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3753  0.2906  0.4486  0.4692  0.6340  0.4863  0.5045  0.3738  0.6904  0.3832

Distributia normalizata peste cifre: 1=0.0000  2=0.0000  3=0.9998  4=0.0002  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[24]` | '1' |
| 2 | `[25]` | '2' |
| 3 | `[26]` | '3' |
| 4 | `[27]` | '4' |
| 5 | `[28]` | '5' |

Avertismente, nu criterii picate:

- masa concentrata pe o cifra la instanta asta: 0.999799 > 0.999. Avertisment, nu FAIL: decide criteriul 5, pe 10 limbi.

## qwen3-8b-8bit [prompt multi]: **PASS**

Rulat 2026-08-23 19:13:57. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3-8B-8bit` |
| revision | `48a0b75b1ae72503e21e1558d040bc227510ff06` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **1.000000e+00** |
| concentrare max(p) | 0.678639 |
| **valoare intoarsa de _once()** | **0.579943124629061** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0436** pe 10/10 finite |
| timp incarcare | 4.9 s |
| **timp per item** | **0.475 s** |
| timp sonda de dispersie, 10 limbi | 6.1 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5699  0.4988  0.5182  0.5566  0.6092  0.5090  0.5265  0.5024  0.6332  0.5393

Distributia normalizata peste cifre: 1=0.0000  2=0.0008  3=0.6786  4=0.3206  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## qwen35-9b-4bit [prompt multi]: **PASS**

Rulat 2026-08-23 19:34:04. Instanta trial: lang `ca`, tinta `coincidit`.

| camp | valoare |
|---|---|
| repo | `mlx-community/Qwen3.5-9B-MLX-4bit` |
| revision | `938d8919941c6e7efd3c7150eff7fe9d12afa631` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Catalan` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.993530e-01** |
| concentrare max(p) | 0.465764 |
| **valoare intoarsa de _once()** | **0.46043313724664514** |
| **dispersia lui B pe 10 limbi (sd)** | **0.0817** pe 10/10 finite |
| timp incarcare | 4.7 s |
| **timp per item** | **0.284 s** |
| timp sonda de dispersie, 10 limbi | 4.8 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.5729  0.4776  0.4448  0.5296  0.6473  0.5656  0.6259  0.4149  0.6749  0.5380

Distributia normalizata peste cifre: 1=0.0181  2=0.3201  3=0.4658  4=0.1942  5=0.0019

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[16]` | '1' |
| 2 | `[17]` | '2' |
| 3 | `[18]` | '3' |
| 4 | `[19]` | '4' |
| 5 | `[20]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-29 20:10:36. Instanta trial: lang `ro`, tinta `urmărire`.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Romanian` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999748e-01** |
| concentrare max(p) | 0.979930 |
| **valoare intoarsa de _once()** | **0.2530716583782241** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 7.5 s |
| **timp per item** | **1.097 s** |
| timp sonda de dispersie, 10 limbi | 7.3 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0040  2=0.9799  3=0.0158  4=0.0002  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-29 20:11:16. Instanta trial: lang `ro`, tinta `urmărire`.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Romanian` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999748e-01** |
| concentrare max(p) | 0.979930 |
| **valoare intoarsa de _once()** | **0.2530716583782241** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 5.8 s |
| **timp per item** | **0.735 s** |
| timp sonda de dispersie, 10 limbi | 7.2 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0040  2=0.9799  3=0.0158  4=0.0002  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |

## gemma4-12b-4bit [prompt multi]: **PASS**

Rulat 2026-08-29 20:59:17. Instanta trial: lang `ro`, tinta `urmărire`.

| camp | valoare |
|---|---|
| repo | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` |
| revision | `63912b888c04ba2c555f198685d10b05f54cf564` |
| backend | mlx |
| device | mlx |
| set de prompturi | multi, limba numita `Romanian` |
| prefix de citire | niciunul (ultima pozitie a sablonului) |
| enable_thinking declarat de sablon | True |
| enable_thinking a avut efect | True |
| bloc de gandire inchis | True |
| **masa bruta peste cele 5 cifre** | **9.999748e-01** |
| concentrare max(p) | 0.979930 |
| **valoare intoarsa de _once()** | **0.2530716583782241** |
| **dispersia lui B pe 10 limbi (sd)** | **0.2144** pe 10/10 finite |
| timp incarcare | 6.1 s |
| **timp per item** | **1.003 s** |
| timp sonda de dispersie, 10 limbi | 8.3 s |

B pe cate o instanta per limba, ordinea limbilor alfabetica: 0.3921  0.2093  0.1571  0.2515  0.6871  0.2508  0.3894  0.0336  0.7556  0.3049

Distributia normalizata peste cifre: 1=0.0040  2=0.9799  3=0.0158  4=0.0002  5=0.0000

Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):

| cifra | id-uri | decodate |
|---|---|---|
| 1 | `[236770]` | '1' |
| 2 | `[236778]` | '2' |
| 3 | `[236800]` | '3' |
| 4 | `[236812]` | '4' |
| 5 | `[236810]` | '5' |
