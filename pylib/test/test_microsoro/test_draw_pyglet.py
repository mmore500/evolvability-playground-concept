import contextlib
import os

import pyglet as pyg
from unittest.mock import patch, Mock

from pylib.microsoro import draw_pyglet, State, Style
from pylib.microsoro.conditioners import ApplyTranslate


def test_draw_pyglet_mock():

    # Mocking the State and Style classes
    state = State(
        height=1,
        width=3,
    )

    ApplyTranslate(dpx=1, dpy=4)(state)

    style = Style(
        background_color=(1.0, 1.0, 1.0),
        scale=2.0,
        cell_color_palette=[(1, 1, 1, 1), (0, 0, 0, 1)],
        cell_radius=1.0,
        xlim=(0, 10),
        ylim=(0, 10),
    )

    # Mocking pyglet's Circle constructor
    with patch("pylib.microsoro.draw_pyglet_.pyg_Circle") as MockCircle, patch(
        "pylib.microsoro.draw_pyglet_.pyg_Rectangle"
    ) as MockRectangle:
        batch, __ = draw_pyglet(state, style)

    # Check that pyg_Rectangle is called with expected parameters
    MockRectangle.assert_any_call(
        x=0.0,
        y=0.0,
        width=20.0,
        height=20.0,
        color=(255, 255, 255),
        batch=batch,
    )
    # Check that pyg_Circle is called with expected parameters
    MockCircle.assert_any_call(
        2.0,
        8.0,
        2.0,
        color=(255, 255, 255),
        batch=batch,
    )
    MockCircle.assert_any_call(
        4.0,
        8.0,
        2.0,
        color=(127, 127, 127),
        batch=batch,
    )
    MockCircle.assert_any_call(
        6.0,
        8.0,
        2.0,
        color=(0, 0, 0),
        batch=batch,
    )


def test_draw_pyglet_image():

    state = State(height=1, width=3)
    ApplyTranslate(dpx=1, dpy=4)(state)

    style = Style(
        background_color=(1.0, 1.0, 0.0),
        scale=20.0,
        cell_color_palette=[(1.0, 0, 0, 1.0), (0, 0, 1.0, 0)],
        cell_radius=1.0,
    )

    xlim_width = style.xlim[1] - style.xlim[0]
    ylim_height = style.ylim[1] - style.ylim[0]
    window = pyg.window.Window(
        width=int(xlim_width * style.scale),
        height=int(ylim_height * style.scale),
        visible=False,
    )

    batch, __ = draw_pyglet(state, style)

    outpath = "/tmp/test_draw_pyglet.png"
    with contextlib.suppress(FileNotFoundError):
        os.remove(outpath)

    window.switch_to()
    window.clear()
    batch.draw()
    pyg.image.get_buffer_manager().get_color_buffer().save(outpath)

    print(f"saved test_draw_pyglet render to file {outpath}")
