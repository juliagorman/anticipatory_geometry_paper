# Anticipatory organization of neural population dynamics speeds behavioral decisions

Analysis code and notebooks that reproduce the figures and statistics in:

> Gorman JC, Sainburg T, McPherson TS, Gentner TQ. *Anticipatory organization of neural population dynamics speeds behavioral decisions.* bioRxiv 2026.06.30.735699 (2026). https://doi.org/10.64898/2026.06.30.735699

European starlings categorize song syllables while sensory expectations are manipulated. Combining large-scale auditory-forebrain recordings with dimensionality reduction and dynamical-systems modeling, we show that expectation organizes the geometry of population trajectories in ways that reflect categorical behavior and predict single-trial accuracy and reaction time.

## Installation

```bash
git clone https://github.com/juliagorman/anticipatory_geometry_paper.git
cd anticipatory_geometry_paper
pip install -e .
```

`pip install -e .` makes `import edn_popdyn` work from any notebook — it holds the shared data paths (`paths.py`) and figure color palette (`colors.py`).

Dependencies: `numpy`, `scipy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `statsmodels`, `joblib`, and `tqdm` (see [System requirements](#system-requirements) for tested versions).

Two lab packages by **Tim Sainburg** — `cdcp` and `behav` — are not on PyPI. The source needed by notebooks `1.1` and `4.2` is vendored under `src/edn_popdyn/vendor/` and put on `sys.path` automatically when `edn_popdyn` is imported, so the notebooks' `from cdcp… import …` lines work with no extra setup.

## Reproducing the paper

Point `EDN_DATA_ROOT` at the data, then run the notebooks in numeric order (`0.1` → `4.2`):

- `0.1`, `0.2` — preprocessing: session discovery and batch PCA
- `1.1` — psychometric behavior (Fig. 1)
- `2.1`, `2.2` — population decoding and within-category cosine similarity (Fig. 2)
- `3.1`, `3.2` — latent-dynamics model and its empirical validation (Fig. 3)
- `4.1`, `4.2` — expectation, pre-target geometry, and reaction time (Fig. 4)

Figures are written to `results/figures/` and stats tables to `results/stats_csv/`. All paths come from `src/edn_popdyn/paths.py` and can be overridden with the `EDN_*` environment variables — no code edits needed.

## System requirements

### Software dependencies

The versions below are the ones the analysis was **tested on**; other recent versions are likely to work but have not been verified.

- **Operating system tested:** Linux `5.15.0-185-generic`, x86_64, glibc 2.35 (Ubuntu 22.04)
- **Python:** 3.10.20

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
| nbformat | 5.10.4 |

The two lab packages `cdcp` and `behav` are vendored under `src/edn_popdyn/vendor/` and require no separate installation.

### Non-standard hardware

**None required.** All analyses are **CPU-only — no GPU is needed** — and run on a standard desktop or laptop. Some steps distribute work across multiple CPU cores in parallel (via `joblib`, e.g. `n_jobs=8`); a multi-core processor shortens run time but is not required, and the code runs correctly on a single core. No specialized or non-standard hardware is needed.

## Data

The neural and behavioral data are large and are **not** included in this repository. Processed data will be published on Zendo; raw recordings are available upon request.

## Citation

If you use this code, please cite:

> Gorman JC, Sainburg T, McPherson TS, Gentner TQ. *Anticipatory organization of neural population dynamics speeds behavioral decisions.* bioRxiv 2026.06.30.735699 (2026). https://doi.org/10.64898/2026.06.30.735699

## License

This repository is released under the MIT License (see [LICENSE](LICENSE)).

### Third-party code

The `edn_popdyn/vendor/` directory contains code by **Tim Sainburg** (`cdcp` and
`behav`), redistributed under the **BSD 3-Clause License**. See the `LICENSE`
file within each vendored package (`edn_popdyn/vendor/cdcp/LICENSE` and
`edn_popdyn/vendor/behav/LICENSE`) for the full terms. This third-party code
retains its original license and is **not** covered by the MIT License above.

Copyright (c) 2026 Julia C. Gorman
