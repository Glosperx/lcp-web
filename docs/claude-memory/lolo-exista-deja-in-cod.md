---
name: lolo-exista-deja-in-cod
description: Bucla leave-one-language-out pe care planul multilingv o trata ca de construit există deja în finetune_xlmr.py și a fost rulată pe it/pt/es
metadata: 
  node_type: memory
  type: project
  originSessionId: 8d525f31-ed64-403d-bcae-3932e312db13
  modified: 2026-08-16T17:59:28.861Z
---

Descoperit pe **15 august 2026**, verificat direct în cod și în CSV-urile de rezultate.

Planul din 8 august ([[paper-extensie-multilingva-arr-octombrie]]) aloca săptămânile 2-3 construirii
buclei leave-one-language-out. **E deja scrisă și deja rulată.**

- `frozen_multi_gate()`, `finetune_xlmr.py:260`: encoder înghețat, antrenat pe CompLex EN + MLSP
  fără limba L, testat pe L. Exact designul propus pentru configurația (i).
- `multilingual_gate()`, `finetune_xlmr.py:235`: același split, cu fine-tuning, comparând EN-only
  față de EN+romanic.

Rezultate rulate, din `data/frozen_multi.csv` și `data/finetune_multi.csv`:

| Limbă ținută deoparte | n | FROZEN | LoRA EN+romanic | LoRA EN-only |
|---|---|---|---|---|
| it | ~585-592 | **0.6006** | 0.5506 | 0.5268 |
| pt | ~592-597 | **0.7775** | 0.6710 | 0.6503 |
| es | ~593-594 | **0.6185** | 0.5782 | 0.5375 |

Trei consecințe.

1. **Rezultatul negativ „frozen bate fine-tuned" e deja replicat 3 din 11**, sub split LOLO curat,
   nu sub validarea in-source. E material mai puternic decât ce e în paperul actual, unde argumentul
   stă pe o singură pereche de limbi.
2. **Antrenarea multilingvă bate EN-only** pe fiecare din cele trei (+0.0238, +0.0207, +0.0406).
   Mic, dar consistent ca semn. Teză nescrisă încă nicăieri.
3. **Varianța între limbi e 0.18** (pt 0.7775 față de it 0.6006), între două limbi romanice, sub
   tratament identic. La n ≈ 590 pe limbă, CI pentru r ≈ 0.6 e de ordinul ±0.05, deci un
   Δ(monolingv − universal) de câteva sutimi **nu se distinge pe o singură limbă**. Δ trebuie
   raportat ca efect pereche agregat peste limbi, cu calcul de putere, nu ca 9 numere separate.

## CORECȚIE 16 august 2026: cei 0.18 NU sunt problema statistică centrală

Punctul 3 de mai sus e greșit în partea lui importantă, iar eroarea ar fi dus planul în direcția
greșită. **Într-un test pereche peste limbi, varianța între limbi se anulează.** Ce contează nu e cât
diferă italiana de portugheza, ci cât diferă Δ-ul italian de Δ-ul portughez.

Estimarea există deja în `data/finetune_multi.csv`, pe contrastul pereche EN+romanic minus EN-only:
+0.0238, +0.0207, +0.0406. Deci **σ_Δ = 0.0107**, de 16 ori mai mic decât 0.18.

Calcul de putere, test pereche bilateral, α = 0.05, putere 80%: Δ minim detectabil e **0.0114 la 9
limbi, 0.0106 la 10, 0.0100 la 11**. Designul nu e evident subputernic; efectul deja măsurat (0.028)
ar fi detectat comod.

**Rezerva, decisivă:** σ_Δ e estimat pe trei numere, iar CI-ul lui 95% urcă până la 0.0673, de 6.3 ori
punctul estimat. La limita aia Δ-ul detectabil la 11 limbi devine 0.063, adică designul e fără
speranță. **Nu știm dacă designul e puternic sau inutil**, iar diferența stă doar în cât de bine e
estimat σ_Δ. Trecerea de la 3 la 5 limbi scade limita superioară de la 6.3σ la 2.9σ.

De aici iese primul experiment de făcut, care e și cel mai ieftin: `frozen_multi_gate` și
`multilingual_gate` au `holdout=("it","pt","es")` **hardcodat ca tuplu implicit**, dar datele locale
au 5 limbi. Franceza și catalana sunt în antrenare și n-au fost niciodată evaluate. Schimbarea
tuplului dă 2 puncte în plus fără nicio descărcare. Criteriul de oprire, decis dinainte: σ_Δ sub
0.015 înseamnă design viabil, peste 0.030 înseamnă că designul centrat pe Δ e mort și se pivotează.

## ÎNCHIS pe 17 august 2026: E1 a rulat pe 10 limbi, σ_Δ = 0.0369

Cele de mai sus sunt istorie. `frozen_multi_gate` a fost rescris (holdout pe toate cele 10 limbi, braț
EN-only adăugat, centrare per limbă și în antrenare, bootstrap pe contexte) și rulat. **157 de secunde
în total**, din care 124 embedding pe MPS. Frica de „14.000 de treceri costisitoare" era nefondată.

