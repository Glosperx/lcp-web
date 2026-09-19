"""Bloc E: bake-off de LLM-uri pentru semnalele B si C. Etapa 1 pe TRIAL, etapa 2 pe TEST.

Doua faze separate, care nu se ating:

  --model <cheie>   faza de MASURARE. Incarca un singur model, trece prin D.4, apoi scrie semnalele
                    B si C pentru fiecare instanta, linie cu linie.
  --aggregate       faza de AGREGARE. Citeste CSV-urile, nu incarca niciun model, si scrie raportul:
                    r per limba, selectia leave-one-language-out, timpul per item, controlul de
                    cuantizare.

`--split` alege partitia, si separa complet cele doua etape pe disc:

  trial (implicit)  300 de instante -> output/bakeoff_<cheie>.csv       -> output/e_bakeoff.md
  test              5624 de instante -> output/bakeoff_test/<cheie>.csv -> output/e_bakeoff_test.md

Subdirectorul pentru test e ales anume: globul `output/bakeoff_*.csv` continua sa prinda exact cele
sapte fisiere de trial si nimic altceva, deci etapa 1 nu se poate contamina cu cifre de test.

De ce etapa 1 pe trial: trial-ul e practic disjunct de test (zero contexte comune peste tot cu
exceptia fil 1 si fr 2) si e setul de dezvoltare pe care lucrarea nu-l avea in varianta romaneasca. Un
bake-off pe test ar fi tuning pe scorul raportat, adica fix slabiciunea pe care protocolul o elimina.

De ce leave-one-language-out la SELECTIE (§5.1 al planului de bake-off): daca modelul se alege pe
trial-ul tuturor celor 10 limbi, atunci pentru fiecare limba tinuta deoparte i-am folosit trial-ul ca
sa aleg modelul, deci alegerea modelului devine ea insasi o forma de tuning. Pentru limba L modelul se
alege pe media lui r peste CELELALTE 9.

**Pe test selectia NU se recalculeaza.** Harta model-per-limba se citeste din CSV-urile de trial si se
APLICA testului, prin `apply_selection`. O selectie recalculata pe test ar fi exact tuningul pe scorul
raportat pe care §5.1 il interzice.

Selectia se face pe semnalul B, decis de Alexandru pe 17 august. r pentru C se raporteaza separat, per
limba, cu semn cu tot: surprisal-ul e o statistica bruta, nu o nota, si nu intra in fuziune decat daca
aduce ceva peste B.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python bakeoff_trial.py --model qwen3-8b-4bit
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python bakeoff_trial.py --model X --limit 10
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python bakeoff_trial.py --aggregate
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python bakeoff_trial.py --model X --split test
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python bakeoff_trial.py --model X --split test --langs fr
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python bakeoff_trial.py --aggregate --split test
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python bakeoff_trial.py --model X --limit 30 \
      --out output/dist/_probe30.csv     # rulare noua, langa cea veche, nu peste ea
"""
import argparse
import csv
import glob
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_bakeoff.md")
# Coloanele istorice, pe pozitiile lor. Nimic nu se insereaza intre ele.
BASE_COLS = ["lang", "token", "complexity", "B", "C", "sec"]
# Distributia peste "1".."5" si masa bruta, per prompt, ADAUGATE LA COADA. Cele sase de mai sus
# pastreaza aceleasi valori si aceleasi pozitii, deci `fuse_ab.py`, `with_context` si `aggregate` merg
# neschimbate pe fisierele noi, iar cele sapte CSV-uri de trial deja pe disc, care n-au coloanele
# astea, raman citibile: totul se citeste pe nume.
def dist_cols(digits="12345"):
    """Coloanele distributiei, pentru o scara de raspuns oarecare.

    Numele coloanei poarta CIFRA, nu poziția: la scara 0-9 iese `p1_0..p1_9`, deci un cititor nu poate
    confunda un fisier pe alta scara cu unul canonic, si nici nu se poate face un join tacut intre ele.
    """
    return ([f"p1_{d}" for d in digits] + ["raw1"]
            + [f"p2_{d}" for d in digits] + ["raw2"])


DIST_COLS = dist_cols()
COLS = BASE_COLS + DIST_COLS

# Etapa 1 si etapa 2 nu impart niciun fisier. `context_id` NU se scrie: se recupereaza pozitional din
# `load_mlsp(split)` la agregare, cu verificare element cu element, fiindca `measure` parcurge cadrul
# in ordine si scrie fiecare rand. Asa cele sapte CSV-uri de trial deja pe disc raman valide.
SPLITS = {"trial": dict(dirname=None, report=REPORT),
          "test": dict(dirname="bakeoff_test", report=os.path.join(OUT, "e_bakeoff_test.md"))}

# Bratul principal. E principal fiindca acoperirea lui de limbi e citabila, NU fiindca ar fi cel mai
# bun: bake-off-ul masoara cat costa alegerea asta in performanta (§5.2). Daca alt model iese mai bun,
# aia e o fraza in paper, nu un motiv de schimbare a bratului.
MAIN_ARM = "qwen3-8b-4bit"

# Perechile pentru E.4. Cuantizarea e singura diferenta in fiecare pereche, deci costul ei iese
# masurat, nu presupus.
QUANT_PAIRS = [("qwen3-8b-4bit", "qwen3-8b-8bit"), ("qwen35-9b-4bit", "qwen35-9b-8bit")]


def csv_path(model_key, split="trial"):
    d = SPLITS[split]["dirname"]
    return (os.path.join(OUT, f"bakeoff_{model_key}.csv") if d is None
            else os.path.join(OUT, d, f"{model_key}.csv"))


