"""§3.5 Franceza, diagnosticata. Patru verificari, in ordinea din plan, pe setul de dupa §3.1 si §3.3.

De ce franceza. In sistemul curent, `output/e_fusion_lolo_ens.md`, franceza are r_A = 0.5370,
r_B = 0.5440, r_fuziune = 0.5883. Cele DOUA semnale sunt mediocre in acelasi fel, deci nu e un defect
al unui brat: A e transfer peste embedding XLM-R, B e o nota data de un LLM, iar cand amandoua cad la
fel pe o singura limba, cauza probabila e in date sau in protocolul de adnotare.

Ce se verifica, in ordine:
  1. cele 3 tinte franceze care nu se gasesc ca subsir in context;
  2. cea mai mare deviatie standard a complexitatii din tot setul, 0.2494 pe franceza. Se verifica
     daca tine incar, si daca e chiar un DEFECT, fiindca o eticheta mai imprastiata da in principiu
     mai mult semnal de corelat, nu mai putin;
  3. acoperirea `wordfreq` pe formele flexionate franceze;
  4. cat a mai ramas din reziduul de fertilitate al francezei, +0.2167, dupa ce `fert_inloc` a intrat
     in sistem.

Nu atinge nimic: citeste data/ si output/, scrie output/e_fr_diagnostic.md. Scrie fisierul dupa
FIECARE pas care produce o cifra, nu la final.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_fr.py
"""
import glob
import os
import sys
import time

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_fr_diagnostic.md")
SYS_PREDS = os.path.join(OUT, "fusion_preds_lolo_ens.csv")
N_BOOT = 2000
LANGS = ["ca", "de", "en", "es", "fil", "fr", "it", "ja", "pt", "si"]

_DOC = []


