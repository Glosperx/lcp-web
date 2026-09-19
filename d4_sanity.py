"""D.4: testul de sanatate al lui LLMRater, obligatoriu per model inainte de orice rulare mare.

De ce exista. Semnalul B citeste masa de probabilitate peste id-urile care se decodeaza ca "1".."5"
la ultima pozitie. Doua lucruri il pot rupe in tacere, fara nicio exceptie si cu cifre plauzibile:

  1. tokenizerul modelului sparge cifra altfel, deci self.digit[d] iese gol si suma e mereu 0;
  2. modul de gandire e activ, deci logits[-1] da distributia peste deschiderea blocului <think>,
     nu peste cifre.

Testul ruleaza pe propozitii reale din TRIAL (niciodata test) si nu citeste nicio eticheta: e test de
mecanism, nu de performanta. Criteriul 5 se masoara pe cate o instanta per limba, zece in total,
fiindca un semnal B constant nu se vede pe una singura, iar el e cel care ar face Pearson r nedefinit.

Nota despre garda de gandire. Verificarea "promptul nu contine <think>" ar fi GRESITA: la Qwen3-8B
configuratia corecta (enable_thinking=False) chiar CONTINE <think>, sub forma blocului inchis
"<think>\\n\\n</think>\\n\\n", iar cea rupta nu-l contine deloc. Se verifica deci blocul INCHIS, plus
faptul ca la Qwen3.5 promptul nu se termina pe un <think> deschis, plus masa nedegenerata, care e
singurul criteriu care prinde Qwen3-8B.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python d4_sanity.py --model qwen3-8b-4bit
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python d4_sanity.py --check-pool
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python d4_sanity.py --model qwen3-8b-4bit \
      --no-thinking-guard      # control: se ASTEAPTA sa pice, altfel garda nu masoara nimic
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python d4_sanity.py --model qwen3-8b-4bit \
      --prompt-set legacy      # prompturile romanesti ale caii vechi, pentru comparatie

`run_sanity()` e apelabila si din bakeoff_trial.py, pe un rater deja incarcat: garda cerută de §10.2 al
planului de bake-off trebuie sa treaca inainte de orice cifra, iar modelul nu se incarca de doua ori.
"""
import argparse
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
LOG = os.path.join(OUT, "d4_sanity.md")

# Praguri. MASS_MIN a fost validat pe date la Bloc D: cu 5.17e-06 (Qwen3.5 fara garda) _once() intoarce
# tacut 0.0378 in loc de 0.5942, deci pragul vechi de 1e-9 lasa sa treaca numere gresite.
MASS_MIN = 1e-3        # masa bruta peste cele 5 cifre, inainte de normalizare
# CONC_MAX a fost, pana pe 17 august, criteriu de FAIL pe o SINGURA instanta. Masurat pe date, forma
# aia respingea semnale bune: Aya Expanse pune 0.99993 din masa pe cifra 3 la instanta `ca` si totusi
# da 10 valori distincte pe cele 10 limbi, sd 0.1163, adica mai multa dispersie decat Qwen3-8B (sd
# 0.0474). In plus Qwen3-8B insusi atinge 0.9933 pe engleza, la un fir de prag. A ramas AVERTISMENT.
CONC_MAX = 0.999
# Criteriul 5, in forma pe care o intentiona: ce ar rupe bake-off-ul nu e o instanta decisa, ci un B
# constant, fiindca atunci Pearson r e nedefinit. Se masoara pe cate o instanta per limba.
SPREAD_MIN = 0.01      # sd minima a lui B peste cele 10 limbi
SPREAD_MIN_OK = 6      # cate din cele 10 trebuie sa iasa finite


def note(text):
    os.makedirs(OUT, exist_ok=True)
    new = not os.path.exists(LOG)
    with open(LOG, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# D.4: testul de sanatate al lui LLMRater\n\n"
                     "Un bloc per rulare, adaugat la sfarsit. Propozitia vine din splitul TRIAL,\n"
                     "fara citirea vreunei etichete. Pragurile: masa bruta >= "
                     f"{MASS_MIN}, concentrare <= {CONC_MAX}.\n")
        fh.write(text)


