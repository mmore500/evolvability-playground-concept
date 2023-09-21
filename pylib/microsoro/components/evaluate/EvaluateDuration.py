import typing

from ...events import EventBuffer
from ...State import State


class EvaluateDuration:

    _halting_component: typing.Callable

    def __init__(
        self: "EvaluateDuration",
        halting_component: typing.Callable,
    ) -> None:
        self._halting_component = halting_component

    def __call__(
        self: "EvaluateDuration",
        state: State,
        event_buffer: typing.Optional[EventBuffer],
    ) -> typing.Optional[float]:
        if self._halting_component(state, event_buffer) is not None:
            return state.t
