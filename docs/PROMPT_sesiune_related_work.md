STARE 11 oct 2026: Related Work e SCRIS si asteapta review-ul lui. Reluarea porneste de la primul bloc din
`docs/PROMPT_sesiune_documentatie_continuare.md`; PDF-urile si uneltele sunt in `docs/papers/related_work/`.

Sesiune noua: scriem sectiunea Related Work din documentatia de curs
`Paper/Articol_Multilingv/documentatie_overleaf.tex`. Doar Related Work. Nu rulam experimente si nu
schimbam celelalte sectiuni.

## Ce citesti intai

- `docs/PROMPT_sesiune_documentatie_continuare.md` (primul bloc, "Unde am ramas") si regulile generale din
  `docs/PROMPT_sesiune_documentatie.md`.
- Memoria: `cerere-sesiune-documentatie`, `noutate-si-precedente-lcp-multilingv` (are corectia din 9 oct:
  TMU-HIT zero-shot isi alege promptul pe trial, deci nu e zero-label; singurul reper publicat fara etichete
  e Archaeology run 1; G-Eval 0.657 e 3-shot; G-Scale cere 30 de etichete ale limbii tinta),
  `model-rals-emnlp-2025`, `rals-rolcp-datele-sunt-ale-lui-nisioi`, `baseline-claude-opus-bate-sistemul`,
  `preferinte-de-scriitura-paper`, `scrie-uman-nu-overexplain`, `lista-utilizatorului-nu-se-reformuleaza`,
  `raspunsuri-fara-diacritice-fara-tabele-md`.
- In .tex: sectiunea Related Work (acum doar comentarii de plan pe patru blocuri, plus notele mutate din
  4.4 in blocul "Systems on the MLSP 2024 data"), apoi Method si Results, ca sa stii ce spunem deja despre
  noi si sa nu repetam.
- Sha-ul .tex-ului la start trebuie sa fie 73a581a3. Daca difera, imi spui intai ce s-a schimbat. Daca am
  editat eu, textul meu ramane cuvant cu cuvant.
- Related Work din RALS (`~/Downloads/2025.emnlp-main.1603.pdf`): forma, lungimea si tonul.
- `docs/instructions_documentation.md`: cursul cere "what other research has been done on this idea" si
  citari, cu un paragraf despre ce face fiecare lucrare.

## Regula principala: nimic fals, nimic inventat

1. Orice afirmatie despre o lucrare (ce face, pe ce date, ce etichete citeste, ce raporteaza) o verifici
   in sesiune, in PDF-ul ei, nu din ce stii. Langa fiecare afirmatie pui un comentariu LaTeX in engleza cu
   sursa: lucrarea, sectiunea sau tabelul, pagina, si data verificarii.
2. PDF-uri locale: RALS (`~/Downloads/2025.emnlp-main.1603.pdf`). Restul le descarci: ACL Anthology (url-ul
   din custom.bib plus `.pdf`), arXiv, sau J-STAGE pentru Nohejl et al. 2025 (doi 10.5715/jnlp.32.1129).
   Le salvezi intr-un director nou din scratchpad si le citesti de acolo.
   `docs/papers/Cross-Lingual Transfer for Romanian Lexical Complexity Prediction.pdf` e lucrarea noastra
   anterioara, doar pe romana. Nu e o sursa externa si nu o citezi ca atare.
3. Daca nu poti verifica o afirmatie, nu o scrii. O treci in chat la "neverificat" si ma intrebi.
4. Citari: doar lucrari care exista. Pentru orice intrare noua in custom.bib verifici titlul, autorii,
   anul, locul si paginile pe aclanthology.org, arxiv.org sau doi.org, si pui deasupra comentariul
   "checked on ..." ca la intrarile existente. Nu inventezi DOI, pagini sau autori. Daca nu gasesti o
   lucrare de care ai avea nevoie, spui asta.
5. Nu pui in gura unei lucrari mai mult decat spune ea ("first", "state of the art", "only"). Nici despre
   noi nu scrii superlative neverificate pe literatura. Claude Opus 5.5 zero-shot e peste noi (0.721 pe 11
   limbi, 0.711 pe 10), deci nu scriem ca suntem cei mai buni fara etichete.
6. Cifre in Related Work: de preferat niciuna. Comparatia numerica e in 4.4 si nu se repeta. Daca o cifra
   e necesara, vine din lucrare, cu tabelul in comentariu.
7. Pentru fiecare sistem pe MLSP 2024 spui exact ce etichete ale limbii evaluate citeste. Notele de
   pornire sunt in comentariul blocului "Systems on the MLSP 2024 data": baseline-ul de frecventa e
   potrivit pe trial; TMU-HIT zero-shot isi alege promptul pe trial; G-Eval isi ia exemplele de pe trial;
   G-Scale e potrivit pe trial; Archaeology run 1 nu citeste nicio eticheta a limbii evaluate. Le
   reverifici pe fiecare in PDF.
