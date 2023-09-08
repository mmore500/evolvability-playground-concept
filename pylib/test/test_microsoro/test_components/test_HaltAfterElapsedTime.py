from pylib.microsoro import State
from pylib.microsoro.components import HaltAfterElapsedTime


def test_HaltAfterElapsedTime():

    state = State()
    HaltAfterElapsedTime(15.0)(state) is None

    state.t = 14.5
    HaltAfterElapsedTime(15.0)(state) is state

    state.t = 16.5
    HaltAfterElapsedTime(15.0)(state) is state
