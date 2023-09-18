import numpy as np

from ..State import State


class ApplyDeflect:
    """Rotate the velocities in the state by theta_degrees clockwise."""

    _theta_radians: float

    def __init__(self: "ApplyDeflect", theta_degrees: float = 45.0) -> None:
        # Convert the angle to radians
        self._theta_radians = np.radians(theta_degrees)

    def __call__(self: "ApplyDeflect", state: State) -> None:

        # Perform the rotation
        theta = self._theta_radians * -1  # make clockwise not counterclockwise
        vx_rotated = state.vx * np.cos(theta) - state.vy * np.sin(theta)
        vy_rotated = state.vx * np.sin(theta) + state.vy * np.cos(theta)

        state.vx = vx_rotated
        state.vy = vy_rotated
