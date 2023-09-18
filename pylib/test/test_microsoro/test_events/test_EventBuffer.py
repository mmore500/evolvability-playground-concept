import pytest
import typing

from pylib.microsoro.events import EventBuffer


def test_event_buffer_initialization():
    """Test that the buffer is initialized as an empty list."""
    eb = EventBuffer()
    assert eb._buffer == []


def test_event_buffer_enqueue():
    """Test that an event can be enqueued."""
    eb = EventBuffer()
    eb.enqueue("test_event")
    assert eb._buffer == ["test_event"]


def test_event_buffer_clear():
    """Test that the buffer can be cleared."""
    eb = EventBuffer()
    eb.enqueue("test_event")
    eb.clear()
    assert eb._buffer == []


@pytest.mark.parametrize(
    "events, event_type, skip_duplicates, expected_remaining, "
    "expected_ncalls, expected_handled",
    [
        (["a", 1, "b", 2], str, False, [1, 2], 2, ["a", "b"]),
        (["a", "b", 2], int, False, ["a", "b"], 1, [2]),
        (["a", "a", 1, 2], str, True, [1, 2], 1, ["a"]),
        (["a", "a", 1, 2], int, True, ["a", "a"], 2, [1, 2]),
    ],
)
def test_event_buffer_consume(
    events: typing.List,
    event_type: typing.Type,
    skip_duplicates: bool,
    expected_remaining: typing.List,
    expected_ncalls: int,
    expected_handled: typing.List,
):
    """Test that events of a specified type can be consumed."""
    eb = EventBuffer()
    for event in events:
        eb.enqueue(event)

    call_counter = 0

    def handler(e: event_type) -> event_type:
        nonlocal call_counter
        call_counter += 1
        return e

    res = eb.consume(event_type, handler, skip_duplicates)
    assert res == expected_handled
    assert eb._buffer == expected_remaining
    assert expected_ncalls == call_counter


def test_event_buffer_consume_unhashable_skip_duplicates():
    """Test ValueError is raised if trying to skip_duplicates on unhashable
    event_type."""
    eb = EventBuffer()
    eb.enqueue(["list_event"])

    with pytest.raises(ValueError):
        eb.consume(list, handler=lambda e: None, skip_duplicates=True)


def test_event_buffer_consume_function_called():
    """Test that the handler function is correctly called."""
    eb = EventBuffer()
    eb.enqueue("test_event")

    # This will collect the events passed to it
    collected = []

    def handler(e: str) -> None:
        collected.append(e)
        return e

    res = eb.consume(str, handler)
    assert collected == ["test_event"]
    assert res == ["test_event"]
