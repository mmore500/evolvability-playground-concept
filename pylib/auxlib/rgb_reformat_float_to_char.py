import typing

import numpy as np


def rgb_reformat_float_to_char(color: typing.Tuple) -> typing.Tuple:
    """Convert RGB or RGBA color from float format to char format.

    Parameters
    ----------
    color : tuple or list
        An RGB or RGBA color tuple with float values ranging from 0.0 to 1.0.

        Example: (0.5, 0.2, 0.7) or (0.5, 0.2, 0.7, 1.0)

    Returns
    -------
    Tuple[int, int, int]
        A tuple of integers representing the RGB color components, each ranging from 0 to 255.
    """

    # Validate and truncate the color tuple to just RGB components if RGBA is passed
    if len(color) not in [3, 4]:
        raise ValueError(f"Input {color=} must be an RGB or RGBA tuple.")

    if not all(0.0 <= val <= 1.0 for val in color):
        raise ValueError(f"Input {color=} values must be in [0.0, 1.0].")

    return tuple(int(val * 255) for val in color[:3])
