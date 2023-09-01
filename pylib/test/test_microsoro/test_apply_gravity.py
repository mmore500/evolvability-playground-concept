import copy

from pylib.microsoro import apply_gravity, Params, State


def test_apply_gravity():
    state = State()
    params = Params()
    state_ = copy.deepcopy(state)

    apply_gravity(state, params)
    assert (state.px == state_.px).all() and (state.py == state_.py).all()
    assert (state.vx == state_.vx).all()
    assert (state.vy == state_.vy - params.dt * params.g).all()
