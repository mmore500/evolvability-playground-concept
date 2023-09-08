from ..State import State
from ..Params import Params


class ApplyIncrementElapsedTime:

    _params: Params

    def __init__(self: "ApplyIncrementElapsedTime", params: Params) -> None:
        self._params = params

    def __call__(self: "ApplyIncrementElapsedTime", state: State) -> None:
        state.t += self._params.dt
