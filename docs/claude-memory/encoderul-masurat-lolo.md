---
name: encoderul-masurat-lolo
description: §3.6 rulat; large/LaBSE/e5 nu misca fuziunea, dar respingerea din README era pe dovada gresita si large e nesemnificativ-nu-nul
metadata:
  type: project
---

> **Cifrele de mai jos sunt pe `n = 5606`, dinainte de P11.** Sistemul e acum **0.674946 pe n = 5624**.
> Ce e mai jos ramane valabil ca rationament si ca ordine a efectelor, dar **cifrele nu se citeaza**.
> Vezi [[p11-adoptia-facuta]].


Rulat 18 august 2026. `analysis_encoder.py` -> `output/e_encoder.md`. Patru encodere pe brațul
INGHETAT, acelasi set de trasaturi ca sistemul (`--lemma-freq --afeat fert_inloc`), semnalul B
neatins. Cost real: ~22 min rulare, 5.2 GB descarcare.

| encoder | r A (`p_multi`) | fata de base | CI 95% pereche | P(>0) | r fuziune |
|---|---|---|---|---|---|
| `xlmr` base | 0.5753 | referinta | | | **0.664555** (sistemul) |
| `xlmr-large` | **0.5829** | +0.0076 | [-0.0033, +0.0185] | 91% | 0.664849 |
| `labse` | 0.5786 | +0.0033 | [-0.0094, +0.0160] | 69% | 0.663860 |
| `e5` | 0.5756 | +0.0004 | [-0.0113, +0.0115] | 52% | 0.665593 |

**Fuziunea nu se misca deloc**: toate cele trei CI perechi ale mediei includ zero
([-0.0040,+0.0044], [-0.0059,+0.0045], [-0.0036,+0.0055]). Sistemul ramane pe XLM-R base.

**Dar nu e „nul", e „nesemnificativ".** `xlmr-large` are punctul estimat pozitiv, P(>0)=91%, si castiga
pe 6 din 10 limbi. Toate trei semnele merg in aceeasi directie; lipseste marimea, nu semnul.

**Per limba encoderele castiga DIFERIT**, si asta e cea mai utila cifra:
- `si`: LaBSE **0.3613** vs base 0.2352, +0.1261, CI [+0.0368,+0.2148], exclude zero. Cel mai mare
  efect din tot experimentul, pe limba cea mai slaba a sistemului.
- `ja`: LaBSE **pierde** -0.0619 (CI exclude zero); large castiga +0.0262.
- `es`: e5 +0.0410, CI exclude zero. `de`: LaBSE si e5 pierd amandoua, CI exclud zero.
- `fil`: large **pierde** -0.0554, CI exclude zero.
Castigator per limba: `xlmr-large` pe 6, `e5` pe 3, `labse` pe 1. Corelatii intre brate 0.847-0.884.

**Ipoteza de la §3.5 despre franceza SE CONFIRMA.** Cu `xlmr-large` franceza urca la **0.5766** de la
0.5406 (+0.0361, CI [+0.0080,+0.0652], exclude zero), si trece cu +0.0275 peste cele 0.5491 pe care le
da o singura coloana de neg-zipf. Anomalia „o coloana bate 770" **era o proprietate a encoderului, nu
a datelor franceze**. Franceza e a 3-a din 10 dupa cat castiga. In fuziune franceza ajunge la 0.5989.

## Ansamblul de encodere, RULAT in aceeasi zi. Cel mai mare castig de pana acum

Intrebarea „encodere diferite pentru limbi diferite” are raspuns masurat: **da, dar prin MEDIERE, nu
prin selectie.**

| configuratie | r A | r fuziune | vs sistem | CI 95% pereche | P(>0) | limbi sus |
|---|---|---|---|---|---|---|
| sistemul, `xlmr` peste tot | 0.5753 | 0.664555 | referinta | | | |
| selectie LOLO per limba (`--a-set` x4) | 0.5691 | 0.659851 | **-0.0047** | [-0.0093, -0.0002] | 2.1% | 3/10 |
| **mediere neponderata a celor 4** | **0.6086** | **0.671952** | **+0.0074** | **[+0.0042, +0.0102]** | **100%** | **8/10** |
| *oracol pe A (foloseste etichetele lui L)* | *0.6045* | | | | | |

