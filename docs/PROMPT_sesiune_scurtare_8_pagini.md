Continuam documentatia de curs din `Paper/Articol_Multilingv/documentatie_overleaf.tex` (titlu: "Lexical Complexity
Prediction Without Target-Language Labels", sablon ACL). Toate sectiunile sunt scrise si acceptate. Experimentele sunt
gata. Nu rulam experimente noi si nu schimbam nicio cifra.

In sesiunea asta scurtam corpul documentului la 8 pagini. Pas cu pas, cu aprobarea mea inainte de fiecare schimbare.

## Ce se numara

- Se numara corpul: de la titlu si Abstract pana la sfarsitul lui Conclusions.
- NU se numara: Limitations, Acknowledgments, bibliografia, anexele (regula ACL/ARR). Daca regula cursului difera,
  conteaza cea a cursului; eu verific asta, tu nu presupui altceva.
- `\section*{Implementation}` (link-ul anonim, doua randuri) sta acum intre Conclusions si Limitations. Intrebi la
  pasul 2 daca se numara sau unde se muta.

## Starea

- .tex sha **bc856e97** (verifici cu `shasum`). Daca sha-ul difera, intrebi inainte sa faci orice: poate am editat in
  Overleaf.
- 15 pagini in total. Corpul se termina pe pagina **12** (Conclusions si Limitations pe 12). Deci trebuie taiate ~4
  pagini de corp.
- Harta de acum (pagina de start, din .aux): Introduction p1, Related Work p1, Method p2 (Data p2, Signal A p3, Signal B
  p4, Fusion p5, Evaluation Protocol p5), Experimental Results p6 (Signal A p6, Signal B p9, Fusion p10, Comparison with
  Published Results p11), What Did Not Work p11, Conclusions p12. Results ocupa ~5.5 pagini, Method ~3.5.
- Floats in corp: Fig. 1 pipeline (figure*, `fig_pipeline_doc_vertical.pdf` la 0.77\textwidth), Fig. 2 t-SNE
  (figure*), Fig. 3 SHAP (figure*, 0.7\textwidth), 7 tabele `table` (tab:signal-a, tab:signal-a-models, tab:ablations,
  tab:llms, tab:signal-b, tab:per-language, tab:corr-ab) si un `table*` (tab:published). Anexa A: SHAP pe toate
  intrarile.
- `\nocite{*}` e inca in fisier. Lungeste doar bibliografia, nu corpul. Se scoate la verificarea finala, nu aici
  (decat daca iti cer).
- Starea completa: primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md`.

## Ce citesti intai

1. Memoriile: `cerere-sesiune-documentatie`, `text-final-rescris-de-gemma`, `preferinte-de-scriitura-paper`,
   `scrie-uman-nu-overexplain`, `lista-utilizatorului-nu-se-reformuleaza`, `fara-agenti-multipli-tokeni`,
   `model-rals-emnlp-2025`, `tabele-un-subiect-pe-tabel`, `grafice-shap-native-nu-custom`, `diagrama-pipeline-drawio`,
   `raspunsuri-fara-diacritice-fara-tabele-md`.
2. Tot .tex-ul, cu comentariile de provenienta de deasupra fiecarei sectiuni (cine a scris textul: eu sau Gemma 4).
3. RALS (`~/Downloads/2025.emnlp-main.1603.pdf`), doar ca reper: ce tine in corp si ce muta in anexe (detalii de
   pipeline, matematica, promptul verbatim).

## Constrangeri deja decise (nu le redeschizi fara sa intrebi)

- Cursul cere pasii metodei explicati in corp (Method ramane cu pasii 1-8) si sectiunea What Did Not Work in corp.
  Mutarea lui What Did Not Work in Limitations a fost respinsa. In anexa: doar daca o confirm eu cu cursul.
- Figurile din corp sunt alese de mine: pipeline, SHAP, t-SNE-ul principal. Le poti propune pentru anexa, cu
  castigul estimat, dar decid eu.
- Pentru pipeline exista deja varianta orizontala, mai joasa: `docs/pipeline.drawio` -> `figures/fig_pipeline_doc.pdf`,
  la `width=\textwidth` (comentariul de langa figura spune asta). Am ales verticala pe 10 oct; poti propune schimbul.
- Un subiect pe tabel. Bold pe rezultatul nostru.
- Fara trucuri de layout interzise de sablon: fara `\vspace` negativ, fara font sau margini schimbate, fara
  `\small` pe text. In tabele, `\small` si `\tabcolsep` sunt deja folosite.

## Cine are voie sa schimbe ce text

- Abstract, Introduction, What Did Not Work, Conclusions, Limitations au textul final scris de Gemma 4. Orice
  reformulare sau scurtare trece prin Gemma: prompt nou `docs/PROMPT_gemma_<sectiune>_vN.txt`, pornind de la textul din
  .tex, cu "Make only this change. Every other sentence stays word for word." (procedura si comanda in
  `docs/PROMPT_sesiune_limitations.md`, Pasul 3). Stergerea unei fraze intregi: intrebi daca o fac direct sau prin
  Gemma.
- Related Work, Method, Experimental Results, Implementation: scrise de Claude si acceptate de mine. Le poti scurta
  tu, dar doar dupa ce aprob planul.
- Mutarea unui bloc in anexa (tabel, paragraf, figura) se face cuvant cu cuvant. Se schimba doar trimiterile
  ("Appendix B"), iar mutarea se noteaza intr-un comentariu.
- Cifrele nu se schimba. Comentariile de sursa raman langa fraza lor, si cand fraza se muta.

## Pasul 1: Masurare (fara nicio scriere in .tex)

- Faci harta exacta: cat ocupa fiecare sectiune, subsectiune, tabel si figura, in coloane sau fractiuni de pagina.
- Pentru fiecare candidat de taiere, il masori, nu il ghicesti: compilezi o copie din scratchpad fara blocul respectiv
  si vezi unde se termina Conclusions (pagina si pozitia, de ex. cu `pdftotext -bbox` pe ultimul cuvant din
  Conclusions). Floats-urile se muta la compilare, deci castigul real poate fi diferit de marimea blocului.
- Cauti si repetitiile dintre sectiuni (aceeasi idee in Method si in Results, sau in Results si Conclusions): sunt
  taieri fara pierdere de continut.

## Pasul 2: Lista in chat

Imi dai lista de optiuni, fiecare cu: ce se muta sau se taie, unde (fisier si linie), castigul masurat, si ce se pierde
din corp. Grupate in: (a) mutari in anexa, (b) taieri de repetitii, (c) layout (pozitia float-urilor, figura
orizontala, `table*` vs `table`). Spui care combinatie ajunge la 8 pagini cu cele mai putine pierderi. Eu aleg.

## Pasul 3: Aplicare

- O schimbare (sau un grup aprobat) o data. Dupa fiecare: compilare, pagina pe care se termina corpul.
- Textele scurtate de tine: intai in chat, apoi in .tex dupa OK-ul meu. Textele lui Gemma: prin Gemma, ca mai sus.
- La final corpul se termina pe pagina 8, iar Limitations poate incepe pe 8 sau pe 9.

## Compilare si reguli

- Inainte de fiecare scriere: backup al .tex-ului in scratchpad. Compilezi intr-un director gol din scratchpad
  (.tex + acl.sty + acl_natbib.bst + figures/ din `Paper/Articol_Multilingv/`, pdflatex, bibtex, pdflatex de doua ori;
  daca logul zice "Label(s) may have changed", inca o trecere). Conditii: 0 erori, 0 Undefined, 0 `??`, 0 Overfull.
  Atentie: hook-ul rtk poate goli iesirea lui `grep -c`; numara in log cu python. Spui cate pagini are documentul si pe
  ce pagina se termina corpul.
- Daca o figura noua trebuie urcata in Overleaf, spui asta explicit.
- Nu atingi paper_full.tex, Paper/documentation_overleaf.tex sau release/. Nu faci git add si nici commit.
- Fara subagenti; verifici singur, cu grep si scripturi.
- In chat: romana, fara diacritice, fara tabele markdown, propozitii scurte.
- La final actualizezi primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md` si memoria
  `cerere-sesiune-documentatie`, cu sha-ul nou, numarul de pagini si ce ramane (verificarea finala cu scoaterea lui
  `\nocite{*}`, autori si emailuri).
