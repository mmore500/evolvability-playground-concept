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


@pytest.mark.parametrize("dpx", range(-10, 10))
@pytest.mark.parametrize("dpy", range(-10, 10))
def test_pairwise_distance_dxdpy(dpx: int, dpy: int):
    state = State(height=8, width=10)
    state_ = copy.deepcopy(state)
    ApplyTranslate(dpx=dpx, dpy=dpy)(state)
    assert np.array_equal(state.px, state_.px + dpx)
    assert np.array_equal(state.py, state_.py + dpy)
