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


Docs
----
- Canon overview: docs/CANON.md
- Frozen contract: docs/CONTRACT.md
- Kernel identities: docs/KERNEL.md
- Weld + SS1m: docs/WELD.md
- Glossary: docs/GLOSSARY.md
- Repro checklist: docs/REPRODUCIBILITY.md
- Scope note: docs/SCOPE.md

  Glossary
========

Admitted trace (Ψ):
A bounded vector time-series Ψ(t) ∈ [0,1]^n produced by a declared embedding N_K and an OOR policy.

Face policy:
The admission rule applied before Tier-1 computation (typically pre_clip to [0,1]).

OOR (out-of-range) flags:
Per-channel markers indicating values observed outside [0,1] prior to clipping.

ε-guard:
A numerical clip to [ε, 1−ε] used only to keep ln(c) and ln(1−c) stable.

Tier-0:
Embedding, normalization, admission, and policy flags that produce Ψ(t).

Tier-1 (kernel):
Reserved invariants computed on Ψ(t): {F, ω, S, C, τR, κ, IC}.

Tier-2 (overlays):
Diagnostics, controllers, narratives, or alternate metrics that must not redefine Tier-1 symbols.

Weights (w_i):
Nonnegative coefficients summing to 1 used in weighted kernel quantities (F and S).

Return domain (Dθ):
The set of candidate past indices allowed for a return search at time t, declared by a generator with parameters θ.

Return set (Uθ):
Past indices u in Dθ with ‖Ψ(t)−Ψ(u)‖ ≤ η.

Return delay (τR):
The smallest time lag to a return within Uθ, expressed in physical time via dt; ∞_rec if none exists.

Closure:
A declared, versioned assumption used in the weld budget (e.g., Γ(ω), DC, R policy).

Weld (seam):
A PRE→POST continuity evaluation that is only meaningful when contract, return settings, and closures are disclosed.

SS1m:
A minimal seam-stamp receipt format used to log weld inputs/assumptions/results in an auditable way.

Residual (s):
The difference between the budget and ledger: s = Δκ_budget − Δκ_ledger.

Regime labels:
Stable/Watch/Collapse derived from kernel gates; “Critical” is a diagnostic overlay (e.g., IC < 0.30).

Reproducibility Checklist
=========================

This kernel is deterministic only after you freeze what is measured and how returns are defined.

Minimum to reproduce Tier-1
---------------------------
Provide:
- The admitted trace Ψ(t) in [0,1]^n, or raw x(t) plus a complete embedding spec N_K.
- The weights w_i (or state that they are uniform).
- The frozen contract snapshot (parameters + policy flags).

Minimum to reproduce τR
-----------------------
Provide:
- dt (cadence)
- Hrec (horizon)
- η (threshold)
- norm identity (e.g., L2)
- return-domain generator name and parameters (Dθ)

Minimum to reproduce a weld claim
---------------------------------
Provide:
- PRE row and POST row (Tier-1 values, at minimum κ, IC, ω, C)
- τR used for the seam (and its reproducibility disclosures)
- Closure IDs and definitions:
  - Γ(ω; …)
  - DC definition (usually αC) and α
  - R policy (explicit R or “infer_R=true”)
- tol_seam and tol_id
- SS1m(weld) receipt

Recommended export bundle (one directory)
-----------------------------------------
bundle/
  contract.json
  ingest.json
  freeze.json
  tier1.json
  regimes.json
  weld_ss1m.json   (optional)
  manifest.json    (SHA256 of every file)

Recommended practice
--------------------
- Treat the manifest hash as a stable audit handle.
- Never compare results across differing contracts/closures without a seam note.
- If a weld fails, report it as an audit outcome; do not tune assumptions post hoc to force PASS.

Scope and Intent
================

This repository is not a “model of the world.” It is a ledger.

The kernel is universal in form:
- It measures an admitted trace Ψ(t) and computes invariants that are stable under disclosed assumptions.
- It separates identities (Tier-1) from assumptions (closures) by construction.

Continuity is not asserted by narrative.
Continuity is asserted only where a return exists under a declared horizon, and the weld budget closes under disclosed closures.

If a return does not exist, the correct output is not metaphysics.
The correct output is a typed boundary: “no return observed,” and therefore no continuity credit.
