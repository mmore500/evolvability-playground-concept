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


@pytest.mark.parametrize("height", range(1, 10))
@pytest.mark.parametrize("width", range(1, 10))
def test_ncells(height: int, width: int):
    state = State(height=height, width=width)
    assert state.ncells == height * width
