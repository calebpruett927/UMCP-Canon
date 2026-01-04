from umcp.eid import EIDCounts, delta_kappa_eid, eid_checksum, prime_pi


def test_prime_pi_small_values():
    assert prime_pi(1) == 0
    assert prime_pi(2) == 1
    assert prime_pi(3) == 2
    assert prime_pi(10) == 4
    assert prime_pi(100) == 25


def test_eid_checksum_shape():
    c = EIDCounts(P=34, Eq=52, Fig=3, Tab=6, List=4, Box=9, Ref=12)
    chk = eid_checksum(c)
    assert len(chk.chk) == 3
    assert all(isinstance(x, int) and x >= 0 for x in chk.chk)


def test_delta_kappa_eid_positive_when_mass_increases():
    a = EIDCounts(P=10, Eq=10, Fig=1, Tab=1, List=0, Box=0, Ref=0)
    b = EIDCounts(P=11, Eq=10, Fig=1, Tab=1, List=0, Box=0, Ref=0)
    assert delta_kappa_eid(a, b) > 0
