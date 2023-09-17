import contextlib
import typing

import pytest

from pylib.auxlib import decorate_with_context


@contextlib.contextmanager
def dummy_context(state: typing.Dict) -> typing.Iterable:
    state["context_active"] = True
    state["invocation_count"] += 1
    yield
    state["context_active"] = False


@pytest.fixture
def state():
    return {"context_active": False, "invocation_count": 0}


def test_without_idempotency(state: typing.Dict):
    @decorate_with_context(lambda: dummy_context(state))
    def sample_function():
        assert state["context_active"] == True

    sample_function()
    assert state["context_active"] == False
    assert state["invocation_count"] == 1


def test_with_idempotency_without_nested_call(state: typing.Dict):
    @decorate_with_context(
        lambda: dummy_context(state), idempotify_decorated_context=True
    )
    def sample_function_idempotent():
        assert state["context_active"] == True

    sample_function_idempotent()
    assert state["context_active"] == False
    assert state["invocation_count"] == 1


@pytest.mark.parametrize("idempotify", [True, False])
def test_with_idempotency_with_nested_call(
    state: typing.Dict, idempotify: bool
):
    dummy_context_factory = lambda: dummy_context(state)

    @decorate_with_context(
        dummy_context_factory, idempotify_decorated_context=idempotify
    )
    def sample_function_idempotent():
        assert state["context_active"] == True

        # Nested invocation
        @decorate_with_context(
            dummy_context_factory, idempotify_decorated_context=idempotify
        )
        def nested_function():
            assert state["context_active"] == True

        nested_function()

    sample_function_idempotent()
    assert state["context_active"] == False
    assert state["invocation_count"] == 1 + (not idempotify)
