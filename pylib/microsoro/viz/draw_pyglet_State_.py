import typing

from pyglet.shapes import Circle as pyg_Circle
from pyglet.shapes import Rectangle as pyg_Rectangle
from pyglet.graphics import Batch as pyg_Batch

from ...auxlib import resample_color_palette, rgb_reformat_float_to_char
from ..State import State
from .Style import Style


def draw_pyglet_State(
    state: State,
    style: typing.Optional[Style] = None,
) -> pyg_Batch:
    """Setup pyglet render of state.

    Parameters
    ----------
    state : State
        The state object with current positions of cells.
    style : Style, optional
        The style settings for drawing.

        Defaults to a new Style object if not provided.

    Returns
    -------
    tuple of pyg_Batch and list of pyglet shapes
        Collection of objects to render.

        Shape objects must be passed to prevent deletion when moving out of
        scope.
    """
    if style is None:
        style = Style()

    batch = pyg_Batch()
    batch_handles = []

    batch_handles.append(
        pyg_Rectangle(
            x=0,
            y=0,
            width=style.xlim_length * style.scale,
            height=style.ylim_length * style.scale,
            batch=batch,
            color=rgb_reformat_float_to_char(style.background_color),
        ),
    )

    palette = style.cell_color_palette
    if len(palette) != state.ncells:
        palette = resample_color_palette(palette, state.ncells)

    for x, y, color in zip(state.px.flat, state.py.flat, palette):
        x1, x2 = style.xlim
        y1, y2 = style.ylim
        batch_handles.append(
            pyg_Circle(
                (x - x1) * style.scale,
                (y - y1) * style.scale,
                style.cell_radius * style.scale,
                batch=batch,
                color=rgb_reformat_float_to_char(color),
            ),
        )

    # prevent batched shapes from going out of scope
    # see https://stackoverflow.com/q/68109538/17332200
    # note: adding attribute to batch causes opengl crash
    return batch, batch_handles
