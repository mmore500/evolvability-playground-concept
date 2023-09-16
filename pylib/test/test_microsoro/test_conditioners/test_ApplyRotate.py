import copy

import numpy as np
import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplyRotate


@pytest.mark.parametrize(
    "rotate_angle", [-180, -90, -45, 33, 45, 90, 180, 360]
)
def test_wraparound(rotate_angle: int):
    state = State(height=8, width=10)
    state_ = copy.deepcopy(state)

    cur_angle = 0
    for __ in range(20):
        ApplyRotate(rotate_angle)(state)
        cur_angle += rotate_angle
        cur_angle %= 360
        for mata, matb in [(state.px, state_.px), (state.py, state_.py)]:
            assert bool(cur_angle) == (not np.allclose(mata, matb))


def test_pairwise_distance():
    state = State(height=8, width=10)

    distances = []
    for i in range(20):
        ApplyRotate(theta_degrees=i)(state)
        pxa, *__, pxb = state.px.flat
        pya, *__, pyb = state.py.flat

        distance = (pxa - pxb) ** 2 + (pya - pyb) ** 2
        distances.append(distance)

    assert np.allclose(distances[:-1], distances[1:])


def test_clockwise():
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplyRotate(theta_degrees=30.0)
    res = ftor(state)
    assert res is None

    assert not State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)

    dx = state.px - prestate.px
    assert dx[0, 0] < 0
    assert dx[-1, 0] > 0
    assert dx[-1, -1] > 0
    assert dx[0, -1] < 0

    dy = state.py - prestate.py
    assert dy[0, 0] > 0
    assert dy[-1, 0] > 0
    assert dy[-1, -1] < 0
    assert dy[0, -1] < 0


def test_counterclockwise():
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplyRotate(theta_degrees=-30.0)
    res = ftor(state)
    assert res is None

    assert not State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)

    dx = state.px - prestate.px
    assert dx[0, 0] > 0
    assert dx[-1, 0] < 0
    assert dx[-1, -1] < 0
    assert dx[0, -1] > 0

    dy = state.py - prestate.py
    assert dy[0, 0] < 0
    assert dy[-1, 0] < 0
    assert dy[-1, -1] > 0
    assert dy[0, -1] > 0
