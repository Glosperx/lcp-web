# Fixul de lema pe limbile MLSP. Cat aduce, si daca urmeaza morfologia

Generat de `analysis_lemma.py`. Date brute: `output/lemma_delta.csv`.

Cele doua brate difera printr-un singur lucru, frecventa formei fata de `max(forma, lema)`. Embedding, regresor, partitie si seminte identice.

Bootstrap **pereche** pe contexte, 2000 reesantionari, aceeasi reesantionare pe ambele brate. MSP e mediat peste 200 subesantioane de cate 4441 de tokeni per limba, numar comun ales ca minimul peste limbi.

## Rezultatul

| limba | n | ctx | MSP | tinte cu lema != forma | r fara lema | r cu lema | Δ | CI 95% |
|---|---|---|---|---|---|---|---|---|
| `es` | 593 | 208 | 1.290 | 57% | +0.6341 | +0.6686 | **+0.0345** | [+0.0197, +0.0506] |
| `fr` | 566 | 191 | 1.222 | 48% | +0.5153 | +0.5305 | +0.0152 | [-0.0034, +0.0331] |
| `it` | 562 | 192 | 1.218 | 54% | +0.6136 | +0.6336 | **+0.0200** | [+0.0030, +0.0382] |
| `pt` | 562 | 557 | 1.197 | 38% | +0.7663 | +0.7705 | +0.0042 | [-0.0073, +0.0164] |
| `ca` | 445 | 150 | 1.196 | 48% | +0.4281 | +0.4470 | +0.0189 | [-0.0072, +0.0451] |
| `de` | 570 | 193 | 1.168 | 48% | +0.6314 | +0.6551 | **+0.0237** | [+0.0026, +0.0441] |
| `en` | 570 | 190 | 1.140 | 38% | +0.8197 | +0.8147 | -0.0050 | [-0.0200, +0.0073] |
| `ja` | 570 | 190 | 1.093 | 67% | +0.4880 | +0.4890 | +0.0010 | [-0.0240, +0.0241] |
| `fil` | 568 | 553 | - | 0% | +0.4047 | +0.4091 | +0.0044 | [-0.0015, +0.0108] |
| `si` | 600 | 578 | - | 0% | +0.2216 | +0.2119 | -0.0098 | [-0.0288, +0.0092] |
| **medie** | | | | | **+0.5523** | **+0.5630** | **+0.0107** | |

Δ ingrosat = intervalul exclude zero.

## Teza morfologica

Pe cele 8 limbi unde fixul se poate aplica:

- Pearson intre MSP si Δ: **+0.782** (p = 0.022)
- Spearman: **+0.619** (p = 0.102)

La n = 8 nu se revendica semnificatie. Coeficientul se raporteaza cu punctele alaturi, iar cititorul vede singur cat de mult atarna fiecare limba.

## Limbile unde fixul nu se poate aplica

| limba | Δ masurat | motiv |
|---|---|---|
| `fil` | +0.0044 | stanza nu are lematizator pentru limba |
| `si` | -0.0098 | `wordfreq` nu serveste limba, deci `zipf_safe` intoarce indisponibil |

Δ **nu** e zero acolo, si nu trebuie sa fie. Coloana lor de frecventa e identica bit cu bit intre cele doua brate, verificat pe toate cele 1170 de randuri, deci fixul chiar nu li se aplica. Dar sub LOLO modelul care prezice limba L se antreneaza pe CELELALTE noua, ale caror trasaturi s-au schimbat. Ce se masoara la `fil` si `si` e deci efectul indirect, prin datele de antrenare, si el e informativ tocmai fiindca e curat de orice efect direct.

## Limitari

MSP e calculat pe propozitiile MLSP, 4441 de tokeni per limba, nu pe treebank-uri UD. Pe un corpus mic MSP subestimeaza, iar subestimarea nu e la fel de mare pentru toate limbile. Cifra e deci un indice ordinal pentru clasarea limbilor, nu o constanta tipologica citabila in afara lucrarii.

Lemele vin de la stanza, deci sunt prezise, nu gold. Pe romana, unde lemele erau gold de la shared task, fixul a adus cel mai mare castig unic al lucrarii; o parte din diferenta fata de limbile de aici poate veni din calitatea lemelor, nu din morfologie.
