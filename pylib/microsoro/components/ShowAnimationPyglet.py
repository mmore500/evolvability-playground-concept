from datetime import datetime, timedelta
import importlib
import logging
import typing

import pause
import pyglet as pyg
from pyglet.window import Window as pyg_Window

from ..draw_pyglet_ import draw_pyglet
from ..DrawPygletFloor import DrawPygletFloor
from ..events import EventBuffer, RenderFloorEvent
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

        frame_width = int(style.xlim_length * style.scale)
        frame_height = int(style.ylim_length * style.scale)
        self._window = pyg_Window(
            width=frame_width, height=frame_height, visible=True
        )

    def __call__(
        self: "ShowAnimationPyglet",
        state: State,
        event_buffer: typing.Optional[EventBuffer] = None,
    ) -> None:
        """Draw an animation frame."""
        # draw frames at most 20fps ---
        # this way, not every frame has to be drawn
        if self._next_frame_walltime < datetime.now():
            logging.debug("ShowAnimationPyglet drawing")
            self._next_frame_walltime = datetime.now() + timedelta(
                seconds=0.05
            )
            batch_packets = []
            batch_packets.append(draw_pyglet(state, self._style))
            if event_buffer is not None:
                batch_packets.extend(
                    event_buffer.consume(
                        RenderFloorEvent,
                        DrawPygletFloor(style=self._style),
                        skip_duplicates=True,
                    ),
                )
                print(batch_packets)

            self._window.switch_to()
            self._window.clear()
            for batch, __ in batch_packets:
                batch.draw()
            self._window.flip()

        else:
            logging.debug("ShowAnimationPyglet passing on draw")
