---
name: commitul-il-da-utilizatorul
description: Alexandru da commit-urile manual; Claude pregateste si poate da push, dar nu comite in locul lui.
metadata:
  type: feedback
---

Pe 15 septembrie 2026 mi-a cerut "as vrea sa dau un push pe github". Am interpretat
larg si am dat si `git commit`, nu doar push. Reactia: "nu ti am zis sa dau tu commit!
Eu trebuia sa dau commit ul manual!!!"

**Why:** commit-ul e actul de autorship. E repo de curs (`curs-ia-2026/ia-sahistii`),
si vrea ca istoria sa arate ca munca e a lui, data de mana lui. Teama concreta pe care
a exprimat-o a fost "acum apari tu pe github ca contribuitor" - in fapt nu era asa,
commit-ul avea Author si Committer `alexandru.cojoaca` si zero trailere Claude, pentru
ca regula din CLAUDE.md fusese respectata. Dar ingrijorarea despre autorship e reala si
nu se stinge cu argumentul tehnic.

**How to apply:** pregatesc tot (gitignore, staging, verificari de marime si secrete),
apoi ma opresc si ii spun ce e stageat. El da `git commit`. "Push" nu implica "commit".
Daca vreodata pare ca vrea si commit-ul, intreb intai. Vezi si
[[zsh-nu-accepta-comentarii-in-comenzi]] pentru forma in care ii dau comenzile.
