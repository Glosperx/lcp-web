Scriem Introduction (sectiunea 1) din documentatia de curs `Paper/Articol_Multilingv/documentatie_overleaf.tex`.
Experimentele sunt gata, Related Work e acceptat, documentatia e urcata in Overleaf. In sesiunea asta scriem
doar introducerea. Nu rulam experimente si nu atingem alte sectiuni.

Titlul lucrarii: "Lexical Complexity Prediction Without Target-Language Labels". Sectiunea 1 e acum goala,
are doar un comentariu-schelet (STEP 5). Abstractul e tot gol, se scrie la final (pasul 7), nu acum.

## Ce citesti intai

1. Memoriile: `intro-style-hgs`, `model-rals-emnlp-2025`, `preferinte-de-scriitura-paper`,
   `scrie-uman-nu-overexplain`, `lista-utilizatorului-nu-se-reformuleaza`, `fara-agenti-multipli-tokeni`,
   `cerere-sesiune-documentatie`, `noutate-si-precedente-lcp-multilingv`, `baseline-claude-opus-bate-sistemul`.
2. Tutorialul de introducere cerut de coordonator: https://www.cs.columbia.edu/~hgs/etc/intro-style.html
   (il citesti cu WebFetch, integral).
3. Paperul model, RALS (Anghel et al., EMNLP 2025): `~/Downloads/2025.emnlp-main.1603.pdf`, paginile 1-2
   (`pdftotext -f 1 -l 2 -layout`). Te uiti la introducere si la cum se leaga de "Challenges and Related Work".
4. Cerintele cursului pentru Introduction: `docs/instructions_documentation.md`, liniile 52-64.
5. Din .tex: comentariul-schelet din `\section{Introduction}`, Related Work intreg (ca sa nu repeti nimic din
   el), Method pe scurt, 4.4 "Comparison with Published Results" (Tabelul `tab:published`) si comentariile
   din Limitations.
6. Doar pentru argument, fara nicio cifra: introducerea din `Paper/Articol_Multilingv/paper_full.tex`
   (linia ~650, draftul din 19 sep, cifrele lui sunt vechi) si `Paper/Articol_Complexity/paste_intro.tex`
   (deschiderea acceptata de el in iulie, pe alt paper).

## Structura

Se combina trei surse. Ghidul hgs da ordinea paragrafelor, RALS da tonul si lungimea, cursul da punctele
care trebuie bifate. Maparea propusa:

- P1, motivatia (hgs P1, ca primele doua paragrafe din RALS): o afirmatie concreta despre vocabular, cine e
  afectat, numele sarcinii (lexical complexity prediction) si ce permite. Aici intra si "why we chose this
  project", cerut de curs, spus ca miza, nu ca poveste personala.
- P2, problema (hgs P2, ca paragraful 3 din RALS): etichetele de complexitate exista in putine limbi; MLSP 2024
  da 30 de instante etichetate pe limba; fara etichete in limba tinta nu ai pe ce antrena si nici cu ce alege
  componentele.
- P3, ce propunem (cursul: "a summary of the approach"; RALS: "In this paper, we address..."): semnalul A
  (encodere inghetate plus trasaturi, regresor), semnalul B (un LLM cu greutati publice, probabilitatile notelor),
  fuziunea, totul ales pe celelalte limbi (LOLO).
- P4, contributiile (hgs P3, paragraful cheie): fiecare o revendicare plus cel mult cifra de titlu.
- P5, diferenta fata de lucrarile anterioare (hgs P4), la nivel inalt, cu trimitere la Sectiunea 2. Fara sa
  repeti ce spune Related Work.
- P6, organizarea (hgs P5): dupa continut, nu "In Section 2..., In Section 3...". Aici intra o fraza care trimite
  la sectiunea "What Did Not Work" (cursul cere "a bullet point list of experiments tried").

RALS nu are contributii numerotate si nici roadmap. Tutorialul le cere, deci raman (decis in iulie).

## Intrebi la inceput, inainte sa scrii (sunt decizia lui)

1. Contributiile: buline ca in paperul de glioma (asa scrie comentariul-schelet) sau paragraf narativ cu
   First/Second/Third (memoria `preferinte-de-scriitura-paper`, ca in RALS)? Cele doua se contrazic, iar regula
   din `docs/PROMPT_sesiune_documentatie.md` e sa intrebi.
