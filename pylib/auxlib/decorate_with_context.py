import contextlib
import functools
import threading
import typing


def decorate_with_context(
    context_manager_factory: typing.Callable,
    idempotify_decorated_context: bool = False,
    *,
    # active context manager factory ids
    # global state shared across all calls to decorate_with_context
    _active_ids: typing.Set[int] = set(),
) -> typing.Callable:
    """Decorate a function to run within an instance of the given context
    manager.

    Parameters
    ----------
    context_manager_factory : Callable[[...], ContextManager]
        The context manager with which to decorate the function.

    idempotify_decorated_context: bool, default False
        Should invocations of context_manager_factory be tracked and only one
        live invocation allowed at any one time?

    Returns
    -------
    Callable[[T], T]
        The decorator to apply to the function.

    Examples
    --------
    >>> @decorate_with_context(hold_canvas)
    ... def my_function():
    ...     # ... function body ...

    Notes
    -----
    Context manager constructor arguments are not supported.
    """

    cmf_id = id(context_manager_factory)

    def decorator(func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> typing.Any:
            context: typing.Callable
            # no idempotency concerns
            if not idempotify_decorated_context:
                context = context_manager_factory
            # if idempotency enforced and factory is live, do no-op
            elif cmf_id in _active_ids:
                assert idempotify_decorated_context
                context = contextlib.nullcontext
            # if idempotency enforced and factory is not live, mark live
            else:
                assert idempotify_decorated_context

                @contextlib.contextmanager
                def context() -> typing.Iterable:
                    with context_manager_factory():
                        try:
                            _active_ids.add(cmf_id)
                            yield
                        finally:
                            _active_ids.discard(cmf_id)

            with context():
                return func(*args, **kwargs)

        return wrapper

    return decorator
