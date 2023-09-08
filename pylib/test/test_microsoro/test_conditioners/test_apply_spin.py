import random
import copy

import numpy as np
import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import apply_spin


@pytest.mark.parametrize("random_seed", range(1, 40))
def test_pairwise_distance(random_seed: int):
    state = State(height=8, width=10)
    random.seed(random_seed)
    idx_a = random.choice(range(state.ncells))
    idx_b = random.choice(range(state.ncells))

    # before
    px_a, py_a = state.px.flat[idx_a], state.py.flat[idx_b]
    px_b, py_b = state.px.flat[idx_a], state.py.flat[idx_b]
    expected_dist = (px_a - px_b) ** 2 - (py_a - py_b) ** 2

    # calculate spin velocities and apply them
    apply_spin(state, random.uniform(-10, 10))
    assert (state.vx != 0).any() and (state.vy != 0).any()
    state.px += state.vx
    state.py += state.vy

    # after
    px_a, py_a = state.px.flat[idx_a], state.py.flat[idx_b]
    px_b, py_b = state.px.flat[idx_a], state.py.flat[idx_b]
    actual_dist = (px_a - px_b) ** 2 - (py_a - py_b) ** 2

    assert np.isclose(expected_dist, actual_dist)
