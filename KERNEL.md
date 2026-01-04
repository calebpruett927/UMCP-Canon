Kernel Identities
=================

Tier-0: admitted trace
----------------------
You must define an embedding from raw observables x(t) to a bounded trace:

- Declare x(t) (units, sampling, measurement pipeline).
- Declare normalization/embedding N_K: x(t) ↦ Ψ(t) ∈ [0,1]^n.
- Apply OOR policy: clip to [0,1] and flag any out-of-range observations.
- Apply ε-guard only for log computations: Ψ_ε(t) = clip_[ε,1−ε](Ψ(t)).

Tier-1: reserved symbols (computed on Ψ_ε where logs appear)
-----------------------------------------------------------
Let Ψ(t) = (c_1, …, c_n), with weights w_i ≥ 0 and Σw_i = 1.

Fidelity:
  F(t) = Σ_i w_i c_i

Drift:
  ω(t) = 1 − F(t)

Entropy (weighted Bernoulli entropy):
  S(t) = − Σ_i w_i [ c_i ln c_i + (1−c_i) ln(1−c_i) ]
  (logs evaluated on ε-guarded values)

Curvature (normalized dispersion):
  C(t) = stddev({c_i}) / 0.5

Return delay (requires explicit disclosure):
- Choose a return domain generator Dθ(t) ⊆ {0,…,t−1}.
- Define Uθ(t) = { u ∈ Dθ(t) : ‖Ψ(t) − Ψ(u)‖ ≤ η }.
- τR(t) = min{ (t−u)·dt : u ∈ Uθ(t) } if Uθ(t) ≠ ∅, else ∞_rec.

Integrity ledger:
  κ(t) = Σ_i ln c_i
  IC(t) = exp(κ(t)) = Π_i c_i

Weighting note (symbol hygiene)
-------------------------------
Weights w_i apply to F and S in the kernel. The current canon pseudocode defines κ as Σ ln c_i (unweighted).
If you introduce a weighted κ for research, implement it under a new name (e.g., kappa_w) and do not relabel it κ.

Minimum disclosures for τR
--------------------------
Any reported τR is non-reproducible unless the following are frozen and exported:
- dt (cadence)
- Hrec (horizon)
- η (threshold)
- norm identity (e.g., L2)
- Dθ generator name/parameters
