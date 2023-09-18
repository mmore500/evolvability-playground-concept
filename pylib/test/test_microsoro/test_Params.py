import copy

import pytest

from pylib.microsoro import Params


def test_init():
    params = Params()
    assert params.dt > 0
    assert params.g > 0
    assert params.k > 0
    assert params.m > 0


def test_bad_init():
    with pytest.raises(ValueError):
        Params(dt=0)

    with pytest.raises(ValueError):
        Params(g=-1.0)

    with pytest.raises(ValueError):
        Params(k=-1.0)

    with pytest.raises(ValueError):
        Params(m=-1.0)

    with pytest.raises(ValueError):
        Params(b=-1.0)


def test_eq():
    assert Params() == Params()
    params = Params()
    assert params == Params()

    params.g *= 2.0
    assert params == params
    assert params == copy.copy(params)
    assert not params == Params()

    params_ = copy.deepcopy(params)
    params.k += 0.7
    assert params == params
    assert params == copy.copy(params)
    assert params == copy.deepcopy(params)
    assert not params == Params()
    assert not params == params_

    assert not Params() == None
    assert not Params() == 0
    assert not Params() == "0"
    assert not Params() == ""
    assert not Params() == [""]
