import typing

from ...State import State
from ...Params import Params


class ApplyIncrementElapsedTime:

    _params: Params

    def __init__(
        self: "ApplyIncrementElapsedTime",
        params: typing.Optional[Params] = None,
    ) -> None:
        if params is None:
            params = Params()
        self._params = params

    def __call__(
        self: "ApplyIncrementElapsedTime",
        state: State,
        event_buffer: typing.Optional = None,
    ) -> None:
        state.t += self._params.dt
