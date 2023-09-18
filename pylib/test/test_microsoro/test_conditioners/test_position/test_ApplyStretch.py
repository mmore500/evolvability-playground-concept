import copy
import typing

import numpy as np
import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplyRotate, ApplyStretch


@pytest.fixture
def basic_state():
    return State(height=3, width=3)


@pytest.mark.parametrize("how", ["sym", "pos", "neg"])
def test_null_stretch(how: str):
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplyStretch(how=how, mx=1.0, my=1.0)
    res = ftor(state)
    assert res is None

    assert State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)


@pytest.mark.parametrize("how", ["sym", "pos", "neg"])
@pytest.mark.parametrize("conditioner", [ApplyRotate(), lambda x: x])
def test_inverse_stretces(how: str, conditioner: typing.Callable):
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplyStretch(how="sym", mx=2.0, my=3.0)
    res = ftor(state)
    assert res is None

    assert not State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)

    ftor = ApplyStretch(how="sym", mx=1 / 2.0, my=1 / 3.0)
    res = ftor(state)
    assert res is None

    assert State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)


def test_symmetric_stretch(basic_state):
    ftor = ApplyStretch(how="sym", mx=2.0, my=3.0)
    res = ftor(basic_state)
    assert res is None

    assert np.array_equal(
        basic_state.px,
        [
            [-1, 1, 3],
            [-1, 1, 3],
            [-1, 1, 3],
        ],
    )
    assert np.array_equal(
        basic_state.py,
        [
            [-2, -2, -2],
            [1, 1, 1],
            [4, 4, 4],
        ],
    )


def test_negative_stretch(basic_state):
    ftor = ApplyStretch(how="neg", mx=2.0, my=3.0)
    res = ftor(basic_state)
    assert res is None

    assert np.array_equal(
        basic_state.px,
        [
            [-2, 0, 2],
            [-2, 0, 2],
            [-2, 0, 2],
        ],
    )
    assert np.array_equal(
        basic_state.py,
        [
            [-4, -4, -4],
            [-1, -1, -1],
            [2, 2, 2],
        ],
    )


def test_positive_stretch(basic_state):
    ftor = ApplyStretch(how="pos", mx=2.0, my=3.0)
    res = ftor(basic_state)
    assert res is None

    assert np.array_equal(
        basic_state.px,
        [
            [0, 2, 4],
            [0, 2, 4],
            [0, 2, 4],
        ],
    )
    assert np.array_equal(
        basic_state.py,
        [
            [0, 0, 0],
            [3, 3, 3],
            [6, 6, 6],
        ],
    )


def test_invalid_config():
    # Expect a ValueError for invalid configuration
    with pytest.raises(ValueError):
        stretch = ApplyStretch(how="invalid")
        res = stretch(State())
        assert res is None
