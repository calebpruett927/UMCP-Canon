Contributing
============

This repository is a reference implementation of a contract-first kernel. The primary objective is
symbol hygiene and auditability. Contributions are welcome, but must preserve the canonical semantics.

Ground rules (non-negotiable)
-----------------------------

1) Tier-1 symbol reservation is strict.
   The following fields are treated as kernel invariants and must not change meaning:
   {F, omega (ω), S, C, tau_R (τR), kappa (κ), I (IC)}.

2) Contract changes are seam events.
   If you change any defaults in `FrozenContract.canon_default()`, treat it as a seam:
   document it in the PR and update tests and README accordingly.

3) Closures are explicit and versioned.
   Welds depend on declared closures. Any change to a closure must change its `closure_id`
   and include tests that demonstrate behavior.

4) Return reproducibility is required for τR.
   Any τR computation must be parameterized by and export: dt, Hrec, η, and the norm identity.

What is encouraged
------------------

- Additional diagnostics or overlays as separate names (Tier-2 style), never by redefining Tier-1.
- Export/manifest improvements that increase reproducibility.
- Additional return-domain generators (explicitly named and exported).
- Additional tests and documentation.

Process
-------

1) Fork and create a feature branch.
2) Install dev tooling:

   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   pre-commit install

3) Ensure:
   ruff check .
   pytest

4) Open a PR. Use the checklist in the PR template.
