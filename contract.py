from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass(frozen=True, slots=True)
class FrozenContract:
    """
    Frozen contract snapshot (UMA.INTSTACK.v1 style).

    Canon defaults are intended to match the most recent canonical contract snapshot and pseudocode.
    The contract is treated as part of the reproducibility boundary: change it only by an explicit seam.
    """

    contract_id: str = "UMA.INTSTACK.v1"
    a: float = 0.0
    b: float = 1.0
    face_policy: str = "pre_clip"
    epsilon: float = 1e-8
    p: int = 3
    alpha: float = 1.0
    lambda_: float = 0.2
    eta: float = 1e-3
    tol_seam: float = 0.005
    tol_id: float = 1e-9
    tz: str = "America/Chicago"
    oor_policy: str = "clip_and_flag"
    inf_rec_label: str = "∞_rec"  # typed infinite return marker (human label)

    # Canon anchors (kept here for convenience when emitting receipts/manifests)
    pre_doi: str = "10.5281/zenodo.17756705"
    post_doi: str = "10.5281/zenodo.18072852"
    weld_id: str = "W-2025-12-31-PHYS-COHERENCE"

    @classmethod
    def canon_default(cls) -> "FrozenContract":
        """Return the canonical default contract snapshot."""
        return cls()

    def snapshot_dict(self) -> Dict[str, Any]:
        """Stable dict representation suitable for manifest emission."""
        return asdict(self)
