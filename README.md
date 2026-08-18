# Anticipatory organization of neural population dynamics speeds behavioral decisions

Analysis code and notebooks that reproduce the figures and statistics in:

> Gorman JC, Sainburg T, McPherson TS, Gentner TQ. *Anticipatory organization of neural population dynamics speeds behavioral decisions.* bioRxiv 2026.06.30.735699 (2026). https://doi.org/10.64898/2026.06.30.735699

European starlings categorize song syllables while sensory expectations are manipulated. Combining large-scale auditory-forebrain recordings with dimensionality reduction and dynamical-systems modeling, we show that expectation organizes the geometry of population trajectories in ways that reflect categorical behavior and predict single-trial accuracy and reaction time.

## System requirements

Tested on **Python 3.10.20**, Linux `5.15.0-185-generic` x86_64, glibc 2.35 (Ubuntu 22.04). Exact versions of every package, including transitive dependencies, are pinned in [`requirements-tested.txt`](requirements-tested.txt).

| Package | Tested version |
|---|---|
| numpy | 2.2.6 |
| scipy | 1.15.3 |
| pandas | 2.3.3 |
| matplotlib | 3.10.9 |
| seaborn | 0.13.2 |
| scikit-learn | 1.7.2 |
| statsmodels | 0.14.6 |
| joblib | 1.5.3 |
| tqdm | 4.67.3 |

Two lab packages by **Tim Sainburg** — `cdcp` and `behav` — are not on PyPI. The source needed by notebooks `1.1` and `4.2` is vendored under `edn_popdyn/vendor/` and placed on `sys.path` when `edn_popdyn` is imported, so no separate installation is required.

**Non-standard hardware: none required.** All analyses are CPU-only and run on a standard desktop or laptop. 

## Installation

```bash
git clone https://github.com/juliagorman/anticipatory_geometry_paper.git
cd anticipatory_geometry_paper
pip install -r requirements-tested.txt   # exact tested versions
pip install -e .                         # installs the edn_popdyn package itself
```

`pip install -e .` makes `import edn_popdyn` work from any notebook; it holds the shared data paths (`paths.py`) and figure palette (`colors.py`). To install with unpinned dependencies instead, run `pip install -e .` alone.

**Typical install time:** 2–5 minutes on a normal desktop over broadband, or seconds if the wheels are already cached.

## Demo

A small synthetic dataset and a runnable demo live in [`demo/`](demo/). 

Jupyter is not installed by `edn_popdyn`; install it first if needed (`pip install jupyterlab`).

```bash
cd demo
python make_demo_data.py        # writes demo_data.npz (optional; already included)
jupyter nbconvert --to notebook --execute --inplace demo_cosine.ipynb
```

**Expected run time:** under a minute on a normal computer

**Expected output:** `demo_grid_active.png` and `demo_passive.png`, reproducing the planted effect — population valid > invalid, single-neuron valid < invalid, passive null. Per-region β values are tabulated in [`demo/README.md`](demo/README.md).

## Instructions for use

### Running on your own data

All filesystem locations resolve in `edn_popdyn/paths.py` and are overridable by environment variable. Set these three:

| Variable | Must point at |
|---|---|
| `EDN_DATA_ROOT` | session lists, trial-event tables, and behavior tables (layout below) |
| `EDN_REP_DRIFT_DATA` | the chronic spike-sorted dataset (per-unit trial-aligned spike pickles; available on request) |
| `EDN_OUTPUT_ROOT` | where intermediates, stats, and figures are written |

```bash
export EDN_DATA_ROOT=/path/to/data
export EDN_REP_DRIFT_DATA=/path/to/chronic_spikesorted
export EDN_OUTPUT_ROOT=/path/to/outputs
```

The remaining `EDN_*` variables derive from these and rarely need setting

Expected input layout:

```
$EDN_DATA_ROOT/
├── bird_str_rec_str_ALL_list.txt              session list
├── ALL/trial_events/
│   └── <exp_dir>_trial_events_full.pickle     (or _trial_events.pickle)
└── behavior/subject_behavior_dfs/B####.pickle
```

Outputs are written to `$EDN_OUTPUT_ROOT/` as `processed_data/pop_mats` (notebook `0.1`), `processed_data/pca_data` (`0.2`), `stats/`, and `figures/`.

### Reproducing the paper

Run the notebooks in numeric order:

- `0.1`, `0.2` — preprocessing: session discovery and batch PCA
- `1.1` — psychometric behavior (Fig. 1)
- `2.1`, `2.2` — population decoding and within-category cosine similarity (Fig. 2)
- `3.1`, `3.2` — latent-dynamics model and its empirical validation (Fig. 3)
- `4.1`, `4.2` — expectation, pre-target geometry, and reaction time (Fig. 4)

Notebook `0.1` requires the raw spike-sorted dataset which is available on request. Starting from the processed data, begin at `0.2`. 

## Data

Processed neural and behavioral data will be available on Zenodo following publication. Raw recordings are available from the corresponding author on request owing to their size.

## Citation

> Gorman JC, Sainburg T, McPherson TS, Gentner TQ. *Anticipatory organization of neural population dynamics speeds behavioral decisions.* bioRxiv 2026.06.30.735699 (2026). https://doi.org/10.64898/2026.06.30.735699

## License

MIT (see [LICENSE](LICENSE)). The `edn_popdyn/vendor/` directory contains code by **Tim Sainburg** (`cdcp`, `behav`) redistributed under the **BSD 3-Clause License**; see `edn_popdyn/vendor/cdcp/LICENSE` and `edn_popdyn/vendor/behav/LICENSE`. That code retains its original license and is **not** covered by the MIT License above.

Copyright (c) 2026 Julia C. Gorman
