import pytest
import numpy as np

from pylib.auxlib import all_rows_equivalent


def test_identical_rows():
    a = np.array(
        [
            [1, 2, 3, 0],
            [1, 2, 3, 0],
            [1, 2, 3, 0],
        ]
    )
    assert all_rows_equivalent(a) is True


def test_near_identical_rows():
    b = np.array(
        [
            [1, 2, 3],
            [1, 2, 3 + 1e-12],
            [1, 2, 3],
        ]
    )
    assert all_rows_equivalent(b) is True


def test_different_rows():
    # Test with different rows
    c = np.array(
        [
            [1, 1, 1],
            [4, 5, 6],
            [7, 8, 9],
        ]
    )
    assert all_rows_equivalent(c) is False


def test_single_row():
    c = np.array(
        [
            [1, 1, 2],
        ]
    )
    assert all_rows_equivalent(c) is True


def test_empty():
    # Test with empty array
    d = np.array([[]])
    assert all_rows_equivalent(d) is True


def test_1d():
    # Test with 1D array (should raise a ValueError due to np.diff's axis=0)
    e = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        all_rows_equivalent(e)
