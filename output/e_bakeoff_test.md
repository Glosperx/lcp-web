# Etapa 2. Semnalul B pe testul complet

Generat 2026-08-19 13:09:04 de `bakeoff_trial.py --aggregate --split test`. Datele brute: `output/bakeoff_test/<model>.csv`, o linie per instanta.

**Harta de mai jos e cea fixata pe trial**, si se aplica testului. Ea nu mai e insa harta sistemului: `fuse_ab.py --pick-split test` alege modelul limbii L pe randurile de TEST ale celorlalte noua limbi, exact ca `w` si ca antrenarea bratului A, deci fara nicio eticheta din L. Interdictia de la §5.1 priveste o selectie care ar folosi testul lui L, nu una leave-one-language-out pe test. Harta efectiv folosita se citeste din `output/e_fusion_lolo_adoptat.md`.

Intervalele vin din bootstrap pe contexte (§10.3), nu din transformarea Fisher: sapte limbi din zece au in medie 3 tinte per context, deci itemii nu sunt independenti.

## Acoperire si NaN

| model | repo | linii | NaN B | NaN C | s per item, medie | s per item, mediana |
|---|---|---|---|---|---|---|
| `qwen3-8b-4bit` | `mlx-community/Qwen3-8B-4bit` | 5624 | 0 | 28 | 0.84 | 0.75 |
| `qwen35-9b-8bit` | `mlx-community/Qwen3.5-9B-MLX-8bit` | 5624 | 0 | 38 | 0.87 | 0.79 |
| `gemma4-12b-4bit` | `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit` | 5624 | 0 | 31 | 1.09 | 1.10 |

NaN-urile nu se imputeaza aici. La B inseamna masa degenerata pe amandoua prompturile, la C inseamna tinta negasita ca subsir in context.

## r per limba

### Semnalul B, nota LLM

| model | ca | de | en | es | fil | fr | it | ja | pt | si | medie |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `qwen3-8b-4bit` | +0.254 | +0.342 | +0.388 | +0.380 | +0.489 | +0.401 | +0.405 | +0.455 | +0.487 | +0.141 | **+0.374** |
| `qwen35-9b-8bit` | +0.507 | +0.583 | +0.768 | +0.707 | +0.506 | +0.542 | +0.597 | +0.658 | +0.730 | +0.308 | **+0.591** |
| `gemma4-12b-4bit` | +0.483 | +0.654 | +0.838 | +0.743 | +0.517 | +0.642 | +0.613 | +0.768 | +0.821 | +0.341 | **+0.642** |

### Semnalul C, surprisal (semnul se raporteaza ca atare)

| model | ca | de | en | es | fil | fr | it | ja | pt | si | medie |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `qwen3-8b-4bit` | +0.132 | +0.265 | -0.055 | +0.073 | +0.045 (n=568) | +0.061 (n=566) | +0.162 (n=562) | -0.006 (n=560) | +0.081 (n=562) | +0.186 | **+0.094** |
| `qwen35-9b-8bit` | +0.023 | +0.126 | -0.048 | -0.043 | +0.036 (n=568) | -0.046 (n=566) | +0.002 (n=562) | -0.117 (n=550) | -0.077 (n=562) | +0.176 | **+0.003** |
| `gemma4-12b-4bit` | -0.039 | -0.118 | +0.043 | -0.002 | -0.136 (n=568) | -0.116 (n=566) | -0.113 (n=562) | -0.143 (n=557) | -0.023 (n=562) | -0.004 | **-0.065** |

## Sistemul selectat LOLO, cu harta fixata pe trial

Modelul per limba e cel ales pe trial-ul celorlalte 9 limbi, in `output/e_bakeoff.md`. Aici doar se aplica: coloana `r pe L, test` e cifra raportabila.

