import pyglet as pyg
from pyglet.window import Window as pyg_Window
import typing

from ...auxlib import ffmpegVideoRenderWorker
from ..draw_pyglet_ import draw_pyglet
from ..Params import Params
from ..State import State
from ..Style import Style


class RecordVideoPyglet:
    """Simulation component that observes simulation state and collates still
    frames from across timesteps into a video animation."""

    _window: pyg_Window
    _worker: ffmpegVideoRenderWorker
    _style: Style

    def __init__(
        self: "RecordVideoPyglet",
        output_path: str,
        fps: typing.Optional[typing.Union[float, Params]] = None,
        style: typing.Optional[Style] = None,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        output_path : str
            Path to save the output video.
        fps : Optional[Union[float, Params]], default=None
            Frames per second for the video.

            If Params object is passed, fps is set to inverse its dt attribute If None, default-initialized Params object is used.
        style : Optional[Style], default=None
            Styling configuration to render state frames.

            If None, default-initialized Style is used.
        """
        if style is None:
            style = Style()
        self._style = style

        if fps is None:
            fps = Params()
        if isinstance(fps, Params):
            fps = 1 / fps.dt

        frame_width = int(style.ylim_length * style.scale)
        frame_height = int(style.ylim_length * style.scale)

        self._window = pyg.window.Window(
            width=frame_width, height=frame_height, visible=False
        )
        self._worker = ffmpegVideoRenderWorker(
            output_path=output_path,
            fps=fps,
            frame_width=frame_width,
            frame_height=frame_height,
        )

    def __call__(self: "RecordVideoPyglet", state: State) -> None:
        """Append video frame depicting current state."""
        batch, __ = draw_pyglet(state, self._style)

        window = self._window
        window.switch_to()
        window.clear()
        batch.draw()
        data = (
            pyg.image.get_buffer_manager()
            .get_color_buffer()
            .get_image_data()
            .get_data()
        )
        self._worker.write_frame(data)
