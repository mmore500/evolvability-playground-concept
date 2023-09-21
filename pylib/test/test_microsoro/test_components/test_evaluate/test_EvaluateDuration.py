import typing

import pytest

from pylib.microsoro import State
from pylib.microsoro.components import EvaluateDuration, HaltAfterElapsedTime
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


def test_HaltAfterElapsedTime(event_buffer: typing.Optional[EventBuffer]):

    state = State()
    ftor_factory = lambda t_thresh: EvaluateDuration(
        halting_component=HaltAfterElapsedTime(t_thresh),
    )

    assert ftor_factory(15.0)(state, event_buffer) is None

    state.t = 14.5
    assert ftor_factory(15.0)(state, event_buffer) is None

    state.t = 16.5
    assert ftor_factory(15.0)(state, event_buffer) == 16.5
