import copy
import typing

import pytest

from pylib.microsoro import Params, State
from pylib.microsoro.components import ApplyIncrementElapsedTime
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


def test_ApplyIncrementElapsedTime(event_buffer: typing.Optional[EventBuffer]):
    state = State()
    params = Params()
    state_ = copy.deepcopy(state)

    res = ApplyIncrementElapsedTime(params)(state, event_buffer)
    assert res is None
    assert State.same_position_as(state, state_)
    assert State.same_velocity_as(state, state_)
    assert state.t == state_.t + params.dt


def test_ApplyIncrementElapsedTime_default_ctor():
    assert ApplyIncrementElapsedTime()._params == Params()
