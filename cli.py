from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence

from umcp.closures import GammaOmegaPower
from umcp.contract import FrozenContract
from umcp.kernel import Tier1Row, compute_tier1_series
from umcp.weld import evaluate_weld


def _read_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _row_from_json(d: Dict[str, Any]) -> Tier1Row:
    # Minimal parser for weld CLI; expects the Tier1Row fields used by evaluate_weld.
    return Tier1Row(
        t=int(d["t"]),
        psi=tuple(d["psi"]),
        weights=tuple(d["weights"]),
        dt=float(d["dt"]),
        h_rec=float(d["h_rec"]),
        eta=float(d["eta"]),
        F=float(d["F"]),
        omega=float(d["omega"]),
        S=float(d["S"]),
        C=float(d["C"]),
        tau_R=float(d["tau_R"]),
        kappa=float(d["kappa"]),
        I=float(d["I"]),
    )


def kernel_cmd(args: argparse.Namespace) -> int:
    import csv

    contract = FrozenContract.canon_default()

    psi: List[List[float]] = []
    with open(args.csv, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            psi.append([float(x) for x in row])

    w = [float(x) for x in args.weights.split(",")] if args.weights else None
    rows = compute_tier1_series(
        psi,
        contract=contract,
        weights=w,
        dt=float(args.dt),
        h_rec=float(args.hrec),
        eta=float(args.eta),
    )
    out = [r.__dict__ for r in rows]  # dataclasses with slots don't have __dict__, but Tier1Row does; keep safe
    # safer:
    out = [dict(
        t=r.t, psi=list(r.psi), weights=list(r.weights), dt=r.dt, h_rec=r.h_rec, eta=r.eta,
        F=r.F, omega=r.omega, S=r.S, C=r.C, tau_R=r.tau_R, kappa=r.kappa, I=r.I
    ) for r in rows]
    print(json.dumps(out, indent=2))
    return 0


def weld_cmd(args: argparse.Namespace) -> int:
    contract = FrozenContract.canon_default()

    pre = _row_from_json(_read_json(args.pre))
    post = _row_from_json(_read_json(args.post))

    gamma = GammaOmegaPower(p=contract.p)
    res = evaluate_weld(
        pre=pre,
        post=post,
        tau_r=float(args.tauR),
        gamma=gamma,
        alpha=contract.alpha,
        tol_seam=contract.tol_seam,
        tol_id=contract.tol_id,
        infer_R=bool(args.infer_R),
        R=float(args.R) if args.R is not None else None,
        theta=args.theta,
        weld_id=args.weld_id,
        pre_id=args.pre_id,
        post_id=args.post_id,
    )
    print(json.dumps(res.ss1m.to_dict(), indent=2))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="umcp", description="UMCP canon kernel + weld CLI")
    sp = p.add_subparsers(dest="cmd", required=True)

    pk = sp.add_parser("kernel", help="Compute Tier-1 rows from a CSV of admitted Ψ(t)")
    pk.add_argument("--csv", required=True, help="CSV file where each row is a Ψ(t) vector in [0,1]")
    pk.add_argument("--dt", required=True, type=float, help="Cadence (seconds)")
    pk.add_argument("--hrec", required=True, type=float, help="Return horizon Hrec (seconds)")
    pk.add_argument("--eta", required=True, type=float, help="Return threshold η")
    pk.add_argument("--weights", default=None, help="Comma-separated weights w_i (defaults uniform)")
    pk.set_defaults(func=kernel_cmd)

    pw = sp.add_parser("weld", help="Evaluate a weld row from PRE/POST Tier-1 JSON rows")
    pw.add_argument("--pre", required=True, help="JSON file containing a Tier1Row dict (PRE)")
    pw.add_argument("--post", required=True, help="JSON file containing a Tier1Row dict (POST)")
    pw.add_argument("--tauR", required=True, type=float, help="Observed/declared τR for the seam")
    pw.add_argument("--R", default=None, help="Return credit rate R (optional if --infer-R)")
    pw.add_argument("--infer-R", action="store_true", dest="infer_R", help="Infer R from the ledger")
    pw.add_argument("--theta", default="θ", help="θ label for the receipt (e.g., PHYS-04)")
    pw.add_argument("--weld-id", default=FrozenContract.canon_default().weld_id, dest="weld_id")
    pw.add_argument("--pre-id", default=FrozenContract.canon_default().pre_doi, dest="pre_id")
    pw.add_argument("--post-id", default=FrozenContract.canon_default().post_doi, dest="post_id")
    pw.set_defaults(func=weld_cmd)

    args = p.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
