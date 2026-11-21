## PUNCT DE RELUARE (12 oct, sesiunea 331020c1): Partea 1 FACUTA, Partea 2 NEINCEPUTA

Stare: .tex sha **2b40639c**, bibliografia SEPARATA in `Paper/Articol_Multilingv/documentatie.bib` (sha 7ed34cf6,
`\bibliography{documentatie}`), 37 intrari, toate citate. Compilat curat (0 erori/Undefined/Overfull, 0 avertismente
bibtex), 14 pagini, Conclusions incepe pe p8. AMBELE urcate de el in Overleaf. Nimic comis. Copii de siguranta in
scratchpad-ul sesiunii 331020c1 (`documentatie_overleaf_7e2b1786.tex`, `_70e8d254.tex`).

Facut azi:
- Metadatele tuturor intrarilor verificate la sursa (ACL Anthology .bib, Crossref, export.arxiv.org, jmlr.org,
  NeurIPS, Zenodo): toate corecte. wordfreq: citam v3.0 (ultima pe Zenodo), am rulat 3.1.1; lasat asa (RALS il
  citeaza la fel, "Speer, 2022").
- Citarile din Introduction si Related Work verificate pe PDF-uri (`docs/papers/related_work/paged/`): sustin fraza.
- ADAUGATE (cerute de el): MultiLS (Shardlow et al. 2024, READI, `shardlow-etal-2024-extensible`) langa BEA si
  CompLex 2.0 (Shardlow, Evans, Zampieri 2022, LRE, `shardlow-etal-2022-predicting`) langa SemEval 2021, in Data
  (1) si (3) si in Data Sharing.
- `\nocite{*}` SCOS. Blocul `filecontents` SCOS; numele nu e custom.bib fiindca paper_full*.tex si copia de
  dinainte de scurtare din acelasi director inca scriu custom.bib cu `[overwrite]`. Intrarile noi se pun in documentatie.bib.
- Comentariile de proces SCOASE din .tex (cerut: "doar chestii concrete, le citeste si profesorul"): cine a
  cerut ce, date de editare, ce s-a mutat/taiat, bak/, sesiuni, STEP, glioma, Glosperx/~/lcp-anon. 364 -> 227
  randuri de comentariu, textul PDF identic. Pastrate: sursele cifrelor, notele de layout, "Text by Gemma 4 12B
  ... Inserted unchanged" scurtat la 1-2 randuri. Corectat un comentariu fals (Tabelul 10: corelatiile dintre
  modele NU mai sunt in text).

Refuzate de el: citare la XGBoost in Related Work si la wordfreq in corp ("nu sunt necesare").

Raman deschise din Partea 1 (propuse, fara raspuns):
- [.tex:221] Nohejl "relatively uncorrelated" e gasit doar pe en/ja/es (Tabelul 12; Anexa H: frecventa strica
  pe 3 din 10 limbi); propus "on English, Japanese and Spanish".
- Lundberg 2017: pagini 4765--4774 dar LightGBM (acelasi volum NeurIPS 30) fara; URL `papers.nips.cc/paper/7062-a`
  trunchiat. Propus: fara pagini + URL proceedings.neurips.cc complet.
- [.tex:311] `pedregosa-etal-2011-scikit` sta dupa HGB; daca ridge e tot sklearn, sa acopere si ridge.
- Libovicky "as in" poate citi ca si cum ei numesc centrarea "domain adaptation" (minor).
- Claude: presa spune ca Opus 5.5 are system card (22 sep 2026), neverificat pe anthropic.com; Sonnet 5.5 nimic.
  Recomandat `@misc` doar daca se gaseste oficial. gorman-bedrick: recomandat la fraza cu bootstrap-ul pereche.
- Comentariile "Text by Gemma 4": pastrate; intrebat daca le vrea scoase (profesorul le-ar vedea). Fara raspuns.
- Blocul comentat al sablonului cu 20 de autori fictivi: oferit sa-l scot, fara raspuns.

URMEAZA: Partea 2 (greseli de scriere si forma), lista de mai jos neschimbata.

---

Sesiune de AUDIT pe `Paper/Articol_Multilingv/documentatie_overleaf.tex` (documentatia de curs, paper in stil RALS, EMNLP 2025).
Context: `docs/PROMPT_sesiune_documentatie_continuare.md` (blocul de sus). Aici nu scriem text nou si nu rulam experimente:
doar verificam si raportam. Nu modifici .tex-ul fara OK-ul lui; mai intai lista gasirilor in chat, apoi aplici ce zice el.

Stare la start: .tex sha **4ff7c0a6**, compilat curat (0 erori/Undefined/Overfull/??), 14 pagini, corpul pana la Conclusions pe p8.
Nimic comis. Compilare: director gol in scratchpad, .tex + acl.sty + acl_natbib.bst + figures/, pdflatex, bibtex, pdflatex x2.
Bibliografia sta in blocul `filecontents*{custom.bib}` din .tex (fara Unicode, acronime in `{}`).

## Partea 1: References

