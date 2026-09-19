# Workshop țintă: MRL @ EMNLP 2026

Verificat pe 23 iulie 2026, direct pe site-urile workshop-urilor. Completat pe
27 iulie 2026 cu statutul arhival al MRL, track-urile secundare, motivul pentru
care EMNLP 2026 main e inaccesibil și căile de după MRL — surse în secțiunile
respective.

## Ținta

**MRL — 6th Workshop on Multilingual Representation Learning** (împreună cu SIGTYP)
<https://sigtyp.github.io/ws2026-mrl.html>

| | |
|---|---|
| Deadline submisie directă | **10 august 2026**, AoE |
| Notificare | 20 septembrie 2026 |
| Camera-ready | 30 septembrie 2026 |
| Format | short 4p / long 8p (fără referințe), template ACL, anonimizat |
| Arhival? | **Da** — „All accepted research papers will be published as part of our workshop proceedings" |
| Alternativă | commitment ARR (ciclul mai 2026 sau mai vechi), deadline **4 septembrie** |
| Track secundar | abstract extins **non-arhival**, 2 pagini, pentru lucrări deja publicate sau incomplete |
| Loc | Budapesta, 24–29 octombrie 2026 |

Track-ul ARR nu ne e accesibil: cere recenzii din ciclul mai 2026 sau mai vechi,
pe care nu le avem. Mergem pe submisia directă din 10 august.

### De ce MRL

Trei puncte din CFP-ul lor sunt exact contribuțiile noastre:

- *zero-shot and few-shot learning for multilingual NLP* → sistemul nu vede nicio etichetă RO;
- *transfer learning for under-studied, **morphologically-rich** languages* → fix-ul de frecvență
  pe lemă (+4.09, cel mai mare câștig singular);
- *analysis and probing of multilingual representations* → analiza SHAP + demonstrația că encoderul
  înghețat bate fine-tuning-ul (0.515 vs 0.461/0.462 in-source).

## De ce nu conferința mare — verificat pe 27 iulie 2026

Întrebare pusă în sesiunea de revizie a introducerii: de ce workshop și nu direct
EMNLP 2026? Răspuns: **nu se poate, indiferent de calitatea lucrării.**

- EMNLP 2026 **nu acceptă submisie directă** — e exclusiv prin ACL Rolling Review:
  „EMNLP 2026 will use ACL Rolling Review (ARR) as a reviewing system, but final
  decisions will be made by the conference."
- Ciclurile ARR care îl alimentează au fost **martie 2026** (deadline 16 martie) și
  **mai 2026** (deadline 25 mai). Ambele închise.
- Deadline-ul de commitment din **2 august 2026** e doar pentru cine are deja
  recenzii ARR. Noi nu avem (vezi și rândul BlackboxNLP din tabelul de mai jos).
- ACL 2026 s-a ținut deja: 5–7 iulie 2026.

### Unde se poate merge după MRL

Decizie amânată deliberat — se ia în toamnă, când avem și recenziile MRL, care
sunt oricum cel mai bun input pentru ea.

| Venue | Deadline ARR | Conferința | Verdict |
|---|---|---|---|
| EACL 2027 | 3 august 2026 | Atena, 9–14 mar 2027 | **Exclus** — ar fi submisie simultană cu MRL (10 aug), încalcă politica de dublă submisie |
| ACL 2027 | TBA, probabil ciclu ian–feb 2027 | Kyoto, 17–22 aug 2027 | Ținta naturală |
| EMNLP 2027 | TBA | TBA | Mai mult timp de lucru decât ACL 2027 |

Ambele sunt top-tier; criteriul de alegere ar trebui să fie timpul disponibil
pentru extindere, nu prestigiul. De ținut minte și **TACL** (jurnal ACL, submisie
continuă fără cicluri, considerat echivalent) și **Findings** ca rezultate valide.
Fereastra realistă de extindere: ~octombrie 2026 – ianuarie 2027.

