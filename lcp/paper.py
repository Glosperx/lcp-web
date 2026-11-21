"""Point lcp_model/data.py at the paper's release folder (read-only), without copying any data.

Sets MLSP_DIR and ROLCP_CSV, and data.DATA_DIR, data.CACHE_DIR, data.PRED_DIR, which data.py reads
when its functions are called. Nothing is written there by the stage 1 scripts.
"""
import os

import data


def use_release(release):
    release = os.path.abspath(release)
    if not os.path.isdir(release):
        raise SystemExit(f"paper release folder not found: {release}")
    data.DATA_DIR = os.path.join(release, "data")
    data.CACHE_DIR = os.path.join(release, "cache")
    data.PRED_DIR = os.path.join(release, "predictions")
    os.environ["MLSP_DIR"] = os.path.realpath(os.path.join(data.DATA_DIR, "MLSP2024"))
    os.environ["ROLCP_CSV"] = os.path.realpath(os.path.join(data.DATA_DIR, "RoLCP.csv"))
    return release
