import copy

import numpy as np

from pylib.microsoro import Params, State
from pylib.microsoro.components import ApplyGravity


def test_ApplyGravity():
    state = State()
    params = Params()
    state_ = copy.deepcopy(state)

    res = ApplyGravity(params)(state)
    assert res is None
    assert State.same_position_as(state, state_)
    assert np.allclose(state.vx, state_.vx)
    assert np.allclose(state.vy, state_.vy - params.dt * params.g)


def test_ApplyGravity_default_ctor():
    assert ApplyGravity()._params == Params()
