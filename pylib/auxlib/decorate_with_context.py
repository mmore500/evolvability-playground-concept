import functools
import typing


def decorate_with_context(
    context_manager_factory: typing.Callable,
) -> typing.Callable:
    """Decorate a function to run within an instance of the given context
    manager.

    Parameters
    ----------
    context_manager_factory : Callable[[...], ContextManager]
        The context manager with which to decorate the function.

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

    def decorator(func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> typing.Any:
            with context_manager_factory():
                return func(*args, **kwargs)

        return wrapper

    return decorator
