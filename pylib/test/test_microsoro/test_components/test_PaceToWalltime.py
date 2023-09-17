import datetime
from unittest.mock import Mock, patch
import typing

from freezegun import freeze_time
import pytest

from pylib.microsoro import Params, State
from pylib.microsoro.components import PaceToWalltime
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[EventBuffer(), None])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture
def params_dt_1sec() -> Params:
    params = Params()
    params.dt = 1.0
    return params


@pytest.fixture
def state() -> State:
    return State()


def test_init_defaults():
    assert PaceToWalltime()._params == Params()
    assert PaceToWalltime()._until_time is None
    assert PaceToWalltime()._allow_catchup in (True, False)


def test_init_params():
    params = Params()
    params.dt = 42.0
    assert PaceToWalltime(params=params)._params.dt == 42.0


def test_init_catchup():
    assert PaceToWalltime(allow_catchup=True)._allow_catchup
    assert not PaceToWalltime(allow_catchup=False)._allow_catchup


@freeze_time(datetime.datetime(year=2023, month=1, day=1))
def test_call_first_time(
    event_buffer: typing.Optional[EventBuffer],
    params_dt_1sec: Params,
    state: State,
):
    functor = PaceToWalltime(params_dt_1sec)

    with patch(
        "pylib.microsoro.components.PaceToWalltime_.pause.until",
    ) as mocked_pause:
        onesec = datetime.timedelta(seconds=1.0)
        # note that time is frozen
        expected_until_time = datetime.datetime.now() + onesec

        functor(state, event_buffer)

        mocked_pause.assert_called_with(datetime.datetime.now())
        assert functor._until_time == expected_until_time


@freeze_time(datetime.datetime(year=2023, month=1, day=1))
def test_call_not_first_time_without_catchup(
    event_buffer: typing.Optional[EventBuffer],
    params_dt_1sec: Params,
    state: State,
):
    functor = PaceToWalltime(params=params_dt_1sec, allow_catchup=False)
    functor._until_time = datetime.datetime(2023, 2, 2)

    with patch(
        "pylib.microsoro.components.PaceToWalltime_.pause.until",
    ) as mocked_pause:
        onesec = datetime.timedelta(seconds=1.0)
        # note that time is frozen
        expected_until_time = datetime.datetime.now() + onesec

        res = functor(state, event_buffer)
        assert res is None

        mocked_pause.assert_called_with(datetime.datetime(2023, 2, 2))
        assert functor._until_time == expected_until_time


@freeze_time(datetime.datetime(year=2023, month=1, day=1))
def test_call_not_first_time_with_catchup(
    event_buffer: typing.Optional[EventBuffer],
    params_dt_1sec: Params,
    state: State,
):
    functor = PaceToWalltime(params=params_dt_1sec, allow_catchup=True)
    functor._until_time = datetime.datetime(2023, 2, 2)

    with patch(
        "pylib.microsoro.components.PaceToWalltime_.pause.until",
    ) as mocked_pause:
        onesec = datetime.timedelta(seconds=1.0)
        expected_until_time = datetime.datetime(2023, 2, 2) + onesec

        res = functor(state, event_buffer)
        assert res is None

        mocked_pause.assert_called_with(datetime.datetime(2023, 2, 2))
        assert functor._until_time == expected_until_time
