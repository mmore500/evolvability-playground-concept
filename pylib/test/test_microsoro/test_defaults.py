from pylib.microsoro import defaults


def test_b():
    b1, b2 = defaults.b_lim
    assert b1 <= b2
    assert b1 <= defaults.b <= b2


def test_dt():
    assert defaults.dt > 0.0


def test_g():
    assert defaults.g >= 0.0


def test_k():
    k1, k2 = defaults.k_lim
    assert k1 <= k2
    assert k1 <= defaults.k <= k2


def test_l():
    l1, l2 = defaults.l_lim
    assert l1 <= l2
    assert l1 <= defaults.l <= l2


def test_m():
    m1, m2 = defaults.m_lim
    assert m1 <= m2
    assert m1 <= defaults.m <= m2


def test_ncol():
    ncol1, ncol2 = defaults.ncol_lim
    assert ncol1 <= ncol2
    assert ncol1 <= defaults.ncol <= ncol2


def test_nrow():
    nrow1, nrow2 = defaults.nrow_lim
    assert nrow1 <= nrow2
    assert nrow1 <= defaults.nrow <= nrow2
