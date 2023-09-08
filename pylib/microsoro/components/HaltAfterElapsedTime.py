import typing

from ..State import State
from ..Params import Params


class HaltAfterElapsedTime:

    _target_duration: float

    def __init__(self: "HaltAfterElapsedTime", target_duration: float = 10.0):
        if target_duration < 0.0:
            raise ValueError(f"{target_duration=} is negative")
        self._target_duration = target_duration

    def __call__(
        self: "HaltAfterElapsedTime",
        state: State,
    ) -> typing.Optional[State]:
        return state if state.t > self._target_duration else None
