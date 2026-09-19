---
name: paper-overleaf-workflow
description: "Paperul e un .tex întreg pe template ACL: paper_full.tex e masterul, paper_full_copy-paste.tex e derivatul de dat pe Overleaf"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d9a89e1a-84a5-41a4-a6ef-303bfbb5b38f
  modified: 2026-07-30T10:28:06.220Z
---

Echipa (Alexandru + Mihai-Alexandru + Sergiu Nisioi, coordonator) lucrează în **Overleaf**, pe
template-ul ACL vanilla din `Paper/Articol_Complexity/`. Livrabilul e **un fișier `.tex` întreg**, de
dat copy-paste, nu fragmente de paste.

## Cele două fișiere, de la 30 iulie 2026

| Fișier | Rol | Se editează? |
|---|---|---|
| `Paper/Articol_Complexity/paper_full.tex` | **masterul**, cu tot istoricul deciziilor în comentarii românești | **da** |
| `Paper/Articol_Complexity/paper_full_copy-paste.tex` | **derivat**, fără comentariile românești. Ăsta se lipește în Overleaf | **nu**, se regenerează |
| `Paper/Articol_Complexity/make_copypaste.py` | generatorul, **e în repo**, nu în scratchpad | — |

```bash
cd Paper/Articol_Complexity && python3 make_copypaste.py paper_full.tex paper_full_copy-paste.tex
```

Generatorul păstrează comentariile englezești ale template-ului și scoate blocul din cap plus
comentariile noastre. Are **plasă de siguranță**: compară liniile de cod ale celor două fișiere și
pică dacă diferă cu un caracter. A prins efectiv o eroare la prima rulare. Detecția de limbă e pe
listă de cuvinte, deci **comentariile inline de pe linii de cod nu sunt prinse** — de verificat manual
cu `grep -n '[^ ]  *%'`.

Fișierele vechi (`overleaf_main.tex`, `intro_preview.tex`, `paste_*.tex`) sunt **depășite** și nu mai
sunt sursa. Rămân doar ca istoric.

## Ce trebuie în proiectul Overleaf

Doar patru fișiere, plus textul lipit: `acl.sty`, `acl_natbib.bst`, și `figures/beeswarm.png` +
`figures/fig_corr_matrix.png` din `report/figures/`. **Nu** se urcă `custom.bib`, e scris de blocul
`filecontents`. Compilator pdfLaTeX. La prima compilare bibliografia poate lipsi, pentru că
`custom.bib` nu există până când primul pdflatex îl scrie; a doua rulare o rezolvă.

## Capcane verificate

- `filecontents*[overwrite]{custom.bib}` înaintea lui `\documentclass`. `[overwrite]` e
  **obligatoriu**, proiectul ACL vine cu un `custom.bib` de exemplu. Consecință: intrări noi se adaugă
  **în blocul din `.tex`**, nu în `custom.bib` din Overleaf.
- `.bib`-ul păstrează și cele 7 intrări ale template-ului, inofensive, ca fișierul să meargă lipit
  într-un proiect ACL nemodificat.
- `acl.sty` setează deja `\bibliographystyle{acl_natbib}`. Nu-l adăuga, dublura dă eroare.
- **Niciun caracter arond în comentariile din `.bib`**, BibTeX îl citește ca început de intrare.
- **Niciun Unicode în `.bib`**: `Creang{\u a}`, `Ana{\"i}s`, `{\v{S}}tajner`. Acronimele se protejează
  cu acolade, altfel `.bst`-ul le scrie cu minuscule: `{MLSP}`, `{RALS}`, `{BEA}`.
- **Anonimizarea o face template-ul, nu noi.** Opțiunea `review` din `acl.sty` pune flagul de
  anonimizare și tipărește „Anonymous ACL submission" în locul lui `\@author`. Deci `\author{}` gol e
  corect și nu are ce se șterge din PDF. Aceeași opțiune aduce numerele de linie și de pagină; toate
  dispar la camera-ready.
- **`\section*{Acknowledgments}` e scos**, obligatoriu: `formatting.md`, secțiunea Acknowledgments,
  „Do not include this section in the review version." De repus la camera-ready, imediat înaintea
  referințelor.
- **Plasarea floats-urilor.** Declararea lor în bloc la finalul unei secțiuni face LaTeX să dedice
  coloane întregi numai lor, cu spațiu elastic între figuri. Fiecare float se declară înaintea
  titlului care urmează primei lui referințe, plus `topfraction` 0.9, `bottomfraction` 0.5,
  `textfraction` 0.08, `floatpagefraction` 0.8 în preambul.
- Cropul PNG-urilor **nu ajută**, `tight_layout` a strâns deja marginile, recuperezi 2%.

## Verificarea, de refolosit

Copiază `.tex`-ul, `acl.sty`, `acl_natbib.bst` și cele două PNG-uri într-un director gol, apoi
`pdflatex` → `bibtex` → `pdflatex` ×2. Condiții: 0 erori, 0 `Undefined`, 0 avertismente bibtex,
0 `??` în PDF, 0 `Overfull`, numărul corect de `\bibitem` (acum **20**), și `.aux`-urile masterului și
derivatului **identice** ca etichete, numere și pagini. Plus verificările de stil: em-dash doar în
cele 5 celule de tabel, zero „the system", zero „leaderboard".

Starea pe 30 iulie 2026: **8 pagini**, conținutul se termină pe pagina 6. Limita MRL e 8 pagini de
conținut, iar Limitations și References nu se numără, deci mai e loc de ~2 pagini.

Vezi [[paper-target-mrl-emnlp-2026]] și [[preferinte-de-scriitura-paper]].