8. Atribuire corecta pentru semnalul B: nota asteptata citita din probabilitatile tokenurilor vine din
   G-Eval (Liu et al. 2023). G-Scale (Nohejl et al. 2025) adauga o calibrare pe etichetele limbii tinta.
   Verifici in ambele PDF-uri inainte sa scrii.

## Ce scriem

- Am decis: Related Work descrie ce face fiecare lucrare si ce metoda foloseste. Sectiunea 4.4 da doar
  rezultatele noastre fata de ale lor.
- Planul din comentariile .tex-ului, pe patru blocuri:
  1. Lexical complexity prediction: de la CWI 2018 la CompLex si SemEval 2021, date in alte limbi
     (catalana si spaniola, mandarina si cantoneza), cele 10 limbi MLSP 2024 sub acelasi protocol,
     romana in RALS (RoLCP), review-ul din 2024.
  2. Systems on the MLSP 2024 data: Archaeology, TMU-HIT, G-Eval si G-Scale; plus baseline-ul Claude din
     sectiunea 4.2.
  3. Cross-lingual transfer with frozen encoders: mBERT si XLM-R, inghetat fata de fine-tuning cand lipsesc
     etichetele, LaBSE si mE5, centrarea pe media limbii (Libovicky et al. 2020).
  4. Frequency, morphology and tokenisation: frecventa masurata pe forme flexionate, fertilitatea
     tokenizerului (Rust et al. 2021), stanza.
- Fiecare bloc se incheie cu o fraza: ce lipseste in lucrarile anterioare si ce facem noi altfel, fara sa
  repete Method.
- Forma: ma intrebi la inceput. Ori titluri in bold pe linie proprie (`\subsection*`, ca acum, ca la
  glioma), ori proza fara subtitluri ca in RALS ("Challenges and Related Work", propunerea din 10 oct).
- Lungime: Introduction si Related Work impreuna, maximum 2 pagini. Introduction se scrie in alta
  sesiune, deci Related Work in jur de o pagina. Masori pe PDF-ul compilat.

## Stilul

- Regulile din `preferinte-de-scriitura-paper`: fara em-dash, fara "the system" pentru lucrarea noastra,
  fara deschidere de dictionar, fara aforisme, nicio idee spusa de doua ori, o citare nu apare in doua
  blocuri.
- Propozitii scurte si concrete. Fara deductii inlantuite ("X, and Y, so Z").
- Expresii respinse deja: "To this end", "held out", "unweighted", "neighbouring", "complementary",
  "gold", "on their own".
- Termenii sunt aceiasi ca in Method si Results: signal A, signal B, LOLO, English regressor,
  multilingual regressor, fusion.
- Nu adaugi nimic necerut. Ce crezi ca mai lipseste, semnalezi separat.

## Cum lucram

1. Audit in chat, inainte de orice .tex. Pentru fiecare lucrare pe care vrei s-o citezi: una-doua
   propozitii despre ce face, ce etichete foloseste, si sursa exacta (sectiune, pagina). Plus lucrarile
   noi pe care le-ai adauga, fiecare cu motivul. Eu aprob sau tai.
2. Abia dupa aprobare scrii, bloc cu bloc. Inainte de orice modificare, backup al .tex-ului in scratchpad.
3. Compilezi intr-un director gol din scratchpad (pdflatex, bibtex, pdflatex de doua ori) cu acl.sty si
   acl_natbib.bst din Paper/Articol_Multilingv plus figures/: 0 erori, 0 Undefined, 0 `??`, 0 Overfull. Imi
   spui cate pagini are documentul si cat ocupa Related Work.
4. La final: in chat, lista tuturor afirmatiilor factuale din Related Work, fiecare cu sursa ei, ca s-o pot
   verifica. Apoi scrii `docs/PROMPT_verificare_related_work.md`, pentru o sesiune separata in care un agent
   reciteste PDF-urile si verifica fiecare afirmatie, fara sa vada rationamentul tau.

## Reguli fixe

- Nu atingi paper_full.tex, Paper/documentation_overleaf.tex sau release/. Nu faci git add si nici commit.
- Daca vezi o contradictie intre Related Work si Method sau Results, o semnalezi; nu schimbi singur
  celelalte sectiuni.
- In chat: romana, fara diacritice, fara tabele markdown.
- La final, sau cand ramane putin context, actualizezi memoria `cerere-sesiune-documentatie` si
  `docs/PROMPT_sesiune_documentatie_continuare.md` cu punctul de reluare.

## Context de pastrat, nu e pentru sesiunea asta

- What Did Not Work: RALS nu are o asemenea sectiune; o cere cursul ("a bullet point list of experiments
  tried"). Vreau totusi sa scriem acolo despre eye-tracking. Se decide la pasul 4.
