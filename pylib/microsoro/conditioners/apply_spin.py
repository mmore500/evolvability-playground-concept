import numpy as np

from ..State import State


def apply_spin(state: State, omega: float = 1.0) -> None:
    """Adjust velocities to impart angular momentum."""

    # Compute the center of rotation
    cx = (state.px.max() + state.px.min()) / 2.0
    cy = (state.py.max() + state.py.min()) / 2.0

    # Compute the radial velocities
    state.vx += -omega * (state.py - cy)
    state.vy += omega * (state.px - cx)
