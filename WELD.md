Weld and SS1m Receipts
======================

A weld is a PRE→POST seam event. A continuity claim is asserted only when a weld PASS receipt exists.

Ledger identity
---------------
Given Tier-1 rows at t0 (PRE) and t1 (POST):

Δκ_ledger = κ1 − κ0
ir = IC1 / IC0
By definition: Δκ_ledger = ln(ir)

Budget model (requires closures)
-------------------------------
Δκ_budget = R·τR − (Dω + DC)

Closures must be declared and versioned:
- Dω = Γ(ω; …)   drift-cost closure (e.g., ω^p with frozen p)
- DC = αC        curvature cost (α frozen in contract, or explicitly overridden)
- R              return credit rate (provided or inferred; must be disclosed)

Residual
--------
s = Δκ_budget − Δκ_ledger

Typed censoring
---------------
If τR = ∞_rec (no return observed under Hrec and η), then the return term contributes no credit:
R·τR := 0
This is not “failure”; it is “no return observed,” which forbids continuity credit.

PASS conditions
---------------
A weld PASS is true iff:
1) Return is finite: τR < ∞_rec
2) Residual tolerance: |s| ≤ tol_seam
3) Identity check: | (IC1/IC0) − exp(Δκ_ledger) | ≤ tol_id

SS1m(weld) minimal fields
-------------------------
A weld receipt should include, at minimum:
- Δκ_ledger, ir
- τR, R, Dω, DC
- s, tol_seam, tol_id
- θ label (domain/seam label) and ϕ regime context (optional; diagnostic only)
- Weld-ID, PRE DOI, POST DOI
- closure IDs (at least Γ id and α/DC definition)

Example SS1m(weld) JSON (shape)
-------------------------------
{
  "delta_kappa": ...,
  "ir": ...,
  "tau_R": ...,
  "R": ...,
  "D_omega": ...,
  "D_C": ...,
  "s": ...,
  "tol": ...,
  "delta_exp": ...,
  "identity_ok": true,
  "return_ok": true,
  "pass_ok": true,
  "theta": "PHYS-04",
  "phi": "S",
  "weld_id": "W-2025-12-31-PHYS-COHERENCE",
  "pre_id": "10.5281/zenodo.17756705",
  "post_id": "10.5281/zenodo.18072852",
  "gamma_id": "GammaOmegaPower(p=3)",
  "alpha": 1.0
}

Interpretation discipline
-------------------------
- A PASS weld is a continuity statement under declared closures.
- A FAIL weld is not “wrong”; it is an audit result: either no return, or the budget does not close under the stated assumptions.
- Do not change closures to force PASS after the fact; if assumptions change, that is a different seam.
