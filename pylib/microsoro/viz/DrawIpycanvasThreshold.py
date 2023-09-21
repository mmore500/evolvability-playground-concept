import typing

from ipycanvas import Canvas as ipy_Canvas
from ipycanvas import hold_canvas as ipy_hold_canvas

from ...auxlib import decorate_with_context
from ..events import RenderThresholdEvent
from .Style import Style


class DrawIpycanvasThreshold:

    _canvas: ipy_Canvas
    _style: Style

    def __init__(
        self: "DrawIpycanvasThreshold",
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
        self: "DrawIpycanvasThreshold",
        event: RenderThresholdEvent,
    ) -> ipy_Canvas:
        """Draw threshold to ipycanvas Canvas.

        Parameters
        ----------
        event : RenderThresholdEvent
            The event object containing threshold details.

        Returns
        -------
        canvas
            ipycanvas Canvas object with threshold illustration.
        """
        coords = event.get_spanning_coordinates(
            xlim=self._style.xlim,
            ylim=self._style.ylim,
            scale=self._style.scale,
        )

        # invert y axis
        sty = self._style
        coords[1] = sty.invert_y_value_renderspace(coords[1])
        coords[3] = sty.invert_y_value_renderspace(coords[3])

        # draw
        hue = {
            "finish": "rgba(0,255,0,1.0)",
        }[event.flavor]
        self._canvas.stroke_style = hue
        self._canvas.stroke_line(*coords)

        return self._canvas
