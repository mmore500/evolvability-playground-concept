import numpy as np

from ...State import State


class ApplyRotate:
    """Rotate the points in the state by theta_degrees clockwise around the
    center."""

    _theta_radians: float

    def __init__(self: "ApplyRotate", theta_degrees: float = 45.0) -> None:
        # Convert the angle to radians
        self._theta_radians = np.radians(theta_degrees)

    def __call__(self: "ApplyRotate", state: State) -> None:

        # Compute the center of rotation
        cx = (state.px.max() + state.px.min()) / 2.0
        cy = (state.py.max() + state.py.min()) / 2.0

        # Perform the rotation
        theta = self._theta_radians * -1  # make clockwise not counterclockwise
        x_rotated = (
            (state.px - cx) * np.cos(theta)
            - (state.py - cy) * np.sin(theta)
            + cx
        )
        y_rotated = (
            (state.px - cx) * np.sin(theta)
            + (state.py - cy) * np.cos(theta)
            + cy
        )

        state.px = x_rotated
        state.py = y_rotated
