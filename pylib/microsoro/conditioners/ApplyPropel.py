import numpy as np

from ..State import State


class ApplyPropel:
    """Adjust velocities to impart translational momentum."""

    _dvx: float
    _dvy: float

    def __init__(
        self: "ApplyPropel", dvx: float = 0.0, dvy: float = 0.0
    ) -> None:
        self._dvx = dvx
        self._dvy = dvy

    def __call__(self: "ApplyPropel", state: State) -> None:
        state.vx += self._dvx
        state.vy += self._dvy
