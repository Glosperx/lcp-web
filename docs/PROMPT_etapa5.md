# Prompt pentru o sesiune noua Claude Code pe PC: Etapa 5, frontend-ul adevarat

Scris pe PC pe 22 nov 2026, dupa auditul de dupa Etapa 8. Rezultatul auditului e in
`bench/results/audit.txt`. Sesiunea asta construieste frontend-ul din `static/`. Nu atinge modelul,
artefactele sau pipeline-ul, decat daca Alexandru cere explicit.

## Unde suntem

- Facute: Etapa 1 (timpi pe CPU, Mac), Etapa 7 pe PC (configuratia GPU), Etapele 2 si 3 (modelul
  exportat si B-ul site-ului), Etapa 4 (pipeline si API in flux), Etapa 8 (serverul si hostingul)
  si auditul. Raman Etapa 5 (acum), Etapa 6 (imaginea finala) si benchmark-ul final prin API
  (Etapa 7 din PLAN, `scripts/benchmark.py`).
- Site-ul e live 24/7:
  - pagina statica pe Vercel: https://lcp-web-static.vercel.app (proiectul `lcp-web`, Root
    Directory `static`, deploy automat la push). Tot ce e in `static/` se publica.
  - API-ul pe GPU-ul acestui PC, in `docker compose` (`docker-compose.yml`), expus doar prin
    Tailscale Funnel: https://lcp.tail6e4ef5.ts.net -> 127.0.0.1:8000. Serverul serveste si el
    `static/` la radacina adresei ts.net (din repo-ul montat, fara restart).
  - UptimeRobot verifica `/api/health` la 5 minute.
- Cifra site-ului: media r pe 11 limbi 0.691328 (paperul are 0.692521).
- `static/index.html` e inca pagina de test din Etapa 8, reparata la audit: offseturi convertite in
  UTF-16, estomparea propozitiilor in lucru, butonul blocat in timpul analizei, eroare la flux
  intrerupt. Poti refolosi din ea logica de flux, login-ul si popover-ul.