### De verificat înainte de a te baza pe asta

Regula prin care un paper de workshop **arhival** poate fi trimis ulterior, în
formă extinsă, la o conferință mare — extinderea trebuie să conțină experimente
noi, analiză nouă sau evaluare nouă, iar paperul anterior trebuie declarat pe
prima pagină — apare în paginile ACL SRW și în FAQ-uri de conferință, **dar pagina
canonică de politică ACL dă 404**. Nu am putut confirma textul la sursă. De citit
în CFP-ul venue-ului țintă înainte de a construi planul de toamnă pe ea.

## De ce nu celelalte

| Workshop | Deadline | Motiv |
|---|---|---|
| BabyLM (workshop track) | 15 aug 2026 | Al doilea ca potrivire tematică, prin surprisal. **Nu îl țintim:** aceeași lucrare nu poate merge la două venue-uri cu review-uri suprapuse (politica ACL de multiple submission), iar ca fallback nu funcționează — notificarea MRL vine pe 20 sep, la o lună după deadline. În plus workshop-ul e despre *antrenarea* de LM-uri mici pe date limitate (track nou MultiLingual: BabyBabelLM, 100M tokens, EN/NL/ZH); noi nu antrenăm niciun LM. |
| Insights (Negative Results) | ~~8 iunie 2026~~ **închis** | Ar fi fost potrivirea perfectă pentru Secțiunea „What Did Not Work". De ținut minte pentru 2027 — deadline-ul lor cade în **iunie**, mult mai devreme decât restul. |
| BlackboxNLP | ~~17 iulie 2026~~ **închis** | ARR-commit rămâne deschis până pe 16 aug, dar n-avem review-uri ARR. |
| ORACLE | 1 aug 2026 | Multilingv + low-resource, dar centrat pe *reasoning*. |
| WiNLP | 26 iul 2026 | Workshop de comunitate (extended abstracts), nu de rezultate. |
| UncertaiNLP / GLM | 7 aug / 5 aug 2026 | Fără legătură cu LCP. |
| Restul celor 28 acceptate | — | Fără legătură tematică (verificat inclusiv LUHME: topicurile lor nu includ lizibilitate/simplificare). |

## Short sau long? — măsurat, nu ghicit

Am compilat `paste_intro.tex` pe template-ul ACL real. Introducerea ocupă **~2.8 coloane**,
Related Work **~1.6 coloane** → ~4.4 coloane, adică peste **două** pagini din patru. Adăugând
abstractul, paperul actual mai are 3 figuri și 4 tabele, care singure umplu ~2 pagini.

> Corectat pe 27 iulie 2026, la recompilarea de după revizia 3. Cifrele de mai sus (1.25 / 0.9
> coloane) erau subestimate de peste două ori — măsurate acum pe PDF-ul compilat, nu estimate.
> Concluzia nu se schimbă, ci se întărește: la 4 pagini nu încape nimic altceva.

**Recomandare: submisie ca long paper (8 pagini).** La 4 pagini ar trebui tăiate fie Related Work
(la 3 paragrafe, fuzionat în introducere), fie două dintre figuri — și exact analiza SHAP și matricea
de corelații sunt ce cere CFP-ul MRL („analysis and probing of multilingual representations").
MRL acceptă ambele formate, la același deadline.

## De rezolvat înainte de submisie

1. **Ponderile sunt tunate pe scorul public al competiției.** Într-un paper asta e tuning pe test set.
   Minim: o frază explicită în Approach. Mai bine: un număr pe leaderboard-ul privat sau pe cele 14
   exemple RO.
2. **Metrica `50(|r| + max(0,R²))` e a competiției**, nu una recunoscută — raportați și Pearson *r*
   și *R²* separat.
3. **Anonimizare** (MRL e double-blind): scos link-ul de GitHub din concluzii.
4. **Limitations** — MRL cere de obicei o secțiune separată; nu intră în limita de pagini.
5. Rezolvat `% TODO: author contributions`.