1. Cheile: fiecare `\cite*` din corp are intrare in bib; fiecare intrare e citata. Acum: 35 intrari, 35 citate, 0 lipsa (verificat cu script).
2. Fiecare intrare fata de SURSA, nu din memorie: titlu, autori (lista completa sau primii 5 + others, ca in restul bib-ului),
   an, venue, pagini, DOI/URL. Surse: ACL Anthology, Crossref, arXiv (`export.arxiv.org`, cu https), pagina oficiala. Intrarile
   adaugate pe 12 oct au deja in comentariu sursa (pedregosa, ke, chen-guestrin, prokhorenkova, geurts, breiman, hu-lora,
   grattafiori-llama3, dang-aya, qwen-team-qwen35, kong-tabfm); celelalte (RALS, MLSP, CompLex, TMU-HIT, G-Eval, G-Scale, Stanza,
   wordfreq, XLM-R, mE5, Gemma 4, Qwen3 etc.) de reverificat.
3. Fiecare citare din text sustine ce se afirma acolo: pentru fiecare `\cite` citesti propozitia si verifici in PDF-ul sursei.
   Sursele Related Work sunt in `docs/papers/related_work/` (cele 21 de PDF-uri, textul pe pagini in `paged/`, `q.py`).
   Frazele comprimate la scurtare NU au trecut prin verificarea pe PDF-uri (vezi lista din continuare, "Next steps" pct. 2).
4. Stilul intrarilor: aceeasi forma pentru acelasi tip (arXiv ca `journal = {Computing Research Repository}, volume = {arXiv:...}`),
   fara intrari duble, majuscule protejate (`{BERT}`, `{TabFM}`), `others` consecvent.
5. De decis cu el, nu de aplicat singur:
   - **TabFM**: paperul (Kong et al., arXiv:2609.37959) descrie checkpoint-ul 1.1.0 (400M, E=128); noi am rulat
     `google/tabfm-1.0.0-pytorch` (1.65 mld de parametri, E=256); textul spune acum "TabFM 1.0.0" in Anexa B. De confirmat ca e ok.
   - **Claude Opus/Sonnet 5.5**: nu au citare (nu exista paper); de decis daca e nevoie de un `@misc`.
   - `\nocite{*}` (randul ~1390) INCA activ: cat timp e acolo, References arata toata bibliografia, nu doar ce e citat.
     Se scoate la verificarea finala (pasul 8), dupa acest audit.
   - `gorman-bedrick-2019-need` scos din bib (necitat). Poate fi pusa la fraza din Anexa A "To see whether a difference ... is
     larger than chance" (bootstrap pereche); NU la "we chose the reported version based on the test scores" (nu sustine asta).
6. Decizii deja luate, nu se redeschid: Pires, Peters, Wu si Dredze, Liu 2021 scoase din bib (paragraful din Related Work scos de
   el); TreeSHAP citat la fraza SHAP din 4.1 (`\citep{lundberg-lee-2017-unified,lundberg-etal-2020-trees}`).

## Partea 2: greseli de scriere si de forma

Exemplul care a declansat-o: `\texttt{1}` si `\texttt{5}` in corp dadeau alt font doar acolo (scos pe 12 oct; era singurul `\texttt`
din corp). Caut aceeasi clasa de lucruri, in corp si in anexe:

- font sau stil schimbat fara motiv (`\texttt`, `\textbf`, `\emph`, `\textit`, `\mbox`), `\emph` consecvent pe numele celor patru trasaturi;
- scriere neuniforma a acelorasi lucruri: "signal A"/"Signal A", "Gemma 4"/"Gemma~4", "Qwen3.5"/"Qwen3", "leave-one-language-out"/"LOLO",
  "eleven"/"11", "centring"/"centering" (stil britanic ales: "centre", "standardise", "quantised"), "labelled"/"labeled";
- numere: zecimale (3 cifre), minus ca `$-$` sau `−`, separator de mii `{,}`, intervale "0.679 to 0.706" fata de "[0.679, 0.706]";
- ghilimele (` `` '' `), cratime/liniute (fara em-dash, regula lui), spatii nerupte `~` inainte de `\ref`/`\cite`/numere;
- trimiteri: "Section~\ref", "Table~\ref", "Appendix~\ref"; trimiteri care duc la ceva mutat in anexa; "Table 8 (Appendix B)" etc.;
- caption-uri: punct la final, un singur subiect, fara "Bold marks ..." in afara Tabelului 8;
- gramatica si fraze stangace, in special in textul scris de Gemma 4 (pus neschimbat, la cererea lui): se SEMNALEAZA, nu se corecteaza.
  Deja semnalate si nerezolvate: "lexical complexity prediction" scris complet de doua ori in Introduction; "its settings" ambiguu;
  "a generally low level of reading proficiency" in loc de "limited"; "using zero-shot prompt" in Abstract (fara articol, singular);
  "This was against 0.551" in bulina de fine-tuning; "do not include any other languages" ambiguu fata de MultiplEYE;
- fraze din text care contrazic cifre din tabele (se verifica cu comentariile de sursa de pe fiecare rand, nu din memorie).

Regula lui: frazele si listele lui raman cuvant cu cuvant; textul de la Gemma 4 se pune neschimbat; fara em-dash, fara "the system",
fara cadru de competitie. Raspunsurile catre el: fara diacritice, fara tabele markdown, scurt, fara agenti multipli (tokeni).

## Iesire

O lista in chat, grupata pe categorii (References / forma / gramatica), cu `fisier:rand`, ce e acum, ce propui si de ce.
Apoi aplici doar ce aproba el, recompilezi curat, dai noul sha1 si spui ca trebuie urcat in Overleaf.
