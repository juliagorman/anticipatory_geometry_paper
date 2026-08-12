"""Central path configuration for the EDNpopdyn manuscript code.

Usage in a notebook or script
------------------------------
    from edn_popdyn.paths import (
        DATA_ROOT, PROCESSED_DATA_DIR, POP_MAT_ROOT, PCA_ROOT,
        FIGURES_DIR, STATS_CSV_DIR,
    )

    pop_mats = POP_MAT_ROOT / "20msbins" / "brokenup_AP_CI_4"   # 0.1 output
    latents  = PCA_ROOT                                          # 0.2 output
    fig      = FIGURES_DIR / "psychometric_curves.svg"

Where things live
-----------------
    DATA_ROOT            raw inputs to 0.1 (neural/behavioral data, NOT committed)
    OUTPUT_ROOT          everything produced from 0.1 onward (= the repo root)
      PROCESSED_DATA_DIR   <OUTPUT_ROOT>/processed_data   (intermediate data + caches)
        POP_MAT_ROOT         <PROCESSED_DATA_DIR>/pop_mats   (0.1 output, read by 0.2 + analysis nbs)
        PCA_ROOT             <PROCESSED_DATA_DIR>/pca_data   (0.2 output, read by 2.1/2.2/4.1)
      STATS_CSV_DIR        <OUTPUT_ROOT>/stats            (stats tables)
      FIGURES_DIR          <OUTPUT_ROOT>/figures          (figures)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _env_path(var: str, default: str | Path) -> Path:
    """Return Path from environment variable `var`, or `default` if unset."""
    return Path(os.environ.get(var, str(default))).expanduser()

ROOT: Path = Path(__file__).resolve().parents[1]

# Original location on the lab cluster 
_CLUSTER_ROOT = Path("/mnt/cube/jugorman/EDNpopdyn")

DATA_ROOT: Path = _env_path("EDN_DATA_ROOT", _CLUSTER_ROOT / "data")

REP_DRIFT_DATA: Path = _env_path(
    "EDN_REP_DRIFT_DATA", Path("/mnt/cube/jugorman/rep_drift/data")
)

# Per-subject behavior pickles that 1.1 reads (B####.pickle).
CDCP_BEHAVIOR_DFS: Path = _env_path(
    "EDN_CDCP_BEHAVIOR_DFS", DATA_ROOT / "behavior" / "subject_behavior_dfs"
)

# Raw Magpi behavioral data that 4.2 reads (was cdcp.paths.DATA_PATH_MAGPI).
MAGPI_RAW: Path = _env_path("EDN_MAGPI_RAW", Path("/mnt/cube/RawData/Magpi"))

BEHAVIOR_RT_DIR: Path = _env_path("EDN_BEHAVIOR_RT_DIR", DATA_ROOT / "behavior_rt")


POP_MAT_DIRNAME: str = os.environ.get("EDN_POP_MAT_DIRNAME", "PSTH_arrays")


# --------------------------------------------------------------------------- #
# Outputs
# --------------------------------------------------------------------------- #
OUTPUT_ROOT: Path = _env_path("EDN_OUTPUT_ROOT", ROOT)
PROCESSED_DATA_DIR: Path = _env_path("EDN_PROCESSED_DATA_DIR", OUTPUT_ROOT / "processed_data")

# The two processed-data products, each a single source of truth:
POP_MAT_ROOT: Path = _env_path("EDN_POP_MAT_ROOT", PROCESSED_DATA_DIR / "pop_mats")   # 0.1 output
PCA_ROOT:     Path = _env_path("EDN_PCA_ROOT",     PROCESSED_DATA_DIR / "pca_data")   # 0.2 output

STATS_CSV_DIR: Path = _env_path("EDN_STATS_CSV_DIR", OUTPUT_ROOT / "stats")
FIGURES_DIR:   Path = _env_path("EDN_FIGURES_DIR",   OUTPUT_ROOT / "figures")

# Colours helper module lives in the package itself.
COLORS_PATH: Path = Path(__file__).resolve().parent / "colors.py"


# --------------------------------------------------------------------------- #
# Convenience helpers
# --------------------------------------------------------------------------- #
def ensure_dir(path: str | Path) -> Path:
    """Create a directory (and parents) if needed; return it as a Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

for _d in (OUTPUT_ROOT, PROCESSED_DATA_DIR, POP_MAT_ROOT, PCA_ROOT, FIGURES_DIR, STATS_CSV_DIR):
    try:
        _d.mkdir(parents=True, exist_ok=True)
    except OSError:
        # e.g. read-only clone; not fatal -- caller can still read paths.
        pass


# --------------------------------------------------------------------------- #
# External lab packages (Tim Sainburg's `cdcp` and `behav`).
# --------------------------------------------------------------------------- #
VENDOR_DIR: Path = Path(__file__).resolve().parent / "vendor"
CDCP_PATH: Path = _env_path("EDN_CDCP_PATH", Path("/mnt/cube/tsainbur"))


def add_external_packages() -> None:
    """Put cdcp/behav on sys.path: prefer the in-repo vendored copy, then fall
    back to the cluster location, so `from cdcp... import ...` just works."""
    vendor = str(VENDOR_DIR)
    if os.path.isdir(vendor) and vendor not in sys.path:
        sys.path.insert(0, vendor)  # in-repo vendored copy wins
    for d in (CDCP_PATH, CDCP_PATH / "Projects" / "github_repos" / "cdcp_chronic"):
        d = str(d)
        if os.path.isdir(d) and d not in sys.path:
            sys.path.append(d)  # cluster fallback


add_external_packages()


if __name__ == "__main__":
    # `python -m edn_popdyn.paths` prints the resolved configuration.
    print("Resolved EDNpopdyn paths")
    print("-" * 60)
    for name in (
        "ROOT", "DATA_ROOT", "REP_DRIFT_DATA", "MAGPI_RAW", "BEHAVIOR_RT_DIR",
        "OUTPUT_ROOT", "PROCESSED_DATA_DIR", "POP_MAT_ROOT", "PCA_ROOT",
        "STATS_CSV_DIR", "FIGURES_DIR", "COLORS_PATH", "VENDOR_DIR", "CDCP_PATH",
    ):
        val = globals()[name]
        exists = "" if Path(val).exists() else "   [missing]"
        print(f"{name:18s} = {val}{exists}")