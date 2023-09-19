import typing

import numpy as np

from . import defaults


class Params:

    b: float  # spring damping constant
    b_lim: typing.Tuple[float, float]
    dt: float  # simulation time step
    dt_lim: typing.Tuple[float, float]
    g: float  # gravitational constant
    g_lim: typing.Tuple[float, float]
    k: float  # spring constant
    k_lim: typing.Tuple[float, float]
    l: float  # spring length
    l_lim: typing.Tuple[float, float]
    m: float  # cell mass
    m_lim: typing.Tuple[float, float]

    def __init__(
        self: "Params",
        *,
        b: typing.Optional[float] = None,
        b_lim: typing.Optional[typing.Tuple[float, float]] = None,
        dt: typing.Optional[float] = None,
        dt_lim: typing.Optional[typing.Tuple[float, float]] = None,
        g: typing.Optional[float] = None,
        g_lim: typing.Optional[typing.Tuple[float, float]] = None,
        k: typing.Optional[float] = None,
        k_lim: typing.Optional[typing.Tuple[float, float]] = None,
        l: typing.Optional[float] = None,
        l_lim: typing.Optional[typing.Tuple[float, float]] = None,
        m: typing.Optional[float] = None,
        m_lim: typing.Optional[typing.Tuple[float, float]] = None,
    ) -> None:
        if b_lim is None:
            b_lim = defaults.b_lim
        self.b_lim = b_lim

        if b is None:
            b = defaults.b
        if not np.clip(b, *b_lim) == b:
            raise ValueError(f"value {b=} not within limits {b_lim}")
        self.b = b

        if dt_lim is None:
            dt_lim = defaults.dt_lim
        self.dt_lim = dt_lim

        if dt is None:
            dt = defaults.dt
        if not np.clip(dt, *dt_lim) == dt:
            raise ValueError(f"value {dt=} not within limits {dt_lim}")
        self.dt = dt

        if g_lim is None:
            g_lim = defaults.g_lim
        self.g_lim = g_lim

        if g is None:
            g = defaults.g
        if not np.clip(g, *g_lim) == g:
            raise ValueError(f"value {g=} not within limits {g_lim}")
        self.g = g

        if k_lim is None:
            k_lim = defaults.k_lim
        self.k_lim = k_lim

        if k is None:
            k = defaults.k
        if not np.clip(k, *k_lim) == k:
            raise ValueError(f"value {k=} not within limits {k_lim}")
        self.k = k

        if l_lim is None:
            l_lim = defaults.l_lim
        self.l_lim = l_lim

        if l is None:
            l = defaults.l
        if not np.clip(l, *l_lim) == l:
            raise ValueError(f"value {l=} not within limits {l_lim}")
        self.l = l

        if m_lim is None:
            m_lim = defaults.m_lim
        self.m_lim = m_lim

        if m is None:
            m = defaults.m
        if not np.clip(m, *m_lim) == m:
            raise ValueError(f"value {m=} not within limits {m_lim}")
        self.m = m

    def __eq__(self: "Params", other: "Params") -> bool:
        return type(self) == type(other) and self.__dict__ == other.__dict__

    @property
    def l_diag(self: "Params") -> float:
        return np.sqrt(2 * self.l**2)
