---
name: rolcp-a-11a-limba-lolo
description: "29 aug 2026 - Romania a intrat ca a 11-a limba in grila LOLO multilingva, cerut explicit de Sergiu; noua cifra 0.693718 (de la 0.690001), Romania singura da 0.7401"
metadata:
  node_type: memory
  type: project
  originSessionId: 61c4f607-25b4-4e50-9827-f13f53d75c5c
  modified: 2026-08-29T18:39:27.945Z
---

Continuarea lui [[update-paper-mesaj2-punctul7]]. Alexandru a intrebat "de curiozitate, nu merg puse
si datele in romana" -> a aflat ca coordonatorul (Sergiu) chiar a cerut asta, si ca lucrarea romaneasca
originala nu se mai publica separat (absorbita in cea multilingva), deci riscul de circularitate
dispare ca argument de recenzent. Decizia: Romania intra ca a 11-a limba, zero-label, in ACELASI
protocol LOLO ca celelalte 10 (niciodata etichetele ei proprii la selectia de model/pondere).

## Descoperirea centrala, in timpul implementarii

`finetune_xlmr.py:429` antreneaza Semnalul A pentru limba L pe `Xen + Xml[celelalte limbi]`, unde
"celelalte limbi" sunt randurile de TEST reale ale lor. Deci adaugarea Romaniei NU e o ablatie
aditiva: RETRANTREAZA semnalul A pentru toate celelalte 10 limbi, fiindca RoLCP intra acum in
bazinul lor de antrenare. Toate cifrele existente s-au recalculat, nu doar s-a adaugat un rand nou.

A doua descoperire, mai adanca: sistemul adoptat (0.690001) NU citeste semnalul B din
`output/bakeoff_test/`, ci din `output/bakeoff_test_M3K/`, un director construit de
`make_fs_runs.py` prin combinarea A TREIA prompt (marcat/target-word, din `prompt_lab.py`) cu cele
doua prompturi de baza, plus selectie LOLO de temperatura si partitie ("colaps"). Iar acel proces
citeste un fisier de referinta FIX pe 10 limbi, `analysis_dist.SYS_PREDS` =
`output/fusion_preds_lolo_adoptat.csv`. Semnalul A adoptat e si el o medie a 3 encodere
(xlm-roberta-base, LaBSE, multilingual-e5-base), produsa de `make_enc_mean.py`, nu un singur encoder.

## Ce s-a construit ca sa se reproduca exact metodologia, nu o aproximare

1. `mlsp_common.py`: `load_rolcp()` (join identic cu `score_rolcp.py`, validat 1587/1587), flag
   `include_ro=False` pe `load_mlsp()`, `lang_name("ro")` -> "Romanian" pentru calea multilingva
   (calea romaneasca veche, `lang=None`, ramane neatinsa).
2. `lemmatize_mlsp.py`: "ro" adaugat la `STANZA_LANGS`, relematizat cu stanza (nu lema gold primita),
   ca sa nu confunde teza morfologica cu un artefact de calitate a lemei.
3. `finetune_xlmr.py`: flag `--include-ro`, plus guard NaN pentru limbi fara split de trial (RoLCP
   n-are), altfel crapa la calculul de decalaj trial-test.
4. `bakeoff_trial.py`: `with_context`/`aggregate`/`measure` AUTO-DETECTEAZA "ro" din datele deja
   incarcate (fara flag nou de trecut prin `fuse_ab.py`).
5. Rulari reale: Gemma4-12b-4bit (mlx, M5) pe cele 1587 randuri RoLCP, doua prompturi de baza (raw
   r_B=0.6449) plus al treilea prompt marcat (separat, script propriu bazat pe `PromptLab.v_marcat`,
   818s). Trei rulari de embedding (xlmr, labse, e5) pentru semnalul A, cate ~5-7 minute fiecare.
6. Fisiere canonice pe 10 limbi EXTINSE in loc (cu backup inainte): `output/bakeoff_test/gemma4-12b-4bit.csv`,
   `output/dist/gemma4-12b-4bit_test.csv`, `output/dist/marcat_gemma4-12b-4bit_test.csv` -> acum au
   7211 randuri (5624+1587). Backup-urile: `output/*_10lang_backup.csv`.
