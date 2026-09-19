"""Ruleaza TabFM peste blocurile exportate. Se cheama din venv-ul izolat sau din Colab.

    ~/.local/share/tabfm-venv/bin/python tabfm_runner.py data/tabfm_blocks_proj200.npz data/tabfm_preds

Nu importa nimic din proiect in afara de `tabfm_bridge`, care la nivel de modul cere numai numpy.
Toata logica e acolo; fisierul asta e doar linia de comanda. Variabilele de mediu recunoscute sunt
TABFM_DEVICE, TABFM_ESTIMATORS, TABFM_MAX_ROWS si TABFM_DTYPE.
"""
import sys

import numpy as np

from tabfm_bridge import ruleaza


def main(argv):
    if len(argv) != 3:
        raise SystemExit(__doc__)
    ruleaza(np.load(argv[1]), argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
