import typing

from ipycanvas import Canvas as ipy_Canvas
from ipycanvas import hold_canvas as ipy_hold_canvas
import numpy as np

from ..auxlib import (
    decorate_with_context,
    resample_color_palette,
    rgb_reformat_float_to_char,
)

from .State import State
from .Style import Style


@decorate_with_context(ipy_hold_canvas, idempotify_decorated_context=True)
def draw_ipycanvas(
    state: State,
    canvas: typing.Optional[ipy_Canvas] = None,
    style: typing.Optional[Style] = None,
) -> ipy_Canvas:
    """Render state to ipycanvas Canvas.

    Parameters
    ----------
    state : State
        The state object with current positions of cells.
    canvas : ipycanvas.Canvas, optional
        The surface to draw to.

        If not provided, a new Canvas object will be created.
    style : Style, optional
        The style settings for drawing.

        Defaults to a new Style object if not provided.

    Returns
    -------
    canvas
        ipycanvas Canvas object with State illustration.
    """
    if style is None:
        style = Style()
    if canvas is None:
        frame_width = int(style.xlim_length * style.scale)
        frame_height = int(style.ylim_length * style.scale)
        canvas = ipy_Canvas(height=frame_height, width=frame_width)

    canvas.clear()

    # add background color
    canvas.stroke_style = "gray"

    # prep palette
    palette = [*map(rgb_reformat_float_to_char, style.cell_color_palette)]
    if len(palette) != state.ncells:
        palette = resample_color_palette(palette, state.ncells)
    palette = np.array(palette)[:, :3]

    # prep cell positions
    xs, ys = state.px.flatten(), state.py.flatten()
    xmin, xmax = style.xlim
    ymin, ymax = style.ylim

    # draw cells
    canvas.fill_styled_circles(
        (xs - xmin) * style.scale,
        canvas.height - (ys - ymin) * style.scale,
        0.4 * style.scale,
        color=palette,
        alpha=style.cell_alpha,
    )
    canvas.stroke_circles(
        (xs - xmin) * style.scale,
        canvas.height - (ys - ymin) * style.scale,
        0.4 * style.scale,
    )

    return canvas
