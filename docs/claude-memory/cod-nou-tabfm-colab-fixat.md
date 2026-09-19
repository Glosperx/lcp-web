---
name: cod-nou-tabfm-colab-fixat
description: "25 aug 2026 - tabfm_colab.ipynb avea 3 bugi reale (HF_HOME setat dupa import tabfm, output de calibrare stale, celula de calibrare fara instaleaza_patch_uri); toate fixate si validate cu o rulare completa pe T4, 12/12 cereri, 142 min, fara OOM"
metadata: 
  node_type: memory
  type: project
  originSessionId: f3a4641f-367e-4f24-b328-31e01a9ad334
  modified: 2026-08-25T13:48:57.267Z
---

`tabfm_colab.ipynb` (rularea TabFM pe T4 in Colab pentru semnalul A) a fost verificat linie cu linie
si avea trei bugi reale, confirmate pe sursa reala din `tabfm`/`huggingface_hub` (nu presupuse):

1. **`HF_HOME` setat DUPA `import tabfm`.** `huggingface_hub/constants.py` calculeaza `HF_HOME` ca o
   constanta de modul, o singura data, la import. `import tabfm` (in vechea celula de instalare)
   importa `huggingface_hub` transitiv, deci setarea de mai tarziu n-avea niciun efect: caching-ul
   checkpointului de 6.59 GB in Drive nu functiona NICIODATA, fiecare sesiune redescarca tot, tacut.
   Fix: mount Drive + `HF_HOME` mutate intr-o celula noua, inaintea instalarii.
2. **Output-ul celulei de calibrare era stale.** Cifrele salvate (T=1700/3200, extrapolare 4.4x)
   corespundeau exact versiunii VECHI si buguite pe care comentariile codului CURENT o descriau ca
   fiind deja reparata (codul curent masoara direct la T=14107, cererea intreaga, nu extrapoleaza).
   Fix: sters output-ul vechi, ca sa nu induca in eroare pana la o rulare noua.
3. **Celula de calibrare nu apela `instaleaza_patch_uri()`.** Markdown-ul o descria pe cea care
   instaleaza patch-urile drept "optionala", dar fara ele, chiar calibrarea (nu doar rularea reala)
   ar crapa cu OOM brut la T=14107. Fix: apel explicit adaugat la inceputul celulei de calibrare.

## Validat end-to-end, nu doar teoretic

Dupa fix, rularea pe un T4 real a mers curat: patch-uri instalate (atentie 9.5e-07, memorie exact 0),
calibrare la T=14107 masurata direct (nu extrapolata): varf 8.52 GiB din 14.6 GiB, marja 4.88 GiB.
Rularea completa (12 cereri, `n_estimators=8`, `TABFM_MAXFEAT=160`) a facut **12/12 in 142 minute**,
toate predictiile finite, zero OOM. Consumul local (`--regressor tabfm-cache`) a mers fara nicio
eroare de potrivire a cheilor.

## Ce s-a facut cu rezultatul

Predictiile TabFM de aici au alimentat retestarea axei [[axa-regresorului-inchisa]] pe `proj-394`, cu
fuziune reala prin `fuse_ab.py`. Concluzia acelei axe ramane inchisa (castig de +0.0002 in fuziune,
sub zgomot), dar acum cu cifre pe spatiul corect, nu doar pe `proj-200`.

## Al patrulea bug, gasit pe 26 aug: `files.download()` nu functioneaza din VSCode

Celula de arhiva (`sectiunea 9`) cheama `google.colab.files.download(z)`, care merge prin
**JavaScript injectat in frontendul web al Colab**. Notebook-ul asta se ruleaza din VSCode pe kernel
Colab, deci JS-ul e returnat si nimeni nu-l executa: celula raporteaza succes, tipareste marimea
arhivei, si **nu se descarca nimic**. Semnul care o dovedeste, si care merita cautat: output-ul
celulei contine `['<IPython.core.display.Javascript object>']` in loc de un fisier. Se vede si in
output-ul salvat al rularii de la 160, deci trapa exista de atunci.

Ruta care merge: se scrie arhiva in **Drive**, nu in `/content`, si se ia din interfata web a
Drive-ului.

    z = shutil.make_archive(os.path.join(LUCRU, os.path.basename(DEST)), 'zip', DEST)

(`os.path.basename(DEST)` in loc de numele fixat `preds_proj394` e deja in notebook, altfel arhiva
de la 256 iesea cu numele celei de la 160.)

## Un lucru lasat deschis, deliberat

`output/e1_frozen_preds_tf-proj-394_reg-tabfm-cache_lemma_fert_inloc.csv` e acum copia rularii de la
**256**. Cele doua variante explicite exista ca `_mf160` si `_mf256`, dar numele canonic ramane
ambiguu: `_p()` il construieste din flag-uri, iar `TABFM_CACHE` nu intra in nume, deci orice rulare
noua il suprascrie tacut. `analysis_regresor.py` citeste NUMAI numele canonic (`CANDIDATI` in
`analysis_regresor.py:44`), de asta n-a fost sters. Cine reia: copiaza intai varianta dorita peste
numele canonic, ca in [[tabfm-maxfeat256-rezultatul]].
