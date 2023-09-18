import pytest

from pylib.microsoro.components import BundleComponents
from pylib.microsoro.events import EventBuffer
from pylib.microsoro import State


def component1(state: State, event_buffer: EventBuffer) -> str:
    return "component1"


def component2(state: State, event_buffer: EventBuffer) -> str:
    return "component2"


def component3(state: State, event_buffer: EventBuffer) -> None:
    return None


def test_initialize_bundle_components():
    ftor = BundleComponents()
    assert len(ftor._components) == 0

    ftor = BundleComponents(component1, component2)
    assert len(ftor._components) == 2

    ftor = BundleComponents(component1, component1)
    assert len(ftor._components) == 2


def test_call_first_component():
    state = State()
    ftor = BundleComponents(component1, component3)
    result = ftor(state)
    assert result == "component1"


def test_call_second_component():
    state = State()
    ftor = BundleComponents(component3, component2)
    result = ftor(state)
    assert result == "component2"


def test_no_components_return_value():
    state = State()
    ftor = BundleComponents(component3, component3)
    result = ftor(state)
    assert result is None


def test_components_shortcircuit():
    state = State()

    def unreachable() -> None:
        assert False

    ftor = BundleComponents(component1, unreachable)
    result = ftor(state)
    assert result == "component1"


def test_event_buffer_passed_correctly():
    state = State()

    def enqueue_component(state: State, event_buffer: EventBuffer) -> None:
        event_buffer.enqueue("boo")

    ftor = BundleComponents(enqueue_component)
    event_buffer = EventBuffer()
    state = State()
    ftor(state, event_buffer)
    assert event_buffer._buffer == ["boo"]


def test_state_passed_correctly():
    state = State()

    def mutate_component(state: State, event_buffer: EventBuffer) -> None:
        state.t = 42.0

    ftor = BundleComponents(mutate_component)
    event_buffer = EventBuffer()
    state = State()
    ftor(state, event_buffer)
    assert state.t == 42.0
