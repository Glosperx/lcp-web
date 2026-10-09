---
name: zsh-nu-accepta-comentarii-in-comenzi
description: Shell-ul lui interactiv nu trateaza # ca si comentariu, deci comenzile date lui nu au voie cu comentarii pe linie.
metadata:
  type: feedback
---

I-am dat doua comenzi cu comentariu explicativ dupa `#` pe aceeasi linie. In zsh-ul lui
interactiv optiunea `interactive_comments` e stinsa, deci `#` a ajuns argument:

```
git reset --soft HEAD~1              # desface commit-ul
  -> fatal: Cannot do soft reset with paths.
git push --force-with-lease origin alex_llm   # readuce remote-ul
  -> error: src refspec # does not match any
```

**Why:** in scripturi non-interactive comentariile merg, deci capcana apare exact cand
scriu comenzi pentru el sa le copieze, nu cand rulez eu prin Bash. Mesajele de eroare nu
arata deloc spre cauza reala, par probleme de git.

**How to apply:** comenzile pe care i le dau sa le copieze se scriu curate, una per bloc,
fara `#` pe linie. Explicatia merge in text deasupra blocului.
