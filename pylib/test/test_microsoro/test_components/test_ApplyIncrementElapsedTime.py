import copy

from pylib.microsoro import Params, State
from pylib.microsoro.components import ApplyIncrementElapsedTime


def test_ApplyIncrementElapsedTime():
    state = State()
    params = Params()
    state_ = copy.deepcopy(state)

    ApplyIncrementElapsedTime(params)(state)
    assert State.same_position_as(state, state_)
    assert State.same_velocity_as(state, state_)
    assert state.t == state_.t + params.dt


def test_ApplyIncrementElapsedTime_default_ctor():
    assert ApplyIncrementElapsedTime()._params == Params()
