from ..State import State
from ..Params import Params


def apply_increment_elapsed_time(state: State, params: Params) -> None:
    state.t += params.dt
