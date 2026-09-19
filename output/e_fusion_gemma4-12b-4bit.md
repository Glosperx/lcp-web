# Fuziunea A plus B, brat `gemma4-12b-4bit`

Generat 2026-08-18 00:59:50 de `fuse_ab.py --arm gemma4-12b-4bit`. Date brute: `output/fusion_gemma4-12b-4bit.csv`, predictii per instanta in `output/fusion_preds_gemma4-12b-4bit.csv`.

Ponderea w e aleasa leave-one-language-out pe TRIAL, apoi aplicata pe TEST. Pentru limba L, w maximizeaza r mediu peste celelalte 9 limbi de trial. Nu vede nici limba L, nici testul. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.20 | +0.4281 | +0.4829 | **+0.5121** | [+0.4448, +0.5748] | +0.0840 | [+0.0139, +0.1556] | +0.0292 | [+0.0127, +0.0457] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.15 | +0.6314 | +0.6544 | **+0.6861** | [+0.6438, +0.7259] | +0.0547 | [+0.0097, +0.1027] | +0.0317 | [+0.0237, +0.0399] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.15 | +0.8197 | +0.8377 | **+0.8556** | [+0.8240, +0.8834] | +0.0359 | [+0.0095, +0.0640] | +0.0179 | [+0.0130, +0.0238] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.15 | +0.6341 | +0.7432 | **+0.7481** | [+0.7099, +0.7839] | +0.1140 | [+0.0775, +0.1515] | +0.0049 | [-0.0006, +0.0107] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.10 | +0.4047 | +0.5190 | **+0.5228** | [+0.4576, +0.5847] | +0.1181 | [+0.0626, +0.1720] | +0.0039 | [-0.0017, +0.0097] |
| fr | `gemma4-12b-4bit` | 566 | 191 | 0.20 | +0.5153 | +0.6457 | **+0.6510** | [+0.5958, +0.7008] | +0.1356 | [+0.0901, +0.1837] | +0.0052 | [-0.0049, +0.0159] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.15 | +0.6136 | +0.6106 | **+0.6299** | [+0.5836, +0.6766] | +0.0163 | [-0.0234, +0.0558] | +0.0193 | [+0.0127, +0.0263] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.20 | +0.4880 | +0.7676 | **+0.7853** | [+0.7431, +0.8199] | +0.2973 | [+0.2420, +0.3562] | +0.0176 | [+0.0071, +0.0281] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.15 | +0.7663 | +0.8222 | **+0.8330** | [+0.7990, +0.8613] | +0.0668 | [+0.0393, +0.0940] | +0.0108 | [+0.0059, +0.0158] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.20 | +0.2216 | +0.3407 | **+0.3495** | [+0.2982, +0.4012] | +0.1278 | [+0.0683, +0.1874] | +0.0088 | [-0.0049, +0.0225] |
| **medie** | | | | 0.16 | +0.5523 | +0.6424 | **+0.6573** | | +0.1050 | | +0.0149 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 6 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5523 |
| semnalul B singur, `gemma4-12b-4bit` | 0.6424 |
| **fuziunea A plus B, w ales LOLO** | **0.6573** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0002**. Trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.20 | +0.5508 | +0.7032 | 0.1524 |
| de | 0.15 | +0.4911 | +0.6846 | 0.1935 |
| en | 0.15 | +0.5010 | +0.7031 | 0.2021 |
| es | 0.15 | +0.4939 | +0.7038 | 0.2099 |
| fil | 0.10 | +0.5141 | +0.7101 | 0.1960 |
| fr | 0.20 | +0.5464 | +0.7206 | 0.1742 |
| it | 0.15 | +0.5039 | +0.6996 | 0.1957 |
| ja | 0.20 | +0.5398 | +0.6958 | 0.1560 |
| pt | 0.15 | +0.4903 | +0.6867 | 0.1964 |
| si | 0.20 | +0.5847 | +0.7704 | 0.1857 |
