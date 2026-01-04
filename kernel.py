from __future__ import annotations

from dataclasses import dataclass
from statistics import pstdev
from typing import Callable, List, Optional, Sequence

import math

from umcp.contract import FrozenContract
from umcp.tier0 import eps_guard, l2_norm


@dataclass(frozen=True, slots=True)
class Tier1Row:
    """
    Tier-1 kernel row computed on an admitted trace Ψ(t) ∈ [0,1]^n.

    Canon pseudocode:
      F = Σ w_i c_i
      ω = 1 - F
      S = -Σ w_i [ c_i ln c_i + (1-c_i) ln(1-c_i) ]
      C = stddev({c_i}) / 0.5
      τR = min{∆t>0 : ||Ψ(t)-Ψ(t-∆t)|| < η} within Hrec
      κ = Σ ln c_i
      I = exp(κ)
    """

    t: int
    psi: tuple[float, ...]
    weights: tuple[float, ...]
    dt: float
    h_rec: float
    eta: float

    F: float
    omega: float
    S: float
    C: float
    tau_R: float
    kappa: float
    I: float

    @property
    def IC(self) -> float:
        """Alias: canon sometimes labels I as IC in stack summaries."""
        return self.I


def _normalize_weights(w: Optional[Sequence[float]], n: int) -> List[float]:
    if w is None:
        return [1.0 / n] * n
    if len(w) != n:
        raise ValueError("weights length must match channel dimension n")
    s = float(sum(w))
    if s <= 0.0:
        raise ValueError("weights must sum to a positive value")
    return [float(x) / s for x in w]


def _weighted_bernoulli_entropy(c_eps: Sequence[float], w: Sequence[float]) -> float:
    total = 0.0
    for ci, wi in zip(c_eps, w):
        ci = float(ci)
        total += wi * (ci * math.log(ci) + (1.0 - ci) * math.log(1.0 - ci))
    return -total


def _curvature_sigma_over_half(c: Sequence[float]) -> float:
    # pstdev is population standard deviation
    sigma = pstdev([float(x) for x in c]) if len(c) > 1 else 0.0
    return sigma / 0.5


def _tau_R_for_index(
    psi_series: Sequence[Sequence[float]],
    t: int,
    *,
    dt: float,
    eta: float,
    h_rec: float,
    norm: Callable[[Sequence[float], Sequence[float]], float],
) -> float:
    if t <= 0:
        return math.inf
    max_lag = int(math.floor(h_rec / dt)) if dt > 0 else 0
    max_lag = max(1, max_lag)
    best: Optional[int] = None
    for lag in range(1, min(t, max_lag) + 1):
        u = t - lag
        if norm(psi_series[t], psi_series[u]) < eta:
            best = lag
            break
    if best is None:
        return math.inf
    return best * dt


def compute_tier1_series(
    psi_series: Sequence[Sequence[float]],
    *,
    contract: FrozenContract,
    weights: Optional[Sequence[float]] = None,
    dt: float,
    h_rec: float,
    eta: Optional[float] = None,
    norm: Callable[[Sequence[float], Sequence[float]], float] = l2_norm,
) -> List[Tier1Row]:
    """
    Compute Tier-1 rows for a discrete admitted trace.

    - psi_series must already be face-policy admitted: each channel in [0,1].
    - dt, h_rec, norm, eta must be disclosed for τR to be reproducible.
    """
    if not psi_series:
        raise ValueError("psi_series is empty")
    n = len(psi_series[0])
    for v in psi_series:
        if len(v) != n:
            raise ValueError("psi_series must have constant dimension n")

    w = _normalize_weights(weights, n)
    eta_val = float(eta) if eta is not None else float(contract.eta)

    out: List[Tier1Row] = []
    for t, psi in enumerate(psi_series):
        c = [float(x) for x in psi]
        c_eps = eps_guard(c, contract.epsilon)

        F = sum(wi * ci for wi, ci in zip(w, c))
        omega = 1.0 - F
        S = _weighted_bernoulli_entropy(c_eps, w)
        C = _curvature_sigma_over_half(c)

        tau_R = _tau_R_for_index(
            psi_series,
            t,
            dt=dt,
            eta=eta_val,
            h_rec=h_rec,
            norm=norm,
        )

        kappa = sum(math.log(ci) for ci in c_eps)
        I = math.exp(kappa)

        out.append(
            Tier1Row(
                t=t,
                psi=tuple(c),
                weights=tuple(w),
                dt=float(dt),
                h_rec=float(h_rec),
                eta=eta_val,
                F=float(F),
                omega=float(omega),
                S=float(S),
                C=float(C),
                tau_R=float(tau_R),
                kappa=float(kappa),
                I=float(I),
            )
        )
    return out
