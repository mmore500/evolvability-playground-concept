from pylib.microsoro import State
from pylib.microsoro.components import NopComponent
from pylib.microsoro.events import EventBuffer


def test_NopComponent():
    state = State()
    event_buffer = EventBuffer()

    ftor = NopComponent()
    res = ftor(state, event_buffer)
    assert res is None

    assert state == State()
    assert event_buffer == EventBuffer()
