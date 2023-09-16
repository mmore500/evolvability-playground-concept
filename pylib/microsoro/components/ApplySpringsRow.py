import typing

import numpy as np

from ..State import State
from ..Params import Params


class ApplySpringsRow:
    """Simulate action of springs between horizontal pairs of cells."""

    _params: Params

    def __init__(
        self: "ApplySpringsRow",
        params: typing.Optional[Params] = None,
    ) -> None:
        """Initialize functor."""
        if params is None:
            params = Params()
        self._params = params

    def __call__(self: "ApplySpringsRow", state: State) -> None:
        """Calculate spring forces between horizontal pairs of cells and apply
        to State velocity."""
        # how far apart are horizontal pairs of cells?
        row_dists_horiz = np.diff(state.px, axis=1)
        row_dists_vert = np.diff(state.py, axis=1)
        row_dists = np.sqrt(row_dists_horiz**2 + row_dists_vert**2)

        # decomposed unit vector
        normed_row_dists_horiz = row_dists_horiz / row_dists
        normed_row_dists_vert = row_dists_vert / row_dists

        # net forces: negative is repulsion, positive is attraction
        l_naught = 1  # natural length of springs
        f = self._params.k * (row_dists - l_naught)

        # decompose force into horizontal and vertical components
        fx = f * normed_row_dists_horiz
        fy = f * normed_row_dists_vert

        # is clipping necessary?
        # fx = np.clip(fx, -1e12, 1e12)
        # fy = np.clip(fy, -1e12, 1e12)

        # horizontal components of acceleration
        ax = np.zeros_like(state.vx)
        ax[:, :-1] += fx[:, :]  # right-facing forces
        ax[:, 1:] -= fx[:, :]  # left-facing forces
        # apply acceleration to state
        state.vx += ax * self._params.dt

        # vertical components of acceleration
        ay = np.zeros_like(state.vy)
        ay[:, :-1] += fy[:, :]  # right-facing forces
        ay[:, 1:] -= fy[:, :]  # left-facing forces
        # apply acceleration to state
        state.vy += ay * self._params.dt
