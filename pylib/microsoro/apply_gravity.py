from .State import State
from .Params import Params


def apply_gravity(state: State, params: Params) -> State:
    state.vy -= params.g * params.dt
    return state
