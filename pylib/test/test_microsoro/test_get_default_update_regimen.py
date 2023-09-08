from pylib.microsoro import get_default_update_regimen, State, Params
from pylib.microsoro.conditioners import ApplySpin


def test_get_default_update_regimen():
    state1 = State()
    regimen1 = get_default_update_regimen()
    for step in regimen1:
        step(state1)
    assert not (
        (state1.px == State().px).all() and (state1.py == State().py).all()
    )
    state2 = State()
    ApplySpin()(state2)
    regimen2 = get_default_update_regimen()
    for step in regimen2:
        step(state2)
    assert not (
        (state1.px == state2.px).all() and (state1.py == state2.py).all()
    )

    state3 = State()
    params3 = Params(g=100.0)
    ApplySpin()(state3)
    regimen3 = get_default_update_regimen(params3)
    for step in regimen3:
        step(state3)
    assert not (
        (state1.px == state3.px).all() and (state1.py == state3.py).all()
    )
