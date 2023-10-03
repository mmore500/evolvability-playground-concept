import typing

import numpy as np

from ...State import State
from ...events import EventBuffer, RenderFloorEvent


class ApplyFloorBounce:
    """Bounce cells off a sloped floor."""

    _elasticity: float
    _intercept: float
    _slope: float

    def __init__(
        self: "ApplyFloorBounce",
        e: float = 1.0,
        m: float = 0.0,
        b: float = 0.0,
    ) -> None:
        """Initialize functor.

        Parameters:
        ----------
        e : float, default 1.0
            Elasticity coefficient of the bounce.

            Specifies proportion of kinetic energy retained after collision.
        m : float, default 0.0
            Slope of the floor, default flat.
        b : float, default 0.0
            Y-intercept of the floor.

        Raises:
        ------
        ValueError:
            If the provided elasticity is negative.
        """
        if e < 0:
            raise ValueError(
                f"ApplyFloorBounce elasticity {e=} must be non-negative."
            )
        self._elasticity = float(e)
        self._intercept = float(b)
        self._slope = float(m)

    def __call__(
        self: "ApplyFloorBounce",
        state: State,
        event_buffer: typing.Optional[EventBuffer] = None,
    ) -> None:
        """If any tresspass past floor boundaries has occurred, correct cell
        positions (i.e., retroactively) and reflect cell velocities off
        surface."""
        m = self._slope
        b = self._intercept
        if event_buffer is not None:
            event_buffer.enqueue(RenderFloorEvent(m=m, b=b, flavor="floor"))

        # Get the floor y-values for all x-positions
        y_floor = m * state.px + b

        # Find the cells which are below the floor
        below_floor_mask = state.py < y_floor

        # if no cells are below floor, we are done
        if not np.any(below_floor_mask):
            return

        # Determine the normalized normal vector to the slope
        normal = np.array([-m, 1])
        normal /= np.linalg.norm(normal)
        assert np.isclose(
            np.dot(normal, np.array([1, m])), 0
        )  # should be perpendicular to slope

        # rough calculation of max ppenetration past surface
        # independently along x and y axes (may overestimate
        tolerance_factor = 1e-12  # should this be configurabe?

        # update state position to correct penetration
        # for now, just shift entire state
        # (for simulation robustness to low precision)
        #
        # another option be just move offending cells
        # and then perform corrections so that the pre-existing less-than and
        # greater-than relationships between successive rows are maintained
        # i.e., any slippage of one layer past the other is corrected
        y_penetration = y_floor[below_floor_mask] - state.py[below_floor_mask]
        state.py += np.max(y_penetration) + tolerance_factor

        # y = mx + b
        # so y / m - b / m = x
        if m:
            x_floor = (state.py[below_floor_mask] - b) / m
            x_penetration = x_floor - state.px[below_floor_mask]
            # update state x positions to correct any penetration
            # shifts all x positions, see note above for y penetration
            state.px += np.sign(m) * np.max(x_penetration) + tolerance_factor

        # Check that all cells now above the floor
        assert not np.any(state.py < m * state.px + b)

        # Compute dot product of incoming velocity with normal for cells below
        # the floor
        dot_product = (
            state.vx[below_floor_mask] * normal[0]
            + state.vy[below_floor_mask] * normal[1]
        )

        # Reflect the velocities of the cells below the floor
        reflection_x = state.vx[below_floor_mask] - 2 * dot_product * normal[0]
        reflection_y = state.vy[below_floor_mask] - 2 * dot_product * normal[1]

        # Make robust: correct sign to ensure upwards bounce
        # (needed due to interactions between intersecting floors)
        # reflection_x = reflection_x * np.sign(reflection_y)
        # ^^^ logically, x component would be reversed when reversing velocity,
        # but this causes a bad feedback loop with other floors
        reflection_y = np.abs(reflection_y)

        # Update velocities, applying velocity loss to imperfect elasticity
        state.vx[below_floor_mask] = reflection_x * self._elasticity
        state.vy[below_floor_mask] = reflection_y * self._elasticity
