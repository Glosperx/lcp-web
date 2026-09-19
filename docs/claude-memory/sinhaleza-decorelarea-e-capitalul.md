---
name: sinhaleza-decorelarea-e-capitalul
description: "24 aug 2026 - sinhaleza are rho(A,B)=0.387, cea mai mica din 10; orice trasatura de FRECVENTA urca rho cu +0.04..+0.12 si strica fuziunea desi urca bratul A; explica trei esecuri cu un mecanism"
metadata: 
  node_type: memory
  type: project
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-24T09:03:38.680Z
---

Masurat **24 august 2026**, in `output/e_ctx_div_fuziune.md` §3. Explica de ce sinhaleza a rezistat la
trei interventii independente care toate ii urcasera bratul A.

## Faptul

`rho(A, B)` pe sinhaleza e **0.3872**, cand media pe cele zece limbi e **0.687**. E cea mai mica din
tot setul. De asta fuziunea ei castiga **+0.1184** peste bratul A, cel mai mult din tabel: A si B
gresesc acolo diferit, si aia e tot capitalul ei.

## Cele trei interventii, si de ce doar una castiga

    interventie      d pe bratul A   d pe rho(A,B)   d pe fuziunea lui si
    first (pooling)     +0.0541         +0.032            +0.0177
    freq-drop           +0.0233         +0.118            -0.0062
    ctx-div plus        +0.0066         +0.037            -0.0023

Frontiera aplicata IN INTERIORUL limbii reproduce fiecare cifra cu eroare sub **5e-5**, deci nu e o
explicatie, e o identitate:

    r_fuz = (w*r_A + (1-w)*r_B) / sqrt(w^2 + (1-w)^2 + 2*w*(1-w)*rho),  w = 0.35, r_B = 0.3979

## Mecanismul

**Semnalul B, nota unui LLM, codifica deja cunoastere de tip frecventa.** Cand ii dai lui A un semnal
de frecventa pe care nu-l avea, A incepe sa **duplice** B in loc sa-l completeze. Pe sinhaleza, unde
tot avantajul fuziunii vine din decorelare, duplicarea costa mai mult decat aduce calitatea.

`first` castiga fiindca e o schimbare de **reprezentare**, nu de frecventa: urca calitatea mult si
corelatia putin.

**How to apply, si e regula practica cea mai utila iesita din coada:** pe sinhaleza **nu se cauta o
trasatura de frecventa mai buna**. Frecventa e chiar directia in care A si B se suprapun. Se cauta ceva
ce un LLM nu poate citi din propozitie. Si orice propunere pentru coada trebuie sa vina cu `d pe rho`,
nu doar cu `d pe r_A`.

Asta reformuleaza si intrebarea din [[prioritate-contributie-si-drumul-la-07]]: drumul la 0.700 trece
prin sinhaleza, dar nu prin resurse lexicale pentru ea, ci prin ceva ortogonal pe LLM.

Vezi [[frontiera-e-identitate-nu-aproximare]], [[dropout-frecventa-inchis]],
[[filipineza-mecanismul-frecventei]].
