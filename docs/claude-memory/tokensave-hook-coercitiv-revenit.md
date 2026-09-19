---
name: tokensave-hook-coercitiv-revenit
description: "hook-ul PreToolUse coercitiv al tokensave (deny pe Explore/grep) a revenit singur intre 29 iul si 15 aug, probabil la update; scos din nou pe 29 aug"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b695b9f3-c330-4e00-b318-a448aad84fc6
  modified: 2026-08-29T16:33:45.614Z
---

Pe 2026-07-29 CLAUDE.md documenteaza eliminarea combo-ului "PreToolUse hook + rules/tokensave.md"
care forta tokensave peste Explore/grep, cu nota "don't re-add without asking first". Pe
2026-08-29, ambele erau active din nou: settings.json avea hook-ul (matcher
`Agent|Grep|Bash|Glob`, deny hard, testat empiric pe Agent-Explore si Bash-grep in proiecte cu
`.tokensave/`), iar rules/tokensave.md avea inca "MANDATORY... No exceptions" (mtime 15 aug,
dupa data "eliminarii"). Binarul tokensave e symlink catre ~/.local/opt/tokensave/tokensave si
pare sa aiba update propriu — cel mai probabil un update/reinstall a rescris ambele fisiere
silentios, fara nicio actiune manuala.

Rezolvat pe 29 aug: scos din nou entry-ul PreToolUse din settings.json (a ramas `rtk hook claude`
pe Bash si hook-urile benigne `hook-prompt-submit`/`hook-stop`), sters rules/tokensave.md.

Descoperire a doua, tot pe 29 aug, in aceeasi sesiune: nu e doar update-ul binarului. Rularea unei
comenzi CLI complet obisnuite — `tokensave gain` (cerut pentru a raporta economia de tokeni) — a
rescris singura `settings.json` (log: "Wrote /Users/alexandrucojoaca/.claude/settings.json") si a
recreat `rules/tokensave.md`, identic cuvant cu cuvant. `tokensave doctor` trateaza prezenta lor ca
un check de sanatate ("PreToolUse hook installed", "rules/tokensave.md contains tokensave rules").
`tokensave install --help` confirma explicit conceptul: flag-ul `--wildcard-permissions` se descrie
ca fiind persistat "so future silent reinstalls keep the choice" — reinstalarea silentioasa e
comportament documentat al tool-ului, nu bug izolat. Nu exista in `~/.tokensave/config.toml` vreun
flag gasit care sa opreasca acest self-heal (doar upload_enabled, watcher_debounce,
extraction_timeout_secs, wildcard_permissions).

**Why:** utilizatorul a cerut explicit sa nu se readauge coercitia fara sa intrebe; a fost
readaugata oricum, silentios, de aproape orice invocare a tokensave CLI care face un self-check
(gain, doctor, probabil si sync/status/serve), nu doar la update-ul binarului.

**How to apply:** dupa ORICE comanda `tokensave` rulata direct din shell (gain, doctor, install,
reinstall, si posibil altele), verifica `~/.claude/settings.json` (hooks.PreToolUse pentru un
matcher `Agent|Grep|Bash|Glob`) si daca `~/.claude/rules/tokensave.md` a reaparut. Politica
decisa cu userul pe 29 aug: **curata din nou fara sa mai intrebi de fiecare data** — nu incerca sa
opresti mecanismul (nu exista flag cunoscut), doar corecteaza cand il vezi. Apelurile MCP
(tokensave_context, tokensave_search etc, prin server-ul `serve`) nu par sa declanseze acelasi
rescriere — problema a fost observata specific la comenzi CLI directe.
