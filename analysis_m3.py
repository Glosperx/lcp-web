"""M3. Leave-one-encoder-out pe medie. Duce un singur encoder tot castigul, si e nevoie de large?

Media a patru encodere duce fuziunea la 0.671952, dar obiectia de cost spune ca cere patru encodere
la inferenta in loc de unul, iar `xlmr-large` e cel scump. M3 raspunde la doua lucruri deodata:

  fragilitate  daca scoaterea unui singur encoder prabuseste castigul, medierea atarna de el si e
               fragila, nu robusta, iar argumentul „mediaza fiindca sunt decorelati" slabeste
  cost         daca media celor trei ieftine pastreaza cea mai mare parte din castig, `xlmr-large`
               iese si obiectia de cost dispare aproape complet

Cele patru variante se ruleaza TOATE si se raporteaza TOATE. **Alegerea uneia pe scorul de test ar fi
acordare pe test si nu se face aici**; M3 produce cifrele, decizia e a lui Alexandru si intra, daca
intra, prin acelasi protocol ca restul.

Nu ruleaza nicio inferenta: fisierele de predictii per encoder exista deja pe disc, deci
`make_enc_mean.py` doar mediaza CSV-uri si fiecare fuziune ia zece secunde.

Rulare, dupa cele patru `make_enc_mean.py --encodere ...` si cele patru `fuse_ab.py`, ~20 de secunde:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_m3.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_m3.md")
TABLE = os.path.join(OUT, "m3.csv")
COST = os.path.join(OUT, "cost_inferenta.csv")
N_BOOT = 2000

ENCODERE = ("xlmr", "xlmr-large", "labse", "e5")
CFG = [("sistem", "sistemul publicat, un encoder", "fusion_preds_lolo_ens.csv"),
       ("toate4", "media celor patru", "fusion_preds_lolo_encmean.csv")]
# Tagul folosit a fost `encmean-fara-X`, fara prefixul `ens_`, deci calea nu are `_ens`.
CFG += [(f"fara-{e}", f"media celor trei, fara `{e}`", f"fusion_preds_lolo_encmean-fara-{e}.csv")
        for e in ENCODERE]


def distributii():
    """r si distributia bootstrap per configuratie per limba, pe randuri aliniate peste toate."""
    from mlsp_common import boot_r_ci
    preds = {}
    for k, _, f in CFG:
        p = os.path.join(OUT, f)
        if not os.path.exists(p):
            raise SystemExit(f"{p} lipseste. Ruleaza intai make_enc_mean.py --encodere ... plus "
                             f"fuse_ab.py --tag encmean-{k}")
        preds[k] = pd.read_csv(p)
    langs = sorted(preds["sistem"]["lang"].unique())
    R, B, meta = {k: {} for k in preds}, {k: {} for k in preds}, {}
    for lg in langs:
        g = {k: v[v["lang"] == lg].drop_duplicates("idx").set_index("idx") for k, v in preds.items()}
        ordine = g["sistem"].index
        for k in g:
            if set(g[k].index) != set(ordine):
                raise SystemExit(f"{lg}/{k}: alte randuri, diferenta n-ar fi pereche")
            g[k] = g[k].reindex(ordine)
        y, ctx = g["sistem"]["y"].values, g["sistem"]["ctx"].values
        for k in g:
            b = boot_r_ci(y, g[k]["p_fuz"].values, ctx, n_boot=N_BOOT)
            R[k][lg], B[k][lg] = b["r"], b["boot"]
            if k == "sistem":
                meta[lg] = {"n": len(ordine), "n_ctx": b["n_ctx"]}
    m = min(len(B[k][lg]) for k in B for lg in langs)
    B = {k: {lg: B[k][lg][:m] for lg in langs} for k in B}
    MED = {k: np.vstack([B[k][lg] for lg in langs]).mean(axis=0) for k in B}
    return langs, R, MED, meta


def pereche(a, b):
    dd = b - a
    return {"lo": float(np.percentile(dd, 2.5)), "hi": float(np.percentile(dd, 97.5)),
            "p": float((dd > 0).mean())}


def main():
    langs, R, MED, meta = distributii()
    rmed = {k: float(np.mean([R[k][l] for l in langs])) for k in R}
    cost = pd.read_csv(COST) if os.path.exists(COST) else None
    sec = {}
    if cost is not None:
        e = cost[cost["componenta"] == "encoder"].set_index("nume")["sec_forward"]
        sec = {"toate4": float(e.sum())}
        sec.update({f"fara-{x}": float(e.drop(x).sum()) for x in ENCODERE})
        sec["sistem"] = float(e.loc["xlmr"])

    rows = []
    for k, eticheta, _ in CFG:
        v = {"config": k, "eticheta": eticheta, "r": rmed[k],
             "d_sistem": rmed[k] - rmed["sistem"], "d_toate4": rmed[k] - rmed["toate4"],
             "sec_encodere": sec.get(k, float("nan"))}
        v.update({f"cs_{a}": b for a, b in pereche(MED["sistem"], MED[k]).items()})
        v.update({f"c4_{a}": b for a, b in pereche(MED["toate4"], MED[k]).items()})
        rows.append(v)
    t = pd.DataFrame(rows)
    t.to_csv(TABLE, index=False)

    trei = t[t["config"].str.startswith("fara-")]
    cel_mai_slab = trei.loc[trei["r"].idxmin()]
    fara_large = t[t["config"] == "fara-xlmr-large"].iloc[0]
    toate_bat_sistemul = bool((trei["cs_lo"] > 0).all())
    pastreaza = fara_large["d_sistem"] / (rmed["toate4"] - rmed["sistem"])

    L = ["# M3. Leave-one-encoder-out pe medie\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_m3.py`. Nicio inferenta: "
         "fisierele de predictii per encoder existau deja, deci `make_enc_mean.py` doar mediaza "
         "CSV-uri. Cele patru variante s-au rulat toate si se raporteaza toate; **alegerea uneia pe "
         "scorul de test ar fi acordare pe test si nu se face aici**. Date brute: "
         f"`output/{os.path.basename(TABLE)}`.\n\n",
         "## Rezultatul\n\n",
         "| configuratie | r fuziune | fata de sistem | CI 95% pereche | fata de media celor patru | "
         "CI 95% pereche |\n|---|---|---|---|---|---|\n"]
    for r in t.itertuples():
        ds = "referinta" if r.config == "sistem" else f"{r.d_sistem:+.6f}"
        cis = "" if r.config == "sistem" else f"[{r.cs_lo:+.4f}, {r.cs_hi:+.4f}]"
        d4 = "referinta" if r.config == "toate4" else f"{r.d_toate4:+.6f}"
        ci4 = "" if r.config == "toate4" else f"[{r.c4_lo:+.4f}, {r.c4_hi:+.4f}]"
        L.append(f"| {r.eticheta} | **{r.r:.6f}** | {ds} | {cis} | {d4} | {ci4} |\n")

    L.append("\n## Ce raspunde la fragilitate\n\n")
    if toate_bat_sistemul:
        L.append("**Niciun encoder nu duce singur castigul.** Toate cele patru medii de cate trei bat "
                 "sistemul cu interval pereche care exclude zero, de la "
                 f"{trei['d_sistem'].min():+.6f} la {trei['d_sistem'].max():+.6f}. Scoaterea oricarui "
                 "encoder lasa castigul in picioare, deci medierea nu atarna de niciunul si "
                 "argumentul „mediaza fiindca sunt decorelati\" se sustine: **e robusta, nu "
                 "norocoasa**. Cel mai mult se pierde scotand "
                 f"`{cel_mai_slab['config'].replace('fara-', '')}`, si chiar si atunci raman "
                 f"{cel_mai_slab['d_sistem']:+.6f} fata de sistem.\n\n")
    else:
        cade = trei[trei["cs_lo"] <= 0]
        L.append("**Medierea atarna de un encoder.** Scotand "
                 f"{', '.join('`' + x.replace('fara-', '') + '`' for x in cade['config'])} castigul "
                 "fata de sistem nu mai are interval care exclude zero, deci medierea nu e robusta si "
                 "argumentul de decorelare slabeste.\n\n")

    L.append("## Ce raspunde la cost, si aici e cifra care conteaza\n\n")
    if sec:
        L.append("| configuratie | encodere la inferenta | forward pe test | fata de un encoder | "
                 "castig pastrat |\n|---|---|---|---|---|\n")
        baza = sec["sistem"]
        castig4 = rmed["toate4"] - rmed["sistem"]
        for r in t.itertuples():
            n_enc = 1 if r.config == "sistem" else (4 if r.config == "toate4" else 3)
            pas = "referinta" if r.config == "sistem" else f"{100*r.d_sistem/castig4:.0f}%"
            L.append(f"| {r.eticheta} | {n_enc} | {r.sec_encodere:.0f}s = "
                     f"{r.sec_encodere/60:.1f} min | {r.sec_encodere/baza:.1f}x | {pas} |\n")
        L.append(f"\n**Scoaterea lui `xlmr-large` e schimbul care conteaza.** Media celor trei ieftine "
                 f"da {fara_large['r']:.6f}, adica {fara_large['d_sistem']:+.6f} fata de sistem cu "
                 f"interval [{fara_large['cs_lo']:+.4f}, {fara_large['cs_hi']:+.4f}], deci "
                 f"**pastreaza {100*pastreaza:.0f}% din castig**. Costul scade de la "
                 f"{sec['toate4']/60:.1f} la {sec['fara-xlmr-large']/60:.1f} minute, adica "
                 f"{100*(1 - sec['fara-xlmr-large']/sec['toate4']):.0f}% mai putin, fiindca "
                 f"`xlmr-large` singur e {sec['toate4'] - sec['fara-xlmr-large']:.0f}s din "
                 f"{sec['toate4']:.0f}s. Ce se pierde fata de media celor patru e "
                 f"{fara_large['d_toate4']:+.6f}, cu interval "
                 f"[{fara_large['c4_lo']:+.4f}, {fara_large['c4_hi']:+.4f}].\n\n")
        L.append("**Dar obiectia de cost era deja slaba.** Pe conducta intreaga, cu LLM-ul la 102 "
                 "minute, diferenta dintre patru encodere si trei e sub doua minute din o suta si "
                 "sapte. Cine scoate `xlmr-large` o face ca sa piarda un model de 24 de straturi din "
                 "dependinte, nu ca sa castige timp.\n\n")

    L.append("## Per limba, si `fil`\n\n"
             "| limba | sistem | toate 4 | fara large |\n|---|---|---|---|\n")
    for lg in langs:
        L.append(f"| {lg} | {R['sistem'][lg]:+.4f} | {R['toate4'][lg]:+.4f} | "
                 f"{R['fara-xlmr-large'][lg]:+.4f} |\n")
    L.append(f"| **medie** | {rmed['sistem']:.6f} | {rmed['toate4']:.6f} | "
             f"{rmed['fara-xlmr-large']:.6f} |\n")
    fil_4 = R["toate4"]["fil"] - R["sistem"]["fil"]
    fil_3 = R["fara-xlmr-large"]["fil"] - R["sistem"]["fil"]
    L.append(f"\n`fil` era limba care scadea, cu {fil_4:+.4f} sub media celor patru, si cauza era "
             "localizata: `xlmr-large` e cel mai prost din patru acolo, cu -0.0554 pe brațul A. "
             f"Scotandu-l, `fil` trece la {fil_3:+.4f} fata de sistem"
             + (f", deci scaderea se ATENUEAZA cu {fil_3 - fil_4:+.4f} dar **nu dispare**: `fil` "
                "ramane sub sistem si cu trei encodere, deci `xlmr-large` explica doar o parte din ea."
                if fil_3 > fil_4 > -1 and fil_3 < 0 else
                (", deci scaderea se repara complet." if fil_3 >= 0 else
                 ", deci scaderea nu se repara."))
             + " Asta e un argument pentru varianta cu trei care nu e de cost, ci de comportament.\n\n"
             "## Ce nu decide M3\n\n"
             "M3 nu alege nimic. Daca varianta cu trei encodere s-ar adopta pentru ca are cifra "
             "convenabila, ar fi exact acordarea pe test pe care restul protocolului o evita. "
             "Alegerea dintre `toate patru` si `fara large` trebuie sa treaca prin acelasi criteriu "
             "leave-one-language-out ca la M1, sau sa fie declarata ca decizie de inginerie luata pe "
             "cost, nu pe scor. Cele doua sunt formulari oneste; a alege pe scor si a nu spune nu e.\n")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("".join(L))
    for r in t.itertuples():
        print(f"[M3] {r.config:<16} {r.r:.6f}  vs sistem {r.d_sistem:+.6f} "
              f"[{r.cs_lo:+.4f}, {r.cs_hi:+.4f}]")
    print(f"-> {REPORT}")
    print(f"-> {TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