def check_pool():
    """LLM_POOL si download_pool.py trebuie sa aiba aceleasi SHA-uri. Divergenta lor ar schimba
    cifrele in tacere, ceea ce e exact ce previne regula revision=."""
    from mlsp_common import LLM_POOL
    import download_pool
    dl = {d["repo"]: d["revision"] for d in (download_pool.POOL + download_pool.CONTROL_8BIT)}
    bad = []
    for key, ent in LLM_POOL.items():
        got = dl.get(ent["repo"])
        if got is None:
            bad.append(f"  {key}: {ent['repo']} nu apare in download_pool.py")
        elif got != ent["revision"]:
            bad.append(f"  {key}: SHA divergent\n     LLM_POOL      {ent['revision']}\n"
                       f"     download_pool {got}")
    print(f"[pool] {len(LLM_POOL)} intrari in LLM_POOL, {len(dl)} in download_pool.py")
    if bad:
        print("DIVERGENTA:"); print("\n".join(bad)); return 1
    print(f"[pool] OK, toate cele {len(LLM_POOL)} revision-uri coincid")
    return 0


def pick_instance(lang=None):
    """O instanta reala din trial. Implicit prima din prima limba, ca rularea sa fie determinista."""
    from mlsp_common import load_mlsp
    ml = load_mlsp("trial")
    if lang:
        ml = ml[ml["lang"] == lang]
        if ml.empty:
            raise SystemExit(f"nicio instanta de trial pentru limba {lang!r}")
    r = ml.iloc[0]
    return str(r["lang"]), str(r["sent"]), str(r["token"]), len(ml)


def prompt_for(rater, prompt_set, lang):
    """(sablonul de prompt, numele englez al limbii) pentru setul cerut.

    `legacy` = cele doua prompturi romanesti ale caii vechi, `multi` = cele in engleza cu limba tintei
    numita explicit. D.4 trebuie sa poata rula pe amandoua, altfel efectul schimbarii de prompt ar fi
    o presupunere, nu o cifra.
    """
    if prompt_set == "legacy":
        return rater.prompts[0], None
    if prompt_set == "multi":
        from mlsp_common import lang_name
        return rater.prompts_multi[0], lang_name(lang)
    raise ValueError(f"set de prompturi necunoscut: {prompt_set!r} (legacy sau multi)")


def spread_probe(rater, prompt_set):
    """Semnalul B pe cate o instanta de trial per limba. -> (valori, sd, n_finite).

    Zece perechi de forward-uri, secunde. Nu citeste nicio eticheta: se uita doar la ce IMPRASTIERE
    are B, fiindcă un B constant face Pearson r nedefinit pe toate cele 300 de instante.
    """
    from mlsp_common import load_mlsp
    sub = load_mlsp("trial").groupby("lang", sort=True).head(1)
    vals = [rater.rate(row.sent, row.token,
                       lang=None if prompt_set == "legacy" else row.lang) for row in sub.itertuples()]
    v = np.asarray(vals, float)
    fin = v[np.isfinite(v)]
    return v, (float(fin.std()) if fin.size else float("nan")), int(fin.size)


