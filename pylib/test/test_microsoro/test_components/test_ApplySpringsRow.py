import typing

from hstrat import _auxiliary_lib as hstrat_aux
import numpy as np
import pytest

from pylib.auxlib import all_rows_equivalent
from pylib.microsoro import State, Params
from pylib.microsoro.components import ApplySpringsRow
from pylib.microsoro.conditioners import (
    ApplyRotate,
    ApplyStretch,
    ApplyTorsion,
    ApplyTranslate,
)


def test_no_stretch_no_v():

    state = State()

    ftor = ApplySpringsRow()
    res = ftor(state)
    assert res is None

    assert np.allclose(state.vy, 0.0)
    assert np.allclose(state.vx, 0.0)

    ApplyRotate(9.0)(state)
    assert np.allclose(state.vy, 0.0)
    assert np.allclose(state.vx, 0.0)


@pytest.mark.parametrize(
    "rotate_degrees", [-10.0, 0.0, 30.0, 42.0, 45.0, 90.0, 91.0]
)
def test_py_stretched_no_v(rotate_degrees: float):
    state = State()
    ApplyStretch(my=2.0)(state)
    ApplyRotate(theta_degrees=rotate_degrees)(state)

    ftor = ApplySpringsRow()
    res = ftor(state)
    assert res is None

    assert np.allclose(state.vy, 0.0)
    assert np.allclose(state.vx, 0.0)


def test_px_stretched_mixed_vx():
    state = State()
    ApplyStretch(mx=2.0)(state)

    ftor = ApplySpringsRow()
    res = ftor(state)
    assert res is None

    assert not np.all(state.vx == 0)
    assert np.all(state.vy == 0)

    assert all_rows_equivalent(state.vx)
    assert np.all(
        state.vx[
            :,
            0,
        ]
        > 0
    )
    assert np.all(state.vx[:, -1] < 0)


def test_diagonal_stretched_mixed_v():
    state = State()
    ApplyRotate(theta_degrees=-45.0)(state)
    ApplyStretch(mx=2.0, my=2.0)(state)

    ftor = ApplySpringsRow()
    res = ftor(state)
    assert res is None

    assert not np.allclose(state.vx, 0.0)
    assert not np.allclose(state.vy, 0.0)
    assert np.allclose(state.vx, state.vy)
    assert np.any(state.vx < 0) and np.any(state.vx > 0)
    assert np.any(state.vy < 0) and np.any(state.vy > 0)


@pytest.mark.parametrize(
    "conditioner",
    [
        ApplyStretch(mx=1.5, my=2.0),
        ApplyTorsion(),
    ],
)
def test_py_stretched_rotation_invariants(
    conditioner: typing.Callable,
):
    sum_speeds = []
    for rotate_degrees in range(360):
        state = State()
        conditioner(state)
        ApplyRotate(rotate_degrees)(state)
        ApplyTranslate(rotate_degrees, -rotate_degrees)(state)
        res = ApplySpringsRow()(state)
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


def test_stretch_scaling():
    sum_speeds = []
    for stretch_factor in range(1, 10):
        state = State()
        ApplyStretch(mx=stretch_factor)(state)
        res = ApplySpringsRow()(state)
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
def test_param_k(conditioner: typing.Callable):
    sum_speeds = []
    for k in range(10):
        state = State()
        conditioner(state)
        params = Params()
        params.k = k
        res = ApplySpringsRow(params=params)(state)
        assert res is None

        speeds = np.sqrt(state.vx**2 + state.vy**2)
        sum_speeds.append(np.sum(speeds))

    # shouldn't all be equivalent
    assert not np.allclose(sum_speeds, sum_speeds[0])

    assert sum_speeds[0] == 0.0

    # should be in increasing order as k is added
    assert hstrat_aux.is_strictly_increasing(sum_speeds)
