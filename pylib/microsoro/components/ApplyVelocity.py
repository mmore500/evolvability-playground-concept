from ..State import State
from ..Params import Params


class ApplyVelocity:
    """Advance position one simulation step under state velocities."""

    _params: Params

    def __init__(self: "ApplyVelocity", params: Params) -> None:
        self._params = params

    def __call__(self: "ApplyVelocity", state: State) -> None:
        params = self._params
        state.px += state.vx * params.dt
        state.py += state.vy * params.dt
        return state