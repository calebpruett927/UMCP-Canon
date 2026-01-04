from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

import math

from umcp.closures import GammaClosure
from umcp.kernel import Tier1Row
from umcp.regime import classify_regime


@dataclass(frozen=True, slots=True)
class SS1mWeld:
    """
    SeamStamp v1-mini (weld row), minimal but audit-sufficient.

    Required fields follow the canonical receipt pattern:
      Δκ, ir, s, tol, θ, ϕ, Weld-ID, PRE, POST (+ identity + return checks).
    """

    delta_kappa: float
    ir: float
    s: float
    tol: float
    theta: str
    phi: str
    weld_id: str
    pre_id: str
    post_id: str

    tau_R: float
    R: float
    D_omega: float
    D_C: float

    identity_ok: bool
    return_ok: bool
    pass_ok: bool
    delta_exp: float

    gamma_id: str
    alpha: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class WeldResult:
    ss1m: SS1mWeld


def evaluate_weld(
    *,
    pre: Tier1Row,
    post: Tier1Row,
    tau_r: float,
    gamma: GammaClosure,
    alpha: float,
    tol_seam: float,
    tol_id: float,
    infer_R: bool = False,
    R: Optional[float] = None,
    theta: str = "θ",
    weld_id: str = "WELD",
    pre_id: str = "PRE",
    post_id: str = "POST",
) -> WeldResult:
    """
    Evaluate a PRE->POST weld row under a declared closure set.

    First law / ledger identity (for budget):
      Δκ_budget = R·τR − (Dω + DC)

    Residual definition:
      s = R·τR − (Δκ_ledger + Dω + DC)

    PASS iff:
      - τR is finite (return_ok)
      - identity check ok: |(I_post/I_pre) - exp(Δκ)| ≤ tol_id
      - |s| ≤ tol_seam
    """
    tau_r_val = float(tau_r)
    return_ok = math.isfinite(tau_r_val)

    delta_kappa = float(post.kappa - pre.kappa)

    # Identity check: compare the ratio I_post/I_pre to exp(Δκ)
    ir_ratio = float(post.I / pre.I) if pre.I != 0.0 else math.inf
    ir_expected = float(math.exp(delta_kappa))
    identity_ok = abs(ir_ratio - ir_expected) <= float(tol_id)

    D_omega = float(gamma(pre.omega))
    D_C = float(alpha) * float(pre.C)

    if R is None:
        if infer_R:
            if not return_ok or tau_r_val == 0.0:
                R_val = 0.0
            else:
                R_val = float((delta_kappa + D_omega + D_C) / tau_r_val)
        else:
            raise ValueError("R must be provided unless infer_R=True")
    else:
        R_val = float(R)

    # Typed censoring: if no return, R·τR contributes 0 by policy.
    return_term = float(R_val * tau_r_val) if return_ok else 0.0

    s = float(return_term - (delta_kappa + D_omega + D_C))

    pass_ok = (abs(s) <= float(tol_seam)) and return_ok and identity_ok

    phi = classify_regime(post).phi  # report regime context (not a gate here)

    ss1m = SS1mWeld(
        delta_kappa=delta_kappa,
        ir=ir_expected,
        s=s,
        tol=float(tol_seam),
        theta=str(theta),
        phi=str(phi),
        weld_id=str(weld_id),
        pre_id=str(pre_id),
        post_id=str(post_id),
        tau_R=tau_r_val,
        R=R_val,
        D_omega=D_omega,
        D_C=D_C,
        identity_ok=identity_ok,
        return_ok=return_ok,
        pass_ok=pass_ok,
        delta_exp=float(tol_id),
        gamma_id=getattr(gamma, "closure_id", gamma.__class__.__name__),
        alpha=float(alpha),
    )
    return WeldResult(ss1m=ss1m)
