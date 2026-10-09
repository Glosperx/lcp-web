---
name: push-github-ce-ramane-afara
description: Deciziile de gitignore din 15 sep 2026 pentru push-ul pe alex_llm, si faptul ca memoriile din docs/claude-memory sunt snapshot manual.
metadata:
  type: project
---

Remote: `git@github.com:curs-ia-2026/ia-sahistii.git`, branch `alex_llm`.
Pe 15 septembrie 2026, in arbore erau 5.4 GB de adaugat. Push-ul ar fi fost respins
oricum: `data/wiki_ctx/` avea 8 parquet-uri peste limita dura de 100 MB a GitHub
(de.parquet 745 MB, fr 734, es 657, ja 583, it 505, pt 406, en 401, ca 327).

Adaugat in `.gitignore`, cu acordul lui: `data/wiki_ctx/`, `data/wiki_tail/`,
`data/ctx_div/`, `data/freq_tail/`, `*.npz`, `data/preds_*.zip`,
`output/e1_frozen_preds_*.csv`, `output/fusion_preds_*.csv`. Ultimele doua familii erau
854 MB de dump-uri per-item; a ales explicit sa pastreze rezumatele `.md` (3.7 MB, unde
stau cifrele de citat) si sa lase predictiile brute afara, regenerabile din scripturi.
Ramane 80.4 MB de adaugat, niciun fisier peste 50 MB.

Capcana: tiparele `output/e1_frozen_preds_*.csv` NU sunt recursive, deci copiile din
`output/_rezerva_reg/` (4.5 MB) trec de ele. Lasate intentionat, sunt mici.

Cele 99 de memorii sunt copiate in `docs/claude-memory/` cu un README care spune ca
sunt notite interne, nu documentatie. **E snapshot, nu sincronizare** - la orice push
viitor trebuie recopiate din `~/.claude/projects/.../memory/` daca vrea versiunea la zi.

Scanare de secrete inainte de commit: singurele potriviri sunt parola `ralsresources`,
publicata chiar in README-ul upstream RALS, deci nu e secret. Vezi
[[rals-rolcp-datele-sunt-ale-lui-nisioi]].

Commit-ul il da el, vezi [[commitul-il-da-utilizatorul]].
