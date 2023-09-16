import copy

import pytest
import numpy as np

from pylib.microsoro import conditioners, State
from pylib.microsoro.components import ApplyFloorBounce


def test_init():
    ApplyFloorBounce()

    with pytest.raises(ValueError):
        ApplyFloorBounce(e=-0.5)

    kwargs = dict(e=0.9, m=0.42, b=-42.0)
    ftor = ApplyFloorBounce(**kwargs)
    assert ftor._elasticity == kwargs["e"]
    assert ftor._slope == kwargs["m"]
    assert ftor._intercept == kwargs["b"]


def test_no_cells_below_floor():
    ftor = ApplyFloorBounce()
    state = State()

    conditioners.ApplyTranslate(dpy=100.0)(state)
    conditioners.ApplyPropel(dvy=-1.0)(state)
    prestate = copy.deepcopy(state)

    res = ftor(state)
    assert res is None
    assert State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)


@pytest.mark.parametrize("elasticity", [0.5, 1.0, 1.5])
def test_some_cells_below_flat_floor(elasticity: float):
    state = State()
    conditioners.ApplyTranslate(dpy=-state.py.min() - 1e-7)(state)
    conditioners.ApplyPropel(dvy=-1.0)(state)
    prestate = copy.deepcopy(state)

    ftor = ApplyFloorBounce(e=elasticity)
    res = ftor(state)
    assert res is None

    assert np.all(state.py[0, :] >= 0.0)
    assert np.all(state.py[1:, :] == prestate.py[1:, :])
    assert np.all(state.px == prestate.px)

    assert np.allclose(state.vy[0, :], elasticity)
    assert np.all(state.vy[1:, :] == prestate.vy[1:, :])
    assert np.all(state.vx == prestate.vx)


@pytest.mark.parametrize("elasticity", [0.5, 1.0, 1.5])
def test_some_cells_below_sloped_floor1(elasticity: float):
    state = State()
    conditioners.ApplyTranslate(  # move lower left cell below floor
        dpx=-state.vx.min() - 1e-7, dpy=-state.vy.min() - 1e-7
    )(state)
    state.vx.fill(0.0)  # no horizontal velocity
    state.vy.fill(-1.0)  # downward velocity
    prestate = copy.deepcopy(state)

    # 45 degrees sloped floor
    ftor = ApplyFloorBounce(m=-1.0, b=0.0, e=elasticity)
    res = ftor(state)
    assert res is None

    # Expecting velocities to reflect after bounce
    assert np.isclose(state.vx[0, 0], elasticity)
    assert np.isclose(state.vy[0, 0], 0.0)
    assert np.all(state.vx[1:, 1:] == prestate.vx[1:, 1:])
    assert np.all(state.vy[1:, 1:] == prestate.vy[1:, 1:])

    # Ensure moved above surface
    assert np.all(state.py >= -state.px)


@pytest.mark.parametrize("elasticity", [0.5, 1.0, 1.5])
def test_some_cells_below_sloped_floor2(elasticity: float):
    state = State()
    conditioners.ApplyTranslate(  # move lower left cell below floor
        dpx=-state.vx.min() - 1e-7, dpy=-state.vy.min() - 1e-7
    )(state)
    state.vx.fill(-1.0)  # no horizontal velocity
    state.vy.fill(-1.0)  # downward velocity
    prestate = copy.deepcopy(state)

    # 45 degrees sloped floor
    ftor = ApplyFloorBounce(m=-1.0, b=0.0, e=elasticity)
    res = ftor(state)
    assert res is None

    # Expecting velocities to reflect after bounce
    assert np.isclose(state.vx[0, 0], elasticity)
    assert np.isclose(state.vy[0, 0], elasticity)
    assert np.all(state.vx[1:, 1:] == prestate.vx[1:, 1:])
    assert np.all(state.vy[1:, 1:] == prestate.vy[1:, 1:])

    # Ensure moved above surface
    assert np.all(state.py >= -state.px)


@pytest.mark.parametrize("elasticity", [0.5, 1.0, 1.5])
def test_slanted_trajectory_flat_floor(elasticity: float):
    state = State()

    conditioners.ApplyRotate(theta_degrees=-45.0)(state)
    conditioners.ApplyTranslate(dpy=-state.py.min() - 1e-7)(state)
    # calc x and y components of velocity based on attack angle 30 degrees
    pre_vx = np.cos(np.radians(30.0))  # Horizontal component
    pre_vy = -np.sin(np.radians(30.0))  # Downward motion, hence negative
    state.vx.fill(pre_vx)
    state.vy.fill(pre_vy)
    prestate = copy.deepcopy(state)

    ftor = ApplyFloorBounce(m=0.0, b=0.0, e=elasticity)
    res = ftor(state)
    assert res is None

    # calc the expected velocities after the bounce
    expected_vx = pre_vx * elasticity  # x component preserved by bounce
    expected_vy = -pre_vy * elasticity  # y component reversed by bounce

    assert np.isclose(state.vx[0, 0], expected_vx)
    assert np.isclose(state.vy[0, 0], expected_vy)
    assert np.all(state.vx[1:, 1:] == prestate.vx[1:, 1:])
    assert np.all(state.vy[1:, 1:] == prestate.vy[1:, 1:])

    # Ensure moved above surface
    assert np.all(state.py >= 0.0)
    assert np.all(state.px[1:, 1:] == prestate.px[1:, 1:])
    assert np.all(state.py[1:, 1:] == prestate.py[1:, 1:])
