import typing

from pyglet.graphics import Batch as pyg_Batch
from pyglet.shapes import Polygon as pyg_Polygon

from ..events import RenderFloorEvent
from .Style import Style


class DrawPygletFloor:

    _style: Style

    def __init__(
        self: "DrawPygletFloor",
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
        self: "DrawPygletFloor",
        event: RenderFloorEvent,
    ) -> pyg_Batch:
        """Setup pyglet render of floor.

        Parameters
        ----------
        event : RenderFloorEvent
            The event object with floor details.

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

        polygon_points = event.get_underfloor_polygon(
            xlim=self._style.xlim,
            ylim=self._style.ylim,
            scale=self._style.scale,
        )
        color = {
            "floor": (127, 127, 127),
            "viscous layer": (127, 127, 255, 127),
        }[event.flavor]
        if polygon_points:  # pyglet crashes with zero polygon points
            batch_handles.append(
                pyg_Polygon(
                    *polygon_points,
                    batch=batch,
                    color=color,
                ),
            )

        # prevent batched shapes from going out of scope
        # see https://stackoverflow.com/q/68109538/17332200
        # note: adding attribute to batch causes opengl crash
        return batch, batch_handles
