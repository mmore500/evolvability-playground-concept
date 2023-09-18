import copy

import numpy as np
import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplyPropel


def test_pairwise_distance_null():
    state = State(height=8, width=10)
    state_ = copy.deepcopy(state)
    ApplyPropel()(state)
    assert State.same_position_as(state, state_)
    assert State.same_velocity_as(state, state_)


@pytest.mark.parametrize("dvx", range(-10, 10))
@pytest.mark.parametrize("dvy", range(-10, 10))
def test_pairwise_distance_dvxdvy(dvx: int, dvy: int):
    state = State(height=8, width=10)
    state_ = copy.deepcopy(state)
    ApplyPropel(dvx=dvx, dvy=dvy)(state)
    assert np.array_equal(state.vx, state_.vx + dvx)
    assert np.array_equal(state.vy, state_.vy + dvy)
    assert State.same_position_as(state, state_)
