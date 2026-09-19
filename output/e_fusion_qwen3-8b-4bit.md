# Fuziunea A plus B, brat `qwen3-8b-4bit`

Generat 2026-08-18 00:59:39 de `fuse_ab.py --arm qwen3-8b-4bit`. Date brute: `output/fusion_qwen3-8b-4bit.csv`, predictii per instanta in `output/fusion_preds_qwen3-8b-4bit.csv`.

Ponderea w e aleasa leave-one-language-out pe TRIAL, apoi aplicata pe TEST. Pentru limba L, w maximizeaza r mediu peste celelalte 9 limbi de trial. Nu vede nici limba L, nici testul. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `qwen3-8b-4bit` | 445 | 150 | 0.45 | +0.4281 | +0.2543 | **+0.3927** | [+0.3129, +0.4680] | -0.0354 | [-0.0854, +0.0143] | +0.1383 | [+0.0925, +0.1806] |
| de | `qwen3-8b-4bit` | 570 | 193 | 0.45 | +0.6314 | +0.3420 | **+0.5532** | [+0.4921, +0.6100] | -0.0782 | [-0.1161, -0.0375] | +0.2112 | [+0.1748, +0.2487] |
| en | `qwen3-8b-4bit` | 570 | 190 | 0.45 | +0.8197 | +0.3882 | **+0.7039** | [+0.6592, +0.7477] | -0.1158 | [-0.1534, -0.0732] | +0.3157 | [+0.2589, +0.3790] |
| es | `qwen3-8b-4bit` | 593 | 208 | 0.40 | +0.6341 | +0.3799 | **+0.5604** | [+0.5100, +0.6131] | -0.0737 | [-0.1186, -0.0305] | +0.1805 | [+0.1498, +0.2138] |
| fil | `qwen3-8b-4bit` | 568 | 553 | 0.40 | +0.4047 | +0.4910 | **+0.5350** | [+0.4623, +0.6019] | +0.1303 | [+0.0664, +0.1883] | +0.0440 | [+0.0116, +0.0789] |
| fr | `qwen3-8b-4bit` | 566 | 191 | 0.45 | +0.5153 | +0.4011 | **+0.5141** | [+0.4538, +0.5693] | -0.0012 | [-0.0420, +0.0425] | +0.1130 | [+0.0786, +0.1527] |
| it | `qwen3-8b-4bit` | 562 | 192 | 0.40 | +0.6136 | +0.3997 | **+0.5733** | [+0.5132, +0.6281] | -0.0403 | [-0.0964, +0.0123] | +0.1736 | [+0.1322, +0.2221] |
| ja | `qwen3-8b-4bit` | 570 | 190 | 0.45 | +0.4880 | +0.4553 | **+0.5914** | [+0.5248, +0.6454] | +0.1034 | [+0.0468, +0.1625] | +0.1361 | [+0.0850, +0.1849] |
| pt | `qwen3-8b-4bit` | 562 | 557 | 0.40 | +0.7663 | +0.4878 | **+0.6734** | [+0.6284, +0.7158] | -0.0928 | [-0.1287, -0.0561] | +0.1857 | [+0.1582, +0.2162] |
| si | `qwen3-8b-4bit` | 600 | 578 | 0.50 | +0.2216 | +0.1405 | **+0.2222** | [+0.1531, +0.2899] | +0.0006 | [-0.0447, +0.0458] | +0.0817 | [+0.0400, +0.1267] |
| **medie** | | | | 0.43 | +0.5523 | +0.3740 | **+0.5320** | | -0.0203 | | +0.1580 | |

Fuziunea bate A pe 3 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 6 limbi fata de A si pe 10 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5523 |
| semnalul B singur, `qwen3-8b-4bit` | 0.3740 |
| **fuziunea A plus B, w ales LOLO** | **0.5320** |

Fata de cel mai bun reper publicat, 0.6571: **-0.1251**. Nu trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.45 | +0.5508 | +0.6792 | 0.1284 |
| de | 0.45 | +0.4911 | +0.6304 | 0.1393 |
| en | 0.45 | +0.5010 | +0.6359 | 0.1349 |
| es | 0.40 | +0.4939 | +0.6496 | 0.1557 |
| fil | 0.40 | +0.5141 | +0.6526 | 0.1385 |
| fr | 0.45 | +0.5464 | +0.6704 | 0.1240 |
| it | 0.40 | +0.5039 | +0.6479 | 0.1440 |
| ja | 0.45 | +0.5398 | +0.6561 | 0.1163 |
| pt | 0.40 | +0.4903 | +0.6426 | 0.1523 |
| si | 0.50 | +0.5709 | +0.6872 | 0.1163 |
