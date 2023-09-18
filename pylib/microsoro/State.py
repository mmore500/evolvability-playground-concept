import numpy as np


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

    def __init__(self: "State", height: int = 8, width: int = 8) -> None:
        self.px = np.tile(np.linspace(0, float(width - 1), width), (height, 1))
        self.py = np.tile(
            np.linspace(0, float(height - 1), height), (width, 1)
        ).T

        self.vx = np.zeros((height, width))
        self.vy = np.zeros((height, width))

        # self.pe = np.zeros((height, width))

        self.t = 0.0

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