2. Lista de experimente ceruta de curs: o fraza in intro care trimite la "What Did Not Work" (asa scrie
   comentariul-schelet) sau lista cu buline chiar in intro?

## Cifre si ce ai voie sa revendici

- Cifra de titlu: 0.692521 pe 11 limbi (.693 in tabele). Pe cele zece limbi MLSP: 0.689745 (.690). Intervalul de
  incredere il iei din .tex sau din `output/`, nu il recalculezi. Langa fiecare cifra, comentariu LaTeX cu sursa.
- Nu se citeaza: 0.674946, 0.683849, 0.690001, 0.692527, 0.693718, 0.687831.
- Comparatia permisa: cea mai mare medie publicata pe MLSP 2024 e G-Scale, 0.669, care citeste 30 de etichete
  din fiecare limba; noi 0.690 cu zero. Spui si cate etichete, altfel comparatia induce in eroare.
- NU scrii ca suntem cei mai buni in general: Claude Opus 5.5 zero-shot e peste noi (.721 pe 11 limbi, .711 pe
  10), si asta e deja in sectiunea 4.2.
- "Zero-label" se spune precis: la LOLO, nicio eticheta a limbii de test nu intra in antrenare sau in alegerea
  setarilor. NU scrii ca nicio alegere n-a vazut vreodata etichete: lista scurta de LLM-uri a fost comparata pe
  trial-ul celor zece limbi, iar al treilea prompt a fost ales in dezvoltare cu scorurile de test la vedere
  (vezi comentariul din capul lui Related Work si Limitations).
- Fara "who did what": decis pe 8 oct, nu apare nicaieri in documentatie.

## Stil

- Regulile din `preferinte-de-scriitura-paper`: fara em-dash, fara deschidere de tip definitie de dictionar,
  fara aforisme, fara "the system" pentru lucrarea noastra, fara formule in intro, nicio idee spusa de doua
  ori, nimic adaugat necerut, fara cadru de competitie sau de tema de facultate. Propozitii scurte si concrete.
- Din tutorial: fara "ce nu face lucrarea", o propozitie-tema la inceputul fiecarui paragraf, aceleasi timpuri
  verbale in interiorul unui paragraf.
- Citari: cel mult cate trebuie pentru motivatie. Nu repeti in intro o afirmatie din Related Work; daca o citare
  apare si acolo, verifici ca nu spune acelasi lucru.
- Lungime: Introduction plus Related Work cel mult 2 pagini. Related Work are ~400 de cuvinte, deci intro tinta
  ~450-550 de cuvinte. Masori cu abstractul gol in build si spui asta cand dai numarul de pagini.
- Reformularile lui le pui cuvant cu cuvant. Daca vezi o problema, o semnalezi separat.

## Pasii sesiunii

1. Verifici sha-ul .tex-ului (trebuie sa fie 1bc24478, versiunea urcata in Overleaf). Daca difera, intrebi.
2. Citesti ce e mai sus.
3. Pui cele doua intrebari.
4. Dai in chat planul: o linie pe paragraf, ce spune si ce cifra sau citare are. Astepti OK-ul lui.
5. Dupa OK: backup al .tex-ului in scratchpad, scrii introducerea in .tex cu comentariile de sursa, compilezi
   intr-un director gol din scratchpad (.tex + acl.sty + acl_natbib.bst + figures/, pdflatex, bibtex, pdflatex
   de doua ori). Conditii: 0 erori, 0 Undefined, 0 `??`, 0 Overfull. Spui cate pagini are documentul si cat
   ocupa Introduction plus Related Work.
6. El revizuieste fraza cu fraza. Aplici exact ce cere.
7. La final actualizezi primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md` si memoria
   `cerere-sesiune-documentatie`, cu sha-ul nou si ce ramane.

## Reguli

- Nu atingi paper_full.tex, Paper/documentation_overleaf.tex sau release/. Nu faci git add si nici commit.
- Fara subagenti; verifici singur, cu grep.
- In chat: romana, fara diacritice, fara tabele markdown, propozitii scurte.
- Dupa introducere urmeaza, in alte sesiuni: verificarea scurta a frazelor reformulate din Related Work, cele
  patru puncte Claude deschise, What Did Not Work, apoi pasii 6-9 (vezi
  `docs/PROMPT_sesiune_documentatie_continuare.md`).
