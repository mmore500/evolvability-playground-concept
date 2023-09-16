import random
import copy

import numpy as np
import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplySpin


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
    ApplySpin(omega=random.uniform(-10, 10))(state)
    assert (state.vx != 0).any() and (state.vy != 0).any()
    state.px += state.vx
    state.py += state.vy

    # after
    px_a, py_a = state.px.flat[idx_a], state.py.flat[idx_b]
    px_b, py_b = state.px.flat[idx_a], state.py.flat[idx_b]
    actual_dist = (px_a - px_b) ** 2 - (py_a - py_b) ** 2

    assert np.isclose(expected_dist, actual_dist)


def test_clockwise():
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplySpin(omega=1.0)
    res = ftor(state)
    assert res is None

    assert State.same_position_as(state, prestate)
    assert not State.same_velocity_as(state, prestate)

    assert state.vx[0, 0] < 0
    assert state.vx[-1, 0] > 0
    assert state.vx[-1, -1] > 0
    assert state.vx[0, -1] < 0

    assert state.vy[0, 0] > 0
    assert state.vy[-1, 0] > 0
    assert state.vy[-1, -1] < 0
    assert state.vy[0, -1] < 0


def test_counterclockwise():
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplySpin(omega=-1.0)
    res = ftor(state)
    assert res is None

    assert State.same_position_as(state, prestate)
    assert not State.same_velocity_as(state, prestate)

    assert state.vx[0, 0] > 0
    assert state.vx[-1, 0] < 0
    assert state.vx[-1, -1] < 0
    assert state.vx[0, -1] > 0

    assert state.vy[0, 0] < 0
    assert state.vy[-1, 0] < 0
    assert state.vy[-1, -1] > 0
    assert state.vy[0, -1] > 0
