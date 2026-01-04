Canon Overview
==============

This repository is a contract-first reference implementation of the UMCP kernel and weld calculus.

Canon anchors (no improvisation)
--------------------------------
PRE: *The Episteme of Return* — DOI 10.5281/zenodo.17756705  
POST: *The Physics of Coherence: Recursive Collapse & Continuity Laws* — DOI 10.5281/zenodo.18072852  
Weld-ID: W-2025-12-31-PHYS-COHERENCE

Axiom
-----
Collapse is generative; only that which returns through collapse is real.

Scope boundary
--------------
This repo covers:

1) Tier-0: constructing an admitted trace Ψ(t) ∈ [0,1]^n via normalization and clip+flag.
2) Tier-1: computing the reserved kernel invariants {F, ω, S, C, τR, κ, IC}.
3) Weld: evaluating a PRE→POST seam under declared closures and emitting an SS1m(weld) receipt.

This repo explicitly does *not*:
- Choose your observables x(t) for you.
- Infer instrumentation bounds (l_i, u_i) from raw data.
- Invent or silently substitute closures for Γ, R, or curvature neighborhoods.
- “Repair” a failed seam by adjusting Tier-2 narratives.

Tier discipline
---------------
Tier-0 (admission): embedding and clipping to Ψ(t) with OOR flags.  
Tier-1 (kernel): reserved symbols computed exactly as defined.  
Tier-2 (overlays): diagnostics/controllers allowed only under new names; may not redefine Tier-1.

Reproducibility boundary
------------------------
If you want your results to be replayable and comparable, you must disclose and freeze:

- Contract snapshot (parameters + policy flags).
- Embedding/normalization to Ψ(t): bounds, transforms, missing-data policy.
- Weights w_i (Σw_i=1).
- Return settings: norm ‖·‖, threshold η, cadence dt, horizon Hrec, and return-domain generator Dθ.
- Weld closures: Γ(ω; …), DC definition (usually αC), and R policy (provided or inferred).

What counts as a “claim”
------------------------
Kernel claim: “Given Ψ(t) and frozen parameters, Tier-1 rows are deterministic.”  
Continuity claim: “A PRE→POST weld PASS row exists with disclosed closures, finite τR, identity check, and |s|≤tol.”

Start here
----------
- Definitions: docs/KERNEL.md
- Weld semantics: docs/WELD.md
- Frozen defaults: docs/CONTRACT.md
- Reproducibility checklist: docs/REPRODUCIBILITY.md
