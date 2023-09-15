import pause
import pytest

from pylib.microsoro import State, Style
from pylib.microsoro.conditioners import ApplySpin, ApplyPropel
from pylib.microsoro.components import (
    ApplyIncrementElapsedTime,
    ApplyVelocity,
    PaceToWalltime,
    ShowAnimationPygletAsync,
)


@pytest.mark.skip(reason="broken --- second launched subprocess crashes")
def test_ShowAnimationPygletAsync():
    state = State()
    ApplySpin(omega=1.0)(state)
    ApplyPropel(dvx=0.5, dvy=1.0)(state)

    style = Style(time_dilation=5.0)
    show_animation_component = ShowAnimationPygletAsync()
    pace_walltime_component = PaceToWalltime()
    apply_velocity_component = ApplyVelocity()
    incr_time_component = ApplyIncrementElapsedTime()
    res = show_animation_component(state)
    assert res is None
    for _frame in range(10000):
        apply_velocity_component(state)
        show_animation_component(state)
        pace_walltime_component(state)
        incr_time_component(state)


@pytest.mark.skip(reason="broken --- second launched subprocess crashes")
def test_ShowAnimationPygletAsync_slow():
    state = State()
    ApplySpin(omega=1.0)(state)
    ApplyPropel(dvx=0.5, dvy=1.0)(state)

    style = Style(time_dilation=5.0)
    show_animation_component = ShowAnimationPygletAsync()
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
        pause.seconds(0.1)

    del show_animation_component
