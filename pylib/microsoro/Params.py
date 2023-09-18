import typing

import numpy as np

from . import defaults


class Params:

    b: float  # spring damping constant
    dt: float  # simulation time step
    g: float  # gravitational constant
    k: float  # spring constant
    m: float  # cell mass

    def __init__(
        self: "Params",
        *,
        b: typing.Optional[float] = None,
        dt: typing.Optional[float] = None,
        g: typing.Optional[float] = None,
        k: typing.Optional[float] = None,
        m: typing.Optional[float] = None,
    ) -> None:
        if b is None:
            b = defaults.b
        if not np.clip(b, *defaults.b_lim) == b:
            raise ValueError(f"value {b=} not within limits {defaults.b_lim}")
        self.b = b

        if dt is None:
            dt = defaults.dt
        if not np.clip(dt, *defaults.dt_lim) == dt:
            raise ValueError(
                f"value {dt=} not within limits {defaults.dt_lim}"
            )
        self.dt = dt

        if g is None:
            g = defaults.g
        if not np.clip(g, *defaults.g_lim) == g:
            raise ValueError(f"value {g=} not within limits {defaults.g_lim}")
        self.g = g

        if k is None:
            k = defaults.k
        if not np.clip(k, *defaults.k_lim) == k:
            raise ValueError(f"value {k=} not within limits {defaults.k_lim}")
        self.k = k

        if m is None:
            m = defaults.m
        if not np.clip(m, *defaults.dt_lim) == m:
            raise ValueError(f"value {m=} not within limits {defaults.m_lim}")
        self.m = m

    def __eq__(self: "Params", other: "Params") -> bool:
        return type(self) == type(other) and self.__dict__ == other.__dict__
