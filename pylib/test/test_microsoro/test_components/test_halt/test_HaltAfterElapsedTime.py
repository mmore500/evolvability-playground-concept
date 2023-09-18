import typing

import pytest

from pylib.microsoro import State
from pylib.microsoro.components import HaltAfterElapsedTime
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


def test_HaltAfterElapsedTime(event_buffer: typing.Optional[EventBuffer]):

    state = State()
    HaltAfterElapsedTime(15.0)(state, event_buffer) is None

    state.t = 14.5
    HaltAfterElapsedTime(15.0)(state, event_buffer) is state

    state.t = 16.5
    HaltAfterElapsedTime(15.0)(state, event_buffer) is state
