import pytest

from pylib.auxlib import rgb_reformat_float_to_char


def test_rgb_reformat_float_to_char_valid():
    assert rgb_reformat_float_to_char((0.0, 0.0, 0.0)) == (0, 0, 0)
    assert rgb_reformat_float_to_char((1.0, 1.0, 1.0)) == (255, 255, 255)
    assert rgb_reformat_float_to_char((0.5, 0.5, 0.5)) == (127, 127, 127)
    assert rgb_reformat_float_to_char((0.1, 0.2, 0.3)) == (25, 51, 76)
    # RGBA input should work
    assert rgb_reformat_float_to_char((0.5, 0.2, 0.7, 1.0)) == (127, 51, 178)


def test_rgb_reformat_float_to_char_invalid_length():
    with pytest.raises(ValueError):
        rgb_reformat_float_to_char((0.5, 0.2))

    with pytest.raises(ValueError):
        rgb_reformat_float_to_char((0.5, 0.2, 0.7, 0.1, 0.2))


def test_rgb_reformat_float_to_char_invalid_value_range():
    with pytest.raises(ValueError):
        rgb_reformat_float_to_char((-0.1, 0.2, 0.7))

    with pytest.raises(ValueError):
        rgb_reformat_float_to_char((0.5, 1.1, 0.7))

    with pytest.raises(ValueError):
        rgb_reformat_float_to_char(
            (0.5, 0.2, 0.7, -1.0)
        )  # RGBA input with invalid alpha

    with pytest.raises(ValueError):
        rgb_reformat_float_to_char(
            (0.5, 0.2, 0.7, 1.1)
        )  # RGBA input with invalid alpha
