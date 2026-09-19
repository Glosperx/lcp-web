# Care fișier e care

| Fișier | Ce e | Se editează? |
|---|---|---|
| `paper_full.tex` | **Masterul.** Lucrarea completă plus tot istoricul deciziilor, în comentarii | **Da**, aici se editează |
| `paper_full_copy-paste.tex` | **Derivat.** Același conținut, fără blocul de comentariu din cap și fără comentariile în română. Ăsta se lipește în Overleaf | **Nu.** Se regenerează, altfel modificările se pierd |
| `make_copypaste.py` | Generatorul celui de-al doilea din primul | — |

Regenerare:

```bash
python3 make_copypaste.py paper_full.tex paper_full_copy-paste.tex
```

Scriptul păstrează comentariile proprii ale template-ului ACL, cele în engleză, și scoate
doar blocurile noastre. Are o plasă de siguranță: la final compară liniile de cod ale celor
două fișiere și **pică** dacă diferă cu un caracter, deci nu se poate pierde conținut. Verificat
la generare: 1077 de linii de cod identice, iar cele două `.aux` au aceleași etichete, aceleași
numere și aceleași pagini, adică se compun identic.

# `paper_full.tex` — lucrarea completă

**Acesta e masterul.** Un singur fișier autonom, template-ul ACL cu textul nostru
în el de la abstract la Limitations: 1 Introduction, 2 Related Work, 3 Approach (3.5 What
was tuned), 4 Results, 5 What Did Not Work, 6 Conclusions, apoi Limitations și
Acknowledgments nenumerotate. Bibliografia vine cu fișierul, într-un bloc
`filecontents*[overwrite]{custom.bib}` cu 25 de intrări (7 ale template-ului, necitate dar
inofensive, plus cele 18 ale lucrării). Proiectul Overleaf nu are nevoie decât de `acl.sty`
și `acl_natbib.bst`, care vin cu template-ul, plus un folder `figures/` cu **două** PNG-uri
din `report/figures/`: `beeswarm.png` și `fig_corr_matrix.png`.

