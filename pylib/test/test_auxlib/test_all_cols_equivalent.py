import pytest
import numpy as np

from pylib.auxlib import all_cols_equivalent


def test_identical_cols():
    a = np.array(
        [
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3],
            [0, 0, 0],
        ]
    )
    assert all_cols_equivalent(a) is True


def test_near_identical_cols():
    b = np.array(
        [
            [1, 1, 1],
            [2, 2, 2],
            [3, 3 + 1e-12, 3],
        ]
    )
    assert all_cols_equivalent(b) is True


def test_different_cols():
    # Test with different cols
    c = np.array(
        [
            [1, 4, 7],
            [1, 5, 8],
            [1, 6, 9],
        ]
    )
    assert all_cols_equivalent(c) is False


def test_single_col():
    c = np.array(
        [
            [1],
            [1],
            [2],
        ]
    )
    assert all_cols_equivalent(c) is True


def test_empty():
    # Test with empty array
    d = np.array([[]])
    assert all_cols_equivalent(d) is True


def test_1d():
    # Test with 1D array (should raise a ValueError due to np.diff's axis=0)
    e = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        all_cols_equivalent(e)
