import pause
import pytest

from pylib.microsoro import State, Style
from pylib.microsoro.conditioners import ApplySpin, ApplyPropel
from pylib.microsoro.components import (
    ApplyIncrementElapsedTime,
    ApplyVelocity,
    PaceToWalltime,
    ShowAnimationIpycanvas,
)


# stub test, ipycanvas does nothing outside notebook contextext
def test_ShowAnimationIpycanvas():
    state = State()
    ApplySpin(omega_degrees=90.0)(state)
    ApplyPropel(dvx=0.5, dvy=1.0)(state)

    style = Style(time_dilation=5.0)
    show_animation_component = ShowAnimationIpycanvas()
    pace_walltime_component = PaceToWalltime()
    apply_velocity_component = ApplyVelocity()
    incr_time_component = ApplyIncrementElapsedTime()
    res = show_animation_component(state)
    assert res is None
    for _frame in range(100):
        apply_velocity_component(state)
        res = show_animation_component(state)
        assert res is None
        pace_walltime_component(state)
        incr_time_component(state)
