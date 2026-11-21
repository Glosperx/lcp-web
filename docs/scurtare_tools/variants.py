#!/usr/bin/env python3
"""Masoara cat castiga fiecare taiere, compilata intreaga (floaturile se muta, deci castigurile NU se aduna).
Folosire: python3 docs/scurtare_tools/variants.py <baza.tex> <spec.json> <director_lucru>
spec.json = lista de [nume, [[linie_start, linie_sfarsit], ...], [[text_vechi, text_nou], ...]]  (linii 1-indexate din baza.tex,
taiate inclusiv; al treilea element, optional, = inlocuiri de text, fiecare cu exact o aparitie in baza dupa taieri).
Se compileaza si o varianta de control fara nicio schimbare. Rulari in paralel, 4 odata."""
import sys,json,subprocess,re,os
from concurrent.futures import ThreadPoolExecutor
base,specf,work=sys.argv[1:4]
HERE=os.path.dirname(os.path.abspath(__file__))
lines=open(base).read().split('\n'); os.makedirs(work,exist_ok=True)
def build(name,cuts,subs):
    L=list(lines)
    for a,b in cuts:
        for i in range(a-1,b): L[i]=None
    txt='\n'.join(l for l in L if l is not None)
    for old,new in subs:
        assert txt.count(old)==1,('inlocuire fara exact o aparitie',old[:60])
        txt=txt.replace(old,new)
    p=f'{work}/v_{name}.tex'; open(p,'w').write(txt); return p
def pos_of(d):
    out=subprocess.run(['python3',f'{HERE}/measure.py',d],capture_output=True,text=True).stdout
    m=re.search(r'corpul se termina la pos (\d+)',out); return float(m.group(1)) if m else None, out
def run(s):
    name,cuts,subs=s[0],s[1],(s[2] if len(s)>2 else [])
    p=build(name,cuts,subs); d=f'{work}/v_{name}'
    info=subprocess.run([f'{HERE}/compile.sh',p,d],capture_output=True,text=True).stdout.replace('\n',' | ')
    pos,_=pos_of(d); return name,pos,info
spec=[['ctrl',[]]]+json.load(open(specf))
with ThreadPoolExecutor(4) as ex: res=list(ex.map(run,spec))
ref=res[0][1]
for name,pos,info in res:
    print(f'{name:28s} pos {pos:.0f}  castig {ref-pos:6.0f} pt = {(ref-pos)/704:.2f} coloane = {(ref-pos)/1408:.2f} pagini   {info}')
