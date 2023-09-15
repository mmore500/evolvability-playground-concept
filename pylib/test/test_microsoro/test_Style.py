import numpy as np
import pytest
import seaborn as sns

from pylib.microsoro import Style


def test_default_init():
    Style()


def test_custom_init():
    custom_palette = sns.color_palette("rocket")
    s = Style(
        background_color=(0.5, 0.5, 0.4),
        cell_alpha=0.5,
        cell_color_palette=custom_palette,
        cell_radius=0.6,
        scale=42.0,
        time_dilation=82.0,
        xlim=(0, 30),
        ylim=(0, 30),
    )
    assert s.background_color == (0.5, 0.5, 0.4)
    assert s.cell_alpha == 0.5
    assert s.cell_radius == 0.6
    assert s.scale == 42.0
    assert s.time_dilation == 82.0
    assert s.xlim == (0, 30)
    assert s.ylim == (0, 30)
    assert s.cell_color_palette == tuple(custom_palette)


def test_xlim_length():
    assert Style(xlim=(5, 30)).xlim_length == 25.0


def test_ylim_length():
    assert Style(ylim=(5, 30)).ylim_length == 25.0


def test_invalid_alpha():
    with pytest.raises(
        ValueError, match="cell_alpha=1.5 not between 0.0 and 1.0"
    ):
        Style(cell_alpha=1.5)


def test_invalid_background_color():
    with pytest.raises(ValueError):
        Style(background_color=(np.nan, 0.0, 0.0))
    with pytest.raises(ValueError):
        Style(background_color=(0.0, 1.0, -0.5))
    with pytest.raises(ValueError):
        Style(background_color=(0.0, 15, 0.5))


def test_invalid_cell_color_palette():
    with pytest.raises(ValueError):
        Style(cell_color_palette=[(0.0, 1.0, 0.5), (np.nan, 0.0, 0.0)])
    with pytest.raises(ValueError):
        Style(cell_color_palette=[(0.0, 1.0, -0.5), (0.5, 0.0, 0.0)])
    with pytest.raises(ValueError):
        Style(cell_color_palette=[(0.0, 1.5, 0.5), (0.5, 0.0, 0.0)])


def test_invalid_radius():
    with pytest.raises(ValueError, match="cell_radius=-0.1 is negative"):
        Style(cell_radius=-0.1)


def test_invalid_scale():
    with pytest.raises(ValueError, match="scale=-1 is negative"):
        Style(scale=-1)


def test_invalid_time_dilation():
    with pytest.raises(ValueError, match="time_dilation=-1 is negative"):
        Style(time_dilation=-1)


def test_invalid_xlim():
    with pytest.raises(ValueError):
        Style(xlim=[0.0])
        Style(xlim=[0.0, 0.0, 0.0])
        Style(xlim=[50.0, -0.5])


def test_invalid_ylim():
    with pytest.raises(ValueError):
        Style(xlim=[0.0])
        Style(xlim=[0.0, 0.0, 0.0])
        Style(xlim=[50.0, -0.5])
