import functools

from pylib.auxlib import ignore_unhashable


# Define the example_func function for testing
@ignore_unhashable
@functools.lru_cache()
def example_func(lst):
    return sum(lst) + max(lst) + min(lst)


def test_ignore_unhashable():
    # Test with list (unhashable type)
    assert example_func([1, 2]) == 6
    assert (
        repr(example_func.cache_info())
        == "CacheInfo(hits=0, misses=0, maxsize=128, currsize=0)"
    )

    # Test with tuple (hashable type)
    assert example_func((1, 2)) == 6
    assert (
        repr(example_func.cache_info())
        == "CacheInfo(hits=0, misses=1, maxsize=128, currsize=1)"
    )

    # Test cache hit with tuple
    assert example_func((1, 2)) == 6
    assert (
        repr(example_func.cache_info())
        == "CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)"
    )
