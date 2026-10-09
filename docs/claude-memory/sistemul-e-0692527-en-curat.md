---
name: sistemul-e-0692527-en-curat
description: PUNCT DE RELUARE 26 sep 2026 - sistemul adoptat pe 11 limbi e 0.692527 cu engleza zero-label curata; comenzile de reproducere, fisierele, ce ramane de facut
metadata:
  type: project
---

Adoptat de Alexandru pe **26 sep 2026**, fiindca tot paperul e construit pe zero-label ("Without
Target-Language Labels" e in titlu). Inlocuieste 0.693718 din [[rolcp-a-11a-limba-lolo]]. Detaliile
masuratorii sunt in [[engleza-nu-e-zero-label]].

## Ce e diferit

Flag nou `finetune_xlmr.py --en-fara-complex` (doar pentru `--frozentrial`, default neschimbat, sufix
`_en-fara-complex` pe iesiri, refuzat de `--export-blocks`). La L = en: p_multi se antreneaza fara
CompLex EN (Xen), doar pe celelalte 10 limbi; p_en al randurilor en = acelasi p_multi, deci `w_src`
nu mai are efect pe engleza (raportul tot afiseaza 0.625, dar e inert).

## Reproducere

```
PY=/opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python
for e in xlmr labse e5; do $PY finetune_xlmr.py --frozentrial --lemma-freq --afeat fert_inloc --include-ro --encoder $e --en-fara-complex; done
$PY make_enc_mean.py --cai xlmr=output/e1_frozen_preds_lemma_fert_inloc_en-fara-complex_ro11.csv labse=output/e1_frozen_preds_labse_lemma_fert_inloc_en-fara-complex_ro11.csv e5=output/e1_frozen_preds_e5_lemma_fert_inloc_en-fara-complex_ro11.csv --dest output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc_en-fara-complex_ro11.csv
$PY fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag en_fara_complex_ro11 --b-dir output/bakeoff_test_M3K_ro11 --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc_en-fara-complex_ro11.csv
```

Fiecare --frozentrial ia ~1 minut (embeddingurile sunt in cache), fuziunea ~10s. Control facut: fara flag,
toate trei encoderele, media si fuziunea reproduc 0.693718 bit cu bit (`cmp`). Rularea de control a
fuziunii e sub tag `control_enfc_ro11` in output/, copie identica, se poate sterge.

## Cifrele

Medie 11 limbi: A 0.6096, B 0.6635, fuziune **0.692527** (d -0.0012 [-0.0020, -0.0005] fata de vechi).
Pe 10 MLSP: 0.68783. Engleza: A 0.8064, B 0.8471, fuziune 0.8695 [0.8455, 0.8912].
Per limba r_final: ca 0.5632, de 0.7704, en 0.8695, es 0.7672, fil 0.5045, fr 0.6608, it 0.6801,
ja 0.7909, pt 0.8416, si 0.4302, ro 0.7394. Raport: `output/e_fusion_lolo_en_fara_complex_ro11.md`.
Celelalte limbi scad putin prin criteriul LOLO (it -0.0037 cel mai mult), efect agregat pe 10 fara en
-0.00095 [-0.0014, -0.0005]. Scriptul de bootstrap pereche nu e in repo (a fost in scratchpad).

## Ce ramane

1. Varianta pe **10 limbi** (0.690001) are aceeasi scurgere pe engleza si NU e rulata curat. Paperul
   (`Paper/Articol_Multilingv/paper_full.tex`) e inca pe 10 limbi. Aceleasi comenzi fara `--include-ro`,
   `--b-dir output/bakeoff_test_M3K`, ~5 minute. Oferit, neconfirmat.
2. Tabelul nou (punctul 8 din `output/update_paper_draft.txt`) i s-a dat in chat, NU e scris in draft;
   el editeaza draftul in paralel, vezi [[update-paper-draft-linia-de-taiere]].
3. Nimic comis: `finetune_xlmr.py` modificat plus fisiere noi in output/. Commit-ul il da el, vezi
   [[commitul-il-da-utilizatorul]].
4. Nota de Limitations "zero-label cu exceptia englezei" nu mai trebuie scrisa; rezerva transductiva
   ramane.

**Why:** fara asta, o sesiune viitoare ar cita 0.693718 sau ar re-deschide scurgerea pe engleza.
**How to apply:** orice cifra pe 11 limbi se citeaza de aici; orice extensie a sistemului pe 11 limbi
porneste de la comanda cu `--en-fara-complex`.
