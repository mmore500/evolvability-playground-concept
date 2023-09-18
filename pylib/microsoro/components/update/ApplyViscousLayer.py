import typing

import numpy as np

from ...events import EventBuffer, RenderFloorEvent
from ...State import State
from ...Params import Params


class ApplyViscousLayer:
    """Slow cells within a viscous layer."""

    _mu: float
    _intercept: float
    _slope: float
    _params: Params

    def __init__(
        self: "ApplyViscousLayer",
        mu: float = 0.1,
        m: float = 0.0,
        b: float = 0.0,
        params: typing.Optional[Params] = None,
    ) -> None:
        """Initialize functor.

        Parameters:
        ----------
        mu : float, default 0.1
            Frictional coefficient of the viscous layer.

            Specifies proportion of kinetic energy drained per unit time.
        m : float, default 0.0
            Slope of the upper boundary of the layer, default flat.
        b : float, default 1.0
            Y-intercept of the upper bound of the layer.

        Raises:
        ------
        ValueError:
            If the provided frictional coefficient mu is negative.
        """
        if not 0 <= mu:
            raise ValueError(
                f"ApplyViscousLayer friction {mu=} must be non-negative."
            )
        self._mu = mu
        self._intercept = b
        self._slope = m
        if params is None:
            params = Params()
        self._params = params

    def __call__(
        self: "ApplyViscousLayer",
        state: State,
        event_buffer: typing.Optional[EventBuffer] = None,
    ) -> None:
        """Apply resistance to any cell moving through viscous layer."""
        m = self._slope
        b = self._intercept
        if event_buffer is not None:
            event_buffer.enqueue(
                RenderFloorEvent(m=m, b=b, flavor="viscous layer")
            )

        # Get the floor y-values for all x-positions
        y_floor = m * state.px + b

        # Find the cells which are below the floor
        below_floor_mask = state.py < y_floor

        # if no cells are below floor, we are done
        if not np.any(below_floor_mask):
            return

        dt = self._params.dt
        # damping constant, clipped to prevent any overshoot
        mu = np.minimum(self._mu, 1 / dt)
        dvx = -state.vx[below_floor_mask] * mu * dt
        dvy = -state.vy[below_floor_mask] * mu * dt

        state.vx[below_floor_mask] += dvx
        state.vy[below_floor_mask] += dvy
