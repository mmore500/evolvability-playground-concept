import numpy as np

from .State import State


def apply_translate(state: State, dx: float = 0.0, dy: float = 0.0) -> State:
    """Adjust position."""
    state.px += dx
    state.py += dy
    return state
