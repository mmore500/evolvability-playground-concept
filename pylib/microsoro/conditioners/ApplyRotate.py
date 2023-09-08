import numpy as np

from ..State import State


class ApplyRotate:
    """Rotate the points in the state by angle_degrees around the center."""

    _angle_degrees: float

    def __init__(self: "ApplyRotate", angle_degrees: float = 45.0) -> None:
        self._angle_degrees = angle_degrees

    def __call__(self: "ApplyRotate", state: State) -> None:

        # Convert the angle to radians
        angle_radians = np.radians(self._angle_degrees)

        # Compute the center of rotation
        cx = (state.px.max() + state.px.min()) / 2.0
        cy = (state.py.max() + state.py.min()) / 2.0

        # Perform the rotation
        x_rotated = (
            (state.px - cx) * np.cos(angle_radians)
            - (state.py - cy) * np.sin(angle_radians)
            + cx
        )
        y_rotated = (
            (state.px - cx) * np.sin(angle_radians)
            + (state.py - cy) * np.cos(angle_radians)
            + cy
        )

        state.px = x_rotated
        state.py = y_rotated
