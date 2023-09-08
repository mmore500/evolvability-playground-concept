from ..State import State
from ..Params import Params


class ApplyGravity:

    _params: Params

    def __init__(self: "ApplyGravity", params: Params) -> None:
        self._params = params

    def __call__(self: "ApplyGravity", state: State) -> None:
        params = self._params
        state.vy -= params.g * params.dt
