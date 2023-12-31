import copy
import typing

from hstrat import _auxiliary_lib as hstrat_aux
import numpy as np
import pytest

from pylib.auxlib import all_rows_equivalent
from pylib.microsoro import State, Structure, Params
from pylib.microsoro.components import ApplySpringDampingRow
from pylib.microsoro.conditioners import (
    ApplyDeflect,
    ApplyPropel,
    ApplyRotate,
    ApplyStretch,
    ApplyTorsion,
    ApplyTranslate,
)
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


def test_no_v_no_v(event_buffer: typing.Optional[EventBuffer]):

    state = State()

    ftor = ApplySpringDampingRow()
    res = ftor(state, event_buffer)
    assert res is None

    assert np.allclose(state.vy, 0.0)
    assert np.allclose(state.vx, 0.0)


def test_no_differential_no_v(event_buffer: typing.Optional[EventBuffer]):

    state = State()
    ApplyPropel(dvx=1.0, dvy=1.0)(state)

    ftor = ApplySpringDampingRow()
    res = ftor(state, event_buffer)
    assert res is None

    assert np.allclose(state.vy, 1.0)
    assert np.allclose(state.vx, 1.0)


@pytest.mark.parametrize("differential_factor", [0.5, 2.0])
def test_vy_differentialed_no_v(
    event_buffer: typing.Optional[EventBuffer],
    differential_factor: float,
):
    state = State()
    ApplyStretch(mx=differential_factor)(state)
    state.vy = state.py
    prestate = copy.deepcopy(state)

    ftor = ApplySpringDampingRow()
    res = ftor(state, event_buffer)
    assert res is None

    assert np.allclose(state.vx, prestate.vx)
    assert np.allclose(state.vy, prestate.vy)


def test_vx_differentialed_mixed_vx(
    event_buffer: typing.Optional[EventBuffer],
):
    state = State()
    state.vx = state.px
    prestate = copy.deepcopy(state)

    ftor = ApplySpringDampingRow()
    res = ftor(state, event_buffer)
    assert res is None

    assert all_rows_equivalent(state.vx)
    assert not np.all(state.vx == prestate.vx)
    assert np.all(state.vx[:, 0] > prestate.vx[:, 0])
    assert np.all(state.vx[:, -1] < prestate.vx[:, -1])
    assert np.all(state.vy == prestate.vy)


@pytest.mark.parametrize(
    "conditioner",
    [
        ApplyStretch(mx=1.5, my=2.0),
        ApplyTorsion(),
    ],
)
def test_py_differentialed_rotation_invariants(
    conditioner: typing.Callable,
    event_buffer: typing.Optional[EventBuffer],
):
    sum_speeds = []
    for rotate_degrees in range(360):
        state = State()
        conditioner(state)
        state.vx = state.px
        state.vy = state.py
        ApplyRotate(rotate_degrees)(state)
        ApplyDeflect(rotate_degrees)(state)
        ApplyTranslate(rotate_degrees, -rotate_degrees)(state)
        res = ApplySpringDampingRow()(state, event_buffer)
        assert res is None

        # ensure springs having effect
        assert not (np.allclose(state.vx, 0.0) and np.allclose(state.vy, 0.0))

        speeds = np.sqrt(state.vx**2 + state.vy**2)
        sum_speeds.append(np.sum(speeds))

    # should all be equivalent, no matter what way rotated
    assert np.allclose(sum_speeds, sum_speeds[0])


def test_differential_scaling(event_buffer: typing.Optional[EventBuffer]):
    sum_speeds = []
    for differential_factor in range(1, 10):
        state = State()
        ApplyStretch(my=differential_factor)(state)
        state.vx = state.px
        state.vy = state.py
        res = ApplySpringDampingRow()(state, event_buffer)
        assert res is None
        speeds = np.sqrt(state.vx**2 + state.vy**2)
        sum_speeds.append(np.sum(speeds))

    # shouldn't all be equivalent or near equivalent
    assert not np.allclose(sum_speeds, sum_speeds[0])

    # should be in increasing order as differential is added
    assert hstrat_aux.is_strictly_increasing(sum_speeds)


@pytest.mark.parametrize(
    "conditioner",
    [
        ApplyStretch(mx=1.5, my=2.0),
        ApplyTorsion(),
    ],
)
def test_param_b(
    conditioner: typing.Callable,
    event_buffer: typing.Optional[EventBuffer],
):
    sum_speeds = []
    for b in range(10):
        state = State()
        conditioner(state)
        state.vx = state.px
        state.vy = state.py
        params = Params()
        params.b = b
        res = ApplySpringDampingRow(params=params)(state, event_buffer)
        assert res is None

        speeds = np.sqrt(state.vx**2 + state.vy**2)
        sum_speeds.append(np.sum(speeds))

    # shouldn't all be equivalent
    assert not np.allclose(sum_speeds, sum_speeds[0])

    # should be in increasing order as b is added
    assert hstrat_aux.is_strictly_decreasing(sum_speeds)


@pytest.mark.parametrize(
    "conditioner",
    [
        ApplyStretch(mx=1.5, my=2.0),
        ApplyTorsion(),
    ],
)
def test_param_Structure(
    conditioner: typing.Callable,
    event_buffer: typing.Optional[EventBuffer],
):
    sum_speeds = []
    for b in range(10):
        state = State()
        conditioner(state)
        state.vx = state.px
        state.vy = state.py
        params = Params()
        params.b = b
        res = ApplySpringDampingRow(
            structure=Structure(params=params),
        )(state, event_buffer)
        assert res is None

        speeds = np.sqrt(state.vx**2 + state.vy**2)
        sum_speeds.append(np.sum(speeds))

    # shouldn't all be equivalent
    assert not np.allclose(sum_speeds, sum_speeds[0])

    # should be in increasing order as b is added
    assert hstrat_aux.is_strictly_decreasing(sum_speeds)
