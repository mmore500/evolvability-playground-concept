from datetime import datetime, timedelta
import importlib
import logging
import typing

import pause
from ipycanvas import Canvas as ipy_Canvas
from ipycanvas import hold_canvas as ipy_hold_canvas
from IPython.display import display as IPy_display

from ....auxlib import decorate_with_context
from ...events import EventBuffer, RenderFloorEvent, RenderThresholdEvent
from ...State import State
from ...viz import (
    draw_ipycanvas_State,
    DrawIpycanvasFloor,
    DrawIpycanvasThreshold,
    Style,
)


class ShowAnimationIpycanvas:
    """Simulation component that observes simulation state and animates frames
    from across timesteps within a jupyter notebooks."""

    _canvas: ipy_Canvas
    _next_frame_walltime: datetime
    _style: Style

    def __init__(
        self: "ShowAnimationIpycanvas",
        canvas: typing.Optional[ipy_Canvas] = None,
        style: typing.Optional[Style] = None,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        canvas : ipython.Canvas
            Surface to render to.

            If None, a new Canvas will be initialized and displayed to IPython.
        style : Optional[Style], default=None
            Styling configuration to render state frames.

            If None, default-initialized Style is used.
        """
        if style is None:
            style = Style()
        self._style = style

        if canvas is None:
            frame_width = int(style.xlim_length * style.scale)
            frame_height = int(style.ylim_length * style.scale)
            canvas = ipy_Canvas(height=frame_height, width=frame_width)
            IPy_display(canvas)
        self._canvas = canvas

        self._next_frame_walltime = datetime.now()

    @decorate_with_context(ipy_hold_canvas, idempotify_decorated_context=True)
    def _draw_frame(
        self: "ShowAnimationIpycanvas",
        state: State,
        event_buffer: typing.Optional[EventBuffer],
    ) -> None:
        # self._canvas.clear()
        draw_ipycanvas_State(state, self._canvas, self._style)
        if event_buffer is not None:
            event_buffer.consume(
                RenderFloorEvent,
                DrawIpycanvasFloor(canvas=self._canvas, style=self._style),
                skip_duplicates=True,
            )
            event_buffer.consume(
                RenderThresholdEvent,
                DrawIpycanvasThreshold(canvas=self._canvas, style=self._style),
                skip_duplicates=True,
            ),

    def __call__(
        self: "ShowAnimationIpycanvas",
        state: State,
        event_buffer: typing.Optional[EventBuffer] = None,
    ) -> None:
        """Draw an animation frame."""
        # draw frames at most 20fps ---
        # this way, not every frame has to be drawn
        if self._next_frame_walltime < datetime.now():
            logging.debug("ShowAnimationIpycanvas drawing")
            self._next_frame_walltime = datetime.now() + timedelta(
                seconds=0.05
            )
            self._draw_frame(state, event_buffer)
        else:
            logging.debug("ShowAnimationIpycanvas passing on draw")
