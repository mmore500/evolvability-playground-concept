import copy

from pylib.microsoro import (
    get_default_update_regimen,
    State,
    Structure,
    Params,
)
from pylib.microsoro.conditioners import ApplySpin, ApplyTranslate


def test_get_default_update_regimen():
    state1 = State()
    ApplyTranslate(dpy=-2)(state1)
    prestate1 = copy.deepcopy(state1)

    regimen1 = get_default_update_regimen()
    for step in regimen1:
        step(state1)
    assert not State.same_position_as(state1, prestate1)
    assert not State.same_velocity_as(state1, prestate1)

    state2 = State()
    ApplyTranslate(dpy=-2)(state2)
    ApplySpin()(state2)
    prestate2 = copy.deepcopy(state2)

    regimen2 = get_default_update_regimen()
    for step in regimen2:
        step(state2)
    assert not State.same_position_as(state2, prestate2)
    assert not State.same_velocity_as(state2, prestate2)

    assert not State.same_position_as(state1, state2)
    assert not State.same_velocity_as(state1, state2)


def test_get_default_update_regimen_params():

    state1 = State()
    ApplyTranslate(dpy=-2)(state1)
    regimen1 = get_default_update_regimen()
    for _update in range(100):  # need several updates to get past np.isclose
        for step in regimen1:
            step(state1)

    state2 = State()
    params2 = Params(g=100.0)
    ApplyTranslate(dpy=-2)(state2)
    regimen2 = get_default_update_regimen(params=params2)
    for _update in range(100):  # need several updates to get past np.isclose
        for step in regimen2:
            step(state2)

    assert not State.same_position_as(state1, state2)
    assert not State.same_velocity_as(state1, state2)


def test_get_default_update_regimen_structure():
    state1 = State()
    ApplyTranslate(dpy=-2)(state1)
    ApplySpin()(state1)
    regimen1 = get_default_update_regimen()
    for step in regimen1:
        step(state1)

    state2 = State()
    ApplyTranslate(dpy=-2)(state1)
    ApplySpin()(state2)
    params2 = Params(m=10.0)
    regimen2 = get_default_update_regimen(
        structure=Structure(params=params2),
    )
    for step in regimen2:
        step(state2)

    assert not State.same_position_as(state1, state2)
    assert not State.same_velocity_as(state1, state2)
