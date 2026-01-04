Frozen Contract
===============

The kernel is contract-first. The contract snapshot is part of the reproducibility boundary.

Contract ID
-----------
UMA.INTSTACK.v1

Canonical defaults (repo implementation)
----------------------------------------
- (a, b) = (0, 1)          admitted range for Ψ(t)
- face policy = pre_clip   admission occurs before Tier-1 computation
- OOR policy = clip_and_flag
- ε = 1e-8                 log-stability guard (clip to [ε, 1−ε] for logs)
- p = 3                    Γ(ω) power closure parameter (when using ω^p)
- α = 1                    curvature cost scale (DC = αC)
- λ = 0.2                  reserved for higher layers (kept for completeness)
- η = 1e-3                 default return threshold (override per dataset if needed)
- tol_seam = 0.005         weld residual tolerance
- tol_id = 1e-9            identity tolerance for exp/log checks
- TZ = America/Chicago
- typed infinite return marker = ∞_rec (human label; implementation uses math.inf)

Interpretation notes
--------------------
Admission vs. numerical guards:
- Face admission is a semantic policy: values outside [0,1] are clipped and flagged.
- ε-guard is purely numerical: values are clipped to [ε, 1−ε] *only* when evaluating logs.

Seam rule (non-negotiable)
--------------------------
Any change to contract defaults is a seam event. If you change them:
- Document the change (what and why).
- Version the repo and the contract snapshot explicitly.
- Update tests and any worked examples.
- Never present results across differing contracts as directly comparable without a weld.

Recommended practice
--------------------
Emit a contract snapshot in every export bundle (JSON), and treat that JSON’s hash as a first-class audit handle.