7. Referinta noua pe 11 limbi: `output/fusion_preds_lolo_adoptat_ro11.csv` (monkeypatch pe
   `analysis_dist.SYS_PREDS`), director nou `output/bakeoff_test_M3K_ro11/` (paralel cu cel vechi,
   NEATINS), semnalul A pe 3 encodere cu Romania: `output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc_ro11.csv`.

**Verificat dupa: comanda ORIGINALA (`--b-dir output/bakeoff_test_M3K`, fara `_ro11`) reproduce
0.6900 bit-cu-bit, deci nimic din ce era publicat nu s-a stricat.**

## Rezultatul final

`output/e_fusion_lolo_adoptat_m3k_ro11.md`. Media pe 11 limbi: **0.693718** (de la 0.690001 pe 10).
Media pe doar cele 10 vechi, in noua rulare: 0.68908 (aproape neschimbata, +0.0037 vine aproape tot
din Romania). Romania singura: A=0.7292, B=0.6588 (T=6, partitia 1|23|45, ca majoritatea celorlalte),
**fuziune=0.7401** [0.7055, 0.7711] - peste media celor 11.

Miscari pe celelalte 10 (efectul antrenarii cu randurile romanesti in plus): ca +0.0009, de +0.0013,
en +0.0009, es +0.0000, fil -0.0029, fr -0.0064, it +0.0043, ja -0.0027, pt +0.0003, si -0.0048. Mici
si in ambele directii, nimic dramatic.

## Limitare de scris in paper

Romania NU e un test complet orb de generalizare ca celelalte 10: arhitectura insasi (encodere,
features, prompturi, alegerea LLM-ului) a fost dezvoltata si validata initial PE romana, in lucrarea
veche nepublicata. Fraza de Limitations e scrisa in planul de sesiune, nefolosita inca in text.

## Ce ramane de facut

Cifrele NU sunt inca in `Paper/Articol_Multilingv/paper_full.tex` - doar calculate si verificate.
Doar Gemma4 a fost rulat pe romana (nu tot bazinul de 7 modele): decizie deliberata, Gemma castiga
LOLO pe 10/10 limbi oricum. Nimic nu e comis in git. Vezi [[cifra-de-raportat-in-paper]] pentru cum
s-a citat 0.690001 pana acum.

**Why:** coordonatorul a cerut explicit includerea RoLCP; fara aceasta memorie, o sesiune viitoare ar
crede ca 0.690001 e inca cifra curenta sau ar re-descoperi de la zero adancimea pipeline-ului
(SYS_PREDS fix, make_enc_mean, al treilea prompt).

**SUPERSEDAT 26 sep 2026:** Alexandru a ADOPTAT varianta cu engleza curata (tot paperul e zero-label),
deci cifra pe 11 limbi e **0.692527**, tag `en_fara_complex_ro11`, vezi [[engleza-nu-e-zero-label]].
0.693718 ramane doar ca referinta veche.

**How to apply (vechi):** daca urmeaza sa scrii in paper, foloseste 0.693718 ca noua cifra pe 11 limbi si
tabelul de mai sus. Daca Sergiu cere si alte modele pe romana (nu doar Gemma4), pipeline-ul de mai
sus (pasii 1-7) e reutilizabil, doar se repeta pasul 5 pentru alt model.

## Actualizare, aceeasi sesiune: tabelul scris in draft, plus intrebarea despre 0.777

Tabelul complet (r_A, r_B, r_final pe toate 11 limbi) plus explicatia mecanismului ("de ce a crescut
media") s-au scris ca punctul 8, la finalul `output/update_paper_draft.txt`. Alexandru a intrebat si
cat scotea vechea lucrare doar-romaneasca: raspuns, r=0.777 (30 iulie, pipeline vechi, tot zero-label
pe romana, dar nesincronizat cu imbunatatirile de dupa). Deci 0.7401 (nou, pipeline generic pe 11
limbi) e sub 0.777 (vechi, facut special pentru romana) cu -0.037 — de asteptat, nu un regres real.

Vezi [[shap-signal-a-feature-importance]] pentru continuarea sesiunii (interpretabilitate).
