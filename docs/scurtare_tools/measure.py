#!/usr/bin/env python3
"""Pozitia sfarsitului corpului intr-un PDF compilat.
Folosire: python3 docs/scurtare_tools/measure.py <director_compilat> [pozitie_referinta]
Corpul se termina chiar inainte de titlul 'IMPLEMENTATION' (dupa Conclusions). Se tipareste pagina, coloana (L/R) si
y (pt) al titlurilor IMPLEMENTATION, Limitations si Acknowledgments, plus o pozitie liniara:
  pos = ((pagina-1)*2 + coloana) * 704 + (y - 70.866)     (704 pt = inaltimea unei coloane; coloana R = 1)
Tinta 'corpul pe 8 pagini' = pos 11264 (sfarsitul coloanei din dreapta de pe pagina 8).
Al doilea argument: o pozitie de referinta; se tipareste castigul in pt si in coloane."""
import re,sys,subprocess
d=sys.argv[1]; ref=float(sys.argv[2]) if len(sys.argv)>2 else None
pdf=f'{d}/documentatie_overleaf.pdf'
n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
H=704.0; found={}
for p in range(1,n+1):
    t=subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-bbox',pdf,'-'],capture_output=True,text=True).stdout
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',t):
        w=m.group(5)
        if w in('IMPLEMENTATION','Limitations','Acknowledgments') and w not in found:
            x,y=float(m.group(1)),float(m.group(2))
            found[w]=(p,'R' if x>300 else 'L',round(y),((p-1)*2+(1 if x>300 else 0))*H+(y-70.866))
print('pagini in total:',n)
for k,(p,c,y,pos) in found.items(): print(f'  {k:15s} pagina {p} coloana {c} y {y}  pos {pos:.0f}')
if 'IMPLEMENTATION' in found:
    pos=found['IMPLEMENTATION'][3]
    print(f'  corpul se termina la pos {pos:.0f}; pana la tinta (11264) mai trebuie taiat {pos-11264:.0f} pt = {(pos-11264)/H:.2f} coloane = {(pos-11264)/H/2:.2f} pagini')
    if ref is not None: print(f'  castig fata de referinta {ref:.0f}: {ref-pos:.0f} pt = {(ref-pos)/H:.2f} coloane')
