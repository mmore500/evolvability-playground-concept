import numpy as np
import pytest

from pylib.microsoro import State


def test_init():
    State()  # test default params
    state = State(height=8, width=10)

    assert isinstance(state.px, np.ndarray)
    assert state.px.shape == (8, 10)
    unraveled = np.ravel(state.px, order="F")
    assert (unraveled[:-1] <= unraveled[1:]).all()

    assert isinstance(state.py, np.ndarray)
    unraveled = np.ravel(state.py, order="C")
    assert state.py.shape == (8, 10)
    assert (unraveled[:-1] <= unraveled[1:]).all()

    assert isinstance(state.vx, np.ndarray)
    assert state.vx.shape == (8, 10)
    assert len({*state.vx.flat}) == 1

    assert isinstance(state.vy, np.ndarray)
    assert state.vy.shape == (8, 10)
    assert len({*state.vy.flat}) == 1

    assert isinstance(state.t, float)
    assert state.t == 0


@pytest.mark.parametrize("height", range(1, 10))
@pytest.mark.parametrize("width", range(1, 10))
def test_ncells(height: int, width: int):
    state = State(height=height, width=width)
    assert state.ncells == height * width


def test_same_position_as():
    # Create two state instances
    s1 = State()
    s2 = State()

    # Check if they have the same position
    assert s1.same_position_as(s2)
    assert State.same_position_as(s1, s2)

    # Modify the position of s2
    s2.px[0, 0] = 100

    # Now they should not have the same position
    assert not s1.same_position_as(s2)
    assert not State.same_position_as(s1, s2)


def test_same_velocity_as():
    # Create two state instances
    s1 = State()
    s2 = State()

    # Check if they have the same velocity
    assert s1.same_velocity_as(s2)
    assert State.same_velocity_as(s1, s2)

    # Modify the velocity of s2
    s2.vx[0, 0] = 1.0

    # Now they should not have the same velocity
    assert not s1.same_velocity_as(s2)
    assert not State.same_velocity_as(s1, s2)
