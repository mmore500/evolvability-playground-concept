import copy
import typing

import numpy as np
import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplyRotate, ApplyTorsion


@pytest.fixture
def basic_state():
    return State(height=3, width=3)


def test_null_torsion():
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplyTorsion(phi_degrees=0.0)
    res = ftor(state)
    assert res is None

    assert State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)

    ftor = ApplyTorsion(phi_degrees=360.0)
    res = ftor(state)
    assert res is None

    assert not State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)


@pytest.mark.parametrize("conditioner", [ApplyRotate(), lambda x: x])
def test_inverse_torsions(conditioner: typing.Callable):
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplyTorsion(phi_degrees=42.0)
    res = ftor(state)
    assert res is None

    assert not State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)

    ftor = ApplyTorsion(phi_degrees=-42.0)
    res = ftor(state)
    assert res is None

    assert State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)


@pytest.mark.parametrize(
    "phi_degrees", [1.0, -8.0, 15.0, 30.0, 42.0, 78.0, 360.0, -380.0]
)
def test_torsion_invariants(phi_degrees: float):
    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplyTorsion(phi_degrees)
    res = ftor(state)
    assert res is None

    assert not np.allclose(state.px.flatten(), prestate.px.flatten())
    assert not np.allclose(state.py.flatten(), prestate.py.flatten())

    cx: float = (prestate.px.max() + prestate.py.min()) / 2
    cy: float = (prestate.py.max() + prestate.py.min()) / 2
    ds_pre = (prestate.px - cx) ** 2 + (prestate.py - cy) ** 2
    ds_post = (state.px - cx) ** 2 + (state.py - cy) ** 2
    assert np.allclose(ds_pre, ds_post)


def test_torsion_clockwise():

    state = State()
    prestate = copy.deepcopy(state)

    ftor = ApplyTorsion(phi_degrees=8.0)
    res = ftor(state)
    assert res is None

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