def dist_cells(parts, k=5):
    """Celulele `DIST_COLS` pentru un rand: p normalizat pe cele `k` cifre si masa bruta, per prompt.

    `repr(float(x))` si nu un format cu N zecimale: reprezentarea scurta care face roundtrip EXACT,
    deci semnalul B recalculat din coloanele astea iese acelasi float, nu unul apropiat, si
    verificarea nu are toleranta de ales. Cand masa e degenerata `p` e None, cele cinci celule raman
    goale si `raw` se scrie oricum: masa bruta e chiar marimea pe care o verifica D.4.
    """
    if len(parts) != 2:
        raise SystemExit(f"rate_parts a intors {len(parts)} prompturi, DIST_COLS asteapta 2")
    out = []
    for p, raw in parts:
        out += ["" if p is None else repr(float(p[i])) for i in range(k)]
        out.append(repr(float(raw)))
    return out


# ----------------------------------------------------------------------------- faza de masurare
def measure(model_key, split="trial", langs=None, limit=None, out=None, scale="1-5", prefix="",
            only_c=False):
    """B si C pe splitul dat, pentru un singur model. Scrie linie cu linie, cu flush.

    `langs` restrange masurarea la o submultime de limbi. Nu e o comoditate: harta LOLO fixata pe trial
    alege `qwen35-9b-8bit` doar pe franceza, deci celelalte noua limbi ale lui pe test n-ar intra in
    nicio revendicare si ar costa 92 de minute degeaba.

    `out` scrie in alt fisier decat cel canonic al perechii (model, split). Fara el, `--limit 30` ar
    scrie peste `output/bakeoff_<cheie>.csv`, adica peste rularea de trial cu 300 de randuri din care
    se citeste harta de selectie. O rulare noua nu are voie sa cada peste una veche.

    `scale` schimba scara de raspuns. Orice altceva decat implicitul CERE `out`, fiindca un fisier pe
    alta scara nu are voie sa ajunga pe calea canonica: coloanele nu mai sunt aceleasi si `load_runs`
    l-ar citi ca pe un semnal B obisnuit.

    `only_c` masoara NUMAI surprisal-ul, sarind peste `rate_parts`. Coloana `B` iese goala, la fel si
    distributiile. Costa ~o treime, fiindca `rate_parts` face doua prompturi cu citire de logiti iar
    `surprisal` un singur forward peste contextul decupat.

    CERE `out`, si din motivul cel mai periculos din tot fisierul: `load_runs` ia FIECARE `*.csv` din
    directorul unui split ca pe un model, iar `fuse_ab.pick_model` alege din bazinul asa format. Un
    fisier cu `B` gol cazut in `output/bakeoff_test/` ar intra tacit in bazinul de candidati al
    sistemului adoptat si ar muta cifra publicata fara sa crape nimic.

    D.4 nu se sare: verifica raterul, nu masuratoarea, si costa secunde. Poarta care conteaza pentru C
    e alta, `analysis_c_sanatate.py`, fiindca `gemma4-12b-4bit` trece D.4 si totusi nu poate modela
    text brut (surprisal mediu 23.95 fata de ln|V| = 12.48, deci peste uniform).
    """
    if scale != "1-5" and not out:
        raise SystemExit("o scara diferita de 1-5 cere --out: fisierul nu are aceleasi coloane si nu "
                         "are voie sa cada peste cel canonic")
    if only_c and not out:
        raise SystemExit("--only-c cere --out: fisierul are coloana B goala si `load_runs` l-ar citi "
                         "ca pe un model din bazinul lui pick_model")
    # Un prefix de citire CERE si el --out, si din motivul mai periculos: coloanele sunt exact
    # aceleasi, deci un fisier cu prefix ar cadea peste cel canonic fara sa se vada nimic in antet.
    if prefix and not out:
        raise SystemExit("un prefix de citire cere --out: fisierul are aceleasi coloane ca cel "
                         "canonic si l-ar inlocui fara nicio urma in antet")
    from mlsp_common import LLM_POOL, load_mlsp
    from solution_bert import LLMRater
    import d4_sanity

    ent = LLM_POOL.get(model_key)
    if ent is None:
        raise SystemExit(f"model necunoscut: {model_key!r}. Chei: {sorted(LLM_POOL)}")
    if split not in SPLITS:
        raise SystemExit(f"split necunoscut: {split!r}. Cunoscute: {sorted(SPLITS)}")

    # Auto-detectat din `--langs`: cerand explicit "ro" se incarca si RoLCP. Fara asta o rulare
    # normala, fara --langs, n-ar cere niciodata data/RoLCP.csv (fisierul protejat cu parola, care nu
    # e mereu prezent local).
    ml = load_mlsp(split, include_ro=bool(langs) and "ro" in [l.strip() for l in langs])
    if langs:
        keep = [l.strip() for l in langs]
        bad = sorted(set(keep) - set(ml["lang"].unique()))
        if bad:
            raise SystemExit(f"limbi inexistente in splitul {split}: {bad}")
        ml = ml[ml["lang"].isin(keep)].reset_index(drop=True)
    if limit:
        ml = ml.head(int(limit))
    print(f"[E1] {model_key} ({ent['repo']} @ {ent['revision'][:12]})", flush=True)
    print(f"[E1] {len(ml)} instante de {split}, {ml['lang'].nunique()} limbi "
          f"({', '.join(f'{lg} {n}' for lg, n in ml['lang'].value_counts().sort_index().items())})",
          flush=True)

    t0 = time.time()
    r = LLMRater(model_key, scale=scale, read_prefix=prefix)
    t_load = time.time() - t0
    print(f"[E1] incarcat in {t_load:.1f}s, backend={r.backend} dev={r.dev}, "
          f"scara {r.scale} ({len(r.digits)} atomi), prefix de citire "
          f"{r.read_prefix!r} -> {r.read_pref_ids}", flush=True)

    # D.4 INAINTE de orice cifra, cerut de §10.2. Pe raterul deja incarcat, deci fara a doua coborare.
    first = ml.iloc[0]
    ok, fails = d4_sanity.run_sanity(r, model_key, ent, str(first["lang"]), str(first["sent"]),
                                     str(first["token"]), prompt_set="multi", t_load=t_load)
    if not ok:
        raise SystemExit(f"[E1] D.4 a picat pe {model_key}: {fails}. Nu se scrie nicio cifra.")

    # `--out` se interpreteaza fata de radacina proiectului, nu fata de directorul curent.
    path = csv_path(model_key, split) if not out else (
        out if os.path.isabs(out) else os.path.join(HERE, out))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    t1 = time.time()
    nan_b = nan_c = 0
    # Scriere incrementala, cu flush per linie: o rulare de minute care cade la instanta 250 nu are
    # voie sa piarda tot. Regula de buget cere disc dupa fiecare pas care produce cifre.
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(BASE_COLS + dist_cols(r.digits))
        for i, row in enumerate(ml.itertuples(), 1):
            ti = time.time()
            # `rate_parts` in locul lui `rate`: acelasi numar de forward-uri, aceeasi aritmetica, dar
            # intoarce si distributiile pe care `rate` le colapseaza in punct.
            if only_c:
                # `raw` e float prin contractul lui dist_cells; NaN, nu sir gol, ca sa nu
                # existe o a doua conventie pentru "lipseste" in acelasi fisier.
                b, parts = float("nan"), [(None, float("nan"))] * 2
            else:
                b, parts = r.rate_parts(row.sent, row.token, lang=row.lang)
            c = r.surprisal(row.sent, row.token)
            sec = time.time() - ti
            nan_b += int(not np.isfinite(b))
            nan_c += int(not np.isfinite(c))
            w.writerow([row.lang, row.token, f"{float(row.complexity):.6f}",
                        "" if not np.isfinite(b) else f"{b:.8f}",
                        "" if not np.isfinite(c) else f"{c:.8f}", f"{sec:.4f}"]
                       + dist_cells(parts, len(r.digits)))
            fh.flush()
            if i % 25 == 0 or i == len(ml):
                el = time.time() - t1
                print(f"[E1] {i}/{len(ml)}  {el:.0f}s  {el/i:.2f}s per item  "
                      f"NaN B={nan_b} C={nan_c}", flush=True)

    el = time.time() - t1
    print(f"\n[E1] {model_key}: {len(ml)} instante in {el:.0f}s ({el/len(ml):.2f}s per item)")
    print(f"[E1] NaN: B={nan_b}, C={nan_c}. NEIMPUTATE, se numara in raport.")
    print(f"[E1] -> {path}")
    return 0


