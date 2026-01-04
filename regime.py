from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from umcp.kernel import Tier1Row


Regime = Literal["Stable", "Watch", "Collapse"]
Phi = Literal["S", "W", "C"]


@dataclass(frozen=True, slots=True)
class RegimeResult:
    regime: Regime
    phi: Phi
    critical: bool  # overlay flag (I < 0.30 by default)

    @property
    def label(self) -> str:
        if self.critical:
            return f"{self.regime} (Critical)"
        return self.regime


def classify_regime(
    row: Tier1Row,
    *,
    stable_omega_max: float = 0.038,
    stable_F_min: float = 0.90,
    stable_S_max: float = 0.15,
    stable_C_max: float = 0.14,
    collapse_omega_min: float = 0.30,
    critical_I_min: float = 0.30,
) -> RegimeResult:
    """
    Kernel-only regime labeling with a 'Critical' overlay.

    Stable gate set:
      ω < 0.038 AND F > 0.90 AND S < 0.15 AND C < 0.14
    Collapse:
      ω ≥ 0.30
    Else:
      Watch
    """
    stable = (
        row.omega < stable_omega_max
        and row.F > stable_F_min
        and row.S < stable_S_max
        and row.C < stable_C_max
    )
    if stable:
        regime: Regime = "Stable"
        phi: Phi = "S"
    elif row.omega >= collapse_omega_min:
        regime = "Collapse"
        phi = "C"
    else:
        regime = "Watch"
        phi = "W"

    critical = row.I < critical_I_min
    return RegimeResult(regime=regime, phi=phi, critical=critical)
