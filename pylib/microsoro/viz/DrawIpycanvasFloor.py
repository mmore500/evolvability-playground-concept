import typing

from ipycanvas import Canvas as ipy_Canvas
from ipycanvas import hold_canvas as ipy_hold_canvas

from ...auxlib import decorate_with_context
from ..events import RenderFloorEvent
from .Style import Style


class DrawIpycanvasFloor:

    _canvas: ipy_Canvas
    _style: Style

    def __init__(
        self: "DrawIpycanvasFloor",
        canvas: typing.Optional[ipy_Canvas] = None,
        style: typing.Optional[Style] = None,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        canvas : ipycanvas.Canvas, optional
            The surface to draw to.

            If not provided, a new Canvas object will be created.
        style : Style, optional
            The style settings for drawing.

            Defaults to a new Style object if not provided.
        """
        if style is None:
            style = Style()
        self._style = style

        if canvas is None:
            frame_width = int(style.xlim_length * style.scale)
            frame_height = int(style.ylim_length * style.scale)
            canvas = ipy_Canvas(height=frame_height, width=frame_width)
        self._canvas = canvas

    @decorate_with_context(ipy_hold_canvas, idempotify_decorated_context=True)
    def __call__(
        self: "DrawIpycanvasFloor",
        event: RenderFloorEvent,
    ) -> ipy_Canvas:
        """Draw floor to ipycanvas Canvas.

        Parameters
        ----------
        event : RenderFloorEvent
            The event object containing floor details.

        Returns
        -------
        canvas
            ipycanvas Canvas object with floor illustration.
        """
        sty = self._style
        polygon_points = event.get_underfloor_polygon(
            xlim=sty.xlim,
            ylim=sty.ylim,
            scale=sty.scale,
        )
        # origin is in upper left corner on HTML canvas
        inverted_polygon_points = [
            (x, sty.invert_y_value_renderspace(y)) for x, y in polygon_points
        ]

        hue = {
            "floor": "rgba(127,127,127,1.0)",
            "viscous layer": "rgba(127,127,255,0.3)",
        }[event.flavor]
        self._canvas.fill_style = hue
        self._canvas.stroke_style = hue
        self._canvas.fill_polygon(inverted_polygon_points)
        self._canvas.fill_rect(2, 2, 2, 2)

        return self._canvas
