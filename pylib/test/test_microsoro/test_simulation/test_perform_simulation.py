import pytest

from pylib.microsoro import defaults, Params, perform_simulation, State
from pylib.microsoro.conditioners import ApplyPropel, ApplySpin
from pylib.microsoro.components import (
    ApplyGravity,
    ApplyIncrementElapsedTime,
    ApplyVelocity,
    EvaluateDuration,
    HaltAfterElapsedTime,
)
from pylib.microsoro.events import EventBuffer


def test_perform_simulation_setup():
    state = perform_simulation(
        update_regimen_components=[
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(1.0),
        ],
    )
    assert state is not None


def test_perform_simulation_custom_setup():
    state1 = perform_simulation(
        setup_regimen_conditioners=[],
        update_regimen_components=[
            ApplyVelocity(),
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(1.0),
        ],
    )
    assert State.same_position_as(state1, State())

    state2 = perform_simulation(
        setup_regimen_conditioners=[ApplyPropel(dvx=1.0)],
        update_regimen_components=[
            ApplyVelocity(),
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(1.0),
        ],
    )
    assert not State.same_position_as(state1, state2), state1.__dict__


def test_perform_simulation_update():
    state = perform_simulation(setup_regimen_conditioners=[])
    assert not State.same_position_as(state, State())


def test_perform_simulation_custom_update():
    state1 = perform_simulation(
        setup_regimen_conditioners=[],
        update_regimen_components=[
            ApplyVelocity(),
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(1.0),
        ],
    )
    assert State.same_position_as(state1, State())

    state2 = perform_simulation(
        setup_regimen_conditioners=[],
        update_regimen_components=[
            ApplyGravity(),
            ApplyVelocity(),
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(1.0),
        ],
    )
    assert not State.same_position_as(state1, state2)


def test_perform_simulation_setup_and_update():
    state1 = perform_simulation(
        setup_regimen_conditioners=[ApplySpin(-1.0)],
        update_regimen_components=[
            ApplyVelocity(),
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(1.0),
        ],
    )
    assert not State.same_position_as(state1, State())

    state2 = perform_simulation(
        setup_regimen_conditioners=[ApplySpin(-1.0), ApplyPropel(dvy=2.0)],
        update_regimen_components=[
            ApplyVelocity(),
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(1.0),
        ],
    )
    assert not State.same_position_as(state2, State())
    assert not State.same_position_as(state1, state2)
    assert (state2.py > state1.py).all()
    assert not (state2.px > state1.px).all()
    assert not (state2.px < state1.px).all()


@pytest.mark.parametrize("target_duration", [1.0, 2.0])
def test_perform_simulation_halt(target_duration: float):
    state = perform_simulation(
        update_regimen_components=[
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(target_duration),
        ],
    )
    assert target_duration <= state.t <= target_duration + Params().dt
    assert not State.same_position_as(state, State())


def test_event_buffer_functionality():
    events = ["event1", "event2", 1]

    def event_enqueue_component(
        state: State, event_buffer: EventBuffer
    ) -> None:
        for event in events:
            event_buffer.enqueue(event)

    def event_consume_component(
        state: State, event_buffer: EventBuffer
    ) -> None:
        assert event_buffer._buffer == events + events
        event_buffer.consume(str, lambda e: None)

    def event_reset_component(state: State, event_buffer: EventBuffer) -> None:
        assert event_buffer._buffer == [1, 1]
        event_buffer.clear()

    state = perform_simulation(
        setup_regimen_conditioners=[],
        update_regimen_components=[
            event_enqueue_component,
            event_enqueue_component,
            event_consume_component,
            event_reset_component,
            ApplyIncrementElapsedTime(),
            HaltAfterElapsedTime(1.0),
        ],
    )

    # No simulation components should be changing cell states
    assert State.same_position_as(state, State())
    assert State.same_velocity_as(state, State())


def test_perform_simulation_evaluation():
    evaluation = perform_simulation(
        update_regimen_components=[
            ApplyIncrementElapsedTime(),
            EvaluateDuration(halting_component=HaltAfterElapsedTime(1.0)),
        ],
    )

    assert 1.0 <= evaluation <= 1.0 + defaults.dt
