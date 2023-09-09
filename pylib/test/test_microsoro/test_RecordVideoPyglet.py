import contextlib
import os

import pytest

from pylib.microsoro import State
from pylib.microsoro.conditioners import ApplySpin, ApplyPropel
from pylib.microsoro.components import ApplyVelocity, RecordVideoPyglet


@pytest.mark.heavy
def test_RecordVideoPyglet():
    outpath = "/tmp/test_RecordVideoPyglet.mp4"
    with contextlib.suppress(FileNotFoundError):
        os.remove(outpath)

    state = State()
    ApplySpin(omega=1.0)(state)
    ApplyPropel(dvx=0.5, dvy=1.0)(state)

    record_video_component = RecordVideoPyglet(outpath)
    apply_velocity_component = ApplyVelocity()
    record_video_component(state)
    for _frame in range(1000):
        apply_velocity_component(state)
        record_video_component(state)

    print(f"saved test_RecordVideoPyglet render to file {outpath}")
