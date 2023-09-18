import typing

import numpy as np

from ...State import State
from ...Params import Params


class ApplySpringDampingCol:
    """Simulate damping action of springs between vertical pairs of cells."""

    _params: Params

    def __init__(
        self: "ApplySpringDampingCol",
        params: typing.Optional[Params] = None,
    ) -> None:
        """Initialize functor."""
        if params is None:
            params = Params()
        self._params = params

    def __call__(
        self: "ApplySpringDampingCol",
        state: State,
        event_buffer: typing.Optional = None,
    ) -> None:
        """Calculate spring damping forces between vertical pairs of cells and
        apply to State velocity."""
        # how far apart are vertical pairs of cells?
        col_relvels_horiz = np.diff(state.vx, axis=0)
        col_relvels_vert = np.diff(state.vy, axis=0)
        col_relvels = np.sqrt(col_relvels_horiz**2 + col_relvels_vert**2)

        # decomposed unit vector
        # make 0/0 -> 0, see https://stackoverflow.com/a/37977222/17332200
        divide_mask = col_relvels != 0
        normed_col_relvels_horiz = np.divide(
            col_relvels_horiz,
            col_relvels,
            out=np.zeros_like(col_relvels_horiz),
            where=divide_mask,
        )
        normed_col_relvels_vert = np.divide(
            col_relvels_vert,
            col_relvels,
            out=np.zeros_like(col_relvels_vert),
            where=divide_mask,
        )

        # net forces: negative is repulsion, positive is attraction
        b = self._params.b  # damping constant
        f = b * col_relvels

        # decompose force into horizontal and vertical components
        fx = f * normed_col_relvels_horiz
        fy = f * normed_col_relvels_vert

        # is clipping necessary?
        # fx = np.clip(fx, -1e12, 1e12)
        # fy = np.clip(fy, -1e12, 1e12)

        # horizontal components of acceleration
        ax = np.zeros_like(state.vx)
        ax[:-1, :] += fx[:, :]  # up-facing forces
        ax[1:, :] -= fx[:, :]  # down-facing forces
        # apply acceleration to state
        state.vx += ax * self._params.dt

        # vertical components of acceleration
        ay = np.zeros_like(state.vy)
        ay[:-1, :] += fy[:, :]  # up-facing forces
        ay[1:, :] -= fy[:, :]  # down-facing forces
        # apply acceleration to state
        state.vy += ay * self._params.dt
