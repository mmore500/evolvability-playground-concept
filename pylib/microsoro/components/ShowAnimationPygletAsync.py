from datetime import datetime, timedelta
import logging
from multiprocessing import Process as mp_Process
from multiprocessing import JoinableQueue as mp_Queue
import typing

import pause
import pyglet as pyg
from pyglet.window import Window as pyg_Window

from ...auxlib import HaltToken
from ..draw_pyglet_ import draw_pyglet
from ..State import State
from ..Style import Style


def _calculate_scheduled_walltime(
    simtime: float, walltime_epoch: datetime, time_dilation: float
) -> datetime:
    """When in realtime is the simulation state at simtime scheduled to be
    rendered?"""
    return walltime_epoch + timedelta(seconds=simtime * time_dilation)


class _ShowAnimationPygletRenderJob(mp_Process):
    """Worker process to asynchronously render animation window."""

    _window: typing.Optional[pyg_Window]
    _style: Style
    # queue provides State stream from paren tprocess
    _queue: mp_Queue  # [typing.Optional[State]]

    # when was the first frame drawn? used to time subsequent frames
    _walltime_epoch: typing.Optional[datetime]

    def __init__(
        self: "_ShowAnimationPygletRenderJob", style: Style, queue: mp_Queue
    ) -> None:
        """Setup, called on parent process."""
        # call Process init
        super().__init__(daemon=True, name="_ShowAnimationPygletRenderJob")

        self._style = style
        self._queue = queue
        self._window = None
        frame_width = int(style.ylim_length * style.scale)
        frame_height = int(style.ylim_length * style.scale)
        self._window = pyg_Window(
            width=frame_width, height=frame_height, visible=True
        )
        self._walltime_epoch = None

    # customizes process kickoff by overriding mp_Process's run()
    # (an ok thing to do, according to official python docs)
    def run(self: "_ShowAnimationPygletRenderJob") -> None:
        """Called on launched child process."""
        logging.debug("_ShowAnimationPygletRenderJob run begin")

        pause.seconds(0.5)  # allow queue to populate
        self._walltime_epoch = datetime.now()
        logging.debug("ShowAnimationPyglet run_init complete")

        # work loop
        while True:
            logging.debug("_ShowAnimationPygletRenderJob getting from queue")
            state = self._queue.get(block=True)  # blocking get
            logging.debug("_ShowAnimationPygletRenderJob got from queue")

            # sentinel value, work is all done
            if isinstance(state, HaltToken):
                logging.debug(
                    "_ShowAnimationPygletRenderJob halt token received."
                )
                self._queue.task_done()
                break

            # if we're behind schedule, consider skipping a render
            state_scheduled_walltime = _calculate_scheduled_walltime(
                state.t, self._walltime_epoch, self._style.time_dilation
            )
            if (
                datetime.now() > state_scheduled_walltime
                and self._queue.qsize()  # simulation isn't bottleneck
            ):
                # discard state and try to catch up
                self._queue.task_done()
                logging.debug("_ShowAnimationPygletRenderJob skipped render")
                continue
            else:
                # wait until next scheduled frame then render
                pause.until(state_scheduled_walltime)
                logging.debug(
                    "_ShowAnimationPygletRenderJob drawing to window"
                )
                batch, __ = draw_pyglet(state, self._style)
                self._window.switch_to()
                self._window.clear()
                batch.draw()
                self._window.flip()
                self._queue.task_done()
                logging.debug("_ShowAnimationPygletRenderJob draw complete")
                continue

        logging.debug("_ShowAnimationPygletRenderJob run complete")


class ShowAnimationPygletAsync:
    """Simulation component that observes simulation state and animates frames
    from across timesteps in a popup window.

    Rendering performed in subprocess.

    Note: on Linux, pyglet crashes on calls after first instantiations of this
    functor due to OpenGL threading issues.
    """

    _render_worker: _ShowAnimationPygletRenderJob
    _queue: mp_Queue  # [typing.Optional[State]]
    _next_frame_walltime: datetime

    def __init__(
        self: "ShowAnimationPygletAsync",
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

        self._next_frame_walltime = datetime.now()
        self._queue = mp_Queue()
        self._render_worker = ShowAnimationPygletRenderJob(
            style=style, queue=self._queue
        )
        self._render_worker.start()

    def __del__(self: "ShowAnimationPygletAsync") -> None:
        """Cleanup."""
        self._queue.put(HaltToken())  # send sentinel value to break work loop
        logging.debug("ShowAnimationPygletAsync joining render worker")
        self._render_worker.join()

    def __call__(self: "ShowAnimationPygletAsync", state: State) -> None:
        """Add a frame to the render queue."""
        # put frames on the render queue no more often than 20fps
        if self._next_frame_walltime < datetime.now():
            logging.debug("ShowAnimationPygletAsync putting on queue")
            self._queue.put_nowait(state)
            self._next_frame_walltime = datetime.now() + timedelta(
                seconds=0.05
            )
        else:
            logging.debug("ShowAnimationPygletAsync passing on put")
