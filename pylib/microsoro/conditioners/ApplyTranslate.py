import numpy as np

from ..State import State


class ApplyTranslate:
    """Adjust position."""

    _dx: float
    _dy: float

    def __init__(self: "ApplySpin", dx: float = 0.0, dy: float = 0.0) -> None:
        self._dx = dx
        self._dy = dy

    def __call__(self: "ApplySpin", state: State) -> None:
        state.px += self._dx
        state.py += self._dy