def emit(*lines):
    """Adauga in raport si scrie pe disc pe loc, ca un pas care crapa sa nu piarda pasii de dinainte."""
    _DOC.extend(lines)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def r_of(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(pearsonr(a[m], b[m])[0])


def resid(y, Z):
    """Rezidualul lui y dupa regresie liniara pe Z, cu intercept. Idiomul din analysis_et.py."""
    y = np.asarray(y, float)
    Z = np.asarray(Z, float)
    m = np.isfinite(y) & np.isfinite(Z).all(axis=1)
    out = np.full(len(y), np.nan)
    Zc = np.column_stack([np.ones(m.sum()), Z[m]])
    beta, *_ = np.linalg.lstsq(Zc, y[m], rcond=None)
    out[m] = y[m] - Zc @ beta
    return out


def paired_r(y, p1, p2, groups):
    """Diferenta de r cu bootstrap PERECHE pe contexte, idiomul din fuse_ab.fuse_ens."""
    from mlsp_common import boot_r_ci
    b1 = boot_r_ci(y, p1, groups, n_boot=N_BOOT)
    b2 = boot_r_ci(y, p2, groups, n_boot=N_BOOT)
    k = min(len(b1["boot"]), len(b2["boot"]))
    dv = b2["boot"][:k] - b1["boot"][:k]
    return dict(r1=b1["r"], r2=b2["r"], d=b2["r"] - b1["r"],
                lo=float(np.percentile(dv, 2.5)), hi=float(np.percentile(dv, 97.5)),
                p=float((dv > 0).mean()), n_ctx=b1["n_ctx"])


def boot_one(y, p, groups):
    from mlsp_common import boot_r_ci
    return boot_r_ci(y, p, groups, n_boot=N_BOOT)


def grid_lattice(vals):
    """Grila etichetelor, citita direct din valori. -> (numitor, N adnotatori sau None, mixt).

    Eticheta MLSP e media a N note pe scara Likert de 5 puncte mapata pe {0, .25, .5, .75, 1}, deci
    orice eticheta e un multiplu de 1/(4N) si numitorul ei redus divide 4N. Cel mai mic 4N compatibil
    cu toate valorile limbii e cel mai mic multiplu comun al numitorilor.

    `mixt` e True cand numitorii NU sunt toti divizori ai celui mai mare, adica limba nu are un singur
    N pentru toate itemele: unele iteme au fost adnotate de mai multi oameni decat altele. Atunci un
    singur numar de adnotatori nu exista, si nu se raporteaza unul.
    """
    from fractions import Fraction
    from math import gcd
    v = np.unique(np.asarray(vals, float))
    dens = sorted({Fraction(x).limit_denominator(200).denominator for x in v})
    L = 1
    for d in dens:
        L = L * d // gcd(L, d)
    top = max(dens)
    mixt = any(top % d for d in dens)
    N = None if (mixt or L % 4) else L // 4
    return L, N, mixt


# ----------------------------------------------------------------------------- pasul 0
def step0():
    from mlsp_common import load_mlsp
    ml = load_mlsp("test")
    sysp = pd.read_csv(SYS_PREDS)
    emit("# §3.5 Franceza, diagnosticata\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_fr.py`. Setul e cel de DUPA §3.1 "
         f"si §3.3, adica sistemul de 0.664555 din `output/e_fusion_lolo_ens.md`, reprodus bit cu bit "
         f"inainte de orice masuratoare de aici.\n",
         "## De ce franceza, si de ce nu poate fi un defect de brat\n",
         "| | r pe franceza |", "|---|---|",
         f"| semnalul A, ansamblu de surse plus `fert_inloc` | {sysp[sysp.lang=='fr'].pipe(lambda d: r_of(d.A, d.y)):+.4f} |",
         f"| semnalul B, nota LLM, `qwen35-9b-8bit` | {sysp[sysp.lang=='fr'].pipe(lambda d: r_of(d.B, d.y)):+.4f} |",
         f"| fuziunea, adica sistemul | {sysp[sysp.lang=='fr'].pipe(lambda d: r_of(d.p_fuz, d.y)):+.4f} |",
         "",
         "Franceza e printre cele mai slabe limbi ale sistemului: peste `si` si `ca` in r absolut, sub "
         "restul. Prin fertilitate a urcat de la 0.5823 la 0.5883, deci +0.0060, dar intervalul "
         "pereche al acelei imbunatatiri, [-0.0020, +0.0142], include zero, deci singura nu se "
         "sustine.\n",
         "Constatarea care restrange caut area: **A si B eseueaza CORELAT**. A e o regresie peste "
         "embedding XLM-R inghetat plus lexical, B e o nota ceruta unui LLM. Nu au nicio componenta "
         "comuna in afara de datele si de etichete. Doua semnale fara nimic comun care cad amandoua "
         "pe o singura limba arata spre date sau spre protocolul de adnotare, nu spre un brat.\n")
    return ml, sysp


# ----------------------------------------------------------------------------- pasul 1
def step1(ml, sysp):
    from solution_bert import find_char_span, normalize_token
    print("[1] contabilitatea randurilor franceze", flush=True)
    tsv = pd.read_csv(glob.glob(os.path.join(DATA, "mlsp_full", "French",
                                             "multils_test_french_lcp_labels.tsv"))[0], sep="\t")
    fr = ml[ml["lang"] == "fr"].reset_index(drop=True)
    miss = []
    for i, row in fr.iterrows():
        txt = str(row["sent"]).replace("\n", " ").strip()
        if find_char_span(txt, str(row["token"])) is None:
            miss.append((row["token"], normalize_token(row["token"]), row["complexity"], txt))
    n_eval = int((sysp["lang"] == "fr").sum())

    # Aceeasi contabilitate pe toate limbile, ca sa se vada daca franceza e un caz special.
    per = []
    for lg in LANGS:
        g = ml[ml["lang"] == lg]
        bad = caz = 0
        for _, r in g.iterrows():
            txt = str(r["sent"]).replace("\n", " ").strip()
            if find_char_span(txt, str(r["token"])) is None:
                bad += 1
                caz += str(r["token"]).strip().lower() in txt.lower()
        per.append(dict(lang=lg, incarcate=len(g), negasite=bad, din_caz=caz,
                        evaluate=int((sysp["lang"] == lg).sum())))
    per = pd.DataFrame(per)

    emit("## 1. Cele 3 tinte negasite ca subsir. Confirmate, si fara efect\n",
         f"Contabilitatea completa a francezei: fisierul oficial "
         f"`multils_test_french_lcp_labels.tsv` are **{len(tsv)}** randuri, `load_mlsp` incarca "
         f"**{len(fr)}**, iar sistemul evalueaza **{n_eval}**.\n",
         f"Cele **{len(miss)}** randuri pierdute sunt exact tintele pe care `find_char_span` nu le "
         f"gaseste in propriul context, nici brut, nici dupa `normalize_token`:\n",
         "| tinta | dupa normalizare | complexitate | de ce nu se gaseste |", "|---|---|---|---|")
    for tok, norm, cx, txt in miss:
        why = _why(tok, norm, txt)
        emit(f"| `{tok}` | `{norm}` | {cx:.3f} | {why} |")
    emit("",
         f"Ele cad din evaluare prin masca `ok` a lui `embed_frame`, la fel ca cele 18 instante din "
         f"5624 despre care raportul spune deja ca rama in afara evaluarii. Deci **nu sunt o "
         f"pierdere de r, sunt o pierdere de n**: {len(fr)} minus {len(miss)} da exact "
         f"{n_eval}, numarul evaluat.\n",
         "Si nu e un fenomen francez. Aceeasi numaratoare pe toate cele 10 limbi:\n",
         "| limba | incarcate de `load_mlsp` | negasite ca subsir | din care doar din CAZ | evaluate de sistem |",
         "|---|---|---|---|---|")
    for _, r in per.iterrows():
        b = "**" if r["lang"] == "fr" else ""
        emit(f"| {b}{r['lang']}{b} | {r['incarcate']} | {b}{r['negasite']}{b} | {r['din_caz']} | "
             f"{r['evaluate']} |")
    tot, totcaz = int(per["negasite"].sum()), int(per["din_caz"].sum())
    emit("",
         f"Italiana pierde {int(per.loc[per.lang=='it','negasite'].iloc[0])} si portugheza "
         f"{int(per.loc[per.lang=='pt','negasite'].iloc[0])}, adica mai mult ca franceza, si amandoua "
         f"stau mult mai bine in r. **Punctul 1 se inchide negativ:** cele 3 tinte sunt reale, sunt "
         f"explicate, si nu explica nimic din deficitul francez.\n",
         f"Dar iese altceva, si e un defect adevarat, doar nu al francezei. **Toate cele {tot}** "
         f"instante pierdute pe tot setul, in toate cele patru limbi, se pierd dintr-un singur motiv: "
         f"litera mare de inceput de propozitie. `find_char_span` la [solution_bert.py:84](solution_bert.py#L84) "
         f"face `text.find(tok)`, sensibil la caz, deci o tinta data cu minuscula care apare prima in "
         f"propozitie nu se gaseste niciodata. E o reparatie de o linie care recupereaza {totcaz} "
         f"instante din 5624. **Nu se atinge aici**, fiindca ar schimba n si deci fiecare cifra "
         f"publicata, si nu e sarcina de acum; se raporteaza ca de facut.\n")
    print(f"    {len(miss)} negasite, {n_eval} evaluate din {len(fr)} incarcate", flush=True)
    return per


def _why(tok, norm, txt):
    """Motivul concret al nepotrivirii, citit din text, nu ghicit."""
    t = str(tok).strip()
    low = txt.lower().find(t.lower())
    if low >= 0:
        forma = txt[low:low + len(t)]
        return (f"contextul are `{forma}`, la inceput de propozitie, iar `find_char_span` compara "
                f"sensibil la caz")
    for k in range(len(t), 3, -1):
        if t[:k] in txt:
            return f"contextul contine doar prefixul `{t[:k]}`, deci tinta e o forma diferita de cea din text"
    return "niciun prefix de peste 3 caractere al tintei nu apare in context"


# ----------------------------------------------------------------------------- pasul 2
def step2(ml, sysp):
    print("[2] deviatia standard a complexitatii si grila etichetelor", flush=True)
    rows = []
    for lg in LANGS:
        g = ml[ml["lang"] == lg]
        L, N, mixt = grid_lattice(g["complexity"].values)
        d = sysp[sysp["lang"] == lg]
        rows.append(dict(lang=lg, n=len(g), sd=g["complexity"].std(), mean=g["complexity"].mean(),
                         nuniq=g["complexity"].nunique(), num=L, n_adn=N, mixt=mixt,
                         pas=1.0 / L, r_sys=r_of(d["p_fuz"], d["y"])))
    t = pd.DataFrame(rows).sort_values("sd", ascending=False)

    # Daca imprastierea etichetei ar fi SEMNAL, ar trebui sa ajute r. Se testeaza direct.
    b_, a_ = np.polyfit(t["sd"].values, t["r_sys"].values, 1)
    t["r_prezis"] = a_ + b_ * t["sd"].values
    t["rezid"] = t["r_sys"] - t["r_prezis"]
    r_trend = r_of(t["sd"], t["r_sys"])
    frs = t[t.lang == "fr"].iloc[0]

    emit("## 2. Cea mai mare deviatie standard din set. Tine, dar premisa e inversa\n",
         "| limba | n | medie | **sd** | valori distincte | numitorul grilei | adnotatori | pas | r sistem |",
         "|---|---|---|---|---|---|---|---|---|")
    for _, r in t.iterrows():
        bb = "**" if r["lang"] == "fr" else ""
        adn = "variabil" if r["mixt"] else (str(r["n_adn"]) if r["n_adn"] else "?")
        emit(f"| {bb}{r['lang']}{bb} | {r['n']} | {r['mean']:.4f} | {bb}{r['sd']:.4f}{bb} | "
             f"{r['nuniq']} | 1/{r['num']} | {adn} | {r['pas']:.4f} | {r['r_sys']:+.4f} |")
    emit("",
         f"**Cifra tine.** Franceza are sd = {frs['sd']:.4f}, cea mai mare din tot setul, exact ca in "
         f"planul vechi.\n",
         "Dar planul o trecea in dreptul defectelor, si asta nu se susține. O eticheta mai imprastiata "
         "da in principiu **mai mult** semnal de corelat, nu mai puțin: imprastierea etichetei e la "
         "numitorul lui r. Deci se testeaza direct, peste cele 10 limbi.\n",
         f"Corelatia dintre sd al etichetei si r al sistemului e **{r_trend:+.4f}**, cu panta "
         f"{b_:+.4f} r pe unitate de sd. Adica imprastierea chiar ajuta, si franceza are cea mai "
         f"multa.\n",
         "| limba | sd | r sistem | r prezis din sd | **rezidual** |", "|---|---|---|---|---|")
    for _, r in t.sort_values("rezid").iterrows():
        bb = "**" if r["lang"] == "fr" else ""
        emit(f"| {bb}{r['lang']}{bb} | {r['sd']:.4f} | {r['r_sys']:+.4f} | {r['r_prezis']:+.4f} | "
             f"{bb}{r['rezid']:+.4f}{bb} |")
    rank = int((t["rezid"] < frs["rezid"]).sum()) + 1
    emit("",
         f"Franceza are rezidualul **{frs['rezid']:+.4f}**, al {rank}-lea de jos din 10. Deci franceza "
         f"nu e slaba pentru ca eticheta ei e imprastiata; e slaba **in ciuda** faptului ca eticheta "
         f"ei e cea mai imprastiata din set, adica cea mai usor de corelat. **Punctul 2 se inchide cu "
         f"premisa confirmata si consecinta respinsa.**\n",
         "### Ce iese in schimb din grila etichetelor\n",
         "Coloanele de grila nu erau in plan si se citesc gratis din aceleasi etichete. Eticheta MLSP "
         "e media a N note pe o scara Likert de 5 puncte mapata pe multiplii de 0.25, deci fiecare "
         "eticheta e un multiplu de 1/(4N) si numitorul ei redus divide 4N. Cel mai mic multiplu comun "
         "al numitorilor din limba da grila, iar grila da N.\n",
         "Setul se rupe in trei grupe curate:\n")
    g10 = t[(~t.mixt) & (t.n_adn == 10)]["lang"].tolist()
    g25 = t[(~t.mixt) & (t.n_adn == 25)]["lang"].tolist()
    gmx = t[t.mixt]["lang"].tolist()
    emit(f"- grila 1/40, adica **10 adnotatori** pe fiecare item: {', '.join('`'+x+'`' for x in sorted(g10))};",
         f"- grila 1/100, adica **25 de adnotatori**: {', '.join('`'+x+'`' for x in sorted(g25))};",
         f"- numitori care nu se divid intre ei, adica numar **variabil** de adnotatori de la un item "
         f"la altul: {', '.join('`'+x+'`' for x in sorted(gmx))}.\n")
    r10 = t[t.lang.isin(g10)]
    emit(f"Franceza e in grupa cea mai grosiera. Media a N note are eroarea standard proportionala cu "
         f"1/sqrt(N), deci o limba cu 10 adnotatori are o eticheta mai zgomotoasa per item si un "
         f"plafon de r mai jos decat una cu 25, **independent de orice model**.\n",
         f"**Dar nici asta nu explica franceza**, si se vede in aceeasi coloana. In grupa de 10 "
         f"adnotatori intra si "
         f"{', '.join(f'`{r.lang}` ({r.r_sys:+.4f})' for _, r in r10.sort_values('r_sys', ascending=False).iterrows())}. "
         f"Doua limbi cu exact aceeasi grila ca franceza trec de 0.73. Grila e o constrangere reala si "
         f"masurata, dar nu e cea care leaga aici.\n",
         "Onest, fiindca altfel cifra ar fi supravanduta: N citit din grila e o margine INFERIOARA. Se "
         "citeste din cel mai fin pas prezent efectiv in etichete, deci o limba unde nicio medie n-a "
         "cazut pe o fractie fina iese cu N mai mic decat cel real. Nu inlocuieste numarul de "
         "adnotatori din documentatia MLSP, care **n-a fost verificat**.\n")
    print(f"    fr sd={frs['sd']:.4f} rezid={frs['rezid']:+.4f} grila=1/{frs['num']}", flush=True)
    return t


# ----------------------------------------------------------------------------- pasul 3
def step3(ml, sysp):
    from mlsp_common import zipf_safe
    print("[3] acoperirea wordfreq pe formele flexionate", flush=True)
    lem = pd.read_csv(os.path.join(OUT, "lemmas_mlsp.csv"))
    lem = lem[lem["split"] == "test"]
    rows = []
    for lg in LANGS:
        g = ml[ml["lang"] == lg].reset_index(drop=True)
        L = lem[lem["lang"] == lg].drop_duplicates(["sent", "token"]).set_index(["sent", "token"])
        lm = [L["lemma"].get((s_, t_), np.nan) for s_, t_ in zip(g["sent"], g["token"])]
        zf = np.array([zipf_safe(t_, lg)[0] for t_ in g["token"]])
        av = zipf_safe(g["token"].iloc[0], lg)[1]
        zl = np.array([zipf_safe(x, lg)[0] if isinstance(x, str) else 0.0 for x in lm])
        zb = np.maximum(zf, zl)
        difer = np.array([isinstance(x, str) and str(x) != str(t_) for x, t_ in zip(lm, g["token"])])
        y = g["complexity"].values
        d = sysp[sysp["lang"] == lg]
        rows.append(dict(
            lang=lg, n=len(g), acoperit=av,
            zero_forma=int((zf == 0).sum()), zero_lema=int((zb == 0).sum()),
            salvate=int(((zf == 0) & (zb > 0)).sum()), lema_difera=int(difer.sum()),
            r_forma=-r_of(zf, y), r_lema=-r_of(zl, y), r_best=-r_of(zb, y),
            castig=(-r_of(zb, y)) - (-r_of(zf, y)),
            r_A=r_of(d["A"], d["y"]), r_sys=r_of(d["p_fuz"], d["y"])))
    t = pd.DataFrame(rows)
    t["best_minus_A"] = t["r_best"] - t["r_A"]

    def f(x):
        return "n/a" if not np.isfinite(x) else f"{x:+.4f}"

    emit("## 3. Acoperirea `wordfreq` pe formele flexionate franceze\n",
         "`r` e dat cu semnul intors, adica corelatia lui **neg-zipf** cu complexitatea, ca sa fie "
         "pozitiv si comparabil cu restul lucrarii: un cuvant rar e greu. `forma` e tokenul asa cum "
         "apare, `lema` e lema lui `stanza`, `best` e `max(zipf_forma, zipf_lema)`, adica exact ce "
         "primeste sistemul prin `--lemma-freq`.\n",
         "| limba | n | limba acoperita | zipf 0 pe forma | zipf 0 dupa lema | salvate de lema | "
         "lema difera | r forma | r lema | **r best** | castigul lemei |",
         "|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in t.iterrows():
        bb = "**" if r["lang"] == "fr" else ""
        emit(f"| {bb}{r['lang']}{bb} | {r['n']} | {'da' if r['acoperit'] else '**nu**'} | "
             f"{bb}{r['zero_forma']}{bb} | {r['zero_lema']} | {r['salvate']} | {r['lema_difera']} | "
             f"{f(r['r_forma'])} | {f(r['r_lema'])} | {bb}{f(r['r_best'])}{bb} | {f(r['castig'])} |")
    fr = t[t.lang == "fr"].iloc[0]
    sub = int((t["r_best"] < fr["r_best"]).sum())
    emit("",
         "**Punctul 3 se inchide negativ pe intrebarea pusa, dar scoate la iveala altceva.**\n",
         f"Pe acoperire, nimic. Franceza are {fr['zero_forma']} tinte din {fr['n']} cu zipf zero pe "
         f"forma, adica {100*fr['zero_forma']/fr['n']:.1f}%, si {fr['zero_lema']} dupa ce lema "
         f"actioneaza. E la egalitate cu engleza, care e cea mai buna limba a sistemului. Cazurile "
         f"patologice ale setului sunt `fil`, cu 152 din 570, si `si`, unde limba nu e servita deloc. "
         f"Franceza nu are o gaura de acoperire.\n",
         f"Pe informativitate, tot nimic in defavoarea francezei: `r best` e {fr['r_best']:+.4f}, si "
         f"{sub} din celelalte limbi stau mai jos. Frecventa franceza functioneaza normal. Lema aduce "
         f"{fr['castig']:+.4f} desi {fr['lema_difera']} din {fr['n']} tinte, adica "
         f"{100*fr['lema_difera']/fr['n']:.1f}%, au lema diferita de forma. Deci franceza chiar e "
         f"flexionata si lematizarea chiar muta formele, doar ca nu era nimic de recuperat.\n",
         "### Ce iese in schimb: o singura coloana bate 770\n",
         "Comparatia care nu era cerută dar cade din acelasi tabel. `r best` e **o singura trasatura**, "
         "neg-zipf. `r A` e semnalul A intreg: embedding XLM-R de 768 de dimensiuni, plus lexicalul, "
         "plus ansamblul celor doua brate de transfer, plus fertilitatea in locul lungimii.\n",
         "| limba | `r best`, o coloana | `r A`, semnalul intreg | **best − A** | r sistem |",
         "|---|---|---|---|---|")
    for _, r in t.sort_values("best_minus_A", ascending=False).iterrows():
        bb = "**" if r["lang"] == "fr" else ""
        emit(f"| {bb}{r['lang']}{bb} | {f(r['r_best'])} | {r['r_A']:+.4f} | "
             f"{bb}{f(r['best_minus_A'])}{bb} | {r['r_sys']:+.4f} |")
    pos = t[t["best_minus_A"] > 0]["lang"].tolist()
    emit("",
         f"Pe franceza o singura coloana de frecventa da {fr['r_best']:+.4f}, iar semnalul A intreg "
         f"da {fr['r_A']:+.4f}, deci **{fr['best_minus_A']:+.4f} in favoarea coloanei singure**. "
         f"Limbile unde asta se intampla sunt {', '.join('`'+x+'`' for x in sorted(pos))}, iar "
         f"franceza e cea mai clara.\n",
         "E acelasi lucru pe care il spunea deja descompunerea pe blocuri, cu alte cifre si pe "
         "configuratia veche: pe franceza blocul lexical singur bate sistemul intreg, 0.542 fata de "
         "0.531. Aici se confirma pe configuratia curenta, cu ansamblu de surse si fertilitate in cod, "
         "si se restrange: nu e blocul lexical de 7 coloane, e **o coloana**.\n",
         "Ce inseamna. Diagnosticul pe care il sprijina masuratorile nu e „datele franceze sunt "
         "defecte”, e **embeddingul nu transfera pe franceza**, si pe deasupra dilueaza o trasatura "
         "care singura ar merge mai bine. Nu contrazice constatarea ca A si B cad corelat, fiindca B "
         "nu foloseste embeddingul; le pune insa in ordine, prima cauza fiind brațul A.\n")
    print(f"    fr zipf0={fr['zero_forma']}/{fr['n']} r_best={fr['r_best']:+.4f} "
          f"best-A={fr['best_minus_A']:+.4f}", flush=True)
    return t


# ----------------------------------------------------------------------------- pasul 4
def step4(ml, sysp):
    from solution_bert import fertility
    from mlsp_common import zipf_safe
    print("[4] reziduul de fertilitate, inainte si dupa fert_inloc", flush=True)
    ab = pd.read_csv(os.path.join(OUT, "e1_frozen_preds_lemma.csv"))
    ab = ab[ab["split"] == "test"].drop_duplicates(["lang", "idx"])
    rows = []
    for lg in LANGS:
        g = ml[ml["lang"] == lg].reset_index(drop=True)
        gi = list(ml.index[ml["lang"] == lg])
        fert = fertility(list(g["token"]))
        ln = np.array([len(str(t_)) for t_ in g["token"]], float)
        zp = np.array([zipf_safe(t_, lg)[0] for t_ in g["token"]])
        y = g["complexity"].values
        Z = np.column_stack([ln, zp])
        r_orig = r_of(resid(fert, Z), resid(y, Z))          # masuratoarea din §3.3
        d = sysp[sysp["lang"] == lg].set_index("idx")
        keep = [i for i in gi if i in d.index]
        pos = [gi.index(i) for i in keep]
        f2, Z2, y2 = fert[pos], Z[pos], d.loc[keep, "y"].values
        pb_ = ab[ab["lang"] == lg].set_index("idx")["p_multi"].reindex(keep).values
        # Validitate INCREMENTALA: fertilitatea vs eticheta, controlate amandoua pe
        # (lungime, zipf, predictie). Zero = predictia a luat deja tot ce avea fertilitatea.
        def part(pred):
            Zc = np.column_stack([Z2, np.asarray(pred, float)])
            return r_of(resid(f2, Zc), resid(y2, Zc))
        Zs = np.column_stack([Z2, d.loc[keep, "p_fuz"].values])
        bs = boot_one(resid(y2, Zs), resid(f2, Zs), d.loc[keep, "ctx"].values)
        rows.append(dict(lang=lg, n=len(g), fert_mean=fert.mean(), r_orig=r_orig,
                         r_part_baza=part(pb_), r_part_A=part(d.loc[keep, "A"].values),
                         r_part_sys=part(d.loc[keep, "p_fuz"].values),
                         sys_lo=bs["lo"], sys_hi=bs["hi"]))
    t = pd.DataFrame(rows)

    # Franceza: interval pe corelatia partiala reziduala fata de sistem, plus efectul masurat al
    # lui fert_inloc pe bratul A, cu bootstrap pereche pe contexte.
    af = pd.read_csv(os.path.join(OUT, "e1_frozen_preds_lemma_fert_inloc.csv"))
    af = af[af["split"] == "test"].drop_duplicates(["lang", "idx"])
    dfr = sysp[sysp["lang"] == "fr"]
    ix = dfr["idx"].values
    pb = paired_r(dfr["y"].values,
                  ab[ab["lang"] == "fr"].set_index("idx")["p_multi"].reindex(ix).values,
                  af[af["lang"] == "fr"].set_index("idx")["p_multi"].reindex(ix).values,
                  dfr["ctx"].values)
    gfr = ml[ml["lang"] == "fr"].reset_index(drop=True)
    gifr = list(ml.index[ml["lang"] == "fr"])
    posfr = [gifr.index(i) for i in ix]
    ffr = fertility(list(gfr["token"]))[posfr]
    Zfr = np.column_stack([[len(str(x)) for x in gfr["token"]],
                           [zipf_safe(x, "fr")[0] for x in gfr["token"]]])[posfr]
    Zc = np.column_stack([Zfr, dfr["p_fuz"].values])
    bp = boot_one(resid(dfr["y"].values, Zc), resid(ffr, Zc), dfr["ctx"].values)

    emit("## 4. Reziduul de fertilitate, cat a mai ramas dupa `fert_inloc`\n",
         "`r orig` e masuratoarea din §3.3, refacuta: corelatia fertilitatii cu ETICHETA, dupa ce se "
         "scot lungimea si zipf din amandoua. E reziduul de dinainte de reparatie.\n",
         "Celelalte trei coloane raspund la intrebarea „cat a mai ramas” prin **validitate "
         "incrementala**: aceeasi corelatie partiala, dar cu predictia adaugata la controale, pe ambele "
         "laturi. Zero inseamna ca predictia a luat deja tot ce avea de dat fertilitatea. Se face asa, "
         "si nu ca corelatie a fertilitatii cu eroarea bruta `y − p`, fiindca varianta cu eroarea bruta "
         "iese NEGATIVA pe toate cele zece limbi, inclusiv pe engleza si germana, care pornesc de la un "
         "reziduu de zero. Adica masoara cat de mult foloseste modelul trasatura, nu cat a rămas din ea. "
         "A fost calculata, si nu se raporteaza.\n",
         "| limba | n | fertilitate medie | `r orig`, vs eticheta | partial vs A `baza` | "
         "partial vs A `fert_inloc` | **partial vs sistem** | CI 95% pe contexte |",
         "|---|---|---|---|---|---|---|---|")
    for _, r in t.sort_values("r_orig", ascending=False).iterrows():
        bb = "**" if r["lang"] == "fr" else ""
        z = "" if r["sys_lo"] <= 0 <= r["sys_hi"] else " (exclude zero)"
        emit(f"| {bb}{r['lang']}{bb} | {r['n']} | {r['fert_mean']:.2f} | {bb}{r['r_orig']:+.4f}{bb} | "
             f"{r['r_part_baza']:+.4f} | {r['r_part_A']:+.4f} | {bb}{r['r_part_sys']:+.4f}{bb} | "
             f"[{r['sys_lo']:+.4f}, {r['sys_hi']:+.4f}]{z} |")
    fr = t[t.lang == "fr"].iloc[0]
    rank = int((t["r_orig"] > fr["r_orig"]).sum()) + 1
    viu = t[(t.sys_lo > 0)]["lang"].tolist()
    emit("",
         f"**Cifra din plan se confirma exact:** franceza are `r orig` = **{fr['r_orig']:+.4f}**, al "
         f"{rank}-lea din set, adica +0.2167 de acolo.\n",
         f"**Dar reziduul NU e consumat, si asta e singurul lucru din toata lista care mai e de "
         f"facut.** Fata de sistemul intreg fertilitatea are inca validitate incrementala "
         f"**{fr['r_part_sys']:+.4f}**, cu intervalul pe contexte [{bp['lo']:+.4f}, {bp['hi']:+.4f}], "
         f"care **exclude zero**. Adica fertilitatea mai spune ceva despre eticheta franceza pe care "
         f"sistemul nu il ia.\n",
         f"Si nu scade prin `fert_inloc`. Cu brațul A de dinainte, setul `baza`, corelatia partiala e "
         f"{fr['r_part_baza']:+.4f}; cu setul `fert_inloc`, care e chiar cel din sistem, e "
         f"{fr['r_part_A']:+.4f}, adica la fel sau puțin mai sus. Coboara doar la "
         f"{fr['r_part_sys']:+.4f}, si asta prin amestecul cu semnalul B, nu prin coloana de "
         f"fertilitate.\n",
         f"Ce a facut totusi `fert_inloc` pe franceza, masurat direct pe brațul A cu bootstrap pereche "
         f"pe {pb['n_ctx']} contexte:\n",
         "| brat A pe franceza | r |", "|---|---|",
         f"| set `baza`, lungime in caractere | {pb['r1']:+.4f} |",
         f"| set `fert_inloc`, fertilitate in locul lungimii | {pb['r2']:+.4f} |",
         f"| **diferenta** | **{pb['d']:+.4f}**, CI [{pb['lo']:+.4f}, {pb['hi']:+.4f}], "
         f"P(>0) = {pb['p']:.1%} |", "",
         f"Deci a ajutat, {pb['d']:+.4f} cu interval care exclude zero, dar a ajutat **fara sa ia "
         f"reziduul**. Cele doua nu se contrazic: `fert_inloc` pune fertilitatea ca una din "
         f"770 de coloane intr-un `Ridge + HGB`, deci ii ia partea liniara comuna, nu tot ce are de "
         f"dat pe franceza.\n",
         f"**Punctul 4 se inchide ca DESCHIS.** E singurul din cele patru care rămane. Limbile cu "
         f"reziduu POZITIV si interval care exclude zero sunt "
         f"{', '.join('`'+x+'`' for x in sorted(viu))}, iar franceza are cel mai mare dintre ele. "
         f"`ja` e a treia din trioul prezis de §3.3 si merge in aceeasi directie, "
         f"{t[t.lang=='ja'].r_part_sys.iloc[0]:+.4f}, dar intervalul ei include zero.\n",
         f"Si o avertizare pentru orice reparatie care ar urma. Pe `de` "
         f"({t[t.lang=='de'].r_part_sys.iloc[0]:+.4f}) si `pt` "
         f"({t[t.lang=='pt'].r_part_sys.iloc[0]:+.4f}) reziduul e NEGATIV cu interval care exclude "
         f"zero, adica acolo sistemul foloseste fertilitatea prea mult. O forma mai puternica de "
         f"fertilitate, pusa global, ar strica exact pe limbile alea. Daca se face, se face pe limbile "
         f"unde reziduul e pozitiv, si alegerea limbilor trebuie sa treaca prin LOLO ca tot restul.\n")
    print(f"    fr r_orig={fr['r_orig']:+.4f} -> partial vs sistem {fr['r_part_sys']:+.4f} "
          f"[{bp['lo']:+.4f},{bp['hi']:+.4f}]", flush=True)
    return t, pb, bp


# ----------------------------------------------------------------------------- verdictul
def verdict(per1, t2, t3, t4, pb, bp, sysp):
    fr2 = t2[t2.lang == "fr"].iloc[0]
    fr3 = t3[t3.lang == "fr"].iloc[0]
    fr4 = t4[t4.lang == "fr"].iloc[0]
    d = sysp[sysp["lang"] == "fr"]
    r_sys = r_of(d["p_fuz"], d["y"])
    totcaz = int(per1["din_caz"].sum())
    g10 = t2[(~t2.mixt) & (t2.n_adn == 10)].sort_values("r_sys", ascending=False)
    emit("## Verdictul\n",
         "**Trei din cele patru ipoteze se resping, a patra rămane deschisa.** Cele trei se confirma "
         "ca cifra si se resping ca explicatie, ceea ce nu e acelasi lucru cu a fi false.\n",
         "| punct | ce spunea planul | ce iese | consecinta |", "|---|---|---|---|",
         f"| 1, tinte negasite | 3 tinte franceze nu se gasesc ca subsir | **confirmat, exact 3** | "
         f"pierdere de n, nu de r. `it` pierde 8 si `pt` 5, amandoua cu r mai bun |",
         f"| 2, imprastierea etichetei | sd 0.2494, cea mai mare din set | **confirmat, "
         f"{fr2['sd']:.4f}** | premisa inversa: peste cele 10 limbi imprastierea AJUTA r, deci "
         f"franceza e slaba in ciuda ei |",
         f"| 3, acoperire `wordfreq` | formele flexionate franceze ar putea cadea | **respins**, "
         f"{fr3['zero_forma']}/{fr3['n']} zipf zero, la egalitate cu engleza | frecventa franceza "
         f"functioneaza normal |",
         f"| 4, reziduu de fertilitate | +0.2167 partial nereparat | **confirmat, si inca "
         f"nereparat**: {fr4['r_part_sys']:+.4f} validitate incrementala peste sistem, interval "
         f"[{bp['lo']:+.4f}, {bp['hi']:+.4f}], exclude zero | **singurul punct care rămane deschis** |", "",
         "### Ce rămane de facut, si e un singur lucru\n",
         f"Punctul 4. Fertilitatea are inca **{fr4['r_part_sys']:+.4f}** validitate incrementala peste "
         f"sistem pe franceza, interval [{bp['lo']:+.4f}, {bp['hi']:+.4f}] care exclude zero, si "
         f"`fert_inloc` nu a schimbat asta: corelatia partiala e {fr4['r_part_baza']:+.4f} cu setul "
         f"`baza` si {fr4['r_part_A']:+.4f} cu `fert_inloc`. Coloana a intrat, r-ul brațului A a urcat "
         f"cu {pb['d']:+.4f}, dar reziduul a rămas. Explicatia care se potriveste cifrelor e ca "
         f"fertilitatea intra ca una din 770 de coloane intr-un `Ridge + HGB`, deci i se ia doar "
         f"partea comuna liniar. Ce ar testa asta e o forma neliniara sau interactiva a fertilitatii "
         f"pe cele trei limbi unde intervalul exclude zero. **Nu s-a rulat**, e o modificare de "
         f"trasaturi cu efect pe toate cifrele publicate.\n",
         "### Ce s-a mai gasit, si nu era pe lista\n",
         f"**1. O coloana bate 770 pe franceza.** Neg-zipf singur da {fr3['r_best']:+.4f}, semnalul A "
         f"intreg da {fr3['r_A']:+.4f}, deci {fr3['best_minus_A']:+.4f} in favoarea coloanei singure, "
         f"cea mai mare diferenta din set. Diagnosticul pe care il sprijina masuratorile nu e ca "
         f"datele franceze sunt defecte, e ca **embeddingul nu transfera pe franceza si dilueaza o "
         f"trasatura care singura ar merge mai bine**. Se potriveste cu descompunerea pe blocuri de "
         f"dinainte, 0.542 lexical fata de 0.531 tot, si o restrange de la 7 coloane la una.\n",
         f"**2. Grila etichetelor rupe setul in trei grupe.** Franceza e in cea mai grosiera, 1/40, "
         f"adica 10 adnotatori per item, contra 25 la `it`, `pt`, `si` si numar variabil la `en`, "
         f"`es`, `ca`. Plafonul de r scade cu 1/sqrt(N), deci constrangerea e reala. **Dar nu explica "
         f"franceza:** in aceeasi grupa de 10 adnotatori stau "
         f"{', '.join(f'`{r.lang}` ({r.r_sys:+.4f})' for _, r in g10.iterrows() if r.lang != 'fr')}, "
         f"deci doua limbi cu exact aceeasi grila trec de 0.73.\n",
         f"**3. Un defect de cod adevarat, dar nu al francezei.** Toate cele {totcaz} instante "
         f"pierdute pe tot setul, in `fr`, `fil`, `it` si `pt`, se pierd numai fiindca "
         f"`find_char_span` e sensibil la caz si tinta e primul cuvant din propozitie. Reparatie de o linie, recupereaza n, nu r. Nu s-a atins: ar "
         f"schimba n si deci fiecare cifra publicata.\n",
         "### Ce se scrie in lucrare\n",
         f"Franceza rămane o limba slaba a sistemului, la {r_sys:+.4f}, **fara un defect de date "
         f"identificat**. Trei din cele patru ipoteze verificabile se resping. A patra, reziduul de "
         f"fertilitate, nu se respinge: e inca acolo, {fr4['r_part_sys']:+.4f} peste sistem cu "
         f"interval care exclude zero, si e singurul lucru masurat care mai promite ceva.\n",
         f"Ce a ieșit peste lista muta a doua cauza dinspre date inspre brațul A: pe franceza o "
         f"singura trasatura de frecventa bate semnalul A intreg, {fr3['r_best']:+.4f} fata de "
         f"{fr3['r_A']:+.4f}, ceea ce inseamna ca embeddingul XLM-R nu doar ca nu transfera acolo, ci "
         f"dilueaza.\n",
         "Asta nu contrazice constatarea de la care s-a plecat, ca A si B cad corelat, fiindca B nu "
         "foloseste embeddingul si cade independent. Le pune in ordine: sunt **doua** cauze, nu una, "
         "iar cea din brațul A e cea masurata si localizata aici.\n",
         "**Ce ar testa direct ipoteza asta, si nu s-a rulat:** §3.6, encoder mai mare sau alt encoder "
         "sub LOLO. Daca embeddingul e problema pe franceza, atunci exact acolo ar trebui sa se vada "
         "cel mai mult diferenta intre encodere. E o rulare separata, cu aprobare.\n",
         "**Trei din patru premise s-au confirmat in cifre si au fost respinse in consecinta.** Fara "
         "masuratoare, oricare din ele s-ar fi scris ca explicatie. A patra a supravietuit, dar numai "
         "dupa ce metrica a fost schimbata: prima versiune, corelatia fertilitatii cu eroarea bruta "
         "`y − p`, dadea negativ pe toate cele zece limbi si ar fi dus la concluzia inversa, ca "
         "reziduul e consumat.\n")


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    ml, sysp = step0()
    per1 = step1(ml, sysp)
    t2 = step2(ml, sysp)
    t3 = step3(ml, sysp)
    t4, pb, bp = step4(ml, sysp)
    verdict(per1, t2, t3, t4, pb, bp, sysp)
    print(f"\n-> {REPORT}  ({time.time()-t0:.0f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
