"""Generate a small synthetic dataset for the notebook-2.2 cosine-similarity demo.

Writes `demo_data.npz`: fake recording sessions spread across 3 brain regions
(NCM, CMM, Field L), 9 birds, 3 sessions each. Each session is a dict of condition
-> array [trials x time-bins x units].

Each STIMULUS is one (strength, interp) pair -- 4 strengths x 3 interps = 12 stimuli.
Keys carry strength / interp / validity / accuracy / modality, e.g.
`sL_AF_valid_correct_active` and `sL_AF_invalid_passive`. The cosine similarity is
compared between SAME-CATEGORY stimuli (same L/R side), matching the manuscript's
"cosine between the two same-category stimuli".

Planted effects (so the demo recovers the paper's pattern):
  * ACTIVE, POPULATION scale: valid-cue same-category templates are more aligned than
    invalid -> valid > invalid cosine (population geometry).
  * ACTIVE, SINGLE-NEURON scale: valid-cue single trials are much noisier than invalid,
    so single-trial vectors are less similar -> valid < invalid cosine. The anticipatory
    organization is a population-geometry effect, not visible at the single-neuron level.
  * PASSIVE: valid and invalid share the same templates -> no effect at either scale.

Usage:
    python make_demo_data.py        # writes demo_data.npz next to this file
"""
import os
import numpy as np

STRENGTHS = ("sL", "wL", "wR", "sR")
INTERPS   = ("AF", "BF", "CE")
CATEGORY  = {"sL": "L", "wL": "L", "wR": "R", "sR": "R"}
STIMULI   = [(s, ip) for s in STRENGTHS for ip in INTERPS]     # 12 (strength, interp) stimuli

N_DIMS, N_BINS, N_TRIALS, SESSIONS_PER_BIRD = 5, 20, 30, 3
INTERP_SEP = 0.25          # how far each interp shifts the stimulus from its category mean

# Bird -> brain region (real IDs; region assignment is for the demo grid).
BIRD_REGION = {
    "B1248": "NCM",     "B1593": "NCM",     "B1595": "NCM",
    "B1188": "CMM",     "B1426": "CMM",     "B1432": "CMM",
    "B1244": "Field L", "B1170": "Field L", "B1276": "Field L",
}

# ACTIVE — validity -> (template scatter eps, trial-to-trial noise).
#   valid  : aligned templates (population HIGH) + very noisy trials (single-neuron LOW)
#   invalid: scattered templates (population LOW) + clean trials (single-neuron HIGH)
_ACTIVE = {"valid": (0.15, 0.90), "invalid": (0.70, 0.02)}
_PASSIVE_EPS, _PASSIVE_NOISE = 0.45, 0.10     # valid & invalid share a template -> null


def make_neural_trial_dicts(seed=0):
    """Return {session: {condition_key: array[trials x time x units]}}."""
    rng = np.random.default_rng(seed)
    temporal = np.exp(-0.5 * ((np.arange(N_BINS) - N_BINS * 0.45) / (N_BINS * 0.18)) ** 2) + 0.2

    def trials_from(spatial, noise):
        signal = np.outer(temporal, spatial)                                  # [time x units]
        return (signal[None] + noise * rng.normal(size=(N_TRIALS, N_BINS, N_DIMS))).astype(np.float32)

    def unit(v): return v / np.linalg.norm(v)

    all_td = {}
    for bird in BIRD_REGION:
        for k in range(SESSIONS_PER_BIRD):
            muL = unit(rng.normal(size=N_DIMS)); muR = unit(rng.normal(size=N_DIMS))
            interp_dir = {ip: unit(rng.normal(size=N_DIMS)) for ip in INTERPS}   # per-interp shift
            td = {}
            # ACTIVE: valid and invalid drawn separately (they differ)
            for validity, (eps, noise) in _ACTIVE.items():
                for st, ip in STIMULI:
                    mu = (muL if CATEGORY[st] == "L" else muR) + INTERP_SEP * interp_dir[ip]
                    spatial = mu + eps * rng.normal(size=N_DIMS)
                    td[f"{st}_{ip}_{validity}_correct_active"] = trials_from(spatial, noise)
            # PASSIVE: valid and invalid share one template per stimulus -> true null
            for st, ip in STIMULI:
                mu = (muL if CATEGORY[st] == "L" else muR) + INTERP_SEP * interp_dir[ip]
                spatial = mu + _PASSIVE_EPS * rng.normal(size=N_DIMS)
                for validity in ("valid", "invalid"):
                    td[f"{st}_{ip}_{validity}_passive"] = trials_from(spatial, _PASSIVE_NOISE)
            all_td[f"{bird}_2021-05-0{k + 1}_sess{k}"] = td
    return all_td


def save(path="demo_data.npz", seed=0):
    td = make_neural_trial_dicts(seed)
    flat = {f"{sess}|||{cond}": arr for sess, d in td.items() for cond, arr in d.items()}
    np.savez_compressed(path, **flat)
    print(f"wrote {path}: {len(td)} sessions, {len(flat)} condition arrays, "
          f"{os.path.getsize(path) / 1e6:.1f} MB")


def load(path="demo_data.npz"):
    """Reload demo_data.npz back into {session: {condition: array}}."""
    z = np.load(path, allow_pickle=False)
    td = {}
    for flatkey in z.files:
        sess, cond = flatkey.split("|||")
        td.setdefault(sess, {})[cond] = z[flatkey]
    return td


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    save(os.path.join(here, "demo_data.npz"))
