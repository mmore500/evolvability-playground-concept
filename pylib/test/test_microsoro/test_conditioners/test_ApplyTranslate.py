import copy

import numpy as np
import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplyTranslate


def test_pairwise_distance_null():
    state = State(height=8, width=10)
    state_ = copy.deepcopy(state)
    ApplyTranslate()(state)
    assert State.same_position_as(state, state_)


@pytest.mark.parametrize("dx", range(-10, 10))
@pytest.mark.parametrize("dy", range(-10, 10))
def test_pairwise_distance_dxdy(dx: int, dy: int):
    state = State(height=8, width=10)
    state_ = copy.deepcopy(state)
    ApplyTranslate(dx=dx, dy=dy)(state)
    assert np.array_equal(state.px, state_.px + dx)
    assert np.array_equal(state.py, state_.py + dy)
