import copy
import typing

from iterpop import iterpop as ip
import numpy as np
import pytest

from pylib.microsoro import Params, State
from pylib.microsoro.components import ApplyVelocity
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


@pytest.mark.parametrize("vx", [-1, 0, 1])
@pytest.mark.parametrize("vy", [-1, 0, 1])
def test_update(event_buffer: typing.Optional[EventBuffer], vx: int, vy: int):
    state_ = State()
    state_.vx, state_.vy = vx, vy
    state1 = copy.deepcopy(state_)
    state2 = copy.deepcopy(state_)
    params1 = Params(dt=1.0)
    params2 = Params(dt=0.1)

    res = ApplyVelocity(params1)(state1, event_buffer)
    assert res is None
    res = ApplyVelocity(params2)(state2, event_buffer)
    assert res is None

    assert np.sign(vx) == ip.pophomogeneous(
        np.sign(state1.px - state_.px).flat
    )
    assert np.sign(vy) == ip.pophomogeneous(
        np.sign(state1.py - state_.py).flat
    )
    assert np.sign(vx) == ip.pophomogeneous(
        np.sign(state2.px - state_.px).flat
    )
    assert np.sign(vy) == ip.pophomogeneous(
        np.sign(state2.py - state_.py).flat
    )

    if vx:
        assert (abs(state2.px - state_.px) < abs(state1.px - state_.px)).all()
    if vy:
        assert (abs(state2.py - state_.py) < abs(state1.py - state_.py)).all()


def test_ApplyVelocity_default_ctor():
    assert ApplyVelocity()._params == Params()
