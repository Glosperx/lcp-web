"""Etapa 0 din bake-off: fertilitatea tokenizerelor pe tintele MLSP.

Incarca DOAR tokenizerele (cativa MB fiecare), nicio greutate de model.
Produce output/fertility_by_lang.csv: subword-uri per tinta, per limba, per tokenizer.

Serveste trei lucruri deodata:
  1. coloana de fertilitate XLM-R din E7;
  2. confirmarea independenta ca modelul candidat trateaza rezonabil si/fil;
  3. tabelul comparativ de tokenizere pentru anexa.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python measure_fertility.py
"""
import os, glob, sys
import numpy as np
import pandas as pd

DATA = "data"
OUT = "output"

# Maparea limbii si incarcarea datelor stau acum in mlsp_common.py, sursa unica pentru calea
# multilingva. Aici erau scrise prima data, in etapa 0.
from mlsp_common import MLSP_LANGS, lang_code, load_mlsp  # noqa: E402,F401


def fertility(tok, targets, prefix_space):
    """Subword-uri per tinta, plus normalizarile per caracter si per octet.

    prefix_space simuleaza pozitia din mijlocul propozitiei. Conteaza pentru
    SentencePiece si BPE cu marcaj de inceput de cuvant: "1" si " 1" dau id-uri
    diferite. Tintele MLSP apar in interiorul contextului, deci varianta cu spatiu
    e cea reprezentativa.

    tok/caracter si tok/octet sunt singurele marimi comparabile intre sisteme de
    scriere: o tinta japoneza are 3.59 caractere in medie fata de 8.78 la italiana,
    iar sinhaleza are 3.00 octeti per caracter fata de 1.00 la engleza. Un raport
    tok/octet apropiat de 0.5 inseamna byte fallback, adica tokenizerul nu are
    merge-uri pentru scrierea respectiva.
    """
    n, nch, nby = [], [], []
    for t in targets:
        t = str(t)
        s = (" " + t) if prefix_space else t
        n.append(len(tok.encode(s, add_special_tokens=False)))
        nch.append(max(len(t), 1))
        nby.append(max(len(t.encode("utf-8")), 1))
    return (np.array(n, dtype=float), np.array(nch, dtype=float),
            np.array(nby, dtype=float))


TOKENIZERS = [
    ("xlmr",          "xlm-roberta-base"),
    ("qwen3-8b",      "Qwen/Qwen3-8B"),
    ("qwen3.5-9b",    "Qwen/Qwen3.5-9B"),
    ("gemma4-12b",    "google/gemma-4-12B-it"),
    ("llama3.1-8b",   "meta-llama/Llama-3.1-8B-Instruct"),
    ("aya-expanse-8b", "CohereLabs/aya-expanse-8b"),
    ("tiny-aya",      "CohereLabs/tiny-aya-global"),
    ("eurollm-9b",    "utter-project/EuroLLM-9B-Instruct"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    from transformers import AutoTokenizer

    ml = load_mlsp("test")
    print(f"MLSP test: {len(ml)} tinte, {ml['lang'].nunique()} limbi")
    print(ml.groupby("lang").size().to_string(), "\n")

    # Verificare de sanatate: XLM-R pe romana trebuie sa dea ~1.95 (masurat anterior in proiect).
    ro = None
    ro_path = os.path.join(DATA, "test_set.csv")
    if os.path.exists(ro_path):
        ro = pd.read_csv(ro_path)["token"].astype(str).tolist()
        print(f"RoLCP: {len(ro)} tinte romanesti pentru verificarea de sanatate\n")

    recs, failed = [], []
    for tag, name in TOKENIZERS:
        try:
            tok = AutoTokenizer.from_pretrained(name)
        except Exception as e:
            msg = str(e).split("\n")[0][:160]
            print(f"[SARIT] {tag:15s} {name}\n         {msg}")
            failed.append((tag, name, msg))
            continue

        vocab = len(tok)
        groups = [(lg, g["token"].tolist()) for lg, g in ml.groupby("lang")]
        if ro is not None:
            groups.append(("ro_rolcp", ro))
        for ps in (True, False):
            for lg, tgs in groups:
                f, nch, nby = fertility(tok, tgs, ps)
                recs.append(dict(tokenizer=tag, model=name, vocab=vocab, lang=lg,
                                 prefix_space=ps, n=len(f), fert_mean=f.mean(),
                                 fert_median=float(np.median(f)), fert_max=f.max(),
                                 tok_per_char=(f / nch).mean(),
                                 tok_per_byte=(f / nby).mean(),
                                 pct_single=float((f == 1).mean())))
        print(f"[OK]    {tag:15s} vocab={vocab}")

    df = pd.DataFrame(recs)
    path = os.path.join(OUT, "fertility_by_lang.csv")
    df.to_csv(path, index=False)
    print(f"\nScris {path}  ({len(df)} randuri)")

    # prefix_space=True e conventia de raportat: reproduce cifra de 1.95 masurata
    # anterior in proiect pentru XLM-R pe romana.
    d = df[df.prefix_space]
    for col, titlu in [("fert_mean", "subword-uri per tinta"),
                       ("tok_per_char", "subword-uri per CARACTER (comparabil intre scrieri)"),
                       ("tok_per_byte", "subword-uri per octet (>0.5 = byte fallback)")]:
        piv = d.pivot(index="lang", columns="tokenizer", values=col).round(3)
        print(f"\n=== {titlu}, prefix_space=True ===")
        print(piv.to_string())

    if failed:
        print("\n=== tokenizere indisponibile ===")
        for tag, name, msg in failed:
            print(f"  {tag:15s} {name}\n    {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
