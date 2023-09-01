from pylib.microsoro import Params


def test_init():
    params = Params()
    assert params.dt > 0
    assert params.g > 0
    assert params.k > 0
    assert params.m > 0
