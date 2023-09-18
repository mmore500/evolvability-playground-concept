import typing

from ...State import State
from ...Params import Params


class ApplyGravity:

    _params: Params

    def __init__(
        self: "ApplyGravity",
        params: typing.Optional[Params] = None,
    ) -> None:
        if params is None:
            params = Params()
        self._params = params

    def __call__(
        self: "ApplyGravity",
        state: State,
        event_buffer: typing.Optional = None,
    ) -> None:
        params = self._params
        state.vy -= params.g * params.dt