Citeste intai, intregi: `docs/PLAN.md` (Etapa 5 si sectiunea de la inceput, "De stiut pentru
site"), `README.md`, `bench/results/audit.txt`, `bench/results/concluzie_etapa4.txt`,
`bench/results/concluzie_etapa8.txt`, `server.py`, `lcp/pipeline.py` (functiile `analyze` si
`languages`), `static/index.html`.

## Ce a ramas nereparat dupa audit

Vezi sectiunea 4 din `audit.txt`. Pentru Etapa 5 conteaza:
- P1: toate cuvintele cu litere care nu sunt de continut vin ca `"function": true`, nivel 1: si
  numele proprii (Einstein, Paris, Eminescu) si numeralele scrise (two, doi). Pagina de test le
  arata "foarte usor, cuvant functional". De decis cu Alexandru (vezi deciziile). Daca vrea sa le
  separe, serverul trebuie sa trimita UPOS-ul sau un camp `kind`. Asta atinge `lcp/pipeline.py`,
  deci restartul containerului.
- P3: `/api/health` nu vede un fir de lucru mort sau blocat.
- CORS accepta orice proiect Vercel numit `lcp-web-static-*`. Efectul e mic, pentru ca accesul tine
  de cod.
- Etapele 6 si 7 finale; "tailscale down/up" dupa restart, daca tunelul e lent.

## API-ul pe care se construieste frontend-ul

Adresa: `const API = "https://lcp.tail6e4ef5.ts.net"` (inline in pagina; Vercel nu are backend).
CORS permite https://lcp-web-static.vercel.app, deploy-urile de preview `lcp-web-static-*.vercel.app`,
adresa ts.net, http://localhost:8000 si http://127.0.0.1:8000.

Accesul: `/api/languages` si `/api/analyze` cer antetul `X-Access-Code`. Pagina cere codul o data,
il verifica cu `POST /api/auth {"code": "..."}` (200 `{"ok": true}`, 401 gresit, 429 dupa 10
coduri gresite de la o adresa in 10 minute) si il tine in localStorage. Codul nu apare in pagina.

`GET /api/languages`:
```
{"languages": [{"code": "en", "name": "English", "r": 0.8704, "ci": [lo, hi], "n_test": 570,
                "warn_chars": 2000, "est_s_per_1000_chars": 17.9}, ...],   // 11 limbi; ja: warn 700
 "mean_r": 0.6913, "mean_ci": [lo, hi], "paper_mean_r": 0.6925,
 "levels": {"1": "very easy", "2": "easy", "3": "neutral", "4": "difficult", "5": "very difficult"},
 "max_chars": 20000}
```

`GET /api/health` (si HEAD), fara cod: 503 `{"status": "loading"}` in cele ~70 s de incarcare,
apoi `{"status": "ok", "active", "waiting", "access_code": true, "tok_s", "slow", "probe_age_s",
"last_text_tok_s"}`. `slow: true` inseamna ca placa merge de ~2 ori mai incet (model partial in
memoria shared). Pagina poate spune atunci ca analiza dureaza mai mult decat estimarea.

`POST /api/analyze {"lang": "en", "text": "..."}` raspunde `application/x-ndjson`, cate un obiect
JSON pe linie, fiecare terminat cu `\n`:
- `{"type": "queued", "position": n}`: doar ca prima linie, cand sunt deja 6 texte active; nu se
  actualizeaza;
- `{"type": "ping"}`: dupa 15 s fara alt eveniment; se ignora;
- `{"type": "paragraphs", "lang", "paragraphs": [{"i", "start", "end"}]}`: primul, fara model;
- per paragraf, `{"type": "sentences", "paragraph": p, "sentences": [{"i", "start", "end",
  "content_words", "split"?}]}`. Indicii propozitiilor merg pe tot textul. `split` marcheaza
  bucatile unei propozitii lungi (peste 192 de tokeni sau 40 de cuvinte de continut);
- cate un `{"type": "sentence", "i", "paragraph", "start", "end", "words": [...]}` pe propozitie
  terminata, in ordine. Cuvintele sunt sortate dupa `start`:
  - de continut: `start`, `end`, `text`, `lemma`, `level` (1-5), `label` (engleza), `score` (0-1,
    4 zecimale), `zipf` (sau null), `A`, `B` (z-score, 3 zecimale), `fused`, plus optional
    `cropped`, `no_A`, `no_B` (true);
  - restul, cu litere: `start`, `end`, `text`, `lemma`, `level` 1, `label`, `"function": true`,
    fara scor;
  - punctuatia si numerele fara litere nu apar;
- `{"type": "done", "lang", "paragraphs", "sentences", "content_words", "function_words",
  "cropped", "low_mass", "timings": {"segment_s", "stanza_loaded", "A_s", "B_s", "fusion_s",
  "total_s", "first_sentence_s", "readings", "s_per_reading", "prompt_tokens",
  "evaluated_tokens"}}`: ultimul;
- `{"type": "error", "message": "analysis failed (TypeName)"}`: la o eroare, apoi fluxul se
  inchide. Un flux care se termina fara `done` si fara `error` e o intrerupere.

Offseturile (`start`, `end` la paragrafe, propozitii si cuvinte) numara code points Unicode
(indici Python), nu unitati UTF-16. Pagina le converteste o data pe text (vezi `cpMap` din
`static/index.html`), altfel un emoji decaleaza tot ce urmeaza. Si limitele numara code points:
`cpLen`.

Erorile HTTP inainte de flux: 400 (limba necunoscuta, text gol sau doar spatii), 401 (cod lipsa
sau gresit: pagina cere din nou codul), 413 (peste `max_chars` sau corp peste 256 KiB), 422 (JSON
gresit), 429 (deja 2 texte de la aceeasi adresa, sau prea multe coduri gresite), 503 (coada de 16
plina sau modele inca in incarcare). Corpul are `{"detail": "..."}` in engleza.

Comportament de stiut:
- pana la 6 texte ruleaza alternat, propozitie cu propozitie, cu coada de 16. Estimarea
  `est_s_per_1000_chars` e pentru un text singur, pe placa sanatoasa;
- o deconectare (pagina inchisa, fetch abandonat cu AbortController) anuleaza textul in ~0.5 s;
- prima propozitie colorata apare dupa 1-6 s; 2 paragrafe dureaza ~15-45 s;
- scorul e relativ la limba si la distributia setului de test, nu la textul dat.

## Cerintele Etapei 5 (din PLAN, cu deciziile luate)

- `static/`: HTML + CSS + JS simplu, fara build (PLAN: `index.html`, `app.css`, `app.js`). Vercel
  publica folderul asa cum e.
- Daca skill-ul `apple-design` e instalat, se incarca inainte de primul rand de cod (vezi
  deciziile).
- Asezare ca DeepL: doua panouri egale, unul langa altul, unul sub altul pe telefon. Stanga: bara
  cu selectorul de limba si r-ul limbii, caseta mare de text, contorul, butonul Analizeaza si
  Cmd/Ctrl+Enter. Dreapta: acelasi text, cu cuvintele colorate.
- Contorul: nu exista limita de 2000 (decizie). Arata `n / 20000`; peste `warn_chars` (2000, ja
  700) cere confirmare inainte de analiza, cu durata estimata din `est_s_per_1000_chars`. Peste
  20000 butonul e oprit.
- Colorare ca FleLex: fundal colorat pe cuvant, cinci culori de la verde (1) prin galben si
  portocaliu la rosu (5), cu variante pentru dark mode. Deasupra, legenda cu cele cinci niveluri
  si cate cuvinte are fiecare; click pe un nivel lasa colorate doar cuvintele lui (lipseste in
  pagina de test).
- Cuvintele functionale SUNT colorate, ca nivel 1, fara model (decizie; planul spunea "raman text
  normal"). In popover: "neevaluat de model". Vezi P1 pentru numele proprii si numerale.
- Propozitiile in lucru apar estompate si se coloreaza pe masura ce sosesc.
- Click pe cuvant (sau Enter; cuvintele sunt focusabile): popover cu nivelul si eticheta, scorul
  0-1, lema, frecventa Zipf si, pe un rand mic, A si B. Escape sau click in afara il inchide.
- Pe pagina: scorul e relativ la limba si nu se compara intre limbi; r-ul limbii alese (increderea
  difera mult: en 0.87, pt 0.84, ja 0.78 ... ca 0.56, fil 0.50, si 0.43); fara text din MLSP,
  RoLCP sau CompLex (nici ca exemplu). In perioada de review ARR, link-ul site-ului nu se pune in
  paper.
- Din Etapa 8 raman: login-ul cu cod, lista de limbi tinuta in cache (pagina apare imediat),
  mesajele pentru server oprit, server in pornire, coada si 429.
- Verificarea din PLAN: un paragraf in fiecare limba, culorile si popover-ul merg; plus telefonul
  (Alexandru testeaza), dark mode, tastatura (Tab, Enter, Escape), un text cu emoji, un text lung
  (confirmarea), doua paragrafe.

## Deciziile de cerut lui Alexandru inainte de cod

1. Scala de culori. Acum, pe texte reale, nivelurile ies 50% / 35% / 10% / 3% / 2%, deci mai ales
   verde: scala e percentila cuvantului in distributia de test a limbii, trecuta prin cuantilele
   etichetelor MLSP. Variante: (a) cum e acum; (b) recalibrata pe texte obisnuite: percentila in
   distributia cuvintelor din texte obisnuite ale fiecarei limbi. Asta e o schimbare de afisare
   (`scale` din `artifacts/params.json`, `lcp/fusion.py:score01`), nu de model. Cere un corpus de
   texte obisnuite pe limba (de exemplu Wikipedia, CC BY-SA, nu MLSP), trecut prin pipeline, deci
   timp de GPU si restartul containerului. Tot atunci, intrebarea P1: numele proprii si
   numeralele raman nivel 1 "functional" sau devin "neevaluat", fara culoare?
2. Limba interfetei: romana, engleza sau ambele (cu comutator). Etichetele de nivel vin de la
   server in engleza; pagina le traduce.
3. Skill-ul `apple-design`: nu e instalat pe PC. Il instaleaza Alexandru sau se lucreaza fara el,
   dupa principiile lui (tipografie de sistem, spatiere generoasa, culori sobre, dark mode).

## Cum testezi

- Logica paginii (flux, offseturi, estompare, legenda, popover) in node 24 (e instalat), cu un DOM
  minimal si un fetch fals, ca in audit. Testele de reproducere stau in scratchpad, nu in repo.
- Pe live: doar texte scurte, scrise de tine. Codul il citesti din `.env` intr-o variabila
  (`CODE="$(grep -E '^LCP_ACCESS_CODE=' .env | cut -d= -f2- | tr -d '\r')"`) si nu-l afisezi.
- Schimbarile din `static/` nu cer restartul containerului: serverul le serveste direct din repo, la
  https://lcp.tail6e4ef5.ts.net/ (sau http://127.0.0.1:8000/). Pe Vercel ajung doar dupa push-ul
  lui Alexandru.
- Calea publica, de pe PC: `curl --resolve lcp.tail6e4ef5.ts.net:443:<IP A din DNS public, de ex.
  prin cloudflare-dns.com> https://lcp.tail6e4ef5.ts.net/...` (MagicDNS raspunde aici cu adresa
  din tailnet).
- Daca atingi `server.py` sau `lcp/`: intrebi intai, apoi `docker compose restart api` (~75 s jos)
  sau `scripts\site_stop.cmd` + `scripts\site_start.cmd`. Verifici `/api/health` local si public,
  inclusiv `tok_s` (~1000 normal; sub 700 = spill: se inchid aplicatiile care folosesc placa si se
  reporneste). Ii spui lui Alexandru ca va primi mail "Down".

## Mediul (verificat, nu mai trebuie redescoperit)

- RTX 2070 SUPER 8 GB, Ryzen 7 3700X, 16 GB RAM, Docker Desktop cu WSL2 (12 GB). Imaginea
  `lcp-web:cuda` si volumele `lcp-hf` si `lcp-stanza` sunt pline. Containerul live ia ~4.2 GB
  dupa pornire si ~7.4 GB dupa ce a lucrat. Verifici `docker stats` inainte de un al doilea
  container cu encodere.
- Python-ul de pe host (3.14) are numpy stricat. Biblioteca standard merge (`scripts/api_check.py`
  ruleaza pe host); restul ruleaza in container (`GPU=0 docker/run_cuda.sh python ...`).
- VRAM: inainte de pornirea serverului trebuie sa fie sub ~700 MiB ocupati. Nici asta nu garanteaza
  ca modelul incape (636 MiB au dat spill), de aceea conteaza `tok_s`. Firefox cu accelerare ia
  ~200 MiB; dwm ~380 MiB pe ecranul de 2560 px.
- Git Bash: `MSYS_NO_PATHCONV=1` si `pwd -W` (deja in `docker/run_cuda.sh`).
- Tailscale CLI: `"C:\Program Files\Tailscale\tailscale.exe"`. Tunelul Funnel trece prin releul
  DERP (Frankfurt): 0.8-7 s pe o conexiune noua, ~0.2 s pe una deschisa. E cunoscut.
- `scripts/site_start.cmd` si `site_stop.cmd` n-au optiune de ajutor; orice rulare porneste sau
  opreste site-ul de-adevaratelea. `site_start` cere Enter daca VRAM-ul e prea plin (cu `-Yes`
  continua).

## Reguli (neschimbate)

- Nu da commit si nu face push. Pregatesti fisierele si staging-ul, iar commit-ul il da Alexandru.
  Comenzile de git i le dai in engleza, cu mesaje scurte, FARA linii `Co-Authored-By` sau alta
  atribuire.
- Cere aprobare inainte de `docker build` si de orice descarcare mare.
- Nu intra in git text din MLSP, RoLCP sau CompLex (repo-ul e privat, dar regula ramane). In
  loguri, nu printezi propozitii din date. Pe site nu apare niciun exemplu din date.
- Codul de acces nu apare in git, in memorie, in `static/` sau in chat. In teste il citesti din
  `.env` intr-o variabila.
- Nu opresti si nu repornesti site-ul fara sa intrebi.
- Fara subagenti; verifici singur.
- In chat: romana fara diacritice, fara tabele markdown, explicatii scurte. La rularile lungi dai
  statusuri dese: progres, s/citire, VRAM.
- Daca o poarta pica sau ceva nu incape in memorie, te opresti si raportezi cifra, fara sa ocolesti.
