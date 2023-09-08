import typing

from .Params import Params
from .components import (
    ApplyGravity,
    ApplyVelocity,
    ApplyIncrementElapsedTime,
)


def get_default_update_regimen(
    params: typing.Optional[Params] = None,
) -> typing.List[typing.Callable]:

    if params is None:
        params = Params()

    return [
        ApplyGravity(params),
        # TODO apply_springs_col
        # TODO apply_springs_row
        # TODO apply_springs_diag_asc
        # TODO apply_springs_diag_desc
        # TODO apply_floor_bounce_naive
        ApplyVelocity(params),
        ApplyIncrementElapsedTime(params),
    ]
