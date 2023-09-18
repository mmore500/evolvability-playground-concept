import typing

from ...events import EventBuffer
from ...State import State


class BundleConditioners:
    """Package simulation conditioners together for sequential application."""

    _conditioners: typing.List[typing.Callable]

    def __init__(self: "BundleConditioners", *conditioners) -> None:
        """Initialize functor with sequence of simulation conditionerss."""
        self._conditioners = conditioners

    def __call__(self: "BundleConditioners", state: State) -> None:
        """Apply conditioner sequence."""
        for conditioner in self._conditioners:
            conditioner(state)
