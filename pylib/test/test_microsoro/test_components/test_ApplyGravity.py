import copy
import typing

import numpy as np
import pytest

from pylib.microsoro import Params, State
from pylib.microsoro.components import ApplyGravity
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


def test_ApplyGravity(event_buffer: typing.Optional[EventBuffer]):
    state = State()
    params = Params()
    state_ = copy.deepcopy(state)

    res = ApplyGravity(params)(state, event_buffer)
    assert res is None
    assert State.same_position_as(state, state_)
    assert np.allclose(state.vx, state_.vx)
    assert np.allclose(state.vy, state_.vy - params.dt * params.g)


def test_ApplyGravity_default_ctor():
    assert ApplyGravity()._params == Params()
