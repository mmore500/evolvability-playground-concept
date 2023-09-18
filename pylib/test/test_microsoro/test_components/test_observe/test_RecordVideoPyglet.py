import contextlib
import os
import typing

import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplySpin, ApplyPropel
from pylib.microsoro.components import (
    ApplyFloorBounce,
    ApplyIncrementElapsedTime,
    ApplyVelocity,
    RecordVideoPyglet,
)
from pylib.microsoro.events import EventBuffer


@pytest.fixture(params=[None, EventBuffer()])
def event_buffer(request: pytest.FixtureRequest):
    return request.param


@pytest.mark.heavy
def test_RecordVideoPyglet(event_buffer: typing.Optional[EventBuffer]):
    outpath = f"/tmp/test_RecordVideoPyglet{int(event_buffer is None)}.mp4"
    with contextlib.suppress(FileNotFoundError):
        os.remove(outpath)

    state = State()
    ApplySpin(omega_degrees=90.0)(state)
    ApplyPropel(dvx=0.5, dvy=1.0)(state)

    record_video_component = RecordVideoPyglet(outpath)
    apply_velocity_component = ApplyVelocity()
    apply_increment_elapsed_time_component = ApplyIncrementElapsedTime()
    apply_floor_bounce_component = ApplyFloorBounce(b=1.0)
    res = record_video_component(state)
    assert res is None
    for _frame in range(1000):
        apply_increment_elapsed_time_component(state)
        apply_velocity_component(state)
        apply_floor_bounce_component(state, event_buffer)
        res = record_video_component(state, event_buffer)
        assert res is None

    print(f"saved test_RecordVideoPyglet render to file {outpath}")
