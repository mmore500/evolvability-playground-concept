import functools
import typing

import numpy as np
import matplotlib.colors as mcolors

from .ignore_unhashable import ignore_unhashable


@ignore_unhashable
@functools.lru_cache()
def resample_color_palette(
    palette: typing.List[typing.Tuple],
    n: int,
) -> typing.List[typing.Tuple[float, float, float, float]]:
    """Interpolate n entries from a given color palette.

    Parameters
    ----------
    palette : Union[
        List[Tuple[float, float, float]],
        List[Tuple[float, float, float, float]],
    ]
        The original color palette represented as a list of RGB or RGBA tuples.

        Each tuple contains four float values ranging from 0 to 1.
    n : int
        The number of colors desired in the resampled palette.

    Returns
    -------
    List[Tuple[float, float, float, float]]
        The resampled palette represented as a list of RGBA tuples.

    Examples
    --------
    >>> orig_palette = [
        (0.0, 0.0, 0.5, 1.0),
        (0.0, 0.5, 0.0, 1.0),
        (0.5, 0.0, 0.0, 1.0),
    ]
    >>> resample_palette(orig_palette, 5)
    [(0.0, 0.0, 0.5, 1.0), (0.0, 0.25, 0.25, 1.0), (0.0, 0.5, 0.0, 1.0), (0.25, 0.25, 0.0, 1.0), (0.5, 0.0, 0.0, 1.0)]
    """
    assert n >= 0
    if n == 0:
        return []

    orig_palette = np.array(palette)
    new_palette = np.linspace(0, 1, n)

    r = np.interp(
        new_palette,
        np.linspace(0, 1, len(orig_palette)),
        orig_palette[:, 0],
    )
    g = np.interp(
        new_palette,
        np.linspace(0, 1, len(orig_palette)),
        orig_palette[:, 1],
    )
    b = np.interp(
        new_palette,
        np.linspace(0, 1, len(orig_palette)),
        orig_palette[:, 2],
    )
    try:
        a = np.interp(
            new_palette,
            np.linspace(0, 1, len(orig_palette)),
            orig_palette[:, 3],
        )
    except IndexError:
        a = np.ones(n)

    return [(r[i], g[i], b[i], a[i]) for i in range(len(r))]
