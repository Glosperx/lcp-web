# E.1 - E.4. Bake-off pe cele 300 de instante de trial

Generat 2026-08-17 20:56:36 de `bakeoff_trial.py --aggregate`. Datele brute: `output/bakeoff_<model>.csv`, o linie per instanta.

Trial, niciodata test. Selectia modelului e leave-one-language-out (§5.1), pe semnalul B. Pentru C se raporteaza r cu semn, fara selectie: surprisal-ul e o statistica bruta, nu o nota, si intra in fuziune abia daca aduce ceva peste B.

## Acoperire si NaN

| model | repo | linii | NaN B | NaN C | s per item, medie | s per item, mediana |
|---|---|---|---|---|---|---|
| `qwen3-8b-4bit` | `mlx-community/Qwen3-8B-4bit` | 300 | 0 | 11 | 0.90 | 0.75 |
| `qwen3-8b-8bit` | `mlx-community/Qwen3-8B-8bit` | 300 | 0 | 11 | 1.03 | 0.89 |
| `qwen35-9b-4bit` | `mlx-community/Qwen3.5-9B-MLX-4bit` | 300 | 0 | 12 | 0.98 | 0.86 |
| `qwen35-9b-8bit` | `mlx-community/Qwen3.5-9B-MLX-8bit` | 300 | 0 | 12 | 1.09 | 0.92 |
| `gemma4-12b-4bit` | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` | 300 | 0 | 12 | 1.19 | 1.19 |
| `llama31-8b-4bit` | `mlx-community/Meta-Llama-3.1-8B-Instruct-4bit` | 300 | 0 | 11 | 1.00 | 0.87 |
| `aya-expanse-8b-4bit` | `mlx-community/aya-expanse-8b-4bit` | 300 | 0 | 10 | 0.97 | 0.77 |

NaN-urile nu se imputeaza aici. La B inseamna masa degenerata pe amandoua prompturile, la C inseamna tinta negasita ca subsir in context.

## r per limba

### Semnalul B, nota LLM

| model | ca | de | en | es | fil | fr | it | ja | pt | si | medie |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `qwen3-8b-4bit` | +0.367 | +0.795 | +0.748 | +0.528 | +0.481 | +0.406 | +0.573 | +0.576 | +0.615 | +0.561 | **+0.565** |
| `qwen3-8b-8bit` | +0.348 | +0.753 | +0.665 | +0.600 | +0.426 | +0.623 | +0.624 | +0.575 | +0.630 | +0.595 | **+0.584** |
| `qwen35-9b-4bit` | +0.672 | +0.728 | +0.653 | +0.704 | +0.589 | +0.401 | +0.727 | +0.793 | +0.802 | +0.153 | **+0.622** |
| `qwen35-9b-8bit` | +0.666 | +0.749 | +0.650 | +0.735 | +0.729 | +0.300 | +0.708 | +0.853 | +0.816 | +0.411 | **+0.662** |
| `gemma4-12b-4bit` | +0.743 | +0.753 | +0.737 | +0.709 | +0.642 | +0.609 | +0.770 | +0.834 | +0.893 | +0.170 | **+0.686** |
| `llama31-8b-4bit` | +0.442 | +0.778 | +0.545 | +0.577 | +0.498 | +0.612 | +0.540 | +0.575 | +0.637 | +0.270 | **+0.547** |
| `aya-expanse-8b-4bit` | +0.586 | +0.647 | +0.581 | +0.652 | +0.410 | +0.426 | +0.679 | +0.607 | +0.551 | +0.001 | **+0.514** |

### Semnalul C, surprisal (semnul se raporteaza ca atare)

| model | ca | de | en | es | fil | fr | it | ja | pt | si | medie |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `qwen3-8b-4bit` | -0.056 | +0.442 (n=23) | +0.120 | +0.442 (n=28) | +0.122 | -0.284 | -0.005 (n=29) | -0.197 (n=29) | -0.124 | +0.257 | **+0.072** |
| `qwen3-8b-8bit` | -0.037 | +0.387 (n=23) | +0.125 | +0.463 (n=28) | +0.041 | -0.283 | -0.007 (n=29) | -0.248 (n=29) | -0.184 | +0.248 | **+0.050** |
| `qwen35-9b-4bit` | -0.302 | +0.224 (n=23) | +0.079 | +0.215 (n=28) | +0.037 | -0.169 | +0.208 (n=29) | -0.356 (n=28) | -0.088 | -0.081 | **-0.023** |
| `qwen35-9b-8bit` | -0.217 | +0.198 (n=23) | +0.084 | +0.244 (n=28) | -0.002 | -0.198 | +0.207 (n=29) | -0.364 (n=28) | -0.165 | -0.107 | **-0.032** |
| `gemma4-12b-4bit` | -0.014 | -0.186 (n=23) | +0.130 | -0.350 (n=28) | +0.061 | +0.071 | -0.404 (n=29) | +0.069 (n=28) | -0.230 | +0.051 | **-0.080** |
| `llama31-8b-4bit` | -0.085 | +0.225 (n=23) | +0.083 | +0.423 (n=28) | -0.061 | -0.289 | +0.197 (n=29) | -0.159 (n=29) | -0.156 | +0.143 | **+0.032** |
| `aya-expanse-8b-4bit` | -0.224 | +0.025 (n=23) | +0.352 | +0.129 (n=28) | +0.039 | +0.020 | +0.028 (n=29) | -0.349 | -0.135 | +0.276 | **+0.016** |

## Selectia leave-one-language-out, §5.1, pe semnalul B

Pentru limba L, modelul e ales pe media lui r peste celelalte 9 limbi. Coloana `r pe L` e cifra raportabila: modelul nu a vazut niciodata trial-ul lui L la selectie.

| limba tinuta deoparte | model ales | media lui r pe celelalte 9 | r pe L |
|---|---|---|---|
| ca | `gemma4-12b-4bit` | +0.6797 | +0.7428 |
| de | `gemma4-12b-4bit` | +0.6786 | +0.7526 |
| en | `gemma4-12b-4bit` | +0.6804 | +0.7369 |
| es | `gemma4-12b-4bit` | +0.6834 | +0.7095 |
| fil | `gemma4-12b-4bit` | +0.6909 | +0.6423 |
| fr | `qwen35-9b-8bit` | +0.7019 | +0.2996 |
| it | `gemma4-12b-4bit` | +0.6767 | +0.7699 |
| ja | `gemma4-12b-4bit` | +0.6696 | +0.8336 |
| pt | `gemma4-12b-4bit` | +0.6630 | +0.8932 |
| si | `gemma4-12b-4bit` | +0.7433 | +0.1702 |

**r mediu sub selectie LOLO: +0.6551** pe 10 limbi.

**Modelele difera per limba: 2 castigatori distincti, ['gemma4-12b-4bit', 'qwen35-9b-8bit'].** Asta e in sine un rezultat si se raporteaza ca atare, nu se ascunde sub un singur model.

## §5.2. Cat costa alegerea bratului principal pe acoperire

`qwen3-8b-4bit` e bratul principal fiindca acoperirea lui de limbi e citabila, nu fiindca ar fi cel mai bun. Tabelul spune cat costa asta, in r.

Cifra care conteaza e coloana **fata de LOLO**: alternativa reala e modelul ales tot leave-one-language-out, adica fara sa fi vazut trial-ul limbii L. Coloana **oracol** e cel mai bun model PE L, ales folosind chiar trial-ul lui L, deci e exact tuningul pe care §5.1 il interzice. Nu e o alternativa disponibila, ci o margine superioara.

| limba | r al bratului principal | model ales LOLO | r al lui | fata de LOLO | oracol pe L | r al lui | fata de oracol |
|---|---|---|---|---|---|---|---|
| ca | +0.3666 | `gemma4-12b-4bit` | +0.7428 | -0.3762 | `gemma4-12b-4bit` | +0.7428 | -0.3762 |
| de | +0.7949 | `gemma4-12b-4bit` | +0.7526 | +0.0424 | `qwen3-8b-4bit` | +0.7949 | +0.0000 |
| en | +0.7477 | `gemma4-12b-4bit` | +0.7369 | +0.0108 | `qwen3-8b-4bit` | +0.7477 | +0.0000 |
| es | +0.5282 | `gemma4-12b-4bit` | +0.7095 | -0.1813 | `qwen35-9b-8bit` | +0.7352 | -0.2070 |
| fil | +0.4812 | `gemma4-12b-4bit` | +0.6423 | -0.1610 | `qwen35-9b-8bit` | +0.7295 | -0.2483 |
| fr | +0.4060 | `qwen35-9b-8bit` | +0.2996 | +0.1064 | `qwen3-8b-8bit` | +0.6229 | -0.2169 |
| it | +0.5733 | `gemma4-12b-4bit` | +0.7699 | -0.1966 | `gemma4-12b-4bit` | +0.7699 | -0.1966 |
| ja | +0.5758 | `gemma4-12b-4bit` | +0.8336 | -0.2577 | `qwen35-9b-8bit` | +0.8527 | -0.2769 |
| pt | +0.6151 | `gemma4-12b-4bit` | +0.8932 | -0.2782 | `gemma4-12b-4bit` | +0.8932 | -0.2782 |
| si | +0.5610 | `gemma4-12b-4bit` | +0.1702 | +0.3907 | `qwen3-8b-8bit` | +0.5946 | -0.0337 |

**Costul alegerii pe acoperire, fata de alternativa LOLO: -0.0901 r**, sd intre limbi 0.2162, interval -0.3762 pana la +0.3907. Fata de oracol, care nu e disponibil: -0.1834 r.

Prag de zgomot: la n = 30 per limba, intervalul de 95% pentru un r de 0.60 e [0.31, 0.79] prin transformarea Fisher. Diferentele per limba mai mici decat atat nu se pot distinge pe trial. Media peste cele 10 limbi e mai stabila decat orice celula individuala, dar limbile nu sunt esantioane independente din aceeasi marime.

## E.3. Timp per item, masurat pe toate instantele

Din coloana `sec`, care acopera `rate()` plus `surprisal()` pentru o instanta. Nu e extrapolat dintr-o singura instanta, ceea ce era rezerva ramasa de la Bloc D.

| model | medie | mediana | min | max | total |
|---|---|---|---|---|---|
| `qwen3-8b-4bit` | 0.90 s | 0.75 s | 0.43 s | 3.09 s | 4.5 min |
| `qwen3-8b-8bit` | 1.03 s | 0.89 s | 0.54 s | 4.19 s | 5.2 min |
| `qwen35-9b-4bit` | 0.98 s | 0.86 s | 0.49 s | 5.24 s | 4.9 min |
| `qwen35-9b-8bit` | 1.09 s | 0.92 s | 0.53 s | 10.21 s | 5.5 min |
| `gemma4-12b-4bit` | 1.19 s | 1.19 s | 0.72 s | 3.10 s | 5.9 min |
| `llama31-8b-4bit` | 1.00 s | 0.87 s | 0.52 s | 3.03 s | 5.0 min |
| `aya-expanse-8b-4bit` | 0.97 s | 0.77 s | 0.45 s | 3.23 s | 4.8 min |

Per limba, `qwen3-8b-4bit`: ca 0.67s, de 0.89s, en 0.68s, es 0.79s, fil 0.65s, fr 0.82s, it 0.79s, ja 0.67s, pt 1.06s, si 1.97s. Diferentele vin din lungimea contextului.

## E.4. Controlul de cuantizare


### `qwen3-8b-4bit` fata de `qwen3-8b-8bit`, semnalul B

| limba | 4 biti | 8 biti | diferenta |
|---|---|---|---|
| ca | +0.3666 | +0.3484 | -0.0182 |
| de | +0.7949 | +0.7527 | -0.0422 |
| en | +0.7477 | +0.6651 | -0.0826 |
| es | +0.5282 | +0.6001 | +0.0720 |
| fil | +0.4812 | +0.4262 | -0.0551 |
| fr | +0.4060 | +0.6229 | +0.2169 |
| it | +0.5733 | +0.6236 | +0.0503 |
| ja | +0.5758 | +0.5751 | -0.0007 |
| pt | +0.6151 | +0.6298 | +0.0147 |
| si | +0.5610 | +0.5946 | +0.0337 |

**Castigul mediu al lui 8 biti: +0.0189 r**, la un cost de timp de 1.15x.

### `qwen35-9b-4bit` fata de `qwen35-9b-8bit`, semnalul B

| limba | 4 biti | 8 biti | diferenta |
|---|---|---|---|
| ca | +0.6716 | +0.6662 | -0.0054 |
| de | +0.7285 | +0.7488 | +0.0203 |
| en | +0.6531 | +0.6498 | -0.0033 |
| es | +0.7036 | +0.7352 | +0.0316 |
| fil | +0.5889 | +0.7295 | +0.1406 |
| fr | +0.4015 | +0.2996 | -0.1019 |
| it | +0.7273 | +0.7084 | -0.0189 |
| ja | +0.7932 | +0.8527 | +0.0595 |
| pt | +0.8020 | +0.8155 | +0.0135 |
| si | +0.1527 | +0.4112 | +0.2585 |

**Castigul mediu al lui 8 biti: +0.0395 r**, la un cost de timp de 1.11x.

## Verdict

1. **Semnalul B merge pe toate cele 10 limbi si pe toate cele 7 modele.** r mediu per model intre +0.514 si +0.686, zero NaN pe B in 2100 de instante masurate.
2. **Cel mai bun pe media celor 10 limbi e `gemma4-12b-4bit`, cu r = +0.686.** Bratul principal `qwen3-8b-4bit` da +0.565.
3. **Selectia LOLO costa si ea.** r mediu sub selectie LOLO +0.6551, fata de +0.6860 pe care l-ar da `gemma4-12b-4bit` peste tot. Diferenta, -0.0310, e pretul protocolului, si se plateste pe 1 din 10 limbi, unde selectia pe celelalte 9 nu alege `gemma4-12b-4bit`.
4. **Semnalul C nu tine.** r mediu per model intre -0.080 si +0.072, cu semnul schimbandu-se intre limbi la fiecare model. Pe dovada asta C nu intra in fuziune.
5. **Limba cea mai grea pentru toate modelele e `si`.** Bratul principal `qwen3-8b-4bit` e cel mai bun model pe ['de', 'en'].
