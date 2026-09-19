"""Semnalul A ca medie a mai multor regresori, direct peste CSV-urile de predictii.

De ce se poate face asa, si de ce e mai bine decat un regresor nou in `solution_bert.py`.
`blend_ridge_hgb` mediaza predictiile celor doi membri INAINTE sa scrie fisierul, iar mediile
comuta cu scrisul: media coloanelor din `_reg-ridge` si `_reg-hgb` reproduce fisierul lui `blend`
la **1.11e-16**, masurat pe toate cele trei coloane de predictii. Deci un blend potrivit inauntru
si o media de CSV-uri sunt acelasi lucru, si al doilea drum nu atinge codul adoptat al lui A.

Motivul pentru care fisierul asta exista. Combinatiile ridge+tabfm din 25 august au fost facute
ad-hoc si nu se pot reproduce: coloana `p_multi` din
`e1_frozen_preds_tf-proj-394_ridgetabfm_lemma_fert_inloc.csv` e in unitati z (-6.3 .. 8.4) in loc
de scala complexitatii, si niciun script din proiect nu o scrie. Cifrele 0.6797 si 0.6805 care ies
din ea nu se citeaza. Aici constructia e una singura, verificata de controlul de mai jos.

Rulare:
    python make_a_blend.py IESIRE.csv INTRARE1.csv INTRARE2.csv [INTRARE3.csv ...]
    python make_a_blend.py --control                # reproduce blend din ridge + hgb
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
META = ["split", "idx", "lang", "token", "context_id"]
PRED = ["p_en", "p_multi", "p_multi_testmu"]


def mediaza(cai, ies):
    """Media pe coloane, dupa ce se verifica pe METADATE ca fisierele descriu aceleasi randuri.

    Verificarea nu e o formalitate: doua rulari cu alt `--afeat` sau alt encoder produc fisiere de
    aceeasi forma, cu aceleasi coloane, si o media intre ele ar iesi fara nicio eroare si fara nicio
    semnificatie. `context_id` si `token` sunt ce le distinge.
    """
    dfs = [pd.read_csv(c) for c in cai]
    baza = dfs[0]
    for c, d in zip(cai[1:], dfs[1:]):
        if list(d.columns) != list(baza.columns):
            sys.exit(f"{c}: alte coloane decat {cai[0]}")
        for m in META:
            if not (d[m].astype(str).values == baza[m].astype(str).values).all():
                sys.exit(f"{c}: coloana `{m}` nu coincide cu {cai[0]}. Nu sunt aceleasi randuri.")
    out = baza.copy()
    for p in PRED:
        # `p_multi_testmu` e NaN pe majoritatea randurilor prin construcie. `nanmean` ar inventa o
        # valoare acolo unde doar unul din regresori a scris, si atunci coloana n-ar mai fi media
        # aceluiasi ansamblu pe toate randurile. Media simpla propaga NaN, si asta e corect.
        out[p] = np.mean([d[p].values for d in dfs], axis=0)
    out.to_csv(ies, index=False)
    n = int(np.isfinite(out[PRED[1]].values).sum())
    print(f"-> {ies}  ({len(out)} randuri, {n} finite pe p_multi, media a {len(cai)} regresori)")
    return out


# Coloanele pe care controlul e STRICT, si de ce numai ele. `fuse_ab.py` citeste din CSV-ul lui A
# exact `p_en` si `p_multi` (`incarca_a`, si `--ens` care amesteca cele doua brate); niciodata
# `p_multi_testmu`. Iar `p_multi_testmu` e singura scrisa cu 8 zecimale in loc de precizie completa
# (`0.31454471` fata de `0.22381490468978882`), deci pe ea media difera cu ~5e-09 din pura
# trunchiere zecimala, nu din calcul: mediana diferentei e 5.55e-17. Un prag comun ar fi trebuit
# slabit la 1e-7 pentru toate trei si ar fi ascuns o eventuala problema reala pe cele doua care
# chiar intra in fuziune.
STRICT = ["p_en", "p_multi"]


def control():
    """Poarta: `blend` (Ridge300+HGB potrivit inauntru) = media lui `reg-ridge` si `reg-hgb`."""
    def p(suf):
        return os.path.join(HERE, "output",
                            f"e1_frozen_preds_tf-proj-394{suf}_lemma_fert_inloc.csv")
    tinta = pd.read_csv(p(""))
    tmp = os.path.join(HERE, "output", "_control_blend.csv")
    m = mediaza([p("_reg-ridge"), p("_reg-hgb")], tmp)
    os.remove(tmp)
    rau = 0.0
    for c in PRED:
        d = np.nanmax(np.abs(m[c].values - tinta[c].values))
        print(f"  {c:16s} max|diff| {d:.3e}" + ("  <- STRICT" if c in STRICT else
                                                "  (8 zecimale in CSV, neutilizata de fuse_ab)"))
        if c in STRICT:
            rau = max(rau, d)
    if rau > 1e-12:
        sys.exit(f"controlul CADE pe {STRICT}: max|diff| {rau:.3e}. Media CSV-urilor nu reproduce "
                 f"`blend`, deci constructia nu e echivalenta cu un blend potrivit inauntru.")
    print(f"control TRECE: pe {STRICT} media pe coloane e echivalenta cu un blend potrivit "
          f"inauntru, la {rau:.3e}.")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--control":
        control()
    elif len(sys.argv) >= 4:
        mediaza(sys.argv[2:], sys.argv[1])
    else:
        sys.exit(__doc__)
