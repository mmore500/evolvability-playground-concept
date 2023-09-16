import contextlib
import os

import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplySpin, ApplyPropel
from pylib.microsoro.components import (
    ApplyIncrementElapsedTime,
    ApplyVelocity,
    RecordVideoPyglet,
)


@pytest.mark.heavy
def test_RecordVideoPyglet():
    outpath = "/tmp/test_RecordVideoPyglet.mp4"
    with contextlib.suppress(FileNotFoundError):
        os.remove(outpath)

    state = State()
    ApplySpin(omega_degrees=90.0)(state)
    ApplyPropel(dvx=0.5, dvy=1.0)(state)

    record_video_component = RecordVideoPyglet(outpath)
    apply_velocity_component = ApplyVelocity()
    apply_increment_elapsed_time_component = ApplyIncrementElapsedTime()
    res = record_video_component(state)
    assert res is None
    for _frame in range(1000):
        apply_increment_elapsed_time_component(state)
        apply_velocity_component(state)
        res = record_video_component(state)
        assert res is None

    print(f"saved test_RecordVideoPyglet render to file {outpath}")
