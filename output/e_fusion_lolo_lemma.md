# Fuziunea A plus B, brat `lolo`

Generat 2026-08-18 10:24:42 de `fuse_ab.py --arm lolo`. Date brute: `output/fusion_lolo_lemma.csv`, predictii per instanta in `output/fusion_preds_lolo_lemma.csv`.

Ponderea w e aleasa leave-one-language-out pe TRIAL, apoi aplicata pe TEST. Pentru limba L, w maximizeaza r mediu peste celelalte 9 limbi de trial. Nu vede nici limba L, nici testul. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.30 | +0.4470 | +0.4829 | **+0.5270** | [+0.4624, +0.5857] | +0.0800 | [+0.0203, +0.1423] | +0.0441 | [+0.0189, +0.0686] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.25 | +0.6551 | +0.6544 | **+0.7085** | [+0.6683, +0.7464] | +0.0534 | [+0.0140, +0.0960] | +0.0541 | [+0.0409, +0.0678] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.25 | +0.8147 | +0.8377 | **+0.8627** | [+0.8331, +0.8884] | +0.0481 | [+0.0237, +0.0750] | +0.0250 | [+0.0167, +0.0346] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.25 | +0.6686 | +0.7432 | **+0.7542** | [+0.7160, +0.7894] | +0.0855 | [+0.0561, +0.1157] | +0.0110 | [+0.0019, +0.0205] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.10 | +0.4091 | +0.5190 | **+0.5228** | [+0.4571, +0.5846] | +0.1137 | [+0.0589, +0.1676] | +0.0038 | [-0.0015, +0.0097] |
| fr | `qwen35-9b-8bit` | 566 | 191 | 0.30 | +0.5305 | +0.5440 | **+0.5793** | [+0.5253, +0.6334] | +0.0488 | [+0.0046, +0.0967] | +0.0353 | [+0.0153, +0.0557] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.25 | +0.6336 | +0.6106 | **+0.6469** | [+0.6013, +0.6930] | +0.0133 | [-0.0216, +0.0487] | +0.0363 | [+0.0241, +0.0488] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.30 | +0.4890 | +0.7676 | **+0.7773** | [+0.7338, +0.8128] | +0.2883 | [+0.2388, +0.3437] | +0.0096 | [-0.0069, +0.0255] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.25 | +0.7705 | +0.8222 | **+0.8377** | [+0.8044, +0.8651] | +0.0673 | [+0.0409, +0.0940] | +0.0155 | [+0.0071, +0.0242] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.20 | +0.2119 | +0.3407 | **+0.3480** | [+0.2962, +0.3994] | +0.1361 | [+0.0771, +0.1963] | +0.0073 | [-0.0063, +0.0214] |
| **medie** | | | | 0.25 | +0.5630 | +0.6322 | **+0.6564** | | +0.0935 | | +0.0242 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5630 |
| semnalul B singur, `lolo` | 0.6322 |
| **fuziunea A plus B, w ales LOLO** | **0.6564** |

Fata de cel mai bun reper publicat, 0.6571: **-0.0007**. Nu trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.30 | +0.5601 | +0.6796 | 0.1195 |
| de | 0.25 | +0.5084 | +0.6597 | 0.1513 |
| en | 0.25 | +0.5148 | +0.6780 | 0.1632 |
| es | 0.25 | +0.5082 | +0.6777 | 0.1695 |
| fil | 0.10 | +0.5295 | +0.7111 | 0.1816 |
| fr | 0.30 | +0.5629 | +0.6926 | 0.1297 |
| it | 0.25 | +0.5220 | +0.6763 | 0.1543 |
| ja | 0.30 | +0.5541 | +0.6740 | 0.1199 |
| pt | 0.25 | +0.5059 | +0.6628 | 0.1569 |
| si | 0.20 | +0.5913 | +0.7706 | 0.1793 |
