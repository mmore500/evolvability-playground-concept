from .State import State
from .Params import Params


def apply_velocity(state: State, params: Params) -> State:
    """Advance position one simulation step under state velocities."""
    state.px += state.vx * params.dt
    state.py += state.vy * params.dt
    return state
