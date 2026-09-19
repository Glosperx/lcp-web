"""Bloc 0: descarca greutatile necesare, cu revision= fixat la fiecare repo.

Doua grupuri:
  --encoder : xlm-roberta-base, blocant pentru E1 (in cache erau doar tokenizerele).
  --pool    : bazinul de bake-off, brat universal, MLX 4-bit, ~28.6 GB.

De ce revision= la fiecare: un `main` mutat schimba greutatile, deci cifrele, in tacere.
SHA-urile grupului MLX sunt cele reconfirmate pe 16 august (planul de bake-off, §12.4).

Scrie output/bloc0_downloads.md dupa FIECARE repo terminat, ca o intrerupere sa nu piarda evidenta.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python download_pool.py --encoder --pool
"""
import argparse
import os
import subprocess
import sys
import time

OUT = "output"
LOG = os.path.join(OUT, "bloc0_downloads.md")

# Encoderul lui E1. allow_patterns taie copiile tf/jax/onnx/pytorch.bin din repo:
# fara filtru s-ar descarca de cateva ori aceleasi greutati in formate nefolosite.
ENCODER = [
    dict(repo="FacebookAI/xlm-roberta-base",
         revision="e73636d4f797dec63c3081bb6ed5c7b0bb3f2089",
         allow=["config.json", "model.safetensors", "sentencepiece.bpe.model",
                "tokenizer.json", "tokenizer_config.json"],
         gb=1.1, note="encoder E1"),
]

# Bratul universal, toate la aceeasi precizie (MLX 4-bit), ca sa nu amestece modelul cu cuantizarea.
POOL = [
    dict(repo="mlx-community/Qwen3-8B-4bit",
         revision="545dc4251c05440727734bcd94334791f6ab0192", allow=None, gb=4.61, note="brat universal"),
    dict(repo="mlx-community/Qwen3.5-9B-MLX-4bit",
         revision="938d8919941c6e7efd3c7150eff7fe9d12afa631", allow=None, gb=5.95, note="brat universal"),
    dict(repo="mlx-community/gemma-4-12B-it-qat-OptiQ-4bit",
         revision="63912b888c04ba2c555f198685d10b05f54cf564", allow=None, gb=9.00, note="brat universal"),
    dict(repo="mlx-community/Meta-Llama-3.1-8B-Instruct-4bit",
         revision="241a666dad6cb93c8ff213d39a7f34a36bf26db4", allow=None, gb=4.52, note="referinta, joaca in ambele comparatii"),
    dict(repo="mlx-community/aya-expanse-8b-4bit",
         revision="3a7cee37dd4ab4ed76642f61f6253da4748e63ba", allow=None, gb=4.52, note="brat universal"),
]

# Controlul de cuantizare: aceleasi doua modele si pe 8 biti, rulate pe cele 300 de instante de trial
# langa variantele lor pe 4 biti. Asa costul cuantizarii e MASURAT, nu presupus, si nu mai e nevoie de
# ipoteza ca 4 bitii nu strica semnalul B. Gemma nu apare aici: checkpoint-ul ales e QAT, antrenat cu
# cuantizarea in bucla, iar varianta QAT pe 8 biti nu exista (404), deci perechea n-ar fi controlata.
CONTROL_8BIT = [
    dict(repo="mlx-community/Qwen3-8B-8bit",
         revision="48a0b75b1ae72503e21e1558d040bc227510ff06", allow=None, gb=8.72,
         note="control, brat principal declarat"),
    dict(repo="mlx-community/Qwen3.5-9B-MLX-8bit",
         revision="84f7c2deea248d8df56240f88102def51c7ed5d6", allow=None, gb=10.45,
         note="control, candidat de robustete"),
    dict(repo="mlx-community/gemma-4-12B-it-qat-8bit",
         revision="eafed06893a6ee299315ebe0e0feb82f435e92fe", allow=None, gb=12.72,
         note="control, modelul lui B din sistem"),
]


def _dir_bytes(path):
    """Octeti reali. snapshot_download intoarce un director de symlink-uri catre blobs/, deci se
    masoara tinta, altfel totul iese 0."""
    total, seen = 0, set()
    for root, _, files in os.walk(path):
        for f in files:
            real = os.path.realpath(os.path.join(root, f))
            if real not in seen and os.path.exists(real):
                seen.add(real)
                total += os.path.getsize(real)
    return total


def note(line):
    os.makedirs(OUT, exist_ok=True)
    new = not os.path.exists(LOG)
    with open(LOG, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# Bloc 0: descarcari, cu revision fixat\n\n"
                     "| repo | revision | GB pe disc | secunde | terminat |\n"
                     "|---|---|---|---|---|\n")
        fh.write(line + "\n")


def fetch(item):
    from huggingface_hub import snapshot_download
    t0 = time.time()
    print(f"[desc] {item['repo']} @ {item['revision'][:12]} (~{item['gb']} GB, {item['note']})", flush=True)
    path = snapshot_download(repo_id=item["repo"], revision=item["revision"],
                             allow_patterns=item["allow"])
    dt = time.time() - t0
    gb = _dir_bytes(path) / 1e9
    note(f"| `{item['repo']}` | `{item['revision']}` | {gb:.2f} | {int(dt)} | "
         f"{time.strftime('%H:%M:%S')} |")
    print(f"  -> {gb:.2f} GB in {int(dt)}s  {path}", flush=True)
    return gb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--encoder", action="store_true", help="xlm-roberta-base, blocant pentru E1")
    ap.add_argument("--pool", action="store_true", help="cele 5 MLX 4-bit, brat universal")
    ap.add_argument("--control8", action="store_true",
                    help="Qwen3-8B si Qwen3.5-9B si pe 8 biti, controlul de cuantizare")
    a = ap.parse_args()
    if not (a.encoder or a.pool or a.control8):
        sys.exit("alege --encoder, --pool si/sau --control8")

    items = ((ENCODER if a.encoder else []) + (POOL if a.pool else [])
             + (CONTROL_8BIT if a.control8 else []))
    total = 0.0
    for it in items:
        try:
            total += fetch(it)
        except Exception as ex:
            msg = str(ex).split("\n")[0][:200]
            print(f"  EROARE {it['repo']}: {msg}", flush=True)
            note(f"| `{it['repo']}` | `{it['revision']}` | EROARE | | {msg} |")
    print(f"\n[bloc 0] gata, {total:.2f} GB. Evidenta in {LOG}")

    free = subprocess.run(["df", "-h", os.path.expanduser("~")], capture_output=True, text=True)
    print(free.stdout.strip().splitlines()[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
