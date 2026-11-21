#!/bin/zsh
# Compileaza o copie a documentatiei intr-un director gol.
# Folosire: docs/scurtare_tools/compile.sh <fisier.tex> <director_iesire>
# Copiaza .tex, acl.sty, acl_natbib.bst si figures/ din Paper/Articol_Multilingv/, ruleaza pdflatex, bibtex,
# pdflatex de doua ori (inca o data daca logul zice "Label(s) may have changed"), apoi numara erorile.
SRC=/Users/alexandrucojoaca/Documents/GitHub/ia-sahistii/Paper/Articol_Multilingv
T=$1; D=$2
rm -rf $D; mkdir -p $D
cp $T $D/documentatie_overleaf.tex
cp $SRC/acl.sty $SRC/acl_natbib.bst $D/
cp -r $SRC/figures $D/figures
cp $SRC/figures/* $D/
cd $D
pdflatex -interaction=nonstopmode documentatie_overleaf.tex >/dev/null 2>&1
bibtex documentatie_overleaf >/dev/null 2>&1
pdflatex -interaction=nonstopmode documentatie_overleaf.tex >/dev/null 2>&1
pdflatex -interaction=nonstopmode documentatie_overleaf.tex >/dev/null 2>&1
if grep -q 'Label(s) may have changed' documentatie_overleaf.log; then pdflatex -interaction=nonstopmode documentatie_overleaf.tex >/dev/null 2>&1; fi
python3 - <<'PY'
import re
l=open('documentatie_overleaf.log',errors='ignore').read()
print('erori',len(re.findall(r'^!',l,re.M)),'| undefined',len(re.findall(r'undefined',l,re.I)),'| overfull',len(re.findall(r'Overfull',l)),
      '| pagini',re.findall(r'Output written on .*\((\d+) pages',l))
PY
pdftotext -layout documentatie_overleaf.pdf out.txt
python3 -c "print('?? in pdf:',open('out.txt').read().count('??'))"
