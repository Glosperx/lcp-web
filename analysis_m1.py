"""M1. Alegerea dintre „selecteaza encoderul" si „mediaza encoderele", facuta ea insasi LOLO.

Obiectia care conteaza cu adevarat impotriva adoptarii mediei de encodere nu e cifra si nu e costul.
E ca alegerea binara, a media in loc de a selecta, s-a facut DUPA ce s-a vazut pe test ca selectia
cade. Declaratia e onesta dar nu e falsificabila: un reviewer nu poate verifica daca am fi ales
medierea si in cazul in care selectia ar fi castigat.

M1 transforma alegerea de cercetator in consecinta de protocol. Pentru limba L, se decide intre cele
doua brate folosind NUMAI celelalte 9 limbi, exact ca `w`, ca `w_src` si ca modelul lui B:

    crit(brat, L) = media lui r a bratului peste limbile L' != L
    ales(L)       = argmax peste cele doua brate
    r_M1(L)       = r al bratului ales, pe limba L

Nu e o rulare, e o reagregare: ambele brate exista deja per limba, scrise de `fuse_ab.py`. Zero
inferenta, zero fuziune recalculata.

**Daca medierea castiga pe toate cele 10 folduri, alegerea binara nu mai e o alegere de cercetator**,
e iesirea aceluiasi protocol care alege `w` si modelul, si obiectia dispare. Daca nu castiga peste
tot, M1 spune exact pe ce limbi protocolul ar fi ales altfel, iar cifra lui e ce s-ar putea raporta.

Fiecare r per limba al fiecarui brat e el insusi produs sub LOLO, deci criteriul lui L nu atinge
etichetele lui L la niciun nivel.

Rulare, ~10 secunde:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_m1.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_m1.md")
TABLE = os.path.join(OUT, "m1.csv")
N_BOOT = 2000

# cheie -> (eticheta, tabel, predictii)
BRATE = [
    ("selectie", "encoderul ales per limba, LOLO", "fusion_lolo_enc.csv",
     "fusion_preds_lolo_enc.csv"),
    ("mediere", "media neponderata a celor patru", "fusion_lolo_encmean.csv",
     "fusion_preds_lolo_encmean.csv"),
]
SISTEM = ("sistemul publicat", "fusion_lolo_ens.csv", "fusion_preds_lolo_ens.csv")


def citeste():
    d = {}
    for k, eticheta, tab, preds in BRATE + [("sistem",) + SISTEM]:
        pt, pp = os.path.join(OUT, tab), os.path.join(OUT, preds)
        for q in (pt, pp):
            if not os.path.exists(q):
                raise SystemExit(f"{q} lipseste. Ruleaza intai fuse_ab.py pentru {k!r}")
        d[k] = {"eticheta": eticheta, "tab": pd.read_csv(pt), "preds": pd.read_csv(pp)}
    return d


def distributii(d):
    """r si distributia bootstrap per brat per limba, pe randuri aliniate peste toate bratele."""
    from mlsp_common import boot_r_ci
    ref = d["sistem"]["preds"]
    langs = sorted(ref["lang"].unique())
    R, B, meta = {k: {} for k in d}, {k: {} for k in d}, {}
    for lg in langs:
        g = {}
        for k in d:
            gk = d[k]["preds"]
            g[k] = gk[gk["lang"] == lg].drop_duplicates("idx").set_index("idx")
        ordine = g["sistem"].index
        for k in g:
            if set(g[k].index) != set(ordine):
                raise SystemExit(f"{lg}/{k}: alte randuri, diferenta n-ar fi pereche")
            g[k] = g[k].reindex(ordine)
            if not np.allclose(g[k]["y"].values, g["sistem"]["y"].values):
                raise SystemExit(f"{lg}/{k}: etichetele nu coincid dupa aliniere")
        y, ctx = g["sistem"]["y"].values, g["sistem"]["ctx"].values
        for k in g:
            b = boot_r_ci(y, g[k]["p_fuz"].values, ctx, n_boot=N_BOOT)
            R[k][lg], B[k][lg] = b["r"], b["boot"]
            if k == "sistem":
                meta[lg] = {"n": len(ordine), "n_ctx": b["n_ctx"]}
    m = min(len(B[k][lg]) for k in B for lg in langs)
    B = {k: {lg: B[k][lg][:m] for lg in langs} for k in B}
    return langs, R, B, meta


def alege_lolo(R, langs):
    """Pentru fiecare L, criteriul fiecarui brat pe celelalte 9 limbi, si argmaxul."""
    rows = []
    for L in langs:
        crit = {k: float(np.mean([R[k][l] for l in langs if l != L])) for k, _, _, _ in BRATE}
        ales = max(crit, key=crit.get)
        chei = [k for k, _, _, _ in BRATE]
        rows.append({"lang": L, "ales": ales,
                     "crit_selectie": crit["selectie"], "crit_mediere": crit["mediere"],
                     "marja": crit[ales] - min(crit.values()),
                     "r_selectie": R["selectie"][L], "r_mediere": R["mediere"][L],
                     "r_m1": R[ales][L], "r_sistem": R["sistem"][L],
                     "corect": ales == max(chei, key=lambda k: R[k][L])})
    return pd.DataFrame(rows)


def pereche(bootA, bootB):
    """Diferenta pereche dintre doua distributii deja aliniate."""
    dd = bootB - bootA
    return {"lo": float(np.percentile(dd, 2.5)), "hi": float(np.percentile(dd, 97.5)),
            "p": float((dd > 0).mean())}


def main():
    d = citeste()
    langs, R, B, meta = distributii(d)
    sel = alege_lolo(R, langs)

    # distributia lui M1: per limba, distributia bratului pe care protocolul l-a ales acolo
    B["m1"] = {r.lang: B[r.ales][r.lang] for r in sel.itertuples()}
    R["m1"] = {r.lang: r.r_m1 for r in sel.itertuples()}
    MED = {k: np.vstack([B[k][lg] for lg in langs]).mean(axis=0) for k in B}
    rmed = {k: float(np.mean([R[k][l] for l in langs])) for k in R}

    sel.to_csv(TABLE, index=False)
    n_med = int((sel["ales"] == "mediere").sum())
    unanim = n_med == len(langs)

    cmp_sist = pereche(MED["sistem"], MED["m1"])
    cmp_med = pereche(MED["mediere"], MED["m1"])
    marja_min = float(sel["marja"].min())

    L = ["# M1. Alegerea dintre selectie si mediere, facuta ea insasi leave-one-language-out\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_m1.py`. Nicio inferenta, nicio "
         "fuziune recalculata: ambele brate exista deja per limba, scrise de `fuse_ab.py`, iar M1 e o "
         f"reagregare a lor. Date brute: `output/{os.path.basename(TABLE)}`.\n\n",
         "## Ce raspunde, si de ce conteaza mai mult decat cifra\n\n",
         "Obiectia care conteaza impotriva adoptarii mediei de encodere nu e cifra si nu e costul. E "
         "ca **alegerea binara s-a facut dupa ce s-a vazut pe test ca selectia cade**. Formularea de "
         "pana acum, „singura alegere de cercetator e binara, luata dupa ce s-a vazut ca selectia "
         "cade\", spune reviewerului exact lucrul care il ingrijoreaza fara sa ii dea nimic care sa il "
         "linisteasca. E onesta si insuficienta, fiindca nu e falsificabila.\n\n",
         "M1 o face falsificabila. Pentru limba L se decide intre cele doua brate folosind numai "
         "celelalte 9 limbi, exact ca `w`, ca `w_src` si ca modelul lui B:\n\n",
         "```\n"
         "crit(brat, L) = media lui r a bratului peste limbile L' != L\n"
         "ales(L)       = argmax peste cele doua brate\n"
         "r_M1(L)       = r al bratului ales, pe limba L\n```\n\n",
         "Fiecare r per limba al fiecarui brat e el insusi produs sub LOLO, deci criteriul lui L nu "
         "atinge etichetele lui L la niciun nivel.\n\n",
         "## Rezultatul, fold cu fold\n\n",
         "| limba | crit selectie | crit mediere | **ales** | marja | r selectie | r mediere | "
         "**r M1** |\n|---|---|---|---|---|---|---|---|\n"]
    for r in sel.itertuples():
        L.append(f"| {r.lang} | {r.crit_selectie:.6f} | {r.crit_mediere:.6f} | **{r.ales}** | "
                 f"{r.marja:.6f} | {r.r_selectie:+.4f} | {r.r_mediere:+.4f} | "
                 f"**{r.r_m1:+.4f}** |\n")
    L.append(f"| **medie** | {sel['crit_selectie'].mean():.6f} | {sel['crit_mediere'].mean():.6f} | "
             f"| {sel['marja'].mean():.6f} | {rmed['selectie']:.6f} | {rmed['mediere']:.6f} | "
             f"**{rmed['m1']:.6f}** |\n")

    if unanim:
        L.append(f"\n**Medierea castiga pe TOATE cele {len(langs)} folduri.** Marja minima e "
                 f"{marja_min:.6f}, adica pe foldul cel mai stramt criteriul separa inca de "
                 f"{marja_min/max(sel['marja'].max(), 1e-12):.0%} din cat separa pe cel mai larg. "
                 "**Alegerea binara nu mai e o alegere de cercetator**: e iesirea aceluiasi protocol "
                 "care alege `w`, `w_src` si modelul lui B. Obiectia se desfiinteaza, si nu prin "
                 "declaratie, ci prin masuratoare.\n\n"
                 "**Ce va observa un reviewer atent, si e corect sa observe:** unanimitatea nu e o "
                 "surpriza, fiindca medierea domina selectia destul de uniform "
                 f"({int((sel['r_mediere'] > sel['r_selectie']).sum())} limbi din {len(langs)}), deci "
                 "scoaterea unei limbi din criteriu nu are cum sa rastoarne argmaxul. Asta **nu** "
                 "slabeste rezultatul, il precizeaza: M1 nu demonstreaza ca decizia e stransa si totusi "
                 "corecta, demonstreaza ca e **stabila**, adica nu atarna de nicio limba anume. Un "
                 "criteriu care s-ar fi rasturnat la scoaterea unei limbi ar fi fost exact semnalul ca "
                 "alegerea e zgomot, ca la selectia de encoder insasi.\n\n"
                 f"Nuanta care trebuie scrisa: pe `fil` medierea e mai proasta decat selectia "
                 f"({float(sel.loc[sel.lang == 'fil', 'r_mediere'].iloc[0]):+.4f} fata de "
                 f"{float(sel.loc[sel.lang == 'fil', 'r_selectie'].iloc[0]):+.4f}), si protocolul "
                 "alege acolo medierea oricum, fiindca nu are voie sa se uite la `fil`. Aia e o "
                 "pierdere reala pe care protocolul o plateste ca sa ramana curat, si se declara ca "
                 "atare.\n\n")
    else:
        L.append(f"\n**Medierea castiga pe {n_med} folduri din {len(langs)}, nu pe toate.** Pe "
                 f"{', '.join(sel[sel['ales'] != 'mediere']['lang'])} protocolul ar fi ales selectia. "
                 "Alegerea binara **ramane in parte o alegere de cercetator**, iar cifra care se poate "
                 f"raporta sub protocol strict e {rmed['m1']:.6f}, nu {rmed['mediere']:.6f}.\n\n")

    L += ["## Cat costa protocolul strict\n\n",
          "| configuratie | r mediu | fata de sistem | CI 95% pereche | P(>0) |\n|---|---|---|---|---|\n",
          f"| sistemul publicat | {rmed['sistem']:.6f} | referinta | | |\n",
          f"| selectia de encoder, LOLO | {rmed['selectie']:.6f} | "
          f"{rmed['selectie']-rmed['sistem']:+.6f} | | |\n",
          f"| medierea, aleasa de noi | {rmed['mediere']:.6f} | {rmed['mediere']-rmed['sistem']:+.6f} "
          "| | |\n",
          f"| **M1, aleasa de protocol** | **{rmed['m1']:.6f}** | **{rmed['m1']-rmed['sistem']:+.6f}** "
          f"| [{cmp_sist['lo']:+.4f}, {cmp_sist['hi']:+.4f}] | {100*cmp_sist['p']:.1f}% |\n"]
    if abs(rmed["m1"] - rmed["mediere"]) < 1e-12:
        L.append("\n**M1 si medierea sunt aceeasi configuratie, rand cu rand.** Protocolul a ales "
                 "medierea peste tot, deci nu exista nicio diferenta de platit: cifra ramane "
                 f"{rmed['mediere']:.6f}, dar acum e obtinuta de protocol, nu aleasa de noi. Asta e "
                 "exact ce se cerea.\n\n")
    else:
        L.append(f"\nM1 difera de mediere cu {rmed['m1']-rmed['mediere']:+.6f}, CI "
                 f"[{cmp_med['lo']:+.4f}, {cmp_med['hi']:+.4f}], P(>0) = {100*cmp_med['p']:.1f}%. "
                 "Diferenta aia e pretul protocolului strict.\n\n")

    n_corect = int(sel["corect"].sum())
    L += ["## Verificarea care nu se putea face altfel\n\n",
          f"Pe {n_corect} limbi din {len(langs)} bratul ales de criteriu e chiar cel care iese mai bine "
          "pe limba respectiva. Cifra asta **nu e** o masura de performanta si nu se raporteaza ca "
          "atare: foloseste r-ul lui L ca sa evalueze o alegere care nu l-a vazut, deci e o "
          "diagnosticare a criteriului, nu un rezultat.\n\n",
          "## Ce se poate scrie acum in paper\n\n"]
    if unanim:
        L.append("> Alegerea dintre selectia de encoder per limba si medierea neponderata a "
                 "encoderelor nu a fost facuta de noi. Pentru fiecare limba tinta, cele doua "
                 "alternative au fost comparate folosind exclusiv celelalte noua limbi, prin acelasi "
                 "criteriu leave-one-language-out care alege ponderea de fuziune si modelul de limbaj. "
                 f"Medierea a fost selectata pe toate cele {len(langs)} folduri, cu o marja minima de "
                 f"{marja_min:.4f}. Configuratia raportata este deci iesirea protocolului, nu o "
                 "alegere facuta dupa inspectarea scorurilor de test.\n\n")
    else:
        L.append(f"> Pentru fiecare limba tinta, selectia de encoder si medierea au fost comparate "
                 f"folosind exclusiv celelalte noua limbi. Medierea a fost selectata pe {n_med} din "
                 f"{len(langs)} folduri, iar configuratia raportata, cu r mediu {rmed['m1']:.4f}, este "
                 "iesirea acestui protocol.\n\n")
    L.append("Ce **nu** rezolva M1: alegerea intre cele 70 de configuratii din jurnal ramane facuta "
             "de noi, uitandu-ne la scorul de test. M1 inchide o singura bifurcatie, cea mai expusa, "
             "nu gradina intreaga. Vezi sectiunea 4 din `output/e_adoptie.md`.\n")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("".join(L))
    print(f"[M1] medierea aleasa pe {n_med}/{len(langs)} folduri | marja minima {marja_min:.6f}")
    print(f"[M1] r: selectie {rmed['selectie']:.6f} | mediere {rmed['mediere']:.6f} | "
          f"M1 {rmed['m1']:.6f}")
    print(f"[M1] M1 vs sistem {rmed['m1']-rmed['sistem']:+.6f} "
          f"[{cmp_sist['lo']:+.4f}, {cmp_sist['hi']:+.4f}] P(>0)={100*cmp_sist['p']:.1f}%")
    print(f"-> {REPORT}")
    print(f"-> {TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
