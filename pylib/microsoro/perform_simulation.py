import typing

from iterpop import iterpop as ip

from .components import HaltAfterElapsedTime
from .conditioners import ApplyTranslate
from .get_default_update_regimen import get_default_update_regimen

from .State import State


def perform_simulation(
    setup_regimen_conditioners: typing.Optional[
        typing.List[typing.Callable]
    ] = None,
    update_regimen_components: typing.Optional[
        typing.List[typing.Callable]
    ] = None,
    yield_intermediate_states: bool = False,
) -> typing.Union[State, typing.Any, typing.Iterator]:
    """Perform simulation through composition of callable ingredients.

    Applies a sequence of State setup steps ("conditioners") and then enters an
    update loop to repeatedly apply a sequence State update steps
    ("components"). Termination occurs at the first simulation update component
    execution to return a non-None value. This value, typically ending State,
    is forwarded out as `perform_simulation`'s return value.

    Parameters
    ----------
    setup_regimen_conditioners : list[Callable], optional
        Sequence of callable conditioners to set up the initial state of the
        simulation.

        These conditioners are called only once, before the main siimulation loop. If not specified, default behavior will apply a translation of
        `dpy=-5.0`.

    update_regimen_components : list[Callable], optional
        Sequence of callable components or string identifiers to be applied to
        simulation state each update loop.

        Defaults to a `get_default_update_regimen()` components, halting after 10 seconds of simulation time. User-specified regimens should include
        at least one halting component --- otherwise, simulation will not end.

    yield_intermediate_states : bool, default False
        Should intermediate state instances be yielded from the simulation loop? Defaults to False.

    Returns
    -------
    State, Any, Iterator
        Returns the final state after the simulation ends. If
        `yield_intermediate_states` is set, instead iterates over sequential simulation states from each update step.

    Examples
    --------
    >>> final_state = perform_simulation(
        update_regimen_components = [
            *get_default_update_regimen(),
            HaltAfterElapsedTime(42.0),
        ],
    )
    >>> final_state.t
    42.0

    """

    # setup defaults as necessary
    if setup_regimen_conditioners is None:
        setup_regimen_conditioners = [ApplyTranslate(dpy=-5.0)]

    if update_regimen_components is None:
        update_regimen_components = [
            *get_default_update_regimen(),
            HaltAfterElapsedTime(10.0),
        ]

    state = State()

    # perform setup using conditioner regimen
    for conditioner in setup_regimen_conditioners:
        conditioner(state)

    # perform simulation, looping until a component returns non-None
    def do_run() -> typing.Iterable:
        while True:
            for component in update_regimen_components:
                res = component(state)
                if res is not None:
                    yield res
                    return
            if yield_intermediate_states:
                yield state

    if yield_intermediate_states:
        return do_run()
    else:
        return ip.popsingleton(do_run())
