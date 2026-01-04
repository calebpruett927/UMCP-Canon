from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import math


@dataclass(frozen=True, slots=True)
class ClipFlag:
    """
    Records whether an out-of-range value was observed and clipped.

    This is deliberately simple: it supports "clip-and-flag" auditing without imposing
    a specific logging backend.
    """

    clipped: bool
    below: bool
    above: bool


def _clip01(x: float) -> Tuple[float, ClipFlag]:
    if x < 0.0:
        return 0.0, ClipFlag(clipped=True, below=True, above=False)
    if x > 1.0:
        return 1.0, ClipFlag(clipped=True, below=False, above=True)
    return x, ClipFlag(clipped=False, below=False, above=False)


def clip01_vector(vec: Sequence[float]) -> Tuple[List[float], List[ClipFlag]]:
    out: List[float] = []
    flags: List[ClipFlag] = []
    for v in vec:
        c, f = _clip01(float(v))
        out.append(c)
        flags.append(f)
    return out, flags


def eps_guard(vec01: Sequence[float], eps: float) -> List[float]:
    """
    ε-guarded clipping for log-stability: clip to [eps, 1-eps].

    This is *not* a face-policy clip; it is a numerical guard to keep ln(c) and ln(1-c) stable.
    """
    lo = float(eps)
    hi = 1.0 - float(eps)
    return [min(hi, max(lo, float(v))) for v in vec01]


def affine_normalize(x: Sequence[float], lows: Sequence[float], highs: Sequence[float]) -> List[float]:
    """
    Per-channel affine mapping to [0,1] before face-policy clipping:

        c_i = (x_i - low_i) / (high_i - low_i)

    Division-by-zero in bounds is not silently repaired; callers should treat it as a contract error.
    """
    if len(x) != len(lows) or len(x) != len(highs):
        raise ValueError("x, lows, highs must have the same length")
    out: List[float] = []
    for xi, lo, hi in zip(x, lows, highs):
        denom = float(hi) - float(lo)
        if denom == 0.0:
            raise ZeroDivisionError("Normalization bound high==low produces undefined affine map")
        out.append((float(xi) - float(lo)) / denom)
    return out


def normalize_to_admitted_trace(
    x_series: Iterable[Sequence[float]],
    lows: Sequence[float],
    highs: Sequence[float],
) -> Tuple[List[List[float]], List[List[ClipFlag]]]:
    """
    Convenience Tier-0: affine normalize + face-policy clip[0,1] + clip flags.
    """
    psi: List[List[float]] = []
    flags_all: List[List[ClipFlag]] = []
    for x in x_series:
        y = affine_normalize(x, lows, highs)
        c, flags = clip01_vector(y)
        psi.append(c)
        flags_all.append(flags)
    return psi, flags_all


def l2_norm(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((float(x) - float(y)) ** 2 for x, y in zip(a, b)))
