import pytest
import seaborn as sns

from pylib.microsoro import Style


def test_default_init():
    Style()


def test_custom_init():
    custom_palette = sns.color_palette("rocket")
    s = Style(
        cell_alpha=0.5,
        cell_color_palette=custom_palette,
        cell_radius=0.6,
        xlim=(0, 30),
        ylim=(0, 30),
    )
    assert s.cell_alpha == 0.5
    assert s.cell_radius == 0.6
    assert s.xlim == (0, 30)
    assert s.ylim == (0, 30)
    assert s.cell_color_palette == custom_palette


def test_invalid_alpha():
    with pytest.raises(
        ValueError, match="cell_alpha=1.5 not between 0.0 and 1.0"
    ):
        Style(cell_alpha=1.5)


def test_invalid_radius():
    with pytest.raises(ValueError, match="cell_radius=-0.1 is negative"):
        Style(cell_radius=-0.1)
