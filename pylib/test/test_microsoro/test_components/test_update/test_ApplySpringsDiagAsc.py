import typing

from hstrat import _auxiliary_lib as hstrat_aux
import numpy as np
import pytest

from pylib.auxlib import all_rows_equivalent
from pylib.microsoro import State, Structure, Params
from pylib.microsoro.components import ApplySpringsDiagAsc
from pylib.microsoro.conditioners import (
    ApplyRotate,
    ApplyStretch,
    ApplyTorsion,
    ApplyTranslate,
)
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


def test_no_stretch_no_v(event_buffer: typing.Optional[EventBuffer]):
    state = State()

    ftor = ApplySpringsDiagAsc()
    res = ftor(state, event_buffer)
    assert res is None

    assert np.allclose(state.vy, 0.0)
    assert np.allclose(state.vx, 0.0)

    ApplyRotate(9.0)(state)
    assert np.allclose(state.vy, 0.0)
    assert np.allclose(state.vx, 0.0)


@pytest.mark.parametrize(
    "rotate_degrees",
    [-10.0, 0.0, 30.0, 42.0, 45.0, 90.0, 91.0],
)
@pytest.mark.parametrize("stretch_factor", [0.5, 2.0])
def test_diagdesc_stretched_no_v(
    event_buffer: typing.Optional[EventBuffer],
    rotate_degrees: float,
    stretch_factor: float,
):
    state = State()
    ApplyRotate(theta_degrees=45.0)(state)
    ApplyStretch(my=stretch_factor)(state)
    ApplyRotate(theta_degrees=-45.0)(state)
    ApplyRotate(theta_degrees=rotate_degrees)(state)

    ftor = ApplySpringsDiagAsc()
    res = ftor(state, event_buffer)
    assert res is None

    assert np.allclose(state.vy, 0.0)
    assert np.allclose(state.vx, 0.0)


def test_diagasc_stretched_mixed_vx(
    event_buffer: typing.Optional[EventBuffer],
):
    state = State()
    ApplyRotate(theta_degrees=45.0)(state)
    ApplyStretch(mx=2.0)(state)

    ftor = ApplySpringsDiagAsc()
    res = ftor(state, event_buffer)
    assert res is None

    assert np.allclose(state.vy, 0.0)
    assert not np.all(state.vx == 0)

    assert state.vx[-1, -1] < 0.0
    assert state.vx[0, 0] > 0.0
    assert np.isclose(state.vx[0, -1], 0.0)
    assert np.isclose(state.vx[-1, 0], 0.0)


def test_diagasc_compressed_mixed_vx(
    event_buffer: typing.Optional[EventBuffer],
):
    state = State()
    ApplyRotate(theta_degrees=45.0)(state)
    ApplyStretch(mx=0.5)(state)

    ftor = ApplySpringsDiagAsc()
    res = ftor(state, event_buffer)
    assert res is None

    assert np.allclose(state.vy, 0.0)
    assert not np.all(state.vx == 0)

    assert state.vx[-1, -1] > 0.0
    assert state.vx[0, 0] < 0.0
    assert np.isclose(state.vx[0, -1], 0.0)
    assert np.isclose(state.vx[-1, 0], 0.0)


@pytest.mark.parametrize(
    "stretch_conditioner",
    [ApplyStretch(mx=2.0, my=2.0), ApplyStretch(my=2.0), ApplyStretch(mx=2.0)],
)
def test_stretched_mixed_v(
    event_buffer: typing.Optional[EventBuffer],
    stretch_conditioner: typing.Callable,
):
    state = State()
    stretch_conditioner(state)

    ftor = ApplySpringsDiagAsc()
    res = ftor(state, event_buffer)
    assert res is None

    assert not np.allclose(state.vx, 0.0)
    assert not np.allclose(state.vy, 0.0)
    if stretch_conditioner._mx == stretch_conditioner._my:
        assert np.allclose(state.vx, state.vy)
    assert np.any(state.vx < 0) and np.any(state.vx > 0)
    assert np.any(state.vy < 0) and np.any(state.vy > 0)


@pytest.mark.parametrize(
    "conditioner",
    [
        ApplyStretch(mx=1.5, my=2.0),
        ApplyStretch(my=2.0),
        ApplyTorsion(),
    ],
)
def test_stretched_rotation_invariants(
    conditioner: typing.Callable,
    event_buffer: typing.Optional[EventBuffer],
):
    sum_speeds = []
    for rotate_degrees in range(360):
        state = State()
        conditioner(state)
        ApplyRotate(rotate_degrees)(state)
        ApplyTranslate(rotate_degrees, -rotate_degrees)(state)
        res = ApplySpringsDiagAsc()(state, event_buffer)
        assert res is None

        # ensure springs having effect
        assert not (np.allclose(state.vx, 0.0) and np.allclose(state.vy, 0.0))

        # conservation of momentum -- sum velocities should cancel
        assert np.isclose(np.sum(state.vx.flat), 0.0)
        assert np.isclose(np.sum(state.vy.flat), 0.0)

        speeds = np.sqrt(state.vx**2 + state.vy**2)
        sum_speeds.append(np.sum(speeds))

    # should all be equivalent, no matter what way rotated
    assert np.allclose(sum_speeds, sum_speeds[0])


def test_stretch_scaling(event_buffer: typing.Optional[EventBuffer]):
    sum_speeds = []
    for stretch_factor in range(1, 10):
        state = State()
        ApplyStretch(mx=stretch_factor)(state)
        res = ApplySpringsDiagAsc()(state, event_buffer)
        assert res is None
        speeds = np.sqrt(state.vx**2 + state.vy**2)
        sum_speeds.append(np.sum(speeds))

    # shouldn't all be equivalent or near equivalent
    assert not np.allclose(sum_speeds, sum_speeds[0])

    # should be in increasing order as stretch is added
    assert hstrat_aux.is_strictly_increasing(sum_speeds)


@pytest.mark.parametrize(
    "conditioner",
    [
        ApplyStretch(mx=1.5, my=2.0),
        ApplyTorsion(),
    ],
)
def test_param_k(
    conditioner: typing.Callable,
    event_buffer: typing.Optional[EventBuffer],
):
    sum_speeds = []
    for k in range(10):
        state = State()
        conditioner(state)
        params = Params()
        params.k = k
        params.k_lim = (0, 11)
        res = ApplySpringsDiagAsc(
            structure=Structure(params=params),
        )(state, event_buffer)
        assert res is None

        speeds = np.sqrt(state.vx**2 + state.vy**2)
        sum_speeds.append(np.sum(speeds))

    # shouldn't all be equivalent
    assert not np.allclose(sum_speeds, sum_speeds[0])

    assert sum_speeds[0] == 0.0

    # should be in increasing order as k is added
    assert hstrat_aux.is_strictly_increasing(sum_speeds)
