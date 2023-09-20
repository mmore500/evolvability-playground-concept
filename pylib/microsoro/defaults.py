import math
import typing
import sys


# spring damping
b: float = 1e1
b_lim: typing.Tuple[float, float] = (0.0, 1e2)

# simulation timestep
dt: float = 1e-3
dt_lim: typing.Tuple[float, float] = (sys.float_info.min, sys.float_info.max)

# gravitational constant
g: float = 1e1
g_lim: typing.Tuple[float, float] = (0, sys.float_info.max)

# spring stiffness
k: float = 1e4
k_lim: typing.Tuple[float, float] = (1e3, 1e4)

# spring natural length
l: float = 1.0
l_lim: typing.Tuple[float, float] = (0.0, 2.0)

# spring natural length, diagonally
def l_diag() -> float:
    return math.sqrt(2 * l**2)


def l_lim_diag() -> typing.Tuple[float, float]:
    l1, l2 = l_lim
    return (math.sqrt(2 * l1**2), math.sqrt(2 * l2**2))


# mass
m: float = 1.0
m_lim: typing.Tuple[float, float] = (1e-1, 1e1)

# cell matrix width
ncol: int = 8
ncol_lim: typing.Tuple[int, int] = (1, sys.maxsize)

# cell matrix height
nrow: int = 8
nrow_lim: typing.Tuple[int, int] = (1, sys.maxsize)
