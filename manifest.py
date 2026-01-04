from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone


def sha256_file(path: str | Path) -> str:
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj: Any) -> str:
    """
    Deterministic JSON serialization (for hashing / manifests).
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True, slots=True)
class Manifest:
    """
    Minimal provenance bundle for audit.

    Not all fields are always available (e.g., git commit hash in offline contexts).
    """
    created_utc: str
    python: str
    platform: str
    inputs: Dict[str, Any]
    artifacts: Dict[str, Any]
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return canonical_json(self.to_dict())


def build_manifest(
    *,
    inputs: Dict[str, Any],
    artifact_paths: Iterable[str | Path] = (),
    notes: Optional[str] = None,
) -> Manifest:
    artifacts: Dict[str, Any] = {}
    for ap in artifact_paths:
        p = Path(ap)
        artifacts[str(p)] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}

    created_utc = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return Manifest(
        created_utc=created_utc,
        python=sys.version.split()[0],
        platform=f"{platform.system()} {platform.release()}",
        inputs=inputs,
        artifacts=artifacts,
        notes=notes,
    )
