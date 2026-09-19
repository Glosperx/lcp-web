---
name: dropout-frecventa-inchis
description: "23 aug 2026 - dropout pe coloana de frecventa in antrenare: mecanismul se CONFIRMA pe A (exact si, fil, ja urca) dar nu trece in fuziune in niciuna din trei variante; selectia LOLO nimereste 0 din 9"
metadata: 
  node_type: memory
  type: project
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-23T20:59:05.051Z
---

Rulat **23 august 2026** noaptea, dupa adoptarea lui M3K. Cod: `finetune_xlmr._freq_drop` plus
`--freq-drop`. Raport: `output/e_freq_drop.md`. **Parghia e INCHISA.**

## Ce era ideea

Ablatia `--no-freq` (p = 1) costa -0.0051 pe fuziune si strica patru limbi, DAR urca filipineza cu
+0.0225 si bratul A al sinhalezei cu +0.0243. Deci cele doua capete sunt masurate si au semne opuse,
si intre ele exista un interior. Anularea coloanei pe o fractiune `p` din randurile de ANTRENARE, cu
blocurile prezise neatinse.

Controlul de reproducere trece: la `p = 0`, `e1_frozen_preds_lemma_fert_inloc.csv` iese **bit cu bit**,
`shasum 30272f99eb1a024d5dc424cd4bb748ed6dc881f7`.

## Mecanismul se confirma pe bratul A, mai precis decat s-a prezis

La `p = 0.15`, pe `xlmr`, **exact trei limbi urca, si numai ele**:

    ja  +0.0357     wordfreq cere MeCab, care lipseste: valorile exista dar nu sunt de incredere
    si  +0.0229     wordfreq nu serveste limba, 600/600 tinte cu zipf 0
    fil +0.0187     152/570 tinte cu zipf 0, de sapte ori mai mult decat urmatoarea limba

Celelalte sapte pierd, intre -0.0045 (en) si -0.0314 (it). Media pe A: -0.0054. `si` si `fil` erau
prezise; `ja` n-a fost, si e a treia limba cu coloana stricata, din al treilea motiv posibil.

## Si totusi nu trece, in niciuna din trei variante

    varianta                       delta pe fuziune   limbi stricate (CI exclude zero)
    p = 0.15 global                -0.0002            de, it
    p = 0.30 global                -0.0015            -
    p = 0.50 global                -0.0033            -
    p ales LOLO peste 4 candidati  -0.0034            -
    dropout NUMAI pe {si,fil,ja}   +0.000456          en, fr

## Doua rezultate metodologice, si sunt mai tari decat cifra

**1. Selectia LOLO a nimerit alegerea buna pe 0 limbi din 9.** Nu aproape de zero: exact zero, si
sistematic pe dos. A ales dropout tocmai pentru limbile care pierd din el si l-a evitat tocmai pentru
filipineza, care castiga cel mai mult. Motivul: **ce face dropout-ul potrivit pentru limba L e o
proprietate A LUI L**, ca propria ei coloana e stricata, si celelalte noua n-au cum s-o stie. Criteriul
nu e doar plat, e **orientat gresit**. E cea mai curata instanta a regulii din
[[criteriu-plat-mediaza-nu-alege]]; recordul anterior era 0 din 10 la selectia de encoder, dar acolo
criteriul era plat, nu inversat.

**2. Regula tintita strica doua limbi care n-au fost atinse deloc.** Cu dropout numai pe {si, fil, ja},
`en` si `fr` pierd cu interval care exclude zero **desi predictiile lor sunt identice bit cu bit**. La
**8 limbi din 10 s-a mutat `w_src` sau `w`**, fiindca criteriul lor se calculeaza pe celelalte noua,
care includ acum cele trei modificate. A treia instanta a patologiei din
[[ponderea-per-item-inchisa]], si cea mai clara.

## Ce ramane utilizabil

Observatia despre coada, a treia oara si acum cu **trei limbi si trei mecanisme distincte** prin care
aceeasi coloana e stricata: **absenta** (si), **gauri** (fil), **nesiguranta de segmentare** (ja). Si
cifra care le leaga: scapand partial de frecventa, exact acele trei urca pe bratul A si numai ele.
E o propozitie pentru paper, nu o parghie pentru cifra. Vezi [[filipineza-mecanismul-frecventei]] si
[[wordfreq-substitutie-tacuta-de-limba]].

Sinhaleza a ilustrat inca o data decuplarea A-fuziune: +0.0229 pe A, -0.0055 pe fuziune.
