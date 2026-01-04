from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import math


class GammaClosure(Protocol):
    """
    Drift-cost closure Γ(ω) used to compute D_ω.

    Closures are not Tier-1 identities. They must be declared and versioned for weld claims.
    """

    closure_id: str

    def __call__(self, omega: float) -> float: ...


@dataclass(frozen=True, slots=True)
class GammaOmegaPower:
    """
    Γ(ω) = ω^p (example closure; matches the canonical worked example when p is frozen).
    """

    p: int = 3

    @property
    def closure_id(self) -> str:
        return f"GammaOmegaPower(p={self.p})"

    def __call__(self, omega: float) -> float:
        o = float(omega)
        if o < 0.0:
            # ω<0 is nonphysical under canonical definition ω=1-F with F in [0,1];
            # still, keep it total and explicit.
            return -((-o) ** self.p)
        return o**self.p


@dataclass(frozen=True, slots=True)
class GammaNegLogOneMinusOmega:
    """
    Γ(ω) = -ln(1 - ω + ε) (alternative closure; not implied by canon, provided for research).

    Use only as an explicitly declared closure; do not silently substitute it into canonical claims.
    """

    epsilon: float = 1e-8

    @property
    def closure_id(self) -> str:
        return f"GammaNegLogOneMinusOmega(eps={self.epsilon:g})"

    def __call__(self, omega: float) -> float:
        return -math.log(max(self.epsilon, 1.0 - float(omega) + self.epsilon))