def run_sanity(rater, model_key, ent, lang, sent, token, no_guard=False, prompt_set="multi",
               t_load=float("nan")):
    """Criteriile 1-6 pe un rater DEJA INCARCAT. -> (ok, fails). Scrie blocul in output/d4_sanity.md.

    Separata de main() ca bakeoff_trial.py sa ruleze D.4 pe modelul lui inainte de orice cifra, fara sa
    coboare greutatile de doua ori.
    """
    r = rater
    if no_guard:
        r.thinking = False       # forteaza netrecerea kwarg-ului: exact capcana
        print("[d4] CONTROL: enable_thinking NU se trece. Se asteapta FAIL.", flush=True)

    fails, warns, lines = [], [], []

    # --- 1. id-uri de cifre nevide
    empty = [d for d in getattr(r, "digits", "12345") if not r.digit[d]]
    if empty:
        fails.append(f"1. self.digit gol pentru cifrele {empty}")

    # --- 2/3. garda de gandire
    prompt = r._render_chat([{"role": "user", "content": "test"}])
    closed = prompt.rfind("<think>") <= prompt.rfind("</think>")
    if not closed:
        fails.append("2. bloc de gandire DESCHIS la finalul promptului")
    applied = None
    if r.thinking:
        bare = r.tok.apply_chat_template([{"role": "user", "content": "test"}],
                                         add_generation_prompt=True, tokenize=False)
        applied = (bare != prompt)
        if not applied:
            fails.append("3. sablonul declara enable_thinking dar kwarg-ul nu are efect")

    # --- 4/5/6. masa si valoarea, pe propozitia reala
    tmpl, label = prompt_for(r, prompt_set, lang)
    t1 = time.time()
    p, raw = r.digit_mass(r._prompt_msgs(sent, token, tmpl, label))
    t_item = time.time() - t1

    conc = float(p.max()) if p is not None else float("nan")
    if raw < MASS_MIN:
        fails.append(f"4. masa bruta degenerata: {raw:.3e} < {MASS_MIN}")
    # Plafonul: masa e o suma de probabilitati dintr-un softmax, deci nu poate trece de 1. Daca trece,
    # un id se numara de mai multe ori in self.digit. Criteriul asta a prins [16, 16] la prima rulare.
    if raw > 1.0 + 1e-6:
        fails.append(f"4b. masa bruta peste 1: {raw:.6f}, deci id-uri duplicate in self.digit")
    if p is not None and conc > CONC_MAX:
        warns.append(f"masa concentrata pe o cifra la instanta asta: {conc:.6f} > {CONC_MAX}. "
                     "Avertisment, nu FAIL: decide criteriul 5, pe 10 limbi.")

    val = r._once(sent, token, tmpl, label)
    if val is None or not np.isfinite(val) or not (0.0 <= val <= 1.0):
        fails.append(f"6. _once() a intors {val!r}, nu un float in [0,1]")

    # --- 5. dispersia lui B peste cele 10 limbi. Un B constant face r nedefinit pe toate cele 300.
    t2 = time.time()
    bvals, bsd, bfin = spread_probe(r, prompt_set)
    t_spread = time.time() - t2
    if bfin < SPREAD_MIN_OK:
        fails.append(f"5a. B finit doar pe {bfin}/10 limbi, sub {SPREAD_MIN_OK}")
    elif not np.isfinite(bsd) or bsd < SPREAD_MIN:
        fails.append(f"5. B nu are dispersie peste cele 10 limbi: sd = {bsd:.6f} < {SPREAD_MIN}")

    # --- raport
    ok = not fails
    status = "PASS" if ok else "FAIL"
    head = f"CONTROL fara enable_thinking, {model_key}" if no_guard else model_key
    head += f" [prompt {prompt_set}]"
    dist = "  ".join(f"{d}={p[i]:.4f}" for i, d in enumerate("12345")) if p is not None else "n/a"

    lines.append(f"\n## {head}: **{status}**\n\n")
    lines.append(f"Rulat {time.strftime('%Y-%m-%d %H:%M:%S')}. "
                 f"Instanta trial: lang `{lang}`, tinta `{token}`.\n\n")
    lines.append("| camp | valoare |\n|---|---|\n")
    lines.append(f"| repo | `{ent['repo']}` |\n")
    lines.append(f"| revision | `{ent['revision']}` |\n")
    lines.append(f"| backend | {r.backend} |\n")
    lines.append(f"| device | {r.dev} |\n")
    lines.append(f"| set de prompturi | {prompt_set}" + (f", limba numita `{label}`" if label else
                                                         ", in romana, fara nume de limba") + " |\n")
    # Prefixul de citire e informativ, nu un criteriu: criteriile 4/5/6 trec prin `digit_mass`, care
    # citeste DEJA de dupa prefix, deci masa si valoarea din tabel sunt cele reale. Garda de gandire
    # rams pe sablonul curat, fiindca acolo se pune intrebarea daca `enable_thinking` a avut efect, si
    # un prefix adaugat ar face comparatia `bare != prompt` sa treaca de la sine.
    pref = getattr(r, "read_prefix", "")
    lines.append(f"| prefix de citire | {repr(pref) + f' -> {r.read_pref_ids}' if pref else 'niciunul (ultima pozitie a sablonului)'} |\n")
    lines.append(f"| enable_thinking declarat de sablon | {r.thinking if not no_guard else 'fortat off'} |\n")
    lines.append(f"| enable_thinking a avut efect | {applied} |\n")
    lines.append(f"| bloc de gandire inchis | {closed} |\n")
    nd = len(getattr(r, "digits", "12345"))
    lines.append(f"| **masa bruta peste cele {nd} cifre** | **{raw:.6e}** |\n")
    lines.append(f"| concentrare max(p) | {conc:.6f} |\n")
    lines.append(f"| **valoare intoarsa de _once()** | **{val}** |\n")
    bfmt = "  ".join(f"{x:.4f}" if np.isfinite(x) else "nan" for x in bvals)
    lines.append(f"| **dispersia lui B pe 10 limbi (sd)** | **{bsd:.4f}** pe {bfin}/10 finite |\n")
    lines.append(f"| timp incarcare | {t_load:.1f} s |\n")
    lines.append(f"| **timp per item** | **{t_item:.3f} s** |\n")
    lines.append(f"| timp sonda de dispersie, 10 limbi | {t_spread:.1f} s |\n")
    lines.append(f"\nB pe cate o instanta per limba, ordinea limbilor alfabetica: {bfmt}\n\n")
    lines.append(f"Distributia normalizata peste cifre: {dist}\n\n")
    lines.append("Id-urile de cifre gasite (capcana SentencePiece, ambele variante incercate):\n\n")
    lines.append("| cifra | id-uri | decodate |\n|---|---|---|\n")
    for d in getattr(r, "digits", "12345"):
        dec = ", ".join(repr(r.tok.decode([t])) for t in r.digit[d]) or "-"
        lines.append(f"| {d} | `{r.digit[d]}` | {dec} |\n")
    if warns:
        lines.append("\nAvertismente, nu criterii picate:\n\n" + "".join(f"- {w}\n" for w in warns))
    if fails:
        lines.append("\nCriterii picate:\n\n" + "".join(f"- {f}\n" for f in fails))
    note("".join(lines))

    print(f"\n[d4] masa bruta = {raw:.6e}   max(p) = {conc:.6f}   _once() = {val}")
    print(f"[d4] B pe 10 limbi: sd = {bsd:.4f} pe {bfin}/10 finite")
    print(f"[d4] timp per item = {t_item:.3f}s, sonda de dispersie {t_spread:.1f}s")
    for w in warns:
        print(f"  AVERTISMENT: {w}")
    for f in fails:
        print(f"  PICAT: {f}")
    print(f"[d4] {status} -> {LOG}")
    return ok, fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3-8b-4bit", help="cheie din mlsp_common.LLM_POOL")
    ap.add_argument("--lang", default=None, help="limba instantei de trial (implicit prima)")
    ap.add_argument("--prompt-set", default="multi", choices=("legacy", "multi"), dest="prompt_set",
                    help="legacy = prompturile romanesti ale caii vechi, multi = cele in engleza")
    ap.add_argument("--check-pool", action="store_true", dest="check_pool",
                    help="doar verifica SHA-urile fata de download_pool.py, fara greutati")
    ap.add_argument("--no-thinking-guard", action="store_true", dest="no_guard",
                    help="CONTROL: dezactiveaza enable_thinking=False. Se asteapta FAIL.")
    a = ap.parse_args()

    if a.check_pool:
        return check_pool()

    from mlsp_common import LLM_POOL
    from solution_bert import LLMRater

    ent = LLM_POOL.get(a.model)
    if ent is None:
        raise SystemExit(f"model necunoscut: {a.model!r}. Chei: {sorted(LLM_POOL)}")

    lang, sent, token, n_trial = pick_instance(a.lang)
    print(f"[d4] {a.model} ({ent['repo']} @ {ent['revision'][:12]})", flush=True)
    print(f"[d4] instanta trial: lang={lang} token={token!r} (din {n_trial})", flush=True)
    print(f"[d4] set de prompturi: {a.prompt_set}", flush=True)

    t0 = time.time()
    r = LLMRater(a.model)
    t_load = time.time() - t0
    print(f"[d4] incarcat in {t_load:.1f}s, backend={r.backend} dev={r.dev} "
          f"thinking_declarat={r.thinking}", flush=True)

    ok, fails = run_sanity(r, a.model, ent, lang, sent, token, no_guard=a.no_guard,
                           prompt_set=a.prompt_set, t_load=t_load)

    if a.no_guard:
        # La control, FAIL e rezultatul asteptat: dovedeste ca garda are putere.
        print("[d4] control: FAIL e rezultatul dorit" if fails else
              "[d4] control: a TRECUT, deci garda NU masoara ce credem. De refacut.")
        return 0 if fails else 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
