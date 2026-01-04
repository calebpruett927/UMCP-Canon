from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import Tuple


def prime_pi(n: int) -> int:
    """
    Prime counting function π(n): number of primes <= n.

    Deterministic sieve implementation (sufficient for typical EID bounds).
    """
    n = int(n)
    if n < 2:
        return 0
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    p = 2
    while p * p <= n:
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:n + 1:step] = b"\x00" * (((n - start) // step) + 1)
        p += 1
    return int(sum(sieve))


@dataclass(frozen=True, slots=True)
class EIDCounts:
    """
    Artifact structural fingerprint counts:
      P, Eq, Fig, Tab, List, Box, Ref
    """
    P: int
    Eq: int
    Fig: int
    Tab: int
    List: int
    Box: int
    Ref: int

    @property
    def M(self) -> int:
        # Default EID mass: sum of structural components
        return int(self.P + self.Eq + self.Fig + self.Tab + self.List + self.Box + self.Ref)


@dataclass(frozen=True, slots=True)
class EIDChecksum:
    """
    Prime-calibration triple:
      b1=10P-1, b2=9Eq+1, b3=12Fig+1, chk=[π(b1), π(b2), π(b3)]
    """
    b1: int
    b2: int
    b3: int
    c1: int
    c2: int
    c3: int

    @property
    def chk(self) -> Tuple[int, int, int]:
        return (self.c1, self.c2, self.c3)


def eid_checksum(counts: EIDCounts) -> EIDChecksum:
    b1 = 10 * int(counts.P) - 1
    b2 = 9 * int(counts.Eq) + 1
    b3 = 12 * int(counts.Fig) + 1
    return EIDChecksum(
        b1=b1, b2=b2, b3=b3,
        c1=prime_pi(b1),
        c2=prime_pi(b2),
        c3=prime_pi(b3),
    )


def delta_kappa_eid(before: EIDCounts, after: EIDCounts) -> float:
    """
    Δκ_EID = ln(M_after / M_before), where M is the EID mass.
    """
    m0 = float(before.M)
    m1 = float(after.M)
    if m0 <= 0.0 or m1 <= 0.0:
        raise ValueError("EID mass must be positive")
    return float(log(m1 / m0))
