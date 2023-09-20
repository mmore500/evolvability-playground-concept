import copy
import typing

from hstrat import _auxiliary_lib as hstrat_aux
import numpy as np
import pytest

from pylib.microsoro import components, conditioners, Params, State
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


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


@pytest.mark.parametrize(
    "conditioner",
    [
        conditioners.ApplySpin(),
        conditioners.ApplyPropel(dvx=1.0),
        conditioners.ApplyPropel(dvy=1.0),
        conditioners.ApplyPropel(dvx=1.0, dvy=1.0),
    ],
)
def test_param_m(
    conditioner: typing.Callable, event_buffer: typing.Optional[EventBuffer]
):
    sum_speeds = []
    for m in range(1, 10):
        state = State()
        conditioner(state)
        prespeeds = np.sqrt(state.vx**2 + state.vy**2)
        assert np.sum(prespeeds) > 0

        params = Params()
        params.m = float(m)
        res = components.ApplyViscousLayer(
            m=0.0,  # slope, not mass
            b=1e9,
            mu=1.0,
            params=params,
        )(state, event_buffer)
        assert res is None

        speeds = np.sqrt(state.vx**2 + state.vy**2)
        assert np.sum(speeds) > 0

        assert np.sum(speeds) < np.sum(prespeeds)  # should decelerate
        sum_speeds.append(np.sum(speeds))

    # shouldn't all be equivalent
    assert not np.allclose(sum_speeds, sum_speeds[0])

    # should be in increasing order as m is added
    assert hstrat_aux.is_strictly_increasing(sum_speeds)
