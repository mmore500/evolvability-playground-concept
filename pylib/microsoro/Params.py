import typing

import numpy as np


class Params:

    b: float  # spring damping constant
    dt: float  # simulation time step
    g: float  # gravitational constant
    k: float  # spring constant
    m: float  # cell mass
    s: float  # floor slope

    def __init__(
        self: "Params",
        *,
        b: float = 1.0,
        dt: float = 0.001,
        g: float = 10.0,
        k: float = 10000.0,
        m: float = 1.0,
        s: float = 0.0,
    ) -> None:
        assert 0 <= b
        self.b = b

        assert dt > 0
        self.dt = dt

        assert g > 0
        self.g = g

        assert k > 0
        self.k = k

        assert m > 0
        self.m = m

    def __eq__(self: "Params", other: "Params") -> bool:
        return type(self) == type(other) and self.__dict__ == other.__dict__
