import typing

from pyglet.graphics import Batch as pyg_Batch
from pyglet.shapes import Line as pyg_Line

from ..events import RenderThresholdEvent
from .Style import Style


class DrawPygletThreshold:

    _style: Style

    def __init__(
        self: "DrawPygletThreshold",
        style: typing.Optional[Style] = None,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        style : Style, optional
            The style settings for drawing.

            Defaults to a new Style object if not provided.
        """
        if style is None:
            style = Style()
        self._style = style

    def __call__(
        self: "DrawPygletThreshold",
        event: RenderThresholdEvent,
    ) -> pyg_Batch:
        """Setup pyglet render of threshold.

        Parameters
        ----------
        event : RenderThresholdEvent
            The event object with threshold details.

        Returns
        -------
        tuple of pyg_Batch and list of pyglet shapes
            Collection of objects to render.

            Shape objects must be passed to prevent deletion when moving out of
            scope.
        """
        style = self._style
        batch = pyg_Batch()
        batch_handles = []

        coords = event.get_spanning_coordinates(
            xlim=self._style.xlim,
            ylim=self._style.ylim,
            scale=self._style.scale,
        )
        color = {
            "finish": (0, 255, 0),
        }[event.flavor]
        batch_handles.append(
            pyg_Line(*coords, batch=batch, color=color),
        )

        # prevent batched shapes from going out of scope
        # see https://stackoverflow.com/q/68109538/17332200
        # note: adding attribute to batch causes opengl crash
        return batch, batch_handles
