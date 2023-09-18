import numpy as np

from ...State import State


class ApplyTranslate:
    """Adjust position."""

    _dpx: float
    _dpy: float

    def __init__(
        self: "ApplyTranslate", dpx: float = 0.0, dpy: float = 0.0
    ) -> None:
        self._dpx = dpx
        self._dpy = dpy

    def __call__(self: "ApplyTranslate", state: State) -> None:
        state.px += self._dpx
        state.py += self._dpy