Asamblat pe 30 iulie 2026 din `intro_preview.tex` (părțile verbatim ale template-ului și
Secțiunile 1–2) plus `paste_body.tex` și `paste_limitations.tex`, ambele aduse la
convențiile introducerii: em-dash scos integral din proză (29 + 9 locuri), expresia
interzisă „the system" scoasă din toate cele 8 locuri, cadrul de competiție scos din
revendicări („the public evaluation score", nu „leaderboard"; „released with the data", nu
„supplied by the shared task"). Divulgarea din 3.5 și din Limitations a rămas integrală:
s-a schimbat încadrarea, nu faptul că cele cinci cantități au fost alese pe scorul public.
Lista completă a schimbărilor e în blocul de comentariu din capul fișierului, împreună cu
cele trei lucruri de rezolvat înainte de submisie.

Două decizii de conținut, luate în aceeași trecere:

- **`fig_confusion.png` scoasă.** Codul care o generează
  (`make_report_figures.py:93-121`) antrenează pe CompLex EN train+trial și testează pe
  CompLex EN test, adică engleză → engleză, monolingv, deși captionul o numea „In-source
  check", iar 3.2 definește in-source ca transfer între seturi de limbi sursă diferite. În
  plus matricea conține strict mai puțină informație decât `r = 0.753` din titlul ei
  propriu, pentru că se obține digitizând ambele axe la tertilele din train. Numărul a fost
  recuperat în 3.2, lângă `0.515`, unde contrastul dintre cele două cuantifică costul
  trecerii între limbi.
- **Tabel de p-value pentru matricea de corelații: cerut, calculat, respins.** La
  n = 1587, |r| critic pentru p < 0.05 e **0.0492**, iar toate cele zece celule îl
  depășesc; cea mai mică, B × C = 0.07, dă p = 5.3e-3 și trece la limită și de Bonferroni
  pe 10 teste (critic 0.0704). Tabelul ar fi fost zece rânduri constante și ar fi sugerat
  că perechea pe care lucrarea o numește „near-independent" e semnificativ corelată. Ar fi
  avut și precizie falsă, pentru că cele 78 de cuvinte fără gaze primesc mediana înainte de
  corelație (`fill()` din `solutie_finala.py:140`), ceea ce umflă df-ul efectiv pe toate
  rândurile cu D. În loc de tabel, captionul lui `fig:corr` declară acum `n` și mută
  cititorul pe varianța comună: 83% între A și frecvență, 0.5% între B și C.

## Plasarea floats-urilor

`paste_body.tex` declara toate cele 7 floats **în bloc**, la sfârșitul subsecțiunii 4.4,
deși cinci dintre ele sunt referite prima dată încă în Secțiunea 3. LaTeX le acumula și
ajungea să dedice coloane întregi doar lor: în prima versiune a lui `paper_full.tex`,
coloana din dreapta a paginii 5 conținea doar cele două figuri, cu ~1.2 inch de alb elastic
între ele și niciun rând de text.

Reparat pe 30 iulie 2026, în două pași:

1. Fiecare float e declarat acum înaintea titlului care urmează primei lui referințe:
   `tab:pca` înainte de 3.4, `tab:signals` înainte de 3.5, `tab:ablation` înainte de
   Secțiunea 4, `tab:ro14` înainte de paragraful cu scope condition, `fig:beeswarm` înainte
   de 4.3, `fig:corr` înainte de 4.4. `tab:fail` e singurul lăsat pe loc, pentru că
   discuția lui e în Secțiunea 5, unde e și declarat.
2. Patru `\renewcommand` în preambul, lângă `\graphicspath`: `topfraction` 0.9,
   `bottomfraction` 0.5, `textfraction` 0.08, `floatpagefraction` 0.8. Implicit LaTeX
   refuză să pună text în aceeași coloană cu floats care depășesc 70% din ea.

Rezultat, verificat la compilare: nicio coloană numai-floats, fiecare figură și fiecare
tabel are text sub el.

**Cropul PNG-urilor a fost verificat și nu ajută.** `tight_layout` a strâns deja marginile:
bounding box-ul real al lui `beeswarm.png` e 1093×614 din 1122×643, iar al lui
`fig_corr_matrix.png` e 827×700 din 900×750. Cropul recuperează ~2% și la matricea de
corelații ar înrăutăți raportul, pentru că marginea e mai lată pe stânga decât sus.

## Curățare de spațiu, 30 iulie 2026

Întrebarea de la care a pornit era dacă trebuie tăiat conținut ca să încapă în 8 pagini.
**Nu trebuia**, iar acum e și mai clar: conținutul numărat se termină pe pagina 6.
[formatting.md:21](formatting.md#L21) limitează doar figurile și tabelele din textul
principal; Limitations, References și apendicele nu intră.

**PDF-ul a ajuns de la 9 la 8 pagini**, fără să se piardă nicio cifră și nicio revendicare.
Trei schimbări:

1. **`\section*{Acknowledgments}` scos.** [formatting.md:244](formatting.md#L244): „Do not
   include this section in the review version." Obligatoriu, nu economie de spațiu. În loc a
   rămas un comentariu care spune că trebuie repus la camera-ready, exact acolo, pentru că
   [formatting.md:242](formatting.md#L242) cere secțiunea imediat înaintea referințelor.
2. **Apendicele de exemplu scos, fără înlocuitor.** Lucrarea nu are apendice.
3. **Cinci duplicări verbatim, scoase.** Patru între proză și captions: fraza despre `+0.84`
   din 3.5 (daggerul din captionul lui `tab:ablation` o spune, lipit de cifră), aritmetica
   `(69.74-41.76)/69.74 ≈ 40%` din captionul lui `tab:ablation` (4.1 o spune, e teza
   paragrafului), clauza „SHAP describes the fitted model and does not choose the weights"
   din 4.3 (captionul lui `tab:signals` o spune), și trimiterea circulară din 4.2 către 3.5.
   A cincea, în Limitations: paragraful despre cele 14 exemple repeta verbatim din 4.2 clauza
   „surprisal was never computed for them and only two carry eye-tracking". Scoasă acolo,
   păstrată în 4.2.

### Drumul parcurs, ca să nu se repete

`tab:pca` a fost între timp mutat în apendice, ca să elibereze ~1/4 de pagină de conținut, ceea
ce [formatting.md:283](formatting.md#L283) chiar încurajează pentru „tables that are not
critical to the reading and understanding of the paper". A funcționat la limita de pagini, dar
**arăta rău**: singur după cele 18 referințe, tabelul ocupa o pagină întreagă cu 14 rânduri de
text. Adus înapoi în 3.3, cu costul celei 1/4 de pagină.

După întoarcere mai treceau trei rânduri de bibliografie pe pagina 9. Recuperate de a cincea
duplicare, cea din Limitations. Tăietura de acolo nu ajută la limita de conținut, dar scurtează
PDF-ul, și era oricum o repetare verbatim.

Nu s-au atins: repetarea lui `69.74` / `+4.09` / `0.913` între abstract, introducere,
rezultate și concluzii, care e structura normală a unei lucrări; procentele `11.7%` / `36.0%`
din introducere și 3.3 (A); Figura 2 și captionul ei.

## Citarea RALS și titlul, 30 iulie 2026

Coordonatorul a confirmat că setul de test trebuie citat și că titlul trebuie pus. Citarea
**nu a fost o linie în bibliografie**: cinci afirmații din text devin false sau contradictorii
în momentul în care RALS e citată. Toate cifrele de mai jos sunt verificate în PDF-ul lor,
[aclanthology.org/2025.emnlp-main.1603](https://aclanthology.org/2025.emnlp-main.1603/), nu în
notițe.

### Ce spune RALS, cu locul din lucrare

| Fapt | Unde |
|---|---|
| Setul nostru de test **este RoLCP**, exact: 1.587 de mostre, 274 de propoziții, fiecare cuvânt notat de 10 adnotatori dintr-un grup de 80; texte din Wikipedia, popular science, literatură, documente instituționale, eseuri argumentative | Tabelul 1 și §3.1, p. 31483 |
| Licența: **CC BY-NC-SA 4.0** | Limitations, p. 31486 |
| **Etichetele sunt publice**, `github.com/senisioi/RALS` | nota 1, p. 31481 |
| Statisticile etichetelor RoLCP: medie **0.23**, std **0.23** | Tabelul 1 |
| Baseline supervizat pe **exact setul nostru**: Ridge cu trăsături handcrafted, 10-fold CV grupat, **`r = 0.71 ± .05`** | Tabelul 2, p. 31484 |
| Corelația Zipf–complexitate: **−0.53** pentru română față de **−0.74** pentru engleză, adnotate după aceleași ghiduri | §3.1, p. 31483 |
| Concluzia lor: *„cross-lingual transfer of complexity scores is not a viable resource creation procedure, causing distribution shifts"* | §5, p. 31485 |

### Cele cinci afirmații reparate

1. **2.1, prima frază.** „Romanian is **not among them**" era fals. RALS publică 3.921 de mostre
   adnotate pentru română.
2. **2.1, final.** „Romanian appears in **none** of these resources" restrâns explicit la
   resursele multilingve inventariate, unde rămâne adevărat.
3. **3.1.** „the gold labels for the test set are **withheld**" era fals. Acum scrie că sunt
   publice, că noi nu le-am folosit ca setarea să rămână fără etichete cap la cap, și că
   **consecința** e imposibilitatea de a descompune metrica.
4. **Limitations.** Același fals, reparat la fel, plus declarația explicită că limitarea e a
   noastră și se poate elimina.
5. **Introducere, P3.** Recunoaște acum că datele există și că le lăsăm deoparte deliberat.
   Altfel se citea ca „nu există date pentru română".

### Trei adăugiri care întăresc lucrarea

- **2.2, diferențierea.** `cristea-nisioi-2024-machine` transferă complexitatea în română prin
  traducere în engleză; RALS raportează `r ≈ 0.3` și **concluzionează că transferul cross-lingual
  de complexitate nu e viabil pentru română**. Rezultatul nostru e contraexemplul: transferul în
  spațiul de reprezentare partajat, nu prin traducere, chiar duce complexitatea în română. E cel
  mai bun cadru de diferențiere pe care îl are lucrarea și ar fi fost o gafă să citezi RALS și
  să-l ocolești.
- **4.1, reperul supervizat.** `r = 0.71 ± 0.05` pe exact acest set, marcat explicit ca
  **necomparabil**, fără nicio revendicare de depășire: al lor e supervizat pe etichete
  românești, in-domain, noi nu vedem niciuna.
- **3.3 (A), sprijin independent.** Corelația Zipf–complexitate de −0.53 pentru română față de
  −0.74 pentru engleză, măsurată de altcineva, e exact fenomenul pe care corecția pe lemă îl
  repară.

### Corecțiile față de intrările de pe Anthology

Trei, toate documentate în comentariile din blocul `filecontents`:

1. `anghel-etal-2025-rals`: Anthology despică prost al doilea autor, `Petru-Theodor, Cristea`,
   ceea ce s-ar randa „Cristea Petru-Theodor". Scris `Cristea, Petru Theodor`, cum apare pe
   pagina lor de titlu și cum confirmă intrarea din 2024.
2. Aceeași intrare: `Creanga` fără diacritică → `Creang{\u a}`, escape-ul folosit deja la
   `{\v{S}}tajner`.
3. `cristea-nisioi-2024-machine`: `MLSP` nebracket-at se randa „mlsp" → `{MLSP}`. Plus `Anaïs`
   convertit la `Ana{\"i}s`, regula fără-Unicode.

Verificat la compilare: se randează „Fabian Anghel, Petru Theodor Cristea, Claudiu Creangă, and
Sergiu Nisioi" și „Archaeology at MLSP 2024", identic cu paginile lor de titlu.

### Titlul și autorii

Titlul e pus, cel din PDF-ul original. Autorii **nu**, și nici nu trebuie: `acl.sty` pune
`\acl@anonymizetrue` pentru opțiunea `review` și tipărește „Anonymous ACL submission" în locul
lui `\@author`. `\author{}` e gol intenționat, cu un bloc comentat de completat la camera-ready;
gol e mai bine decât placeholderii template-ului, care ar pleca la tipar dacă cineva comută pe
`final`.

## Compilare

Compilat local pe 30 iulie 2026 (pdflatex → bibtex → pdflatex ×3): **0 erori, 0 citări
nerezolvate, 0 `??`, 0 avertismente bibtex, 0 overfull hbox**, **20** de referințe în `.bbl`,
ambele figuri și cele 5 tabele plasate.

**9 pagini în PDF, și nu e o depășire.** Structura: paginile 1–7 conținut, cu Conclusions
terminându-se la ~55% din pagina 7, apoi Limitations pe pagina 7 și References pe paginile 8–9.
Pagina 9 are 62 de rânduri de referințe, deci nu e o pagină orfană. Nicio coloană numai-floats.

Conținutul numărat (Introduction → Conclusions) e **~6.5 pagini din cele 8**. Limita MRL pentru
long paper e 8 pagini de conținut, iar Limitations și References nu se numără, deci mai e loc de
~1.5 pagini.

> PDF-ul a fost 8 pagini înainte de citarea RALS. Cele două intrări noi au împins bibliografia
> peste pagina 8. Referințele nu intră în limită, deci nu s-a forțat nimic.

# Ordinea de lipit în Overleaf, pe fragmente

Tabelul de mai jos rămâne valabil pentru **editarea** textului: fragmentele sunt sursa,
`paper_full.tex` se reasamblează din ele. Nu mai e nevoie să fie lipite pe rând în Overleaf.

Recompilat local pe 27 iulie 2026, după revizia 3 a introducerii (pdflatex → bibtex →
pdflatex ×2): **0 erori, 0 citări nerezolvate, 0 referințe încrucișate nerezolvate,
0 avertismente bibtex**, 18 referințe în `.bbl`. Tot **7 pagini de conținut**
(Introduction → Conclusions), plus Limitations și References, care nu se numără — 9 pagini
în total în PDF. Limita MRL e 8 pagini, deci mai e loc de aproximativ o pagină.

## Fișierele, în ordine

| # | Fișier | Unde intră în `acl_latex.tex` |
|---|---|---|
| 0 | `paste_preamble.tex` | după `\usepackage{graphicx}`, înainte de `\begin{document}` |
| 1 | `paste_abstract.tex` | peste blocul `\begin{abstract}...\end{abstract}` |
| 2 | `paste_intro.tex` | peste `\section{Introduction}` — conține și Related Work |
| 3 | `paste_body.tex` | imediat după, Approach → Conclusions |
| 4 | `paste_limitations.tex` | după Conclusions, **înainte** de `\bibliography{custom}` |

`paste_bib_additions.bib` nu se lipește în `.tex` — vezi mai jos.

## `intro_preview.tex`, fișierul de dat copy-paste în Overleaf

Este **template-ul ACL vanilla integral**, cu Introduction și Related Work ale noastre în el.
Un singur fișier, autonom: se lipește într-un `main.tex` gol, iar proiectul nu are nevoie decât
de `acl.sty` și `acl_natbib.bst`, care vin cu template-ul.

Din template s-a păstrat verbatim tot ce e structură: preambulul cu toate comentariile lui,
`%\setlength\titlebox`, blocul de autori plus varianta comentată pe 20 de autori,
`\section*{Limitations}`, `\section*{Acknowledgments}`, `\bibliography{custom}`, `\appendix`.
Introducerea și Related Work au luat locul corpului lui `\section{Introduction}`.

> Corectat pe 30 iulie 2026. Paragraful ăsta susținea că secțiunile de manual ale
> template-ului (Engines, Preamble, Document Body, Citations, Equations, BibTeX Files) au fost
> înlocuite. **Nu au fost:** în `intro_preview.tex` au rămas, cu tabelele și figurile lor, iar
> numerotarea iese acolo 1 Introduction, 2 Related Work, 3 Engines și așa mai departe. Scoase
> sunt abia în `paper_full.tex`, unde secțiunile lucrării le iau locul. Consecințele scoaterii,
> toate verificate la compilare: dispar `\nocite{Ando2005,...}`, citările la `Gusfield:97`,
> referințele la `tab:accents`, `fig:experiments`, `eq:example` și `sec:bibtex`, și dispare
> nevoia de pachetul `mwe` pentru `example-image-golden`.

**Bibliografia vine cu fișierul**, scrisă de un bloc `filecontents*[overwrite]{custom.bib}` cu
toate cele 18 intrări. Consecința lui `[overwrite]`: `custom.bib` se rescrie la fiecare
compilare, deci intrări noi (RALS, Kuvshynova, când se decid) se adaugă **în blocul din `.tex`**,
nu editând `custom.bib` în Overleaf, unde s-ar pierde. În schimb, fișierul funcționează lipit
și într-un proiect ACL nemodificat, care are deja un `custom.bib` de exemplu.

Nu înlocuiește tabelul de mai sus: textul se editează în `paste_abstract.tex` și
`paste_intro.tex`, iar `intro_preview.tex` se regenerează din ele.

Compilat pe 27 iulie 2026 în două directoare goale, unul dintre ele cu un `custom.bib` preexistent
ca să se confirme `[overwrite]` (pdflatex → bibtex → pdflatex ×2): 0 erori, 0 avertismente,
0 citări nerezolvate, 0 `??`, 15 referințe în `.bbl`, 3 pagini. Introduction și Related Work se
termină pe pagina 2. PDF-ul rezultat e `intro_preview.pdf`.

Blocul `\pinlabel` din fișier fixează numerele Secțiunilor 3–5, care în preview nu există încă,
și **se șterge** când se lipește `paste_body.tex`. Locul unde se lipește e marcat cu un comentariu.

## Bibliografia

`custom.bib` trebuie să conțină, la final:

1. cele 5 intrări nemodificate din `report/custom.bib`: `conneau2020xlmr`, `hale2001probabilistic`,
   `rayner1998eye`, `lundberg2017shap`, `wei2022cot`;
2. tot conținutul din `paste_bib_additions.bib` (13 intrări, toate luate literal de pe
   `aclanthology.org/<id>.bib`).

Cele 4 intrări vechi cu `% TODO` din `report/custom.bib` (`shardlow2021complex`,
`shardlow2024mlsp`, `openllmro2024rollama3`, `gaze4nlp2025surprisal`) **se șterg** — sunt
înlocuite de chei noi și nu mai e citată niciuna. Total: 18 referințe, toate rezolvate.

Cele 2 intrări adăugate la revizia 3 a introducerii (27 iulie) sunt `qiu-etal-2024-complex`
și `saggion-etal-2024-lexical`, ambele TSAR 2024; sunt citate atât în paragraful de
motivație, cât și în Related Work.

## Figuri

Se urcă **două** PNG-uri din `report/figures/` (`beeswarm.png`, `fig_corr_matrix.png`) într-un
folder `figures/` din proiectul Overleaf. `paste_preamble.tex` conține deja
`\graphicspath{{figures/}}`. `fig_confusion.png` **nu** se mai urcă: figura a fost scoasă din
`paper_full.tex`, motivele sunt sus.

## Capcane de compilare — verificate

- **Nu** adăugați `\bibliographystyle{acl_natbib}`; `acl.sty` îl setează singur.
- **Niciun** caracter arond în comentariile din `.bib` — BibTeX îl citește ca început de intrare.
- `enumitem` nu e necesar: lista de contribuții folosește `enumerate` standard.
- `amsmath` nu e necesar: nu se folosește `\text{}` nicăieri (doar `\mathrm{}`, care e din kernel).
- `booktabs` **este** necesar, pentru `\toprule`/`\midrule`/`\bottomrule` din cele 5 tabele.
  E singura adăugire reală de preambul, alături de `\graphicspath`.

## Anonimizare

Toate fișierele sunt anonimizate: fără nume de autori, fără link de GitHub, fără afiliere.
De verificat înainte de submisie că `\author{}` din `acl_latex.tex` e golit și că opțiunea
`[review]` e activă în `\usepackage[review]{acl}`.

## De re-verificat înainte de submisie

- **`tab:fail`, rândul Lasso (in-source 0.569).** Celelalte valori in-source sunt verificate în
  loguri (`sweep_log.txt`, `sweep_enc_log.txt`, `finetune_sweep_log.txt`, `finetune_lora_log.txt`),
  dar pentru Lasso nu s-a salvat niciun log. `analysis_lasso.py` afișează ambele metrici — o rulare
  confirmă dacă `0.569` e `transfer_avg` (cum e trecut acum) sau `EN→ML`.
