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

    def __init__(self: "State", height: int = 8, width: int = 8) -> None:
        self.px = np.tile(np.linspace(0, float(width - 1), width), (height, 1))
        self.py = np.tile(
            np.linspace(0, float(height - 1), height), (width, 1)
        ).T

        self.vx = np.zeros((height, width))
        self.vy = np.zeros((height, width))

        # self.pe = np.zeros((height, width))

    @property
    def ncells(self: "State") -> int:
        return self.px.size
