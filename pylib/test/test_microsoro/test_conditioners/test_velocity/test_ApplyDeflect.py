import pytest
import numpy as np

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplyDeflect


def test_zero_velocities_remain_zero():
    state = State()
    ftor = ApplyDeflect()
    res = ftor(state)
    assert res is None
    assert np.all(state.vx == 0.0)
    assert np.all(state.vy == 0.0)


def test_single_cell():
    state = State()
    state.vx[0, 0] = 1.0
    state.vy[0, 0] = 0.0
    # 90 degrees should rotate clockwise to a vy of -1.0 and vx of 0.0
    ftor = ApplyDeflect(90)
    res = ftor(state)
    assert res is None
    assert np.isclose(state.vx[0, 0], 0.0)
    assert np.isclose(state.vy[0, 0], -1.0)
    assert np.allclose(state.vx[1:, 1:], 0.0)
    assert np.allclose(state.vy[1:, 1:], 0.0)


def test_all_cells():
    state = State()
    state.vx.fill(1.0)
    state.vy.fill(0.0)
    # 90 degrees should rotate clockwise to a vy of 0.0 and vx of -1.0
    ftor = ApplyDeflect(180)
    res = ftor(state)
    assert res is None
    assert np.allclose(state.vx, -1.0)
    assert np.allclose(state.vy, 0.0)


# def test_magnitude_of_velocity_maintained():
#     initial_vx = np.random.rand()
#     initial_vy = np.random.rand()
#     state = State(initial_vx, initial_vy)
#     ftor = ApplyDeflect(45)  # or any other angle
#     res = ftor(state)
#     assert res is None
#
#     initial_magnitude = np.sqrt(initial_vx**2 + initial_vy**2)
#     final_magnitude = np.sqrt(state.vx**2 + state.vy**2)
#
#     assert np.isclose(initial_magnitude, final_magnitude, atol=1e-8)
