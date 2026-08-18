# Demo

Runs notebook `2.2`'s within-category cosine analysis on a small **synthetic** dataset —
so the code can be tested without the real recordings. Same functions and figures as 2.2.

Each stimulus is one `(strength, interp)` pair (4 strengths × 3 interps; keys like
`sL_AF_valid_correct_active`). Cosine is computed within each `(strength, interp)`
stratum: population = split-half template cosine, single-neuron = single-trial pairwise.

## Run

```bash
python make_demo_data.py        # writes demo_data.npz (optional; already included)
jupyter nbconvert --to notebook --execute --inplace demo_cosine.ipynb
```

Needs `numpy`, `pandas`, `matplotlib`, `seaborn`, `statsmodels`, `scipy`. Runs in a few
seconds.

## Files

- `make_demo_data.py` — builds `demo_data.npz` (27 sessions, 9 birds, 3 regions).
- `demo_cosine.ipynb` — runs single-neuron + population cosine, per-region grid, passive.
- `demo_grid_active.png`, `demo_passive.png` — the output figures.

## Expected output (seed 0)

Planted effect: **population** valid > invalid, **single-neuron** valid < invalid,
**passive** null. β = valid − invalid cosine.

| Region | single-neuron β (P) | population β (P) |
|---|---|---|
| ALL | −0.225 (≪1e-3) | +0.041 (≪1e-3) |
| NCM | −0.214 (≪1e-3) | +0.042 (≪1e-3) |
| CMM | −0.221 (≪1e-3) | +0.041 (≪1e-3) |
| Field L | −0.241 (≪1e-3) | +0.041 (≪1e-3) |
| passive | ≈0 (0.89) | ≈0 (0.88) |

Δ bars use the 2.2 palette (brown = sig. positive, green = sig. negative, grey = n.s.).

The other notebooks (`2.1`, `3.x`, `4.x`) follow the same pattern on the real data.
