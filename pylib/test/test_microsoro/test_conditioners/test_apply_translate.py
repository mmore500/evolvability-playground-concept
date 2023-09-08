import copy

import numpy as np
import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import apply_translate


def test_pairwise_distance_null():
    state = State(height=8, width=10)
    state_ = copy.deepcopy(state)
    apply_translate(state)
    assert (state.px == state_.px).all() and (state.py == state_.py).all()


@pytest.mark.parametrize("dx", range(-10, 10))
@pytest.mark.parametrize("dy", range(-10, 10))
def test_pairwise_distance_dxdy(dx: int, dy: int):
    state = State(height=8, width=10)
    state_ = copy.deepcopy(state)
    apply_translate(state, dx=dx, dy=dy),
    assert (state.px == state_.px + dx).all()
    assert (state.py == state_.py + dy).all()
