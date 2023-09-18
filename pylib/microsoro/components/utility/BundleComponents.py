import typing

from ...events import EventBuffer
from ...State import State


class BundleComponents:
    """Package simulation components together for sequential application."""

    _components: typing.List[typing.Callable]

    def __init__(self: "BundleComponents", *components) -> None:
        """Initialize functor with sequence of simulation components."""
        self._components = components

    def __call__(
        self: "BundleComponents",
        state: State,
        event_buffer: typing.Optional[EventBuffer] = None,
    ) -> typing.Optional:
        """Apply component sequence.

        Shortcircuits to return the first non-None component return value if
        any.
        """
        for component in self._components:
            res = component(state, event_buffer)
            if res is not None:
                return res
