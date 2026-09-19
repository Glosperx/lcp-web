# Fuziunea A plus B, brat `lolo`

Generat 2026-08-18 01:00:01 de `fuse_ab.py --arm lolo`. Date brute: `output/fusion_lolo.csv`, predictii per instanta in `output/fusion_preds_lolo.csv`.

Ponderea w e aleasa leave-one-language-out pe TRIAL, apoi aplicata pe TEST. Pentru limba L, w maximizeaza r mediu peste celelalte 9 limbi de trial. Nu vede nici limba L, nici testul. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.25 | +0.4281 | +0.4829 | **+0.5171** | [+0.4495, +0.5785] | +0.0890 | [+0.0234, +0.1562] | +0.0341 | [+0.0132, +0.0553] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.20 | +0.6314 | +0.6544 | **+0.6948** | [+0.6533, +0.7342] | +0.0634 | [+0.0207, +0.1090] | +0.0404 | [+0.0295, +0.0512] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.20 | +0.8197 | +0.8377 | **+0.8602** | [+0.8296, +0.8871] | +0.0405 | [+0.0155, +0.0672] | +0.0225 | [+0.0160, +0.0302] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.20 | +0.6341 | +0.7432 | **+0.7482** | [+0.7100, +0.7838] | +0.1141 | [+0.0794, +0.1502] | +0.0050 | [-0.0024, +0.0127] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.10 | +0.4047 | +0.5190 | **+0.5228** | [+0.4576, +0.5847] | +0.1181 | [+0.0626, +0.1720] | +0.0039 | [-0.0017, +0.0097] |
| fr | `qwen35-9b-8bit` | 566 | 191 | 0.25 | +0.5153 | +0.5440 | **+0.5715** | [+0.5169, +0.6270] | +0.0561 | [+0.0078, +0.1055] | +0.0274 | [+0.0114, +0.0441] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.25 | +0.6136 | +0.6106 | **+0.6398** | [+0.5939, +0.6865] | +0.0262 | [-0.0087, +0.0620] | +0.0292 | [+0.0178, +0.0411] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.30 | +0.4880 | +0.7676 | **+0.7814** | [+0.7387, +0.8161] | +0.2935 | [+0.2429, +0.3487] | +0.0138 | [-0.0026, +0.0297] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.25 | +0.7663 | +0.8222 | **+0.8367** | [+0.8031, +0.8641] | +0.0705 | [+0.0457, +0.0954] | +0.0145 | [+0.0064, +0.0228] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.20 | +0.2216 | +0.3407 | **+0.3495** | [+0.2982, +0.4012] | +0.1278 | [+0.0683, +0.1874] | +0.0088 | [-0.0049, +0.0225] |
| **medie** | | | | 0.22 | +0.5523 | +0.6322 | **+0.6522** | | +0.0999 | | +0.0200 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 6 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5523 |
| semnalul B singur, `lolo` | 0.6322 |
| **fuziunea A plus B, w ales LOLO** | **0.6522** |

Fata de cel mai bun reper publicat, 0.6571: **-0.0049**. Nu trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.25 | +0.5508 | +0.6771 | 0.1263 |
| de | 0.20 | +0.4911 | +0.6566 | 0.1655 |
| en | 0.20 | +0.5010 | +0.6754 | 0.1744 |
| es | 0.20 | +0.4939 | +0.6756 | 0.1817 |
| fil | 0.10 | +0.5141 | +0.7101 | 0.1960 |
| fr | 0.25 | +0.5464 | +0.6876 | 0.1412 |
| it | 0.25 | +0.5039 | +0.6728 | 0.1689 |
| ja | 0.30 | +0.5398 | +0.6705 | 0.1307 |
| pt | 0.25 | +0.4903 | +0.6596 | 0.1693 |
| si | 0.20 | +0.5847 | +0.7704 | 0.1857 |
