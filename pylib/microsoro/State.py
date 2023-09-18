import typing

import numpy as np

from . import defaults


class State:

    # position
    px: np.ndarray
    py: np.ndarray

    # velocity
    vx: np.ndarray
    vy: np.ndarray

    # potential energy
    # pe: np.ndarray

    # elapsed time
    t: float

    def __init__(
        self: "State",
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
    ) -> None:
        if height is None:
            height = defaults.nrow
        if not np.clip(height, *defaults.nrow_lim) == height:
            raise ValueError(
                f"value {height=} not within limits {defaults.nrow_lim}",
            )

        if width is None:
            width = defaults.ncol
        if not np.clip(width, *defaults.ncol_lim) == width:
            raise ValueError(
                f"value {width=} not within limits {defaults.ncol_lim}",
            )

        self.px = np.tile(np.linspace(0, float(width - 1), width), (height, 1))
        self.py = np.tile(
            np.linspace(0, float(height - 1), height), (width, 1)
        ).T

        self.vx = np.zeros((height, width))
        self.vy = np.zeros((height, width))

        # self.pe = np.zeros((height, width))

        self.t = 0.0

    def __eq__(self: "State", other: "State") -> bool:
        return (
            (type(self) == type(other))
            and np.array_equal(self.px, other.px, equal_nan=True)
            and np.array_equal(self.py, other.py, equal_nan=True)
            and np.array_equal(self.vx, other.vx, equal_nan=True)
            and np.array_equal(self.vy, other.vy, equal_nan=True)
            and (self.t == other.t)
        )

    @property
    def ncells(self: "State") -> int:
        return self.px.size

    def validate(self: "State") -> bool:
        return (
            not np.any(np.isnan(self.px))
            and not np.any(np.isnan(self.py))
            and not np.any(np.isnan(self.vx))
            and not np.any(np.isnan(self.vy))
            and not np.isnan(self.t)
            and self.t >= 0
        )

    def same_position_as(self: "State", other: "State") -> bool:
        return np.allclose(self.px, other.px, equal_nan=True) and np.allclose(
            self.py, other.py, equal_nan=True
        )

    def same_velocity_as(self: "State", other: "State") -> bool:
        return np.allclose(self.vx, other.vx, equal_nan=True) and np.allclose(
            self.vy, other.vy, equal_nan=True
        )
