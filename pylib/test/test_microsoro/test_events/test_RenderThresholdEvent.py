import typing

import pytest

from pylib.microsoro.events import RenderThresholdEvent


def _scaleup(
    points: typing.List[float],
    scale: float,
) -> typing.List[float]:
    return list(map(lambda v: v * scale, points))


def test_render_threshold_event_properties():
    event = RenderThresholdEvent(m=2.0, b=1.0, independent_axis="horizontal")
    assert event.m == 2.0
    assert event.b == 1.0
    assert event.independent_axis == "horizontal"
    assert event.flavor


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_spanning_coordinates_horizontal(scale: float):
    event = RenderThresholdEvent(m=2.0, b=1.0, independent_axis="horizontal")
    coords = event.get_spanning_coordinates((-1, 5), (0, 10), scale)
    expected_coords = _scaleup([0, -1, 6, 11], scale)
    assert coords == expected_coords


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_spanning_coordinates_vertical(scale: float):
    event = RenderThresholdEvent(m=0.0, b=1.0, independent_axis="vertical")
    coords = event.get_spanning_coordinates((-1, 5), (0, 10), scale)
    expected_coords = _scaleup([2, 0, 2, 10], scale)
    assert coords == expected_coords
