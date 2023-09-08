from ..State import State
from ..Params import Params


def apply_gravity(state: State, params: Params) -> None:
    state.vy -= params.g * params.dt