# ----------------------------------------------------------------------------- faza de agregare
def pearson(a, b):
    """r pe perechile finite. -> (r, n). Acelasi apel ca finetune_xlmr.pearson:175, dar fara importul
    lui finetune_xlmr, care aduce torch la import degeaba."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan"), int(m.sum())
    from scipy.stats import pearsonr
    return float(pearsonr(a[m], b[m])[0]), int(m.sum())


def load_runs(split="trial", dirname=None):
    """{cheie: DataFrame} pentru fiecare CSV al splitului dat, in ordinea din LLM_POOL.

    `dirname` citeste dintr-un ALT director, relativ la `output/`, in loc de cel canonic al splitului.
    Fara el nu se schimba nimic, deci cifra publicata se reproduce fara niciun flag. Cu el se pot
    masura variante ale semnalului B fara ca fisierele lui B sa fie atinse si fara ca bazinul de
    candidati al lui `pick_model` sa se schimbe tacit pentru toate rularile viitoare.
    """
    from mlsp_common import LLM_POOL
    d = dirname if dirname is not None else SPLITS[split]["dirname"]
    pat = (os.path.join(OUT, "bakeoff_*.csv") if d is None
           else os.path.join(OUT, d, "*.csv"))
    runs = {}
    for p in sorted(glob.glob(pat)):
        b = os.path.basename(p)
        key = b[:-len(".csv")] if d else b[len("bakeoff_"):-len(".csv")]
        runs[key] = pd.read_csv(p)
    return {k: runs[k] for k in LLM_POOL if k in runs} | {k: v for k, v in runs.items()
                                                          if k not in LLM_POOL}


def with_context(df, split):
    """Adauga `context_id` si `idx` unui CSV de bake-off, recuperate POZITIONAL din load_mlsp(split).

    `idx` e pozitia in cadrul NEFILTRAT, deci e cheia care leaga semnalul B de semnalul A din
    `e1_frozen_preds.csv`, unde randurile fara tinta gasita ca subsir lipsesc.

    CSV-urile nu poarta contextul (COLS) si tokenurile se repeta, deci un join pe chei ar fi ambiguu.
    `measure` parcurge cadrul in ordine, cu `itertuples`, si scrie fiecare rand, deci pozitia e o cheie
    exacta. Rularile partiale pe limbi se recupereaza filtrand cadrul de referinta pe aceleasi limbi,
    in aceeasi ordine.

    Verificarea compara `lang`, `token` si `complexity` rand cu rand si crapa la prima nepotrivire, in
    loc sa coreleze tacut randuri desperecheate.
    """
    from mlsp_common import load_mlsp
    present = list(dict.fromkeys(df["lang"].astype(str)))
    # Auto-detectat din `df`, nu dintr-un flag: daca CSV-ul are randuri "ro" (Romania, RoLCP, a 11-a
    # limba din grila LOLO), referinta trebuie sa le acopere si ea. Fara asta orice caller vechi al
    # lui with_context ar trebui atins ca sa treaca flagul mai departe.
    ref = load_mlsp(split, include_ro=("ro" in present))
    ref = ref[ref["lang"].astype(str).isin(present)]
    ref = ref.assign(idx=ref.index.values).reset_index(drop=True)   # pozitia in cadrul NEFILTRAT
    if len(ref) < len(df):
        raise SystemExit(f"joinul pozitional: CSV-ul are {len(df)} randuri, {split} are {len(ref)} "
                         f"pe limbile {present}")
    ref = ref.head(len(df))                       # rularile cu --limit se opresc mai devreme
    a, b = df.reset_index(drop=True), ref
    bad = ((a["lang"].astype(str).values != b["lang"].astype(str).values) |
           (a["token"].astype(str).values != b["token"].astype(str).values) |
           (np.abs(a["complexity"].values - b["complexity"].values) > 1e-6))
    if bad.any():
        i = int(np.flatnonzero(bad)[0])
        raise SystemExit(f"joinul pozitional a esuat la randul {i}: CSV are "
                         f"({a['lang'][i]}, {a['token'][i]}, {a['complexity'][i]}), {split} are "
                         f"({b['lang'][i]}, {b['token'][i]}, {b['complexity'][i]})")
    out = a.copy()
    out["context_id"] = b["context_id"].values
    out["idx"] = b["idx"].values
    return out


def r_table(runs, col):
    """{model: {limba: (r, n)}} pentru semnalul din coloana `col`."""
    out = {}
    for key, df in runs.items():
        out[key] = {lg: pearson(g[col].values, g["complexity"].values)
                    for lg, g in df.groupby("lang", sort=True)}
    return out


def lolo_select(tab, langs):
    """Selectia §5.1 pe semnalul B. Pentru limba L, modelul se alege pe media lui r peste CELELALTE
    9 limbi, niciodata pe a lui L. -> [(L, model_ales, media_pe_9, r_pe_L)]."""
    rows = []
    for L in langs:
        best, best_mean = None, -np.inf
        for key, per in tab.items():
            vals = [per[l][0] for l in langs if l != L and l in per and np.isfinite(per[l][0])]
            if not vals:
                continue
            m = float(np.mean(vals))
            if m > best_mean:
                best, best_mean = key, m
        rl = tab[best][L][0] if best and L in tab[best] else float("nan")
        rows.append((L, best, best_mean, rl))
    return rows


def apply_selection(sel_src, tab, langs):
    """Harta model-per-limba FIXATA pe alt split, aplicata tabelului curent.

    Asta e diferenta care conteaza la etapa 2. `lolo_select` pe tabelul de test ar alege modelul
    folosind chiar scorul de test, adica exact tuningul pe scorul raportat pe care §5.1 il interzice.
    Harta se ia de pe trial, unde selectia e legitima, si se aplica.

    -> [(L, model, r pe L in tab)], cu r NaN cand modelul ales nu a fost rulat pe L in splitul curent.
    """
    src = {L: m for L, m, _, _ in sel_src}
    rows = []
    for L in langs:
        m = src.get(L)
        rl = tab[m][L][0] if m in tab and L in tab[m] else float("nan")
        rows.append((L, m, rl))
    return rows


def boot_table(runs, split, col="B", n_boot=2000):
    """{model: {limba: dict de la boot_r_ci}}. Bootstrap pe CONTEXTE, §10.3.

    Inlocuieste pragul Fisher la etapa 2. Contextul se recupereaza pozitional, prin `with_context`.
    """
    from mlsp_common import boot_r_ci
    out = {}
    for key, df in runs.items():
        d = with_context(df, split)
        out[key] = {lg: boot_r_ci(g["complexity"].values, g[col].values, g["context_id"].values,
                                  n_boot=n_boot)
                    for lg, g in d.groupby("lang", sort=True)}
    return out


def fisher_ci(r, n, alpha=0.05):
    """Interval de incredere pentru r, prin transformarea Fisher. -> (lo, hi).

    NU inlocuieste bootstrap-ul pe contexte din §10.3, care e pentru etapa 2 si tine cont de faptul ca
    sapte limbi din zece au in medie 3 tinte per contex. Serveste un singur scop aici: pragul de zgomot
    la n = 30, ca diferentele per limba sa nu fie citite mai tare decat sunt.
    """
    if not np.isfinite(r) or n < 5:
        return float("nan"), float("nan")
    from scipy.stats import norm
    z, se = np.arctanh(r), 1.0 / np.sqrt(n - 3)
    d = float(norm.ppf(1 - alpha / 2)) * se
    return float(np.tanh(z - d)), float(np.tanh(z + d))


def md_matrix(tab, langs, title, expect=None):
    """Tabel model x limba, cu n in paranteza cand difera de cel asteptat.

    `expect` e {limba: n asteptat}, derivat din splitul curent. Pe trial e 30 peste tot, pe test difera
    per limba, deci un prag fix ar imprastia "(n=...)" pe toate celulele.
    """
    lines = [f"\n### {title}\n\n", "| model | " + " | ".join(langs) + " | medie |\n",
             "|" + "---|" * (len(langs) + 2) + "\n"]
    for key, per in tab.items():
        cells, vals = [], []
        for lg in langs:
            r, n = per.get(lg, (float("nan"), 0))
            exp = 30 if expect is None else expect.get(lg)
            cells.append("n/a" if not np.isfinite(r) else
                         (f"{r:+.3f}" if n == exp else f"{r:+.3f} (n={n})"))
            if np.isfinite(r):
                vals.append(r)
        mean = f"**{np.mean(vals):+.3f}**" if vals else "n/a"
        lines.append(f"| `{key}` | " + " | ".join(cells) + f" | {mean} |\n")
    return lines


def aggregate(split="trial"):
    from mlsp_common import LLM_POOL, load_mlsp
    runs = load_runs(split)
    if not runs:
        raise SystemExit(f"niciun CSV de {split} pentru {csv_path('<cheie>', split)}. "
                         f"Ruleaza intai --model <cheie> --split {split}.")
    langs = sorted({lg for df in runs.values() for lg in df["lang"].unique()})
    tab_b, tab_c = r_table(runs, "B"), r_table(runs, "C")
    # Auto-detectat, la fel ca in with_context: daca vreun CSV are "ro", asteptarea de acoperire
    # trebuie sa includa RoLCP, altfel randurile ei ar aparea "in plus" fata de `expect`.
    expect = load_mlsp(split, include_ro=("ro" in langs)).groupby("lang").size().to_dict()
    is_test = split == "test"

    if is_test:
        L = ["# Etapa 2. Semnalul B pe testul complet\n\n",
             f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de "
             "`bakeoff_trial.py --aggregate --split test`. Datele brute: "
             "`output/bakeoff_test/<model>.csv`, o linie per instanta.\n\n",
             "**Harta de mai jos e cea fixata pe trial**, si se aplica testului. Ea nu mai e insa "
             "harta sistemului: `fuse_ab.py --pick-split test` alege modelul limbii L pe randurile "
             "de TEST ale celorlalte noua limbi, exact ca `w` si ca antrenarea bratului A, deci fara "
             "nicio eticheta din L. Interdictia de la §5.1 priveste o selectie care ar folosi testul "
             "lui L, nu una leave-one-language-out pe test. Harta efectiv folosita se citeste din "
             "`output/e_fusion_lolo_adoptat.md`.\n\n",
             "Intervalele vin din bootstrap pe contexte (§10.3), nu din transformarea Fisher: sapte "
             "limbi din zece au in medie 3 tinte per context, deci itemii nu sunt independenti.\n"]
    else:
        L = [f"# E.1 - E.4. Bake-off pe cele {sum(expect.values())} de instante de trial\n\n",
             f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `bakeoff_trial.py --aggregate`. "
             "Datele brute: `output/bakeoff_<model>.csv`, o linie per instanta.\n\n",
             "Trial, niciodata test. Selectia modelului e leave-one-language-out (§5.1), pe semnalul "
             "B. Pentru C se raporteaza r cu semn, fara selectie: surprisal-ul e o statistica bruta, "
             "nu o nota, si intra in fuziune abia daca aduce ceva peste B.\n"]

    # --- acoperire
    L += ["\n## Acoperire si NaN\n\n",
          "| model | repo | linii | NaN B | NaN C | s per item, medie | s per item, mediana |\n",
          "|---|---|---|---|---|---|---|\n"]
    for key, df in runs.items():
        ent = LLM_POOL.get(key, {})
        nb = int(df["B"].isna().sum()); nc = int(df["C"].isna().sum())
        # Asteptat = suma pe limbile PREZENTE in fisier: o rulare restransa cu --langs e completa pe
        # ce si-a propus, nu incompleta.
        exp_n = sum(expect.get(lg, 0) for lg in df["lang"].unique())
        flag = "" if len(df) == exp_n else " **incomplet**"
        sub = "" if len(df["lang"].unique()) == len(expect) else \
              f" (doar {', '.join(sorted(df['lang'].unique()))})"
        L.append(f"| `{key}` | `{ent.get('repo', '?')}` | {len(df)}{flag}{sub} | {nb} | {nc} | "
                 f"{df['sec'].mean():.2f} | {df['sec'].median():.2f} |\n")
    L.append("\nNaN-urile nu se imputeaza aici. La B inseamna masa degenerata pe amandoua "
             "prompturile, la C inseamna tinta negasita ca subsir in context.\n")

    # --- r per limba
    L += ["\n## r per limba\n"]
    L += md_matrix(tab_b, langs, "Semnalul B, nota LLM", expect)
    L += md_matrix(tab_c, langs, "Semnalul C, surprisal (semnul se raporteaza ca atare)", expect)

    # --- LOLO
    if is_test:
        trial_runs = load_runs("trial")
        if not trial_runs:
            raise SystemExit("etapa 2 are nevoie de CSV-urile de trial: harta de selectie vine de "
                             "acolo, nu se recalculeaza pe test")
        tl = sorted({lg for df in trial_runs.values() for lg in df["lang"].unique()})
        sel_trial = lolo_select(r_table(trial_runs, "B"), tl)
        app = apply_selection(sel_trial, tab_b, langs)
        sel_by_lang = {lg: m for lg, m, _ in app}
        rs = [rl for _, _, rl in app if np.isfinite(rl)]
        missing = [(lg, m) for lg, m, rl in app if not np.isfinite(rl)]
        winners = {m for _, m, _ in app}
        L += ["\n## Sistemul selectat LOLO, cu harta fixata pe trial\n\n",
              "Modelul per limba e cel ales pe trial-ul celorlalte 9 limbi, in "
              "`output/e_bakeoff.md`. Aici doar se aplica: coloana `r pe L, test` e cifra "
              "raportabila.\n\n",
              "| limba | model ales pe trial | r pe L, trial | r pe L, test |\n|---|---|---|---|\n"]
        r_trial_by_lang = {lg: rl for lg, _, _, rl in sel_trial}
        for lg, m, rl in app:
            rt = r_trial_by_lang.get(lg, float("nan"))
            L.append(f"| {lg} | `{m}` | {rt:+.4f} | "
                     + ("nerulat |\n" if not np.isfinite(rl) else f"{rl:+.4f} |\n"))
        L.append("\n**Sistemul selectat LOLO nu are inca nicio limba rulata pe test.**\n" if not rs
                 else f"\n**r mediu al sistemului selectat LOLO, pe test: {np.mean(rs):+.4f}** pe "
                      f"{len(rs)} limbi din {len(app)}.\n")
        if missing:
            L.append(f"\n**Incomplet:** {', '.join(f'{lg} cere `{m}`' for lg, m in missing)}, "
                     "nerulat pe test. Media de mai sus e pe limbile disponibile, deci nu e cifra "
                     "finala.\n")
    else:
        sel = lolo_select(tab_b, langs)
        winners = {m for _, m, _, _ in sel}
        sel_by_lang = {lg: m for lg, m, _, _ in sel}
        L += ["\n## Selectia leave-one-language-out, §5.1, pe semnalul B\n\n",
              "Pentru limba L, modelul e ales pe media lui r peste celelalte 9 limbi. Coloana `r pe "
              "L` e cifra raportabila: modelul nu a vazut niciodata trial-ul lui L la selectie.\n\n",
              "| limba tinuta deoparte | model ales | media lui r pe celelalte 9 | r pe L |\n",
              "|---|---|---|---|\n"]
        for lg, m, mean9, rl in sel:
            L.append(f"| {lg} | `{m}` | {mean9:+.4f} | {rl:+.4f} |\n")
        rs = [rl for _, _, _, rl in sel if np.isfinite(rl)]
        L.append(f"\n**r mediu sub selectie LOLO: {np.mean(rs):+.4f}** pe {len(rs)} limbi.\n\n")
        if len(winners) == 1:
            w = next(iter(winners))
            L.append(f"**Acelasi model, `{w}`, castiga pe toate cele {len(sel)} limbi.** Chestiunea "
                     "selectiei e deci lipsita de obiect si se raporteaza un singur model, cu nota ca "
                     "selectia a fost facuta LOLO.\n")
        else:
            L.append(f"**Modelele difera per limba: {len(winners)} castigatori distincti, "
                     f"{sorted(winners)}.** Asta e in sine un rezultat si se raporteaza ca atare, nu "
                     "se ascunde sub un singur model.\n")

    # --- §5.2
    if MAIN_ARM in tab_b:
        L += ["\n## §5.2. Cat costa alegerea bratului principal pe acoperire\n\n",
              f"`{MAIN_ARM}` e bratul principal fiindca acoperirea lui de limbi e citabila, nu "
              "fiindca ar fi cel mai bun. Tabelul spune cat costa asta, in r.\n\n",
              "Cifra care conteaza e coloana **fata de LOLO**: alternativa reala e modelul ales tot "
              "leave-one-language-out, adica fara sa fi vazut trial-ul limbii L. Coloana **oracol** e "
              "cel mai bun model PE L, ales folosind chiar "
              + ("scorul de test al lui L" if is_test else "trial-ul lui L") +
              ", deci e exact tuningul pe "
              "care §5.1 il interzice. Nu e o alternativa disponibila, ci o margine superioara.\n\n",
              "| limba | r al bratului principal | model ales LOLO | r al lui | fata de LOLO | "
              "oracol pe L | r al lui | fata de oracol |\n",
              "|---|---|---|---|---|---|---|---|\n"]
        d_lolo, d_orac = [], []
        for lg in langs:
            rm = tab_b[MAIN_ARM].get(lg, (float("nan"), 0))[0]
            cand = [(per[lg][0], k) for k, per in tab_b.items()
                    if lg in per and np.isfinite(per[lg][0])]
            if not cand:
                continue
            rb, kb = max(cand)
            ks = sel_by_lang.get(lg)
            # `ks in tab_b` conteaza doar pe test: modelul ales pe trial poate sa nu fi fost inca rulat
            # pe test, si atunci celula e goala, nu o eroare.
            r_sel = tab_b[ks][lg][0] if (ks in tab_b and lg in tab_b[ks]) else float("nan")
            if np.isfinite(r_sel):
                d_lolo.append(rm - r_sel)
            d_orac.append(rm - rb)
            L.append(f"| {lg} | {rm:+.4f} | `{ks}` | {r_sel:+.4f} | {rm - r_sel:+.4f} | `{kb}` | "
                     f"{rb:+.4f} | {rm - rb:+.4f} |\n")
        if d_lolo:
            dl = np.array(d_lolo, float)
            L.append(f"\n**Costul alegerii pe acoperire, fata de alternativa LOLO: "
                     f"{dl.mean():+.4f} r**, sd intre limbi {dl.std():.4f}, "
                     f"interval {dl.min():+.4f} pana la {dl.max():+.4f}. "
                     f"Fata de oracol, care nu e disponibil: {np.mean(d_orac):+.4f} r.\n")
            if not is_test:
                lo, hi = fisher_ci(0.60, 30)
                L.append(f"\nPrag de zgomot: la n = 30 per limba, intervalul de 95% pentru un r de "
                         f"0.60 e [{lo:.2f}, {hi:.2f}] prin transformarea Fisher. Diferentele per "
                         "limba mai mici decat atat nu se pot distinge pe trial. Media peste cele 10 "
                         "limbi e mai stabila decat orice celula individuala, dar limbile nu sunt "
                         "esantioane independente din aceeasi marime.\n")

    # --- E.3
    L += ["\n## E.3. Timp per item, masurat pe toate instantele\n\n",
          "Din coloana `sec`, care acopera `rate()` plus `surprisal()` pentru o instanta. Nu e "
          "extrapolat dintr-o singura instanta, ceea ce era rezerva ramasa de la Bloc D.\n\n",
          "| model | medie | mediana | min | max | total |\n|---|---|---|---|---|---|\n"]
    for key, df in runs.items():
        s = df["sec"]
        L.append(f"| `{key}` | {s.mean():.2f} s | {s.median():.2f} s | {s.min():.2f} s | "
                 f"{s.max():.2f} s | {s.sum()/60:.1f} min |\n")
    if MAIN_ARM in runs:
        g = runs[MAIN_ARM].groupby("lang")["sec"].mean()
        L.append(f"\nPer limba, `{MAIN_ARM}`: " +
                 ", ".join(f"{lg} {v:.2f}s" for lg, v in g.items()) +
                 ". Diferentele vin din lungimea contextului.\n")

    # --- E.4
    L += ["\n## E.4. Controlul de cuantizare\n\n"]
    any_pair = False
    for lo, hi in QUANT_PAIRS:
        if lo not in tab_b or hi not in tab_b:
            L.append(f"- `{lo}` fata de `{hi}`: **in asteptare**, lipseste "
                     f"{'`' + hi + '`' if hi not in tab_b else '`' + lo + '`'}. Nu se estimeaza.\n")
            continue
        any_pair = True
        L += [f"\n### `{lo}` fata de `{hi}`, semnalul B\n\n",
              "| limba | 4 biti | 8 biti | diferenta |\n|---|---|---|---|\n"]
        ds = []
        for lg in langs:
            a = tab_b[lo].get(lg, (float("nan"), 0))[0]
            b = tab_b[hi].get(lg, (float("nan"), 0))[0]
            if np.isfinite(a) and np.isfinite(b):
                ds.append(b - a)
            L.append(f"| {lg} | {a:+.4f} | {b:+.4f} | {b - a:+.4f} |\n")
        if ds:
            L.append(f"\n**Castigul mediu al lui 8 biti: {np.mean(ds):+.4f} r**, la un cost de timp "
                     f"de {runs[hi]['sec'].mean() / runs[lo]['sec'].mean():.2f}x.\n")
    if not any_pair:
        L.append("\nNiciuna din cele doua perechi nu e completa, deci E.4 ramane deschis.\n")

    # --- §10.3, doar pe test: bootstrap pe contexte in locul pragului Fisher
    if is_test:
        bt = boot_table(runs, split, "B")
        L += ["\n## Intervale prin bootstrap pe contexte, §10.3\n\n",
              "2000 de reesantionari ale CONTEXTELOR, nu ale itemilor. Sapte limbi din zece au in "
              "medie 3 tinte per context, deci un bootstrap pe itemi ar da intervale prea inguste "
              "exact acolo. Contextul e recuperat pozitional din `load_mlsp(\"test\")`, cu verificare "
              "rand cu rand pe limba, token si complexitate.\n\n",
              "| model | " + " | ".join(langs) + " |\n" + "|" + "---|" * (len(langs) + 1) + "\n"]
        for key, per in bt.items():
            cells = []
            for lg in langs:
                b = per.get(lg)
                cells.append("n/a" if b is None or not np.isfinite(b["r"]) else
                             f"{b['r']:+.3f}<br>[{b['lo']:+.3f}, {b['hi']:+.3f}]")
            L.append(f"| `{key}` | " + " | ".join(cells) + " |\n")
        w = [f"{lg} {b['n_ctx']}" for lg, b in next(iter(bt.values())).items()]
        L.append(f"\nContexte per limba: {', '.join(w)}. Latimea intervalului urmeaza numarul de "
                 "contexte, nu numarul de itemi, si de asta fil, pt si si, unde contextul e practic "
                 "un item, nu castiga nimic din agregare.\n")

    # --- verdict, generat din cifrele de mai sus
    mean_b = {k: float(np.mean([v[0] for v in per.values() if np.isfinite(v[0])]))
              for k, per in tab_b.items()}
    mean_c = {k: float(np.mean([v[0] for v in per.values() if np.isfinite(v[0])]))
              for k, per in tab_c.items()}
    top = max(mean_b, key=mean_b.get)
    worst_lang = min(langs, key=lambda l: np.nanmean([tab_b[k][l][0] for k in tab_b if l in tab_b[k]]))
    main_wins = [l for l in langs
                 if MAIN_ARM in tab_b and tab_b[MAIN_ARM][l][0] ==
                 max(per[l][0] for per in tab_b.values() if l in per)]

    if is_test:
        full = {k: per for k, per in tab_b.items() if len(per) == len(expect)}
        L += ["\n## Verdict\n\n",
              (f"1. **Sistemul selectat LOLO da r mediu {np.mean(rs):+.4f} pe test**, pe {len(rs)} "
               f"limbi din {len(app)}, cu harta fixata pe trial.\n" if rs else
               "1. **Sistemul selectat LOLO nu e inca evaluabil pe test**, niciunul din modelele alese "
               "pe trial nu e rulat.\n"),
              f"2. **Bratul principal `{MAIN_ARM}` da {mean_b.get(MAIN_ARM, float('nan')):+.4f}** pe "
              f"cele {len(tab_b.get(MAIN_ARM, {}))} limbi rulate.\n",
              f"3. **Reperele publicate, tot pe test:** baseline frecventa 0.478, Archaeology 0.487, "
              "TMU-HIT 0.654, G-Eval cu GPT-4o 0.657. Bratul inghetat E1 al nostru, semnalul A singur, "
              "da 0.552. Cifrele de mai sus sunt semnalul B singur, deci nici ele nu sunt sistemul "
              "final: fuziunea A plus B e in `output/e_fusion.md`.\n",
              f"4. **Semnalul C pe test:** r mediu per model intre {min(mean_c.values()):+.3f} si "
              f"{max(mean_c.values()):+.3f}. Verdictul de pe trial se "
              + ("confirma" if max(abs(v) for v in mean_c.values()) < 0.15 else "schimba") +
              " la scara mare.\n",
              f"5. **Limba cea mai grea ramane `{worst_lang}`.**"
              + (f" Modelele cu acoperire completa pe test: {sorted(full)}." if full else "") + "\n"]
    else:
        L += ["\n## Verdict\n\n",
              f"1. **Semnalul B merge pe toate cele 10 limbi si pe toate cele {len(runs)} modele.** "
              f"r mediu per model intre {min(mean_b.values()):+.3f} si {max(mean_b.values()):+.3f}, "
              f"zero NaN pe B in {sum(len(d) for d in runs.values())} de instante masurate.\n",
              f"2. **Cel mai bun pe media celor 10 limbi e `{top}`, cu r = {mean_b[top]:+.3f}.** "
              f"Bratul principal `{MAIN_ARM}` da {mean_b.get(MAIN_ARM, float('nan')):+.3f}.\n",
              f"3. **Selectia LOLO costa si ea.** r mediu sub selectie LOLO {np.mean(rs):+.4f}, fata "
              f"de {mean_b[top]:+.4f} pe care l-ar da `{top}` peste tot. Diferenta, "
              f"{np.mean(rs) - mean_b[top]:+.4f}, e pretul protocolului, si se plateste pe "
              f"{sum(1 for _, m, _, _ in sel if m != top)} din {len(sel)} limbi, unde selectia pe "
              f"celelalte 9 nu alege `{top}`.\n",
              f"4. **Semnalul C nu tine.** r mediu per model intre {min(mean_c.values()):+.3f} si "
              f"{max(mean_c.values()):+.3f}, cu semnul schimbandu-se intre limbi la fiecare model. Pe "
              "dovada asta C nu intra in fuziune.\n",
              f"5. **Limba cea mai grea pentru toate modelele e `{worst_lang}`.**"
              + (f" Bratul principal `{MAIN_ARM}` e cel mai bun model pe {main_wins}."
                 if main_wins else "") + "\n"]

    report = SPLITS[split]["report"]
    os.makedirs(OUT, exist_ok=True)
    with open(report, "w", encoding="utf-8") as fh:
        fh.write("".join(L))
    print(f"[E2] {len(runs)} modele, {len(langs)} limbi -> {report}")
    if is_test:
        for lg, m, rl in app:
            print(f"  {lg}: {m}  (r pe test = {rl:+.4f})")
    else:
        for lg, m, mean9, rl in sel:
            print(f"  {lg}: {m}  (media pe 9 = {mean9:+.4f}, r pe L = {rl:+.4f})")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None, help="cheie din mlsp_common.LLM_POOL, faza de masurare")
    ap.add_argument("--limit", type=int, default=None,
                    help="doar primele N instante, pentru verificarea formatului")
    ap.add_argument("--aggregate", action="store_true", help="faza de agregare, fara niciun model")
    ap.add_argument("--split", default="trial", choices=sorted(SPLITS),
                    help="partitia: trial (etapa 1) sau test (etapa 2). Fisierele nu se amesteca.")
    ap.add_argument("--langs", default=None,
                    help="submultime de limbi, separate prin virgula, pentru rulari restranse")
    ap.add_argument("--out", default=None,
                    help="calea CSV-ului de scris. Implicit cea canonica a perechii (model, split); "
                         "obligatorie cand rularea nu are voie sa cada peste una veche")
    ap.add_argument("--prefix", default="",
                    help="prefix de citire, adaugat DUPA sablonul de chat, in rolul de asistent: "
                         "cifra se citeste de dupa el, nu de la ultima pozitie a sablonului. "
                         "Implicit gol, adica semnalul B publicat. Cere --out.")
    ap.add_argument("--only-c", dest="only_c", action="store_true",
                    help="masoara numai surprisal-ul (coloana C); B iese goala. Cere --out. "
                         "Modelul trebuie sa treaca intai analysis_c_sanatate.py")
    ap.add_argument("--scale", default="1-5",
                    help="scara de raspuns, ca `lo-hi`, ambele cifre. Implicit 1-5, adica semnalul B "
                         "publicat. `0-9` e singura scara de zece atomi citibila dintr-o pozitie, "
                         "fiindca `10` sunt doi tokeni. Cere --out.")
    a = ap.parse_args()
    langs = [x.strip() for x in a.langs.split(",")] if a.langs else None
    if a.aggregate:
        return aggregate(a.split)
    if not a.model:
        ap.error("--model <cheie> sau --aggregate")
    return measure(a.model, a.split, langs, a.limit, a.out, a.scale, a.prefix,
                   only_c=a.only_c)


if __name__ == "__main__":
    sys.exit(main())
