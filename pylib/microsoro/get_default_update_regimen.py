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
    """Lists core simulation components as ordered, callable objects.

    Parameters
    ----------
    params : Params, optional
        Configuration parameters for the update regimen. If not provided,
        a default `Params` instance will be used.

    Returns
    -------
    list[typing.Callable]
        List of callable components that make up the default update regimen.

    Notes
    -----
    Does not include any halting component to terminate simulation. Users
    should append an appropriate halting component for their application.
    """
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
