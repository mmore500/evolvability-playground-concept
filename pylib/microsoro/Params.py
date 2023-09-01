import typing

import numpy as np


class Params:

    # b: float  # damping constant
    dt: float  # simulation time step
    g: float  # gravitational constant
    k: float  # spring constant
    m: float  # cell mass

    def __init__(
        self: "Params",
        *,
        # b: float = ?,
        dt: float = 0.001,
        g: float = 10.0,
        k: float = 1000.0,
        m: float = 1.0,
    ) -> None:
        assert dt > 0
        self.dt = dt

        assert g > 0
        self.g = g

        assert k > 0
        self.k = k

        assert m > 0
        self.m = m
