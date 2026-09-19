---
name: update-paper-draft-semnale-a-b
description: "output/update_paper_draft.txt scris si corectat: sistemul multilingv e A (medie 3 encodere + Ridge/HGB) + B (LLM ales LOLO), r=0.674946, fara eyetracking, 2 paper-uri de referinta; plus corectii 29 aug pe descrierea soft-read/softmax a lui B"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c91d735-9e68-4319-b624-a2bf6fc90cbf
  modified: 2026-08-29T12:52:10.683Z
---

Scris si iterat impreuna cu Alexandru intr-o sesiune lunga, in `output/update_paper_draft.txt`
(text simplu, fara diacritice, fara tabele markdown — vezi [[raspunsuri-fara-diacritice-fara-tabele-md]]).
E o explicatie/draft a metodei pentru paper, nu codul insusi.

## Ce descrie fisierul

**Semnalul A**: pentru fiecare din 3 encodere (`xlm-roberta-base`, `LaBSE`, `multilingual-e5-base`)
se antreneaza SEPARAT un blend Ridge + HistGradientBoosting (2 modele, media predictiilor lor),
folosind ca trasaturi: embeddingul encoderului respectiv + frecventa lemei + fertilitatea (nr de
subword-uri per cuvant). Cele 3 predictii finale (nu embeddingurile) se standardizeaza per limba si
se mediaza. `xlm-roberta-large` a fost testat si EXCLUS: da un scor putin mai mare (0.675996 vs
0.674946 in sistemul complet), dar diferenta nu e semnificativa statistic (CI include zero) si e
2.7x mai scump — corect descris acum in draft ca "acelasi scor", nu ca "3 e mai bun". Semnalul A
singur (fara niciun LLM) da r mediu 0.598 pe 10 limbi.

**Semnalul B**: nota LLM 1-5, medie a doua prompturi zero-shot (rol expert + varianta scurta), FARA
few-shot in productie. Modelul se alege per limba prin LOLO pe testul celorlalte 9 limbi
(`--pick-split test`) — sub acest criteriu Gemma4-12B castiga pe toate cele 10 limbi, inclusiv
franceza (0.642), nu doar pe 9 cum arata selectia pe trial. Semnalul C (surprisal) a fost testat si
scos, r intre -0.080 si +0.072, semn instabil intre limbi.

**Rezultatul final**: r mediu = 0.674946 pe 10 limbi, testul complet MLSP (n=5624). Eyetracking-ul
NU e folosit in acest sistem multilingv — a fost investigat separat, doar pentru cazul romanesc
(RoLCP), unde aducea +0.0067 in r.

**Sectiunea de research**, redusa la cerere la 2 paper-uri, fara Cristea/Nisioi (Archaeology, scos
explicit de Alexandru):
1. Nohejl et al. (2025) — foloseste date labeled (G-Eval 3-shot: 0.657, G-Scale 30-shot: 0.669)
2. Enomoto et al. (2024), TMU-HIT — are o rulare zero-shot fara date labeled: 0.610

## Corectii facute pe parcurs (utilizatorul scrisese initial altfel)

- xlmr-large NU scade media, cum scrisese initial — da un scor putin mai mare, dar nesemnificativ.
- Productia nu foloseste few-shot in varianta cea mai buna — doar 2 prompturi zero-shot, verificat
  direct in `solution_bert.py` (`LLMRater.rate()`).
- Ridge si HGB sunt 2 modele separate care primesc ACELASI X (nu trasaturi diferite), antrenate o
  data per encoder (deci 3 perechi Ridge+HGB = 6 modele in total), iar rezultatele lor se mediaza
  post-hoc, nu e stacking.

**Why:** utilizatorul scrie draftul manual, direct in fisier, si ma foloseste ca sa verific fapte in
cod inainte sa intre in paper, sa completez cifre lipsa (calculate direct din CSV-urile din
`output/`), si sa scurtez/simplific proza — nu ca sa scriu eu tot textul.

**How to apply:** daca se reia lucrul la lucrarea multilingva, `output/update_paper_draft.txt` e
starea curenta a explicatiei semnalelor A/B, verificata fapt cu fapt. Vezi [[p11-adoptia-facuta]]
pentru cifra 0.674946, [[selectia-modelului-b-e-pe-splitul-gresit]] pentru mecanismul pick-split
test, [[eye-tracking-cat-a-adus-in-r]] pentru de ce eyetracking nu intra aici.

## Sesiune 29 aug 2026: corectii pe descrierea soft-read a semnalului B

Draftul mentioneaza acum 3 prompturi (nu 2 ca in versiunea verificata mai sus — M3K a fost adoptat
intre timp, vezi [[sistemul-e-0690001-m3k]], dar cifra finala din draft ramane 0.674946, nu s-a
actualizat la 0.690001). Corectii facute in paragraful care descrie mecanismul soft-read
(`solution_bert.py` — `digit_mass` + `_expected`, liniile 656-670):

- Fraza cu TabFM, "o diferenta in limita zgomotului", schimbata in "o diferenta nesemnificativa"
  (linia ~207).
- Fraza despre softmax era ambigua initial ("aplic un softmax peste tokenii care sunt doar cei cu
  nota de la 1 la 5" putea fi citita ca softmax restrans SAU ca softmax global). Corectata final la
  "softmax peste logits-urile care corespund doar tokenilor din vocabular care reprezinta notele de
  la 1 la 5" — adica softmax restrans explicit.
- **Fapt matematic netrivial, verificat cu Alexandru:** softmax restrans direct la cele 5 (sau mai
  multe, din cauza variantelor SentencePiece) logits ale cifrelor da REZULTAT IDENTIC cu ce face de
  fapt codul (softmax pe tot vocabularul, apoi extragere de masa pe cei 5 si renormalizare — vezi
  `digit_mass`, linia 666-670). E o identitate: a conditiona un softmax pe apartenenta la o
  submultime echivaleaza cu softmax facut direct pe submultime, fiindca termenul de normalizare Z
  se simplifica in raport. Deci formularea simplificata din draft ("softmax restrans") e CORECTA
  tehnic pentru numerele finale (`p_final`), nu doar o aproximare acceptabila.
- **Ce se pierde prin formularea simplificata, si de ce e OK sa se piarda:** codul real trece prin
  tot vocabularul ca sa poata calcula `raw` (suma celor 5 mase INAINTE de renormalizare), folosit
  separat ca test de sanatate (garda D.4, vezi [[rute-rulare-logits]]): daca modelul a deviat spre
  alt raspuns (ex. bloc `<think>`), `raw` iese aproape 0 si semnalul se arunca. Un softmax restrans
  direct la cele 5 logits n-ar da niciodata acest semnal — ar normaliza mereu la suma 1, oricat de
  nesemnificativa ar fi masa absoluta. Draftul nu mentioneaza `raw`/D.4 deloc, deci simplificarea nu
  strica nimic din ce e scris acolo.
- Doua imprecizii ramase DELIBERAT nefixate, la decizia lui Alexandru: propozitia "Semnalul B
  foloseste acum 3 prompturi" e orfana (nu leaga explicit de restul paragrafului ca procesul se
  repeta x3 si se mediaza), si "o probabilitate de certitudine asupra raspunsului" descrie gresit ce
  se calculeaza de fapt (o nota FRACTIONARA/valoare asteptata, nu o certitudine). Nu se re-propun
  decat daca Alexandru le redeschide singur.
