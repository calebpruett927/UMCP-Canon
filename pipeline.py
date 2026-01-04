from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable, Dict, List, Optional, Sequence

from umcp.closures import GammaClosure, GammaOmegaPower
from umcp.contract import FrozenContract
from umcp.kernel import Tier1Row, compute_tier1_series
from umcp.regime import RegimeResult, classify_regime
from umcp.tier0 import ClipFlag, normalize_to_admitted_trace, l2_norm
from umcp.weld import WeldResult, evaluate_weld


@dataclass(frozen=True, slots=True)
class IngestSpec:
    """
    Tier-0 ingest declaration: defines what is measured and how it is embedded.

    For a publication-grade artifact, you would also record:
      - units and instrumentation for each raw observable,
      - feature extractors g_i,
      - calibration / bounds (l_i, u_i),
      - missing-data policy and OOR policy (clip+flag).
    """
    lows: Sequence[float]
    highs: Sequence[float]


@dataclass(frozen=True, slots=True)
class FreezeSpec:
    """
    Frozen run bundle: contract + return settings + weights + closure registry.
    """
    contract: FrozenContract
    weights: Optional[Sequence[float]]
    dt: float
    h_rec: float
    eta: float
    norm: Callable[[Sequence[float], Sequence[float]], float]
    gamma: GammaClosure
    alpha: float
    tol_seam: float
    tol_id: float


@dataclass(frozen=True, slots=True)
class ComputeResult:
    psi: List[List[float]]
    clip_flags: List[List[ClipFlag]]
    tier1: List[Tier1Row]
    regimes: List[RegimeResult]


class UMCPSession:
    """
    Minimal "Start → /ingest → /freeze → /compute → /regime → /render → /export" orchestrator.

    This keeps the canonical sequence explicit while remaining light enough for a GitHub reference repo.
    """
    def __init__(self) -> None:
        self._ingest: Optional[IngestSpec] = None
        self._freeze: Optional[FreezeSpec] = None
        self._compute: Optional[ComputeResult] = None

    def ingest(self, *, lows: Sequence[float], highs: Sequence[float]) -> "UMCPSession":
        self._ingest = IngestSpec(lows=list(lows), highs=list(highs))
        return self

    def freeze(
        self,
        *,
        contract: Optional[FrozenContract] = None,
        weights: Optional[Sequence[float]] = None,
        dt: float,
        h_rec: float,
        eta: Optional[float] = None,
        norm: Callable[[Sequence[float], Sequence[float]], float] = l2_norm,
        gamma: Optional[GammaClosure] = None,
        alpha: Optional[float] = None,
        tol_seam: Optional[float] = None,
        tol_id: Optional[float] = None,
    ) -> "UMCPSession":
        c = contract or FrozenContract.canon_default()
        self._freeze = FreezeSpec(
            contract=c,
            weights=weights,
            dt=float(dt),
            h_rec=float(h_rec),
            eta=float(eta) if eta is not None else float(c.eta),
            norm=norm,
            gamma=gamma or GammaOmegaPower(p=c.p),
            alpha=float(alpha) if alpha is not None else float(c.alpha),
            tol_seam=float(tol_seam) if tol_seam is not None else float(c.tol_seam),
            tol_id=float(tol_id) if tol_id is not None else float(c.tol_id),
        )
        return self

    def compute(self, *, x_series: Sequence[Sequence[float]]) -> ComputeResult:
        if self._ingest is None:
            raise RuntimeError("Nonconformant: /ingest must be declared before /compute")
        if self._freeze is None:
            raise RuntimeError("Nonconformant: /freeze must be declared before /compute")

        psi, clip_flags = normalize_to_admitted_trace(
            x_series=x_series,
            lows=self._ingest.lows,
            highs=self._ingest.highs,
        )
        tier1 = compute_tier1_series(
            psi,
            contract=self._freeze.contract,
            weights=self._freeze.weights,
            dt=self._freeze.dt,
            h_rec=self._freeze.h_rec,
            eta=self._freeze.eta,
            norm=self._freeze.norm,
        )
        regimes = [classify_regime(r) for r in tier1]
        self._compute = ComputeResult(psi=psi, clip_flags=clip_flags, tier1=tier1, regimes=regimes)
        return self._compute

    def weld(
        self,
        *,
        pre_index: int,
        post_index: int,
        tau_r: float,
        infer_R: bool = True,
        R: Optional[float] = None,
        theta: str = "θ",
        weld_id: Optional[str] = None,
        pre_id: Optional[str] = None,
        post_id: Optional[str] = None,
    ) -> WeldResult:
        if self._freeze is None or self._compute is None:
            raise RuntimeError("Nonconformant: /freeze and /compute must occur before /weld")

        c = self._freeze.contract
        return evaluate_weld(
            pre=self._compute.tier1[pre_index],
            post=self._compute.tier1[post_index],
            tau_r=float(tau_r),
            gamma=self._freeze.gamma,
            alpha=self._freeze.alpha,
            tol_seam=self._freeze.tol_seam,
            tol_id=self._freeze.tol_id,
            infer_R=infer_R,
            R=R,
            theta=theta,
            weld_id=weld_id or c.weld_id,
            pre_id=pre_id or c.pre_doi,
            post_id=post_id or c.post_doi,
        )

    def render_compute_json(self) -> str:
        """
        Render the compute result to JSON for export (simple reference serializer).
        """
        if self._compute is None:
            raise RuntimeError("Nothing to render; run /compute first")
        payload: Dict[str, Any] = {
            "psi": self._compute.psi,
            "tier1": [
                dict(
                    t=r.t, psi=list(r.psi), weights=list(r.weights), dt=r.dt, h_rec=r.h_rec, eta=r.eta,
                    F=r.F, omega=r.omega, S=r.S, C=r.C, tau_R=r.tau_R, kappa=r.kappa, I=r.I
                )
                for r in self._compute.tier1
            ],
            "regimes": [asdict(rr) for rr in self._compute.regimes],
        }
        import json
        return json.dumps(payload, indent=2)
