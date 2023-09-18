import numpy as np

from ...State import State


class ApplySpin:
    """Adjust velocities to impart clockwise angular momentum."""

    _omega_radians: float

    def __init__(self: "ApplySpin", omega_degrees: float = 120.0) -> None:
        self._omega_radians = np.radians(omega_degrees)

    def __call__(self: "ApplySpin", state: State) -> None:
        # Compute the center of rotation
        cx = (state.px.max() + state.px.min()) / 2.0
        cy = (state.py.max() + state.py.min()) / 2.0

        omega = self._omega_radians
        # Compute the radial velocities
        state.vx += omega * (state.py - cy)
        state.vy += -omega * (state.px - cx)
