Continuam scurtarea documentatiei de curs din `Paper/Articol_Multilingv/documentatie_overleaf.tex` (titlu: "Lexical Complexity
Prediction Without Target-Language Labels", sablon ACL). Toate sectiunile sunt scrise si acceptate, experimentele sunt gata.
Nu rulam experimente noi si nu schimbam nicio cifra. Prima sesiune de scurtare (11 oct 2026) a adus corpul de la 12 la 11
pagini si a aratat ce NU vrea el sa taiem. In sesiunea asta il aducem la 8 pagini. Pas cu pas, cu aprobarea lui inainte de
fiecare schimbare. Prompt-ul vechi, `docs/PROMPT_sesiune_scurtare_8_pagini.md`, ramane valabil pentru regulile generale;
asta il continua.

## Intrebare pusa la inceput

El a scris: "avem 11 pagini scrise pana la Limitations, trebuie sa scriem maxim 8 pagini inclusiv". Nu e clar ce intra in cele 8:
- (A) corpul pana la sfarsitul lui Conclusions (regula ACL/ARR, varianta din prompt-ul vechi: Limitations, Acknowledgments,
  bibliografia, anexele NU se numara). Asta presupui implicit.
- (B) si Implementation, si Limitations.
Intrebi intai care. Daca cursul difera de ACL, conteaza cursul (el verifica, tu nu presupui).

## Starea (verifici cu `shasum`; daca difera de 409c89f3, intrebi inainte sa faci orice: poate a editat in Overleaf)

- .tex sha **409c89f3**, **14 pagini** in total (bibliografia, apoi anexa A cu SHAP si anexa B cu Tabelul 8, ambele pe pagina 14, sunt la sfarsit).
- Corpul se termina pe **pagina 11**, coloana dreapta, y ~565 (titlul Implementation e la y 577). Limitations incepe pe
  p11, coloana dreapta, y 635, si se termina pe p12, coloana stanga, y 381 (Acknowledgments).
- Pozitie liniara (vezi `measure.py`): corpul se termina la 15290, tinta pentru (A) e 11264. Mai trebuie taiat **4026 pt = 5.7
  coloane = 2.9 pagini**. Pentru (B) tinta e la sfarsitul lui Limitations, pos 15799: ~3.2 pagini.
- Hartă (pagina de start, din .aux): Introduction p1, Related Work p1, Method p2 (Data p2, Signal A p3, Signal B p4, Fusion p5,
  Evaluation Protocol p5), Experimental Results p6 (4.1 Signal A p6, 4.2 Signal B p8, 4.3 Fusion p10, 4.4 Comparison p10),
  What Did Not Work p11, Conclusions p11.
- Backup-uri ale primei sesiuni: scratchpad-ul sesiunii a0f202c1 `bak/` (bc856e97 = originalul, 5761d922, d51b9eca, 31330342).
  Scratchpad-ul nu se pastreaza intre sesiuni: copiezi tu .tex-ul in scratchpad-ul sesiunii tale inainte de prima scriere.
- Floats in corp: Fig. 1 pipeline (figure*, `fig_pipeline_doc_vertical.pdf`, 0.65\textwidth), Fig. 2 t-SNE (figure*, 0.75),
  Fig. 3 SHAP (figure*, 0.55), 7 tabele `table` (tab:signal-a, tab:signal-a-models, tab:ablations, tab:llms, tab:signal-b,
  tab:per-language, tab:corr-ab). Tabelul 8 (tab:published, table*) e in anexa B. `\nocite{*}` e inca in fisier si lungeste doar
  bibliografia; se scoate la verificarea finala.
- Starea completa: primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md`.

## Ce citesti intai

1. Memoriile: `documentatie-scurtare-feedback-11-oct` (CEA MAI IMPORTANTA), `cerere-sesiune-documentatie`,
   `text-final-rescris-de-gemma`, `preferinte-de-scriitura-paper`, `scrie-uman-nu-overexplain`,
   `lista-utilizatorului-nu-se-reformuleaza`, `fara-agenti-multipli-tokeni`, `tabele-un-subiect-pe-tabel`,
   `grafice-shap-native-nu-custom`, `diagrama-pipeline-drawio`, `raspunsuri-fara-diacritice-fara-tabele-md`.
2. Tot .tex-ul, cu comentariile de provenienta deasupra fiecarei sectiuni (cine a scris textul: el, Claude sau Gemma 4).
3. RALS (`~/Downloads/2025.emnlp-main.1603.pdf`), doar ca reper: ce tine in corp si ce muta in anexe.

## Ce a decis el (nu redeschizi fara sa intrebi)

- **Method si sectiunea 4 (Experimental Results) sunt cele mai importante.** El a RESPINS taierea definitiilor care se repeta intre
  Method si Results (definitia grupurilor, a regresorilor, a prompturilor, intro-ul lui Step 8 etc.): "nu mai scoate definitii",
  "nu mi se pare capitolul 4 cel de unde ar trebui sa tai masiv text". Nu propui "repetitii" din sectiunile 3 si 4 ca taieri.
- Intro-ul sectiunii 4: doar scurtat putin, nu taiat. Propunerea din chat (scos "Signal B does not fine-tune the language model or use
  any similar technique" si "in the dataset", restul neschimbat) nu a primit raspuns.
- Cursul cere pasii metodei explicati in corp (Method ramane cu pasii 1-8) si sectiunea What Did Not Work in corp. Mutarea lui in
  Limitations: respinsa. In anexa: doar daca el confirma cu cursul.
- Figurile din corp sunt alese de el: pipeline, SHAP, t-SNE. Le poti propune pentru anexa cu castigul masurat, dar decide el.
- Tabelul 8 (Comparison with Published Results) e deja in anexa B (decis de el). A zis "da, cred ca e ok" la mutarea lui a1, a3, a4 in
  anexa, dar NU s-a executat inca.
- Un subiect pe tabel. Bold pe rezultatul nostru. Fara trucuri de layout interzise de sablon: fara `\vspace` negativ, fara font sau
  margini schimbate, fara `\small` pe text. `\small` si `\tabcolsep` in tabele sunt deja folosite.
- Spatiul dintre elementele listei din 3.1 Data: am masurat `\itemsep`, `\parsep`, `\topsep` la 0 si textul de dupa lista nu se
  muta (justificarea verticala a coloanei absoarbe). Singura varianta reala: lista inline "(1) ... (2) ... (3)". Nedecis.
- El credea ca tabelele s-au micsorat. NU s-au micsorat: doar cele trei figuri. Daca vrei tabele mai mici, masori intai si intrebi.

## Ce s-a facut deja (nu repeti)

- Figuri: pipeline 0.65, t-SNE 0.75, SHAP 0.55 (era 0.77, 1.0, 0.7). Tabelul 8 in anexa B (titlu "Comparison with Published Results by
  Language"), cu trimitere "Table 8 (Appendix B)" in 4.4.
- Step 2 (3.2): scoase propozitia cu scala Zipf si cea cu indicatorii.
- Rescrise de Gemma 4 (prompturi `docs/PROMPT_gemma_*`): 4.2 Language models (400 -> 239 de cuvinte, `_language_models` ... `_v5`),
  4.1 Regression models (116 -> 89), 4.1 TabFM (124 -> 115), 4.2 Baseline (218 -> 171), 4.4 (303 -> 273, cu valorile in text),
  Sectiunea 5 (335 -> 302). Gemma NU respecta limitele de cuvinte: scurteaza 10-25% si introduce erori daca regulile sunt strambe
  (a scris "Six LoRA runs reached 0.462" in loc de "best of six", si "target" -> "test language" din cauza unei reguli). Verifici
  fiecare rezultat fata de lista de fapte.

## Ce mai poate iesi (masurat in prima sesiune; NU se aduna si bazele difera, deci RE-MASORI)

Castig in coloane (1 coloana = jumatate de pagina) cand blocul e scos singur:
- a1: paragraful Regression models + `tab:signal-a-models` + paragraful TabFM: ~1.2. Cu a3 + a4 impreuna: ~2.7 (1.3 pagini), cu a2: ~3.3.
- a2: Encoder Layers (7 randuri): ~0.2.
- a3: `tab:llms` + cele doua paragrafe Language models: era 1.1; ACUM textul e deja mai scurt, deci mai putin. Remasoara.
- a4: `tab:corr-ab` (coloana Ridge--HGB pleaca oricum cu a1; A--B pe limba se pierde, media .685 ramane in text): ~0.3.
- a5: Embedding Centring + t-SNE (figura aleasa de el + ecuatia 3): ~1.3.
- a6: paragraful cu bootstrap-ul din 3.5: ~0.6. a7: lista celor patru trasaturi din Step 2: ~1.0 (risc: cursul cere pasii explicati).
- a8: Baseline Claude + `tab:ablations`: ~0.7 (nu recomandat, el tine la rezultat). a9: Prompts + `tab:signal-b` ~0.6, Temperature and
  grouping ~0.6. a10: figura SHAP ~0.6, textul SHAP ~0.6 (alese de el). a11: `tab:signal-a` + Encoders ~0.6.
- Related Work intreg: ~1.1 (accepta de el; un paragraf, ~0.2).
- Fig. 1 orizontala (`figures/fig_pipeline_doc.pdf`, `\textwidth`) in loc de verticala 0.65: ~0.3. El a ales verticala; poti propune schimbul.
- Combinatiile din prima sesiune care ajungeau la 8 pagini FOLOSEAU taierile de repetitii din sectiunea 4, acum respinse. Fara ele
  trebuie mutate in anexa cele mai multe blocuri de ablatii (a1, a2, a3, a4, a6, a7 si t-SNE-ul sau patru blocuri de text) plus
  eventual Related Work si Fig. 1 orizontala. Spui asta pe fata, cu cifrele masurate, nu promiti 8 pagini fara ele.

## Pasul 1: Masurare (fara nicio scriere in .tex)

Unelte gata in `docs/scurtare_tools/` (rulate pe .tex-ul de acum, functioneaza):
- `compile.sh <tex> <director_gol>`: copiaza .tex + acl.sty + acl_natbib.bst + figures/, pdflatex, bibtex, pdflatex de doua ori,
  tipareste erori/Undefined/Overfull/pagini/`??`.
- `measure.py <director_compilat> [pozitie_referinta]`: pagina, coloana si y ale titlurilor Implementation/Limitations/Acknowledgments si
  cat mai trebuie taiat pana la tinta 8 pagini.
- `variants.py <baza.tex> <spec.json> <director_lucru>`: spec = `[["nume",[[linie_start,linie_sfarit],...],[["text vechi","text nou"],...]], ...]`,
  linii 1-indexate din baza; compileaza fiecare varianta intreaga si da castigul fata de control, in 4 rulari paralele.
Fiecare candidat: il masori compilat, nu il ghicesti. Combinatiile le masori si ele intregi.

## Pasul 2: Lista in chat

Optiunile, fiecare cu: ce se muta sau se taie, unde (fisier si linie), castigul masurat, ce se pierde din corp, ce trimiteri se schimba.
Grupate in: (a) mutari in anexa, (b) taieri (doar ce indica el sau blocuri intregi, NU definitii repetate din 3 si 4), (c) layout.
Spui ce combinatie ajunge la 8 pagini cu cele mai putine pierderi si ce NU ajunge. Eu aleg.

## Pasul 3: Aplicare

- O schimbare (sau un grup aprobat) o data. Dupa fiecare: compilare, pagina si pozitia pe care se termina corpul.
- Mutarea unui bloc in anexa se face cuvant cu cuvant; se schimba doar trimiterile ("Appendix B", "Appendix C"), iar mutarea se noteaza
  intr-un comentariu. Comentariile de sursa raman langa fraza lor. Cifrele nu se schimba.
- Sectiunile lui Gemma 4 (Abstract, Introduction, What Did Not Work, Conclusions, Limitations, plus acum Language models, Regression
  models, TabFM, Baseline, 4.4): orice scurtare trece prin Gemma, un prompt nou `docs/PROMPT_gemma_<sectiune>_vN.txt`. Rulare:
  `HF_HUB_OFFLINE=1 /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python docs/gemma_introducere.py docs/PROMPT_gemma_X.txt <scratchpad>/gemma_X.txt`
  (gemma-4-12B-it-qat-OptiQ-4bit, revizia 63912b88, T 0.7, top-p 0.95, seed 0, gandirea oprita, ~1 minut).
  Prompt: in engleza, textul intre `<<< >>>`, "Facts that must stay true" cu cifrele exact, "Rules" (cel mult N cuvinte, fara em-dash, "we",
  nicio cifra schimbata, `\ref` si `\cite` neschimbate), iar la schimbari mici "Make only this change. Every other sentence stays
  word for word." Pentru scurtari NUMESTE schimbarile (ce propozitii se unesc, ce fapte pot cadea): limita de cuvinte singura nu e
  respectata. Verifici cu script: acelasi set de cifre, aceleasi `\ref` si `\cite`, diferenta pe propozitii, lungimea.
  Pui textul NESCHIMBAT, rupt la ~100 de caractere, cu sursele cifrelor la sfarsit de rand si un comentariu deasupra (model, revizie,
  prompturi, script, seed, data, ce a cazut). Verifici cu script ca textul din .tex, fara comentarii, e identic cu raspunsul lui Gemma.
- Texte ale lui Claude (Related Work, Method, Results): le poti scurta tu, dar intai textul in chat, apoi in .tex dupa OK.
- La final corpul se termina pe pagina 8; Limitations poate incepe pe 8 sau pe 9 (daca e varianta A).

## Compilare si reguli

- Inainte de fiecare scriere: backup al .tex-ului in scratchpad. Conditii: 0 erori, 0 Undefined, 0 `??`, 0 Overfull. Hook-ul rtk poate
  goli iesirea lui `grep -c`; numara in log cu python. Spui cate pagini are documentul si pe ce pagina se termina corpul.
- Daca o figura noua trebuie urcata in Overleaf, spui asta explicit. El urca .tex-ul in Overleaf dupa fiecare grup aprobat.
- Nu atingi paper_full.tex, Paper/documentation_overleaf.tex sau release/. Nu faci git add si nici commit. Fara subagenti; verifici singur.
- In chat: romana, fara diacritice, fara tabele markdown, propozitii scurte. Nu propui nimic necerut si nu rescrii listele lui.

## Deschise, de pus la momentul potrivit

- Anexa B (Tabelul 8): REZOLVAT. Titlul e primul lucru din float, iar figura 4 din anexa A e `figure*` (aceeasi latime), ca figura 4 si tabelul 8 sa
  stea impreuna pe pagina 14, in ordinea anexelor. Fara `\clearpage` (el crea doua pagini separate, cu cate un float in centru). Comentariu in .tex.
- Baseline (4.2): fuziunea metoda + Claude e data pe zece limbi (0.706, 0.724, +0.013), iar restul paragrafului pe unsprezece; pe
  unsprezece sunt 0.713, 0.732, +0.011 (`output/doc_claude.txt`). "below our method by 0.008" pe unsprezece e in zgomot
  (-0.0076 [-0.0176, +0.0020]). TabFM nu are citare in bibliografie.
- Sectiunea 5: el a cerut "mai concret"; nu s-au adaugat cifrele eye-tracking 0.777 fata de 0.770 si few-shot 0.697 fata de 0.641/0.658.
- `\section*{Implementation}` (link-ul anonim, doua randuri) sta intre Conclusions si Limitations: intrebi daca se numara sau unde se muta.
- Anexa: el verifica la curs ca blocurile mutate pot sta acolo.
- Apoi verificarea finala: scos `\nocite{*}`, autori si emailuri.

## La final

Actualizezi primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md` si memoria `cerere-sesiune-documentatie` cu sha-ul nou,
numarul de pagini, pagina pe care se termina corpul si ce ramane.
