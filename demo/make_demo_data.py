"""Synthetic dataset for the notebook-2.2 cosine demo. Writes demo_data.npz."""
import os
import numpy as np

STRENGTHS = ("sL", "wL", "wR", "sR")
INTERPS   = ("AF", "BF", "CE")
CATEGORY  = {"sL": "L", "wL": "L", "wR": "R", "sR": "R"}
STIMULI   = [(s, ip) for s in STRENGTHS for ip in INTERPS]
BIRD_REGION = {
    "B1248": "NCM", "B1593": "NCM", "B1595": "NCM",
    "B1188": "CMM", "B1426": "CMM", "B1432": "CMM",
    "B1244": "Field L", "B1170": "Field L", "B1276": "Field L",
}
N_DIMS, N_BINS, SESSIONS_PER_BIRD, INTERP_SEP = 5, 20, 3, 0.25
N_VALID, S_VALID     = 50, 0.5     # many trials + higher noise  -> POP split-half up, SN pairwise down
N_INVALID, S_INVALID = 8, 0.25     # few trials + lower noise
N_PASSIVE, S_PASSIVE = 16, 0.4     # equal valid/invalid -> null


def make_neural_trial_dicts(seed=0):
    rng = np.random.default_rng(seed)
    temporal = np.exp(-0.5 * ((np.arange(N_BINS) - N_BINS * 0.45) / (N_BINS * 0.18)) ** 2) + 0.2

    def trials(spatial, n, noise):
        return (np.outer(temporal, spatial)[None] + noise * rng.normal(size=(n, N_BINS, N_DIMS))).astype(np.float32)

    def unit(v):
        return v / np.linalg.norm(v)

    all_td = {}
    for bird in BIRD_REGION:
        for k in range(SESSIONS_PER_BIRD):
            muL = unit(rng.normal(size=N_DIMS)); muR = unit(rng.normal(size=N_DIMS))
            idir = {ip: unit(rng.normal(size=N_DIMS)) for ip in INTERPS}
            td = {}
            for st, ip in STIMULI:
                mu = (muL if CATEGORY[st] == "L" else muR) + INTERP_SEP * idir[ip]
                td[f"{st}_{ip}_valid_correct_active"]   = trials(mu, N_VALID, S_VALID)
                td[f"{st}_{ip}_invalid_correct_active"] = trials(mu, N_INVALID, S_INVALID)
                td[f"{st}_{ip}_valid_passive"]          = trials(mu, N_PASSIVE, S_PASSIVE)
                td[f"{st}_{ip}_invalid_passive"]        = trials(mu, N_PASSIVE, S_PASSIVE)
            all_td[f"{bird}_2021-05-0{k + 1}_sess{k}"] = td
    return all_td


def save(path="demo_data.npz", seed=0):
    td = make_neural_trial_dicts(seed)
    flat = {f"{s}|||{c}": a for s, d in td.items() for c, a in d.items()}
    np.savez_compressed(path, **flat)
    print(f"wrote {path}: {len(td)} sessions, {os.path.getsize(path) / 1e6:.1f} MB")


def load(path="demo_data.npz"):
    z = np.load(path, allow_pickle=False)
    td = {}
    for k in z.files:
        s, c = k.split("|||"); td.setdefault(s, {})[c] = z[k]
    return td


if __name__ == "__main__":
    save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_data.npz"))
