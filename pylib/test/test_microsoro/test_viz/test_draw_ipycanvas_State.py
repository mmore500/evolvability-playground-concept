import ipycanvas

from pylib.microsoro import State
from pylib.microsoro.viz import draw_ipycanvas_State


# stub test
def test_draw_ipycanvas_State():
    state = State()
    canvas = draw_ipycanvas_State(state)

    # doesn't actually do anything outside jupyter notebook context
    def save_to_file(*args, **kwargs):
        canvas.to_file("/tmp/test_draw_ipycanvas_State.png")

    canvas.observe(save_to_file, "image_data")
