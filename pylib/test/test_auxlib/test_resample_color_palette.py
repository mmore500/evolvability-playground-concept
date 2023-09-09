import numpy as np
import pytest

from pylib.auxlib import resample_color_palette


def test_resample_color_palette_rgba():
    # Define an original palette for testing
    orig_palette = [
        (0.0, 0.0, 0.5, 1.0),
        (0.0, 0.5, 0.0, 0.9),
        (0.5, 0.0, 0.0, 1.0),
    ]

    # Call the function to resample the palette
    resampled_palette = resample_color_palette(orig_palette, 5)

    # Expected resampled palette
    expected_palette = [
        (0.0, 0.0, 0.5, 1.0),
        (0.0, 0.25, 0.25, 0.95),
        (0.0, 0.5, 0.0, 0.9),
        (0.25, 0.25, 0.0, 0.95),
        (0.5, 0.0, 0.0, 1.0),
    ]

    # Check if the resampled palette matches the expected palette
    for i, color in enumerate(resampled_palette):
        np.testing.assert_almost_equal(color, expected_palette[i], decimal=4)


def test_resample_color_palette_rgb():
    # Define an original palette for testing
    orig_palette = [
        (0.0, 0.0, 0.5),
        (0.0, 0.5, 0.0),
        (0.5, 0.0, 0.0),
    ]

    # Call the function to resample the palette
    resampled_palette = resample_color_palette(orig_palette, 5)

    # Expected resampled palette
    expected_palette = [
        (0.0, 0.0, 0.5, 1.0),
        (0.0, 0.25, 0.25, 1.0),
        (0.0, 0.5, 0.0, 1.0),
        (0.25, 0.25, 0.0, 1.0),
        (0.5, 0.0, 0.0, 1.0),
    ]

    # Check if the resampled palette matches the expected palette
    for i, color in enumerate(resampled_palette):
        np.testing.assert_almost_equal(color, expected_palette[i], decimal=4)


def test_empty():
    assert resample_color_palette([], 0) == []
    assert resample_color_palette([(0.0, 0.0, 0.5, 1.0)], 0) == []
    assert resample_color_palette([(0.0, 0.0, 0.5)], 0) == []


def test_singleton():
    assert resample_color_palette([(0.0, 0.0, 0.5, 0.5)], 1) == [
        (0.0, 0.0, 0.5, 0.5),
    ]
    assert resample_color_palette([(0.0, 0.0, 0.5, 0.6)], 2) == [
        (0.0, 0.0, 0.5, 0.6),
        (0.0, 0.0, 0.5, 0.6),
    ]
    assert resample_color_palette([(0.0, 0.0, 0.5)], 1) == [
        (0.0, 0.0, 0.5, 1.0),
    ]
    assert resample_color_palette([(0.0, 0.0, 0.5)], 2) == [
        (0.0, 0.0, 0.5, 1.0),
        (0.0, 0.0, 0.5, 1.0),
    ]
