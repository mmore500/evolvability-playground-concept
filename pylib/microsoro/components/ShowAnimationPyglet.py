from datetime import datetime, timedelta
import importlib
import logging
import typing

import pause
import pyglet as pyg
from pyglet.window import Window as pyg_Window

from ...auxlib import HaltToken
from ..draw_pyglet_ import draw_pyglet
from ..State import State
from ..Style import Style


class ShowAnimationPyglet:
    """Simulation component that observes simulation state and animates frames
    from across timesteps in a popup window."""

    _next_frame_walltime: datetime
    _style: Style
    _window: pyg_Window

    def __init__(
        self: "ShowAnimationPyglet",
        style: typing.Optional[Style] = None,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        style : Optional[Style], default=None
            Styling configuration to render state frames.

            If None, default-initialized Style is used.
        """
        if style is None:
            style = Style()
        self._style = style

        self._next_frame_walltime = datetime.now()

        frame_width = int(style.ylim_length * style.scale)
        frame_height = int(style.ylim_length * style.scale)
        self._window = pyg_Window(
            width=frame_width, height=frame_height, visible=True
        )

    def __call__(self: "ShowAnimationPyglet", state: State) -> None:
        """Draw an animation frame."""
        # draw frames at most 20fps ---
        # this way, not every frame has to be drawn
        if self._next_frame_walltime < datetime.now():
            logging.debug("ShowAnimationPyglet drawing")
            self._next_frame_walltime = datetime.now() + timedelta(
                seconds=0.05
            )
            batch, __ = draw_pyglet(state, self._style)
            self._window.switch_to()
            self._window.clear()
            batch.draw()
            self._window.flip()

        else:
            logging.debug("ShowAnimationPyglet passing on draw")
