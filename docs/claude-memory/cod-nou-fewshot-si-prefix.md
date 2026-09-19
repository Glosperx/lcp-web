---
name: cod-nou-fewshot-si-prefix
description: "Ce scripturi noi au aparut pe 21 aug 2026 pentru few-shot pe test si pentru pozitia de citire, plus controalele care le valideaza si capcana de prefix masurata pe Gemma."
metadata: 
  node_type: memory
  type: project
  originSessionId: c41c7657-b13d-4c6e-b16c-1f1864b8ecb1
  modified: 2026-08-21T18:22:29.438Z
---

Scrise **21 august 2026**, pentru [[fewshot-pe-test-masurat]] si [[pozitia-de-citire-masurata]].

## Ce face fiecare, si de ce exista separat

- `make_fs_runs.py` - scrie directoare de bake-off cu `B` din **una, doua sau trei** distributii.
  Exista separat de `make_bt_runs.py` fiindca acolo `B` e mereu media a DOUA distributii, `p1` si `p2`
  din acelasi fisier, si toata selectia (`analysis_dist.per_lang`, `b_build`, `_r_cube`) e scrisa pe
  cele doua nume. A generaliza `make_bt_runs` ar fi cerut atins fiecare loc prin care trece o cifra
  publicata.
- `make_fs_dist.py` - din `output/promptlab_test/<model>.csv` scoate un CSV de distributii cu UN
  slot de prompt, lipind `C` verbatim din `output/bakeoff_test/<model>.csv`.
- `analysis_fewshot.py` -> `output/e_fewshot.md`. Recalculeaza P(>0) **al mediei** o singura data,
  pentru toate configuratiile, exact ca sa nu se citeasca din greseala cealalta statistica din
  rapoartele lui `fuse_ab`.
- `analysis_citire.py` -> `output/e_citire.md`. Bratele sunt declarate in `BRATE`, la varf.

`prompt_lab.py` salveaza acum distributiile (`dist_cells_pad`, cu `repr(float(x))`) si are `--split`.
Trial scrie pe calea canonica, test in `output/promptlab_test/`: **subdirector, nu sufix in nume**,
fiindca `aggregate()` face glob pe `output/promptlab_*.csv` si un sufix ar fi intrat tacut in raportul
E.10 ca al unsprezecelea „model". Are si o garda de antet la append: fisierele vechi au sase coloane,
si randuri late sub antet ingust dau coloane deplasate fara nicio eroare.

`solution_bert.LLMRater` are `read_prefix=""`, iar `bakeoff_trial.py` are `--prefix`, care CERE `--out`.

## Controalele care le valideaza. Se reruleaza cand se atinge ceva

1. **`make_fs_runs` pe cele doua surse ale sistemului iese identic la OCTET** cu
   `output/bakeoff_test_Text/`, pe toate trei CSV-urile, iar fuziunea pe el da +0.6838 cu diferenta
   +0.0000 pe toate zece limbile. Asta e ce face credibila reimplementarea selectiei:
   `python make_fs_runs.py --dir bakeoff_test_CTRL --src output/dist/gemma4-12b-4bit_test.csv`
2. **Refactorul lui `prompt_lab` nu schimba nicio cifra**: 12/12 randuri de trial reproduc
   `output/promptlab_gemma4-12b-4bit.csv` la 8 zecimale, deci si promptul si cele 6 exemple sunt
   identice.
3. **`--prefix ""` reproduce fisierul canonic de trial**, si aici e o capcana de CONTROL, nu de cod:
   comparatia la octet trebuie sa EXCLUDA coloana `sec`, care e timp de ceas si nu se reproduce.
   Prima rulare a controlului a picat numai pe ea.
4. `analysis_citire.py` pe bratul fara prefix reproduce cifrele publicate din sondajul de scara:
   r(T=1) = +0.6860, T* = 8, r = +0.7067.

## Capcana de prefix, masurata

**Prefixul de citire trebuie sa se termine cu SPATIU.** Dupa `"Rating:"` Gemma pune **0.9999 pe un
token de spatiu simplu**, iar cifra vine abia dupa el, deci masa pe cele cinci cifre iese 5.5e-08 si
D.4 pica pe criteriul 4. Dupa `"Rating: "` masa e 0.99999. Motivul: `self.digit` are la Gemma cate un
singur id per cifra, cel FARA spatiu, fiindca `encode(" 1")` da doi tokeni si cel de spatiu nu se
decodeaza ca cifra. A largi harta ar schimba semnalul publicat; spatiul in prefix nu schimba nimic
altceva. **D.4 a prins-o din prima, pe toate trei prefixele**, deci nu s-a scris nicio cifra greasita.

## Ce a rams nefacut si e gratis

Cate un T per prompt in ansamblul de trei. Acum e o singura temperatura pentru toate trei, T=6, desi
few-shot-ul singur vrea T=4 si perechea zero-shot vrea T=12. `make_bt_runs.pick_temps` are deja grila
`per-prompt` pentru asta si nu s-a folosit.