Rezultate în `output/e1_lolo_frozen.csv`, verdictul în `output/e1_verdict.md`.

- **σ_Δ între limbi = 0.0369**, față de 0.0107 estimat pe cele 3 limbi. Criteriul §5.2, aplicat înainte
  de interpretare: peste 0.030 înseamnă **designul centrat pe Δ e mort**, deci cvartetul Δ_controlat
  (RoLlama3.1, Swallow, Gervásio, ~80 GB) **nu se descarcă**.
- Δ mediu −0.0045. CI exclude zero la 4 limbi din 10, în ambele direcții: pozitiv la ca/es/it, toate
  romanice, negativ la **ja, −0.0896**. Japoneza singură produce imprăștierea: fără ea σ_Δ = 0.0228.
- σ_Δ în interiorul limbii, bootstrap pe contexte, e 0.0142, adică altă mărime decât cea din §5.2.
- **r-ul nostru, semnal A singur, bate run 1 al lui Cristea și Nisioi pe 8 din 9**, pierde doar
  franceza cu 0.018. Media 0.5523 față de 0.4188. Bate și Archaeology 8 din 10. Dar pierde 9 din 10
  față de G-Eval cu GPT-4o, medie 0.6571.

**Why:** decizia despre cele 80 GB și despre săptămânile 4-5 se ia din cifra asta, nu din estimarea pe
3 limbi. Vezi [[r-si-r2-masurate-pe-rolcp]] pentru cifrele românești, care sunt alt protocol.

## Alte corecții din aceeași verificare

- **Filtrul romanic nu e un filtru, e o mapare cu fallback tăcut.** `MLSP_LANGS` mapează prin
  `.map()`, iar o limbă nemapată dă `NaN`, pe care `lexical()` îl transformă în `"en"`
  (`solution_bert.py:153`, `recompute_gpu.py:63`). Deci limbile noi nu sunt aruncate, ci primesc
  frecvențe **englezești**, tăcut. Scos cum propune planul, e mai rău, nu mai bine.
- **`data/mlsp/` n-a avut niciodată decât 5 limbi**, nici pe Windows. `load_mlsp()` din
  finetune_xlmr.py globează fără filtru și tot a tipărit `['ca','es','fr','it','pt']`. Deci gate-ul
  HuggingFace e pe calea critică indiferent de ce mai există pe Windows.
- **LOLO-ul existent e semnalul A dezbrăcat:** fără fix de lemă, fără B, fără C, fără D. Bucla e
  construită, conținutul nu.
- **Configurația (ii) nu e definibilă pentru semnalul A.** Un encoder monolingv pe limba țintă pune
  antrenarea și testul în spații diferite. Δ rămâne definibil doar pe semnalele B și C, care sunt
  scalari per item.

Alte trei lucruri verificate în aceeași sesiune, care contrazic ipoteze din plan:

- **Filtrul romanic e duplicat**, nu într-un loc: `solution_bert.py:56` și `recompute_gpu.py:31`.
- **Scoaterea filtrului nu ajunge.** Șapte funcții presupun alfabet latin (`VOWELS` la
  `solution_bert.py:55`, `n_syllables`, `max_consonant_run`, `vowel_ratio`, `normalize_token`,
  coloana de majusculă din `lexical()`, și `text.find(token)` din `find_char_span`/`surprisal`).
  **Sinhaleza e abugida**, deci intră la muncă de cod lângă japoneză, nu în palierul „doar XLM-R".
- **Setarea e transductivă, nu inductivă.** `_Xc()` centrează pe media setului, iar în
  `frozen_multi_gate` limba de test e centrată pe propria ei medie, deci se folosesc datele
  neetichetate ale limbii țintă. Legitim, dar nenumit în paper. De numit înainte s-o facă un
  reviewer.
- **Semnalul B e legat de română prin prompt**, hardcodat la `recompute_gpu.py:228` („Esti expert in
  lingvistica romana"). Limba promptului e un confound, nu un detaliu: interacționează cu calitatea
  modelului pe limba respectivă, deci un Δ măsurat cu prompturi diferite amestecă două efecte.

**Why:** schimbă atât calendarul, cât și ce e riscul principal. Partea despre care planul credea că e
muncă de construcție e făcută; partea despre care credea că e trivială (scoaterea filtrului) e muncă
reală; iar modul cel mai probabil în care lucrarea iese fără rezultat nu e lipsa de compute, ci
varianța între limbi care înghite Δ-ul.

**How to apply:** înainte de a estima orice calendar pentru extensia multilingvă, citește
`finetune_xlmr.py:235-280` și cele două CSV-uri. Nu replanifica construirea a ceva ce rulează deja.
Vezi și [[hardware-doua-masini]] și [[paper-extensie-multilingva-arr-octombrie]].
