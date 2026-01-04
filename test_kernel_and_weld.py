import math

from umcp.closures import GammaOmegaPower
from umcp.contract import FrozenContract
from umcp.kernel import compute_tier1_series
from umcp.weld import evaluate_weld


def test_identity_I_equals_exp_kappa():
    contract = FrozenContract.canon_default()
    psi = [[0.9, 0.8, 0.7, 0.6]]
    rows = compute_tier1_series(psi, contract=contract, dt=1.0, h_rec=10.0, eta=0.01)
    r = rows[0]
    assert math.isclose(r.I, math.exp(r.kappa), rel_tol=1e-12, abs_tol=1e-12)


def test_weld_passes_when_constructed_to_close_budget():
    contract = FrozenContract.canon_default()
    psi = [
        [0.98, 0.98, 0.98, 0.98],  # PRE
        [0.98, 0.98, 0.98, 0.98],  # allow a return
        [0.985, 0.985, 0.985, 0.985],  # POST
    ]
    rows = compute_tier1_series(
        psi,
        contract=contract,
        weights=[0.25, 0.25, 0.25, 0.25],
        dt=0.001,
        h_rec=2.0,
        eta=0.02,
    )
    pre, post = rows[0], rows[-1]
    gamma = GammaOmegaPower(p=contract.p)

    # Choose τR and infer R so s should be ~0.
    weld = evaluate_weld(
        pre=pre,
        post=post,
        tau_r=0.8,
        gamma=gamma,
        alpha=contract.alpha,
        tol_seam=contract.tol_seam,
        tol_id=contract.tol_id,
        infer_R=True,
        theta="TEST",
        weld_id=contract.weld_id,
        pre_id=contract.pre_doi,
        post_id=contract.post_doi,
    )
    assert weld.ss1m.return_ok
    assert weld.ss1m.identity_ok
    assert abs(weld.ss1m.s) <= contract.tol_seam
