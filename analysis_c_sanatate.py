"""Poarta de sanatate pentru semnalul C: poate modelul sa modeleze TEXT BRUT?

De ce exista, si e o masuratoare, nu o precautie. Coloana `C` a lui `gemma4-12b-4bit` din
`output/bakeoff_test*/` are surprisal mediu **21-25 nati per subword**, in timp ce vocabularul lui are
262.144 de intrari, deci o distributie UNIFORMA ar da ln(262144) = 12.48 nati. O valoare peste
uniform e imposibila pentru un model antrenat pe text real, deci coloana nu masoara previzibilitate.

Diagnosticul, rulat pe 23 august 2026: modelul e sanatos, dar numai prin sablonul de chat.

    prin sablon:   "What is the capital of France?" -> "Paris"; rate("thrombocytopenia") = 0.905,
                   rate("water") = 0.000. Semnalul B e in regula.
    pe text brut:  "The capital of France is" -> "1111111111111111111111111"

`surprisal()` scoreaza deliberat o secventa DATA, fara sablon de chat, fiindca asa se defineste
previzibilitatea contextuala. Pentru un model base asta e corect. Pentru `gemma-4-12B-it-qat`, care e
instruction-tuned SI cuantizat cu antrenare, capacitatea de continuare pe text brut a disparut, iar
`<bos>` nu o aduce inapoi (ajuta: 23.06 -> 14.84 pe "Paris", dar argmaxul ramane o cifra).

Deci C nu e o cantitate care se poate cere oricarui model din bazin, si asta nu se vedea din nicio
cifra agregata: r al lui C cu eticheta iese -0.065, adica "aproape zero", exact cum ar iesi si un
semnal slab dar valid.

## Cele trei probe, si de ce toate trei

  1. `uniform`     surprisal mediu pe itemi REALI din test < ln(|V|). E granita imposibilului, nu un
                   prag de calitate: peste ea, modelul e mai prost decat aruncarea cu zarul.
  2. `degenerare`  continuarea greedy pe text brut are >= 3 tokeni distincti din 10. Prinde colapsul
                   pe un singur token, care e chiar tiparul lui Gemma.
  3. `ordonare`    surprisal(continuare corecta) < surprisal(continuare implauzibila). E proba de
                   semnal: fara ea, C n-ar ordona itemii nici daca marimile ar fi plauzibile.

Proba 3 NU e suficienta singura: Gemma o trece (23.06 fata de 28.79) desi e degenerat. De aia poarta
cere toate trei.

Rulare:
  python analysis_c_sanatate.py                       # toate modelele din LLM_POOL
  python analysis_c_sanatate.py --model qwen3-8b-4bit
"""
import argparse
import gc
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

# Perechi (context, continuare corecta, continuare implauzibila) pentru proba de ordonare. Ambele
# continuari sunt nume proprii de orase, deci difera prin potrivirea in context, nu prin frecventa.
ORDONARE = [("The capital of France is {}.", "Paris", "Bucharest"),
            ("She drank a glass of {}.", "water", "granite")]
N_ITEMI = 30       # itemi reali per proba `uniform`, esantionati cu pas fix peste toate limbile


def probe(r):
    """Cele trei probe pe un rater deja incarcat. -> dict cu cifrele si verdictul."""
    from mlsp_common import load_mlsp
    t = r.hf_tok
    V = int(getattr(t, "vocab_size", 0) or len(t))
    lnV = float(np.log(V))

    ml = load_mlsp("test")
    pas = max(1, len(ml) // N_ITEMI)
    esant = ml.iloc[::pas].head(N_ITEMI)
    s = np.array([r.surprisal(str(x.sent), str(x.token)) for x in esant.itertuples()], float)
    s_fin = s[np.isfinite(s)]
    s_med = float(s_fin.mean()) if len(s_fin) else float("nan")

    # Decodare greedy pe TEXT BRUT, prin `_logits_last`, care are deja ambele backend-uri. Calea
    # romaneasca merge pe `transformers` cu RoLlama3, deci poarta trebuie sa poata fi rulata si acolo:
    # riscul e acelasi, un model instruction-tuned care si-a pierdut continuarea pe text brut.
    ids = t("The capital of France is")["input_ids"]
    cur = list(ids)
    for _ in range(10):
        cur.append(int(np.asarray(r._logits_last(cur)).argmax()))
    cont = t.decode(cur[len(ids):])
    n_dist = len(set(cur[len(ids):]))

    ord_ok, ord_det = True, []
    for sab, bun, rau in ORDONARE:
        a, b = r.surprisal(sab.format(bun), bun), r.surprisal(sab.format(rau), rau)
        ord_det.append(f"{bun} {a:.2f} < {rau} {b:.2f}" if a < b else
                       f"{bun} {a:.2f} !>= {rau} {b:.2f}")
        ord_ok &= bool(np.isfinite(a) and np.isfinite(b) and a < b)

    p1, p2, p3 = s_med < lnV, n_dist >= 3, ord_ok
    return dict(vocab=V, ln_vocab=round(lnV, 2), surprisal_mediu=round(s_med, 2),
                n_itemi=int(len(s_fin)), uniform=p1, tokeni_distincti=n_dist, degenerare=p2,
                ordonare=p3, continuare=repr(cont)[:60], detaliu_ordonare="; ".join(ord_det),
                SANATOS=bool(p1 and p2 and p3))


def main(argv=None):
    from mlsp_common import LLM_POOL
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", action="append", default=None)
    ap.add_argument("--out", default="e_c_sanatate.md")
    a = ap.parse_args(argv)
    chei = a.model or list(LLM_POOL)

    from solution_bert import LLMRater
    rows = []
    for k in chei:
        print(f"\n[S] {k}", flush=True)
        try:
            r = LLMRater(k)
            d = probe(r)
            del r
            gc.collect()
        except Exception as ex:
            d = dict(SANATOS=False, detaliu_ordonare=f"EROARE: {type(ex).__name__}: {ex}"[:160])
        d["model"] = k
        rows.append(d)
        print(f"    {'SANATOS' if d.get('SANATOS') else 'DEGENERAT'}  "
              f"surprisal_mediu={d.get('surprisal_mediu')} ln|V|={d.get('ln_vocab')} "
              f"continuare={d.get('continuare')}", flush=True)

    t = pd.DataFrame(rows).set_index("model")
    cols = ["SANATOS", "surprisal_mediu", "ln_vocab", "uniform", "tokeni_distincti",
            "degenerare", "ordonare", "n_itemi"]
    cols = [c for c in cols if c in t.columns]
    L = ["# Poarta de sanatate pentru semnalul C", "",
         "Generat de `analysis_c_sanatate.py`. Trei probe pe TEXT BRUT, fara sablon de chat, "
         "fiindca asa se calculeaza surprisal-ul. Un model care pica poarta **nu poate furniza C**, "
         "indiferent cat de bun e semnalul lui B.", "",
         "```", t[cols].to_string(), "```", "",
         "## Detalii", "", "```",
         t[[c for c in ("continuare", "detaliu_ordonare") if c in t.columns]].to_string(), "```", "",
         f"**Sanatoase: {int(t['SANATOS'].sum())} din {len(t)}.** "
         f"Modele care NU pot furniza C: "
         f"{sorted(t.index[~t['SANATOS'].astype(bool)]) or 'niciunul'}.", "",
         "Pragul `uniform` e ln(|V|), adica surprisal-ul unei distributii uniforme. Nu e un prag de "
         "calitate, e granita imposibilului: un model peste ea e mai prost decat zarul.", ""]
    dest = os.path.join(OUT, a.out)
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n" + "\n".join(L))
    print(f"-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