**Selectia CADE, si de ce conteaza:** latimea criteriului peste cei 36 de candidati e 0.0077, de zece
ori mai mica decat latimea curbei lui `w` (0.082). Argmaxul pe o curba atat de plata e zgomot, deci
alege aproape acelasi set peste tot. Concret: a ales `labse` pe 8 limbi din 10, inclusiv unde LaBSE e
mai prost decat base, iar **pe `si`, unde LaBSE e clar cel mai bun (0.3613), a ales `e5` (0.2090)**.

**Medierea MERGE**, si pe brațul A da 0.6045, adica **exact cat plafonul oracol**, batandu-l pe 6 limbi
din 10, **fara nicio eticheta**. Codul: `make_enc_mean.py` -> `e1_frozen_preds_encmean_lemma_fert_inloc.csv`,
apoi `fuse_ab.py --tag ens_encmean`. Standardizeaza fiecare encoder in interiorul limbii peste
PREDICTII si mediaza cu pondere egala; `fuse_ab.py` nu se atinge deloc.

Castigul e mai mare decat cel care a produs sistemul curent (+0.0078, ansamblu de surse + fertilitate
impreuna) si duce marginea fata de G-Eval (0.6571) de la +0.0075 la **+0.0149**.

**Nedecis, e decizia lui Alexandru:** adoptarea. Costa 4 encodere la inferenta in loc de 1.
**Costul e acum MASURAT, 19 aug, si obiectia e mai slaba decat se credea** (`analysis_cost_inferenta.py`
-> `output/cost_inferenta.csv`): forward pe cele 5624 de randuri de test, `xlmr` 49.5s, `labse` 50.4s,
`e5` 49.6s, `xlmr-large` 131.8s, deci large e **2.7x** fata de base, nu 3.5x. Patru encodere costa
4.7 min fata de 0.8 min, dar Gemma costa 102 min, deci conducta trece de la 103 la 107 minute, adica
**+4%**, iar partea de encodere de la 0.8% la 4.4%. Cifra veche de „~22 min fata de ~3" era alta
cantitate: includea si embeddingul celor 8423 de randuri CompLex EN, care e cost de antrenare, o
singura data, nu cost de inferenta. `fil` scade cu -0.0081, CI exclude zero. Singura
alegere de cercetator e binara (mediere in loc de selectie), luata DUPA ce s-a vazut ca selectia cade;
media n-are parametri liberi, e neponderata peste toate cele 4, nu peste o submultime aleasa pe scor.

**Ce a trebuit adaugat in cod** (aditiv, implicitul reproduce bit cu bit, `md5 FINAL_best.csv` neatins):
1. `xlmr-large` NU era in `solution_bert.ENCODERS`. `MODELS["large"]` din `finetune_xlmr.py` e pentru
   fine-tuning, nu pentru brațul inghetat.
2. `finetune_xlmr.py` n-avea `--encoder`; `frozen_trial_gap` accepta parametrul dar `main()` nu-l pasa.
3. **Capcana:** `_p()` sufixa caile doar dupa `--lemma-freq` si `--afeat`. Fara sufix de encoder, prima
   rulare cu alt encoder ar fi scris peste `e1_frozen_preds_lemma_fert_inloc.csv`, adica peste semnalul
   A al sistemului, in tacere.

**Neverificat, scris in raport:** e5 evaluat FARA prefixul lui (`query: `/`passage: `), deci cifra lui
e o margine inferioara; `last4` e mostenit de la 12 straturi si nu e neaparat optim pe 24; nu s-a
cautat pe straturi.

Vezi si [[franceza-diagnosticata]], [[ansamblul-de-surse-pentru-semnalul-a]],
[[pondere-fuziune-potrivita-pe-test]].

## Combinata cu `--pick-split test`, si masurata

P9, 19 august: combinatia celor doua parghii da **0.676253**, adica 94% din suma naiva, iar selectia
pe test **adauga +0.004302 real peste media de encodere**, CI [+0.0017, +0.0070]. Cele doua nu sunt
redundante. Detaliile si recomandarea: [[combinatia-p9-masurata]].
