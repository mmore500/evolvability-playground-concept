import typing

from ...events import EventBuffer
from ...State import State


class ClearEventBuffer:
    """Removes all events from buffer."""

    def __call__(
        self: "ClearEventBuffer",
        state: State,
        event_buffer: typing.Optional[EventBuffer] = None,
    ) -> None:
        """Clear event buffer."""
        if event_buffer is not None:
            event_buffer.clear()
