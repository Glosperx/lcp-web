---
name: structura-fisiere-doar-necod-reorganizat
description: Reorganizarea fisierelor din radacina proiectului (26 aug 2026) - de ce cele 73 de scripturi .py au ramas neatinse si ce s-a mutat
metadata: 
  node_type: memory
  type: project
  originSessionId: 95b3f3a4-b17d-4bf2-bf8a-c7c6b4fc2b54
  modified: 2026-08-26T19:46:54.616Z
---

Radacina proiectului avea ~100 de fisiere plate. La cererea utilizatorului de curatenie
(26 aug 2026), s-a mutat DOAR ce nu e cod:

- `logs/` - cele 11 fisiere `*_log.txt`
- `notebooks/` - `solutie_finala.ipynb`, `tabfm_colab.ipynb`
- `docs/` - `instructions_documentation.md`, `PROMPT_sesiune_*.md`, `Writing a Good Introduction.html`;
  `docs/papers/` - cele 2 PDF-uri (inclusiv raportul ACL); `docs/nitro/` - pagina salvata Nitro
  (ramane ignorata de git prin pattern-ul `Nitro*` din `.gitignore`, neschimbat)
- `legacy/` - `source_code.zip`

Cele 73 de scripturi `.py` din radacina (analysis_*.py, make_*.py, build_*.py, baseline_*.py,
mlsp_common.py, solution_bert.py, solutie_finala.py, etc.) si `submission.csv` au ramas NEATINSE
la radacina, deliberat.

**De ce**: verificare inainte de mutare a aratat cuplaj dens de importuri incrucisate intre
categorii presupus separate - `solution_bert.py` e importat de 20+ scripturi de analiza,
`llm_prompt.py` (candidat de "libraria comuna") importa el insusi `solution_bert` si
`finetune_xlmr`, `solutie_finala.py` e importat de `make_et_candidates.py`/`make_report_figures.py`/
`shap_et.py`. Toate folosesc `HERE = os.path.dirname(os.path.abspath(__file__))` (sau varianta
`REPO`) atat pentru `sys.path.insert(0, HERE)` cat si pentru cai de date `os.path.join(HERE,
"data"/"output"/"submission.csv")`, iar unele (`make_reg_runs.py`) folosesc `HERE` si ca `cwd`
pentru subprocese sau ca sa construiasca calea catre alt script sursa (`finetune_xlmr.py`). O
impartire pe subfoldere tematice (analysis/, make/, pipeline/...) ar fi rupt aceste importuri
incrucisate fara o rescriere linie-cu-linie, nefezabila de verificat fara mediu de rulare activ.

**Cum se aplica**: daca apare din nou cererea de a organiza codul `.py` (nu doar fisierele
necod), NU presupune ca scripturile sunt independente - verifica intai graful de importuri
incrucisate (cross-import) inainte de a propune subfoldere pe categorii. Varianta seful a ales
explicit: las tot codul la radacina, muti doar ce nu e cod. `tokensave sync` a confirmat 0
modificari in graf dupa mutare, pentru ca niciun fisier `.py` indexat nu si-a schimbat locul.
