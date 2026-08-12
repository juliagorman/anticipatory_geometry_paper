"""
behavior_rt_io.py -- save/load the 4.2 behavioral RT table.

Put this at src/edn_popdyn/behavior_rt_io.py.

Why it exists
-------------
4.2 currently builds its trial table by reading raw Magpi off the cluster:

    behav_data_subject = loading.load_data_pandas([subject], DATA_PATH_MAGPI)

Nobody outside the lab can do that. This module lets 4.2 build the table once,
save it, and read it back thereafter -- so the notebook runs identically on the
cluster (builds from Magpi, caches) and for someone who downloaded the Zenodo
deposit (reads the cached table, never touches Magpi).

Format
------
Parquet when pyarrow/fastparquet is available -- it round-trips dtypes exactly.
Otherwise gzipped CSV plus a small .dtypes.json sidecar, so datetimes and
categoricals survive the trip. Both are readable by any pandas; neither is a
pickle, so the deposit carries no Python-version or security baggage.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

STEM = "fig4_behavior_rt"


def _parquet_ok() -> bool:
    for mod in ("pyarrow", "fastparquet"):
        try:
            __import__(mod)
            return True
        except ImportError:
            continue
    return False


def table_path(dirpath, stem: str = STEM):
    """Return (path, kind) of an existing saved table, or (None, None)."""
    d = Path(dirpath)
    for suffix, kind in ((".parquet", "parquet"), (".csv.gz", "csv")):
        p = d / f"{stem}{suffix}"
        if p.exists():
            return p, kind
    return None, None


def save_behavior_table(df: pd.DataFrame, dirpath, stem: str = STEM) -> Path:
    """Write df to dirpath, preferring parquet. Returns the path written."""
    d = Path(dirpath)
    d.mkdir(parents=True, exist_ok=True)

    if _parquet_ok():
        out = d / f"{stem}.parquet"
        df.to_parquet(out, index=False)
    else:
        out = d / f"{stem}.csv.gz"
        df.to_csv(out, index=False, compression="gzip")
        # CSV loses dtypes; keep them alongside so load() can restore them.
        (d / f"{stem}.dtypes.json").write_text(
            json.dumps({c: str(t) for c, t in df.dtypes.items()}, indent=2)
        )

    n_subj = df["subject"].nunique() if "subject" in df else "?"
    print(f"saved {len(df):,} trials from {n_subj} subjects -> {out} "
          f"({out.stat().st_size / 1e6:.1f} MB)")
    return out


def load_behavior_table(dirpath, stem: str = STEM) -> pd.DataFrame:
    """Read the table back with dtypes restored. Raises if absent."""
    path, kind = table_path(dirpath, stem)
    if path is None:
        raise FileNotFoundError(
            f"no {stem}.parquet or {stem}.csv.gz in {dirpath}. "
            "Run 4.2 once on the cluster to build it from Magpi."
        )

    if kind == "parquet":
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path, compression="gzip", low_memory=False)
        sidecar = Path(dirpath) / f"{stem}.dtypes.json"
        if sidecar.exists():
            for col, dt in json.loads(sidecar.read_text()).items():
                if col not in df.columns:
                    continue
                try:
                    if dt.startswith("datetime"):
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                    elif dt == "category":
                        df[col] = df[col].astype("category")
                    elif dt == "bool":
                        # CSV writes True/False; guard against NaN-widened columns
                        df[col] = df[col].map(
                            {"True": True, "False": False, True: True, False: False}
                        ).astype("boolean").astype(dt) if df[col].notna().all() \
                            else df[col].map({"True": True, "False": False,
                                              True: True, False: False})
                    else:
                        df[col] = df[col].astype(dt)
                except (ValueError, TypeError):
                    pass          # leave the column as pandas inferred it

    n_subj = df["subject"].nunique() if "subject" in df else "?"
    print(f"loaded {len(df):,} trials from {n_subj} subjects <- {path}")
    return df