| limba | model ales pe trial | r pe L, trial | r pe L, test |
|---|---|---|---|
| ca | `gemma4-12b-4bit` | +0.7428 | +0.4829 |
| de | `gemma4-12b-4bit` | +0.7526 | +0.6544 |
| en | `gemma4-12b-4bit` | +0.7369 | +0.8377 |
| es | `gemma4-12b-4bit` | +0.7095 | +0.7432 |
| fil | `gemma4-12b-4bit` | +0.6423 | +0.5173 |
| fr | `qwen35-9b-8bit` | +0.2996 | +0.5420 |
| it | `gemma4-12b-4bit` | +0.7699 | +0.6127 |
| ja | `gemma4-12b-4bit` | +0.8336 | +0.7676 |
| pt | `gemma4-12b-4bit` | +0.8932 | +0.8213 |
| si | `gemma4-12b-4bit` | +0.1702 | +0.3407 |

**r mediu al sistemului selectat LOLO, pe test: +0.6320** pe 10 limbi din 10.

## §5.2. Cat costa alegerea bratului principal pe acoperire

`qwen3-8b-4bit` e bratul principal fiindca acoperirea lui de limbi e citabila, nu fiindca ar fi cel mai bun. Tabelul spune cat costa asta, in r.

Cifra care conteaza e coloana **fata de LOLO**: alternativa reala e modelul ales tot leave-one-language-out, adica fara sa fi vazut trial-ul limbii L. Coloana **oracol** e cel mai bun model PE L, ales folosind chiar scorul de test al lui L, deci e exact tuningul pe care §5.1 il interzice. Nu e o alternativa disponibila, ci o margine superioara.

| limba | r al bratului principal | model ales LOLO | r al lui | fata de LOLO | oracol pe L | r al lui | fata de oracol |
|---|---|---|---|---|---|---|---|
| ca | +0.2543 | `gemma4-12b-4bit` | +0.4829 | -0.2286 | `qwen35-9b-8bit` | +0.5073 | -0.2529 |
| de | +0.3420 | `gemma4-12b-4bit` | +0.6544 | -0.3124 | `gemma4-12b-4bit` | +0.6544 | -0.3124 |
| en | +0.3882 | `gemma4-12b-4bit` | +0.8377 | -0.4495 | `gemma4-12b-4bit` | +0.8377 | -0.4495 |
| es | +0.3799 | `gemma4-12b-4bit` | +0.7432 | -0.3632 | `gemma4-12b-4bit` | +0.7432 | -0.3632 |
| fil | +0.4889 | `gemma4-12b-4bit` | +0.5173 | -0.0283 | `gemma4-12b-4bit` | +0.5173 | -0.0283 |
| fr | +0.4008 | `qwen35-9b-8bit` | +0.5420 | -0.1411 | `gemma4-12b-4bit` | +0.6424 | -0.2416 |
| it | +0.4054 | `gemma4-12b-4bit` | +0.6127 | -0.2073 | `gemma4-12b-4bit` | +0.6127 | -0.2073 |
| ja | +0.4553 | `gemma4-12b-4bit` | +0.7676 | -0.3124 | `gemma4-12b-4bit` | +0.7676 | -0.3124 |
| pt | +0.4874 | `gemma4-12b-4bit` | +0.8213 | -0.3339 | `gemma4-12b-4bit` | +0.8213 | -0.3339 |
| si | +0.1405 | `gemma4-12b-4bit` | +0.3407 | -0.2002 | `gemma4-12b-4bit` | +0.3407 | -0.2002 |

**Costul alegerii pe acoperire, fata de alternativa LOLO: -0.2577 r**, sd intre limbi 0.1152, interval -0.4495 pana la -0.0283. Fata de oracol, care nu e disponibil: -0.2702 r.

## E.3. Timp per item, masurat pe toate instantele

Din coloana `sec`, care acopera `rate()` plus `surprisal()` pentru o instanta. Nu e extrapolat dintr-o singura instanta, ceea ce era rezerva ramasa de la Bloc D.

| model | medie | mediana | min | max | total |
|---|---|---|---|---|---|
| `qwen3-8b-4bit` | 0.84 s | 0.75 s | 0.41 s | 3.89 s | 78.7 min |
| `qwen35-9b-8bit` | 0.87 s | 0.79 s | 0.45 s | 6.21 s | 81.4 min |
| `gemma4-12b-4bit` | 1.09 s | 1.10 s | 0.69 s | 2.43 s | 102.3 min |

