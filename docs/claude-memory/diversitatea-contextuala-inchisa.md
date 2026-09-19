---
name: diversitatea-contextuala-inchisa
description: "24 aug 2026 - diversitatea contextuala construita pentru toate 10 limbile din Wikipedia: inlocuirea lui zipf pierde -0.0242 pe A, adaugarea da +0.0014; pe fuziune -0.0062 si -0.00065. Inchisa pe sursa asta."
metadata:
  type: project
---

Rulat **24 august 2026**. Cod nou: `build_ctx_div.py`, `mlsp_common.load_ctx_div` si `ctx_div_safe`,
`solution_bert.lexical(ctxdiv=...)`, `finetune_xlmr --ctx-div {plus,inloc}`. Raport:
`output/e_ctx_div_fuziune.md` si `output/e_ctx_div.md`.

## Ce s-a construit, si costa 4.5 GB pe disc

In cate DOCUMENTE distincte apare cuvantul, nu de cate ori. Diferenta de cod fata de
`build_freq_tail.numara` e **un `set()`**. Sursa: `wikimedia/wikipedia` 20231101, **un shard per
limba** pentru cele opt mari (140-185k articole fiecare) si dump-ul intreg pentru si (23k) si tl (45k),
in `data/wiki_ctx/`. Tabelele in `data/ctx_div/`. Normalizata ca rata, aceeasi scara ca `zipf`.

Acoperirea pe tintele de test, forma exacta, fara backoff: **si 87.5% (fata de 0% la wordfreq)**,
fil 82.6% (fata de 73.3%), ja **55.3%** (japoneza nu se separa prin spatii, deci tokenizatorul pe clase
de caractere nu nimereste granitele; acelasi defect ca la wordfreq fara MeCab), restul 90.8-99.0%.

## Rezultatul

    brat A, xlmr    zipf (referinta)          0.5778
                    inloc (CD in loc de zipf) 0.5535   -0.0242
                    plus  (CD pe langa zipf)  0.5792   +0.0014

    fuziune fata de M3K = 0.690001
                    inloc                     -0.0062
                    plus                      -0.00065,  zero limbi stricate

**`inloc` pierde pe noua limbi din zece si castiga pe una: sinhaleza, +0.0279 pe A**, singura unde
`zipf` nu exista deloc.

**Rezultatul lui Adelman, Brown si Quesada (2006) nu se transfera**, dar comparatia e CONFUNDATA si se
declara: `wordfreq` agrega subtitrari, web, stiri si Wikipedia peste un corpus mult mai mare, iar
diversitatea noastra vine dintr-un singur shard de Wikipedia. S-a masurat "corpus mic fata de corpus
mare", nu "diversitate fata de frecventa".

Controlul de reproducere trece: fara `--ctx-div`, `e1_frozen_preds_lemma_fert_inloc.csv` iese bit cu
bit, `shasum 30272f99eb1a024d5dc424cd4bb748ed6dc881f7`.

## De ce nu se reia

Chiar reparata, ar intra prin bratul A, unde transmisia masurata e **0.137**, deci ar trebui sa urce A
cu **+0.033** ca fuziunea sa treaca bara. Cea mai mare parghie de encoder masurata vreodata e +0.027.

Si mai important, pe sinhaleza directia e gresita din principiu: vezi
[[sinhaleza-decorelarea-e-capitalul]].

## Capcana de proces, platita de doua ori azi

Un `python - <<PY` cu mai multe `assert` care crapa la ultimul **nu scrie fisierul**, deci patch-urile
dinainte se pierd in tacere si urmatoarea rulare esueaza cu o eroare fara legatura
(`TypeError: unexpected keyword argument`). Se verifica intotdeauna cu `grep` ca patch-ul chiar e in
fisier, nu ca scriptul a tiparit "ok".
