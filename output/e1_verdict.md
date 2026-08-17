# E1 inchis. Δ_frozen pe 10 limbi, plus criteriul §5.2 aplicat

Rulat pe 17 august 2026, `finetune_xlmr.py --frozenmulti`, MPS float32, XLM-R base last4.
Date brute: `output/e1_lolo_frozen.csv`. Timp total 157 secunde, din care 124 embedding.

Acoperire: EN 8422/8423, MLSP **5606/5624**. Cele 18 tinte pierdute nu se gasesc ca subsir in context:
it 8, pt 5, fr 3, fil 2. Coincide cu masuratoarea V9 (it 98.6%).

## Criteriul §5.2, aplicat inainte de a interpreta rezultatul

`σ_Δ` din §5.2 e imprastierea lui Δ **intre limbi**, aceeasi marime care pe cele 3 limbi vechi
(it/pt/es) dadea 0.0107.

| Marime | Valoare |
|---|---|
| **σ_Δ intre cele 10 limbi** | **0.0369** |
| σ_Δ in interiorul limbii (bootstrap pe contexte, medie) | 0.0142 |
| Δ mediu | −0.0045 |

Tabelul din §5.2 spune: peste 0.030 inseamna **„designul centrat pe Δ e mort. Nu se descarca niciun
LLM monolingv. Se pivoteaza integral pe ideea 10 plus ideea 11."**

**Verdictul se consemneaza ca atare, nu se renegociaza.** Consecinta operationala concreta: cvartetul
Δ_controlat din saptamana 3, adica RoLlama3.1, Swallow v0.3 si Gervásio, circa 80 GB, **nu se mai
descarca**.

Doua fapte care se raporteaza fara sa schimbe verdictul:

- Imprastierea vine aproape integral de la **japoneza**, Δ = −0.0896. Fara ea, σ_Δ = 0.0228, adica
  zona gri. Japoneza nu e insa un outlier de masurare: CI-ul ei exclude zero net, [−0.1430, −0.0422].
- Cele doua σ nu masoara acelasi lucru. Cel de 0.0142 e zgomotul de esantionare in interiorul unei
  limbi. Cel de 0.0369 e **heterogenitate reala intre limbi**, si exact el intra in puterea unui test
  pe Δ mediu, deci el e cel cerut de §5.2.

## Δ per limba

CI-ul exclude zero la 4 limbi din 10, si **in ambele directii**: pozitiv la ca, es, it, negativ la ja.

| limba | n | ctx | EN-only | EN+MLSP∖L | Δ | CI 95% | σ_Δ |
|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | 0.3932 | 0.4281 | **+0.0349** | [+0.0039, +0.0640] | 0.0153 |
| de | 570 | 193 | 0.6359 | 0.6314 | −0.0044 | [−0.0270, +0.0166] | 0.0111 |
| en | 570 | 190 | 0.8221 | 0.8197 | −0.0024 | [−0.0152, +0.0095] | 0.0063 |
| es | 593 | 208 | 0.5981 | 0.6341 | **+0.0360** | [+0.0170, +0.0558] | 0.0097 |
| fil | 568 | 553 | 0.4158 | 0.4047 | −0.0111 | [−0.0255, +0.0026] | 0.0072 |
| fr | 566 | 191 | 0.5145 | 0.5153 | +0.0008 | [−0.0238, +0.0251] | 0.0128 |
| it | 562 | 192 | 0.5850 | 0.6136 | **+0.0286** | [+0.0059, +0.0523] | 0.0121 |
| ja | 570 | 190 | 0.5776 | 0.4880 | **−0.0896** | [−0.1430, −0.0422] | 0.0255 |
| pt | 562 | 557 | 0.7748 | 0.7663 | −0.0085 | [−0.0233, +0.0063] | 0.0076 |
| si | 600 | 578 | 0.2507 | 0.2216 | −0.0290 | [−0.0980, +0.0343] | 0.0348 |

Structura e interpretabila: cele trei limbi unde adaugarea celorlalte limbi **ajuta** sunt toate
romanice, ca/es/it. Singura unde **strica**, si strica mult, e japoneza, singura limba din set cu alt
sistem de scriere si cu trasaturi de suprafata NaN. Sinhaleza, cealalta limba cu NaN, are acelasi semn
dar CI care include zero.

## r al nostru fata de reperele publicate

Coloana noastra e bratul EN+MLSP∖L, adica sistemul zero-label. Reperele sunt transcrise din V2.e
(Cristea si Nisioi, run 1) si Tabelul 13 al lui Nohejl et al. 2025.

| limba | **noi** | run 1 | diferenta | baseline frecventa | Archaeology | TMU-HIT | G-Eval, GPT-4o |
|---|---|---|---|---|---|---|---|
| ca | **0.4281** | 0.2960 | +0.1321 | 0.301 | 0.274 | 0.616 | 0.573 |
| de | **0.6314** | 0.5508 | +0.0806 | 0.591 | 0.551 | 0.718 | 0.711 |
| en | **0.8197** | — | | 0.748 | 0.790 | 0.820 | 0.827 |
| es | **0.6341** | 0.5274 | +0.1067 | 0.551 | 0.527 | 0.762 | 0.739 |
| fil | **0.4047** | 0.3620 | +0.0427 | 0.389 | 0.443 | 0.569 | 0.494 |
| fr | **0.5153** | 0.5335 | **−0.0182** | 0.517 | 0.533 | 0.625 | 0.764 |
| it | **0.6136** | 0.5341 | +0.0795 | 0.519 | 0.534 | 0.601 | 0.629 |
| ja | **0.4880** | 0.2803 | +0.2077 | 0.642 | 0.485 | 0.733 | 0.745 |
| pt | **0.7663** | 0.7143 | +0.0520 | 0.713 | 0.683 | 0.786 | 0.761 |
| si | **0.2216** | −0.0290 | +0.2506 | −0.196 | 0.044 | 0.308 | 0.328 |
| **medie** | **0.5523** | 0.4188 | | 0.4775 | 0.4864 | 0.6538 | 0.6571 |

- **8 din 9** fata de run 1, singurul rezultat publicat pe MLSP obtinut fara nicio eticheta in limba
  tinta. Pierdem doar franceza, cu 0.018.
- **8 din 10** fata de baseline-ul de frecventa si fata de Archaeology.
- **1 din 10** fata de TMU-HIT si fata de G-Eval. Media noastra e cu 0.105 sub G-Eval.

Cifrele de mai sus sunt **semnalul A singur**: embedding inghetat plus patru trasaturi lexicale. Fara
semnalul B, fara semnalul C, fara fixul de lema. Bara de 0.657 a lui G-Eval ramane cea reala pentru
Tabelul 1, cum avertiza V2.a-bis.

## Ce s-a schimbat in cod ca sa iasa cifrele

Cinci reparatii, toate din §2.5 pasii 0-4, plus rescrierea lui C.1 si C.2. Detaliile in
`~/.claude/plans/e-ti-pe-proiectul-din-breezy-flute.md`. Reproducerea bit-exacta a caii romanesti e
pastrata: garda de frecventa si NaN-urile intra prin `na_policy="mlsp"`, opt-in.
