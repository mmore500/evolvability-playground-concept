import functools
import typing


# adapted from https://stackoverflow.com/a/64111268
def ignore_unhashable(func: typing.Callable) -> typing.Callable:
    """Decorator that makes functools.lru_cache robust calls with unhashable
    arguments.

    This decorator catches the TypeError that occurs when an unhashable argument
    is passed to an lru_cache-decorated function. In such cases, it falls back
    to calling the original (uncached) function.

    Parameters
    ----------
    func : callable
        A function that has been decorated with functools.lru_cache.

    Returns
    -------
    callable
        A wrapped function that behaves the same as the original function
        but ignores cache operations for unhashable arguments.

    Examples
    --------
    @ignore_unhashable
    @functools.lru_cache()
    def example_func(lst):
        return sum(lst) + max(lst) + min(lst)

    >>> example_func([1, 2])
    6
    >>> example_func((1, 2))
    6
    """
    uncached = func.__wrapped__
    attributes = functools.WRAPPER_ASSIGNMENTS + ("cache_info", "cache_clear")

    @functools.wraps(func, assigned=attributes)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as error:
            if "unhashable type" in str(error):
                return uncached(*args, **kwargs)
            raise

    wrapper.__uncached__ = uncached
    return wrapper
