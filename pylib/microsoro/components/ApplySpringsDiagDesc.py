import typing

import numpy as np

from ..State import State
from ..Params import Params


class ApplySpringsDiagDesc:
    """Simulate action of springs between pairs of cells along descending
    diagonals."""

    _params: Params

    def __init__(
        self: "ApplySpringsDiagDesc",
        params: typing.Optional[Params] = None,
    ) -> None:
        """Initialize functor."""
        if params is None:
            params = Params()
        self._params = params

    def __call__(self: "ApplySpringsDiagDesc", state: State) -> None:
        """Calculate spring forces between pairs of cells along descending
        diagonals and apply to State velocity."""
        # how far apart are pairs of cells along descending diagonals?
        diag_dists_horiz = state.px[:-1, 1:] - state.px[1:, :-1]
        diag_dists_vert = state.py[:-1, 1:] - state.py[1:, :-1]
        diag_dists = np.sqrt(diag_dists_horiz**2 + diag_dists_vert**2)

        # decomposed unit vector
        normed_diag_dists_horiz = diag_dists_horiz / diag_dists
        normed_diag_dists_vert = diag_dists_vert / diag_dists

        # net forces: negative is repulsion, positive is attraction
        l_naught = np.sqrt(2)  # natural length of springs, on diagonal
        f = self._params.k * (diag_dists - l_naught)

        # decompose force into horizontal and vertical components
        fx = f * normed_diag_dists_horiz
        fy = f * normed_diag_dists_vert

        # is clipping necessary?
        # fx = np.clip(fx, -1e12, 1e12)
        # fy = np.clip(fy, -1e12, 1e12)

        # horizontal components of acceleration
        ax = np.zeros_like(state.vx)
        ax[:-1, 1:] -= fx[:, :]  # up-left facing forces
        ax[1:, :-1] += fx[:, :]  # down-right facing forces
        # apply acceleration to state
        state.vx += ax * self._params.dt

        # vertical components of acceleration
        ay = np.zeros_like(state.vy)
        ay[:-1, 1:] -= fy[:, :]  # up-left facing forces
        ay[1:, :-1] += fy[:, :]  # down-right facing forces
        # apply acceleration to state
        state.vy += ay * self._params.dt
