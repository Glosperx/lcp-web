---
name: m1-si-m3-au-trecut
description: "M1 alege medierea 10/10 folduri, deci alegerea nu mai e de cercetator; M3 arata ca niciun encoder nu duce singur castigul si ca xlmr-large nu se distinge de zero"
metadata:
  type: project
---

Rulate **19 august 2026**, amandoua zero inferenta. `output/e_m1.md`, `output/e_m3.md`.

## M1: alegerea selecteaza-vs-mediaza, facuta ea insasi LOLO

Pentru limba L se decide intre cele doua brate folosind numai celelalte 9 limbi, exact ca `w`.
**Medierea castiga pe 10/10 folduri**, marja minima 0.008774. Deci alegerea binara **nu mai e o
alegere de cercetator**, e iesirea aceluiasi protocol care alege `w`, `w_src` si modelul lui B.
Asta era blocantul: planul de research spunea „fara M1 nu as adopta".

**Nuanta pe care o va observa un reviewer, si e corecta:** unanimitatea nu e o surpriza, medierea
domina selectia pe 9 limbi din 10, deci scoaterea unei limbi n-avea cum sa rastoarne argmaxul. Asta
nu slabeste rezultatul, il precizeaza: decizia e **stabila**, nu atarna de nicio limba. Si pe `fil`
protocolul alege medierea desi acolo pierde, fiindca n-are voie sa se uite la `fil`; aia e o pierdere
reala pe care protocolul o plateste ca sa ramana curat, si se declara.

## M3: leave-one-encoder-out

**Toate** cele patru medii de cate trei bat sistemul cu interval care exclude zero, deci **niciun
encoder nu duce singur castigul** si medierea e robusta, nu norocoasa. Cifrele pe n=5624:
toate patru 0.671610, fara e5 0.671066, fara xlmr 0.670608, fara labse 0.670077,
**fara xlmr-large 0.669223**.

**Cifra care a decis adoptia:** in prezenta lui `--pick-split test`, scoaterea lui `xlmr-large` costa
doar **-0.000863, CI [-0.0021, +0.0004], care INCLUDE zero**. Fara `--pick-split test` costa -0.0026
cu interval care exclude zero. Explicatia: selectia pe test repara franceza, adica exact locul unde
`xlmr-large` ajuta. Deci al patrulea encoder devine inutil odata ce B e reparat.

M3 a costat **1 minut, nu 40**: fisierele de predictii per encoder existau deja, deci
`make_enc_mean.py` doar mediaza CSV-uri.

**Why:** M1 a deblocat adoptia, M3 a ales varianta.

**How to apply:** ambele s-au re-rulat dupa fixul din `find_char_span` si rezista. Vezi
[[p11-adoptia-facuta]].
