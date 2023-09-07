import pyglet as pyg
import pytest
from unittest.mock import patch, Mock

from pylib.microsoro import apply_translate, draw_pyglet, State, Style


def test_draw_pyglet_mock():

    # Mocking the State and Style classes
    state = State(
        height=1,
        width=3,
    )

    apply_translate(state, dx=1, dy=4)

    style = Style(
        scale=2.0,
        cell_color_palette=[(1, 1, 1, 1), (0, 0, 0, 1)],
        cell_radius=1.0,
    )

    # Mocking pyglet's Circle constructor
    with patch("pylib.microsoro.draw_pyglet_.pyg_Circle") as MockCircle:
        batch = draw_pyglet(state, style)

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
    apply_translate(state, dx=1, dy=4)

    style = Style(
        scale=20.0,
        cell_color_palette=[(1.0, 0, 0, 1.0), (0, 0, 1.0, 0)],
        cell_radius=1.0,
    )

    xlim_width = style.xlim[1] - style.xlim[0]
    ylim_height = style.ylim[1] - style.ylim[0]
    print(xlim_width, ylim_height)
    window = pyg.window.Window(
        width=int(xlim_width * style.scale),
        height=int(ylim_height * style.scale),
        visible=False,
    )

    batch = draw_pyglet(state, style)

    temp_path = "/tmp/test_draw_pyglet.png"

    def save_and_close(dt):
        window.clear()
        batch.draw()
        pyg.image.get_buffer_manager().get_color_buffer().save(temp_path)
        pyg.app.exit()

    pyg.clock.schedule_once(save_and_close, 0)

    pyg.app.run()

    print(f"saved test_draw_pyglet render to file {temp_path}")
    # TODO add background color
