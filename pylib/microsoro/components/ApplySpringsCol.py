import typing

import numpy as np

from ..State import State
from ..Params import Params


class ApplySpringsCol:
    """Simulate action of springs between vertical pairs of cells."""

    _params: Params

    def __init__(
        self: "ApplySpringsCol",
        params: typing.Optional[Params] = None,
    ) -> None:
        """Initialize functor."""
        if params is None:
            params = Params()
        self._params = params

    def __call__(self: "ApplySpringsCol", state: State) -> None:
        """Calculate spring forces between vertical pairs of cells and apply to
        State velocity."""
        # how far apart are vertical pairs of cells?
        col_dists_horiz = np.diff(state.px, axis=0)
        col_dists_vert = np.diff(state.py, axis=0)
        col_dists = np.sqrt(col_dists_horiz**2 + col_dists_vert**2)

        # decomposed unit vector
        normed_col_dists_horiz = col_dists_horiz / col_dists
        normed_col_dists_vert = col_dists_vert / col_dists

        # net forces: negative is repulsion, positive is attraction
        l_naught = 1  # natural length of springs
        f = self._params.k * (col_dists - l_naught)

        # decompose force into horizontal and vertical components
        fx = f * normed_col_dists_horiz
        fy = f * normed_col_dists_vert

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
