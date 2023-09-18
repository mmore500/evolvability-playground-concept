import copy
import typing

import pytest

from pylib.microsoro import Params, State
from pylib.microsoro.components import ClearEventBuffer
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


def test_ClearEventBuffer(event_buffer: typing.Optional[EventBuffer]):
    state = State()
    prestate = copy.deepcopy(state)

    if event_buffer is not None:
        event_buffer.enqueue("test")

    ftor = ClearEventBuffer()
    res = ftor(state, event_buffer)
    assert res is None

    if event_buffer is not None:
        assert event_buffer._buffer == []

    # state shouldn't have been mutaed
    assert State.same_position_as(state, prestate)
    assert State.same_velocity_as(state, prestate)
    assert state.t == prestate.t
