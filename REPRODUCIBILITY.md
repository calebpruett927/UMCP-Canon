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
