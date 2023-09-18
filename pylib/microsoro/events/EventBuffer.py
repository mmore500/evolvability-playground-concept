from collections import abc

import functools
import typing


class EventBuffer:
    """Accumulates events for deferred processing."""

    _buffer: typing.List

    def __init__(self: "EventBuffer") -> None:
        """Initialize buffer."""
        self._buffer = list()

    def __eq__(self: "EventBuffer", other: "EventBuffer") -> bool:
        """Test equality."""
        return type(self) == type(other) and self.__dict__ == other.__dict__

    def clear(self: "EventBuffer") -> None:
        """Clear all events from the buffer."""
        self._buffer = list()

    def enqueue(self: "EventBuffer", event: typing.Any) -> None:
        """Append an event to the buffer.

        Parameters
        ----------
        event : Any
            The event to be added.
        """
        self._buffer.append(event)

    def consume(
        self: "EventBuffer",
        event_type: typing.Type,
        handler: typing.Callable,
        skip_duplicates: bool = False,
    ) -> typing.List:
        """Process events of specified type, removing them from the buffer.

        Events that do not match the specified type are left in the buffer.

        Parameters
        ----------
        event_type : Type
            The type of event to be processed.
        handler : Callable
            The function to be used to process the event.
        skip_duplicates : bool, default False
            If True, among equivalent events the handle will only be called on
            the first.

            All equivalent events will still be discarded.

        Returns
        -------
        list
            Results of handler invocations.

        Notes
        -----
        The skip_duplicates option is implemented using an lru_cache, so .
        """

        results = []
        appending_handler = lambda event: results.append(handler(event))

        if skip_duplicates:
            if not issubclass(event_type, abc.Hashable):
                raise ValueError(
                    f"to use {skip_duplicates=}, "
                    f"{event_type=} must be hashable"
                )
            appending_handler = functools.lru_cache(maxsize=None)(
                appending_handler,
            )

        remaining_events = []
        for event in self._buffer:
            if isinstance(event, event_type):
                appending_handler(event)
            else:
                remaining_events.append(event)

        self._buffer = remaining_events
        return results
