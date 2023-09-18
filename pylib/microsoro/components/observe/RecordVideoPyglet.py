import typing

import pyglet as pyg
from pyglet.window import Window as pyg_Window

from ....auxlib import ffmpegVideoRenderWorker
from ...events import EventBuffer, RenderFloorEvent
from ...Params import Params
from ...State import State
from ...viz import draw_pyglet_State, DrawPygletFloor, Style


class RecordVideoPyglet:
    """Simulation component that observes simulation state and collates still
    frames from across timesteps into a video animation."""

    _window: pyg_Window
    _worker: ffmpegVideoRenderWorker
    _style: Style

    _last_frame_simtime: float
    _seconds_per_frame: float

    def __init__(
        self: "RecordVideoPyglet",
        output_path: str,
        fps: float = 20,
        style: typing.Optional[Style] = None,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        output_path : str
            Path to save the output video.
        fps : float, default 20
            Frames per second for the video.

        style : Optional[Style], default=None
            Styling configuration to render state frames.

            If None, default-initialized Style is used.
        """
        if style is None:
            style = Style()
        self._style = style

        frame_width = int(style.xlim_length * style.scale)
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

        # ensure at least one frame written to worker
        # to prevent corrupt video files
        self._window.switch_to()
        self._write_frame()

        self._last_frame_simtime = 0.0
        self._seconds_per_frame = 1.0 / fps

    def _render_frame(
        self: "RecordVideoPyglet",
        state: State,
        event_buffer: typing.Optional[EventBuffer],
    ) -> None:
        """Append video frame depicting current state."""
        batch_packets = []
        batch_packets.append(draw_pyglet_State(state, self._style))
        if event_buffer is not None:
            batch_packets.extend(
                event_buffer.consume(
                    RenderFloorEvent,
                    DrawPygletFloor(style=self._style),
                    skip_duplicates=True,
                ),
            )

        self._window.switch_to()
        self._window.clear()
        for batch, __ in batch_packets:
            batch.draw()
        self._write_frame()

    def _write_frame(self: "RecordVideoPyglet") -> None:
        data = (
            pyg.image.get_buffer_manager()
            .get_color_buffer()
            .get_image_data()
            .get_data()
        )
        self._worker.write_frame(data)

    def __call__(
        self: "RecordVideoPyglet",
        state: State,
        event_buffer: typing.Optional[EventBuffer] = None,
    ) -> None:
        """Render frame if scheduled under fps and time dilation settings."""
        time_dilation = self._style.time_dilation
        simtime_since_last_frame = state.t - self._last_frame_simtime
        walltime_since_last_frame = simtime_since_last_frame * time_dilation
        if walltime_since_last_frame >= self._seconds_per_frame:
            self._render_frame(state, event_buffer)
            simtime_step_size = self._seconds_per_frame / time_dilation
            self._last_frame_simtime += simtime_step_size
