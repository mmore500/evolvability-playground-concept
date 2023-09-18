import numpy as np
import typing

from ...State import State


class ApplyStretch:
    """Gather or spread cell positions by a constnt factor."""

    _how: typing.Literal["sym", "pos", "neg"]
    _mx: float
    _my: float

    def __init__(
        self: "ApplyStretch",
        mx: float = 1.0,
        my: float = 1.0,
        how: typing.Literal["sym", "pos", "neg"] = "sym",
    ) -> None:
        """Initialize functor.

        `mx` and `my` values less than one will gather cells along respective
        axes; values greater than one will spread cells along respective axes.
        """
        self._how = how
        self._mx = mx
        self._my = my

    def __call__(self: "ApplyStretch", state: State) -> None:
        """Apply stretch to State."""
        # Compute the center of stretch
        how = self._how
        if how == "sym":
            refx = (state.px.max() + state.px.min()) / 2.0
            refy = (state.py.max() + state.py.min()) / 2.0
        elif how == "pos":
            refx, refy = state.px.min(), state.py.min()
        elif how == "neg":
            refx, refy = state.px.max(), state.py.max()
        else:
            raise ValueError(f"bad ApplyStretch config {how=}")

        # Apply stretch
        state.px = self._mx * (state.px - refx) + refx
        state.py = self._my * (state.py - refy) + refy
