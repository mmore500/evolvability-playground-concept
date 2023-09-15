import ipycanvas

from pylib import microsoro


# stub test
def test_draw_ipycanvas():
    state = microsoro.State()
    canvas = microsoro.draw_ipycanvas(state)

    # doesn't actually do anything outside jupyter notebook context
    def save_to_file(*args, **kwargs):
        canvas.to_file("/tmp/test_draw_ipycanvas.png")

    canvas.observe(save_to_file, "image_data")
