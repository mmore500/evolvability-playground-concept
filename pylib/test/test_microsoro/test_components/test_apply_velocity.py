import copy

import numpy as np
import pytest

from pylib.microsoro import Params, State
from pylib.microsoro.components import apply_velocity


@pytest.mark.parametrize("vx", [-1, 0, 1])
@pytest.mark.parametrize("vy", [-1, 0, 1])
def test_update(vx: int, vy: int):
    state_ = State()
    state_.vx, state_.vy = vx, vy
    state1 = copy.deepcopy(state_)
    state2 = copy.deepcopy(state_)
    params1 = Params(dt=1.0)
    params2 = Params(dt=0.1)

    apply_velocity(state1, params1)
    apply_velocity(state2, params2)

    assert (np.sign(state1.px - state_.px) == np.sign(vx)).all()
    assert (np.sign(state1.py - state_.py) == np.sign(vy)).all()
    assert (np.sign(state2.px - state_.px) == np.sign(vx)).all()
    assert (np.sign(state2.py - state_.py) == np.sign(vy)).all()

    if vx:
        assert (abs(state2.px - state_.px) < abs(state1.px - state_.px)).all()
    if vy:
        assert (abs(state2.py - state_.py) < abs(state1.py - state_.py)).all()
