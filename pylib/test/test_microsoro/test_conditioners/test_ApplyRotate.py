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
            assert (cur_angle == 0) == np.isclose(mata, matb).all()


def test_pairwise_distance():
    state = State(height=8, width=10)

    distances = []
    for i in range(20):
        ApplyRotate(angle_degrees=i)(state)
        pxa, *__, pxb = state.px.flat
        pya, *__, pyb = state.py.flat

        distance = (pxa - pxb) ** 2 + (pya - pyb) ** 2
        distances.append(distance)

    assert np.isclose(distances[:-1], distances[1:]).all()
