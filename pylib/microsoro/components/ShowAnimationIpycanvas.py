from datetime import datetime, timedelta
import importlib
import logging
import typing

import pause
from ipycanvas import Canvas as ipy_Canvas
from IPython.display import display as IPy_display

from ..draw_ipycanvas import draw_ipycanvas
from ..State import State
from ..Style import Style


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

    def __call__(self: "ShowAnimationIpycanvas", state: State) -> None:
        """Draw an animation frame."""
        # draw frames at most 20fps ---
        # this way, not every frame has to be drawn
        if self._next_frame_walltime < datetime.now():
            logging.debug("ShowAnimationIpycanvas drawing")
            self._next_frame_walltime = datetime.now() + timedelta(
                seconds=0.05
            )
            draw_ipycanvas(state, self._canvas, self._style)
        else:
            logging.debug("ShowAnimationIpycanvas passing on draw")
