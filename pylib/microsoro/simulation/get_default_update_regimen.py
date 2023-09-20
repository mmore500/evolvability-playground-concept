import typing

from ..Params import Params
from ..Structure import Structure
from .. import components


def get_default_update_regimen(
    params: typing.Optional[Params] = None,
    structure: typing.Optional[Structure] = None,
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
    if structure is None:
        structure = Structure(params=params)

    return [
        components.ClearEventBuffer(),  # 1st (not last) so handle events after
        components.ApplyGravity(params),
        components.ApplySpringsCol(params, structure),
        components.ApplySpringsRow(params, structure),
        components.ApplySpringsDiagAsc(params, structure),
        components.ApplySpringsDiagDesc(params, structure),
        components.ApplySpringDampingCol(params, structure),
        components.ApplySpringDampingRow(params, structure),
        components.ApplyVelocity(params),
        components.ApplyFloorBounce(),
        components.ApplyIncrementElapsedTime(params),
    ]
