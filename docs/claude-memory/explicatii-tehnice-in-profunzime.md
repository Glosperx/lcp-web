---
name: explicatii-tehnice-in-profunzime
description: "Când utilizatorul repetă \"ce înseamnă X mai exact\", vrea explicație la nivel de formulă/cod, nu reformularea aceleiași abstracții"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7991b03d-de53-43f2-a4be-6d864309fb76
  modified: 2026-08-18T09:52:15.391Z
---

Când utilizatorul întreabă "ce înseamnă asta mai exact" pe o explicație deja dată, tratează asta ca
cerere explicită de a coborî un nivel: citează codul exact (fișier:linie), desface fiecare simbol din
formulă, și adaugă un exemplu numeric concret dacă ajută. Nu reformula aceeași abstracție cu alte
cuvinte.

**Why:** Pe 18 august 2026, la explicarea configurației `xlmr + nota 1-5 + lema + ansamblu + set ales
LOLO (w pe test)` din [[ansamblul-de-surse-pentru-semnalul-a]], utilizatorul a împins de trei ori la
rând ("ce inseamna asta mai exact") până explicația a ajuns la mecanica exactă a lui `zscore`/`zA_of`
din `fuse_ab.py` și la un exemplu numeric jucărie. Pe parcurs au apărut și corectat două impresii
greșite formate din explicații de nivel prea abstract: că "ansamblu" ar combina 2 LLM-uri (de fapt
combină `p_en`/`p_multi`, cele două brațe ale semnalului xlmr; B rămâne un singur LLM ales, nu mediat),
și că 0.6636 ar fi cea mai bună cifră a sistemului (de fapt e nota de robustețe; sistemul decis e
0.664555, vezi [[pondere-fuziune-potrivita-pe-test]]).

**How to apply:** La orice întrebare despre metodologia/pipeline-ul acestui proiect, citește codul
sursă direct (nu te baza doar pe rezumatul din memorie) înainte de a explica, și verifică cifra
"actuală" decisă/măsurată (memorie sau `output/*.md`) înainte să afirmi ce e "cel mai bun" număr —
un rezumat vechi din memorie poate fi depășit de o decizie ulterioară.
