import copy
import typing

import numpy as np
import pytest

from pylib.microsoro import components, conditioners, Params, State


@pytest.mark.parametrize(
    "conditioner",
    [
        conditioners.ApplyPropel(dvx=1.0),
        conditioners.ApplyPropel(dvx=1.0, dvy=2.0),
        conditioners.BundleConditioners(
            conditioners.ApplyPropel(dvy=2.0),
            conditioners.ApplyRotate(),
            conditioners.ApplyDeflect(),
        ),
        conditioners.BundleConditioners(
            conditioners.ApplyTorsion(),
            conditioners.ApplySpin(),
        ),
        conditioners.ApplySpin(),
    ],
)
@pytest.mark.parametrize("m", [-5.0, 0.0, 3.0, 100.0])
@pytest.mark.parametrize("b", [-5.0, 0.0, 0.5, 1.0])
@pytest.mark.parametrize("mu", [0.0, 1.0, 10.0])
@pytest.mark.parametrize("dt", [0.001, 0.0001])
def test_interaction(
    conditioner: typing.Callable,
    m: float,
    b: float,
    mu: float,
    dt: float,
) -> None:

    state = State()
    conditioner(state)
    prestate = copy.deepcopy(state)

    params = Params(dt=dt)
    ftor = components.ApplyViscousLayer(m=m, b=b, mu=mu, params=params)
    res = ftor(state)
    assert res is None

    mask = state.py < state.px * m + b
    assert np.allclose(
        state.vx[mask].flatten(), prestate.vx[mask].flatten() * (1.0 - mu * dt)
    )
    assert np.allclose(
        state.vy[mask].flatten(), prestate.vy[mask].flatten() * (1.0 - mu * dt)
    )
    assert np.allclose(state.vx[~mask].flatten(), prestate.vx[~mask].flatten())
    assert np.allclose(state.vy[~mask].flatten(), prestate.vy[~mask].flatten())
