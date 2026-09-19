"""Pozitia de citire: cifra citita dupa un prefix FORTAT, nu de la ultima pozitie a sablonului de chat.

Ultima parghie chiar netestata din `output/e_prioritate.md`. Pana acum `digit_mass` citeste logits-urile
la ultima poziție a sablonului de chat, adica exact acolo unde modelul mai are de ales si FORMA
raspunsului, nu doar nota: poate deschide o propozitie, poate pune un semn, poate pune cifra. Masa
care pleaca pe deschideri de propozitie nu e masa peste note, si totusi ea intra in numitorul
normalizarii. Ipoteza e ca dupa un inceput de raspuns fortat, „Rating:", alegerea de format e deja
facuta si ce rams e chiar nota.

Ipoteza asta are o marime observabila care o testeaza direct, si nu e `r`: **masa bruta** peste cele
cinci cifre, adica `raw1` si `raw2`. Daca prefixul curata citirea, masa bruta trebuie sa urce. Daca
urca masa dar `r` nu se mișcă, atunci masa care se pierdea era pierduta uniform si normalizarea o
scotea oricum, iar parghia e nula prin construcție, nu prin ghinion. Se raporteaza amandoua.

Cernere pe cele 300 de instante de trial, ~6 minute per brat. Bratul de referinta e fisierul CANONIC
de trial, nu o rulare noua: prefixul gol trece prin `_read_ids` fara sa adune nimic, si controlul de
30 de randuri o verifica la octet.

Temperatura se realege pentru FIECARE brat, pe grila extinsa, in doua forme raportate amandoua:
argmaxul pe MEDIA celor zece limbi, care e un oracol dar acelasi oracol pentru toate bratele, deci nu
favorizeaza niciunul; si alegerea LOLO, care e protocolul lucrarii. Un prefix schimba ascutimea
distributiei, deci o comparatie la T = 1 ar masura ascutimea, nu pozitia de citire.

Cifra de trial nu e o predictie a cifrei de test. Numai ordinea supravietuieste, si numai castigatorul
urca pe test.

Rulare:
  python bakeoff_trial.py --model gemma4-12b-4bit --prefix "Rating:" \\
      --out output/dist/pref_rating_trial.csv
  python analysis_citire.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_citire.md")

# Bratele. Primul e referinta si trebuie sa fie bratul fara prefix. `doc` intra in tabel.
# Prefixele se termina cu SPATIU, si nu e cosmetic: fara el cifra e cu o poziție mai departe si masa
# pe cele cinci cifre iese 5.5e-08. Vezi comentariul din `solution_bert.LLMRater.__init__`.
BRATE = [("niciunul", "ultima poziție a sablonului de chat, adica semnalul B publicat",
          os.path.join(OUT, "dist", "gemma4-12b-4bit_trial.csv")),
         ("Rating: ", "numeste chiar marimea cerută, si e cuvantul din instructiune",
          os.path.join(OUT, "dist", "pref_rating_trial.csv")),
         ("Answer: ", "neutru fata de marime: forteaza formatul, nu sensul",
          os.path.join(OUT, "dist", "pref_answer_trial.csv")),
         ("Difficulty: ", "numeste constructul, nu nota; mai lung, deci si un control de lungime",
          os.path.join(OUT, "dist", "pref_difficulty_trial.csv"))]

_DOC = []


def emit(*lines):
    """Adauga in raport si scrie pe disc pe loc, ca un pas care crapa sa nu piarda pasii de dinainte.
    Acelasi idiom ca `analysis_prioritate.emit`."""
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def b_at(D, T):
    """Semnalul B la temperatura T, media celor doua prompturi. Aceeasi aritmetica cu
    `analysis_dist.b_at`, rescrisa aici doar ca sa nu depinda de forma cadrului de test."""
    import analysis_dist as ad
    return 0.5 * (ad.expected(ad.temper(D["P1"], T)) + ad.expected(ad.temper(D["P2"], T)))


def load_arms():
    """[(nume, doc, {limba: dict})], plus limbile. Crapa daca bratele nu sunt pe aceleasi randuri."""
    from bakeoff_trial import with_context
    arms, ref = [], None
    for nume, doc, q in BRATE:
        if not os.path.exists(q):
            continue
        d = with_context(pd.read_csv(q), "trial")
        key = (d["lang"].astype(str).values, d["token"].astype(str).values,
               d["complexity"].values)
        if ref is None:
            ref = key
        else:
            bad = ((key[0] != ref[0]) | (key[1] != ref[1]) | (np.abs(key[2] - ref[2]) > 1e-6))
            if bad.any():
                raise SystemExit(f"{q} nu e pe aceleasi randuri ca bratul de referinta, prima "
                                 f"diferenta la {int(np.flatnonzero(bad)[0])}")
        per = {}
        for lg, g in d.groupby("lang", sort=True):
            per[lg] = dict(P1=g[[f"p1_{c}" for c in "12345"]].values.astype(float),
                           P2=g[[f"p2_{c}" for c in "12345"]].values.astype(float),
                           raw=np.concatenate([g["raw1"].values.astype(float),
                                               g["raw2"].values.astype(float)]),
                           y=g["complexity"].values.astype(float),
                           ctx=g["context_id"].values, B=g["B"].values.astype(float), n=len(g))
        arms.append((nume, doc, per))
    return arms, sorted(arms[0][2]) if arms else []


def main():
    import analysis_dist as ad
    arms, langs = load_arms()
    lipsa = [n for n, _, q in BRATE if not os.path.exists(q)]
    if not arms or arms[0][0] != "niciunul":
        raise SystemExit(f"bratul de referinta lipseste: {BRATE[0][2]}")
    n_tot = sum(arms[0][2][lg]["n"] for lg in langs)

    emit("# E.11. Pozitia de citire, cernere pe trial\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_citire.py`. "
         f"{n_tot} instante de trial per brat, {len(langs)} limbi, ambele prompturi. "
         "Datele brute: `output/dist/pref_*_trial.csv`.\n",
         __doc__.split("Rulare:")[0].split("\n", 2)[2].strip() + "\n")
    if lipsa:
        emit(f"**Brate nerulate**, deci absente din tabele: {lipsa}.\n")

    # --- temperatura, in cele doua forme
    ST = {}
    emit("## 1. Bratele, fiecare la temperatura lui\n",
         "`T* pe medie` e argmaxul mediei pe cele zece limbi, deci un ORACOL: e in tabel fiindca e "
         "acelasi oracol pentru toate bratele si nu favorizeaza niciunul. `T LOLO` e protocolul "
         "lucrarii, temperatura limbii L aleasa pe celelalte noua. `masa bruta` e marimea care testeaza "
         "direct ipoteza prefixului, si e mediata peste ambele prompturi si toate instantele.\n",
         "| prefix | ce schimba | masa bruta | r la T=1 | T* pe medie | r la T* | T LOLO, r | "
         "atomi efectivi la T=1 |",
         "|---|---|---|---|---|---|---|---|")
    for nume, doc, per in arms:
        R = {T: float(np.mean([ad.r_of(b_at(per[lg], T), per[lg]["y"]) for lg in langs]))
             for T in ad.T_GRID_EXT}
        Tb = max(R, key=R.get)
        # LOLO: pentru limba L, T e argmaxul mediei lui r peste celelalte noua limbi. Aceeasi forma
        # cu `analysis_dist.temp_pick` si cu `fuse_ab.pick_model`.
        Rl = {lg: np.array([ad.r_of(b_at(per[lg], T), per[lg]["y"]) for T in ad.T_GRID_EXT])
              for lg in langs}
        Tlolo, rlolo = {}, []
        for lg in langs:
            crit = np.mean([Rl[l2] for l2 in langs if l2 != lg], axis=0)
            j = int(np.argmax(crit))
            Tlolo[lg] = ad.T_GRID_EXT[j]
            rlolo.append(Rl[lg][j])
        P = {lg: 0.5 * (per[lg]["P1"] + per[lg]["P2"]) for lg in langs}
        ae = float(np.mean([np.exp(ad.entropy(P[lg])).mean() for lg in langs]))
        raw = float(np.mean([np.nanmean(per[lg]["raw"]) for lg in langs]))
        ST[nume] = dict(R=R, T=Tb, Tlolo=Tlolo, per=per, rl=float(np.mean(rlolo)),
                        raw=raw, ae=ae)
        emit(f"| `{nume}` | {doc} | {raw:.4f} | {R[1.0]:+.4f} | {Tb:g} | **{R[Tb]:+.4f}** | "
             f"{float(np.mean(rlolo)):+.4f} | {ae:.2f} din 5 |")
        print(f"    {nume:12s} masa {raw:.4f}  r(T=1) {R[1.0]:+.4f}  T*={Tb:g} r {R[Tb]:+.4f}  "
              f"LOLO r {float(np.mean(rlolo)):+.4f}", flush=True)
    emit("")

    # --- comparatia pereche, fiecare brat la temperatura lui, fata de bratul fara prefix
    emit("## 2. Comparatia pereche fata de citirea de acum\n",
         "Fiecare brat la temperatura lui, aleasa LOLO, adica protocolul lucrarii. Reesantionarea e pe "
         "CONTEXTE si are seed fix, deci perechea vede aceeasi reesantionare in ambele brate si "
         "zgomotul comun se anuleaza. Intervalele sunt late si trebuie sa fie: 30 de instante per "
         "limba, nu 560.\n",
         "**Coloana `limbi stricate` se citeste INAINTEA mediei.** Asa a fost respins `distTpp` la "
         "0.685763 si asa a fost respins `prio_KW` la 0.685727, desi amandoua aveau media mai mare.\n",
         "| prefix | diferenta pe medie | CI 95% pereche | P(>0) | limbi stricate cu CI care exclude "
         "zero | limbi urcate cu CI care exclude zero |",
         "|---|---|---|---|---|---|")

    def boots(nume):
        S = ST[nume]
        return [ad.boot_one(S["per"][lg]["y"], b_at(S["per"][lg], S["Tlolo"][lg]),
                            S["per"][lg]["ctx"])["boot"] for lg in langs]

    B = {n: boots(n) for n in ST}
    base = arms[0][0]
    per_lang = {}
    for nume, _, _ in arms[1:]:
        dm, lo, hi, pp = ad.mean_diff_ci(B[nume], B[base])
        rup, rdn, rows = [], [], []
        for i, lg in enumerate(langs):
            k = min(len(B[nume][i]), len(B[base][i]))
            dv = B[nume][i][:k] - B[base][i][:k]
            l2, h2 = float(np.percentile(dv, 2.5)), float(np.percentile(dv, 97.5))
            d2 = float(np.mean(dv))
            rows.append((lg, d2, l2, h2))
            if h2 < 0:
                rdn.append(lg)
            elif l2 > 0:
                rup.append(lg)
        per_lang[nume] = rows
        emit(f"| `{nume}` | **{dm:+.4f}** | [{lo:+.4f}, {hi:+.4f}] | {pp:.1%} | "
             f"{', '.join(rdn) if rdn else 'niciuna'} | {', '.join(rup) if rup else 'niciuna'} |")
        print(f"    {nume:12s} {dm:+.4f} [{lo:+.4f},{hi:+.4f}] P={pp:.1%}  stricate={rdn or '-'}",
              flush=True)
    emit("")

    emit("### Per limba, fiecare brat fata de citirea de acum\n",
         "| prefix | " + " | ".join(langs) + " |", "|---" * (len(langs) + 1) + "|")
    for nume, rows in per_lang.items():
        emit(f"| `{nume}` | " + " | ".join(f"{d:+.3f}" for _, d, _, _ in rows) + " |")
    emit("")

    # --- unde anume strica prefixul: capul sau coada distributiei
    emit("## 3. Capul distributiei fata de coada\n",
         "Bloc adaugat dupa ce cifrele de sus au ieșit toate negative, ca sa se vada UNDE. `masa pe "
         "argmax`, `atomi efectivi` si `r la T=1` descriu capul distributiei, adica partea vizibila. "
         "`r al coadei` e semnalul la T -> infinit in forma inchisa, `analysis_dist.s_limit`, adica "
         "`suma_i (i-3) log p_i`: exact marimea din care temperatura scoate cand urca de la T=1 la T=8. "
         "Daca in coada nu e semnal, un T mare nu are ce sa extraga, oricat de curat ar fi capul.\n",
         "| prefix | masa pe argmax | atomi efectivi | r la T=1 | r la T=8 | r al COADEI | "
         "r al cifrei generate |",
         "|---|---|---|---|---|---|---|")
    for nume, _, per in arms:
        ma = float(np.mean([(0.5 * (per[lg]["P1"] + per[lg]["P2"])).max(axis=1).mean()
                            for lg in langs]))
        ae = float(np.mean([np.exp(ad.entropy(0.5 * (per[lg]["P1"] + per[lg]["P2"]))).mean()
                            for lg in langs]))
        r1 = float(np.mean([ad.r_of(b_at(per[lg], 1.0), per[lg]["y"]) for lg in langs]))
        r8 = float(np.mean([ad.r_of(b_at(per[lg], 8.0), per[lg]["y"]) for lg in langs]))
        rs = float(np.mean([ad.r_of(0.5 * (ad.s_limit(per[lg]["P1"]) + ad.s_limit(per[lg]["P2"])),
                                    per[lg]["y"]) for lg in langs]))
        rh = float(np.mean([ad.r_of(0.5 * ((per[lg]["P1"].argmax(1) + 1.0)
                                           + (per[lg]["P2"].argmax(1) + 1.0)),
                                    per[lg]["y"]) for lg in langs]))
        emit(f"| `{nume}` | {ma:.3f} | {ae:.2f} din 5 | {r1:+.4f} | {r8:+.4f} | **{rs:+.4f}** | "
             f"{rh:+.4f} |")
    emit("")

    # --- verdict, fara nicio cifra scrisa de mana
    best = max(per_lang, key=lambda n: ad.mean_diff_ci(B[n], B[base])[0]) if per_lang else None
    if best is None:
        emit("## Verdict\n", "Niciun brat cu prefix nu e rulat, deci nu exista verdict.\n")
    else:
        dm, lo, hi, pp = ad.mean_diff_ci(B[best], B[base])
        stricate = [lg for lg, _, _, h in per_lang[best] if h < 0]
        emit("## Verdict\n",
             f"Cel mai bun brat e `{best}`: {dm:+.4f} fata de citirea de acum, interval pereche "
             f"[{lo:+.4f}, {hi:+.4f}], deci {ad.zero_out(lo, hi)}, P(>0) = {pp:.1%}. Limbi stricate cu "
             f"interval care exclude zero: {', '.join(stricate) if stricate else 'niciuna'}.\n",
             f"Masa bruta trece de la {ST[base]['raw']:.4f} la {ST[best]['raw']:.4f}, adica "
             f"{ST[best]['raw'] - ST[base]['raw']:+.4f}. "
             + ("Prefixul deci NU curata citirea in sensul ipotezei: masa care pleca pe format nu se "
                "recupereaza, si atunci nici nu era de recuperat."
                if ST[best]["raw"] <= ST[base]["raw"] else
                "Prefixul curata deci citirea in sensul ipotezei: masa peste cifre urca.") + "\n",
             ("**Se propune confirmarea pe test**, ~102 minute, fiindca intervalul de trial exclude "
              "zero si nicio limba nu e stricata."
              if lo > 0 and not stricate else
              "**Nu se propune confirmarea pe test**: pe trial nu se vede nimic care sa merite "
              "cele ~102 minute, si cifra de trial nu e oricum o predictie a celei de test, doar "
              "ordinea supravietuieste.") + "\n")
    print(f"[E11] -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
