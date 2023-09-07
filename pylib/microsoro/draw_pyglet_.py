import typing

from pyglet.shapes import Circle as pyg_Circle
from pyglet.graphics import Batch as pyg_Batch

from ..auxlib import resample_color_palette, rgb_reformat_float_to_char
from .State import State
from .Style import Style


def draw_pyglet(
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
    pyg_Batch
        Collection of objects to render.
    """
    if style is None:
        style = Style()

    batch = pyg_Batch()
    # prevent batched shapes from going out of scope
    # see https://stackoverflow.com/q/68109538/17332200
    assert not hasattr(batch, "_handles")
    batch._handles = []

    palette = style.cell_color_palette
    if len(palette) != state.ncells:
        palette = resample_color_palette(palette, state.ncells)

    for x, y, color in zip(state.px.flat, state.py.flat, palette):
        batch._handles.append(
            pyg_Circle(
                x * style.scale,
                y * style.scale,
                style.cell_radius * style.scale,
                batch=batch,
                color=rgb_reformat_float_to_char(color),
            ),
        )

    return batch
