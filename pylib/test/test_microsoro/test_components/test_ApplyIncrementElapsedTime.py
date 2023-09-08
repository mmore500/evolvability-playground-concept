import copy

from pylib.microsoro import Params, State
from pylib.microsoro.components import ApplyIncrementElapsedTime


def test_ApplyIncrementElapsedTime():
    state = State()
    params = Params()
    state_ = copy.deepcopy(state)

    ApplyIncrementElapsedTime(params)(state)
    assert (state.px == state_.px).all() and (state.py == state_.py).all()
    assert (state.vx == state_.vx).all() and (state.vy == state_.vy).all()
    assert state.t == state_.t + params.dt