Per limba, `qwen3-8b-4bit`: ca 0.95s, de 0.90s, en 0.63s, es 0.75s, fil 0.66s, fr 0.80s, it 0.79s, ja 0.60s, pt 0.82s, si 1.50s. Diferentele vin din lungimea contextului.

## E.4. Controlul de cuantizare

- `qwen3-8b-4bit` fata de `qwen3-8b-8bit`: **in asteptare**, lipseste `qwen3-8b-8bit`. Nu se estimeaza.
- `qwen35-9b-4bit` fata de `qwen35-9b-8bit`: **in asteptare**, lipseste `qwen35-9b-4bit`. Nu se estimeaza.

Niciuna din cele doua perechi nu e completa, deci E.4 ramane deschis.

## Intervale prin bootstrap pe contexte, §10.3

2000 de reesantionari ale CONTEXTELOR, nu ale itemilor. Sapte limbi din zece au in medie 3 tinte per context, deci un bootstrap pe itemi ar da intervale prea inguste exact acolo. Contextul e recuperat pozitional din `load_mlsp("test")`, cu verificare rand cu rand pe limba, token si complexitate.

| model | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| `qwen3-8b-4bit` | +0.254<br>[+0.176, +0.334] | +0.342<br>[+0.270, +0.412] | +0.388<br>[+0.319, +0.459] | +0.380<br>[+0.314, +0.449] | +0.489<br>[+0.411, +0.557] | +0.401<br>[+0.331, +0.466] | +0.405<br>[+0.318, +0.481] | +0.455<br>[+0.363, +0.533] | +0.487<br>[+0.429, +0.543] | +0.141<br>[+0.068, +0.209] |
| `qwen35-9b-8bit` | +0.507<br>[+0.437, +0.570] | +0.583<br>[+0.532, +0.630] | +0.768<br>[+0.728, +0.806] | +0.707<br>[+0.673, +0.740] | +0.506<br>[+0.444, +0.563] | +0.542<br>[+0.483, +0.599] | +0.597<br>[+0.554, +0.642] | +0.658<br>[+0.607, +0.704] | +0.730<br>[+0.686, +0.769] | +0.308<br>[+0.245, +0.367] |
| `gemma4-12b-4bit` | +0.483<br>[+0.413, +0.550] | +0.654<br>[+0.610, +0.697] | +0.838<br>[+0.802, +0.869] | +0.743<br>[+0.703, +0.781] | +0.517<br>[+0.451, +0.581] | +0.642<br>[+0.585, +0.694] | +0.613<br>[+0.566, +0.661] | +0.768<br>[+0.724, +0.803] | +0.821<br>[+0.789, +0.852] | +0.341<br>[+0.288, +0.394] |

Contexte per limba: ca 150, de 193, en 190, es 208, fil 555, fr 191, it 192, ja 190, pt 562, si 578. Latimea intervalului urmeaza numarul de contexte, nu numarul de itemi, si de asta fil, pt si si, unde contextul e practic un item, nu castiga nimic din agregare.

## Verdict

1. **Sistemul selectat LOLO da r mediu +0.6320 pe test**, pe 10 limbi din 10, cu harta fixata pe trial.
2. **Bratul principal `qwen3-8b-4bit` da +0.3743** pe cele 10 limbi rulate.
3. **Reperele publicate, tot pe test:** baseline frecventa 0.478, Archaeology 0.487, TMU-HIT 0.654, G-Eval cu GPT-4o 0.657. Bratul inghetat E1 al nostru, semnalul A singur, da 0.552. Cifrele de mai sus sunt semnalul B singur, deci nici ele nu sunt sistemul final: fuziunea A plus B e in `output/e_fusion.md`.
4. **Semnalul C pe test:** r mediu per model intre -0.065 si +0.094. Verdictul de pe trial se confirma la scara mare.
5. **Limba cea mai grea ramane `si`.** Modelele cu acoperire completa pe test: ['gemma4-12b-4bit', 'qwen3-8b-4bit', 'qwen35-9b-8bit'].
