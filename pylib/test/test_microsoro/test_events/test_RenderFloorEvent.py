import typing

import pytest

from pylib.microsoro.events import RenderFloorEvent


def _scaleup(
    points: typing.List[typing.Tuple[float, float]],
    scale: float,
) -> typing.List[typing.Tuple[float, float]]:
    return [tuple(map(lambda x: x * scale, point)) for point in points]


def test_render_floor_event_properties():
    event = RenderFloorEvent(m=2.0, b=1.0)
    assert event.m == 2.0
    assert event.b == 1.0


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_positive_slope(scale: float):
    event = RenderFloorEvent(m=2.0, b=1.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 5), (0, 10), scale, invert_y=False
    )
    expected_points = _scaleup([(0, 0), (0, 1), (5, 11), (5, 0)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_negative_slope(scale: float):
    event = RenderFloorEvent(m=-1.0, b=24.0)
    polygon_points = event.get_underfloor_polygon(
        (5, 10), (10, 20), scale, invert_y=False
    )
    expected_points = _scaleup([(0, 0), (0, 9), (5, 4), (5, 0)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_zero_slope(scale: float):
    event = RenderFloorEvent(m=0.0, b=5.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 5), (0, 10), scale, invert_y=False
    )
    expected_points = _scaleup([(0, 0), (0, 5), (5, 5), (5, 0)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_with_b1_less_than_y1(scale: float):
    event = RenderFloorEvent(m=0.5, b=-1.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 6), (0, 10), scale, invert_y=False
    )
    expected_points = _scaleup([(0, -1), (6, 2), (6, 0)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_with_b2_less_than_y1(scale: float):
    event = RenderFloorEvent(m=-0.5, b=1.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 6), (0, 10), scale, invert_y=False
    )
    expected_points = _scaleup([(0, 0), (0, 1), (6, -2)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
@pytest.mark.parametrize("slope", [1.0, -0.5, 0.0])
def test_get_underfloor_polygon_out_of_frame(scale: float, slope: float):
    event = RenderFloorEvent(m=slope, b=-5000.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 5), (0, 10), scale, invert_y=False
    )
    expected_points = []
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_positive_slope_inverty(scale: float):
    event = RenderFloorEvent(m=2.0, b=1.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 5), (0, 10), scale, invert_y=True
    )
    expected_points = _scaleup([(0, 10), (0, 9), (5, -1), (5, 10)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_negative_slope_inverty(scale: float):
    event = RenderFloorEvent(m=-1.0, b=24.0)
    polygon_points = event.get_underfloor_polygon(
        (5, 10), (10, 20), scale, invert_y=True
    )
    expected_points = _scaleup([(0, 10), (0, 1), (5, 6), (5, 10)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_zero_slope_inverty(scale: float):
    event = RenderFloorEvent(m=0.0, b=5.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 5), (0, 10), scale, invert_y=True
    )
    expected_points = _scaleup([(0, 10), (0, 5), (5, 5), (5, 10)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_with_b1_less_than_y1_inverty(scale: float):
    event = RenderFloorEvent(m=0.5, b=-1.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 6), (0, 10), scale, invert_y=True
    )
    expected_points = _scaleup([(0, 11), (6, 8), (6, 10)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
def test_get_underfloor_polygon_with_b2_less_than_y1_inverty(scale: float):
    event = RenderFloorEvent(m=-0.5, b=1.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 6), (0, 10), scale, invert_y=True
    )
    expected_points = _scaleup([(0, 10), (0, 9), (6, 12)], scale)
    assert polygon_points == expected_points


@pytest.mark.parametrize("scale", [1.0, 0.5, 2.0])
@pytest.mark.parametrize("slope", [1.0, -0.5, 0.0])
def test_get_underfloor_polygon_out_of_frame_inverty(
    scale: float, slope: float
):
    event = RenderFloorEvent(m=slope, b=-5000.0)
    polygon_points = event.get_underfloor_polygon(
        (0, 5), (0, 10), scale, invert_y=True
    )
    expected_points = []
    assert polygon_points == expected_points
