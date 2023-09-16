import numpy as np

from ..State import State


class ApplyTorsion:
    """Adjust angular position of cells clockwise, twisting outer cells
    further."""

    _phi_radians: float

    def __init__(
        self: "ApplyTorsion",
        phi_degrees: float = 45.0,
    ) -> None:
        """
        Initialize functor.

        Parameters
        ----------
        phi_degrees : float, default 1.0
            Outermost cells will rotate by this many degrees.
        """
        self._phi_radians = np.radians(phi_degrees)

    def __call__(self: "ApplyTorsion", state: State) -> None:
        """Adjust cell positions to add torsion."""
        # Compute the center of twist
        cx: float = (state.px.max() + state.px.min()) / 2.0
        cy: float = (state.py.max() + state.py.min()) / 2.0

        # Calculate the displacement of each point from the center
        dx = state.px - cx
        dy = state.py - cy

        # Calculate distance of each point from the center
        distance_from_center = np.sqrt(dx**2 + dy**2)
        max_distance = distance_from_center.max()

        # Modulate rotation angle based on distance from the center
        phi = self._phi_radians * -1  # make clockwise, not counterclockwise
        scaled_phi = phi * (distance_from_center / max_distance)

        # Apply torsion
        state.px = cx + dx * np.cos(scaled_phi) - dy * np.sin(scaled_phi)
        state.py = cy + dx * np.sin(scaled_phi) + dy * np.cos(scaled_phi)
