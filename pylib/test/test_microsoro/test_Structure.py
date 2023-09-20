import numpy as np
import pytest

from pylib.microsoro import defaults, Structure, Params


def test_structure_init_default():
    # Given default values
    s = Structure()

    # Assert default height and width are set
    assert s.height == defaults.nrow
    assert s.width == defaults.ncol


def test_structure_init_with_values():
    # Given specific values
    s = Structure(height=10, width=15)

    # Assert the height and width are set correctly
    assert s.height == 10
    assert s.width == 15


def test_structure_init_invalid_values():
    # Given invalid values, the instantiation should raise a ValueError
    with pytest.raises(ValueError):
        Structure(height=defaults.nrow_lim[0] - 1)

    with pytest.raises(ValueError):
        Structure(width=defaults.ncol_lim[0] - 1)


def test_structure_properties():
    # Given a structure instance
    s = Structure(height=10, width=15)

    # The properties should return the correct values
    assert s.height == 10
    assert s.width == 15


def test_make_random_default():
    # The static method should return an instance of Structure with default
    # values
    s = Structure.make_random()
    assert isinstance(s, Structure)
    assert s.height == defaults.nrow
    assert s.width == defaults.ncol


def test_make_random_with_values():
    # Given specific values, the static method should return a structure
    # instance with those values
    s = Structure.make_random(height=10, width=15)
    assert isinstance(s, Structure)
    assert s.height == 10
    assert s.width == 15


def test_make_random_invalid_values():
    # Given invalid values, the method should raise a ValueError
    with pytest.raises(ValueError):
        Structure.make_random(height=defaults.nrow_lim[0] - 1)

    with pytest.raises(ValueError):
        Structure.make_random(width=defaults.ncol_lim[0] - 1)


def test_structure_with_params():
    params = Params(
        b=42.0,
        k=defaults.k_lim[0] + 24.0,
        l=0.42,
        m=2.4,
    )
    structure = Structure(params=params)

    # Check if the default values are set correctly based on params
    assert np.all(structure.bc == params.b)
    assert np.all(structure.br == params.b)
    assert np.all(structure.ba == params.b)
    assert np.all(structure.bd == params.b)

    assert np.all(structure.kc == params.k)
    assert np.all(structure.kr == params.k)
    assert np.all(structure.ka == params.k)
    assert np.all(structure.kd == params.k)

    assert np.all(structure.lc == params.l)
    assert np.all(structure.lr == params.l)
    assert np.all(structure.la == params.l_diag)
    assert np.all(structure.ld == params.l_diag)

    assert np.all(structure.m == params.m)


def test_structure_with_b():
    b = np.full((defaults.nrow, defaults.ncol), 0.5)
    params = Params()
    params.b_lim = (42.0, 88.0)
    structure = Structure(b=b, params=params)

    # Check if b was correctly set
    assert np.all(structure.bc == np.mean(params.b_lim))
    assert np.all(structure.br == np.mean(params.b_lim))
    assert np.all(structure.ba == np.mean(params.b_lim))
    assert np.all(structure.bd == np.mean(params.b_lim))


def test_structure_with_k():
    k = np.full((defaults.nrow, defaults.ncol), 0.5)
    params = Params()
    params.k_lim = (42.0, 88.0)
    structure = Structure(k=k, params=params)

    # Check if k was correctly set
    assert np.all(structure.kc == np.mean(params.k_lim))
    assert np.all(structure.kr == np.mean(params.k_lim))
    assert np.all(structure.ka == np.mean(params.k_lim))
    assert np.all(structure.kd == np.mean(params.k_lim))


def test_structure_with_l():
    l = np.full((defaults.nrow, defaults.ncol), 0.5)
    params = Params()
    params.l_lim = (42.0, 88.0)
    structure = Structure(l=l, params=params)

    # Check if l was correctly set
    assert np.all(structure.lc == np.mean(params.l_lim))
    assert np.all(structure.lr == np.mean(params.l_lim))
    assert np.all(structure.la == np.mean(params.l_lim))
    assert np.all(structure.ld == np.mean(params.l_lim))


def test_structure_with_m():
    m = np.full((defaults.nrow, defaults.ncol), 0.5)
    params = Params()
    params.m_lim = (42.0, 88.0)
    structure = Structure(m=m, params=params)

    # Check if m was correctly set
    assert np.all(structure.m == np.mean(params.m_lim))
