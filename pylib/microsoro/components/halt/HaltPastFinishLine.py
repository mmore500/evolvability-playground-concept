import typing

import numpy as np

from ...events import EventBuffer, RenderThresholdEvent
from ...State import State
from ...Params import Params


class HaltPastFinishLine:
    """Inspects state and triggers simulation halt by returning non-None value
    when cell positions pass a threshold."""

    _m: float
    _b: float
    _independent_axis: typing.Literal["horizontal", "vertical"]
    _comparator: typing.Callable

    def __init__(
        self: "HaltPastFinishLine",
        m: float = 0.0,
        b: float = 10.0,
        independent_axis: typing.Literal[
            "horizontal", "vertical"
        ] = "vertical",
        comparator: typing.Optional[typing.Callable] = None,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        m : float, default 0.0
            Slope of the finish line.
        b : float, default 10.0
            Intercept of the finish line, by default 10.0.
        independent_axis : typing.Literal["horizontal", "vertical"], optional
            Axis considered as independent axis in the equation, by default
            "vertical".
        comparator : typing.Callable, optional
            Comparator between positions and finish line thresholds used to
            decide termination.

            Default np.any(np.greater(a, b)) if independent_axis is
            "horizontal" and default np.any(np.less(a, b)) if independent axis
            is "vertical".

            To terminate when all cells are past finish line, use `np.all`. To
            terminate when cells go below the finish line (with respect to the
            dependent axis), use `np.less`.
        """
        self._m = m
        self._b = b

        if independent_axis not in ("horizontal", "vertical"):
            raise ValueError(
                f"{independent_axis=} should be 'horizontal' or 'vertical'.",
            )

        self._independent_axis = independent_axis
        if comparator is None:
            comparator = {
                "vertical": lambda a, b: np.any(np.greater(a, b)),
                "horizontal": lambda a, b: np.any(np.less(a, b)),
            }[independent_axis]
        self._comparator = comparator

    def __call__(
        self: "HaltPastFinishLine",
        state: State,
        event_buffer: typing.Optional = None,
    ) -> typing.Optional[State]:
        """Check if cell positions within state are past the finish line.

        Parameters
        ----------
        state : State
            The current state to be evaluated.
        event_buffer : typing.Optional, optional
            Event buffer for recording events, by default None.

        Returns
        -------
        typing.Optional[State]
            The state if cells cross the finish line, None otherwise.
        """

        independent_axis = self._independent_axis
        comparator, m, b = self._comparator, self._m, self._b

        if event_buffer is not None:
            event_buffer.enqueue(
                RenderThresholdEvent(
                    m=m,
                    b=b,
                    independent_axis=independent_axis,
                    flavor="finish",
                ),
            )

        independent_positions, dependent_positions = {
            "vertical": (state.py, state.px),
            "horizontal": (state.px, state.py),
        }[independent_axis]

        threshold_positions = m * independent_positions + b
        if comparator(dependent_positions, threshold_positions):
            return state
        else:
            return None
