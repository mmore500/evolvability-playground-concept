import datetime
import typing

import pause

from ..Params import Params
from ..State import State


class PaceToWalltime:
    """Ensures simulation time proceeds no faster than realtime."""

    _allow_catchup: bool
    _params: Params
    _until_time: typing.Optional[datetime.datetime]

    def __init__(
        self: "RecordVideoPyglet",
        params: typing.Optional[Params] = None,
        allow_catchup: bool = False,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        params : Params, optional
            What is the simulation time delta between update steps?

            Defaults to default-initialized Params.
        allow_catchup : bool, default False
            Should faster-than-realtime updates be allowed if simulation has
            fallen behind realtime pace?
        """
        if params is None:
            params = Params()
        self._params = params

        self._allow_catchup = allow_catchup
        self._until_time = None

    def __call__(self: "RecordVideoPyglet", __: State) -> None:
        """If necessary, delay simulation to maintain realtime pace."""
        if self._until_time is None:
            self._until_time = datetime.datetime.now()

        pause.until(self._until_time)

        now = datetime.datetime.now
        from_time = self._until_time if self._allow_catchup else now()
        dt = datetime.timedelta(seconds=self._params.dt)
        self._until_time = from_time + dt
