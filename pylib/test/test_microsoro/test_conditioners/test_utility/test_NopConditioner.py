from pylib.microsoro import State
from pylib.microsoro.conditioners import NopConditioner
from pylib.microsoro.events import EventBuffer


def test_NopConditioner():
    state = State()
    event_buffer = EventBuffer()

    ftor = NopConditioner()
    res = ftor(state, event_buffer)
    assert res is None

    assert state == State()
    assert event_buffer == EventBuffer()
