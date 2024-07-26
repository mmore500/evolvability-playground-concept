import typing

import numpy as np
import zodiax as zdx

from . import defaults


class State(zdx.Base):

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
        *,
        px: np.ndarray,
        py: np.ndarray,
        vx: np.ndarray,
        vy: np.ndarray,
        t: float,
    ) -> None:
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.t = t

    def update(
        self: "State",
        **kwargs,
    ) -> None:
        return State(
            px=kwargs.get("px", self.px),
            py=kwargs.get("py", self.py),
            vx=kwargs.get("vx", self.vx),
            vy=kwargs.get("vy", self.vy),
            t=kwargs.get("t", self.t),
        )

    @staticmethod
    def make_starting(
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

        return State(
            px=np.tile(np.linspace(0, float(width - 1), width), (height, 1)),
            py=np.tile(np.linspace(0, float(height - 1), height), (width, 1)).T,
            vx=np.zeros((height, width)),
            vy=np.zeros((height, width)),
            t=0.0,
        )

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
