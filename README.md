UMCP Canon Kernel (Tier-0 → Tier-1 → Weld)
=========================================

This repository is a clean, contract-first reference implementation of:

- Tier-0: bounded admitted trace construction Ψ(t) ∈ [0,1]^n under a frozen contract (clip+flag, ε-guard).
- Tier-1: kernel invariants {F, ω, S, C, τR, κ, I}.
- Weld: admissibility checks (finite return, identity check, residual |s| ≤ tol) + SS1m receipt emission.

Canon anchors (for provenance in manifests / SS1m receipts):
- PRE: "The Episteme of Return" DOI 10.5281/zenodo.17756705
- POST: "The Physics of Coherence: Recursive Collapse & Continuity Laws" DOI 10.5281/zenodo.18072852
- Weld ID: W-2025-12-31-PHYS-COHERENCE

Design goals
------------
1) Symbol hygiene: Tier-1 symbols are computed exactly as defined; closures are explicit.
2) Reproducibility: τR requires a declared norm, η, cadence dt, and horizon Hrec.
3) Auditability: SS1m(weld) rows are produced with explicit PASS/FAIL outcomes.
4) Minimal dependencies: core kernel is pure-Python. (CLI CSV convenience is optional.)

Quick start (library)
---------------------
```python
from umcp.contract import FrozenContract
from umcp.kernel import compute_tier1_series
from umcp.regime import classify_regime
from umcp.weld import evaluate_weld
from umcp.closures import GammaOmegaPower

contract = FrozenContract.canon_default()

# A toy admitted trace: list of vectors (each vector is c_i in [0,1])
psi = [
    [0.97, 0.98, 0.99, 0.98],
    [0.97, 0.98, 0.99, 0.98],
    [0.98, 0.985, 0.99, 0.985],
]

rows = compute_tier1_series(
    psi,
    contract=contract,
    weights=[0.25, 0.25, 0.25, 0.25],
    dt=0.001,          # 1 ms cadence
    h_rec=2.0,         # 2 s horizon
    eta=0.02,          # return threshold
)

for r in rows:
    print(r.t, classify_regime(r))

# Example weld between two states (PRE and POST) with an observed τR
gamma = GammaOmegaPower(p=contract.p)
pre, post = rows[0], rows[-1]
weld = evaluate_weld(
    pre=pre,
    post=post,
    tau_r=0.8,
    gamma=gamma,
    alpha=contract.alpha,
    tol_seam=contract.tol_seam,
    tol_id=contract.tol_id,
    infer_R=True,
    theta="PHYS-04",
)

print(weld.pass_ok, weld.ss1m)
```

CLI (optional)
--------------
Install with:
```bash
pip install -e ".[cli]"
```

Compute Tier-1 from a CSV of admitted Ψ(t):
```bash
umcp kernel --csv path/to/psi.csv --dt 0.001 --hrec 2.0 --eta 0.02
```

Compute a weld row from JSON inputs:
```bash
umcp weld --pre pre.json --post post.json --tauR 0.8 --infer-R
```

Repository layout
-----------------
- umcp/contract.py   Frozen contract snapshot + canonical defaults
- umcp/tier0.py      normalization and clip+flag helpers
- umcp/kernel.py     Tier-1 computation on admitted Ψ(t)
- umcp/closures.py   Γ(ω) closures (drift-cost) with explicit IDs
- umcp/regime.py     Stable/Watch/Collapse (+ Critical overlay) labeling
- umcp/weld.py       Weld evaluation + SS1m receipt dataclasses
- umcp/manifest.py   SHA256 / manifest helpers for audit bundles
- tests/             pytest coverage for key identities

Notes on κ and I
----------------
This implementation follows the current canon pseudocode where:

- κ = Σ_i ln c_i
- I = exp(κ) = Π_i c_i

Weights w_i apply to F and S, but not to κ in the canon pseudocode.
If you need a weighted-κ variant for research, implement it as a *separate* overlay
(e.g., `kappa_w`) so Tier-1 symbol reservation remains intact.

License
-------
MIT. See LICENSE.


Pipeline wrapper (optional)
-------------------------
```python
from umcp.pipeline import UMCPSession

sess = (
    UMCPSession()
    .ingest(lows=[0,0,0,0], highs=[10,10,10,10])
    .freeze(dt=0.001, h_rec=2.0, eta=0.02)
)
compute = sess.compute(x_series=[[1,2,3,4],[1,2,3,4],[1.1,2,3.1,4]])
weld = sess.weld(pre_index=0, post_index=2, tau_r=0.8, theta="PHYS-04")
print(weld.ss1m.pass_ok)
```

Development workflow (recommended)
----------------------------------
- Install dev tooling: `pip install -e ".[dev]"` then `pre-commit install`
- Lint: `ruff check .`
- Tests: `pytest`

EID utilities (optional)
------------------------
This repo includes a small `umcp.eid` module for EID mass and the prime-calibration checksum triple.
These are export/audit utilities and do not modify Tier-1 kernel computation.
