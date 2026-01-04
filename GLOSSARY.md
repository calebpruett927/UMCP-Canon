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
