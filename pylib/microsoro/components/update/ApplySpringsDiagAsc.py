import typing

import numpy as np

from ...State import State
from ...Structure import Structure
from ...Params import Params


class ApplySpringsDiagAsc:
    """Simulate action of springs between pairs of cells along ascending
    diagonals."""

    _params: Params
    _structure: Structure

    def __init__(
        self: "ApplySpringsDiagAsc",
        params: typing.Optional[Params] = None,
        structure: typing.Optional[Structure] = None,
    ) -> None:
        """Initialize functor."""
        if params is None:
            params = Params()
        self._params = params
        if structure is None:
            structure = Structure(params=params)
        self._structure = structure

    def __call__(
        self: "ApplySpringsDiagAsc",
        state: State,
        event_buffer: typing.Optional = None,
    ) -> None:
        """Calculate spring forces between pairs of cells along ascending
        diagonals and apply to State velocity."""
        # how far apart are pairs of cells along ascending diagonals?
        diag_dists_horiz = state.px[:-1, :-1] - state.px[1:, 1:]
        diag_dists_vert = state.py[:-1, :-1] - state.py[1:, 1:]
        diag_dists = np.sqrt(diag_dists_horiz**2 + diag_dists_vert**2)

        # decomposed unit vector
        normed_diag_dists_horiz = diag_dists_horiz / diag_dists
        normed_diag_dists_vert = diag_dists_vert / diag_dists

        # net forces: negative is repulsion, positive is attraction
        l_naught = self._structure.la  # natural len of springs, on diagonal
        f = self._structure.ka * (diag_dists - l_naught)

        # decompose force into horizontal and vertical components
        fx = f * normed_diag_dists_horiz
        fy = f * normed_diag_dists_vert

        # is clipping necessary?
        # fx = np.clip(fx, -1e12, 1e12)
        # fy = np.clip(fy, -1e12, 1e12)

        # horizontal components of acceleration
        ax = np.zeros_like(state.vx)
        ax[:-1, :-1] -= fx[:, :]  # up-right facing forces
        ax[1:, 1:] += fx[:, :]  # down-left facing forces
        ax /= self._structure.m
        # apply acceleration to state
        state.vx += ax * self._params.dt

        # vertical components of acceleration
        ay = np.zeros_like(state.vy)
        ay[:-1, :-1] -= fy[:, :]  # up-right facing forces
        ay[1:, 1:] += fy[:, :]  # down-left facing forces
        ay /= self._structure.m
        # apply acceleration to state
        state.vy += ay * self._params.dt
